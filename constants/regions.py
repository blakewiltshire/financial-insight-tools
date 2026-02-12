# regions.py
"""
This module contains a dictionary of regions, sub-regions, and countries (`regions`),
as well as a dictionary of geographical coordinates for countries (`country_coordinates`).

To manage countries in the `regions` dictionary:
- Countries currently supported with data are listed and uncommented.
- Countries without data are either commented out or not listed. Uncomment or add them as data becomes available.

To add or update a country in `country_coordinates`:
- Uncomment the country line if it exists and is commented out.
- Add the country with its latitude and longitude in the format: "Country Name": (latitude, longitude).
  Use online resources to find accurate coordinates if not already provided.

Note:
- Countries without coordinates will not appear on the map.
- It's essential to keep both `regions` and `country_coordinates` updated to ensure consistency between available data and the map display.
"""



regions = {
    "World": {
        "World": {
            "Global": "WORLD"
        }
    },
    "Americas": {
        "Latin America": {
            # "Argentina": "AMER",
            "Brazil": "AMER",
            # "Chile": "AMER",
            # "Colombia": "AMER",
            # "Costa Rica": "AMER",
            # "Peru": "AMER",
            # "Puerto Rico": "AMER",
        },
        "North America": {
            "Canada": "AMER",
            "United States": "AMER",
        },
        "South America": {
            # "Mexico": "AMER",
        }
    },
    "Asia Pacific": {
        "Central Asia": {
            # "Kazakhstan": "APAC",
            # "Kyrgyzstan": "APAC",
            # "Tajikistan": "APAC",
            # "Uzbekistan": "APAC",
        },
        "East Asia": {
            "China": "APAC",
            # "Hong Kong Sar": "APAC",
            "Japan": "APAC",
            "South Korea": "APAC",
            # "Taiwan": "APAC",
        },
        "Oceania": {
            "Australia": "APAC",
            # "New Zealand": "APAC",
        },
        "South Asia": {
            "India": "APAC",
            # "Sri Lanka": "APAC",
        },
        "Southeast Asia": {
            # "Brunei": "APAC",
            # "Cambodia": "APAC",
            # "Indonesia": "APAC",
            # "Laos": "APAC",
            # "Malaysia": "APAC",
            # "Myanmar": "APAC",
            # "Philippines": "APAC",
            # "Thailand": "APAC",
            # "Vietnam": "APAC",
        },
        "Western Asia": {
            # "Armenia": "APAC",
        }
    },
    "Asia Pacific / Europe": {
        "Eastern Europe / Northern Asia": {
            # "Russia": "APAC / EMEA",
        },
        "Eastern Europe / Western Asia": {
            # "Azerbaijan": "APAC / EMEA",
        }
    },
    "Europe, The Middle East And Africa": {
        "Central Europe": {
            # "Austria": "EMEA",
        },
        "Central And Eastern Europe": {
            # "Albania": "EMEA",
            # "Bosnia And Herzegovina": "EMEA",
            # "Bulgaria": "EMEA",
            # "Croatia": "EMEA",
            # "Czech Republic": "EMEA",
            # "Estonia": "EMEA",
            # "Hungary": "EMEA",
            # "Latvia": "EMEA",
            # "Lithuania": "EMEA",
            # "Montenegro": "EMEA",
            # "North Macedonia": "EMEA",
            # "Poland": "EMEA",
            # "Romania": "EMEA",
            # "Serbia": "EMEA",
            # "Slovak Rep": "EMEA",
            # "Slovenia": "EMEA",
        },
        "Eastern Europe": {
            # "Belarus": "EMEA",
            # "Moldova": "EMEA",
        },
        "Northern Europe": {
            # "Denmark": "EMEA",
            # "Finland": "EMEA",
            # "Iceland": "EMEA",
            # "Norway": "EMEA",
            # "Sweden": "EMEA",
        },
        "Southern Europe": {
            # "Cyprus": "EMEA",
            # "Greece": "EMEA",
            "Italy": "EMEA",
            # "Malta": "EMEA",
            # "Portugal": "EMEA",
            # "San Marino": "EMEA",
            # "Spain": "EMEA",
            # "Turkey": "EMEA",
        },
        "Western Europe": {
            # "Andorra": "EMEA",
            # "Belgium": "EMEA",
            "Euro Area": "EMEA",
            "France": "EMEA",
            "Germany": "EMEA",
            # "Ireland": "EMEA",
            # "Liechtenstein": "EMEA",
            # "Luxembourg": "EMEA",
            # "Monaco": "EMEA",
            # "Netherlands": "EMEA",
            # "Switzerland": "EMEA",
            "United Kingdom": "EMEA",
        },
        "Eastern Africa": {
            # "Kenya": "EMEA",
            # "Mozambique": "EMEA",
            # "Uganda": "EMEA",
            # "Zambia": "EMEA",
        },
        "Northern Africa": {
            # "Egypt": "EMEA",
        },
        "Sub-Saharan Africa": {
            # "South Africa": "EMEA",
        },
        "West African Country": {
            # "Ghana": "EMEA",
            # "Nigeria": "EMEA",
        },
        "Middle East": {
            # "Israel": "EMEA",
            # "Lebanon": "EMEA",
            # "Saudi Arabia": "EMEA",
            # "Uae": "EMEA",
        },
        "Western Asia": {
            # "Qatar": "EMEA",
        }
    },
}

