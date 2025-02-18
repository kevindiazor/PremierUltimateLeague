import os
from google_drive_handler import download_game_day_folder, extract_game_files
from process_game_data import integrate_raw_game_data
from calculate_statistics import main as calculate_stats

def main():
    # Configuration
    FOLDER_ID = "15PeXmyFNiqaDOVeH7svsJezZTwQKDmg0"  # Add your Google Drive folder ID
    GAME_DAY_FOLDER = "game_day_info"
    INTEG_DATA_DIR = "integ-data"
    
    # Step 1: Download data from Google Drive
    print("Downloading game day data from Google Drive...")
    download_game_day_folder(FOLDER_ID, GAME_DAY_FOLDER)
    
    # Step 2: Process raw game data
    print("Processing raw game data...")
    integrate_raw_game_data(GAME_DAY_FOLDER, INTEG_DATA_DIR)
    
    # Step 3: Calculate statistics
    print("Calculating season statistics...")
    calculate_stats()
    
    print("Data processing complete!")

if __name__ == "__main__":
    main()
