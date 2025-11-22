import cv2
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import numpy as np
from datetime import datetime
from pathlib import Path
import pickle

class SimpleFaceIDSystem:
    def __init__(self):
        # --- DATABASE CONFIGURATION ---
        self.database_folder = "training photos"
        self.user_dictionary = {}
        
        # Face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Store face data
        self.known_faces = {}  # name: list of face images
        self.user_ids = {}     # name: ID
        
        # Initialize Tkinter (hidden)
        self.root = tk.Tk()
        self.root.withdraw()

    def log_activity(self, name, status):
        """Log access attempts"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] User: {name} | Status: {status}\n"
        
        try:
            with open("access_logs.txt", "a") as f:
                f.write(log_entry)
            print(f" >> Logged: {log_entry.strip()}")
        except Exception as e:
            print(f"Error writing to log: {e}")

    def load_database(self):
        """Load all faces from the training photos folder"""
        print("\n=== LOADING FACE DATABASE ===")
        
        if not os.path.exists(self.database_folder):
            print(f"Error: Database folder '{self.database_folder}' not found.")
            return False
        
        image_files = [f for f in os.listdir(self.database_folder) 
                      if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if not image_files:
            print(f"Error: No images found in '{self.database_folder}'.")
            return False
        
        for filename in image_files:
            # Parse filename: Name_ID.jpg
            name_parts = filename.rsplit('.', 1)[0]
            
            # Try to extract name and ID
            if '_' in name_parts:
                parts = name_parts.rsplit('_', 1)
                # Check if last part is numeric (ID)
                if parts[-1].isdigit():
                    name = parts[0].replace('_', ' ')
                    user_id = parts[-1]
                else:
                    # No ID in filename, use whole name
                    name = name_parts.replace('_', ' ')
                    user_id = "0000"
            else:
                name = name_parts.replace('_', ' ')
                user_id = "0000"
            
            # Load and process image
            image_path = os.path.join(self.database_folder, filename)
            img = cv2.imread(image_path)
            
            if img is None:
                print(f"Warning: Could not load {filename}")
                continue
            
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            if len(faces) == 0:
                print(f"Warning: No face detected in {filename}")
                continue
            
            # Get the largest face
            (x, y, w, h) = max(faces, key=lambda face: face[2] * face[3])
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (100, 100))
            
            # Store face data
            if name not in self.known_faces:
                self.known_faces[name] = []
                self.user_ids[name] = user_id
                self.user_dictionary[name] = user_id
            
            self.known_faces[name].append(face_img)
            print(f"✓ Loaded: {name} (ID: {user_id}) from {filename}")
        
        if not self.known_faces:
            print("Error: No valid faces loaded.")
            return False
        
        print(f"\n✓ Database loaded: {len(self.known_faces)} users")
        for name, id_num in self.user_ids.items():
            print(f"  - {name}: {len(self.known_faces[name])} photo(s), ID: {id_num}")
        
        return True

    def compare_faces(self, face_img, name):
        """Simple face comparison using template matching"""
        if name not in self.known_faces:
            return 0.0
        
        face_img = cv2.resize(face_img, (100, 100))
        
        # Compare with all stored faces for this person
        similarities = []
        for stored_face in self.known_faces[name]:
            # Normalize both images
            face_norm = cv2.normalize(face_img, None, 0, 255, cv2.NORM_MINMAX)
            stored_norm = cv2.normalize(stored_face, None, 0, 255, cv2.NORM_MINMAX)
            
            # Calculate similarity using histogram comparison
            hist1 = cv2.calcHist([face_norm], [0], None, [256], [0, 256])
            hist2 = cv2.calcHist([stored_norm], [0], None, [256], [0, 256])
            
            similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            similarities.append(similarity)
        
        # Return best match
        return max(similarities) if similarities else 0.0

    def recognize_face(self, face_img):
        """Find best matching person"""
        best_match = None
        best_score = 0.0
        
        for name in self.known_faces.keys():
            score = self.compare_faces(face_img, name)
            if score > best_score:
                best_score = score
                best_match = name
        
        # Threshold for recognition (adjust as needed)
        if best_score > 0.5:  # 50% similarity
            return best_match, best_score
        else:
            return None, 0.0

    def show_next_page(self, user_name):
        """Success page after login"""
        success_window = tk.Toplevel()
        success_window.title("System Unlocked")
        success_window.geometry("400x250")
        
        label = tk.Label(success_window, text=f"WELCOME, {user_name}", 
                        font=("Arial", 20, "bold"), fg="green")
        label.pack(pady=20)
        
        info = tk.Label(success_window, text="Identity Verified.\nID Check Passed.\nLogging entry...", 
                       font=("Arial", 12))
        info.pack(pady=10)
        
        btn = tk.Button(success_window, text="Logout / Close", command=success_window.destroy)
        btn.pack(pady=20)
        
        success_window.wait_window()

    def request_id_popup(self, name):
        """Ask for ID verification"""
        entered_id = simpledialog.askstring(
            "Security Check", 
            f"Face Recognized: {name}\n\nPlease enter your ID Number:"
        )
        
        if entered_id is None:
            return False

        required_id = self.user_dictionary.get(name)
        
        if entered_id == required_id:
            self.log_activity(name, "ACCESS GRANTED")
            messagebox.showinfo("Access Granted", "Identity Confirmed.")
            return True
        else:
            self.log_activity(name, f"ACCESS DENIED (Wrong ID: {entered_id})")
            messagebox.showerror("Access Denied", "ID Number did not match database.")
            return False

    def start_camera(self):
        """Start camera and begin face recognition"""
        print("Trying to open camera 1...")
        video_capture = cv2.VideoCapture(1, cv2.CAP_DSHOW)
        
        # Give it a moment to initialize
        import time
        time.sleep(1)
        
        if not video_capture.isOpened():
            print("Camera 1 not available, trying camera 0...")
            video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            time.sleep(1)
            
            if not video_capture.isOpened():
                print("Error: Could not access any camera!")
                print("Please make sure:")
                print("  1. Camera is connected")
                print("  2. No other app is using the camera")
                print("  3. Camera permissions are enabled")
                return
        
        print("\n=== CAMERA ACTIVE ===")
        print("Press 'q' to quit\n")
        
        frame_count = 0
        last_recognition_time = 0
        recognition_cooldown = 30  # Process every 30 frames
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Could not read from camera.")
                break

            frame_count += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                # Draw rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Only process every N frames
                if frame_count - last_recognition_time > recognition_cooldown:
                    face_img = gray[y:y+h, x:x+w]
                    
                    # Recognize
                    name, confidence = self.recognize_face(face_img)
                    
                    if name:
                        last_recognition_time = frame_count
                        
                        cv2.putText(frame, f"{name}", (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                        
                        print(f"\n>>> Match: {name} (Confidence: {confidence:.2f})")
                        
                        # Show frame
                        cv2.imshow('Face Recognition System', frame)
                        cv2.waitKey(1)
                        
                        # Request ID
                        access_granted = self.request_id_popup(name)
                        
                        if access_granted:
                            cv2.destroyAllWindows()
                            video_capture.release()
                            self.show_next_page(name)
                            return
                        else:
                            print("Access Denied. Continuing...\n")
                    else:
                        cv2.putText(frame, "Unknown", (x, y-10), 
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                else:
                    cv2.putText(frame, "Scanning...", (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            cv2.imshow('Face Recognition System', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

# --- MAIN ---
if __name__ == "__main__":
    app = SimpleFaceIDSystem()
    
    print("=" * 60)
    print("  SIMPLE FACE RECOGNITION SYSTEM")
    print("=" * 60)
    
    if app.load_database():
        print("=" * 60)
        app.start_camera()
    else:
        print("\n" + "=" * 60)
        print("SETUP REQUIRED:")
        print("=" * 60)
        print(f"Add photos to '{app.database_folder}' folder")
        print("Format: Name_ID.jpg (e.g., John_Doe_5555.jpg)")
        print("=" * 60)
