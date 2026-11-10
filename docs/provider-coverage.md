# API-Football: gate de cobertura

La API documenta un endpoint de ligas que devuelve temporadas y un objeto
`coverage` por competición/temporada. La cobertura puede variar por temporada;
un indicador `true` tampoco garantiza disponibilidad del 100% de los registros.

Antes de importar:
1. Configura `APISPORTS_KEY`.
2. Ejecuta `python scripts/check_api_football_coverage.py`.
3. Identifica las competiciones españolas correspondientes a Primera y Segunda.
4. Guarda los IDs confirmados en configuración local (no asumir IDs).
5. Comprueba por separado `players`, `fixtures.events`, `fixtures.lineups`,
   `fixtures.statistics_fixtures` y `fixtures.statistics_players`.
6. Comprueba temporadas históricas disponibles y límites de plan.
7. No marques cobertura completa si falta cualquiera de los datos requeridos.

Endpoints a evaluar según documentación:
- `leagues`: competiciones, temporadas y cobertura.
- `teams` / `teams/squads` o `players/squads`: equipos y plantillas.
- `fixtures`: calendario y resultados.
- `fixtures/lineups`: alineaciones.
- `fixtures/events`: eventos del partido.
- `players`: estadísticas individuales por competición y temporada.
- `players/seasons` y `players/teams`: temporadas y trayectoria disponibles.

La disponibilidad real debe medirse con la cuenta y plan del proyecto.
