# DEPENDENCIES
# Be sure to run the following `install` first:
'''
$ pip install pandas openpyxl keyboard
'''
# NOTES:
# "Vibe Coded" with Gemini
# Script works best with Windows

"""
Script Name: Street View Global Tab Viewer
Description: Reads a CSV or Excel file containing spatial data, prompts for 
             the file path, and sequentially opens each location in Google 
             Street View using global hotkeys.

Global Controls:
  - [Ctrl + Shift + F] : Advance to the next row / location (works globally, 
                         even when the terminal is not active/highlighted).
  - [Ctrl + Shift + Q] : Quit / exit the script at any time.

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
    
    # Remove surrounding quotes if the file path was drag-and-dropped
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

    # Verify latitude and longitude columns exist explicitly
    if 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        print("\n[Error] Missing required columns. The file must contain 'Latitude' and 'Longitude' columns.")
        return

    print(f"\n[Success] Loaded {len(df)} rows from {file_path}.")
    print("-" * 60)
    print("ACTIVE CONTROLS (Global):")
    print("  -> Press [Ctrl + Shift + F] to go to the next location")
    print("  -> Press [Ctrl + Shift + Q] to quit the script")
    print("-" * 60 + "\n")

    for index, row in df.iterrows():
        lat = row['Latitude']
        lon = row['Longitude']
        road = row.get('Road_name', 'Unknown Road')
        row_num = row.get('Row', index + 1)
        
        # Official Google Maps Street View panorama URL format
        url = f"https://www.google.com/maps/@?api=1&map_action=pano&viewpoint={lat},{lon}"
        
        print(f"[{index + 1}/{len(df)}] Opening -> Row: {row_num} | Road: {road} | Lat: {lat}, Lon: {lon}")
        
        # Open location in a new browser tab
        webbrowser.open_new_tab(url)
        
        # Terminate loop if it is the final row
        if index == len(df) - 1:
            print("\n[Complete] Reached the end of the file.")
            break
            
        print("Waiting for global hotkey [Ctrl + Shift + F]...")
        
        # Block execution globally until one of the designated hotkeys is triggered
        while True:
            if keyboard.is_pressed('ctrl+shift+f'):
                # Debounce: wait until the key combination is released to prevent multi-triggering
                while keyboard.is_pressed('ctrl+shift+f'):
                    pass
                break
            elif keyboard.is_pressed('ctrl+shift+q'):
                print("\n[Exited] Script terminated by user.")
                return

if __name__ == "__main__":
    open_street_view()