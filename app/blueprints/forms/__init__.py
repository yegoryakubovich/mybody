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


from flask import Blueprint, request, redirect, url_for
from app.adecty_design.interface import interface
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputText, Form, InputButton
from app.database import Parameter, Translate, Account, AccountParameter, TagParameter

blueprint_forms = Blueprint(
    name='blueprint_forms',
    import_name=__name__,
    url_prefix='/forms'
)


@blueprint_forms.route('/', endpoint='create', methods=['GET', 'POST'])
def form_create():
    account = Account.get()
    parameters = Parameter.select().join(TagParameter).order_by(TagParameter.id)
    account_parameters = AccountParameter.select().where(AccountParameter.account == account)
    account_parameter_ids = [ap.parameter.id for ap in account_parameters]
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

        unanswered_parameters = [p for p in parameters if p.id not in account_parameter_ids]
        if unanswered_parameters:
            next_tag_id = unanswered_parameters[0].tag.id
            return redirect(url_for('blueprint_account.blueprint_forms.create', tag_id=next_tag_id))
        else:
            return redirect('/ыавпвап')

    tag_id = request.args.get('tag_id', None)
    form_widgets = []
    current_tag = None
    is_next_tag = False

    heading_widget = Text(
        text='Ответьте на несколько вопросов',
        font=Font(size=18, weight=600),
        margin=Margin(down=16),
    )
    form_widgets.append(heading_widget)

    for parameter in parameters:
        if parameter.id not in account_parameter_ids:
            tag_parameter = parameter.tag
            if current_tag is None:
                current_tag = tag_parameter
            if tag_parameter != current_tag:
                if is_next_tag:
                    break

                current_tag = tag_parameter

            if tag_id and current_tag.id != int(tag_id):
                continue

            text = parameter.text
            translates = Translate.select().where(Translate.text == text)

            for translate in translates:
                if (
                        (account.gender == 'men' and (parameter.is_gender is None or parameter.is_gender == 'men')) or
                        (account.gender == 'female' and (
                                parameter.is_gender is None or parameter.is_gender == 'female'))
                ):
                    text_widget = Text(
                        text=translate.value,
                        font=Font(size=14, weight=400),
                        margin=Margin(down=8),
                    )
                    input_text_widget = InputText(id=f'new_text_value_{translate.id}')

                    form_widgets.extend([text_widget, input_text_widget])

            if not is_next_tag and current_tag == tag_parameter:
                is_next_tag = True

    save_button_widget = InputButton(text='Далее', margin=Margin(top=8))
    form_widgets.append(save_button_widget)

    form = Form(widgets=form_widgets)
    interface_html = interface.html_get(widgets=[form])

    return interface_html
