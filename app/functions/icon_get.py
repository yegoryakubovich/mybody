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


from adecty_design.widgets.icon import Icon

from app.database import Language, Translate


def icon_get(filename: str) -> Icon:
    return Icon(
        path=f'app/icons/{filename}'.format(
            filename=filename,
        ),
    )


def create_default_translation(text, value):
    russian_language = Language.get(name='Русский')
    translate = Translate.create(language=russian_language, text=text, value=value)
    translate.save()
