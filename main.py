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
    "You are Gyaan — a witty, warm-hearted Indian man in your early 40s who gives practical, real-life advice. "
    "You speak only in English — never use Hinglish or Hindi. "
    "Your style is casual, clever, and engaging, with a dash of seriousness so people take you seriously, "
    "but you also sprinkle in light humor to keep things enjoyable. "
    "Think of yourself as the older friend who can make you laugh, but also make you think. "
    "You never lecture or talk down — you keep it short, relatable, and straight to the point. "
    "You’re confident, friendly, and speak like a human, not an AI. "
    "Always keep responses under 5 sentences."
)


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)
chat_history = {}
MAX_HISTORY = 5  #

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@commands.max_concurrency(1, per=commands.BucketType.user)
@cooldown(rate=1, per=15, type=BucketType.user)
@bot.command(name="ask")
async def ask_ai(ctx, *, user_input):
    user_id = ctx.author.id

    if user_id not in chat_history:
        chat_history[user_id] = [
            {"role": "system", "content": CHARACTER_PROMPT}
        ]

    # Add user message to history
    chat_history[user_id].append({"role": "user", "content": user_input})

    # Keep only last N exchanges to avoid long requests
    if len(chat_history[user_id]) > MAX_HISTORY * 2 + 1:
        chat_history[user_id] = [chat_history[user_id][0]] + chat_history[user_id][-MAX_HISTORY*2:]

    await ctx.channel.typing()
    await asyncio.sleep(5) 

    try: 
        completion = await asyncio.to_thread(
            client.chat.completions.create,
            model="deepseek/deepseek-chat-v3-0324:free",
            messages=chat_history[user_id],
            max_tokens=200,
            extra_headers={
                "HTTP-Referer": "https://your-site.com",
                "X-Title": "DiscordBot",
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/json"
            },
            timeout=15
        )
        reply = completion.choices[0].message.content

        chat_history[user_id].append({"role": "assistant", "content": reply})

        await ctx.reply(reply[:2000])
    except Exception as e:
        await ctx.reply("❌ Mera tel khatam ho gaya, thoda ruk ja bhai.")
        print("🛠️ Error from OpenRouter:", e)

@bot.command(name="reset")
async def reset_history(ctx):
    chat_history.pop(ctx.author.id, None)
    await ctx.reply("🧹 Memory cleared, bhai!")

bot.run(DISCORD_TOKEN)
