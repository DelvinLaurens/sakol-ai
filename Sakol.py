import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv("secret.env")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

print("Groq:", GROQ_API_KEY)
print("Discord:", DISCORD_TOKEN)

client = Groq(api_key=GROQ_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("Bot AI sudah online!")

@bot.command()
async def hallo(ctx, *, prompt):

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    reply = response.choices[0].message.content
    await ctx.send(reply)

bot.run(DISCORD_TOKEN)

