"""
Analizador de estadísticas de partidos
"""
from datetime import datetime
from typing import List, Dict

def extract_match_data(match: dict) -> dict:
    """
    Extrae los datos relevantes de un partido
    
    Args:
        match: Datos del partido de la API
    
    Returns:
        dict: Datos filtrados y estructurados
    """
    try:
        return {
            'fecha': match.get('utcDate', '').split('T')[0],
            'equipo_local': match.get('homeTeam', {}).get('name', 'Desconocido'),
            'equipo_visitante': match.get('awayTeam', {}).get('name', 'Desconocido'),
            'goles_local': match.get('score', {}).get('fullTime', {}).get('home'),
            'goles_visitante': match.get('score', {}).get('fullTime', {}).get('away'),
            'estado': match.get('status', 'DESCONOCIDO'),
            'competicion': match.get('competition', {}).get('name', 'Desconocida')
        }
    except Exception as e:
        print(f"❌ Error al procesar partido: {str(e)}")
        return None

def format_match_display(match_data: dict) -> str:
    """
    Formatea un partido para mostrar en consola
    
    Args:
        match_data: Datos del partido procesados
    
    Returns:
        str: Partido formateado para mostrar
    """
    if not match_data:
        return ""
    
    goles_local = match_data['goles_local']
    goles_visitante = match_data['goles_visitante']
    
    # Determinar ganador
    if goles_local > goles_visitante:
        resultado = f"{goles_local}-{goles_visitante} ✓ Local gana"
    elif goles_visitante > goles_local:
        resultado = f"{goles_local}-{goles_visitante} ✓ Visitante gana"
    else:
        resultado = f"{goles_local}-{goles_visitante} = Empate"
    
    return f"""
    📅 {match_data['fecha']} | {match_data['competicion']}
    {match_data['equipo_local']:30} vs {match_data['equipo_visitante']}
    Resultado: {resultado}
    """

def display_team_matches(team_name: str, matches: List[dict], limit: int = 5):
    """
    Muestra los partidos de un equipo en consola
    
    Args:
        team_name: Nombre del equipo
        matches: Lista de partidos
        limit: Cantidad de partidos a mostrar
    """
    print(f"\n{'='*70}")
    print(f"📊 ÚLTIMOS PARTIDOS DE {team_name.upper()}")
    print(f"{'='*70}")
    
    if not matches:
        print("❌ No hay partidos disponibles")
        return
    # Ordenar partidos por fecha (más recientes primero) y mostrar los últimos `limit`
    try:
        sorted_matches = sorted(matches, key=lambda m: m.get('utcDate', ''), reverse=True)
    except Exception:
        sorted_matches = matches

    for i, match in enumerate(sorted_matches[:limit], 1):
        match_data = extract_match_data(match)
        if match_data:
            print(f"\n{i}. {format_match_display(match_data)}")

def calculate_basic_stats(matches: List[dict], team_id: int = None) -> dict:
    """
    Calcula estadísticas básicas de los partidos
    
    Args:
        matches: Lista de partidos
        team_id: ID del equipo para determinar correctamente victorias/derrotas
    
    Returns:
        dict: Estadísticas calculadas
    """
    if not matches:
        return {
            'total_partidos': 0,
            'goles_promedio': 0,
            'victorias': 0,
            'empates': 0,
            'derrotas': 0
        }
    
    total_goles_a_favor = 0
    total_goles_en_contra = 0
    victorias = 0
    empates = 0
    derrotas = 0
    
    for match in matches:
        goles_local = match.get('score', {}).get('fullTime', {}).get('home')
        goles_visitante = match.get('score', {}).get('fullTime', {}).get('away')
        
        if goles_local is not None and goles_visitante is not None:
            # Determinar si el equipo es local o visitante
            team_is_home = match.get('homeTeam', {}).get('id') == team_id
            team_is_away = match.get('awayTeam', {}).get('id') == team_id
            
            if team_is_home or team_is_away:
                if team_is_home:
                    goles_equipo = goles_local
                    goles_rival = goles_visitante
                else:
                    goles_equipo = goles_visitante
                    goles_rival = goles_local
                
                total_goles_a_favor += goles_equipo
                total_goles_en_contra += goles_rival
                
                if goles_equipo > goles_rival:
                    victorias += 1
                elif goles_equipo < goles_rival:
                    derrotas += 1
                else:
                    empates += 1
            else:
                # Si no se puede determinar, usar el método antiguo (para compatibilidad)
                total_goles_a_favor += goles_local
                total_goles_en_contra += goles_visitante
                
                if goles_local > goles_visitante:
                    victorias += 1
                elif goles_local < goles_visitante:
                    derrotas += 1
                else:
                    empates += 1
    
    total_partidos = len(matches)
    goles_totales = total_goles_a_favor + total_goles_en_contra
    
    return {
        'total_partidos': total_partidos,
        'goles_promedio': goles_totales / total_partidos if total_partidos > 0 else 0,
        'goles_promedio_a_favor': total_goles_a_favor / total_partidos if total_partidos > 0 else 0,
        'goles_promedio_en_contra': total_goles_en_contra / total_partidos if total_partidos > 0 else 0,
        'victorias': victorias,
        'empates': empates,
        'derrotas': derrotas
    }

