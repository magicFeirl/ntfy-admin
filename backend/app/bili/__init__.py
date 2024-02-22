# copy from: https://github.com/magicFeirl/BiliReminder/blob/main/app/bilibili/live.py

import requests


class LiveInfoCrawler(object):
    def __init__(self) -> None:
        pass
    
    @classmethod
    def get_room_master_info(cls, uid: str):
        api = 'https://api.live.bilibili.com/live_user/v1/Master/info'

        return requests.get(api, params={'uid': uid}).json()

    @classmethod
    def get_room_info(cls, room_id: str):
        api = 'https://api.live.bilibili.com/room/v1/Room/get_info'

        return requests.get(api, params={'room_id': room_id}).json()

    @classmethod
    def get_room_info_and_master_info(cls, room_id):
        resp = cls.get_room_info(room_id=room_id)

        if resp['code'] != 0:
            return

        room_info = resp['data']

        uid = room_info.get('uid')
        live_id = str(room_info.get('room_id'))
        title = room_info.get('title')
        user_cover = room_info.get('user_cover')
        live_status = room_info.get('live_status')
        live_time = room_info.get('live_time')

        
        master_info_resp = cls.get_room_master_info(uid=uid)
        user_info = master_info_resp['data']['info']
        username = user_info['uname']

        return {
            "uid": uid,
            "live_id": live_id,
            "title": title,
            "user_cover": user_cover,
            "live_status": live_status,
            "live_time": live_time,
            "username": username,
        }

import re
from string import Template
from datetime import datetime


def format_live_message(room_id: str):
    resp = get_room_info(room_id)

    if resp['code'] != 0:
        return

    room_info = resp['data']

    uid = room_info.get('uid')
    live_id = str(room_info.get('room_id'))
    title = room_info.get('title')
    user_cover = room_info.get('user_cover')
    live_status = room_info.get('live_status')
    live_time = room_info.get('live_time')
    if live_time[:4] != '0000':
        minutes = (datetime.now() - datetime.strptime(live_time,
                   '%Y-%m-%d %H:%M:%S')).total_seconds() / 60
    else:
        minutes = 0

    minutes = round(minutes)

    master_info_resp = get_room_master_info(uid)
    user_info = master_info_resp['data']['info']
    username = user_info['uname']

    message = Template('''
        $title 
        开播时间 $live_time

        $minutes 分钟前
    ''').substitute(title=title, live_time=live_time, minutes=minutes)

    message = re.sub(r'\n\s+(.)', r'\n\g<1>', message.strip())
    actions = f'view, 看!, bilibili://live/{live_id}'.encode(
    ) if live_status == 1 else ''

    return live_status, username, {
        'message': message.encode(),
        'headers': {
            'Title': f'{username}{"开" if live_status == 1 else "下"}播了'.encode(),
            'Attach': user_cover,
            'Tags': 'loudspeaker',
            'Actions': actions
        }
    }