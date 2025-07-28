# discord_gemini_bot/main.py
#
# A free-tier AI Discord bot powered by Gemini 1.5 Pro.
# Commands:
#   !ask  <prompt>      – normal chat response
#   !short <prompt>     – concise reply (max 60 tokens)

import os, asyncio, discord, google.generativeai as genai
from dotenv import load_dotenv




# ── 1  LOAD SECRETS ─────────────────────────────────────────────
load_dotenv()  # reads .env
TOKEN = os.getenv("DISCORD_TOKEN")
APIKEY = os.getenv("GEMINI_API_KEY")
if not TOKEN or not APIKEY:
    raise RuntimeError("DISCORD_TOKEN or GEMINI_API_KEY missing")

# ── 2  SET UP GEMINI MODEL ──────────────────────────────────────
genai.configure(api_key=APIKEY)
MODEL = genai.GenerativeModel("gemma-3-27b-it")


# quick helper so we don’t block the Discord event loop
async def gemini_reply(prompt: str, max_tokens=256) -> str:
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: MODEL.generate_content(
                prompt,
                safety_settings={                 # basic content filter
                    "HARASSMENT": "BLOCK_ONLY_HIGH",
                    "HATE":       "BLOCK_ONLY_HIGH",
                    "SEXUAL":     "BLOCK_ONLY_HIGH",
                },
                generation_config={
                    "temperature": 0.7,
                    "max_output_tokens": max_tokens,
                },
            ),
        )
        return response.text.strip()
    except Exception as err:
        print("Gemini error:", err)
        return "⚠️ Sorry, I couldn’t process that just now."


# ── 3  DISCORD BOT ──────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID {bot.user.id})")


@bot.event
async def on_message(msg: discord.Message):
    if msg.author == bot.user:
        return

    content = msg.content.strip()
    if content.startswith("!ask "):
        prompt = content[5:].strip()
        if not prompt:
            return await msg.reply("Usage: `!ask your question`")

        async with msg.channel.typing():
            reply = await gemini_reply(prompt, 256)
        await msg.reply(reply, mention_author=False)

    elif content.startswith("!short "):
        prompt = content[7:].strip()
        if not prompt:
            return await msg.reply("Usage: `!short your question`")

        async with msg.channel.typing():
            reply = await gemini_reply(prompt, 60)
        await msg.reply(reply, mention_author=False)





# ── 4  RUN ──────────────────────────────────────────────────────
bot.run(TOKEN)
