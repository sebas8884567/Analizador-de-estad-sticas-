from api_client import get_team_matches
import json

matches = get_team_matches(66, limit=1)
print(json.dumps(matches, indent=2))
