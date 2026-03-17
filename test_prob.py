from stats_analyzer import analyze_future_match
loc={'goles_promedio_a_favor':1.4,'goles_promedio_en_contra':0.8,'victorias':2,'empates':2,'derrotas':1,'goles_promedio':2.2,'total_partidos':5}
vis={'goles_promedio_a_favor':2.2,'goles_promedio_en_contra':1.6,'victorias':2,'empates':1,'derrotas':2,'goles_promedio':3.8,'total_partidos':5}
print(analyze_future_match(loc,vis))
