# ⚽ Analizador de Estadísticas de Fútbol

Proyecto de backend en Python que consume una API de fútbol y analiza estadísticas básicas de partidos.

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación y configuración

### 1. Clonar o descargar el proyecto
```bash
cd "analista de stats"
```

### 2. Crear un entorno virtual (recomendado)
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar API Key

**Obtener API Key gratis:**
1. Ve a https://www.football-data.org/
2. Regístrate (es gratis)
3. Copia tu API key

**Configurar en el proyecto:**
1. Copia el archivo `.env.example` a `.env`
2. Reemplaza `your_api_key_here` con tu API key real

```bash
# En el archivo .env
FOOTBALL_API_KEY=tu_api_key_aqui
```

## 📖 Uso

### Ejecutar el análisis
```bash
python main.py
```

### Ejemplo de salida
```
======================================================================
⚽ ANALIZADOR DE ESTADÍSTICAS DE FÚTBOL
======================================================================

🔍 Validando API key...
✅ API key validada correctamente

======================================================================
📊 ÚLTIMOS PARTIDOS DE MANCHESTER UNITED
======================================================================

1. 
    📅 2026-01-15 | Premier League
    Manchester United              vs Liverpool
    Resultado: 2-1 ✓ Local gana
    
======================================================================
📈 ESTADÍSTICAS DE MANCHESTER UNITED
======================================================================

    Total de partidos:          10
    Victorias:                  7
    Empates:                    2
    Derrotas:                   1
    
    Promedio de goles:          2.50
    Promedio goles a favor:     1.70
    Promedio goles en contra:   0.80
```

## 📁 Estructura del proyecto

```
analista de stats/
├── main.py              # Script principal
├── api_client.py        # Cliente para consumir la API
├── stats_analyzer.py    # Lógica de análisis estadístico
├── requirements.txt     # Dependencias del proyecto
├── .env.example         # Template de configuración
├── .env                 # Configuración (git ignored)
└── README.md           # Este archivo
```

## 🔧 Módulos

### `api_client.py`
- `get_team_matches()`: Obtiene los últimos partidos de un equipo
- `get_team_info()`: Obtiene información del equipo
- `validate_api_key()`: Valida la API key configurada

### `stats_analyzer.py`
- `extract_match_data()`: Extrae datos relevantes de un partido
- `format_match_display()`: Formatea partidos para mostrar en consola
- `display_team_matches()`: Muestra los partidos de un equipo
- `calculate_basic_stats()`: Calcula estadísticas básicas
- `display_team_stats()`: Muestra las estadísticas formateadas

## 📊 Equipos disponibles

El proyecto incluye estos equipos de ejemplo:
- Manchester United (ID: 66)
- Manchester City (ID: 65)
- Liverpool (ID: 64)
- Arsenal (ID: 57)
- Chelsea (ID: 61)
- Real Madrid (ID: 86)
- Barcelona (ID: 81)
- Atletico Madrid (ID: 78)
- Bayern Munich (ID: 27)
- Borussia Dortmund (ID: 4)

Puedes cambiar los equipos editando `main.py`.

## 🔮 Próximas fases

- [x] Consumir API de fútbol
- [x] Obtener lista de partidos
- [x] Mostrar datos en consola
- [x] Filtrar información relevante
- [x] Calcular estadísticas básicas
- [ ] **Fase 2**: Estadísticas avanzadas (rachas, rendimiento local/visitante)
- [ ] **Fase 3**: Integración con FastAPI
- [ ] **Fase 4**: Análisis textual con IA

## 🚨 Manejo de errores

El proyecto maneja automáticamente:
- ❌ Errores de conexión
- ❌ Timeouts
- ❌ Errores de autenticación (API key inválida)
- ❌ Errores HTTP (404, 403, etc.)

## 📝 Notas

- La API gratuita tiene límite de 10 llamadas por minuto
- Los datos son de football-data.org
- Solo muestra partidos finalizados

## 📧 Soporte

Para problemas con la API, consulta: https://www.football-data.org/

## 🧠 Análisis automático

El sistema genera recomendaciones basadas en estadísticas recientes de los equipos:

- Tendencia de goles (Over/Under 2.5)
- Probabilidad de ambos anotan (BTTS)
- Comparación de forma entre equipos

Estas recomendaciones se calculan utilizando los últimos 5 partidos de liga de cada equipo y reglas estadísticas simples.
## 📄 Licencia

Proyecto educativo para análisis de datos de fútbol.
