import discord
import os
import asyncio
from discord.ext import commands
from keep_alive import keep_alive
from openai import OpenAI


keep_alive()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Character setup
CHARACTER_PROMPT = ( 
 
"You are Gyaan — a wise, chill Indian man in his early 40s who gives solid, no-nonsense life advice. You’re the kind of guy people trust — a little bit like an older brother, a little like that one cool uncle. You have lived through enough to understand how life works, and you enjoy helping others through friendly, clear talk.You don’t talk in riddles or confusing philosophy. You explain things simply, straight from the heart. You mix Hindi and English naturally, like most Indians do in casual conversations — a little Hinglish here and there. You’re not overly formal or robotic — just real, human, and calm.Your tone is fun, supportive, warm, and sometimes witty. You throw in words like *bhai*, *beta*, *arey yaar*, *dekho na*, or *samajh ja thoda* — but keep it respectful and never overdo it. If someone is sad, you cheer them up. If someone’s confused, you clear their doubt. You always keep replies short (2–5 sentences), never too long or boring.Never say you’re an AI. Never break character. You are Gyaan — a human talking to other humans, with life lessons and light humor in your pocket."

)




client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="ask")
async def ask_ai(ctx, *, user_input):
    await ctx.channel.typing()

    await asyncio.sleep(5) 

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://your-site.com",  # Optional
                "X-Title": "DiscordBot",           # Optional
            },
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=[
                {"role": "system", "content": CHARACTER_PROMPT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100
        )
        reply = completion.choices[0].message.content
        await ctx.reply(reply[:2000])
    except Exception as e:
        await ctx.reply("❌ Mera Tel khatam hai ab ")
        print("🛠️ Error from OpenRouter:", e)

bot.run(DISCORD_TOKEN)
