#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.database import Account
from config import TELEGRAM_BOT_TOKEN

bot_token = TELEGRAM_BOT_TOKEN
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message):
    tg_id = message.from_user.id

    is_tied = Account.get_or_none(Account.telegram == tg_id)
    account_id = message.text.split()[-1]
    account = Account.get_or_none(Account.id == account_id)

    if is_tied:
        account.telegram = str(tg_id)
        account.save()
        await message.reply('Вас приветствует телеграм бот MyBody')


def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(dp.start_polling())


def stop_bot():
    loop = asyncio.get_event_loop()
    loop.stop()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('aiogram')
dp.logger = logger