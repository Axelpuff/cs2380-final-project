# Source data

Not included in the repo. From the repo root:

```
git clone --depth 1 https://github.com/datameet/maps.git data/dm_maps
git clone --depth 1 https://github.com/thecont1/india-votes-data.git data/india-votes-data
mkdir -p data/census2011
curl -L -o data/census2011/DDW_PCA0000_2011_Indiastatedist.xlsx \
  "https://censusindia.gov.in/nada/index.php/catalog/6191/download/9268/DDW_PCA0000_2011_Indiastatedist.xlsx"
```

- `dm_maps`: DataMeet shapefiles. The analysis reads `assembly-constituencies/India_AC.shp` and `parliamentary-constituencies/india_pc_2019.shp`.
- `india-votes-data`: Election Commission results. The analysis reads `archive/2024 Parliamentary Elections India.csv` and the assembly files in `data/csv/`.
- `census2011`: the Census of India 2011 Primary Census Abstract for India, states and districts. It's the "PCA SD" table, catalog 6191 on censusindia.gov.in, published by the Office of the Registrar General. Used for the reserved-seat work in `04_reserved_seats.md`, which needs SC and ST shares by state.
  - **Size and checksum:** 1.4 MB. SHA-256 `7a8f70d46c43b5dd30eefe920f251752f69f6af8589594c21ac06499074646f5`, as downloaded on 27 Nov 2026.
  - **Layout:** one sheet, `Sheet1`, with one row per area and residence type. `Level` is `India`, `STATE` or `DISTRICT`. `TRU` is `Total`, `Rural` or `Urban`. The columns needed here are `TOT_P`, `P_SC` and `P_ST` (persons), with `_M` and `_F` variants by sex. Codes are strings, e.g. State `"28"` and District `"532"`.
  - **Check after download:** the `India`/`Total` row should read `TOT_P` 1,210,854,977, `P_SC` 201,378,372 and `P_ST` 104,545,716. District rows sum exactly to their state rows.
  - **Boundaries are 2011, not today's.** Build current states from district rows:
    - Telangana is Andhra Pradesh (State 28) districts 532–541, Adilabad to Khammam. That gives 35,193,978 people, 15.4% SC and 9.3% ST. `apportion.py` uses 35,004 thousand for Telangana in 2011. The gap is presumably the Khammam mandals moved to Andhra Pradesh in 2014; this is not checked.
    - Ladakh is Jammu & Kashmir (State 01) districts 003–004, Leh and Kargil. That gives 274,289 people and 79.5% ST, matching `apportion.py`.
    - Daman & Diu and Dadra & Nagar Haveli appear separately. They merged in 2020.
  - **Reading it:** reading the `.xlsx` with pandas needs `openpyxl`.

Population (1971 census, 2011 census, Technical Group projections to 2036) and state GDP (2022-23) are typed into `analysis/apportion.py` with their sources in the comments.

`page/topo_ac.json` and `page/topo_states.json` are simplified from the DataMeet shapes. Check each source's licence before redistributing.
