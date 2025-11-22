"""
Simple photo capture - no face detection required
Just press SPACE to capture your photo
"""

import cv2
import os

def capture_photo():
    print("\n" + "="*60)
    print("  SIMPLE PHOTO CAPTURE")
    print("="*60)
    
    # Get user info
    print("\nEnter your information:")
    name = input("Name (e.g., John_Doe): ").strip().replace(" ", "_")
    user_id = input("ID Number (e.g., 5555): ").strip()
    
    # Create folder
    folder = "training photos"
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"✓ Created '{folder}' folder")
    
    filename = f"{folder}/{name}_{user_id}.jpg"
    
    print("\n" + "="*60)
    print("CAMERA CONTROLS:")
    print("  SPACE = Capture photo")
    print("  ESC = Cancel")
    print("="*60)
    
    input("\nPress ENTER to open camera...")
    
    # Open camera 1
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("\n❌ Error: Could not open camera 1")
        print("Trying camera 0...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not access any camera!")
            return False
    
    print("\n✓ Camera opened successfully!")
    print("Position yourself and press SPACE to capture...\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read from camera")
            break
        
        # Simple display with instructions
        cv2.putText(frame, "SPACE: Capture | ESC: Cancel", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Position yourself in frame", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Capture Photo - Press SPACE', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE
            cv2.imwrite(filename, frame)
            print(f"\n✓ Photo saved: {filename}")
            print(f"✓ Name: {name.replace('_', ' ')}")
            print(f"✓ ID: {user_id}")
            cap.release()
            cv2.destroyAllWindows()
            return True
        
        elif key == 27:  # ESC
            print("\n❌ Cancelled")
            cap.release()
            cv2.destroyAllWindows()
            return False
    
    cap.release()
    cv2.destroyAllWindows()
    return False

if __name__ == "__main__":
    if capture_photo():
        print("\n" + "="*60)
        print("SUCCESS! Photo captured.")
        print("\nAdd more people? Run this script again.")
        print("Ready to test? Run: python security_system_database.py")
        print("="*60)
