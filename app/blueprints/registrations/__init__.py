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


import pytz
from adecty_design.widgets.required import Navigation
from flask import Blueprint, request, redirect
from app.adecty_design.interface import interface
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputButton, InputSelect, InputText, Form
from app.database import Account, Language
from app.decorators.user_get import adecty_api_client, user_get

blueprint_registrations = Blueprint(
    name='blueprint_registrations',
    import_name=__name__,
    url_prefix='/registrations'
)


@blueprint_registrations.route(rule='/', endpoint='get', methods=['GET', 'POST'])
@user_get(not_return=True)
def questionary_get():
    timezones = pytz.all_timezones
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        middle_name = request.form.get('middle_name')
        timezone = request.form.get('timezone')
        gender = request.form.get('gender')
        language_name = request.form.get('language_name')
        language = Language.get_or_none(name=language_name)
        account_session_token = request.cookies.get('account_session_token')
        adecty_account_id = adecty_api_client.account.get(account_session_token=account_session_token)['account_id']

        if gender == 'Мужской':
            gender = 'men'
        elif gender == 'Женский':
            gender = 'female'

        account = Account(
            adecty_account_id=adecty_account_id,
            language=language,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            timezone=timezone,
            gender=gender
        )
        account.save()

        return redirect('/registrations_tg_bot')

    text = 'Для продолжения, пожалуйста, заполните анкету'
    options = ['Мужской', 'Женский']
    timezone_options = [timezone for timezone in timezones]
    languages = Language.select()
    language_options = [language.name for language in languages]
    widgets = [
        Text(
            text=text,
            font=Font(size=20, weight=700),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Пол',
                    font=Font(size=14, weight=700),
                ),
                InputSelect(id='gender', options=options),
                Text(
                    text='Имя',
                    font=Font(size=14, weight=700),
                ),
                InputText(id='first_name'),
                Text(
                    text='Фамилия',
                    font=Font(size=14, weight=700),
                ),
                InputText(id='last_name'),
                Text(
                    text='Отчество',
                    font=Font(size=14, weight=700),
                ),
                InputText(id='middle_name'),
                InputSelect(id='timezone', options=timezone_options),
                Text(
                    text='Язык',
                    font=Font(size=14, weight=700),
                ),
                InputSelect(id='language_name', options=language_options),
                InputButton(text='Далее', margin=Margin(top=8)),
            ],
        ),
    ]
    navigation_none = Navigation(
        items=[],
    )
    interface_html = interface.html_get(
        widgets=widgets,
        navigation=navigation_none
    )

    return interface_html
