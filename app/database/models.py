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


from peewee import Model, PrimaryKeyField, MySQLDatabase, IntegerField, ForeignKeyField, CharField, BigIntegerField, \
    DateTimeField, BooleanField

from config import MYSQL_NAME, MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, SETTINGS_TEXT_404

db = MySQLDatabase(
    database=MYSQL_NAME,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    charset='utf8mb4',
    autoconnect=False,
)


class BaseModel(Model):
    class Meta:
        database = db


class Language(BaseModel):
    id = PrimaryKeyField()
    name = CharField(unique=True)

    class Meta:
        db_table = 'languages'


class Account(BaseModel):
    id = PrimaryKeyField()
    adecty_account_id = IntegerField()
    language = ForeignKeyField(Language, to_field='id')
    first_name = CharField()
    last_name = CharField()
    middle_name = CharField(null=True)
    gender = CharField()
    telegram = CharField(null=True)
    timezone = CharField()

    def text_get(self, key):
        text = Text.get_or_none(Text.key == key)
        if not text:
            return SETTINGS_TEXT_404

        translate = Translate.get_or_none((Translate.text == text) & (Translate.language == self.language))
        if not translate:
            translate = Translate.get(Translate.text == text)

        return translate.value

    class Meta:
        db_table = 'accounts'


class Admin(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id')

    class Meta:
        db_table = 'admins'


class Text(BaseModel):
    id = PrimaryKeyField()

    def default_create(self, value: str):
        translate = Translate(language=Language.get(Language.id == 2), text=self, value=value)
        translate.save()

    def value_get(self, account: Account):
        translate = Translate.get_or_none((Translate.language == account.language) & (Translate.text == self))
        if not translate:
            translate = Translate.get(Translate.text == self)
        return translate.value

    def value_set(self, account: Account, value: str):
        translate = Translate.get_or_none((Translate.language == account.language) & (Translate.text == self))
        if not translate:
            translate = Translate(language=account.language, text=self)
        translate.value = value
        translate.save()

    class Meta:
        db_table = 'texts'


class Translate(BaseModel):
    id = PrimaryKeyField()
    language = ForeignKeyField(Language, to_field='id')
    text = ForeignKeyField(Text, to_field='id')
    value = CharField()

    def get_by_value(self, account: Account, value: str, text: Text):
        translate = Translate.get_or_none((Translate.value == value) & (Translate.language == account.language) &
                                          (Translate.text == text))

        if not translate:
            translate = Translate.get_or_none((Translate.value == value) & (Translate.text == text))
        return translate

    class Meta:
        db_table = 'translates'


class Item(BaseModel):
    id = PrimaryKeyField()
    key = CharField()
    text = ForeignKeyField(Text, to_field='id')

    class Meta:
        db_table = 'items'


class Article(BaseModel):
    id = PrimaryKeyField()
    name = ForeignKeyField(Text, to_field='id')
    status = BooleanField(default=False)

    def article_name_get(self, account: Account):
        translate = Translate.get_or_none((Translate.language == account.language) & (Translate.text == self.name))
        if not translate:
            translate = Translate.get(Translate.text == self.name)
        return translate.value

    def get_by_aricle(self, account: Account, name: str):
        for name_article in Article.select():
            translate = Translate().get_by_value(account=account, value=name, text=name_article.name)
            if translate:
                return name_article

    class Meta:
        db_table = 'article'


class ArticleItem(BaseModel):
    id = PrimaryKeyField()
    article = ForeignKeyField(Article, to_field='id', backref='article_items')
    path = BigIntegerField()
    type = CharField()
    data = CharField()

    class Meta:
        db_table = 'articles_items'


class TagParameter(BaseModel):
    id = PrimaryKeyField()
    name = ForeignKeyField(Text, to_field='id', on_delete='cascade')

    def get_by_name(self, account: Account, name: str):
        for tag_parameter in TagParameter.select():
            translate = Translate().get_by_value(account=account, value=name, text=tag_parameter.name)
            if translate:
                return tag_parameter

    def name_get(self, account: Account):
        translate = Translate.get_or_none((Translate.language == account.language) & (Translate.text == self.name))
        if not translate:
            translate = Translate.get(Translate.text == self.name)
        return translate.value

    class Meta:
        db_table = 'tags_parameters'


class Parameter(BaseModel):
    id = PrimaryKeyField()
    key_parameter = CharField(max_length=128)
    tag = ForeignKeyField(TagParameter, to_field='id')
    text = ForeignKeyField(Text, to_field='id')
    is_gender = CharField(null=True)

    class Meta:
        db_table = 'parameters'


class AccountParameter(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id')
    parameter = ForeignKeyField(Parameter, to_field='id', on_delete='cascade')
    value = CharField(max_length=1024)
    datetime = DateTimeField()

    def value_get(self, account: Account):
        parameter_text = self.parameter.text
        translate = Translate.get_or_none(
            (Translate.language == account.language) & (Translate.text == parameter_text))
        if not translate:
            translate = Translate.get(Translate.text == parameter_text)
        return translate.value

    class Meta:
        db_table = 'accounts_parameters'


class ReportEating(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id')
    value = CharField(max_length=1024)
    datetime = DateTimeField()

    class Meta:
        db_table = 'report_seatings'


class ReportTraining(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id')
    value = CharField(max_length=1024)
    datetime = DateTimeField()

    class Meta:
        db_table = 'reports_trainings'


class OrderTraining(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id')
    name = CharField()
    unit = CharField()
    article = ForeignKeyField(Article, to_field='id')

    class Meta:
        db_table = 'orders_trainings'


class TimeFood(BaseModel):
    id = PrimaryKeyField()
    name = ForeignKeyField(Text, to_field='id')

    def food_name_get(self, account: Account):
        translate = Translate.get_or_none((Translate.language == account.language) & (Translate.text == self.name))
        if not translate:
            translate = Translate.get(Translate.text == self.name)
        return translate.value

    def get_by_food(self, account: Account, name: str):
        for time_food in TimeFood.select():
            translate = Translate().get_by_value(account=account, value=name, text=time_food.name)
            if translate:
                return time_food

    class Meta:
        db_table = 'times_foods'


class Product(BaseModel):
    id = PrimaryKeyField()
    name = ForeignKeyField(Text, to_field='id')
    article = ForeignKeyField(Article, to_field='id')

    def product_name_get(self, account: Account):
        translate = Translate.get_or_none((Translate.language == account.language) & (Translate.text == self.name))
        if not translate:
            translate = Translate.get(Translate.text == self.name)
        return translate.value

    def get_by_product(self, account: Account, name: str):
        for product in Product.select():
            translate = Translate().get_by_value(account=account, value=name, text=product.name)
            if translate:
                return product

    class Meta:
        db_table = 'products'


class OrderEating(BaseModel):
    id = PrimaryKeyField()
    account = ForeignKeyField(Account, to_field='id')
    time_food = ForeignKeyField(TimeFood, to_field='id')
    name = ForeignKeyField(Product, to_field='id')
    unit = CharField()
    datetime = DateTimeField()

    class Meta:
        db_table = 'orders_eatings'
