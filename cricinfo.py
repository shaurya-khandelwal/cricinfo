import requests
import pandas as pd
import json


def get_match_data(match_id="1237181"):
    url = "https://www.espncricinfo.com/matches/engine/match/{}.json".format(
        match_id)
    response = requests.get(url)
    # print(response.json())
    with open("match_{}.json".format(match_id), "w+") as f:
        json.dump(response.json(), f)


def main(match_id="1237181"):
    with open("match_{}.json".format(match_id), "r") as f:
        data = json.load(f)
    # print(data["team"])
    rows = []
    for team in data["team"]:
        # print(team["team_id"])
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
    df.to_csv("{}.csv".format(match_id), sep="\t")


def get_season_data(season_name="ipl-2020-21-1210595"):
    url = "https://www.espncricinfo.com/series/{}/match-results".format(
        season_name)
    response = requests.get(url)
    print(response.json())
    with open("season_{}.json".format(season_name), "w+") as f:
        json.dump(response.json(), f)


if __name__ == "__main__":
    # get_match_data()
    # main()
    get_season_data()
