import pandas as pd
import numpy as np
from typing import Dict, Tuple

def calculate_player_statistics(player_stats: pd.DataFrame) -> pd.DataFrame:
    """Calculate seasonal statistics for each player"""
    # Group by player and calculate aggregate stats
    season_stats = player_stats.groupby(['player_name', 'team']).agg({
        'points': 'sum',
        'assists': 'sum',
        'completions': 'sum',
        'throws': 'sum',
        'catches': 'sum',
        'turnovers': 'sum',
        'blocks': 'sum',
    }).reset_index()
    
    # Calculate derived statistics
    season_stats['completion_percentage'] = (
        season_stats['completions'] / season_stats['throws']
    ).round(3)
    
    # Add more advanced statistics as needed
    return season_stats

def calculate_team_statistics(team_stats: pd.DataFrame) -> pd.DataFrame:
    """Calculate seasonal statistics for each team"""
    # Group by team and calculate aggregate stats
    season_stats = team_stats.groupby('team').agg({
        'points_for': 'sum',
        'points_against': 'sum',
        'wins': 'sum',
        'losses': 'sum',
        'break_opportunities': 'sum',
        'break_conversions': 'sum',
        'red_zone_attempts': 'sum',
        'red_zone_scores': 'sum',
    }).reset_index()
    
    # Calculate derived statistics
    season_stats['point_differential'] = season_stats['points_for'] - season_stats['points_against']
    season_stats['win_percentage'] = (
        season_stats['wins'] / (season_stats['wins'] + season_stats['losses'])
    ).round(3)
    
    return season_stats

def calculate_game_statistics(game_stats: pd.DataFrame) -> pd.DataFrame:
    """Calculate statistics for each game"""
    # Process individual game statistics
    games = game_stats.copy()
    
    # Add derived game statistics
    games['total_points'] = games['team1_score'] + games['team2_score']
    
    return games

def main():
    # Load integrated data
    player_stats = pd.read_csv('integ-data/player_stats.csv')
    team_stats = pd.read_csv('integ-data/team_stats.csv')
    game_stats = pd.read_csv('integ-data/game_stats.csv')
    
    # Calculate statistics
    season_player_stats = calculate_player_statistics(player_stats)
    season_team_stats = calculate_team_statistics(team_stats)
    processed_game_stats = calculate_game_statistics(game_stats)
    
    # Save processed statistics
    os.makedirs('stats', exist_ok=True)
    season_player_stats.to_csv('stats/season_player_stats.csv', index=False)
    season_team_stats.to_csv('stats/season_team_stats.csv', index=False)
    processed_game_stats.to_csv('stats/processed_game_stats.csv', index=False)

if __name__ == "__main__":
    main()
