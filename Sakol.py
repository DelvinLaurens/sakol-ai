import discord
from discord.ext import commands
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# Ambil token dari Environment variable
GROQ_API_KEY = os.environ['GROQ_API_KEY']
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

if not GROQ_API_KEY or not DISCORD_TOKEN:
    raise ValueError("API KEY atau DISCORD TOKEN belum di set!")

# Client Groq untuk AI
groq_client = Groq(api_key=GROQ_API_KEY)

# Bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!sk", intents=intents)

@bot.event
async def on_ready():
    print("Bot AI sudah online!")

@bot.command()
async def hallo(ctx, *, prompt):
    response = groq_client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    await ctx.send(reply)

bot.run(DISCORD_TOKEN)