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

from flask import Blueprint, request
from app.adecty_design.interface import interface
from adecty_design.properties import Font
from adecty_design.widgets import Text, InputText
from app.database import Account, Parameter, AccountParameter
from app.decorators.user_get import user_get

blueprint_forms = Blueprint(
    name='blueprint_forms',
    import_name=__name__,
    url_prefix='/forms'
)


@blueprint_forms.route('/', methods=['GET', 'POST'])
def form_create():
    user_gender = Account.get().gender

    if user_gender == 'мужчина':
        query = Parameter.select().where((Parameter.is_gender == 'men') | (Parameter.is_gender.is_null()))
    elif user_gender == 'женщина':
        query = Parameter.select().where((Parameter.is_gender == 'female') | (Parameter.is_gender.is_null()))
    else:
        query = Parameter.select().where(Parameter.is_gender.is_null())

    questions = [parameter.key_parameter for parameter in query]

    widgets = []
    for question in questions:
        widgets.append(Text(
            text=question,
            font=Font(
                size=14,
                weight=700,
            )
        ))
        widgets.append(InputText(id=question.lower().replace(' ', '_'), value=''))

    if request.method == 'POST':
        account = Account.get()
        for question in questions:
            parameter = Parameter.get(Parameter.key_parameter == question)
            value = request.form.get(question.lower().replace(' ', '_'))
            AccountParameter.create(
                account=account,
                parameter=parameter,
                value=value,
                datetime=datetime.now()
            )

    interface_html = interface.html_get(
        widgets=widgets,
        active='registration',
    )

    return interface_html