import csv
from http.client import HTTPException
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from functions import finalGrid, playerGuess, getISOCode
from models import PlayerInfo

router = APIRouter()

@router.get("/final_grid/{league_id}")
def final_grid(league_id: str):
    nations, clubs = finalGrid(league_id)
    return {"nations": nations, "clubs": clubs}

@router.post("/guess_player/")
def guess_player(player_info: PlayerInfo):
    answer = playerGuess(player_info.player_name, player_info.nationality, player_info.club)
    return answer

@router.get("/club_logo/{league_id}/{club_name}")
def club_logo(league_id: str, club_name: str):
    logoURL = f"https://raw.githubusercontent.com/luukhopman/football-logos/master/logos/{league_id}/{club_name}.png"
    return {"logoURL": logoURL}

@router.get("/country_iso/{country_name}")
def get_ISO_code(country_name: str):
    code = getISOCode(country_name)
    return {"countryISO": code}

@router.get("/player_names")
def get_player_names(query: str = Query("")):
    try:
        matching_players = []
        # Try reading the CSV file with UTF-8 encoding first
        try:
            with open('players.csv', mode='r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    player_name = row['name']
                    if player_name.lower().startswith(query.lower()):
                        matching_players.append(player_name)
        except UnicodeDecodeError:
            # If UTF-8 fails, try ISO-8859-1 encoding
            with open('players.csv', mode='r', encoding='iso-8859-1') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    player_name = row['name']
                    if player_name.lower().startswith(query.lower()):
                        matching_players.append(player_name)

        # Ensure the response is correctly encoded in UTF-8
        return JSONResponse(
            content={"player_names": matching_players},
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
