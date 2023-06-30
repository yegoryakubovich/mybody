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


import os
from datetime import datetime


from adecty_design.properties import Margin, Padding, Font
from adecty_design.widgets import Text, InputFile, InputText, InputButton, Form
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename

from app.adecty_design.interface import interface
from app.database.models import ReportEating, Account
from app.decorators.admin_get import adecty_api_client

blueprint_eatings_reports = Blueprint(
    name='blueprint_eatings_reports',
    import_name=__name__,
    url_prefix='/eating_reports'
)

UPLOAD_FOLDER = 'static/eating_reports'

# Сохранение фото не знаю как осуществляться будет, по этому пока написано так
@blueprint_eatings_reports.route(rule='/', endpoint='eating_reports', methods=['GET', 'POST'])
def eating_reports():
    if request.method == 'POST':
        value = request.form.get('value')
        image = request.files.get('image')

        if image:
            filename = secure_filename(image.filename)
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in ['.jpg', '.jpeg', '.png']:
                return 'Только файлы с расширениями JPEG, GIF, PNG допустимы.'

            upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            os.makedirs(upload_path, exist_ok=True)

            file_path = os.path.join(upload_path, filename)
            image.save(file_path)

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
            text='Опишите свой приём пищи в свободной форме, что кушали и в каком количестве, и приложите фото ',
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
                InputFile(
                    id='image',
                    margin=Margin(right=24),
                    padding=Padding(horizontal=2, vertical=2)
                ),
                InputButton(text='Ура я покушала', margin=Margin(top=8)),
            ]
        )
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='meal_report'
    )

    return interface_html
