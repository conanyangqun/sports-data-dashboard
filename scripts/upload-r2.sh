#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

DATA_FILE="${1:-}"
if [ -z "$DATA_FILE" ]; then
  DATA_FILE="$PROJECT_ROOT/data.json"
fi

if [ ! -f "$DATA_FILE" ]; then
  echo "❌ 文件不存在: $DATA_FILE"
  echo ""
  echo "   用法: $0 [data.json路径]"
  echo "   示例: $0 ~/my-sports-data.json"
  exit 1
fi

FILE_SIZE=$(du -k "$DATA_FILE" | cut -f1)
FILE_SIZE_HUMAN=$(du -h "$DATA_FILE" | cut -f1)
echo "📁 文件: $DATA_FILE ($FILE_SIZE_HUMAN)"

echo ""
echo "═══════════════════════════════════════════"
echo "  Cloudflare R2 data.json 上传工具"
echo "═══════════════════════════════════════════"
echo ""

DETECT_METHOD=""

if command -v wrangler &>/dev/null; then
  DETECT_METHOD="wrangler"
elif command -v rclone &>/dev/null; then
  DETECT_METHOD="rclone"
elif command -v aws &>/dev/null; then
  DETECT_METHOD="aws-cli"
elif command -v curl &>/dev/null; then
  DETECT_METHOD="curl"
else
  echo "❌ 未检测到可用的上传工具，请安装其中之一:"
  echo "   1. wrangler (推荐): npm install -g wrangler"
  echo "   2. rclone:         brew install rclone"
  echo "   3. aws-cli:        brew install awscli"
  exit 1
fi

echo "🔧 检测到工具: $DETECT_METHOD"