def display_upcoming_matches(team_name: str, matches: List[dict], limit: int = 5):
    """
    Muestra los próximos partidos de un equipo
    
    Args:
        team_name: Nombre del equipo
        matches: Lista de partidos
        limit: Cantidad de partidos a mostrar
    """
    print(f"\n{'='*70}")
    print(f"📅 PRÓXIMOS PARTIDOS DE {team_name.upper()}")
    print(f"{'='*70}")
    
    if not matches:
        print("❌ No hay próximos partidos disponibles")
        return
    
    # Ordenar partidos por fecha (más próximos primero)
    try:
        sorted_matches = sorted(matches, key=lambda m: m.get('utcDate', ''))
    except Exception:
        sorted_matches = matches

    for i, match in enumerate(sorted_matches[:limit], 1):
        fecha = match.get('utcDate', '').split('T')[0]
        equipo_local = match.get('homeTeam', {}).get('name', 'Desconocido')
        equipo_visitante = match.get('awayTeam', {}).get('name', 'Desconocido')
        competicion = match.get('competition', {}).get('name', 'Desconocida')
        
        print(f"""
    {i}. 📅 {fecha} | {competicion}
       {equipo_local:30} vs {equipo_visitante}
       ⏳ Próximamente""")
def display_team_stats(team_name: str, stats: dict):
    """
    Muestra las estadísticas de un equipo
    
    Args:
        team_name: Nombre del equipo
        stats: Estadísticas calculadas
    """
    print(f"\n{'='*70}")
    print(f"📈 ESTADÍSTICAS DE {team_name.upper()}")
    print(f"{'='*70}")
    
    print(f"""
    Total de partidos:          {stats['total_partidos']}
    Victorias:                  {stats['victorias']}
    Empates:                    {stats['empates']}
    Derrotas:                   {stats['derrotas']}
    
    Promedio de goles:          {stats['goles_promedio']:.2f}
    Promedio goles a favor:     {stats['goles_promedio_a_favor']:.2f}
    Promedio goles en contra:   {stats['goles_promedio_en_contra']:.2f}
    """)

def _compute_form_points(stats: dict) -> int:
    """Calcula puntos de forma según victorias (3), empates (1) y derrotas (0)."""
    return stats.get('victorias', 0) * 3 + stats.get('empates', 0) * 1


def analyze_future_match(stats_local: dict, stats_visitante: dict) -> dict:
    """
    Analiza un partido futuro entre dos equipos y devuelve recomendaciones.
    
    Args:
        stats_local: Estadísticas del equipo local
        stats_visitante: Estadísticas del equipo visitante
    
    Retorna:
        dict con claves 'tendencia_goles', 'ambos_anotan', 'ventaja_forma'.
    """
    result = {
        'tendencia_goles': 'Indefinido',
        'ambos_anotan': 'No',
        'ventaja_forma': 'Forma equilibrada'
    }

    # 1. Tendencia Over/Under 2.5
    prom_total = stats_local.get('promedio_goles_favor', 0) + stats_visitante.get('promedio_goles_favor', 0)
    if prom_total >= 2.6:
        result['tendencia_goles'] = 'Over 2.5 probable'
    elif prom_total < 2.3:
        result['tendencia_goles'] = 'Under 2.5 probable'

    # 2. Ambos anotan: calcular probabilidad usando modelo de Poisson simple
    # lambda se toma del promedio de goles a favor ajustado por goles en contra
    # (una versión muy básica, se puede refinar más adelante).
    # nuestros stats usan claves generadas por calculate_basic_stats
    lam_local = stats_local.get('goles_promedio_a_favor', 0)
    lam_visit = stats_visitante.get('goles_promedio_a_favor', 0)
    # probabilidad de marcar al menos un gol = 1 - exp(-lambda)
    import math
    p_local = 1 - math.exp(-lam_local)
    p_visit = 1 - math.exp(-lam_visit)
    prob_btts = p_local * p_visit
    result['probabilidad_ambos_anotan'] = round(prob_btts * 100, 1)
    # umbral para etiqueta
    if prob_btts >= 0.6:
        result['ambos_anotan'] = 'Ambos anotan probable'
    elif prob_btts <= 0.4:
        result['ambos_anotan'] = 'Poco probable'
    else:
        result['ambos_anotan'] = 'Neutral'

    # 3. Forma comparativa
    pts_local = _compute_form_points(stats_local)
    pts_visitante = _compute_form_points(stats_visitante)
    if pts_local > pts_visitante + 2:
        result['ventaja_forma'] = 'Ventaja local'
    elif pts_visitante > pts_local + 2:
        result['ventaja_forma'] = 'Ventaja visitante'
    else:
        result['ventaja_forma'] = 'Forma equilibrada'

    return result
