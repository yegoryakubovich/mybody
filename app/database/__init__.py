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


from app.database.db_manager import db_manager
from app.database.models import db, Admin, Language, Text, Translate, Account, Item, Article, ArticleItem, Parameter, \
    AccountParameter, TagParameter, ReportEating, ReportTraining, OrderTraining, OrderEating, Product, TimeFood

models = [
    Language,
    Account,
    Admin,
    Text,
    Translate,
    Item,
    TagParameter,
    Article,
    ArticleItem,
    Parameter,
    AccountParameter,
    ReportEating,
    ReportTraining,
    OrderTraining,
    OrderEating,
    Product,
    TimeFood
]


@db_manager
def tables_create():
    db.create_tables(
        models=models,
    )
