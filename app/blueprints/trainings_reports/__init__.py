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


from datetime import datetime

from adecty_design.properties import Margin, Font
from adecty_design.widgets import Text,  InputText, InputButton, Form
from flask import Blueprint, request
from app.adecty_design.interface import interface
from app.database.models import ReportEating, Account
from app.decorators.admin_get import adecty_api_client
from app.decorators.user_get import user_get

blueprint_trainings_reports = Blueprint(
    name='blueprint_trainings_reports',
    import_name=__name__,
    url_prefix='/trainings_reports'
)


@blueprint_trainings_reports.route(rule='/', endpoint='eating_reports', methods=['GET', 'POST'])
@user_get()
def eating_reports():
    if request.method == 'POST':
        value = request.form.get('value')

        account_session_token = request.cookies.get('account_session_token')
        adecty_account_id = adecty_api_client.account.get(account_session_token=account_session_token)['account_id']
        account = Account.get(Account.adecty_account_id == adecty_account_id)
        eating_report = ReportEating(
            account=account.id,
            value=value,
            datetime=datetime.now()
        )
        eating_report.save()

        messages = 'Отчет успешно добавлен.'
        message = Text(
            text=messages,
            font=Font(size=16),
        )

        interface_html = interface.html_get(widgets=[message])
        return interface_html

    widgets = [
        Text(
            text='Опишите в свободной форме что вы сделали, что не получилось и т.д',
            font=Font(
                size=22,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='',
                    font=Font(
                        size=14,
                        weight=700,
                    ),
                ),
                InputText(id='value'),
                InputButton(text='Отправить отчет', margin=Margin(top=8)),
            ]
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='meal_report'
    )

    return interface_html
