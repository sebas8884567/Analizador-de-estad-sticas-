"""
Script principal del analizador de estadísticas de fútbol
"""
from api_client import get_team_matches, get_teams_by_competition, validate_api_key
from stats_analyzer import display_team_matches, calculate_basic_stats, display_team_stats, display_upcoming_matches, analyze_future_match

# Ligas principales con sus códigos en football-data.org
MAIN_COMPETITIONS = {
    'Premier League': 'PL',
    'La Liga': 'PD',
    'Serie A': 'SA',
    'Bundesliga': 'BL1',
    'Ligue 1': 'FL1'
}

def select_competition() -> tuple:
    """
    Permite al usuario seleccionar una liga
    
    Returns:
        tuple: (nombre_liga, codigo_liga) o (None, None) si cancela
    """
    competitions_list = list(MAIN_COMPETITIONS.items())
    
    print("\nLigas disponibles:")
    for i, (name, code) in enumerate(competitions_list, 1):
        print(f"  {i}. {name}")
    
    while True:
        try:
            choice = input("\nSelecciona una liga (número) o 'q' para salir: ").strip()
            
            if choice.lower() == 'q':
                return None, None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(competitions_list):
                comp_name, comp_code = competitions_list[choice_num - 1]
                return comp_name, comp_code
            else:
                print(f"❌ Por favor selecciona un número entre 1 y {len(competitions_list)}")
        except ValueError:
            print("❌ Entrada inválida. Ingresa un número o 'q' para salir")

def select_team(competition_code: str) -> tuple:
    """
    Permite al usuario seleccionar un equipo de una liga específica
    
    Args:
        competition_code: Código de la competición
    
    Returns:
        tuple: (nombre_equipo, id_equipo) o (None, None) si cancela
    """
    print(f"\n📡 Obteniendo equipos...")
    teams_data = get_teams_by_competition(competition_code)
    
    if not teams_data:
        print("❌ No se pudieron obtener los equipos")
        return None, None
    
    # Filtrar solo equipos con información válida
    teams_list = [(t.get('name', 'Desconocido'), t.get('id')) for t in teams_data if t.get('id')]
    
    if not teams_list:
        print("❌ No hay equipos disponibles")
        return None, None
    
    print(f"\nEquipos disponibles ({len(teams_list)}):")
    for i, (name, _) in enumerate(teams_list, 1):
        print(f"  {i:2d}. {name}")
    
    while True:
        try:
            choice = input(f"\nSelecciona un equipo (número 1-{len(teams_list)}) o 'q' para salir: ").strip()
            
            if choice.lower() == 'q':
                return None, None
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(teams_list):
                team_name, team_id = teams_list[choice_num - 1]
                return team_name, team_id
            else:
                print(f"❌ Por favor selecciona un número entre 1 y {len(teams_list)}")
        except ValueError:
            print("❌ Entrada inválida. Ingresa un número o 'q' para salir")



def analizar_partido_seleccionado(team_id: int, rival_id: int, league_code: str) -> dict:
    """
    Obtiene estadísticas de ambos equipos dentro de la misma liga y calcula recomendaciones.

    Args:
        team_id: ID del equipo base
        rival_id: ID del equipo rival
        league_code: código de la liga para filtrar partidos

    Returns:
        dict: {
            'stats_team': {...},
            'stats_rival': {...},
            'recomendaciones': {...}
        }
    """
    # descargar partidos finalizados para ambos equipos
    def _recent_in_league(tid):
        resp = get_team_matches(tid, limit=100, status='FINISHED')
        matches = []
        if resp and 'matches' in resp:
            # filtrar por liga
            for m in resp['matches']:
                comp = m.get('competition', {}).get('code')
                if comp == league_code:
                    matches.append(m)
        # ordenar y tomar últimos 5
        matches = sorted(matches, key=lambda m: m.get('utcDate',''), reverse=True)
        return matches[:5]

    team_matches = _recent_in_league(team_id)
    rival_matches = _recent_in_league(rival_id)
    stats_team = calculate_basic_stats(team_matches, team_id=team_id)
    stats_rival = calculate_basic_stats(rival_matches, team_id=rival_id)
    recomendaciones = analyze_future_match(stats_team, stats_rival)
    return {
        'stats_team': stats_team,
        'stats_rival': stats_rival,
        'recomendaciones': recomendaciones
    }


