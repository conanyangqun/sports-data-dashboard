from fitparse import FitFile
import os

fit_file_path = os.path.join(os.path.dirname(__file__), '..', 'fit-files', 'ride-0-2023-11-18-13-05-12.fit')

print(f"Analyzing FIT file: {fit_file_path}\n")

fit_file = FitFile(fit_file_path)

print("=== File ID Message ===")
for record in fit_file.get_messages('file_id'):
    for data in record:
        print(f"  {data.name}: {data.value} (type: {data.type})")

print("\n=== Session Message ===")
for record in fit_file.get_messages('session'):
    for data in record:
        print(f"  {data.name}: {data.value} (type: {data.type})")

print("\n=== Device Info Messages ===")
for record in fit_file.get_messages('device_info'):
    for data in record:
        print(f"  {data.name}: {data.value} (type: {data.type})")

print("\n=== All Message Types ===")
message_types = set()
for record in fit_file.get_messages():
    message_types.add(record.type)
print(f"Message types found: {sorted(message_types)}")

print("\n=== Searching for timezone-related fields ===")
timezone_fields = []
for record in fit_file.get_messages():
    for data in record:
        if 'time' in data.name.lower() or 'zone' in data.name.lower() or 'offset' in data.name.lower():
            timezone_fields.append(f"{record.type}.{data.name}: {data.value}")

if timezone_fields:
    print("Found timezone-related fields:")
    for field in timezone_fields:
        print(f"  {field}")
else:
    print("No timezone-related fields found")

print("\n=== Timestamp Details ===")
for record in fit_file.get_messages('session'):
    for data in record:
        if data.name == 'timestamp':
            print(f"  Raw timestamp: {data.value}")
            print(f"  Type: {data.type}")
            if hasattr(data.value, 'tzinfo'):
                print(f"  Timezone info: {data.value.tzinfo}")
            else:
                print("  No timezone info attached")
