import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
import os


def get_match_data(match_id="1237181"):
    url = "https://www.espncricinfo.com/matches/engine/match/{}.json".format(
        match_id)
    response = requests.get(url)
    with open("match_json/match_{}.json".format(match_id), "w+") as f:
        json.dump(response.json(), f)


def match_to_csv(match_id="1237181"):
    with open("match_json/match_{}.json".format(match_id), "r") as f:
        data = json.load(f)
    rows = []
    for team in data["team"]:
        for player in team["player"]:
            rows.append({
                "match_id": match_id,
                "date": data["match"]["start_date_raw"],
                "ground_id": data["match"]["ground_id"],
                "home_team_id": data["match"]["home_team_id"],
                "home_team_name": data["match"]["team1_name"],
                "away_team_id": data["match"]["away_team_id"],
                "away_team_name": data["match"]["team2_name"],
                "player_name": player["known_as"],
                "player_id": player["player_id"],
                "team_id": team["team_id"],
                "bowling_style": player["bowling_style"],
                "batting_style": player["batting_style"]
            })

    df = pd.DataFrame(rows)
    df.to_csv("match_csv/{}.csv".format(match_id), sep="\t")


def get_matches_in_season(season_name="ipl-2020-21-1210595"):
    match_ids = []
    url = "https://www.espncricinfo.com/series/{}/match-results".format(
        season_name)
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    for a in soup.find_all("a", {"class": "match-info-link-FIXTURES"}):
        print("match_id : ", a["href"].split("/")[-2].split("-")[-1])
        match_ids.append(a["href"].split("/")[-2].split("-")[-1])
    return match_ids


def get_season_data(season_name="ipl-2020-21-1210595"):
    match_ids = get_matches_in_season(season_name)
    for match_id in match_ids:
        get_match_data(match_id)
        match_to_csv(match_id)


if __name__ == "__main__":
    if not os.path.exists("match_csv"):
        os.makedirs("match_csv")

    if not os.path.exists("match_json"):
        os.makedirs("match_json")

    # get_match_data()
    # main()
    get_season_data()
