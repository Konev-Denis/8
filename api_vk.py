import requests
from urllib.parse import urlencode
import re

TOKEN = ""

class APIVK:
    def request(self, method, **kwargs):
        kwargs.setdefault('v', '5.8')
        kwargs.setdefault('access_token', TOKEN)
        return requests.get(f'https://api.vk.com/method/{method}?{urlencode(kwargs)}').json()

    def get_user_name(self, user_id):
        try:
            user = self.request('users.get', user_ids=user_id)['response'][0]
        except KeyError:
            print('что-то пошло не так, проверте вводимый вами id')
            return
        print(user["first_name"] + ' ' + user["last_name"] + f' (id {user["id"]})')
        return user["id"]

    def get_friends(self, user_id, count=None):
        id = re.match( r'[A-Za-z]', user_id)
        if id:
            user_id = self.get_user_name(user_id)
        try:
            if count:
                response = self.request('friends.get', user_id=user_id, order='hints', count=count)['response']['items']
            else:
                response = self.request('friends.get', user_id=user_id, order='hints')['response']['items']
        except KeyError:
            print('что-то пошло не так, проверте вводимый вами id')
            return
        if response:
            print("Список друзей:")
            for friend in response:
                self.get_user_name(friend)
        else:
            print('Список друзей пуст')

    def get_albums(self, user_id, count=None):
        id = re.match( r'[A-Za-z]', user_id)
        if id:
            user_id = self.get_user_name(user_id)
        try:
            if count:
                response = self.request('photos.getAlbums', owner_id=user_id, count=count)['response']['items']
            else:
                response = self.request('photos.getAlbums', owner_id=user_id)['response']['items']
        except KeyError:
            print('что-то пошло не так, проверте вводимый вами id')
            return
        if response:
            print('Список альбомов:')
            for items in response:
                print(items['title'])
        else:
            print('Список альбомов пуст')

    def get_members_group(self, group_id, count=None):
        #скорее всего не возможен без авторизации
        try:
            if count:
                response = self.request('groups.getMembers', owner_id=group_id, count=count)['response']['items']
            else:
                response = self.request('groups.getMembers', owner_id=group_id)['response']['items']
        except KeyError:
            if self.request('groups.getMembers', owner_id=group_id, count=count)['error']['error_code'] == 125:
                print('Недопустимый идентификатор сообщества')
                return
            print('что-то пошло не так, проверте вводимый вами id')
            return
        if response:
            print('Список участников группы:')
            for user_id in response:
                print(self.get_user_name(user_id))


if __name__ == '__main__':
    api = APIVK()
    print('Введите команду')
    com = input().split(' ')
    try:
        if com[0] == 'user':
            api.get_user_name(com[1])
        elif com[0] == 'friends':
            id = com[1]
            try:
                count = com[2]
            except IndexError:
                count = None
            api.get_friends(id, count)
        elif com[0] == "albums":
            id = com[1]
            try:
                count = com[2]
            except IndexError:
                count = None
            api.get_albums(id, count)
        else:
            print('Поддерживаемые команды:')
            print('user <user id>')
            print('friends <user id> [count]')
            print('albums <user id> [count]')   
    except IndexError:
        print('Поддерживаемые команды:')
        print('user <user id>')
        print('friends <user id> [count]')
        print('albums <user id> [count]')