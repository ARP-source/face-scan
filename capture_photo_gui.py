"""
Photo capture with GUI dialogs
No terminal input required!
"""

import cv2
import os
import tkinter as tk
from tkinter import simpledialog, messagebox

def capture_photo_gui():
    # Create hidden root window for dialogs
    root = tk.Tk()
    root.withdraw()
    
    print("\n" + "="*60)
    print("  PHOTO CAPTURE - GUI MODE")
    print("="*60)
    
    # Get name via popup
    name = simpledialog.askstring("Enter Name", "Enter your name (e.g., John_Doe):")
    if not name:
        print("❌ Cancelled - no name entered")
        return False
    
    name = name.strip().replace(" ", "_")
    
    # Get ID via popup
    user_id = simpledialog.askstring("Enter ID", "Enter your ID number (e.g., 5555):")
    if not user_id:
        print("❌ Cancelled - no ID entered")
        return False
    
    user_id = user_id.strip()
    
    # Create folder
    folder = "training photos"
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"✓ Created '{folder}' folder")
    
    filename = f"{folder}/{name}_{user_id}.jpg"
    
    print(f"\n✓ Name: {name.replace('_', ' ')}")
    print(f"✓ ID: {user_id}")
    print(f"✓ Will save to: {filename}")
    
    # Show instructions
    messagebox.showinfo("Camera Instructions", 
                       "Camera will open next.\n\n"
                       "Controls:\n"
                       "  • SPACE = Capture photo\n"
                       "  • ESC = Cancel\n\n"
                       "Position yourself and press SPACE!")
    
    # Open camera 1
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("\n⚠ Camera 1 not available, trying camera 0...")
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Camera Error", "Could not access any camera!")
            return False
    
    print("\n✓ Camera opened successfully!")
    print("Press SPACE to capture photo...\n")
    
    captured = False
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Error: Could not read from camera")
            break
        
        # Add text overlay
        cv2.putText(frame, f"User: {name.replace('_', ' ')}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {user_id}", (10, 65),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(frame, "SPACE: Capture | ESC: Cancel", (10, frame.shape[0] - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Draw center crosshair to help positioning
        height, width = frame.shape[:2]
        cv2.line(frame, (width//2 - 20, height//2), (width//2 + 20, height//2), (0, 255, 0), 2)
        cv2.line(frame, (width//2, height//2 - 20), (width//2, height//2 + 20), (0, 255, 0), 2)
        
        cv2.imshow('Capture Photo - Press SPACE', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == 32:  # SPACE
            cv2.imwrite(filename, frame)
            print(f"\n✅ Photo saved: {filename}")
            captured = True
            break
        
        elif key == 27:  # ESC
            print("\n❌ Cancelled by user")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    if captured:
        messagebox.showinfo("Success!", 
                          f"Photo captured successfully!\n\n"
                          f"Saved as: {name}_{user_id}.jpg\n\n"
                          f"Add more people or run the security system.")
        return True
    else:
        return False

def main():
    while True:
        if capture_photo_gui():
            # Ask if user wants to add another person
            root = tk.Tk()
            root.withdraw()
            
            result = messagebox.askyesno("Add Another?", 
                                        "Photo saved successfully!\n\n"
                                        "Would you like to add another person?")
            
            if not result:
                messagebox.showinfo("Complete!", 
                                  "Setup complete!\n\n"
                                  "Run: python security_system_database.py\n"
                                  "to start the face recognition system.")
                break
        else:
            break

if __name__ == "__main__":
    main()
