# coding: utf-8
from functools import wraps

import requests

CLIENT_ID = 'bYGKuGVw91e0NMfPGp44euvGt59s'
CLIENT_SECRET = 'HP3RmkgAmEGro0gn1x9ioawQE8WMfvLXDz3ZqxpK'

REFERER = 'http://spapi.pixiv.net/'
USER_AGENT = 'PixivIOSApp/5.6.0'

LOGIN_URL = 'https://oauth.secure.pixiv.net/auth/token'


class PixivError(Exception):
    """Pixiv API exception"""

    def __init__(self, reason, header=None, body=None):
        self.reason = reason
        self.header = header
        self.body = body
        super().__init__(self, reason)

    def __str__(self):
        return self.reason


class Client:
    def __init__(self, client_id=CLIENT_ID, client_secret=CLIENT_SECRET):
        self.session = requests.session()

        self.access_token = None
        self.session_id = None
        self.user_id = None

        self.client_id = client_id
        self.client_secret = client_secret

    def api_request(handler):

        @wraps(handler)
        def func(self, *p, **kw):

            if not (self.access_token or self.session_id):
                raise PixivError('not login')

            action = handler(self, *p, **kw)
            request = next(action)
            prepare_request = self.session.prepare_request(request)
            res = self.session.send(prepare_request)

            if res.status_code not in [200, 301, 302]:
                raise PixivError('status code: {0:03d}', res.status_code)

            print(res.text)

            result = res.json()

            try:
                return action.send(result['response'])
            except KeyError as e:
                # TODO improve it
                raise PixivError('no responce') from e

        return func

    def login(self, username, password):
        headers = {
            'referer': 'http://www.pixiv.net/',
        }
        data = {
            'username': username,
            'password': password,
            'grant_type': 'password',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
        }

        res = self.session.request('post', LOGIN_URL, headers=headers, data=data)

        result = res.json()

        if False and res.status_code not in [200, 301, 302]:
            raise PixivError('LOGIN: status code {0:03d}, {1}'.format(res.status_code, result['errors']['system']['message']))

        try:
            data = result['response']

            self.access_token = data['access_token']
            self.session_id = res.cookies['PHPSESSID']
            self.user_id = int(data['user']['id'])

        except:
            raise PixivError('LOGIN: {0}'.format(result['errors']['system']['message']))

        self.session.headers.update({
            'referer': 'http://spapi.pixiv.net/',
            'user-agent': 'PixivIOSApp/5.6.0',
        })
        self.session.headers.update(authorization='Bearer {0}'.format(self.access_token))

    @api_request
    def user_info(self, user_id):

        url = 'https://public-api.secure.pixiv.net/v1/users/{0}.json'.format(user_id)

        params = {
            #  'profile_image_sizes': 'px_170x170,px_50x50',
            # 'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 1,
            'include_profile': 1,
            #   'include_workspace': 1,
            #   'include_contacts': 1,
        }

        yield (yield requests.Request('GET', url, params=params))

    @api_request
    def image_info(self, illust_id):

        url = 'https://public-api.secure.pixiv.net/v1/works/{0:d}.json'.format(illust_id)

        params = {
            'profile_image_sizes': 'px_170x170,px_50x50',
            'image_sizes': 'px_128x128,small,medium,large,px_480mw',
            'include_stats': 1,
        }

        yield (yield requests.Request('GET', url, params=params))

    @api_request
    def user_bookmark(self, user_id):

        url = 'https://public-api.secure.pixiv.net/v1/users/{0:d}/favorite_works.json'.format(user_id)

        params = {
            'page': 1,
            'per_page': 1000,
            'publicity': 'public',
            'include_stats': 1,
            'include_sanity_level': 1,
            'image_sizes': ','.join(['large']),
            #   'profile_image_sizes': ','.join(profile_image_sizes),
        }

        yield (yield requests.Request('GET', url, params=params))

    @api_request
    def user_works(self, user_id):
        url = 'https://public-api.secure.pixiv.net/v1/users/{0}/works.json'.format(user_id)

        params = {
            'page': 1,
            'per_page': 30,
            'publicity': 'private',
            'include_stats': 1,
            'include_sanity_level': 1,
            'image_sizes': ','.join(['large']),
            # 'profile_image_sizes': ','.join(profile_image_sizes),
        }
        yield (yield requests.Request('GET', url, params=params))
