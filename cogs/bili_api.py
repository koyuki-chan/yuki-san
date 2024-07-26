
from typing import Dict
from bilibili_api import user, sync, Credential,dynamic
from cogs.config import config

credential = Credential(sessdata=config.SESSDATA)
u = user.User(config.UID,credential=credential)



async def fetch_dyn():
    page = await u.get_dynamics(0)
    return page['cards'][0]['desc']

async def get_info_live():
    data = await u.get_live_info()
    return data

async def get_dync_info(d_id: int) -> Dict:
    d  = dynamic.Dynamic(dynamic_id=d_id,credential=credential)
    data = await d.get_info()
    return data

def isOpus(d_id: int):
    d = dynamic.Dynamic(dynamic_id=d_id,credential=credential)
    return d.is_opus()