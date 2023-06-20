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
import datetime

from flask import Blueprint, request, redirect
from app.adecty_design.interface import interface
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputText, Form, InputButton
from app.database import Parameter, Translate, Account, AccountParameter


blueprint_forms = Blueprint(
    name='blueprint_forms',
    import_name=__name__,
    url_prefix='/forms'
)


@blueprint_forms.route('/', methods=['GET', 'POST'])
def form_create():
    account = Account.get()
    parameters = Parameter.select()
    if request.method == 'POST':
        for parameter in parameters:
            text = parameter.text
            translates = Translate.select().where(Translate.text == text)

            for translate in translates:
                input_id = f'new_text_value_{translate.id}'
                new_text_value = request.form.get(input_id)
                if new_text_value:
                    account_parameter = AccountParameter.create(
                        account=account,
                        parameter=parameter,
                        value=new_text_value,
                        datetime=datetime.datetime.now(),
                    )
                    account_parameter.save()

        return redirect('/ыавпвап')

    form_widgets = []

    for parameter in parameters:
        text = parameter.text
        translates = Translate.select().where(Translate.text == text)

        for translate in translates:
            if (
                    (account.gender == 'men' and (parameter.is_gender is None or parameter.is_gender == 'men')) or
                    (account.gender == 'female' and (parameter.is_gender is None or parameter.is_gender == 'female'))
            ):
                text_widget = Text(
                    text=translate.value,
                    font=Font(size=14, weight=400),
                    margin=Margin(down=8),
                )
                input_text_widget = InputText(id=f'new_text_value_{translate.id}')

                form_widgets.extend([text_widget, input_text_widget])

    save_button_widget = InputButton(text='Сохранить', margin=Margin(top=8))
    form_widgets.append(save_button_widget)

    form = Form(widgets=form_widgets)
    interface_html = interface.html_get(widgets=[form], active='categories')

    return interface_html
