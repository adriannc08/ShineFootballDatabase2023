
type TeamDetail = {
  team: {
    id: number;
    name: string;
    country: string | null;
    founded: number | null;
    logo: string | null;
  };
  league_id: number;
  season: number;
  statistics: {
    played: number;
    wins: number;
    draws: number;
    losses: number;
    goals_for: number;
    goals_against: number;
    goal_difference: number;
    points: number;
    win_percentage: number;
    goals_for_per_match: number;
    points_per_match: number;
    home_win_percentage: number;
    away_win_percentage: number;
  } | null;
  recent_fixtures: {
    date: string;
    status: string;
    home_team: string;
    away_team: string;
    home_goals: number | null;
    away_goals: number | null;
  }[];
};

const API_URL = process.env.FDI_API_URL ?? "http://127.0.0.1:8000";

async function getTeam(id: string): Promise<TeamDetail | null> {
  try {
    const response = await fetch(
      `${API_URL}/api/v1/teams/${id}?league_id=140&season=2023`,
      { cache: "no-store" }
    );

    if (!response.ok) return null;

    return await response.json();
  } catch {
    return null;
  }
}

function percentage(value: number | undefined) {
  return `${(value ?? 0).toFixed(1)}%`;
}

function formatDate(date: string) {
  return new Intl.DateTimeFormat("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(date));
}

export default async function TeamPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const data = await getTeam(id);

  if (!data) {
    return (
      <main className="team-page">
        <a href="/">← Volver al dashboard</a>
        <h1>Equipo no encontrado</h1>
        <p>No se han podido recuperar los datos de este equipo.</p>
      </main>
    );
  }

  const stats = data.statistics;

  return (
    <main className="team-page">
      <a className="back-link" href="/">← Volver al dashboard</a>

      <section className="team-hero">
        {data.team.logo && (
          <img
            className="team-logo"
            src={data.team.logo}
            alt={`Escudo de ${data.team.name}`}
          />
        )}

        <div>
          <p className="eyebrow">PERFIL DEL CLUB · LALIGA 2023/24</p>
          <h1>{data.team.name}</h1>
          <p className="team-subtitle">
            {data.team.country ?? "País no disponible"}
            {data.team.founded ? ` · Fundado en ${data.team.founded}` : ""}
          </p>
        </div>
      </section>

      {!stats && (
        <div className="warning">
          No hay estadísticas disponibles para este equipo y temporada.
        </div>
      )}

      {stats && (
        <>
          <section className="team-metrics">
            <article className="metric-card">
              <span>Partidos jugados</span>
              <strong>{stats.played}</strong>
            </article>
            <article className="metric-card">
              <span>Victorias</span>
              <strong>{stats.wins}</strong>
            </article>
            <article className="metric-card">
              <span>Empates</span>
              <strong>{stats.draws}</strong>
            </article>
            <article className="metric-card">
              <span>Derrotas</span>
              <strong>{stats.losses}</strong>
            </article>
          </section>

          <section className="team-metrics">
            <article className="metric-card">
              <span>Puntos</span>
              <strong>{stats.points}</strong>
            </article>
            <article className="metric-card">
              <span>Goles a favor</span>
              <strong>{stats.goals_for}</strong>
            </article>
            <article className="metric-card">
              <span>Goles en contra</span>
              <strong>{stats.goals_against}</strong>
            </article>
            <article className="metric-card">
              <span>Diferencia de goles</span>
              <strong>
                {stats.goal_difference > 0 ? "+" : ""}
                {stats.goal_difference}
              </strong>
            </article>
          </section>

          <section className="team-analysis">
            <article className="panel">
              <p className="eyebrow">EFICACIA</p>
              <h3>Rendimiento general</h3>

              <div className="analysis-item">
                <span>Porcentaje de victorias</span>
                <strong>{percentage(stats.win_percentage)}</strong>
              </div>

              <div className="analysis-item">
                <span>Goles por partido</span>
                <strong>{stats.goals_for_per_match.toFixed(2)}</strong>
              </div>

              <div className="analysis-item">
                <span>Puntos por partido</span>
                <strong>{stats.points_per_match.toFixed(2)}</strong>
              </div>
            </article>

            <article className="panel">
              <p className="eyebrow">LOCAL Y VISITANTE</p>
              <h3>Rendimiento por condición</h3>

              <div className="analysis-item">
                <span>Victorias en casa</span>
                <strong>{percentage(stats.home_win_percentage)}</strong>
              </div>

              <div className="analysis-item">
                <span>Victorias fuera</span>
                <strong>{percentage(stats.away_win_percentage)}</strong>
              </div>
            </article>
          </section>
        </>
      )}

      <section className="panel team-fixtures">
        <p className="eyebrow">HISTORIAL</p>
        <h3>Últimos partidos</h3>

        {data.recent_fixtures.length > 0 ? (
          <div className="match-list">
            {data.recent_fixtures.map((fixture, index) => (
              <div className="match" key={`${fixture.date}-${index}`}>
                <span className="match-date">
                  {formatDate(fixture.date)}
                </span>
                <div className="match-teams">
                  <span>{fixture.home_team}</span>
                  <span>{fixture.away_team}</span>
                </div>
                <strong className="score">
                  {fixture.home_goals ?? "–"} - {fixture.away_goals ?? "–"}
                </strong>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No hay partidos disponibles.</p>
        )}
      </section>

      <footer className="footer">
        FDI · Football Data Intelligence · Temporada 2023/24
      </footer>
    </main>
  );
}
