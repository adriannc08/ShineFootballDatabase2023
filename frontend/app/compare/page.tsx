type Team = {
  id: number;
  provider_id: number;
  name: string;
  country: string | null;
  logo: string | null;
};

type TeamStats = {
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
  goals_against_per_match: number;
  points_per_match: number;
  home_played: number;
  home_wins: number;
  away_played: number;
  away_wins: number;
  home_win_percentage: number;
  away_win_percentage: number;
};

type TeamDetail = {
  statistics: TeamStats | null;
};

type PageProps = {
  searchParams: Promise<{
    home?: string;
    away?: string;
  }>;
};

const API_URL =
  process.env.FDI_API_URL ?? "http://127.0.0.1:8000";

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

function formatNumber(value: number | null | undefined) {
  return (value ?? 0).toFixed(2);
}

function MetricRow({
  label,
  home,
  away,
  suffix = "",
  decimals = false,
}: {
  label: string;
  home: number;
  away: number;
  suffix?: string;
  decimals?: boolean;
}) {
  const homeText = decimals
    ? formatNumber(home)
    : String(home);

  const awayText = decimals
    ? formatNumber(away)
    : String(away);

  return (
    <div className="compare-metric-row">
      <span
        className={`compare-number ${
          home > away ? "winner" : ""
        }`}
      >
        {homeText}{suffix}
      </span>

      <span className="compare-metric-label">{label}</span>

      <span
        className={`compare-number ${
          away > home ? "winner" : ""
        }`}
      >
        {awayText}{suffix}
      </span>
    </div>
  );
}

