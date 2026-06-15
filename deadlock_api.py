import httpx

class DeadlockApi():
    def __init__(self):
        self.url = 'https://api.deadlock-api.com'
        self.client = httpx.AsyncClient(timeout=30)

    async def get_player_match_history(self, account_id):
        try:
            resp = await self.client.get(f'{self.url}/v1/players/{account_id}/match-history')
            resp.raise_for_status()
            matches = resp.json()

            if not matches:
                return None
            
            last_match = matches[0]

            return {
                'match_id': last_match['match_id'],
                'hero': last_match.get('hero_name', 'Unknown'),
                'kills': last_match.get('player_kills', 0),
                'deaths': last_match.get('player_deaths', 0),
                'result': last_match.get('match_result', 'loss')
            }
        
        except Exception:
            return None
        
    async def close(self):
        await self.client.aclose()