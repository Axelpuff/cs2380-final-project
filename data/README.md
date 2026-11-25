# Source data

Not included in the repo. From the repo root:

```
git clone --depth 1 https://github.com/datameet/maps.git data/dm_maps
git clone --depth 1 https://github.com/thecont1/india-votes-data.git data/india-votes-data
```

- `dm_maps`: DataMeet shapefiles. The analysis reads `assembly-constituencies/India_AC.shp` and `parliamentary-constituencies/india_pc_2019.shp`.
- `india-votes-data`: Election Commission results. The analysis reads `archive/2024 Parliamentary Elections India.csv` and the assembly files in `data/csv/`.

Population (1971 census, 2011 census, Technical Group projections to 2036) and state GDP (2022-23) are typed into `analysis/apportion.py` with their sources in the comments.

`page/topo_ac.json` and `page/topo_states.json` are simplified from the DataMeet shapes. Check each source's licence before redistributing.
