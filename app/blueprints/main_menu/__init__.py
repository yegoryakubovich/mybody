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


blueprint_main_menu = Blueprint(
    name='blueprint_main_menu',
    import_name=__name__,
    url_prefix='/menu'
)

"""@blueprint_main_menu.route(rule='/', endpoint='menu', methods=['GET', 'POST'])
def menu():"""
