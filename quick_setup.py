"""
Create a test user for the face database using webcam
This will capture your photo and add you as "Test User" with ID 9999
"""

import cv2
import os

def capture_test_user():
    print("\n" + "="*60)
    print("  QUICK TEST - Capture Your Face")
    print("="*60)
    print("\nCreating test user:")
    print("  Name: Test_User")
    print("  ID: 9999")
    print("\n1. Look at the camera")
    print("2. Press SPACE to capture")
    print("3. Press ESC to cancel")
    print("="*60)
    
    # Create database folder
    if not os.path.exists("training photos"):
        os.makedirs("training photos")
    
    filename = "training photos/Test_User_9999.jpg"
    
    # Open camera
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("\nError: Could not access camera!")
        print("Make sure your webcam is connected and not in use.")
        return False
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    print("\nCamera active! Press SPACE when ready...\n")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read from camera")
            break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw face detection
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected - Ready!", (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Instructions
        cv2.putText(frame, "SPACE: Capture | ESC: Cancel", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        if len(faces) == 0:
            cv2.putText(frame, "Position your face in frame", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.imshow('Capture Test User Photo', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE
            if len(faces) > 0:
                cv2.imwrite(filename, frame)
                print(f"✓ Photo saved: {filename}")
                cap.release()
                cv2.destroyAllWindows()
                return True
            else:
                print("No face detected! Please position yourself in frame.")
        
        elif key == 27:  # ESC
            print("Cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            return False
    
    cap.release()
    cv2.destroyAllWindows()
    return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  CREATING TEST USER FOR FACE DATABASE")
    print("="*60)
    
    if capture_test_user():
        print("\n" + "="*60)
        print("✓ Test user created successfully!")
        print("\nYou can now run the main system:")
        print("  python security_system_database.py")
        print("\nWhen prompted, enter ID: 9999")
        print("="*60)
    else:
        print("\nSetup cancelled.")
