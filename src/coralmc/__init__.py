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