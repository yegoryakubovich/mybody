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


from adecty_design.properties import Margin, Font
from adecty_design.widgets import Card, InputText, InputButton, Form, Button, ButtonType, Text
from flask import Blueprint, request, redirect
from app.adecty_design.interface import interface
from app.database import Text as TextDB, Translate, Language
from app.decorators.admin_get import admin_get


blueprint_items = Blueprint(
    name='blueprint_items',
    import_name=__name__,
    url_prefix='/items'
)


@blueprint_items.route(rule='/', endpoint='get', methods=['GET', 'POST'])
@admin_get(not_return=True)
def items_get():
    widgets = [
        Button(
            type=ButtonType.chip,
            text='Создать текст',
            url='/items/create',
        ),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='items',
    )
    return interface_html


# FIXME
@blueprint_items.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get(not_return=True)
def items_create():
    text_key_value = None
    text_description_value = None
    default_text_value = None

    if request.method == 'POST':
        text_key_value = request.form.get('text_key')
        text_description_value = request.form.get('text_description')
        default_text_value = request.form.get('default_text')

        if not text_key_value or not text_description_value or not default_text_value:
            error_message = 'Все поля должны быть заполнены.'
            error_card = Card(widgets=[
                Text(
                    text=error_message,
                    font=Font(size=16),
                )
            ])
            interface_html = interface.html_get(widgets=[
                Text(
                    text='Создать текст',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Form(widgets=[
                    Text(
                        text='Ключ',
                        font=Font(
                            size=14,
                            weight=700,
                        )
                    ),
                    InputText(id='text_key', value=text_key_value),
                    Text(
                        text='Текст по умолчанию',
                        font=Font(
                            size=14,
                            weight=700,
                        )
                    ),
                    InputText(id='default_text', value=default_text_value),
                    InputButton(text='Создать', margin=Margin(horizontal=8))
                ]),
                error_card
            ])
            return interface_html

        existing_text = TextDB.get_or_none(TextDB.key == text_key_value)
        if existing_text:
            error_message = 'Запись с таким ключом уже существует.'
            error_card = Card(widgets=[
                Text(
                    text=error_message,
                    font=Font(size=16),
                )
            ])
            interface_html = interface.html_get(widgets=[
                Text(
                    text='Создать текст',
                    font=Font(
                        size=32,
                        weight=700,
                    ),
                    margin=Margin(down=16),
                ),
                Form(widgets=[
                    Text(
                        text='Ключ',
                        font=Font(
                            size=14,
                            weight=700,
                        )
                    ),
                    InputText(id='text_key', value=text_key_value),
                    Text(
                        text='Описание',
                        font=Font(
                            size=14,
                            weight=700,
                        )
                    ),
                    InputText(id='text_description', value=text_description_value),
                    Text(
                        text='Текст по умолчанию',
                        font=Font(
                            size=14,
                            weight=700,
                        )
                    ),
                    InputText(id='default_text', value=default_text_value),
                    InputButton(text='Создать', margin=Margin(horizontal=8))
                ]),
                error_card
            ])
            return interface_html

        text = TextDB.create(key=text_key_value, description=text_description_value, default_text=default_text_value)
        russian_language = Language.get(name='Русский')
        translate = Translate.create(language=russian_language, text=text, value=default_text_value)
        translate.save()
        return redirect('/items')

    widgets = [
        Text(
            text='Создать текст',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(widgets=[
            Text(
                text='Ключ',
                font=Font(
                    size=14,
                    weight=700,
                )
            ),
            InputText(id='text_key', value=text_key_value),
            Text(
                text='Описание',
                font=Font(
                    size=14,
                    weight=700,
                )
            ),
            InputText(id='text_description', value=text_description_value),
            Text(
                text='Текст по умолчанию',
                font=Font(
                    size=14,
                    weight=700,
                )
            ),
            InputText(id='default_text', value=default_text_value),
            InputButton(text='Создать', margin=Margin(horizontal=8))
        ]),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='items',
    )

    return interface_html
