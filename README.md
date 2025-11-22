# Face Recognition Database System

A facial recognition security system that uses a **database folder** to identify multiple people.

## 🎯 Key Features

- **Database System**: Automatically loads all users from a folder
- **Easy to Add Users**: Just drop photos in the `face_database` folder
- **Two-Factor Authentication**: Face recognition + ID verification
- **Auto-Logging**: Tracks all access attempts in `access_logs.txt`
- **No Complex Dependencies**: Uses OpenCV's built-in algorithms (no dlib needed!)

## 📦 Installation

```bash
pip install opencv-python opencv-contrib-python numpy pillow
```

## 🚀 Quick Start

### Step 1: Add People to Database

1. Create photos of people you want to recognize
2. Save them in the `face_database` folder with this naming format:
   ```
   FirstName_LastName_ID.jpg
   ```

**Examples:**
- `face_database/John_Doe_5555.jpg`
- `face_database/Jane_Smith_1234.jpg`
- `face_database/Administrator_0000.jpg`
- `face_database/Bob_Johnson_9999.jpg`

### Step 2: Run the System

```bash
python security_system_database.py
```

The system will:
1. ✅ Auto-load all faces from the database folder
2. ✅ Train the face recognizer
3. ✅ Start the camera
4. ✅ Recognize anyone in the database

## 📸 Photo Guidelines

For best results:
- Use clear, front-facing photos
- Good lighting (avoid shadows)
- Face should be clearly visible
- JPG, JPEG, or PNG format
- One face per photo

## 🔐 How It Works

1. **Camera Scans**: System continuously scans for faces
2. **Face Match**: Compares detected face against database
3. **ID Verification**: If face matches, prompts for ID number
4. **Access Control**:
   - ✅ Correct face + correct ID = Access Granted
   - ❌ Wrong ID = Access Denied, continues scanning
5. **Logging**: All attempts logged to `access_logs.txt`

## 📁 File Structure

```
c:/A dahacks/
├── security_system_database.py    # Main program
├── face_database/                  # Database folder
│   ├── John_Doe_5555.jpg
│   ├── Jane_Smith_1234.jpg
│   └── Administrator_0000.jpg
└── access_logs.txt                 # Auto-generated logs
```

## 🎮 Controls

- **'q' key**: Quit the camera
- **Cancel**: Cancel ID entry (denies access)
- **Logout/Close**: Exit after successful login

## ➕ Adding More People

Just add more photos to the `face_database` folder and restart the program!

```
face_database/
├── Alice_Wonder_1111.jpg    # New person
├── Bob_Builder_2222.jpg      # New person
└── Charlie_Brown_3333.jpg    # New person
```

The system will automatically:
- Detect all photos
- Extract names and IDs from filenames
- Train the recognizer
- Be ready to recognize them!

## 📊 Database Info

The system shows you:
- How many users are loaded
- Each user's name and ID
- Training status

Example output:
```
=== LOADING FACE DATABASE ===
✓ Loaded: John Doe (ID: 5555)
✓ Loaded: Jane Smith (ID: 1234)
✓ Loaded: Administrator (ID: 0000)

=== TRAINING FACE RECOGNIZER ===
✓ Training complete!

Database loaded: 3 users registered
```

## 🔧 Troubleshooting

**"No images found in face_database"**
- Make sure you created the `face_database` folder
- Add at least one photo with a face

**"No face detected in [filename]"**
- Make sure the photo has a clear, visible face
- Try a photo with better lighting
- Face should be front-facing

**"Could not read from camera"**
- Check if webcam is connected
- Make sure no other app is using the camera
- Try restarting the program

**Face not recognized**
- Try adjusting the confidence threshold in the code (line with `if confidence < 70`)
- Add more photos of the same person from different angles
- Ensure good lighting when using the camera

## 🎨 Naming Convention

The filename format is: `Name_ID.extension`

- **Underscores in name**: Use underscores between parts of the name
  - `John_Doe_5555.jpg` → Name: "John Doe", ID: "5555"
- **Last underscore separates ID**: The last underscore separates the ID
  - `Mary_Jane_Watson_7777.jpg` → Name: "Mary Jane Watson", ID: "7777"

## 📝 Access Logs

View `access_logs.txt` to see all activity:

```
[2025-11-21 18:20:15] User: John Doe | Status: ACCESS GRANTED
[2025-11-21 18:21:30] User: Jane Smith | Status: ACCESS DENIED (Wrong ID: 9999)
[2025-11-21 18:22:45] User: Administrator | Status: ACCESS GRANTED
```

## 🆚 Comparison with Original System

| Feature | Original | Database System |
|---------|----------|----------------|
| Add Users | Edit code | Add photo to folder |
| Max Users | Manual setup | Unlimited |
| Setup | Hardcoded | Auto-detected |
| Dependencies | face_recognition (complex) | OpenCV (simple) |

## 🚀 Next Steps

- Add more people to your database
- Customize the confidence threshold
- Add sound notifications
- Export database to CSV
