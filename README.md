# CoralMC

## About
A [Python](https://python.org) module that allows you to interact with the [CoralMC](https://coralmc.it/) API.

> **Warning**
CoralMC's API is still in alpha and isn't documented. In the future an access token is going to be required. At the current state, it isn't recommended for production usage as it could stop working at any point.

## Installation
```py
python -m pip install coralmc
```

## Example usage
```py
import coralmc
import asyncio

async def main():
    client = coralmc.CoralMCClient()
    try:
        player_info = await client.get_player_info("Feryzz")
        if player_info:
            print(player_info)
        else:
            print("Player not found!")

        player_stats = await client.get_player_stats("Feryzz")
        if player_stats:
            print(player_stats["kitpvp"])
            print(player_stats["bedwars"])
        else:
            print("Player not found!")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        await client.close()  # Ensure the session is closed

asyncio.run(main())

```

## Links
* [PyPi](https://pypi.org/p/coralmc)
* [JS/TS](https://github.com/gigantino/CoralMC)
