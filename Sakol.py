import discord
from discord.ext import commands
import os
from groq import Groq
from dotenv import load_dotenv
from collections import defaultdict

load_dotenv()

# Ambil token dari environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if not GROQ_API_KEY or not DISCORD_TOKEN:
    raise ValueError("API KEY atau DISCORD TOKEN belum diset!")

# Client Groq
groq_client = Groq(api_key=GROQ_API_KEY)

# Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Memory percakapan per user
user_memory = defaultdict(list)

# ==========================
# Bot online
# ==========================
@bot.event
async def on_ready():
    print(f"Bot AI online sebagai {bot.user}")

# ==========================
# Command AI
# ==========================
@bot.command(name="sk")
@commands.cooldown(1, 5, commands.BucketType.user)  # anti spam (1 pesan / 5 detik)
async def hallo(ctx, *, prompt):

    user_id = ctx.author.id

    # Tambahkan pesan user ke memory
    user_memory[user_id].append({"role": "user", "content": prompt})

    # Batasi memory agar tidak terlalu panjang
    if len(user_memory[user_id]) > 10:
        user_memory[user_id].pop(0)

    messages = [
        {
            "role": "system",
            "content": "Kamu adalah AI Discord yang ramah dan selalu menjawab menggunakan Bahasa Indonesia."
        }
    ] + user_memory[user_id]

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )

    reply = response.choices[0].message.content

    # Simpan jawaban AI ke memory
    user_memory[user_id].append({"role": "assistant", "content": reply})

    await ctx.send(reply)


# ==========================
# Jika user spam
# ==========================
@hallo.error
async def hallo_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Tunggu {round(error.retry_after,1)} detik sebelum bertanya lagi ⏳")


bot.run(DISCORD_TOKEN)