export default async function ComparePage({
  searchParams,
}: PageProps) {
  const params = await searchParams;

  const teamsData = await getData<Team[] | { teams: Team[] }>(
    "/api/v1/teams"
  );

  const teams = Array.isArray(teamsData)
    ? teamsData
    : teamsData?.teams ?? [];

  const homeId =
    params.home ?? String(teams[0]?.provider_id ?? "");

  const awayId =
    params.away ?? String(teams[1]?.provider_id ?? "");

  const homeTeam = teams.find(
    (team) => String(team.provider_id) === homeId
  );

  const awayTeam = teams.find(
    (team) => String(team.provider_id) === awayId
  );

  const [homeDetail, awayDetail] =
    homeTeam && awayTeam && homeId !== awayId
      ? await Promise.all([
          getData<TeamDetail>(
            `/api/v1/teams/${homeId}?league_id=140&season=2023`
          ),
          getData<TeamDetail>(
            `/api/v1/teams/${awayId}?league_id=140&season=2023`
          ),
        ])
      : [null, null];

  const homeStats = homeDetail?.statistics;
  const awayStats = awayDetail?.statistics;

  return (
    <main className="compare-page">
      <a href="/" className="back-link">
        ← Volver al dashboard
      </a>

      <header className="compare-header">
        <p className="eyebrow">FOOTBALL DATA INTELLIGENCE</p>
        <h1>Comparador de equipos</h1>
        <p>
          Compara el rendimiento de dos clubes de LaLiga
          durante la temporada 2023.
        </p>
      </header>

      <form action="/compare" method="get" className="compare-form">
        <div className="compare-select-group">
          <label htmlFor="home">Equipo local</label>
          <select
            id="home"
            name="home"
            defaultValue={homeId}
            className="compare-select"
          >
            {teams.map((team) => (
              <option
                key={team.provider_id}
                value={team.provider_id}
              >
                {team.name}
              </option>
            ))}
          </select>
        </div>

        <span className="compare-vs">VS</span>

        <div className="compare-select-group">
          <label htmlFor="away">Equipo visitante</label>
          <select
            id="away"
            name="away"
            defaultValue={awayId}
            className="compare-select"
          >
            {teams.map((team) => (
              <option
                key={team.provider_id}
                value={team.provider_id}
              >
                {team.name}
              </option>
            ))}
          </select>
        </div>

        <button type="submit" className="compare-button">
          Comparar equipos
        </button>
      </form>

      {homeId === awayId && (
        <p className="warning">
          Selecciona dos equipos diferentes para compararlos.
        </p>
      )}

      {homeTeam && awayTeam && homeId !== awayId &&
        homeStats && awayStats && (
          <>
            <section className="compare-teams">
              <div className="compare-team">
                {homeTeam.logo && (
                  <img
                    src={homeTeam.logo}
                    alt={homeTeam.name}
                    className="compare-logo"
                  />
                )}
                <h2>{homeTeam.name}</h2>
              </div>

              <span className="compare-vs-large">VS</span>

              <div className="compare-team">
                {awayTeam.logo && (
                  <img
                    src={awayTeam.logo}
                    alt={awayTeam.name}
                    className="compare-logo"
                  />
                )}
                <h2>{awayTeam.name}</h2>
              </div>
            </section>

            <section className="compare-panel">
              <h2>Estadísticas generales</h2>

              <MetricRow
                label="Partidos jugados"
                home={homeStats.played}
                away={awayStats.played}
              />
              <MetricRow
                label="Victorias"
                home={homeStats.wins}
                away={awayStats.wins}
              />
              <MetricRow
                label="Empates"
                home={homeStats.draws}
                away={awayStats.draws}
              />
              <MetricRow
                label="Derrotas"
                home={homeStats.losses}
                away={awayStats.losses}
              />
              <MetricRow
                label="Puntos"
                home={homeStats.points}
                away={awayStats.points}
              />
              <MetricRow
                label="Porcentaje de victorias"
                home={homeStats.win_percentage}
                away={awayStats.win_percentage}
                suffix="%"
                decimals
              />
            </section>

            <section className="compare-panel">
              <h2>Rendimiento goleador</h2>

              <MetricRow
                label="Goles a favor"
                home={homeStats.goals_for}
                away={awayStats.goals_for}
              />
              <MetricRow
                label="Goles en contra"
                home={homeStats.goals_against}
                away={awayStats.goals_against}
              />
              <MetricRow
                label="Diferencia de goles"
                home={homeStats.goal_difference}
                away={awayStats.goal_difference}
              />
              <MetricRow
                label="Goles a favor por partido"
                home={homeStats.goals_for_per_match}
                away={awayStats.goals_for_per_match}
                decimals
              />
              <MetricRow
                label="Goles en contra por partido"
                home={homeStats.goals_against_per_match}
                away={awayStats.goals_against_per_match}
                decimals
              />
              <MetricRow
                label="Puntos por partido"
                home={homeStats.points_per_match}
                away={awayStats.points_per_match}
                decimals
              />
            </section>

            <section className="compare-panel">
              <h2>Rendimiento como local y visitante</h2>

              <MetricRow
                label="Partidos en casa"
                home={homeStats.home_played}
                away={awayStats.home_played}
              />
              <MetricRow
                label="Victorias en casa"
                home={homeStats.home_wins}
                away={awayStats.home_wins}
              />
              <MetricRow
                label="Porcentaje de victorias en casa"
                home={homeStats.home_win_percentage}
                away={awayStats.home_win_percentage}
                suffix="%"
                decimals
              />
              <MetricRow
                label="Partidos fuera"
                home={homeStats.away_played}
                away={awayStats.away_played}
              />
              <MetricRow
                label="Victorias fuera"
                home={homeStats.away_wins}
                away={awayStats.away_wins}
              />
              <MetricRow
                label="Porcentaje de victorias fuera"
                home={homeStats.away_win_percentage}
                away={awayStats.away_win_percentage}
                suffix="%"
                decimals
              />
            </section>
          </>
        )}

      {homeTeam && awayTeam && homeId !== awayId &&
        (!homeStats || !awayStats) && (
          <p className="warning">
            No se han podido cargar las estadísticas de ambos equipos.
          </p>
        )}

      {!homeTeam || !awayTeam ? (
        <p className="warning">
          No se han encontrado los equipos seleccionados.
        </p>
      ) : null}
    </main>
  );
}
