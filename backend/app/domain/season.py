from dataclasses import dataclass

@dataclass(frozen=True)
class Season:
    label: str
    provider_year: int

def parse_season(label: str) -> Season:
    parts = label.split("-")
    if len(parts) != 2 or len(parts[0]) != 4 or len(parts[1]) != 2:
        raise ValueError("Expected season format YYYY-YY, e.g. 2026-27")
    start, end = int(parts[0]), int(parts[1])
    if (start + 1) % 100 != end:
        raise ValueError("Season end year must follow start year")
    return Season(label=label, provider_year=start)
