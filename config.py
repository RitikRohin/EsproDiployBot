import os

API_ID = int(os.getenv("API_ID", 12345))
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
HEROKU_API_KEY = os.getenv("HEROKU_API_KEY", "your_heroku_api_key")

# GitHub repo to deploy
GITHUB_TEMPLATE = "https://github.com/RitikRohin/EsproMusicBot"
