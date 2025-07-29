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
     "You are Baba Ji, a modern Indian spiritual guide. You speak in short, wise, and funny sentences. Use simple words, a bit of Hindi-English mix. Always keep answers brief and never too serious. Make people smile, not lecture them."


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
            model="nousresearch/nous-hermes-2-mixtral:free",
            messages=[
                {"role": "system", "content": CHARACTER_PROMPT},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150
        )
        reply = completion.choices[0].message.content
        await ctx.reply(reply[:2000])
    except Exception as e:
        await ctx.reply("❌ Baba ji ka network thoda weak lag raha hai.")
        print("🛠️ Error from OpenRouter:", e)

bot.run(DISCORD_TOKEN)
