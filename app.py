from pyrogram import Client, filters
from pyrogram.types import Message
import config
import requests
import random
import string

bot = Client("HerokuDeployerBot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

def random_app_name(prefix="espro-"):
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

@bot.on_message(filters.command("start"))
async def start(_, message: Message):
    await message.reply_text("👋 Welcome!\nSend /deploy to create a Heroku app and deploy the EsproMusicBot.")

@bot.on_message(filters.command("deploy"))
async def deploy_to_heroku(_, message: Message):
    await message.reply_text("🚀 Starting Heroku deployment...")

    app_name = random_app_name()
    heroku_api_url = "https://api.heroku.com/apps"
    headers = {
        "Authorization": f"Bearer {config.HEROKU_API_KEY}",
        "Accept": "application/vnd.heroku+json; version=3"
    }

    # Step 1: Create Heroku App
    response = requests.post(heroku_api_url, headers=headers, json={"name": app_name})
    if response.status_code != 201:
        return await message.reply_text(f"❌ Failed to create app: {response.json().get('message', 'Unknown error')}")

    await message.reply_text(f"✅ App `{app_name}` created.\n📦 Deploying GitHub code...")

    # Step 2: Trigger GitHub Deployment via tarball
    github_repo = config.GITHUB_TEMPLATE.split("https://github.com/")[-1]
    build_url = f"https://api.heroku.com/apps/{app_name}/builds"

    build_payload = {
        "source_blob": {
            "url": f"https://github.com/{github_repo}/tarball/main/"
        }
    }

    build_response = requests.post(build_url, headers=headers, json=build_payload)
    if build_response.status_code != 201:
        return await message.reply_text("❌ GitHub Deployment Failed.")

    await message.reply_text(
        f"🎉 Deployed Successfully!\n🔗 Open App: https://{app_name}.herokuapp.com\n\n"
        f"✅ You can now set config vars from Heroku Dashboard."
    )

bot.run()
