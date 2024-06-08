import requests
import json
from typing import Dict,List
import asyncio
from bilibili_api import user, sync, Credential


credential = Credential(sessdata="xxxxxxxxxxxxxxxx")
u = user.User(123123123123,credential=credential)

HEADERS: Dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

async def fetch_dyn():
    page = await u.get_dynamics(0)
    # print(page['cards'][0]['desc'])
    return page['cards'][0]['desc']

async def get_info_live():
    data = await u.get_live_info()
    return data

