from fitparse import FitFile
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser(description='Analyze FIT file message types and fields')
parser.add_argument('fit_file', help='Path to the FIT file to analyze')
args = parser.parse_args()

print(f"Analyzing FIT file: {args.fit_file}\n")

fit_file = FitFile(args.fit_file)

message_types_fields = defaultdict(set)
message_types_count = defaultdict(int)
message_types_example = {}

for record in fit_file.get_messages():
    message_types_count[record.name] += 1
    if record.name not in message_types_example:
        message_types_example[record.name] = record
    for data in record:
        message_types_fields[record.name].add(data.name)

print("=== Message Types and Their Fields ===\n")

for msg_type in sorted(message_types_fields.keys()):
    count = message_types_count[msg_type]
    fields = sorted(message_types_fields[msg_type])
    print(f"[{msg_type}] (count: {count})")
    print(f"  Fields: {', '.join(fields)}")
    print(f"  Example:")
    for data in message_types_example[msg_type]:
        print(f"    {data.name}: {data.value}")
    print()
