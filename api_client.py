"""
Cliente para consumir la API de football-data.org
"""
import requests
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

API_KEY = os.getenv('FOOTBALL_API_KEY')
BASE_URL = 'https://api.football-data.org/v4'

def get_headers():
    """Retorna los headers necesarios para la API"""
    return {
        'X-Auth-Token': API_KEY
    }

def get_team_matches(team_id: int, limit: int = 10, status: str = 'FINISHED') -> dict:
    """
    Obtiene los partidos de un equipo (pasados o futuros)
    
    Args:
        team_id: ID del equipo en football-data.org
        limit: Cantidad de partidos a recuperar (máximo 100)
        status: Estado del partido ('FINISHED', 'SCHEDULED', 'LIVE')
    
    Returns:
        dict: Respuesta de la API con información de partidos
    """
    try:
        url = f'{BASE_URL}/teams/{team_id}/matches'
        params = {
            'limit': min(limit, 100),  # Limitar a 100 máximo
            'status': status
        }
        
        response = requests.get(
            url,
            headers=get_headers(),
            params=params,
            timeout=10
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.Timeout:
        print(f"❌ Error: Timeout al conectar con la API")
        return None
    except requests.exceptions.ConnectionError:
        print(f"❌ Error: No se pudo conectar con la API")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"❌ Error HTTP: {e.response.status_code}")
        if e.response.status_code == 404:
            print(f"   Equipo no encontrado (ID: {team_id})")
        elif e.response.status_code == 403:
            print(f"   Error de autenticación. Verifica tu API_KEY")
        return None
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return None

def get_team_info(team_id: int) -> dict:
    """
    Obtiene información básica de un equipo
    
    Args:
        team_id: ID del equipo en football-data.org
    
    Returns:
        dict: Información del equipo
    """
    try:
        url = f'{BASE_URL}/teams/{team_id}'
        response = requests.get(
            url,
            headers=get_headers(),
            timeout=10
        )
        
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        print(f"❌ Error al obtener información del equipo: {str(e)}")
        return None

def get_teams_by_competition(competition_code: str) -> list:
    """
    Obtiene los equipos de una competición específica
    
    Args:
        competition_code: Código de la competición (PL, PD, SA, BL1, FL1, etc)
    
    Returns:
        list: Lista de equipos con su id y nombre
    """
    try:
        url = f'{BASE_URL}/competitions/{competition_code}/teams'
        response = requests.get(
            url,
            headers=get_headers(),
            timeout=10
        )
        
        response.raise_for_status()
        data = response.json()
        
        if 'teams' in data:
            return data['teams']
        return []
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"❌ Competición no encontrada: {competition_code}")
        else:
            print(f"❌ Error HTTP: {e.response.status_code}")
        return []
    except Exception as e:
        print(f"❌ Error al obtener equipos: {str(e)}")
        return []

def validate_api_key() -> bool:
    """Valida que la API key sea correcta"""
    if not API_KEY:
        print("❌ Error: FOOTBALL_API_KEY no está configurada")
        print("   Crea un archivo .env con tu API key")
        return False
    
    try:
        response = requests.get(
            f'{BASE_URL}/competitions/',
            headers=get_headers(),
            timeout=5
        )
        return response.status_code == 200
    except Exception:
        return False
