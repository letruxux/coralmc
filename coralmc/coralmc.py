import aiohttp
import re

def is_username_valid(username):
    return 3 <= len(username) <= 16 and bool(re.match("^[a-zA-Z0-9_]+$", username))

async def get_player_stats(username):
    if not is_username_valid(username):
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.coralmc.it/api/user/{username}") as response:
            json_data = await response.json()

    bedwars = json_data.get("bedwars", {})
    kitpvp = json_data.get("kitpvp", {})

    if not all(bedwars.get(field) for field in ["name", "displayName"]) or not kitpvp.get("displayName"):
        return None

    return {
        "bedwars": {
            "level": bedwars["level"],
            "experience": bedwars["exp"],
            "coins": bedwars["coins"],
            "kills": bedwars["kills"],
            "deaths": bedwars["deaths"],
            "finalKills": bedwars["final_kills"],
            "finalDeaths": bedwars["final_deaths"],
            "wins": bedwars["wins"],
            "losses": bedwars["played"] - bedwars["wins"],
            "winstreak": bedwars["winstreak"],
            "highestWinstreak": bedwars["h_winstreak"],
        },
        "kitpvp": {
            "balance": kitpvp.get("balance", 0),
            "kills": kitpvp.get("kills", 0),
            "deaths": kitpvp.get("deaths", 0),
            "bounty": kitpvp.get("bounty", 0),
            "highestBounty": kitpvp.get("topBounty", 0),
            "streak": kitpvp.get("streak", 0),
            "highestStreak": kitpvp.get("topstreak", 0),
        },
    }

def get_formatted_rank(raw_rank):
    formatted_rank = re.sub("[^A-Z]", "", raw_rank)
    return formatted_rank if formatted_rank else None

async def get_player_info(username):
    if not is_username_valid(username):
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.coralmc.it/api/user/{username}/infos") as response:
            json_data = await response.json()

    if not json_data.get("username"):
        return None

    return {
        "username": json_data["username"],
        "isBanned": json_data["isBanned"],
        "ranks": {
            "global": get_formatted_rank(json_data.get("globalRank")),
            "bedwars": get_formatted_rank(json_data.get("vipBedwars")),
            "kitpvp": get_formatted_rank(json_data.get("vipKitpvp")),
            "raw": {
                "global": json_data.get("globalRank"),
                "bedwars": json_data.get("vipBedwars"),
                "kitpvp": json_data.get("vipKitpvp"),
            },
        },
    }
    
