import httpx
import json

class DeadlockApi():
    def __init__(self):
        self.url = 'https://api.deadlock-api.com'
        self.client = httpx.AsyncClient(timeout=30)

    async def get_player_last_match(self, account_id):
        try:
            resp = await self.client.get(f'{self.url}/v1/players/{account_id}/match-history')
            resp.raise_for_status()
            raw = await resp.aread()
            data = json.loads(raw)
            
            if not data:
                return None
            
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

        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_hero_by_id(self, hero_id):
        try:
            resp = await self.client.get(f"{self.url}/v1/assets/heroes/{hero_id}")
            resp.raise_for_status()

            raw = await resp.aread()
            data = json.loads(raw)

            if not data:
                return None
            
            return data

        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_id_by_steam_id(self, steam_id):
        try:
            id = steam_id - 76561197960265728
            return id
        
        except Exception as e:
            print("Error:", e)
            return None

    async def close(self):
        await self.client.aclose()