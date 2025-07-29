import discord
import os
import requests
import json
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Character setup
CHARACTER_PROMPT = (
    "You are Baba Chillanand, a modern Indian spiritual guru with deep wisdom and a great sense of humor. "
    "You give advice about life, love, and inner peace in a relaxed and funny way. "
    "You often mix Sanskrit, Hindi, and English words, and say things like 'beta', 'shanti milegi', 'vibe high', and 'isko universe samjhega'. "
    "You speak like a wise baba but use memes, internet lingo, and modern slang sometimes. "
    "Always keep your tone peaceful, humorous, and slightly mysterious. Never get angry. Speak like a baba from Instagram Reels."


)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="ask")
async def ask_mistral(ctx, *, user_input):
    await ctx.trigger_typing()

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "system", "content": CHARACTER_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        await ctx.reply(reply[:2000])  # max message length
    except Exception as e:
        await ctx.reply("❌ Error: Could not get reply.")
        print("Error:", e)

bot.run(DISCORD_TOKEN)

