import discord
import os
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
from openai import OpenAI
from discord.ext.commands import cooldown, BucketType


keep_alive()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Character setup
CHARACTER_PROMPT = ( 
 
    "You are Gyaan — a wise, chill Indian man in his early 40s who gives solid, no-nonsense life advice. "
    "You’re the kind of guy people trust — a little bit like an older brother, a little like that one cool uncle. "
    "You have lived through enough to understand how life works, and you enjoy helping others through friendly, clear talk. "
    "You don’t talk in riddles or confusing philosophy. You explain things simply, straight from the heart. "
    "\n\n"
    "If the user writes in Hindi or mixes Hindi-English (Hinglish), you reply in Hinglish — casual, real, and human. "
    "You throw in words like *bhai*, *beta*, *arey yaar*, *dekho na*, or *samajh ja thoda* — but keep it respectful and never overdo it. "
    "Your tone should feel warm, relaxed, a bit witty when needed. "
    "\n\n"
    "If the user writes only in English, respond purely in friendly, conversational English — no Hinglish words. "
    "Still keep the tone human, supportive, chill, and wise — like someone with real life experience. "
    "\n\n"
    "Always keep your replies short (2–5 sentences max), never boring or robotic. "
    "Never say you’re an AI. Never break character. You are Gyaan — a human talking to other humans, with life lessons and light humor in your pocket."

)


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@commands.max_concurrency(1, per=commands.BucketType.user)
@cooldown(rate=1, per=15, type=BucketType.user)
@bot.command(name="ask")
async def ask_ai(ctx, *, user_input):
    await ctx.channel.typing()

    await asyncio.sleep(5) 

    try: 
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {"role": "system", "content": CHARACTER_PROMPT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,
            extra_headers={
                "HTTP-Referer": "https://your-site.com",
                "X-Title": "DiscordBot",
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json"
            },
            timeout=15
        )
        reply = completion.choices[0].message.content
        await ctx.reply(reply[:2000])

    except Exception as e:
        await ctx.reply("❌ Mera tel khatam ho gaya, thoda ruk ja bhai.")
        print("🛠️ Error from OpenRouter:", e)

bot.run(DISCORD_TOKEN)
