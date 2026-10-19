import httpx
import json
from datetime import datetime, timedelta

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
        
    async def get_steam_id_by_id(self, id):
        try:
            steam_id = id + 76561197960265728
            return steam_id
        
        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_steam_profile_by_id(self, id):
        try:
            steam_id = await self.get_steam_id_by_id(id)
            resp = await self.client.get(f"{self.url}/v1/players/steam?account_ids={steam_id}")
            resp.raise_for_status()

            raw = await resp.aread()
            data = json.loads(raw)

            if not data:
                return None
            
            return {
                "name": data[0]["personaname"],
                "realname": data[0]["realname"],
                "avatar": data[0]["avatar"],
                "steam_url": data[0]["profileurl"],
                "matches_played_last_30d": data[0]["matches_played_last_30d"]
            }
        
        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_leaderboard(self, region):
        try:
            resp = await self.client.get(f"{self.url}/v1/leaderboard/{region}")
            resp.raise_for_status()

            raw = await resp.aread()
            data = json.loads(raw)

            if not data:
                return None
            
            profiles = []
            for i in range(0, 10):
                profile = data["entries"][i]            
                profiles.append(profile)

            return profiles

        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_rank_image(self, account_id):
        try:
            resp = await self.client.get(f"{self.url}/v1/players/{account_id}/rank-predict/image?size=small")
            resp.raise_for_status()

            image_data = await resp.aread()

            if not image_data:
                return None
            
            return image_data

        except Exception as e:
            print("Error:", e)
            return None
        
    async def get_all_hero_stats(self):
        try:
            resp = await self.client.get(f"{self.url}/v1/analytics/hero-stats?game_mode=normal")
            resp.raise_for_status()

            raw = await resp.aread()
            data = json.loads(raw)

            if not data:
                return None
            
            results = []
            for hero_data in data:
                results.append({
                    "hero_id": hero_data["hero_id"],
                    "wins": hero_data["wins"],
                    "losses": hero_data["losses"],
                    "matches": hero_data["matches"],
                    "kills": hero_data["total_kills"],
                    "deaths": hero_data["total_deaths"],
                    "assists": hero_data["total_assists"],
                    "damage": hero_data["total_player_damage"],
                    "networth": hero_data["total_net_worth"]
                })
            
            return results

        except Exception as e:
            print("Error:", e)
            return None

    async def get_patch_info(self):
        try:
            resp = await self.client.get(f"{self.url}/v2/patches")
            resp.raise_for_status()

            raw = await resp.aread()
            data = json.loads(raw)

            if not data:
                return None
            
            date = datetime.fromisoformat(data[0]["pub_date"]) + timedelta(hours=3)
        
            return {
                "source": data[0]["source"],
                "title": data[0]["title"],
                "date": date,
                "link": data[0]["link"]
            }
        
        except Exception as e:
            print("Error:", e)
            return None

    async def close(self):
        await self.client.aclose()