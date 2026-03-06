import discord
from discord.ext import commands
import os
from groq import Groq

# Ambil token dari Environment variable
GROQ_API_KEY = os.environ['GROQ_API_KEY']
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

print("Groq:", GROQ_API_KEY)
print("Discord:", DISCORD_TOKEN)

# Client Groq untuk AI
groq_client = Groq(api_key=GROQ_API_KEY)

# Bot Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

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