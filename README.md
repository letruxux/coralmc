# CoralMC

## About
A [Python](https://python.org) module that allows you to interact with the [CoralMC](https://coralmc.it/) API.

> **Warning**
CoralMC's API is still in alpha and isn't documented. In the future an access token is going to be required. At the current state, it isn't recommended for production usage as it could stop working at any point.

## Installation
```py
python -m pip install 'coralmc @ git+https://github.com/letruxux/coralmc@ed323d6a0421580cc95a0667fd74cfe22f10eba7'
```

## Example usage
Get basic player info:
```py
import coralmc
import asyncio

async def main():
    try:
        playerInfo = await coralmc.getPlayerInfo("Feryzz")
        if playerInfo:
            print(playerInfo)
        else:
            print("Player not found!")
    except Exception as error:
        print(f"Error: {error}")

asyncio.run(main())
```
Get player stats:
```py
import coralmc
import asyncio

async def main():
    try:
        playerStats = await coralmc.getPlayerStats("Feryzz")
        if playerStats:
            print(playerStats["kitpvp"])
            print(playerStats["bedwars"])
        else:
            print("Player not found!")
    except Exception as error:
        print(f"Error: {error}")

asyncio.run(main())
```
