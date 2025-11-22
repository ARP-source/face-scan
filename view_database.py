"""
View what's in the face database
"""
import os

folder = "training photos"

print("\n" + "="*60)
print("  FACE DATABASE CONTENTS")
print("="*60)

if not os.path.exists(folder):
    print(f"Error: '{folder}' folder not found!")
else:
    files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if not files:
        print("No images found!")
    else:
        print(f"\nFound {len(files)} image(s):\n")
        
        for idx, filename in enumerate(files, 1):
            name_parts = filename.rsplit('.', 1)[0]
            
            if '_' in name_parts:
                parts = name_parts.rsplit('_', 1)
                if parts[-1].isdigit():
                    name = parts[0].replace('_', ' ')
                    user_id = parts[-1]
                else:
                    name = name_parts.replace('_', ' ')
                    user_id = "0000 (DEFAULT)"
            else:
                name = name_parts.replace('_', ' ')
                user_id = "0000 (DEFAULT)"
            
            print(f"{idx}. {filename}")
            print(f"   - Name: '{name}'")
            print(f"   - ID: '{user_id}'")
            print()

print("="*60)
print("\nTo use the system, enter the EXACT ID shown above")
print("="*60)