country_coordinates = {
    # Template for adding new coordinates
    # "Country Name": (latitude, longitude),

    # Currently supported countries with coordinates
    "Australia": (-25.2744, 133.7751),
    "Brazil": (-14.2350, -51.9253),
    "Canada": (56.1304, -106.3468),
    "China": (35.8617, 104.1954),
    "Euro Area": (50.8503, 4.3517),  # Brussels, Belgium (Euro Area HQ)
    "France": (46.2276, 2.2137),
    "Germany": (51.1657, 10.4515),
    "India": (20.5937, 78.9629),
    "Italy": (41.8719, 12.5674),
    "Japan": (36.2048, 138.2529),
    "United Kingdom": (55.3781, -3.4360),
    "United States": (37.0902, -95.7129),
    "South Korea": (35.9078, 127.7669),

    # Countries awaiting data or to be added in the future

    # "Albania": (, ),
    # "Andorra": (, ),
    # "Argentina": (, ),
    # "Armenia": (, ),
    # "Austria": (, ),
    # "Azerbaijan": (, ),
    # "Belarus": (, ),
    # "Belgium": (, ),
    # "Bosnia And Herzegovina": (, ),
    # "Brunei": (, ),
    # "Bulgaria": (, ),
    # "Cambodia": (, ),
    # "Central Asia": (, ),
    # "Chile": (, ),
    # "Colombia": (, ),
    # "Costa Rica": (, ),
    # "Croatia": (, ),
    # "Cyprus": (, ),
    # "Czech Republic": (, ),
    # "Denmark": (, ),
    # "Egypt": (, ),
    # "Estonia": (, ),
    # "Finland": (, ),
    # "Ghana": (, ),
    # "Greece": (, ),
    # "Hong Kong Sar": (, ),
    # "Hungary": (, ),
    # "Iceland": (, ),
    # "Indonesia": (, ),
    # "Ireland": (, ),
    # "Israel": (, ),
    # "Kazakhstan": (, ),
    # "Kenya": (, ),
    # "Kyrgyzstan": (, ),
    # "Laos": (, ),
    # "Latvia": (, ),
    # "Lebanon": (, ),
    # "Liechtenstein": (, ),
    # "Lithuania": (, ),
    # "Luxembourg": (, ),
    # "Malaysia": (, ),
    # "Malta": (, ),
    # "Mexico": (, ),
    # "Moldova": (, ),
    # "Monaco": (, ),
    # "Montenegro": (, ),
    # "Mozambique": (, ),
    # "Myanmar": (, ),
    # "Netherlands": (, ),
    # "New Zealand": (, ),
    # "Nigeria": (, ),
    # "North Macedonia": (, ),
    # "Norway": (, ),
    # "Peru": (, ),
    # "Philippines": (, ),
    # "Poland": (, ),
    # "Portugal": (, ),
    # "Puerto Rico": (, ),
    # "Qatar": (, ),
    # "Romania": (, ),
    # "San Marino": (, ),
    # "Saudi Arabia": (, ),
    # "Serbia": (, ),
    # "Slovak Rep": (, ),
    # "Slovenia": (, ),
    # "South Africa": (, ),
    # "Spain": (, ),
    # "Sri Lanka": (, ),
    # "Sweden": (, ),
    # "Switzerland": (, ),
    # "Taiwan": (, ),
    # "Tajikistan": (, ),
    # "Thailand": (, ),
    # "Turkey": (, ),
    # "Uae": (, ),
    # "Uganda": (, ),
    # "Uzbekistan": (, ),
    # "Vietnam": (, ),
    # "Zambia": (, ),
}
