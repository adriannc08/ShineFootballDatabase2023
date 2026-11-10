type Standing = {
  team: string;
  played: number;
  wins: number;
  draws: number;
  losses: number;
  goals_for: number;
  goals_against: number;
  goal_difference: number;
  points: number;
};

type Fixture = {
  date: string;
  status: string;
  home_team: string;
  away_team: string;
  home_goals: number | null;
  away_goals: number | null;
};

type Statistics = {
  team: string;
  goals_for: number;
  goals_against: number;
  win_percentage: number;
  points_per_match: number;
};

type Team = {
  id: number;
  provider_id: number;
  name: string;
  country: string | null;
  founded: number | null;
  logo: string | null;
};

const API_URL = process.env.FDI_API_URL ?? "http://127.0.0.1:8000";

async function getData<T>(path: string): Promise<T | null> {
  try {
    const response = await fetch(`${API_URL}${path}`, {
      cache: "no-store",
    });

    if (!response.ok) return null;
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

function formatDate(date: string) {
  return new Intl.DateTimeFormat("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(date));
}


export default async function Home() {
  const [
    standingsData,
    fixturesData,
    statisticsData,
    teamsData,
  ] = await Promise.all([
    getData<{ standings: Standing[] }>(
      "/api/v1/leagues/140/seasons/2023/standings"
    ),
    getData<{ fixtures: Fixture[]; total_fixtures: number }>(
      "/api/v1/leagues/140/seasons/2023/fixtures"
    ),
    getData<{ statistics: Statistics[] }>(
      "/api/v1/leagues/140/seasons/2023/statistics"
    ),
    getData<Team[] | { teams: Team[] }>("/api/v1/teams"),
  ]);

  const standings = standingsData?.standings ?? [];
  const fixtures = fixturesData?.fixtures ?? [];
  const statistics = statisticsData?.statistics ?? [];

  const teams = Array.isArray(teamsData)
    ? teamsData
    : teamsData?.teams ?? [];

  const completedFixtures = fixtures.filter(
    (fixture) =>
      ["FT", "AET", "PEN"].includes(fixture.status) &&
      fixture.home_goals !== null &&
      fixture.away_goals !== null
  );

  const totalGoals = completedFixtures.reduce(
    (total, fixture) =>
      total + fixture.home_goals! + fixture.away_goals!,
    0
  );

  const averageGoals =
    completedFixtures.length > 0
      ? (totalGoals / completedFixtures.length).toFixed(2)
      : "0.00";

  const recentFixtures = [...completedFixtures]
    .sort(
      (a, b) =>
        new Date(b.date).getTime() - new Date(a.date).getTime()
    )
    .slice(0, 5);

  const topScoringTeams = [...statistics]
    .sort((a, b) => b.goals_for - a.goals_for)
    .slice(0, 5);

  return (
    <main className="dashboard">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">FDI</div>
          <div>
            <strong>FOOTBALL</strong>
            <span>DATA INTELLIGENCE</span>
          </div>
        </div>

        <p className="nav-label">PLATAFORMA</p>
        <nav className="navigation">
          
          <a className="nav-link active" href="#overview">▦ <span>Dashboard</span></a>
          <a className="nav-link" href="#standings">▤ <span>Clasificación</span></a>
          <a className="nav-link" href="#matches">◷ <span>Partidos</span></a>
          <a className="nav-link" href="#statistics">▥ <span>Estadísticas</span></a>
          <a className="nav-link" href="/compare">⚖ <span>Comparador</span></a>
        </nav>

        <div className="sidebar-bottom">
          <span className="status-dot" />
          <span>Football Data Intelligence</span>
          <small>Versión 0.1.0</small>
        </div>
      </aside>

      <section className="main-content" id="overview">
        <header className="topbar">
          <div>
            <p className="eyebrow">CENTRO DE ANÁLISIS</p>
            <h1>Dashboard</h1>
          </div>
          <div className="season-badge">
            <span className="status-dot" />
            LaLiga · 2023/24
          </div>
        </header>

        <section className="welcome">
          <div>
            <p className="eyebrow">FOOTBALL DATA INTELLIGENCE</p>
            <h2>El fútbol, analizado con datos.</h2>
            <p>
              Una visión global del rendimiento de los equipos
              en la Primera División española.
            </p>
          </div>
          <div className="welcome-mark">⚽</div>
        </section>

        <section className="metrics">
          <article className="metric-card">
            <span>Equipos</span>
            <strong>{standings.length || "—"}</strong>
            <small>Clubes en competición</small>
          </article>
          <article className="metric-card">
            <span>Partidos almacenados</span>
            <strong>{fixturesData?.total_fixtures ?? "—"}</strong>
            <small>Encuentros importados</small>
          </article>
          <article className="metric-card">
            <span>Partidos disputados</span>
            <strong>{completedFixtures.length || "—"}</strong>
            <small>Con resultado definitivo</small>
          </article>
          <article className="metric-card">
            <span>Goles por partido</span>
            <strong>{averageGoals}</strong>
            <small>Media de goles</small>
          </article>
        </section>

        {!standingsData && !fixturesData && (
          <div className="warning">
            No se ha podido conectar con FastAPI. Comprueba que el backend
            está funcionando en el puerto 8000 y recarga esta página.
          </div>
        )}

        <section className="content-grid">
          <article className="panel standings-panel" id="standings">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">COMPETICIÓN</p>
                <h3>Clasificación</h3>
              </div>
              <span className="panel-tag">2023/24</span>
            </div>

            <div className="table-scroll">
              <table>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Equipo</th>
                    <th>PJ</th>
                    <th>DG</th>
                    <th>PTS</th>
                  </tr>
                </thead>
                <tbody>
                  {standings.map((team, index) => (
                    <tr key={team.team}>
                      <td className="position">{index + 1}</td>
                      <td className="team-name">
                        {(() => {
                          const club = teams.find((item) => item.name === team.team);

                          return club ? (
                            <a
                              className="team-link"
                              href={`/teams/${club.provider_id}`}
                            >
                              {team.team}
                            </a>
                          ) : (
                            team.team
                          );
                        })()}
                      </td>
                      <td>{team.played}</td>
                      <td>{team.goal_difference > 0 ? "+" : ""}
                        {team.goal_difference}</td>
                      <td className="points">{team.points}</td>
                    </tr>
                  ))}
                  {standings.length === 0 && (
                    <tr><td colSpan={5}>No hay datos disponibles.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </article>

          <article className="panel" id="matches">
            <div className="panel-heading">
              <div>
                <p className="eyebrow">ACTIVIDAD</p>
                <h3>Últimos resultados</h3>
              </div>
            </div>

            <div className="match-list">
              {recentFixtures.map((fixture, index) => (
                <div className="match" key={`${fixture.date}-${index}`}>
                  <div className="match-date">{formatDate(fixture.date)}</div>
                  <div className="match-teams">
                    <span>{fixture.home_team}</span>
                    <span>{fixture.away_team}</span>
                  </div>
                  <div className="score">
                    {fixture.home_goals} - {fixture.away_goals}
                  </div>
                </div>
              ))}
              {recentFixtures.length === 0 && (
                <p className="empty-state">No hay resultados disponibles.</p>
              )}
            </div>
          </article>
        </section>

        <section className="panel top-scorers" id="statistics">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">RENDIMIENTO COLECTIVO</p>
              <h3>Equipos más goleadores</h3>
            </div>
            <span className="panel-tag">Goles a favor</span>
          </div>

          <div className="scoring-list">
            {topScoringTeams.map((team, index) => {
              const maximum = topScoringTeams[0]?.goals_for || 1;
              const width = (team.goals_for / maximum) * 100;

              return (
                <div className="scoring-row" key={team.team}>
                  <span className="scoring-position">
                    {String(index + 1).padStart(2, "0")}
                  </span>
                  <strong>{team.team}</strong>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${width}%` }} />
                  </div>
                  <b>{team.goals_for}</b>
                </div>
              );
            })}
            {topScoringTeams.length === 0 && (
              <p className="empty-state">No hay estadísticas disponibles.</p>
            )}
          </div>
        </section>

        <footer className="footer">
          FDI · Football Data Intelligence · Datos de LaLiga 2023/24
        </footer>
      </section>
    </main>
  );
}
