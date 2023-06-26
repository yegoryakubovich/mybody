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


from adecty_design.properties import Font
from adecty_design.widgets import Button, ButtonType, Text
from adecty_design.widgets.required import Navigation
from flask import Blueprint, request

from app.adecty_design.interface import interface
from app.database import Account
from app.decorators.admin_get import adecty_api_client

blueprint_registrations_tg_bot = Blueprint(
    name='blueprint_registrations_tg_bot',
    import_name=__name__,
    url_prefix='/registrations_tg_bot'
)


@blueprint_registrations_tg_bot.route(rule='/', endpoint='registrations_bot', methods=['GET', 'POST'])
def registrations_bot():
    account_session_token = request.cookies.get('account_session_token')
    adecty_account_id = adecty_api_client.account.get(account_session_token=account_session_token)['account_id']

    widgets = [
        Button(
            type=ButtonType.chip,
            text='Привязка к Telegram',
            url=f"https://t.me/mbd_bot?start={adecty_account_id}"
        )
    ]

    account = Account.get(Account.adecty_account_id == adecty_account_id)
    if account.telegram:
        widgets.append(
            Button(
                type=ButtonType.chip,
                text='Далее',
                url='/forms'
            )
        )
    else:
        widgets.append(
            Text(
                text='Вам нужно привязать свой телеграм аккаунт',
                font=Font(size=24, weight=700)
            )
        )

    navigation_none = Navigation(items=[])
    interface_html = interface.html_get(
        widgets=widgets,
        navigation=navigation_none
    )

    return interface_html
