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
from adecty_design.properties import Font, Margin
from adecty_design.widgets import Text, InputButton, Button, ButtonType, Form, InputSelect, InputText
from flask import Blueprint, request, redirect

from app.adecty_design.interface import interface
from app.database.models import Article, Translate, ArticleItem
from app.database import Text as TextDB
from app.functions.icon_get import create_default_translation

blueprint_articles = Blueprint(
    name='blueprint_articles',
    import_name=__name__,
    url_prefix='/articles'
)


@blueprint_articles.route('/', methods=['GET'])
def articles_page():
    articles = Translate.select(Translate.value).execute()

    widgets = [
        Text(
            text='Статьи',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Button(
            type=ButtonType.chip,
            text='Создать',
            url='/articles/create'
        ),
        Text(
            text='Список статей:',
            font=Font(
                size=14,
                weight=700,
            ),
            margin=Margin(down=8),
        ),
    ]

    for article in articles:
        article_widget = Text(text=article.value)
        widgets.append(article_widget)

    interface_html = interface.html_get(widgets=widgets)
    return interface_html


@blueprint_articles.route('/create', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        text = request.form.get('text')
        header = request.form.get('header')
        subheader_text = request.form.get('subheader_text')
        headers = request.form.get('headers')
        resource_link = request.form.get('resource_link')

        # Создаем текст статьи
        article_text = TextDB()
        article_text.save()

        # Создаем статью в базе данных
        new_article = Article(name=article_text)
        new_article.save()

        # Создаем элементы статьи и устанавливаем связь с созданной статьей
        article_items = []
        for i, header in enumerate([header, text, subheader_text, headers, resource_link], start=1):
            article_item = ArticleItem(article=new_article, path=i)
            article_item.save()
            article_items.append(article_item)

        # Сохраняем тексты в базе данных
        translate_entries = [
            create_default_translation(article_text, value)
            for value in [name, text, header, subheader_text, headers, resource_link]
        ]

        return redirect('/')

    # Отображаем форму создания статьи
    widgets = [
        Text(
            text='Создание статьи',
            font=Font(
                size=32,
                weight=700,
            ),
            margin=Margin(down=16),
        ),
        Form(widgets=[
            Text(
                text='Название статьи',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputText(id='name'),
            Text(
                text='Текст',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputText(id='text'),
            Text(
                text='Заголовок',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputText(id='header'),
            Text(
                text='Текст под заголовком',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputText(id='subheader_text'),
            Text(
                text='Заголовок 2',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputText(id='headers'),
            Text(
                text='Ссылка на ресурс',
                font=Font(
                    size=14,
                    weight=700,
                ),
            ),
            InputText(id='resource_link'),
            InputButton(text='Сохранить', margin=Margin(horizontal=8)),
        ]),
    ]

    interface_html = interface.html_get(widgets=widgets)
    return interface_html




