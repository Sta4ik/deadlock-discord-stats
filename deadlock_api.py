import httpx
from datetime import datetime, timedelta

ID_SHIT = 76561197960265728

class DeadlockApi():
    def __init__(self):
        self.url = 'https://api.deadlock-api.com'
        self.client = httpx.AsyncClient(timeout=30)

    async def _get_json(self, path, transform=None):
        try:
            resp = await self.client.get(f'{self.url}{path}')
            resp.raise_for_status()
            data = resp.json()
            
            if not data:
                return None
            
            return transform(data) if transform is not None else data

        except Exception as e:
            print("Error:", e)
            return None

    async def _get_bytes(self, path):
        try:
            resp = await self.client.get(f'{self.url}{path}')
            resp.raise_for_status()
            data = resp.content

            if not data:
                return None

            return data

        except Exception as e:
            print("Error:", e)
            return None

    async def get_player_last_match(self, account_id):
        def _map(data):
            match = data[0]
            return {
                "match_id": match["match_id"],
                "hero_id": match["hero_id"],
                "hero_level": match["hero_level"],
                "start_time": match["start_time"],
                "player_team": match["player_team"],
                "player_kills": match["player_kills"],
                "player_deaths": match["player_deaths"],
                "player_assists": match["player_assists"],
                "net_worth": match["net_worth"],
                "match_duration_s": match["match_duration_s"],
                "match_result": match["match_result"],
            }

        return await self._get_json(f"/v1/players/{account_id}/match-history",
            transform=_map)
        
    async def get_hero_by_id(self, hero_id):
        return await self._get_json(f"/v1/assets/heroes/{hero_id}")
        
    async def get_id_by_steam_id(self, steam_id):
        try:
            return steam_id - ID_SHIT
        
        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_steam_id_by_id(self, id):
        try:
            return id + ID_SHIT
        
        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_steam_profile_by_id(self, id):
        steam_id = await self.get_steam_id_by_id(id)

        def _map(data):
            profile = data[0]
            return {
                "name": profile["personaname"],
                "realname": profile["realname"],
                "avatar": profile["avatar"],
                "steam_url": profile["profileurl"],
                "matches_played_last_30d": profile["matches_played_last_30d"],
            }

        return await self._get_json(f"/v1/players/steam?account_ids={steam_id}",
            transform=_map)

        
    async def get_leaderboard(self, region):
        def _map(data):
            return [data["entries"][i] for i in range(0, 10)]

        return await self._get_json(f"/v1/leaderboard/{region}",
            transform=_map)
        
    async def get_rank_image(self, account_id):
        return await self._get_bytes(f"/v1/players/{account_id}/rank-predict/image?size=small")


    async def get_all_hero_stats(self):
        def _map(data):
            return [
                {
                    "hero_id": hero_data["hero_id"],
                    "wins": hero_data["wins"],
                    "losses": hero_data["losses"],
                    "matches": hero_data["matches"],
                    "kills": hero_data["total_kills"],
                    "deaths": hero_data["total_deaths"],
                    "assists": hero_data["total_assists"],
                    "damage": hero_data["total_player_damage"],
                    "networth": hero_data["total_net_worth"],
                }
                for hero_data in data
            ]

        return await self._get_json("/v1/analytics/hero-stats?game_mode=normal",
            transform=_map)

    async def get_patch_info(self):
        def _map(data):
            patch = data[0]
            date = datetime.fromisoformat(patch["pub_date"]) + timedelta(hours=3)
            return {
                "source": patch["source"],
                "title": patch["title"],
                "date": date,
                "link": patch["link"],
            }

        return await self._get_json("/v2/patches", 
            transform=_map)
        
    async def get_crosshair(self, crosshair_code):
        return await self._get_bytes(f"/v1/crosshair/code/image?code={crosshair_code}&screen_height=1080&scale=1")

    async def close(self):
        await self.client.aclose()