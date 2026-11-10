-- Minimal reference seed. Competition IDs are intentionally not guessed.
INSERT INTO seasons (label, provider_year)
VALUES ('2026-27', 2026)
ON CONFLICT (label) DO NOTHING;