case "$DETECT_METHOD" in
  wrangler)
    R2_BUCKET="${R2_BUCKET:-}"
    if [ -z "$R2_BUCKET" ]; then
      echo ""
      echo "请设置环境变量 R2_BUCKET（你的 R2 bucket 名称）"
      echo "   export R2_BUCKET=your-bucket-name"
      echo ""
      read -p "或直接输入 bucket 名称: " R2_BUCKET_INPUT
      R2_BUCKET="$R2_BUCKET_INPUT"
    fi

    if [ -z "$R2_BUCKET" ]; then
      echo "❌ 未指定 R2 Bucket"
      exit 1
    fi

    echo ""
    echo "📤 正在上传到 R2 bucket: $R2_BUCKET ..."
    wrangler r2 object put "${R2_BUCKET}/data.json" --file="$DATA_FILE"
    ;;

  rclone)
    R2_REMOTE="${R2_REMOTE:-r2}"
    R2_BUCKET="${R2_BUCKET:-}"

    if [ -z "$R2_BUCKET" ]; then
      echo ""
      read -p "请输入 R2 bucket 名称: " R2_BUCKET_INPUT
      R2_BUCKET="$R2_BUCKET_INPUT"
    fi

    echo ""
    echo "📤 正在上传到 ${R2_REMOTE}:${R2_BUCKET}/data.json ..."
    rclone copy "$DATA_FILE" "${R2_REMOTE}:${R2_BUCKET}/data.json" --progress
    ;;

  aws-cli)
    R2_ENDPOINT="${R2_ENDPOINT:-https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com}"
    R2_BUCKET="${R2_BUCKET:-}"

    if [ -z "$R2_BUCKET" ]; then
      echo ""
      read -p "请输入 R2 bucket 名称: " R2_BUCKET_INPUT
      R2_BUCKET="$R2_BUCKET_INPUT"
    fi

    echo ""
    echo "📤 正在上传到 s3://${R2_BUCKET}/data.json ..."
    AWS_SHARED_CREDENTIALS_FILE="${AWS_SHARED_CREDENTIALS_FILE:-}" \
      aws --endpoint-url "$R2_ENDPOINT" \
        s3 cp "$DATA_FILE" "s3://${R2_BUCKET}/data.json"
    ;;

  curl)
    R2_ENDPOINT="${R2_ENDPOINT:-}"
    R2_BUCKET="${R2_BUCKET:-}"
    R2_ACCESS_KEY_ID="${R2_ACCESS_KEY_ID:-}"
    R2_SECRET_ACCESS_KEY="${R2_SECRET_ACCESS_KEY:-}"

    if [ -z "$R2_ENDPOINT" ] || [ -z "$R2_BUCKET" ] || [ -z "$R2_ACCESS_KEY_ID" ] || [ -z "$R2_SECRET_ACCESS_KEY" ]; then
      echo ""
      echo "使用 curl 模式需要以下环境变量:"
      echo "   R2_ENDPOINT        (如 https://xxx.r2.cloudflarestorage.com)"
      echo "   R2_BUCKET           (bucket 名称)"
      echo "   R2_ACCESS_KEY_ID    (API Access Key ID)"
      echo "   R2_SECRET_ACCESS_KEY (API Secret Access Key)"
      echo ""
      echo "建议改用 wrangler 或 rclone，配置更简单"
      exit 1
    fi

    DATE_VALUE=$(date -u +"%Y%m%dT%H%M%Z")
    DATE_SHORT=$(date -u +%Y%m%d)

    CONTENT_TYPE="application/json"
    PAYLOAD_HASH=$(openssl dgst -sha256 -binary "$DATA_FILE" | openssl enc -base64)

    CANONICAL_REQUEST="PUT\n/data.json\n\ncontent-type:${CONTENT_TYPE}\nhost:${R2_ENDPOINT#https://}\nx-amz-content-sha256:${PAYLOAD_HASH}\nx-amz-date:${DATE_VALUE}\n\ncontent-type;host;x-amz-content-sha256;x-amz-date\n${PAYLOAD_HASH}"

    CREDENTIAL_SCOPE="${DATE_SHORT}/auto/s3/aws4_request"
    STRING_TO_SIGN="AWS4-HMAC-SHA256\n${DATE_VALUE}\n${CREDENTIAL_SCOPE}\n$(printf "%s" "$CANONICAL_REQUEST" | openssl dgst -sha256 -hex | awk '{print $2}')"

    SIGNING_KEY=$(printf "%s" "aws4${R2_SECRET_ACCESS_KEY}" | openssl dgst -sha256 -hex -hkey "$(printf "%s" "${DATE_SHORT}" | openssl dgst -sha256 -hex -hkey "$(printf "%s" "auto" | openssl dgst -sha256 -hex -hkey "$(printf "%s" "s3" | openssl dgst -sha256 -hex -hkey "" | awk '{print $2}')" | awk '{print $2}')" | awk '{print $2}')

    SIGNATURE=$(printf "%s" "$STRING_TO_SIGN" | openssl dgst -sha256 -hex -hkey "$SIGNING_KEY" | awk '{print $2}')

    AUTHORIZATION_HEADER="AWS4-HMAC-SHA256 Credential=${R2_ACCESS_KEY_ID}/${CREDENTIAL_SCOPE}, SignedHeaders=content-type;host;x-amz-content-sha256;x-amz-date, Signature=${SIGNATURE}"

    echo ""
    echo "📤 正在上传到 ${R2_ENDPOINT}/${R2_BUCKET}/data.json ..."

    curl -fSL -X PUT \
      -T "$DATA_FILE" \
      -H "Content-Type: ${CONTENT_TYPE}" \
      -H "Host: ${R2_ENDPOINT#https://}" \
      -H "X-Amz-Content-Sha256: ${PAYLOAD_HASH}" \
      -H "X-Amz-Date: ${DATE_VALUE}" \
      -H "Authorization: ${AUTHORIZATION_HEADER}" \
      "${R2_ENDPOINT}/${R2_BUCKET}/data.json"
    ;;
esac

echo ""
echo "✅ 上传成功!"
echo "   文件大小: $FILE_SIZE_HUMAN"
echo "   存储:     R2 / $R2_BUCKET / data.json"
echo ""

PUBLIC_URL=""
if [ -n "${R2_PUBLIC_URL:-}" ]; then
  PUBLIC_URL="$R2_PUBLIC_URL"
elif [ -n "${R2_ACCOUNT_ID:-}" ] && [ -n "${R2_BUCKET:-}" ]; then
  PUBLIC_URL="https://pub-${R2_ACCOUNT_ID}.r2.dev/${R2_BUCKET}/data.json"
fi

if [ -n "$PUBLIC_URL" ]; then
  echo "🔗 公开访问 URL: $PUBLIC_URL"
  echo ""
  echo "💡 将此 URL 设置为 GitHub Secret 'R2_DATA_URL' 即可在部署时自动下载"
else
  echo "💡 如需公开访问，请在 Cloudflare Dashboard 中为 bucket 启用 Public Access"
  echo "   然后设置环境变量 R2_PUBLIC_URL 或 R2_ACCOUNT_ID 以显示链接"
fi
