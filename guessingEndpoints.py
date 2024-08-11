import csv
from http.client import HTTPException
from fastapi import APIRouter
from functions import finalGrid, playerGuess, getISOCode
from models import PlayerInfo
from fastapi import Query


router = APIRouter()

@router.get("/final_grid/{league_id}")
def final_grid(league_id: str):
    nations, clubs = finalGrid(league_id)
    return{"nations":nations, "clubs":clubs}

@router.post("/guess_player/")
def guess_player(player_info:PlayerInfo):
    answer = playerGuess(player_info.player_name,player_info.nationality,player_info.club)
    return answer


@router.get("/club_logo/{league_id}/{club_name}")
def club_logo(league_id: str, club_name: str):
    logoURL = f"https://raw.githubusercontent.com/luukhopman/football-logos/master/logos/{league_id}/{club_name}.png"
    return{"logoURL": logoURL}

@router.get("/country_iso/{country_name}")
def get_ISO_code(country_name: str):
    code = getISOCode(country_name)
    return{"countryISO":code}

@router.get("/player_names")
def get_player_names(query: str = Query("")):
    try:
        matching_players = []
        with open('players.csv', mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                player_name = row['name']  # Sütun adının 'name' olduğunu varsayıyoruz
                if player_name.lower().startswith(query.lower()):
                    matching_players.append(player_name)
        return {"player_names": matching_players}
    except UnicodeDecodeError as e:
        print(f"Unicode decoding error: {e}")
        raise HTTPException(status_code=500, detail="Unicode decoding error.")
    except Exception as e:
        print(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")