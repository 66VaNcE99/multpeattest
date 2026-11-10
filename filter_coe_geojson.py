
import json
from pathlib import Path

SOURCE = Path("natural-earth-countries.geojson")
OUTPUT = Path("static/countries-council-of-europe.geojson")

COE_COUNTRY_CODES = {
    "AL", "AD", "AM", "AT", "AZ", "BE", "BA", "BG",
    "HR", "CY", "CZ", "DK", "EE", "FI", "FR", "GE",
    "DE", "GR", "HU", "IS", "IE", "IT", "LV", "LI",
    "LT", "LU", "MT", "MD", "MC", "ME", "NL", "MK",
    "NO", "PL", "PT", "RO", "SM", "RS", "SK", "SI",
    "ES", "SE", "CH", "TR", "UA", "GB"
}

with SOURCE.open(encoding="utf-8") as file:
    source_data = json.load(file)

features = []
found_codes = set()

for feature in source_data["features"]:
    properties = feature["properties"]

    iso2 = properties.get("ISO3166-1-Alpha-2")

    if iso2 not in COE_COUNTRY_CODES:
        continue

    # Preserve compatibility with the existing factsheet.
    country_code = "EL" if iso2 == "GR" else iso2

    properties["CNTR_ID"] = country_code
    properties["NAME_ENGL"] = properties.get("name", country_code)

    features.append(feature)
    found_codes.add(iso2)

missing_codes = COE_COUNTRY_CODES - found_codes

result = {
    "type": "FeatureCollection",
    "features": features
}

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT.open("w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False)

print(f"Council of Europe countries found: {len(features)}/46")
print(f"Output: {OUTPUT}")

if missing_codes:
    print("Missing ISO codes:", sorted(missing_codes))
else:
    print("All 46 member states successfully included.")
