CREATE TABLE competitions (
 id BIGSERIAL PRIMARY KEY, provider TEXT NOT NULL, provider_competition_id BIGINT NOT NULL,
 name TEXT NOT NULL, country TEXT NOT NULL, tier SMALLINT,
 UNIQUE(provider, provider_competition_id)
);
CREATE TABLE seasons (
 id BIGSERIAL PRIMARY KEY, label VARCHAR(7) NOT NULL UNIQUE,
 provider_year INTEGER NOT NULL UNIQUE, starts_on DATE, ends_on DATE
);
CREATE TABLE teams (
 id BIGSERIAL PRIMARY KEY, provider TEXT NOT NULL, provider_team_id BIGINT NOT NULL,
 name TEXT NOT NULL, country TEXT, logo_url TEXT,
 UNIQUE(provider, provider_team_id)
);
CREATE TABLE players (
 id BIGSERIAL PRIMARY KEY, provider TEXT NOT NULL, provider_player_id BIGINT NOT NULL,
 full_name TEXT NOT NULL, birth_date DATE, nationality TEXT, position TEXT,
 UNIQUE(provider, provider_player_id)
);
CREATE TABLE team_squads (
 id BIGSERIAL PRIMARY KEY, team_id BIGINT NOT NULL REFERENCES teams(id),
 player_id BIGINT NOT NULL REFERENCES players(id),
 season_id BIGINT NOT NULL REFERENCES seasons(id), shirt_number INTEGER,
 position TEXT, valid_from DATE, valid_to DATE,
 UNIQUE(team_id, player_id, season_id, valid_from)
);
CREATE TABLE player_transfers (
 id BIGSERIAL PRIMARY KEY, player_id BIGINT NOT NULL REFERENCES players(id),
 from_team_id BIGINT REFERENCES teams(id), to_team_id BIGINT REFERENCES teams(id),
 transfer_date DATE, transfer_type TEXT
);
CREATE TABLE matches (
 id BIGSERIAL PRIMARY KEY, provider TEXT NOT NULL, provider_fixture_id BIGINT NOT NULL,
 competition_id BIGINT NOT NULL REFERENCES competitions(id),
 season_id BIGINT NOT NULL REFERENCES seasons(id),
 home_team_id BIGINT NOT NULL REFERENCES teams(id),
 away_team_id BIGINT NOT NULL REFERENCES teams(id),
 kickoff_at TIMESTAMPTZ, status TEXT NOT NULL, home_score INTEGER, away_score INTEGER,
 UNIQUE(provider, provider_fixture_id),
 CHECK(home_team_id <> away_team_id),
 CHECK(home_score IS NULL OR home_score >= 0),
 CHECK(away_score IS NULL OR away_score >= 0)
);
CREATE TABLE lineups (
 id BIGSERIAL PRIMARY KEY, match_id BIGINT NOT NULL REFERENCES matches(id),
 team_id BIGINT NOT NULL REFERENCES teams(id), player_id BIGINT NOT NULL REFERENCES players(id),
 is_starting BOOLEAN NOT NULL, formation_position TEXT,
 UNIQUE(match_id, team_id, player_id)
);
CREATE TABLE player_match_stats (
 id BIGSERIAL PRIMARY KEY, match_id BIGINT NOT NULL REFERENCES matches(id),
 team_id BIGINT NOT NULL REFERENCES teams(id), player_id BIGINT NOT NULL REFERENCES players(id),
 minutes_played INTEGER, goals INTEGER, assists INTEGER, yellow_cards INTEGER, red_cards INTEGER,
 raw_stats JSONB NOT NULL DEFAULT '{}'::jsonb, UNIQUE(match_id, player_id),
 CHECK(minutes_played IS NULL OR minutes_played BETWEEN 0 AND 150),
 CHECK(goals IS NULL OR goals >= 0), CHECK(assists IS NULL OR assists >= 0)
);
CREATE TABLE data_sources (
 id BIGSERIAL PRIMARY KEY, provider TEXT NOT NULL, endpoint TEXT NOT NULL,
 retrieved_at TIMESTAMPTZ NOT NULL DEFAULT now(), request_scope JSONB NOT NULL DEFAULT '{}'::jsonb,
 payload_hash TEXT, coverage_status TEXT NOT NULL DEFAULT 'unknown'
);
CREATE TABLE sync_logs (
 id BIGSERIAL PRIMARY KEY, provider TEXT NOT NULL, entity_type TEXT NOT NULL,
 started_at TIMESTAMPTZ NOT NULL DEFAULT now(), finished_at TIMESTAMPTZ,
 status TEXT NOT NULL, records_seen INTEGER NOT NULL DEFAULT 0,
 records_created INTEGER NOT NULL DEFAULT 0, records_updated INTEGER NOT NULL DEFAULT 0,
 error_summary TEXT
);
CREATE TABLE validation_errors (
 id BIGSERIAL PRIMARY KEY, entity_type TEXT NOT NULL, entity_id BIGINT,
 severity TEXT NOT NULL, rule_code TEXT NOT NULL, message TEXT NOT NULL,
 detected_at TIMESTAMPTZ NOT NULL DEFAULT now(), resolved_at TIMESTAMPTZ
);
CREATE INDEX ix_matches_home_date ON matches(home_team_id, kickoff_at DESC);
CREATE INDEX ix_matches_away_date ON matches(away_team_id, kickoff_at DESC);
CREATE INDEX ix_player_stats_player ON player_match_stats(player_id, match_id);
CREATE INDEX ix_squads_season_team ON team_squads(season_id, team_id);
