import pandas as pd
import os
from typing import Dict, List, Tuple
import re

def identify_game_info(file_path: str) -> Dict[str, str]:
    """Extract game information from file path and name"""
    # Expected format: Week_X/TeamA_vs_TeamB/stats.xlsx
    path_parts = file_path.split(os.sep)
    
    # Extract week number
    week_match = re.search(r'Week_(\d+)', file_path)
    week = week_match.group(1) if week_match else None
    
    # Extract teams
    teams_match = re.search(r'(.+)_vs_(.+)', path_parts[-2])
    if teams_match:
        team1 = teams_match.group(1)
        team2 = teams_match.group(2)
    else:
        team1 = team2 = None
    
    return {
        'week': week,
        'team1': team1,
        'team2': team2,
        'file_path': file_path
    }

def process_game_file(file_info: Dict[str, str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Process individual game file to extract player and team statistics"""
    # Read the Excel file
    game_data = pd.read_excel(file_info['file_path'])
    
    # Process player statistics
    player_stats = process_player_stats(game_data, file_info)
    
    # Process team statistics
    team_stats = process_team_stats(game_data, file_info)
    
    return player_stats, team_stats

def process_player_stats(game_data: pd.DataFrame, game_info: Dict[str, str]) -> pd.DataFrame:
    """Extract and format player statistics from game data"""
    # This would be customized based on your Excel format
    # Example processing:
    player_stats = game_data.copy()
    player_stats['week'] = game_info['week']
    player_stats['team1'] = game_info['team1']
    player_stats['team2'] = game_info['team2']
    
    return player_stats

def process_team_stats(game_data: pd.DataFrame, game_info: Dict[str, str]) -> pd.DataFrame:
    """Extract and format team statistics from game data"""
    # This would be customized based on your Excel format
    # Example processing:
    team_stats = pd.DataFrame({
        'week': [game_info['week']],
        'team1': [game_info['team1']],
        'team2': [game_info['team2']],
        # Add other team statistics here
    })
    
    return team_stats

def integrate_raw_game_data(game_day_folder: str, output_dir: str):
    """Main function to process all game files"""
    os.makedirs(output_dir, exist_ok=True)
    
    all_player_stats = []
    all_team_stats = []
    
    # Walk through the game day folder
    for root, _, files in os.walk(game_day_folder):
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(root, file)
                game_info = identify_game_info(file_path)
                
                player_stats, team_stats = process_game_file(game_info)
                
                all_player_stats.append(player_stats)
                all_team_stats.append(team_stats)
    
    # Combine all statistics
    combined_player_stats = pd.concat(all_player_stats, ignore_index=True)
    combined_team_stats = pd.concat(all_team_stats, ignore_index=True)
    
    # Save processed data
    combined_player_stats.to_csv(os.path.join(output_dir, 'player_stats.csv'), index=False)
    combined_team_stats.to_csv(os.path.join(output_dir, 'team_stats.csv'), index=False)

if __name__ == "__main__":
    integrate_raw_game_data('game_day_info', 'integ-data')
