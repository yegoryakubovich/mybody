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
from app.database.models import Article, Account, ArticleItem
from app.decorators.user_get import user_get

blueprint_article = Blueprint(
    name='blueprint_article',
    import_name=__name__,
    url_prefix='/<int:article_id>/'
)


@blueprint_article.route(rule='/', endpoint='get', methods=['GET'])
@user_get(not_return=True)
def articles_select_get(article_id):
    article_items = ArticleItem.select()
    widgets = []
    for article_item in article_items:
        article_widget = Card(
            margin=Margin(down=16),
            widgets=[
                Text(text=f"ID: {article_item.id}", font=Font(size=16)),
                Text(text=f"Path: {article_item.path}", font=Font(size=16)),
                Text(text=f"Type: {article_item.type}", font=Font(size=16)),
                Text(text=f"Data: {article_item.data}", font=Font(size=16)),
            ]
        )
        widgets.append(article_widget)

    interface_html = interface.html_get(
        widgets=widgets,
        active='articles',
    )

    return interface_html
