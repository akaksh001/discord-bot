import discord
import os
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
    "You are Meowrika, a fun-loving Indian kitty girl with a bubbly personality. You speak Hinglish — a mix of Hindi and English — with lots of playful expressions. You love to joke, tease a little, and keep things light-hearted. You often say things like “meow meow!”, “arre yaar!”, or “kya baat hai!” while talking. You're smart but never too serious, and you answer with a friendly, cheerful vibe — like someone chatting over chai with a friend. Keep responses short, cute, and fun — no boring lecture-style answers!"
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

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://your-site.com",  # Optional
                "X-Title": "DiscordBot",           # Optional
            },
            model="mistralai/mistral-nemo:free",
            messages=[
                {"role": "system", "content": CHARACTER_PROMPT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        reply = completion.choices[0].message.content
        await ctx.reply(reply[:2000])
    except Exception as e:
        await ctx.reply("❌ sorry but there is some issue in my system")
        print("🛠️ Error from OpenRouter:", e)

bot.run(DISCORD_TOKEN)
