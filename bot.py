import os, asyncio
from xgorn_api import NoidAPI
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Environments / Configs
API_HASH = os.environ.get('API_HASH', '2c015c994c57b312708fecc8a2a0f1a6')
APP_ID = int(os.environ.get('APP_ID', 15830858))
BOT_TOKEN = os.environ.get('BOT_TOKEN', '6356894716:AAFKniX_OeErKo3gUfS0pryfbrIo6lkxDRg')
API_KEY = os.environ.get('API_KEY', '8Mlzmd2031mrdlgz')
OWNER_ID = os.environ.get('OWNER_ID', 5468192421)

# See Docs for more details (api.xgorn.pp.ua/docs)
SAMPLER = os.environ.get('SAMPLER', 'k_euler_a')
MODEL = os.environ.get('MODEL', 'anime')
GENDER = os.environ.get('GENDER', 'female')
NSFW = os.environ.get('NSFW', 'true)


api = NoidAPI()

api.api_key = API_KEY

# Helpers
def get_text(update) -> [None, str]:
    text_to_return = update.text
    if update.text is None:
        return None
    if " " in text_to_return:
        try:
            return update.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None

# Button
START_BUTTONS=[
    [
        InlineKeyboardButton('Source', url='https://github.com/X-Gorn/Anime-Ai'),
        InlineKeyboardButton('Rest API', url='https://api.xgorn.pp.ua'),
    ],
    [InlineKeyboardButton('Author', url="https://t.me/xgorn")],
]



# Running bot
xbot = Client('Anime-Ai', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Notify about bot start
with xbot:
    xbot_username = xbot.get_me().username  # Better call it global once due to telegram flood id
    print("Bot started!")
    xbot.send_message(int(OWNER_ID), "Bot started!")


# Start message
@xbot.on_message(filters.command('start') & filters.private)
async def _start(bot, update):
    await update.reply_text(
        f"I'm Anime-Ai!\nYou can generate anime art with words!\n\nUsage: `/animeai girl with red hair`",
        True, 
        reply_markup=InlineKeyboardMarkup(START_BUTTONS)
    )


# Generating
@xbot.on_message(filters.command('animeai') & filters.private)
async def _animeai(bot, update):
    prompt = get_text(update)
    if prompt:
        x = await update.reply('Wait for 10~20 seconds..')
        await bot.send_chat_action(update.from_user.id, enums.ChatAction.UPLOAD_PHOTO)
        result = api.make_request('post', '/ai/silmin_generate', prompt=prompt, sampler=SAMPLER, gender=GENDER, model=MODEL, nsfw=NSFW)
        if not result['error']:
            count = 1
            while True:
                await asyncio.sleep(10)
                task = api.make_request('post', '/ai/silmin_task', task_id=result['task_id'])
                if not task['error']:
                    break
                else:
                    if count > 5:
                        break
                    count+=1
            await x.delete()
            await update.reply_photo(task['image'])
        else:
            await x.edit(result['message'])


xbot.run()
