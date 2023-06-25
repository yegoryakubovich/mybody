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


from flask import Flask
from app.blueprints import blueprint_main
from app.database import tables_create
from app.flask import before_request, teardown_request
from config import SETTINGS_KEY


def app_create():
    tables_create()
    app = Flask(import_name=__name__)
    app.secret_key = SETTINGS_KEY
    app.before_request(f=before_request)
    app.teardown_request(f=teardown_request)
    app.register_blueprint(blueprint=blueprint_main)
    return app
