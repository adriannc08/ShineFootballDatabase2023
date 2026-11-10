# Validation rules

Blocking:
- Published entities have provider-scoped external IDs and provenance.
- No duplicate provider IDs for the same entity type.
- Match teams differ; scores are non-negative.
- Player stats link to existing player, team and match.
- Squad membership links to existing player, team and season.
- Historical squad records are not deleted by current-season refresh.

Warnings:
- Missing biography fields; incomplete historical player stats; conflicting providers;
  partially documented endpoint coverage.

Head-to-head is calculated from `matches`, not stored as a separately maintained
source of truth. Return sample size, competition and date window.
