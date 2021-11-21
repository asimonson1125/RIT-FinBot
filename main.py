from dotenv import load_dotenv
import os
import discord

load_dotenv('.env')
client = discord.Client()

def startup():
    print("Starting discord bot...")
    client.run(os.getenv("botToken"))

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')



if __name__ == '__main__':
    startup()
