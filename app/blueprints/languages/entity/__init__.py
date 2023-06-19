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
# See the License for the specific languages governing permissions and
# limitations under the License.
#


from adecty_design.properties import Font, Margin
from adecty_design.widgets import Form, Text, InputText, InputButton
from flask import Blueprint, redirect, request

from app.adecty_design.interface import interface
from app.database import Language


blueprint_language = Blueprint(
    name='blueprint_language',
    import_name=__name__,
    url_prefix='/<int:language_id>'
)


@blueprint_language.route('/delete', methods=['GET', 'POST'])
def language_delete(language_id):
    language = Language.get_by_id(language_id)
    language.delete_instance()
    return redirect('/languages')


@blueprint_language.route('/update', methods=['GET', 'POST'])
def language_update(language_id):
    language = Language.get_by_id(language_id)
    if not language:
        return redirect('/languages')

    if request.method == 'POST':
        language.name = request.form.get('name')
        language.save()
        return redirect('/languages')

    widgets = [
        Text(
            text='Редактирование языка',
            font=Font(size=32, weight=700),
            margin=Margin(down=16),
        ),
        Form(
            widgets=[
                Text(
                    text='Название языка',
                    font=Font(size=14, weight=700),
                ),
                InputText(id='name', value=language.name),
                InputButton(text='Сохранить', margin=Margin(top=8)),
            ],
        ),
    ]
    interface_html = interface.html_get(
        widgets=widgets,
        active='items',
    )
    return interface_html