def main():
    """Función principal"""
    
    print("\n" + "="*70)
    print("⚽ ANALIZADOR DE ESTADÍSTICAS DE FÚTBOL")
    print("="*70)
    
    # Validar API key
    print("\n🔍 Validando API key...")
    if not validate_api_key():
        print("❌ No se pudo validar la API key")
        print("📋 Por favor:")
        print("   1. Obtén tu API key en: https://www.football-data.org/")
        print("   2. Copia .env.example a .env")
        print("   3. Agrega tu API key al archivo .env")
        return
    
    print("✅ API key validada correctamente\n")
    
    try:
        # Seleccionar liga
        print("="*70)
        print("SELECCIONA UNA LIGA")
        print("="*70)
        competition_name, competition_code = select_competition()
        
        if competition_name is None:
            print("\n⚠️  Análisis cancelado")
            return
        
        # Seleccionar equipo
        print("\n" + "="*70)
        print(f"SELECCIONA UN EQUIPO DE {competition_name.upper()}")
        print("="*70)
        team_name, team_id = select_team(competition_code)
        
        if team_name is None:
            print("\n⚠️  Análisis cancelado")
            return
        
        print(f"\n{'='*70}")
        print(f"📊 ANALIZANDO {team_name.upper()} - {competition_name}")
        print(f"{'='*70}")
        
        # Obtener y mostrar partidos del equipo
        print(f"\n📡 Descargando partidos de {team_name}...")
        matches = get_team_matches(team_id, limit=20)
        
        if matches and 'matches' in matches:
            # Usar los últimos 5 partidos para mostrar y calcular estadísticas
            RECENT_N = 5
            recent_matches = sorted(matches['matches'], key=lambda m: m.get('utcDate', ''), reverse=True)[:RECENT_N]
            display_team_matches(team_name, recent_matches, limit=RECENT_N)
            
            # Calcular y mostrar estadísticas usando solo los últimos N y pasando el ID del equipo
            stats = calculate_basic_stats(recent_matches, team_id=team_id)
            display_team_stats(team_name, stats)
        else:
            print(f"❌ No se pudieron obtener partidos de {team_name}")
        
        # Obtener próximos partidos del equipo y filtrar por liga
        print(f"\n📡 Descargando próximos partidos de {team_name}...")
        upcoming_matches = get_team_matches(team_id, limit=100, status='SCHEDULED')
        filtered = []
        if upcoming_matches and 'matches' in upcoming_matches:
            for m in upcoming_matches['matches']:
                if m.get('competition', {}).get('code') == competition_code:
                    filtered.append(m)
        
        if filtered:
            # mostrar lista numerada al usuario
            print(f"\nPróximos encuentros en {competition_name}:")
            for idx, m in enumerate(filtered, 1):
                ht = m.get('homeTeam', {}).get('name', 'Desconocido')
                at = m.get('awayTeam', {}).get('name', 'Desconocido')
                date = m.get('utcDate', '')[:10]
                print(f"  {idx}. {date} - {ht} vs {at}")
            
            # permitir selección
            sel = None
            while sel is None:
                choice = input(f"Selecciona un partido (1-{len(filtered)}) o 'q' para saltar: ").strip()
                if choice.lower() == 'q':
                    break
                try:
                    num = int(choice)
                    if 1 <= num <= len(filtered):
                        sel = filtered[num-1]
                    else:
                        print("Número fuera de rango")
                except ValueError:
                    print("Entrada inválida")
            
            if sel:
                # determinar rival
                ht = sel.get('homeTeam', {})
                at = sel.get('awayTeam', {})
                home_id = ht.get('id')
                away_id = at.get('id')
                if home_id == team_id:
                    rival_id = away_id
                    rival_name = at.get('name', 'Desconocido')
                else:
                    rival_id = home_id
                    rival_name = ht.get('name', 'Desconocido')
                
                resultado = analizar_partido_seleccionado(team_id, rival_id, competition_code)
                print(f"\n📊 ESTADÍSTICAS PARA {team_name} vs {rival_name}")
                def _print_stats(label, stats):
                    print(f"\n  {label}:")
                    print(f"    Total partidos: {stats.get('total_partidos',0)}")
                    print(f"    Victorias: {stats.get('victorias',0)}")
                    print(f"    Empates: {stats.get('empates',0)}")
                    print(f"    Derrotas: {stats.get('derrotas',0)}")
                    print(f"    Goles prom. a favor: {stats.get('goles_promedio_a_favor',0):.2f}")
                    print(f"    Goles prom. en contra: {stats.get('goles_promedio_en_contra',0):.2f}")
                    print(f"    Goles prom. total: {stats.get('goles_promedio',0):.2f}")

                _print_stats(f"Local ({team_name})", resultado['stats_team'])
                _print_stats(f"Visitante ({rival_name})", resultado['stats_rival'])
                print(f"\n🔍 RECOMENDACIONES:")
                rec = resultado['recomendaciones']
                print(f" - Tendencia goles: {rec['tendencia_goles']}")
                print(f" - Ambos anotan: {rec['ambos_anotan']} ({rec.get('probabilidad_ambos_anotan',0)}%)")
                print(f" - Ventaja forma: {rec['ventaja_forma']}")
        else:
            print(f"❌ No hay próximos partidos en {competition_name} para {team_name}")
        
        print("\n" + "="*70)
        print("✅ Análisis completado")
        print("="*70 + "\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Análisis cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error durante el análisis: {str(e)}")

if __name__ == '__main__':
    main()
