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
from adecty_design.widgets import Text, Button, ButtonType, Card, View, ViewType
from flask import Blueprint
from app.adecty_design.interface import interface
from app.blueprints.aticles.article import blueprint_article
from app.database.models import Article, Account
from app.decorators.user_get import user_get

blueprint_articles = Blueprint(
    name='blueprint_articles',
    import_name=__name__,
    url_prefix='/articles'
)

blueprint_articles.register_blueprint(blueprint=blueprint_article)


@blueprint_articles.route(rule='/', endpoint='articles_get', methods=['GET', 'POST'])
@user_get()
def articles_get(account: Account):
    articles = Article.select()
    widgets = [
        Text(
            text="Эти статьи могут вас заинтересовать",
            font=Font(size=18, weight=600),
            margin=Margin(down=16),
        )
    ]
    print(articles)
    for article in articles:
        if article.status:
            article_text = article.name.value_get(account)
            article_widget = Card(
                margin=Margin(down=16),
                widgets=[
                    Text(text=f"{article_text}", font=Font(size=16)),
                    View(
                        type=ViewType.horizontal,
                        widgets=[
                            Button(
                                type=ButtonType.chip,
                                text='Читать',
                                margin=Margin(horizontal=8, right=6),
                                url=f'/article/{article.id}',
                            )
                        ],
                    ),
                ]
            )
            widgets.append(article_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html
