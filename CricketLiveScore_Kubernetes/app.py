from flask import Flask, render_template
import requests
import json
from tabulate import tabulate
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env


app = Flask(__name__)

def fetch_cricket_scores():
    url = 'https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent'
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers)
    data = response.json()

    matches_data = []

    for match in data['typeMatches'][0]['seriesMatches'][0]['seriesAdWrapper']['matches']:
        try:
            match_info = match.get('matchInfo', {})
            match_score = match.get('matchScore', {})
            team1 = match_info.get('team1', {}).get('teamName', 'N/A')
            team2 = match_info.get('team2', {}).get('teamName', 'N/A')
            team1_score = match_score.get('team1Score', {}).get('inngs1', {})
            team2_score = match_score.get('team2Score', {}).get('inngs1', {})

            table = [
                [f"{match_info.get('matchDesc', 'N/A')} , {team1} vs {team2}"],
                ["Series Name", match_info.get('seriesName', 'N/A')],
                ["Match Format", match_info.get('matchFormat', 'N/A')],
                ["Result", match_info.get('status', 'N/A')],
                [f"{team1} Score", f"{team1_score.get('runs', 'N/A')}/{team1_score.get('wickets', 'N/A')} in {team1_score.get('overs', 'N/A')} overs"],
                [f"{team2} Score", f"{team2_score.get('runs', 'N/A')}/{team2_score.get('wickets', 'N/A')} in {team2_score.get('overs', 'N/A')} overs"]
            ]
            matches_data.append(tabulate(table, tablefmt="html"))
        except Exception as e:
            print(f"Error processing match: {e}. Full match data: {match}")
            continue

    return matches_data

def fetch_upcoming_matches():
    url = 'https://cricbuzz-cricket.p.rapidapi.com/matches/v1/recent'
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': 'cricbuzz-cricket.p.rapidapi.com'
    }
    response = requests.get(url, headers=headers)
    upcoming_matches = []

    if response.status_code == 200:
        try:
            data = response.json()
            match_schedules = data.get('matchScheduleMap', [])

            for schedule in match_schedules:
                if 'scheduleAdWrapper' in schedule:
                    date = schedule['scheduleAdWrapper']['date']
                    matches = schedule['scheduleAdWrapper']['matchScheduleList']

                    for match_info in matches:
                        for match in match_info['matchInfo']:
                            description = match['matchDesc']
                            team1 = match['team1']['teamName']
                            team2 = match['team2']['teamName']
                            match_data = {
                                'Date': date,
                                'Description': description,
                                'Teams': f"{team1} vs {team2}"
                            }
                            upcoming_matches.append(match_data)
                else:
                    print("No match schedule found for this entry.")

        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
        except KeyError as e:
            print("Key error:", e)
    else:
        print("Failed to fetch cricket scores. Status code:", response.status_code)

    return upcoming_matches

@app.route('/')
def index():
    cricket_scores = fetch_cricket_scores()
    upcoming_matches = fetch_upcoming_matches()
    return render_template('index.html', cricket_scores=cricket_scores, upcoming_matches=upcoming_matches)

if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 8080)),host='0.0.0.0',debug=True)

