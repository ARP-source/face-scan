"""
Quick Setup Script for Face Database
This script helps you capture photos from your webcam and add them to the database.
"""

import cv2
import os
from datetime import datetime

def capture_face_for_database():
    print("\n" + "="*60)
    print("  FACE DATABASE - QUICK SETUP")
    print("="*60)
    
    # Get user information
    print("\nEnter the person's information:")
    first_name = input("First Name: ").strip().replace(" ", "_")
    last_name = input("Last Name (optional): ").strip().replace(" ", "_")
    user_id = input("ID Number (4 digits): ").strip()
    
    # Construct filename
    if last_name:
        filename = f"{first_name}_{last_name}_{user_id}.jpg"
    else:
        filename = f"{first_name}_{user_id}.jpg"
    
    save_path = os.path.join("training photos", filename)
    
    # Check if database folder exists
    if not os.path.exists("training photos"):
        os.makedirs("training photos")
        print("\n✓ Created 'training photos' folder")
    
    print("\n" + "="*60)
    print("  CAMERA INSTRUCTIONS")
    print("="*60)
    print("1. Look directly at the camera")
    print("2. Ensure good lighting")
    print("3. Press SPACE to capture your photo")
    print("4. Press ESC to cancel")
    print("="*60)
    
    input("\nPress ENTER to open camera...")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not access camera!")
        return
    
    # Load face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("\nCamera active! Position yourself and press SPACE when ready...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read from camera")
            break
        
        # Detect faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Display instructions
        cv2.putText(frame, "SPACE: Capture | ESC: Cancel", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if len(faces) > 0:
            cv2.putText(frame, "Ready to capture!", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "No face detected", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow('Database Setup - Capture Photo', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # SPACE key to capture
        if key == 32:  # SPACE
            if len(faces) > 0:
                cv2.imwrite(save_path, frame)
                print(f"\n✓ Photo saved: {save_path}")
                print(f"✓ Name: {first_name.replace('_', ' ')} {last_name.replace('_', ' ')}")
                print(f"✓ ID: {user_id}")
                break
            else:
                print("\nNo face detected! Please position yourself properly.")
        
        # ESC key to cancel
        elif key == 27:  # ESC
            print("\nCapture cancelled.")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    print("\n" + "="*60)
    
    # Ask if they want to add another person
    another = input("\nAdd another person? (y/n): ").strip().lower()
    if another == 'y':
        capture_face_for_database()
    else:
        print("\n✓ Setup complete!")
        print("✓ Run 'python security_system_database.py' to start the system")
        print("="*60)

if __name__ == "__main__":
    try:
        capture_face_for_database()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
    except Exception as e:
        print(f"\nError: {e}")
