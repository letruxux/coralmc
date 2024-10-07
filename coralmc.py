import aiohttp
import re
from typing import Optional, Dict, Any


class PlayerInfo:
    def __init__(self, username: str, is_banned: bool, ranks: Dict[str, Any]):
        self.username: str = username
        self.is_banned: bool = is_banned
        self.ranks: Dict[str, Any] = ranks

    @staticmethod
    def get_formatted_rank(raw_rank: Optional[str]) -> Optional[str]:
        """Format the rank by removing all non-uppercase letters."""
        if raw_rank is None:
            return None
        formatted_rank = re.sub(r"[^A-Z]", "", raw_rank)
        return formatted_rank if formatted_rank else None

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> Optional['PlayerInfo']:
        """Create a PlayerInfo instance from a JSON response."""
        if not json_data.get("username"):
            return None

        ranks = {
            "global": cls.get_formatted_rank(json_data.get("globalRank")),
            "bedwars": cls.get_formatted_rank(json_data.get("vipBedwars")),
            "kitpvp": cls.get_formatted_rank(json_data.get("vipKitpvp")),
            "raw": {
                "global": json_data.get("globalRank"),
                "bedwars": json_data.get("vipBedwars"),
                "kitpvp": json_data.get("vipKitpvp"),
            }
        }
        return cls(
            username=json_data["username"],
            is_banned=json_data.get("isBanned", False),
            ranks=ranks
        )


class PlayerStats:
    def __init__(self, bedwars: Dict[str, Any], kitpvp: Dict[str, Any]):
        self.bedwars: Dict[str, Any] = bedwars
        self.kitpvp: Dict[str, Any] = kitpvp

    @classmethod
    def from_json(cls, json_data: Dict[str, Any]) -> 'PlayerStats':
        """Create a PlayerStats instance from a JSON response."""
        bedwars = json_data.get("bedwars", {})
        kitpvp = json_data.get("kitpvp", {})

        return cls(
            bedwars={
                "level": bedwars.get("level", 0),
                "experience": bedwars.get("exp", 0),
                "coins": bedwars.get("coins", 0),
                "kills": bedwars.get("kills", 0),
                "deaths": bedwars.get("deaths", 0),
                "final_kills": bedwars.get("final_kills", 0),
                "final_deaths": bedwars.get("final_deaths", 0),
                "wins": bedwars.get("wins", 0),
                "losses": bedwars.get("played", 0) - bedwars.get("wins", 0),
                "winstreak": bedwars.get("winstreak", 0),
                "highest_winstreak": bedwars.get("h_winstreak", 0),
            },
            kitpvp={
                "balance": kitpvp.get("balance", 0),
                "kills": kitpvp.get("kills", 0),
                "deaths": kitpvp.get("deaths", 0),
                "bounty": kitpvp.get("bounty", 0),
                "highest_bounty": kitpvp.get("topBounty", 0),
                "streak": kitpvp.get("streak", 0),
                "highest_streak": kitpvp.get("topstreak", 0),
            }
        )


class CoralMCClient:
    BASE_URL: str = "https://api.coralmc.it/api/user/"

    def __init__(self):
        self.session: Optional[aiohttp.ClientSession] = None

    @staticmethod
    def is_username_valid(username: str) -> bool:
        """Check if the username is valid (3-16 chars, alphanumeric, or underscores)."""
        return 3 <= len(username) <= 16 and bool(re.match(r"^[a-zA-Z0-9_]+$", username))

    async def _get_json(self, endpoint: str) -> Dict[str, Any]:
        """Perform a GET request and return the JSON response."""
        async with self.session.get(endpoint) as response:
            return await response.json()

    async def get_player_stats(self, username: str) -> Optional[PlayerStats]:
        """Fetch and return player stats for Bedwars and KitPvP."""
        if not self.is_username_valid(username):
            return None

        if self.session is None:
            self.session = aiohttp.ClientSession()

        json_data = await self._get_json(f"{self.BASE_URL}{username}")

        if json_data.get("error") is not None:
            return None

        return PlayerStats.from_json(json_data)

    async def get_player_info(self, username: str) -> Optional[PlayerInfo]:
        """Fetch and return basic player info, including ranks and ban status."""
        if not self.is_username_valid(username):
            return None

        if self.session is None:
            self.session = aiohttp.ClientSession()

        json_data = await self._get_json(f"{self.BASE_URL}{username}/infos")

        return PlayerInfo.from_json(json_data)

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None
