"""
Script para debuggear la API y ver todos los datos disponibles
"""
from api_client import get_team_matches
import json

# ID de Manchester United
team_id = 66

print("Descargando todos los partidos de Manchester United...\n")
matches = get_team_matches(team_id, limit=20)

if matches and 'matches' in matches:
    print(f"Total de partidos encontrados: {len(matches['matches'])}\n")
    
    for i, match in enumerate(matches['matches'], 1):
        fecha = match.get('utcDate', 'N/A').split('T')[0]
        local = match.get('homeTeam', {}).get('name', 'N/A')
        visitante = match.get('awayTeam', {}).get('name', 'N/A')
        goles_local = match.get('score', {}).get('fullTime', {}).get('home', 'N/A')
        goles_visitante = match.get('score', {}).get('fullTime', {}).get('away', 'N/A')
        estado = match.get('status', 'N/A')
        
        print(f"{i}. {fecha} | {estado}")
        print(f"   {local} {goles_local} - {goles_visitante} {visitante}\n")
else:
    print("No se pudieron obtener los datos")
