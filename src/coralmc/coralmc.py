import aiohttp
import re


def isUsernameValid(username):
    return 3 <= len(username) <= 16 and bool(re.match("^[a-zA-Z0-9_]+$", username))


async def getPlayerStats(username):
    if not isUsernameValid(username):
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.coralmc.it/api/user/{username}"
        ) as response:
            json_data = await response.json()

    bedwars: dict = json_data.get("bedwars", {})
    kitpvp: dict = json_data.get("kitpvp", {})

    if not all(
        bedwars.get(field) for field in ["name", "displayName"]
    ) or not kitpvp.get("displayName"):
        return None

    return {
        "bedwars": {
            "level": bedwars.get("level", 0),
            "experience": bedwars.get("exp", 0),
            "coins": bedwars.get("coins", 0),
            "kills": bedwars.get("kills", 0),
            "deaths": bedwars.get("deaths", 0),
            "finalKills": bedwars.get("final_kills", 0),
            "finalDeaths": bedwars.get("final_deaths", 0),
            "wins": bedwars.get("wins", 0),
            "losses": bedwars.get("played", 0) - bedwars.get("wins", 0),
            "winstreak": bedwars.get("winstreak", 0),
            "highestWinstreak": bedwars.get("h_winstreak", 0),
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


def getFormattedRank(raw_rank):
    formatted_rank = re.sub("[^A-Z]", "", raw_rank)
    return formatted_rank if formatted_rank else None


async def getPlayerInfo(username):
    if not isUsernameValid(username):
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.coralmc.it/api/user/{username}/infos"
        ) as response:
            json_data = await response.json()

    if not json_data.get("username"):
        return None

    return {
        "username": json_data["username"],
        "isBanned": json_data["isBanned"],
        "ranks": {
            "global": getFormattedRank(json_data.get("globalRank")),
            "bedwars": getFormattedRank(json_data.get("vipBedwars")),
            "kitpvp": getFormattedRank(json_data.get("vipKitpvp")),
            "raw": {
                "global": json_data.get("globalRank"),
                "bedwars": json_data.get("vipBedwars"),
                "kitpvp": json_data.get("vipKitpvp"),
            },
        },
    }
