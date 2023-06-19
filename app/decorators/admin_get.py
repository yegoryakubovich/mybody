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


from flask import request, redirect

from adecty_api_client.adecty_api_client import AdectyApiClient
from adecty_api_client.adecty_api_client_error import AdectyApiClientError

from app.database.models import Admin, Account
from config import URL_APP, URL_APP_ADMIN


ACCOUNT_SESSION_TOKEN_GET_URL = 'https://account.adecty.com/account/session/token/get?redirect_url={url}'.format(
    url=URL_APP_ADMIN,
)
adecty_api_client = AdectyApiClient()


def admin_get(not_return: bool = False):
    def wrapper(function):
        def validator(*args, **kwargs):
            account_session_token = request.cookies.get('account_session_token')
            if not account_session_token:
                return redirect(location=ACCOUNT_SESSION_TOKEN_GET_URL)
            try:
                adecty_api_client.account.get(account_session_token=account_session_token)
            except AdectyApiClientError:
                return redirect(location=ACCOUNT_SESSION_TOKEN_GET_URL)

            account_id = adecty_api_client.account.get(account_session_token)['account_id']
            account = Account.get_or_none(Account.adecty_account_id == account_id)
            if not account:
                return redirect(location=URL_APP)

            admin = Admin.get_or_none(Admin.account == account)
            if not admin:
                return redirect(location=URL_APP)

            if not not_return:
                kwargs['admin'] = admin

            return function(*args, **kwargs)

        return validator

    return wrapper
