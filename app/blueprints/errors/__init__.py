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


from adecty_design.properties import Font
from adecty_design.widgets import Text
from flask import Blueprint, request
from werkzeug.exceptions import InternalServerError

from app.adecty_design.interface import interface
from app.decorators.admin_get import admin_get


blueprint_errors = Blueprint('blueprint_errors', __name__)


@blueprint_errors.app_errorhandler(404)
@admin_get(not_return=True)
def errors_404(error: InternalServerError):
    if 'favicon.ico' in request.url:
        return error.get_body()

    widgets = [
        Text(
            text='Page not found',
            font=Font(size=24),
        ),
    ]
    interface_html = interface.html_get(
        widgets=widgets,
    )
    return interface_html
