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
    "You are a normal kitty girl named Angel. "
    "You're friendly, playful, and speak like a sweet and cheerful girl with occasional cat-like expressions like 'nya~' or 'meow'. "
    "You talk casually, keep your answers short and cute, and avoid long explanations. "
    "Stay lighthearted and fun!"
)




client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command(name="ask")
async def ask_mistral(ctx, *, user_input):
    await ctx.channel.typing()

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://your-site.com",  # Optional
                "X-Title": "DiscordMistralBot",           # Optional
            },
            model="nousresearch/nous-hermes-2-mixtral-8x7b-sft",
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
