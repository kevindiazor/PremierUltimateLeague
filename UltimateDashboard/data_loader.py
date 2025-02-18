import os
import pandas as pd
from typing import Tuple

def load_stats_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load the processed statistics from the stats directory
    Returns:
        Tuple containing (teams_df, players_df, games_df)
    """
    stats_dir = "stats"
    
    # Load team stats
    teams_df = pd.read_csv(os.path.join(stats_dir, "season_team_stats.csv"))
    
    # Load player stats
    players_df = pd.read_csv(os.path.join(stats_dir, "season_player_stats.csv"))
    
    # Load game stats
    games_df = pd.read_csv(os.path.join(stats_dir, "processed_game_stats.csv"))
    
    # Convert date column to datetime
    games_df['date'] = pd.to_datetime(games_df['date'])
    
    return teams_df, players_df, games_df

def process_and_load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Run the data processing pipeline and load the results
    """
    try:
        # Import and run the processing pipeline
        from data_processing.main import main as process_data
        process_data()
        
        # Load the processed data
        return load_stats_data()
    except Exception as e:
        print(f"Error processing data: {str(e)}")
        # If processing fails, use sample data as fallback
        from data_generator import generate_all_data
        return generate_all_data()
