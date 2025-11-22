import cv2
import face_recognition
import tkinter as tk
from tkinter import simpledialog, messagebox
import sys
import numpy as np
from datetime import datetime

class FaceIDSystem:
    def __init__(self):
        # --- 1. THE DICTIONARY (Database) ---
        # Stores Name -> ID Number
        self.user_dictionary = {
            "Administrator": "5555",
            "Staff_Member": "9999"
        }
        
        self.known_encodings = []
        self.known_names = []
        
        # Initialize Tkinter (hidden)
        self.root = tk.Tk()
        self.root.withdraw() 

    def log_activity(self, name, status):
        """
        Writes the entry attempt to a text file with a timestamp.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] User: {name} | Status: {status}\n"
        
        try:
            with open("access_logs.txt", "a") as f:
                f.write(log_entry)
            print(f" >> Logged: {log_entry.strip()}")
        except Exception as e:
            print(f"Error writing to log: {e}")

    def load_authorized_face(self, image_path, name):
        """
        Loads a photo and learns the face.
        """
        try:
            print(f"Loading biometric data for {name}...")
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            
            self.known_encodings.append(encoding)
            self.known_names.append(name)
            print(" > Data loaded successfully.")
        except IndexError:
            print(f"Error: Could not find a face in {image_path}.")
            sys.exit()
        except FileNotFoundError:
            print(f"Error: File '{image_path}' not found. Please create it or check the path.")
            sys.exit()

    def show_next_page(self, user_name):
        """
        The 'Next Page' GUI after successful login.
        """
        success_window = tk.Toplevel()
        success_window.title("System Unlocked")
        success_window.geometry("400x250")
        
        label = tk.Label(success_window, text=f"WELCOME, {user_name}", font=("Arial", 20, "bold"), fg="green")
        label.pack(pady=20)
        
        info = tk.Label(success_window, text="Identity Verified.\nID Check Passed.\nLogging entry...", font=("Arial", 12))
        info.pack(pady=10)
        
        btn = tk.Button(success_window, text="Logout / Close", command=success_window.destroy)
        btn.pack(pady=20)
        
        # Wait until this window is closed
        success_window.wait_window()

    def request_id_popup(self, name):
        """
        Opens a graphical popup asking for the ID.
        """
        # Prompt user for input via popup
        entered_id = simpledialog.askstring(
            "Security Check", 
            f"Face Recognized: {name}\n\nPlease enter your ID Number:"
        )
        
        # If user hits cancel on the box, entered_id will be None
        if entered_id is None: 
            return False

        # Check the dictionary
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
        # 0 is usually the default webcam
        video_capture = cv2.VideoCapture(0)
        print("\n--- CAMERA ACTIVE: LOOK AT THE CAMERA ---")
        print("--- Press 'q' to quit manual override ---")
        
        process_this_frame = True

        while True:
            # 1. Grab a single frame of video
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Could not read from camera.")
                break

            # 2. Resize frame of video to 1/4 size for faster processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

            # 3. Process every other frame to save CPU
            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding in face_encodings:
                    # Check for matches
                    matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                    name = "Unknown"

                    face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = self.known_names[best_match_index]

                        # --- MATCH FOUND ---
                        # Show the frame briefly so user sees the lock-on
                        cv2.imshow('Security Gate', frame)
                        cv2.waitKey(1)
                        
                        print(f"Match found: {name}. Requesting ID...")
                        
                        # Trigger the popup logic
                        access_granted = self.request_id_popup(name)
                        
                        if access_granted:
                            # Clean up camera to show next page clearly
                            cv2.destroyAllWindows()
                            video_capture.release()
                            
                            # Show the Success Page
                            self.show_next_page(name)
                            
                            # Exit script completely after success
                            return 
                        else:
                            print("Access Denied. Retrying surveillance...")
                            
            process_this_frame = not process_this_frame

            # Display the resulting image
            cv2.imshow('Security Gate', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        video_capture.release()
        cv2.destroyAllWindows()

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    app = FaceIDSystem()
    
    # SETUP:
    # Ensure 'admin.jpg' exists in the folder.
    # 'Administrator' is the key used in the dictionary at the top of the code.
    app.load_authorized_face("admin.jpg", "Administrator")
    
    # RUN:
    app.start_camera()
