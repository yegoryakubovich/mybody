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


from adecty_design.properties import Margin, Font, Align, AlignType

from adecty_design.widgets import Card, Text, View, ViewType, Button, ButtonType, InputText, InputButton, Form
from flask import Blueprint, request

from app.adecty_design.interface import interface
from app.blueprints.languages.entity import blueprint_language
from app.database import Language
from app.decorators.admin_get import admin_get


blueprint_languages = Blueprint(
    name='blueprint_languages',
    import_name=__name__,
    url_prefix='/languages'
)
blueprint_languages.register_blueprint(blueprint=blueprint_language)


@blueprint_languages.route(rule='/', endpoint='get', methods=['GET', 'POST'])
@admin_get(not_return=True)
def languages_get():
    languages = Language.select()
    language_widgets = []
    for language in languages:
        language_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text=f"Язык: {language.name}", font=Font(size=16)),
                View(
                    type=ViewType.horizontal,
                    widgets=[
                        Button(
                            type=ButtonType.chip,
                            text='Редактировать',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/languages/{language.id}/update',
                        ),
                        Button(
                            type=ButtonType.chip,
                            text='Удалить',
                            margin=Margin(horizontal=8, right=6),
                            url=f'/languages/{language.id}/delete',
                        ),
                    ],
                ),
            ]
        )

        language_widgets.append(language_widget)

    if not language_widgets:
        empty_message = Text(text="У вас нет языков", font=Font(size=16))
        language_widgets.append(empty_message)

    widgets = [
        View(
            properties_additional=[Align(type=AlignType.space_between)],
            type=ViewType.horizontal,
            widgets=[
                Text(
                    text='Список языков',
                    font=Font(size=32, weight=700),
                    margin=Margin(down=16),
                ),
                Button(
                    type=ButtonType.chip,
                    text='Создать',
                    url='/languages/create',
                )
            ],
        ),
        *language_widgets,
    ]
    interface_html = interface.html_get(
        widgets=widgets,
        active='items',
    )
    return interface_html


@blueprint_languages.route(rule='/create', endpoint='create', methods=['GET', 'POST'])
@admin_get(not_return=True)
def languages_create():
    if request.method == 'POST':
        name = request.form.get('name')

        if not name:
            error_message = 'Поле должно быть заполнено, вернитесь и попробуйте снова.'
            error_card = Card(widgets=[
                Text(
                    text=error_message,
                    font=Font(size=16),
                )
            ])
            interface_html = interface.html_get(widgets=[error_card])
            return interface_html

        language = Language.create(name=name)
        success_message = f'Язык "{language.name}" успешно создан.'
        success_card = Card(widgets=[
            Text(
                text=success_message,
                font=Font(size=16),
            )
        ])
        interface_html = interface.html_get(
            widgets=[success_card],
            active='languages'
        )

        return interface_html

    widgets = [
        Text(
            text='Создание языка',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(widgets=[
            Text(
                text='Название языка',
                font=Font(
                    size=14,
                    weight=700,
                )
            ),
            InputText(id='name'),
            InputButton(text='Создать', margin=Margin(horizontal=8))
        ]),
    ]

    interface_html = interface.html_get(
        widgets=widgets,
        active='items',
    )

    return interface_html
