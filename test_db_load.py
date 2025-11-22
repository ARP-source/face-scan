import os

folder = "training photos"
user_dictionary = {}

files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print("\nLoading database...")
print("="*60)

for filename in files:
    name_parts = filename.rsplit('.', 1)[0]
    
    if '_' in name_parts:
        parts = name_parts.rsplit('_', 1)
        if parts[-1].isdigit():
            name = parts[0].replace('_', ' ')
            user_id = parts[-1]
        else:
            name = name_parts.replace('_', ' ')
            user_id = "0000"
    else:
        name = name_parts.replace('_', ' ')
        user_id = "0000"
    
    user_dictionary[name] = user_id
    print(f"File: {filename}")
    print(f"  Parsed Name: '{name}'")
    print(f"  Parsed ID: '{user_id}'")
    print()

print("="*60)
print("\nDICTIONARY CONTENTS:")
print("="*60)
for name, user_id in user_dictionary.items():
    print(f"'{name}' --> '{user_id}'")
print("="*60)
