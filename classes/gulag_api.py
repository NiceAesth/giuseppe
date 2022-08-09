import aiohttp
from classes import osu

class Gulag:
    def __init__(self):
        self.__base_url = 'https://api.giuseppeosu.tk'
    
    async def get_profile(self, name: str) -> osu.User:
        params = {'scope': 'all', 'name': name}
        async with aiohttp.ClientSession() as session:
            async with session.get(self.__base_url + '/get_player_info', params=params) as r:
                res = await r.json()
                if r.status != 200 or res.get('status') != 'success':
                    raise ValueError
                return osu.User.from_dict(res.get('player'))