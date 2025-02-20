import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_team_data():
    team_names = [
        "Sky Riders", "Ground Force", "Wind Chasers", "Disc Masters",
        "Spirit Squad", "Flow State", "High Flyers", "Zone Defense"
    ]

    teams_data = []
    for name in team_names:
        teams_data.append({
            'name': name,
            'wins': np.random.randint(0, 15),
            'losses': np.random.randint(0, 15),
            'points_for': np.random.randint(150, 300),
            'points_against': np.random.randint(150, 300),
            'break_opportunities': np.random.randint(50, 100),
            'break_conversions': np.random.randint(20, 50),
            'red_zone_attempts': np.random.randint(40, 80),
            'red_zone_scores': np.random.randint(20, 40),
            'completion_percentage': round(np.random.uniform(0.8, 0.95), 3),
            'total_yards': np.random.randint(2000, 4000)
        })

    return pd.DataFrame(teams_data)

def generate_player_data(teams_df):
    players_data = []
    for team in teams_df['name']:
        for i in range(15):  # 15 players per team
            # Generate role indicators
            handler_score = np.random.uniform(0, 100)  # 0 = pure handler, 100 = pure cutter
            defense_score = np.random.uniform(0, 100)  # 0 = pure offense, 100 = pure defense

            # Calculate usage and efficiency metrics
            touches = np.random.randint(50, 200)
            team_touches = np.random.randint(800, 1200)
            usage_rate = round(touches / team_touches, 3)

            # Generate yards and OIS components
            throwing_yards = np.random.randint(100, 1000)
            receiving_yards = np.random.randint(100, 1000)
            turnovers = np.random.randint(0, 15)

            # Calculate Offensive Impact Score
            goals = np.random.randint(5, 30)
            assists = np.random.randint(5, 30)
            effective_yards = throwing_yards + receiving_yards
            possessions = np.random.randint(50, 150)
            ois = round((goals * 100 + assists * 100 - turnovers * 100 + effective_yards) / possessions, 2)

            players_data.append({
                'name': f"Player_{team}_{i+1}",
                'team': team,
                'points': goals,
                'assists': assists,
                'completions': np.random.randint(50, 200),
                'throws': np.random.randint(100, 300),
                'catches': np.random.randint(80, 250),
                'turnovers': turnovers,
                'blocks': np.random.randint(0, 20),
                'throwing_yards': throwing_yards,
                'receiving_yards': receiving_yards,
                'total_yards': throwing_yards + receiving_yards,
                'usage_rate': usage_rate,
                'offensive_impact_score': ois,
                'handler_cutter_score': round(handler_score, 1),
                'offense_defense_score': round(defense_score, 1),
                'completion_percentage': round(np.random.uniform(0.7, 1.0), 3),
                'red_zone_scores': np.random.randint(0, 15),
                'hucks_attempted': np.random.randint(0, 30),
                'hucks_completed': np.random.randint(0, 20)
            })

    return pd.DataFrame(players_data)

def generate_games_data(teams_df):
    games_data = []
    teams = teams_df['name'].tolist()

    start_date = datetime.now() - timedelta(days=60)

    for i in range(56):  # 7 weeks of games
        game_date = start_date + timedelta(days=i)
        team1, team2 = np.random.choice(teams, 2, replace=False)

        # Generate detailed game stats
        team1_score = np.random.randint(0, 15)
        team2_score = np.random.randint(0, 15)

        games_data.append({
            'date': game_date.strftime('%Y-%m-%d'),
            'team1': team1,
            'team2': team2,
            'team1_score': team1_score,
            'team2_score': team2_score,
            'week': i // 8 + 1,
            'team1_breaks': np.random.randint(0, 5),
            'team2_breaks': np.random.randint(0, 5),
            'team1_turnovers': np.random.randint(5, 15),
            'team2_turnovers': np.random.randint(5, 15),
            'team1_completion_pct': round(np.random.uniform(0.8, 0.95), 3),
            'team2_completion_pct': round(np.random.uniform(0.8, 0.95), 3),
            'team1_yards': np.random.randint(200, 400),
            'team2_yards': np.random.randint(200, 400)
        })

    return pd.DataFrame(games_data)

def generate_all_data():
    teams_df = generate_team_data()
    players_df = generate_player_data(teams_df)
    games_df = generate_games_data(teams_df)

    return teams_df, players_df, games_df