"""
Script Name: Street View Global Tab Viewer
Description: Reads a CSV or Excel file containing spatial data, prompts for 
             the file path, and sequentially opens each location in Google 
             Street View using global hotkeys.

Global Controls:
  - [Ctrl + Shift + F] : Advance to the next location.
  - [Ctrl + Shift + J] : Jump to a specific file row (prompts in terminal).
  - [Ctrl + Shift + Q] : Quit the script.

Operating System Notes:
  - Windows: Works immediately.
  - Linux: Requires root/sudo privileges to monitor global keypresses.
  - macOS: Requires Accessibility permissions granted to your terminal app 
           under System Settings > Privacy & Security > Accessibility.
"""

import os
import webbrowser
import keyboard
import pandas as pd

def open_street_view():
    print("=" * 60)
    print(" GOOGLE STREET VIEW BATCH VIEWER")
    print("=" * 60)
    
    # Prompt the user for the file path explicitly
    file_path = input("Enter the path to your .csv or .xlsx file (or drag & drop it here): ").strip()
    file_path = file_path.strip('"\'')

    if not os.path.exists(file_path):
        print(f"\n[Error] File not found at '{file_path}'. Please check the path and try again.")
        return

    # Automatically detect and load CSV or Excel files
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file_path)
        else:
            print("\n[Error] Unsupported file format. Please provide a .csv or .xlsx file.")
            return
    except Exception as e:
        print(f"\n[Error] Failed to read file: {e}")
        return

    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        print("\n[Error] Missing required columns. The file must contain 'Latitude' and 'Longitude' columns.")
        return

    print(f"\n[Success] Loaded {len(df)} rows from {file_path}.")
    print("-" * 60)
    print("ACTIVE CONTROLS (Global):")
    print("  -> Press [Ctrl + Shift + F] to go to the next location")
    print("  -> Press [Ctrl + Shift + J] to jump to a specific file row")
    print("  -> Press [Ctrl + Shift + Q] to quit the script")
    print("-" * 60 + "\n")

    idx = 0
    while idx < len(df):
        row = df.iloc[idx]
        lat = row['Latitude']
        lon = row['Longitude']
        road = row.get('Road_name', 'Unknown Road')
        
        # File row compensation: index 0 is Excel/CSV row 2
        file_row = idx + 2
        
        url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"
        
        print(f"[{idx + 1}/{len(df)}] Opening -> File Row: {file_row} | Road: {road} | Lat: {lat}, Lon: {lon}")
        webbrowser.open_new_tab(url)
        
        if idx == len(df) - 1:
            print("\n[Complete] Reached the end of the file.")
            break
            
        print("Waiting for hotkey ([Ctrl+Shift+F] Next | [Ctrl+Shift+J] Jump | [Ctrl+Shift+Q] Quit)...")
        
        action = None
        while True:
            if keyboard.is_pressed('ctrl+shift+f'):
                while keyboard.is_pressed('ctrl+shift+f'):
                    pass
                action = 'next'
                break
            elif keyboard.is_pressed('ctrl+shift+j'):
                while keyboard.is_pressed('ctrl+shift+j'):
                    pass
                action = 'jump'
                break
            elif keyboard.is_pressed('ctrl+shift+q'):
                while keyboard.is_pressed('ctrl+shift+q'):
                    pass
                action = 'quit'
                break
        
        if action == 'quit':
            print("\n[Exited] Script terminated by user.")
            return
        elif action == 'jump':
            # Prompt user in terminal for target file row
            target_input = input(f"\nEnter target file row number to jump to (2 to {len(df) + 1}): ").strip()
            try:
                target_row = int(target_input)
                new_idx = target_row - 2
                if 0 <= new_idx < len(df):
                    idx = new_idx
                    print(f"[Jump] Resuming from File Row {target_row} (Index {idx}).\n")
                    continue
                else:
                    print(f"[Error] Row {target_row} is out of bounds. Valid range is 2 to {len(df) + 1}. Continuing from current row.\n")
            except ValueError:
                print("[Error] Invalid input. Please enter a valid integer. Continuing from current row.\n")
        
        idx += 1

if __name__ == "__main__":
    open_street_view()