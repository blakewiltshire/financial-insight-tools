# Relationship Manager Seed Package

Generated first-pass business capability and relationship-candidate data for the US Large-Cap universe.

## Purpose

This package supports the FIT Relationship Manager workflow:

Observation / headline
→ relationship areas
→ candidate assets
→ FIT examination
→ Observation & AI Export.

The files do **not** provide investment advice, rankings, or trade signals. They only help frame why an asset may belong in an investigation.

## Files

- `us_large_business_capability_map.yaml`  
  Main generated company map. Includes ticker, company name, business tags, relationship-candidate draft tags, FIT price-data availability, and source overview.

- `us_large_business_capability_map.csv`  
  Review-friendly CSV version of the same map.

- `business_capability_tag_registry.csv` / `.yaml`  
  Controlled vocabulary for business capability tags.

- `relationship_tag_registry_v1.csv` / `.yaml`  
  Draft relationship tags that can be used by the Relationship Manager.

- `fit_price_available_us_large_caps.csv`  
  Subset of companies already available in the current FIT price-data universe.

## Layer distinction

- Classification = what the company is.
- Business tags = what the company does.
- Relationship tags = why the company might matter to an observation.
- FIT examination = how the market/asset is behaving.

## Status

Generated first pass. Review before locking. Some companies may be outdated due to the source file and index universe timing.
