# Simple RAG Hazard Report (One-shot)

- **Mode:** `simple_rag_hazard_one_shot`
- **Model:** `gpt-oss-120b`
- **Base URL:** `http://localhost:1234/v1`

## Snippet / Question
Hazard classification (Top-1). Use ONLY CONTEXT as evidence.

    Output requirements:
    - Direct Answer: ONE-LINE JSON as specified by the simple-rag prompt.
    - After the JSON, write a detailed, operator-style report:
      * Observed anomalies / signatures (bullet list)
      * Why the chosen hazard matches (cite specific retrieved fields: sampleData, keywords/altLabel, triggers/causes, impacts)
      * 1–3 close alternatives and why they were rejected (with citations)
      * What would confirm/deny (additional measurements / logs).

    The snippet is a raw telemetry; Focus on anomalies onset/recovery trajectory and plateau behavior.

    SNIPPET:
    
00:00,50
00:10,55
00:20,60
00:30,62
00:40,400
00:50,420
01:00,415
01:10,410
01:20,405


ADDITIONAL REQUIREMENTS:
- After the Direct Answer JSON, provide a Detailed Report with: hazard overview; why this match (with citations); operator recommendations; further information links (from cited hazard card sources).

## Final Answer
**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Power_Grid_Failure_Blackout","label":"Power Grid Failure / Blackout","confidence":0.55,"evidence":["[Knowledge:145 hazards:Hazard_Power_Grid_Failure_Blackout] The sample data shows a time‑series of outage metrics (timestamp, customers_out) that can exhibit a sudden jump when an outage begins.","[Knowledge:20 hazards:Hazard_Blackout] Describes blackout impacts and typical data structures for power outages."],"notes":"The snippet displays a rapid increase in the measured value at 00:40, consistent with the onset of a large‑scale power outage where the number of customers affected spikes sharply."}
```

**Detailed Report**

- **Hazard Overview**
  - **Name:** Power Grid Failure / Blackout  
  - **Group:** Technological  
  - **Subtype:** Infrastructure Failure / Disruption  
  - **Typical Data:** Time‑stamped records of outage metrics such as number of customers affected, total customers, and outage percentage (e.g., `timestamp_utc,fips,customers_out,customers_total,outage_pct`).  

- **Why This Hazard Matches the Snippet**
  - The snippet is a simple two‑column time series (`time,value`) showing a relatively low baseline (≈50–62) that abruptly rises to ≈400 and stays elevated.  
  - Such a pattern mirrors the typical signature of a power outage: before the event, few customers are out; when the grid fails, the count spikes sharply and then remains high while the outage persists.  
  - The hazard card for **Power Grid Failure / Blackout** explicitly mentions “high‑frequency (e.g., 15‑minute) county‑level electric outage snapshots with customers‑out counts”【[Knowledge:145 hazards:Hazard_Power_Grid_Failure_Blackout]】, matching the structure of the provided data.  

- **Operator Recommendations**
  1. **Validate Data Source:** Confirm that the metric represents “customers out” or a similar outage indicator rather than another physical measurement.  
  2. **Correlate with Grid Events:** Cross‑reference the timestamps with utility incident logs to verify the onset of an outage at 00:40.  
  3. **Assess Impact Scope:** Use additional fields (e.g., total customers, outage percentage) if available to quantify the severity and geographic extent.  
  4. **Trigger Response Protocols:** If this represents a real‑time detection of a blackout, initiate restoration crews, public communication, and load‑shedding strategies as per grid operator SOPs.  

- **Further Information Links**
  - NOAA Power Outage Data description: https://catalog.data.gov/dataset/eagle-i-outage-data  
  - U.S. DOE OE‑417 Electric Emergency Incident Reports (critical infrastructure failures): httpshttps://www.oe.netl.doe.gov/OE417_annual_summary.aspx  
  - General blackout mitigation guidance (IEEE, NERC): https://www.nerc.com/standards/blackout-mitigation  

*All evidence and reasoning are derived solely from the provided knowledge base.*

## Metrics
```json
{
  "citation_count": 3,
  "min_citations_threshold": 1,
  "has_min_citations": true,
  "uses_retrieval": true,
  "llm_calls": 1
}
```

## Retrieved Context
### Knowledge
```
[Knowledge:141 hazards:Hazard_Pacific_Heatwave Pacific Heatwave] HAZARD_ID: hazards:Hazard_Pacific_Heatwave
LABEL: Pacific Heatwave
GROUP: Climatological
SUBTYPE: Marine Incident
ALIASES: The Blob; Pacific Heatwave
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: The Blob. Schlüsselwörter: Pacific Heatwave. Sources: https://en.wikipedia.org/wiki/Coronal_mass_ejection | NOAA NCEI ERDDAP OISST (daily SST) | https://www.ncei.noaa.gov/erddap/griddap/ncdc_oisst_v2_avhrr_by_time_zlev_lat_lon.html. Sample data: ts_utc,lat,lon,sst_c,anom_c
2014-08-15T12:00:00Z,40.0,-140.0,18.42,2.10
2014-08-16T12:00:00Z,40.0,-140.0,18.55,2.23
2014-08-17T12:00:00Z,40.0,-140.0,18.61,2.29

Source description: Daily gridded sea-surface temperature (SST) values (and optional anomalies) extracted for a Pacific region/time window; used to characterize marine heatwave / “Pacific heatwave” conditions.
Source: NOAA NCEI ERDDAP OISST (daily SST) | https://www.ncei.noaa.gov/erddap/griddap/ncdc_oisst_v2_avhrr_by_time_zlev_lat_lon.html.
VERBALIZED_EN: Caused by hazard(s): Climate change. Keywords: The Blob. Schlüsselwörter: Pacific Heatwave. Sources: https://en.wikipedia.org/wiki/Coronal_mass_ejection | NOAA NCEI ERDDAP OISST (daily SST) | …

[Knowledge:46 hazards:Hazard_Derecho Derecho] HAZARD_ID: hazards:Hazard_Derecho
LABEL: Derecho
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: derecho; straight-line winds; bow echo; Derecho; geradlinige Winde; Bogenecho
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: derecho; straight-line winds; bow echo. Schlüsselwörter: Derecho; geradlinige Winde; Bogenecho. Sources: https://en.wikipedia.org/wiki/Derecho | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: derecho; straight-line winds; bow …

[Knowledge:49 hazards:Hazard_Downburst_Microburst Downburst / Microburst] HAZARD_ID: hazards:Hazard_Downburst_Microburst
LABEL: Downburst / Microburst
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: convective downdraft; downburst outflow; microburst (<4 km); macroburst (>4 km); damaging straight-line winds; thunderstorm gust front; rapid wind shear; aviation hazard; short-lived local footprint; konvektiver Abwind; Fallböe (Downburst) (auch: Fallwind); Mikroburst (<4 km); Makroburst (>4 km); schadensträchtige geradlinige Böen; Böenfront; rasche Windscherung; Gefahr für Luftfahrt; kurzlebig und lokal begrenzt
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: convective downdraft; downburst outflow; microburst (<4 km); macroburst (>4 km); damaging straight-line winds; thunderstorm gust front; rapid wind shear; aviation hazard; short-lived local footprint. Schlüsselwörter: konvektiver Abwind; Fallböe (Downburst) (auch: Fallwind); Mikroburst (<4 km); Makroburst (>4 km); schadensträchtige geradlinige Böen; Böenfront; rasche Windscherung; Gefahr für Luftfahrt; kurzlebig und lokal begrenzt. Sources: https://www.undrr.org/understanding-disaster-risk/terminology/hips/mh0101 | https://www.noaa.gov/jetstream/wind_damage | NOAA NCEI Storm Events Database (bulk CSV) …

[Knowledge:131 hazards:Hazard_Nocturnal_Tornado Nocturnal Tornado] HAZARD_ID: hazards:Hazard_Nocturnal_Tornado
LABEL: Nocturnal Tornado
GROUP: Meteorological
SUBTYPE: Tornado
ALIASES: Tornado; Großtrombe; Windhose; Wasserhose; nächtlicher tornado
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: Tornado; Großtrombe; Windhose; Wasserhose. Schlüsselwörter: nächtlicher tornado. Sources: https://en.wikipedia.org/wiki/Nocturnal_tornado | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: Tornado; Großtrombe; Windhose; …

[Knowledge:80 hazards:Hazard_Hail Hail] HAZARD_ID: hazards:Hazard_Hail
LABEL: Hail
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: hail; hailstorm; large hail; Hagel; Hagelsturm; Großhagel
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: hail; hailstorm; large hail. Schlüsselwörter: Hagel; Hagelsturm; Großhagel. Sources: https://en.wikipedia.org/wiki/Hail | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: hail; hailstorm; large hail. Schlüsselwörter: Hagel; Hagelsturm; Großhagel. Sources: …

[Knowledge:21 hazards:Hazard_Blizzard Blizzard] HAZARD_ID: hazards:Hazard_Blizzard
LABEL: Blizzard
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: blizzard; snowstorm; whiteout; blowing snow; Blizzard; Schneesturm; Whiteout; Schneeverwehungen
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: blizzard; snowstorm; whiteout; blowing snow. Schlüsselwörter: Blizzard; Schneesturm; Whiteout; Schneeverwehungen. Sources: https://en.wikipedia.org/wiki/Blizzard | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. …

[Knowledge:193 hazards:Hazard_Tornado Tornado] HAZARD_ID: hazards:Hazard_Tornado
LABEL: Tornado
GROUP: Meteorological
SUBTYPE: Tornado
ALIASES: tornado; twister; funnel cloud; violent wind; Tornado; Wirbelsturm; Trichterwolke; heftiger Wind
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: tornado; twister; funnel cloud; violent wind. Schlüsselwörter: Tornado; Wirbelsturm; Trichterwolke; heftiger Wind. Sources: https://en.wikipedia.org/wiki/Tornado | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. …

[Knowledge:164 hazards:Hazard_Severe_Weather Severe Weather] HAZARD_ID: hazards:Hazard_Severe_Weather
LABEL: Severe Weather
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: severe weather; Unwetter
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: severe weather. Schlüsselwörter: Unwetter. Sources: https://en.wikipedia.org/wiki/Severe_weather | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: severe weather. Schlüsselwörter: Unwetter. Sources: https://en.wikipedia.org/wiki/Severe_weather | NOAA NCEI Storm …

[Knowledge:61 hazards:Hazard_Extreme_Weather Extreme Weather] HAZARD_ID: hazards:Hazard_Extreme_Weather
LABEL: Extreme Weather
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: weather extremes; Extremwetter
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: weather extremes. Schlüsselwörter: Extremwetter. Sources: https://en.wikipedia.org/wiki/Extreme_weather | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: weather extremes. Schlüsselwörter: Extremwetter. Sources: https://en.wikipedia.org/wiki/Extreme_weather | …

[Knowledge:165 hazards:Hazard_Severe_Winter_Conditions Severe Winter Conditions] HAZARD_ID: hazards:Hazard_Severe_Winter_Conditions
LABEL: Severe Winter Conditions
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: severe winter conditions; Strenge Winterbedingungen
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: severe winter conditions. Schlüsselwörter: Strenge Winterbedingungen. Sources: https://en.wikipedia.org/wiki/Severe_winter_conditions | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: severe winter conditions. …

[Knowledge:23 hazards:Hazard_Carrington_Event Carrington Event] HAZARD_ID: hazards:Hazard_Carrington_Event
LABEL: Carrington Event
GROUP: Black Swan
SUBTYPE: Space Weather
ALIASES: geomagnetic storm; solar storm; space weather; aurora; Geomagnetischer Sturm; Sonnensturm; Weltraumwetter; Polarlicht
BM25_TEXT_EN: Caused by hazard(s): Space weather solar storm. Keywords: geomagnetic storm; solar storm; space weather; aurora. Schlüsselwörter: Geomagnetischer Sturm; Sonnensturm; Weltraumwetter; Polarlicht. Sources: https://en.wikipedia.org/wiki/Carrington_Event | NASA OMNIWeb (near-Earth solar wind & geomagnetic indices) | https://omniweb.gsfc.nasa.gov/ | NOAA NCEI Geomagnetic Indices (Kp/Dst/aa/AE) | https://www.ncei.noaa.gov/products/geomagnetic-indices. Sample data: time_utc,Bz_nT,Vsw_km_s,Np_cm3,Kp,Dst_nT
2024-05-10 00:00, -15.2, 720, 12.3, 6, -85
2024-05-10 01:00, -18.7, 760, 14.1, 7, -120
2024-05-10 02:00, -10.5, 690, 10.8, 6, -95

Source description: OMNI provides time-shifted near-Earth solar wind plasma/magnetic field parameters and geomagnetic indices (e.g., Kp, Dst) at multiple cadences.
Source: NASA OMNIWeb (near-Earth solar wind & geomagnetic indices) | …

[Knowledge:71 hazards:Hazard_Freezing_Rain_Ice_Storm Freezing Rain / Ice Storm] HAZARD_ID: hazards:Hazard_Freezing_Rain_Ice_Storm
LABEL: Freezing Rain / Ice Storm
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: supercooled raindrops; freezing on contact; glaze ice accretion; powerline/tree loading; black ice; transport disruption; infrastructure outages; aircraft icing; temperature inversion; unterkühlte Regentropfen; Gefrieren beim Auftreffen; Glatteis/Eisansatz; Eisauflast auf Leitungen/Bäumen; Blitzeis (Black Ice) (Begriff variiert); Verkehrsbehinderungen; Infrastrukturausfall (Strom/Kommunikation); Flugzeugvereisung; Temperaturinversion
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: supercooled raindrops; freezing on contact; glaze ice accretion; powerline/tree loading; black ice; transport disruption; infrastructure outages; aircraft icing; temperature inversion. Schlüsselwörter: unterkühlte Regentropfen; Gefrieren beim Auftreffen; Glatteis/Eisansatz; Eisauflast auf Leitungen/Bäumen; Blitzeis (Black Ice) (Begriff variiert); Verkehrsbehinderungen; Infrastrukturausfall (Strom/Kommunikation); Flugzeugvereisung; Temperaturinversion. Sources: https://www.undrr.org/understanding-disaster-risk/terminology/hips/mh0506 | …

[Knowledge:179 hazards:Hazard_Storm_2 Storm] HAZARD_ID: hazards:Hazard_Storm_2
LABEL: Storm
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: storm (general); Sturm
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: storm (general). Schlüsselwörter: Sturm. Sources: https://en.wikipedia.org/wiki/Storm | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: storm (general). Schlüsselwörter: Sturm. Sources: https://en.wikipedia.org/wiki/Storm | NOAA NCEI Storm Events Database (bulk CSV) | …

[Knowledge:178 hazards:Hazard_Storm Storm] HAZARD_ID: hazards:Hazard_Storm
LABEL: Storm
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: extreme wind; windstorm; gale; downburst; Extremwind; Windsturm; Sturm; Downburst
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: extreme wind; windstorm; gale; downburst. Schlüsselwörter: Extremwind; Windsturm; Sturm; Downburst. Sources: https://en.wikipedia.org/wiki/Windstorm | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: extreme wind; windstorm; …

[Knowledge:22 hazards:Hazard_Blizzard_Winter_Storm Blizzard / Winter Storm] HAZARD_ID: hazards:Hazard_Blizzard_Winter_Storm
LABEL: Blizzard / Winter Storm
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: blizzard/winter storm; Schneesturm/Wintersturm
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: blizzard/winter storm. Schlüsselwörter: Schneesturm/Wintersturm. Sources: https://en.wikipedia.org/wiki/Blizzard/Winter_storm | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: blizzard/winter storm. Schlüsselwörter: …

[Knowledge:57 hazards:Hazard_Extra_Tropical_Storm Extra-tropical Storm] HAZARD_ID: hazards:Hazard_Extra_Tropical_Storm
LABEL: Extra-tropical Storm
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: extra-tropical storm; Außertropischer Sturm
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: extra-tropical storm. Schlüsselwörter: Außertropischer Sturm. Sources: https://en.wikipedia.org/wiki/Extra-tropical_storm | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: extra-tropical storm. Schlüsselwörter: Außertropischer Sturm. …

[Knowledge:173 hazards:Hazard_Space_Weather_Solar_Storm Space Weather (Solar Storm)] HAZARD_ID: hazards:Hazard_Space_Weather_Solar_Storm
LABEL: Space Weather (Solar Storm)
GROUP: Extraterrestrial
SUBTYPE: Space Weather
ALIASES: space weather; solar storm; geomagnetic storm; solar flare; CME; Weltraumwetter; Sonnensturm; geomagnetischer Sturm; Sonnenflare
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: space weather; solar storm; geomagnetic storm; solar flare; CME. Schlüsselwörter: Weltraumwetter; Sonnensturm; geomagnetischer Sturm; Sonnenflare; CME. Sources: https://en.wikipedia.org/wiki/Space_weather | NASA OMNIWeb (near-Earth solar wind & geomagnetic indices) | https://omniweb.gsfc.nasa.gov/ | NOAA NCEI Geomagnetic Indices (Kp/Dst/aa/AE) | https://www.ncei.noaa.gov/products/geomagnetic-indices. Sample data: time_utc,Bz_nT,Vsw_km_s,Np_cm3,Kp,Dst_nT
2024-05-10 00:00, -15.2, 720, 12.3, 6, -85
2024-05-10 01:00, -18.7, 760, 14.1, 7, -120
2024-05-10 02:00, -10.5, 690, 10.8, 6, -95

Source description: OMNI provides time-shifted near-Earth solar wind plasma/magnetic field parameters and geomagnetic indices (e.g., Kp, Dst) at multiple cadences.
Source: NASA OMNIWeb (near-Earth solar wind & geomagnetic indices) | …

[Knowledge:112 hazards:Hazard_Lightning_Thunderstorms Lightning/Thunderstorms] HAZARD_ID: hazards:Hazard_Lightning_Thunderstorms
LABEL: Lightning/Thunderstorms
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: lightning/thunderstorms; Blitz/Gewitter
BM25_TEXT_EN: Caused by hazard(s): Storm|hazards:hazard lightning. Keywords: lightning/thunderstorms. Schlüsselwörter: Blitz/Gewitter. Sources: https://en.wikipedia.org/wiki/Lightning/Thunderstorms | NOAA NCEI Storm Events Database (bulk CSV) | https://www.ncei.noaa.gov/stormevents/ftp.jsp. Sample data: EVENT_ID,BEGIN_DATE_TIME,END_DATE_TIME,STATE,EVENT_TYPE,MAGNITUDE,MAGNITUDE_TYPE,BEGIN_LAT,BEGIN_LON,DEATHS_DIRECT,INJURIES_DIRECT,DAMAGE_PROPERTY,DAMAGE_CROPS
1023456,2021-06-28 22:50:00,2021-06-28 23:20:00,IOWA,Hail,2.75,in,41.60,-93.62,0,0,0,0
1023457,2021-06-29 01:12:00,2021-06-29 01:45:00,IOWA,Tornado,0,EF,41.74,-93.57,0,0,250000,0
1023458,2021-02-15 03:00:00,2021-02-16 12:00:00,TEXAS,Winter Storm,0,,31.76,-99.90,0,0,5000000,0

Source description: NOAA Storm Events Database records U.S. severe weather events (e.g., hail, tornado, blizzard) with time, location, impacts, and narratives; bulk CSV files are available by year..
VERBALIZED_EN: Caused by hazard(s): Storm|hazards:hazard lightning. Keywords: …

[Knowledge:82 hazards:Hazard_Heat_Burst Heat Burst] HAZARD_ID: hazards:Hazard_Heat_Burst
LABEL: Heat Burst
GROUP: Meteorological
SUBTYPE: Extreme Temperature
ALIASES: Satans Storm; Heat burst
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: Satans Storm. Schlüsselwörter: Heat burst. Sources: https://en.wikipedia.org/wiki/Heat_burst | https://ericsweatherlibrary.com. Sample data: …

[Knowledge:36 hazards:Hazard_Coronal_Mass_Ejection Coronal Mass Ejection] HAZARD_ID: hazards:Hazard_Coronal_Mass_Ejection
LABEL: Coronal Mass Ejection
GROUP: Extraterrestrial
SUBTYPE: Space Weather
ALIASES: coronal mass ejection; Coronal Mass Ejection
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: coronal mass ejection. Schlüsselwörter: Coronal Mass Ejection. Sources: https://en.wikipedia.org/wiki/Coronal_mass_ejection | NASA OMNIWeb (near-Earth solar wind & geomagnetic indices) | https://omniweb.gsfc.nasa.gov/ | NOAA NCEI Geomagnetic Indices (Kp/Dst/aa/AE) | https://www.ncei.noaa.gov/products/geomagnetic-indices. Sample data: time_utc,Bz_nT,Vsw_km_s,Np_cm3,Kp,Dst_nT
2024-05-10 00:00, -15.2, 720, 12.3, 6, -85
2024-05-10 01:00, -18.7, 760, 14.1, 7, -120
2024-05-10 02:00, -10.5, 690, 10.8, 6, -95

Source description: OMNI provides time-shifted near-Earth solar wind plasma/magnetic field parameters and geomagnetic indices (e.g., Kp, Dst) at multiple cadences.
Source: NASA OMNIWeb (near-Earth solar wind & geomagnetic indices) | https://omniweb.gsfc.nasa.gov/

---

date,time_utc,kp
2024-05-10,00:00,6
2024-05-10,03:00,7
2024-05-10,06:00,8

Source description: Official archive for geomagnetic activity indices such as Kp (planetary K-index) and Dst, …

[Knowledge:86 hazards:Hazard_Ice_Jam_Flooding_Including_Debris Ice-jam Flooding (Including Debris)] HAZARD_ID: hazards:Hazard_Ice_Jam_Flooding_Including_Debris
LABEL: Ice-jam Flooding (Including Debris)
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: river ice jam; breakup/freeze-up; channel constriction; backwater rise; sudden release wave (jave); debris/ice blockage at bridges; local inundation; rapid onset flooding; mechanical damage from ice; Eisstau; Eisaufbruch/Eisbildung; Verengung des Flussquerschnitts; Rückstau/Anstau; plötzliche Freisetzungswelle (jave/Eisstoß) (Begriff variiert); Treibgut-/Eisblockade an Brücken; lokale Überflutung; plötzliches Hochwasser; mechanische Schäden durch Eisgang
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: river ice jam; breakup/freeze-up; channel constriction; backwater rise; sudden release wave (jave); debris/ice blockage at bridges; local inundation; rapid onset flooding; mechanical damage from ice. Schlüsselwörter: Eisstau; Eisaufbruch/Eisbildung; Verengung des Flussquerschnitts; Rückstau/Anstau; plötzliche Freisetzungswelle (jave/Eisstoß) (Begriff variiert); Treibgut-/Eisblockade an Brücken; lokale Überflutung; plötzliches Hochwasser; mechanische Schäden durch Eisgang. Sources: Wikipedia | …

[Knowledge:1 Hazard_Cellular_Jamming Cellular jamming] HAZARD_ID: Hazard_Cellular_Jamming
LABEL: Cellular jamming
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: cellular jamming, mobile phone jammer, cell phone jammer, GSM jamming, UMTS jamming, LTE jamming, 4G jamming, 5G jamming, base station disruption, network outage, no service, call drops, SMS failure, data interruption, coverage loss; Mobilfunk-Jamming, Handy-Jammer, GSM-Störung, UMTS-Störung, LTE-Störung, 4G-Störung, 5G-Störung, Basisstation gestört, Netzausfall, kein Netz, Gesprächsabbruch, SMS-Ausfall, Datenunterbruch, Abdeckungsausfall
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism|hazards:hazard war. Keywords: cellular jamming, mobile phone jammer, cell phone jammer, GSM jamming, UMTS jamming, LTE jamming, 4G jamming, 5G jamming, base station disruption, network outage, no service, call drops, SMS failure, data interruption, coverage loss. Schlüsselwörter: Mobilfunk-Jamming, Handy-Jammer, GSM-Störung, UMTS-Störung, LTE-Störung, 4G-Störung, 5G-Störung, Basisstation gestört, Netzausfall, kein Netz, Gesprächsabbruch, SMS-Ausfall, Datenunterbruch, Abdeckungsausfall. Sources: Wikipedia | https://en.wikipedia.org/wiki/Mobile_phone_jammer | INRIA …

[Knowledge:63 hazards:Hazard_Flash_Flood Flash Flood] HAZARD_ID: hazards:Hazard_Flash_Flood
LABEL: Flash Flood
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: flash flood; rapid flooding; intense rainfall; Sturzflut; plötzliche Überflutung; Starkregen
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: flash flood; rapid flooding; intense rainfall. Schlüsselwörter: Sturzflut; plötzliche Überflutung; Starkregen. Sources: Wikipedia | https://en.wikipedia.org/wiki/Flash_flood | NOAA NCEI Storm Events Database | https://www.ncei.noaa.gov/stormevents/ | Storm Data Bulk CSV Format | https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/Storm-Data-Bulk-csv-Format.pdf. Sample data: event_id,begin_date_time,end_date_time,state,cz_name,event_type,injuries_direct,deaths_direct,damage_property_usd,begin_lat,begin_lon,episode_narrative
2234501,2023-09-17 17:05,2023-09-17 23:10,IL,Cook,Flash Flood,6,0,18000000,41.83,-87.68,"Training thunderstorms produced rapid urban inundation; vehicles stranded; swiftwater rescues"
2234502,2024-07-10 14:30,2024-07-10 18:00,AZ,Pima,Flash Flood,1,0,750000,32.22,-110.97,"Short-duration intense rainfall caused arroyo flooding and road washouts"

Source description: …

[Knowledge:72 hazards:Hazard_GNSS_Disruption_Jamming_Spoofing_Outage GNSS Disruption] HAZARD_ID: hazards:Hazard_GNSS_Disruption_Jamming_Spoofing_Outage
LABEL: GNSS Disruption
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: PNT dependency; GNSS jamming; GNSS spoofing; timing loss; navigation errors; aviation/maritime disruption; emergency services impacts; critical infrastructure synchronization; interference detection; fallback systems; Abhängigkeit von PNT (Positionierung/Navigation/Timing); GNSS-Jamming (Störung); GNSS-Spoofing (Täuschung); Verlust der Zeitreferenz; Navigationsfehler; Störungen in Luftfahrt/Schifffahrt; Auswirkungen auf Rettungsdienste; Synchronisation kritischer Infrastrukturen; Erkennung von Funkstörungen; Ausweichsysteme (z.B. Trägheitsnavigation/eLoran) (Begriffe variieren)
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: PNT dependency; GNSS jamming; GNSS spoofing; timing loss; navigation errors; aviation/maritime disruption; emergency services impacts; critical infrastructure synchronization; interference detection; fallback systems. Schlüsselwörter: Abhängigkeit von PNT (Positionierung/Navigation/Timing); GNSS-Jamming (Störung); GNSS-Spoofing (Täuschung); Verlust der Zeitreferenz; Navigationsfehler; Störungen in …

[Knowledge:69 hazards:Hazard_Freeze_Thaw_Thaw_Hazard_To_Ground_Infrastructure Freeze–thaw (Thaw) Hazard To Ground/infrastructure] HAZARD_ID: hazards:Hazard_Freeze_Thaw_Thaw_Hazard_To_Ground_Infrastructure
LABEL: Freeze–thaw (Thaw) Hazard To Ground/infrastructure
GROUP: Meteorological
SUBTYPE: Extreme Temperature
ALIASES: freeze–thaw cycles; frost heave; thaw settlement; pavement cracking/potholes; rail/bridge deformation; pipeline/foundation movement; slope instability; drainage impairment; seasonal transition risk; Frost-Tau-Wechsel; Frosthebung; Tau-Setzung (auch: Auftau-Setzung); Fahrbahnrisse/Schlaglöcher; Gleis-/Brückenverformung; Bewegung von Leitungen/Fundamenten; Hanginstabilität; Beeinträchtigung der Entwässerung; Risiko in Übergangsjahreszeiten
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: freeze–thaw cycles; frost heave; thaw settlement; pavement cracking/potholes; rail/bridge deformation; pipeline/foundation movement; slope instability; drainage impairment; seasonal transition risk. Schlüsselwörter: Frost-Tau-Wechsel; Frosthebung; Tau-Setzung (auch: Auftau-Setzung); Fahrbahnrisse/Schlaglöcher; Gleis-/Brückenverformung; Bewegung von Leitungen/Fundamenten; Hanginstabilität; Beeinträchtigung der Entwässerung; Risiko in Übergangsjahreszeiten. Sources: Wikipedia | …

[Knowledge:74 hazards:Hazard_Gamma_Ray_Burst Gamma Ray Burst] HAZARD_ID: hazards:Hazard_Gamma_Ray_Burst
LABEL: Gamma Ray Burst
GROUP: Extraterrestrial
SUBTYPE: Space Weather
ALIASES: gamma ray burst; Gamma Ray Burst
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: gamma ray burst. Schlüsselwörter: Gamma Ray Burst. Sources: https://en.wikipedia.org/wiki/Gamma-ray_burst | NASA HEASARC Swift Gamma-Ray Bursts Catalog | https://heasarc.gsfc.nasa.gov/w3browse/swift/swiftgrb.html. Sample data: grb_name,trigger_time_utc,ra_deg,dec_deg,t90_s,fluence_15_150keV
GRB200219A,2020-02-19T01:10:00,143.21,12.34,25.6,2.3e-06
GRB210731A,2021-07-31T14:42:00,210.55,-5.67,12.4,8.1e-07

Source description: Catalog of gamma-ray bursts observed by Swift with trigger time, position, and multi-instrument properties..
VERBALIZED_EN: Caused by hazard(s): Impact event. Keywords: gamma ray burst. Schlüsselwörter: Gamma Ray Burst. Sources: https://en.wikipedia.org/wiki/Gamma-ray_burst | NASA HEASARC Swift Gamma-Ray Bursts Catalog | https://heasarc.gsfc.nasa.gov/w3browse/swift/swiftgrb.html. Sample data: …

[Knowledge:30 hazards:Hazard_Cloud_Service_Outage_Systemic_Cloud_Dependency_Failure Cloud Service Outage / Systemic Cloud Dependency Failure] HAZARD_ID: hazards:Hazard_Cloud_Service_Outage_Systemic_Cloud_Dependency_Failure
LABEL: Cloud Service Outage / Systemic Cloud Dependency Failure
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: cloud provider outage; shared service dependency; multi-tenant platform failure; regional/AZ disruption; cascading IT outages; identity/API unavailability; data access loss; business continuity; concentration risk; resilience architecture; Ausfall von Cloud-Anbietern; gemeinsame Abhängigkeiten (Shared Dependency); Mehrmandantenplattform (Multi-Tenant) (Begriffe teils englisch); Region-/Availability-Zone-Ausfall (AZ); kaskadierende IT-Ausfälle; Identity-/API-Nichtverfügbarkeit; Verlust des Datenzugriffs; Business-Continuity-Management; Konzentrationsrisiko; Resilienz-Architektur
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: cloud provider outage; shared service dependency; multi-tenant platform failure; regional/AZ disruption; cascading IT outages; identity/API unavailability; data access loss; business continuity; concentration risk; resilience architecture. Schlüsselwörter: Ausfall von Cloud-Anbietern; gemeinsame Abhängigkeiten (Shared Dependency); Mehrmandantenplattform …

[Knowledge:64 hazards:Hazard_Flood Flood] HAZARD_ID: hazards:Hazard_Flood
LABEL: Flood
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: Hochwasser; high water
BM25_TEXT_EN: Location: River area spree. Related activity: Residential use. Caused by hazard(s): Atmospheric river extreme precipitation event. Caused by: Heavy rainfall. Consequences: Injury; Property damage. Creates risk: Flood impact. Keywords: high water. Schlüsselwörter: Hochwasser. Sources: https://en.wikipedia.org/wiki/Flood; Wikipedia | https://en.wikipedia.org/wiki/Flood | USGS Water Services Instantaneous Values API | https://waterservices.usgs.gov/docs/instantaneous-values/instantaneous-values-details/ | NOAA NCEI Storm Events Database | https://www.ncei.noaa.gov/stormevents/. Sample data: sample data for high water ... 5000 liters/minute/m2; site_no,ts_utc,discharge_cfs,gage_height_ft,qualifiers
01646500,2025-09-29T12:00:00Z,28400,18.42,A
01646500,2025-09-29T12:15:00Z,30100,18.77,A
01646500,2025-09-29T12:30:00Z,32600,19.10,A
01646500,2025-09-29T12:45:00Z,35200,19.45,A

Source description: High-frequency streamgage time series (discharge and stage) used to quantify flood peaks, rise rate, and duration at a gauge.
Source: USGS Water Services Instantaneous …

[Knowledge:73 hazards:Hazard_GPS_Jamming GPS Jamming] HAZARD_ID: hazards:Hazard_GPS_Jamming
LABEL: GPS Jamming
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: GPS jamming, GNSS interference, lost link, return-to-home failure; GPS-Jamming, GNSS-Störung, Link-Verlust, Return-to-Home-Ausfall
BM25_TEXT_EN: Caused by hazard(s): GNSS disruption (jamming/spoofing/outage)|hazards:hazard major ICT outage affecting critical services|hazards:hazard cyberattack causing physical disruption. Keywords: GPS jamming, GNSS interference, lost link, return-to-home failure. Schlüsselwörter: GPS-Jamming, GNSS-Störung, Link-Verlust, Return-to-Home-Ausfall. Sources: Wikipedia | https://en.wikipedia.org/wiki/GPS_jamming | GNSS Dataset Under Jamming, Spoofing, and Meaconing (Zenodo, Jammertest 2024) | https://zenodo.org/records/15911359. Sample data: ts_utc,lat_deg,lon_deg,fix_type,num_sats,hdop,cn0_avg_dBHz,interference_label
2025-06-14T10:00:00Z,69.2801,16.0102,3D,12,0.8,43.5,clean
2025-06-14T10:00:01Z,69.2801,16.0102,3D,12,0.8,43.2,clean
2025-06-14T10:00:02Z,69.2801,16.0102,2D,7,2.4,31.0,jamming
2025-06-14T10:00:03Z,69.2800,16.0100,NOFIX,0,99.9,0.0,jamming
2025-06-14T10:00:04Z,69.2800,16.0100,NOFIX,0,99.9,0.0,jamming

Source description: Controlled …

[Knowledge:166 hazards:Hazard_Smog Smog] HAZARD_ID: hazards:Hazard_Smog
LABEL: Smog
GROUP: Chemical
SUBTYPE: Visibility
ALIASES: smog
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Consequences: Great smog of london. Keywords: smog. Schlüsselwörter: smog. Sources: https://en.wikipedia.org/wiki/Smog | OpenAQ Measurements API | https://docs.openaq.org/resources/measurements. Sample data: datetime_utc,location,parameter,value,unit,lat,lon
2024-11-01T12:00:00Z,Zurich Stampfenbachstrasse,pm25,18.2,µg/m³,47.38,8.54
2024-11-01T12:00:00Z,Zurich Stampfenbachstrasse,no2,42.1,µg/m³,47.38,8.54

Source description: OpenAQ provides harmonized air quality measurements from many providers with timestamps, coordinates, pollutant parameter, value and units..
VERBALIZED_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Consequences: Great smog of london. Keywords: smog. Schlüsselwörter: smog. Sources: https://en.wikipedia.org/wiki/Smog | OpenAQ Measurements API | https://docs.openaq.org/resources/measurements. Sample data: datetime_utc,location,parameter,value,unit,lat,lon
2024-11-01T12:00:00Z,Zurich …

[Knowledge:3 hazards:Hazard_Air_Pollution Air pollution] HAZARD_ID: hazards:Hazard_Air_Pollution
LABEL: Air pollution
GROUP: Chemical
SUBTYPE: Visibility
ALIASES: air pollution, smog, haze, particulate matter, PM2.5, PM10, soot, smoke, poor air quality, reduced visibility, air quality alert; Luftverschmutzung, Smog, Dunst, Feinstaub, PM2.5, PM10, Ruß, Rauch, schlechte Luftqualität, Sichtbehinderung, Luftqualitätswarnung
BM25_TEXT_EN: Caused by hazard(s): Environmental pollution|hazards:hazard industrial explosion|hazards:hazard critical infrastructure failure. Keywords: air pollution, smog, haze, particulate matter, PM2.5, PM10, soot, smoke, poor air quality, reduced visibility, air quality alert. Schlüsselwörter: Luftverschmutzung, Smog, Dunst, Feinstaub, PM2.5, PM10, Ruß, Rauch, schlechte Luftqualität, Sichtbehinderung, Luftqualitätswarnung. Sources: https://en.wikipedia.org/wiki/Air_pollution | OpenAQ Measurements API | https://docs.openaq.org/resources/measurements. Sample data: datetime_utc,location,parameter,value,unit,lat,lon
2024-11-01T12:00:00Z,Zurich Stampfenbachstrasse,pm25,18.2,µg/m³,47.38,8.54
2024-11-01T12:00:00Z,Zurich Stampfenbachstrasse,no2,42.1,µg/m³,47.38,8.54

Source description: OpenAQ provides harmonized air …

[Knowledge:117 hazards:Hazard_Major_ICT_Outage_Affecting_Critical_Services Major ICT Outage Affecting Critical Services] HAZARD_ID: hazards:Hazard_Major_ICT_Outage_Affecting_Critical_Services
LABEL: Major ICT Outage Affecting Critical Services
GROUP: Digital
SUBTYPE: Cyber Incident
ALIASES: ICT outage; network outage; internet outage; service disruption; IKT-Ausfall; Netzausfall; Internetausfall; Dienststörung
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: ICT outage; network outage; internet outage; service disruption. Schlüsselwörter: IKT-Ausfall; Netzausfall; Internetausfall; Dienststörung. Sources: Wikipedia | https://en.wikipedia.org/wiki/Internet_outage | CAIDA IODA | https://catalog.caida.org/dataset/ioda. Sample data: ts_utc,entity_type,entity_code,signal_type,signal_value,baseline_value,anomaly_score
2025-10-01T08:00:00Z,country,IR,routing,0.42,0.95,0.88
2025-10-01T08:05:00Z,country,IR,active_probing,0.38,0.93,0.91
2025-10-01T08:10:00Z,country,IR,dns,0.55,0.96,0.79

Source description: Internet-outage detection time series by country/ASN (routing, active probing, DNS) suitable as raw signals for major ICT outages affecting services.
Source: CAIDA IODA | https://catalog.caida.org/dataset/ioda.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: ICT outage; network outage; …

[Knowledge:195 hazards:Hazard_Tropical_Cyclone Tropical Cyclone] HAZARD_ID: hazards:Hazard_Tropical_Cyclone
LABEL: Tropical Cyclone
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: tropical cyclone; hurricane; typhoon; storm surge; high winds; Tropischer Wirbelsturm; Hurrikan; Taifun; Sturmflut; starke Winde
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: tropical cyclone; hurricane; typhoon; storm surge; high winds. Schlüsselwörter: Tropischer Wirbelsturm; Hurrikan; Taifun; Sturmflut; starke Winde. Sources: https://en.wikipedia.org/wiki/Tropical_cyclone | NOAA NCEI IBTrACS Tropical Cyclone Best Track | https://www.ncei.noaa.gov/products/international-best-track-archive. Sample data: sid,season,name,iso_time,lat,lon,usa_wind,usa_pres,agency
2019273N11311,2019,DORIAN,2019-09-01 12:00:00,26.6,-77.0,145,910,USA
2019273N11311,2019,DORIAN,2019-09-01 18:00:00,26.7,-77.3,150,910,USA
2019273N11311,2019,DORIAN,2019-09-02 00:00:00,26.8,-77.6,160,910,USA

Source description: IBTrACS provides global tropical cyclone best-track positions and intensities (multiple agencies) at synoptic intervals..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: tropical cyclone; hurricane; typhoon; storm surge; high winds. Schlüsselwörter: Tropischer Wirbelsturm; …

[Knowledge:174 hazards:Hazard_Spaceflight_Launch_Re_Entry_Accident Spaceflight Launch / Re-Entry Accident] HAZARD_ID: hazards:Hazard_Spaceflight_Launch_Re_Entry_Accident
LABEL: Spaceflight Launch / Re-Entry Accident
GROUP: Transportation
SUBTYPE: Transport Incident
ALIASES: spaceflight accident; launch failure; re-entry accident; Raumfahrtunfall; Startversagen; Wiedereintrittsunfall
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: spaceflight accident; launch failure; re-entry accident. Schlüsselwörter: Raumfahrtunfall; Startversagen; Wiedereintrittsunfall. Sources: https://en.wikipedia.org/wiki/List_of_spaceflight-related_accidents_and_incidents | FAA Commercial Space Data | https://www.faa.gov/data_research/commercial_space_data. Sample data: date,operator,vehicle,mission_type,event_type,outcome
2014-10-31,Scaled Composites,SpaceShipTwo,Test flight,Mishap,Fatal
2023-04-20,SpaceX,Starship,Test flight,Anomaly,Vehicle lost

Source description: FAA commercial space data and safety records (launches, reentries, mishaps) for licensed commercial space transportation in the U.S.
Source: FAA Commercial Space Data | https://www.faa.gov/data_research/commercial_space_data.
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: spaceflight accident; launch failure; re-entry accident. …

[Knowledge:136 hazards:Hazard_Ocean_Acidification Ocean Acidification] HAZARD_ID: hazards:Hazard_Ocean_Acidification
LABEL: Ocean Acidification
GROUP: Environmental
SUBTYPE: Marine Incident
ALIASES: ocean pH decline; CO2 uptake; carbonate chemistry shift; reduced carbonate ions; aragonite saturation; impacts on corals/shellfish; food-web effects; fisheries/aquaculture risk; monitoring (pH/TA/DIC); Ozeanversauerung; pH-Abnahme; CO2-Aufnahme; Verschiebung der Karbonatchemie; weniger Carbonat-Ionen; Aragonit-Sättigung; Auswirkungen auf Korallen/Schalentiere; Effekte auf Nahrungsnetze; Risiko für Fischerei/Aquakultur; Monitoring (pH/TA/DIC) (TA=Gesamtalkalinität; DIC=gelöster anorganischer Kohlenstoff)
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: ocean pH decline; CO2 uptake; carbonate chemistry shift; reduced carbonate ions; aragonite saturation; impacts on corals/shellfish; food-web effects; fisheries/aquaculture risk; monitoring (pH/TA/DIC). Schlüsselwörter: Ozeanversauerung; pH-Abnahme; CO2-Aufnahme; Verschiebung der Karbonatchemie; weniger Carbonat-Ionen; Aragonit-Sättigung; Auswirkungen auf Korallen/Schalentiere; Effekte auf Nahrungsnetze; Risiko für Fischerei/Aquakultur; Monitoring (pH/TA/DIC) (TA=Gesamtalkalinität; DIC=gelöster …

[Knowledge:144 hazards:Hazard_Postfire_Debris_Flow_Hazard Postfire Debris-flow Hazard] HAZARD_ID: hazards:Hazard_Postfire_Debris_Flow_Hazard
LABEL: Postfire Debris-flow Hazard
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: burn scar; vegetation loss; soil water repellency; intense short rainfall; runoff amplification; debris flow initiation; boulders/ash/logs; channel avulsion; flash flood coupling; near-term after fire; Brandnarbe; Vegetationsverlust; wasserabweisender Boden; kurzer Starkregen; verstärkter Oberflächenabfluss; Auslösung von Muren/Schuttströmen (Mure vs Schuttstrom); Geröll/Asche/Holz; Rinnenverlagerung (Avulsion); Kopplung mit Sturzflut; v. a. kurz nach Brand
BM25_TEXT_EN: Caused by hazard(s): Wildfire|hazards:hazard landslide. Keywords: burn scar; vegetation loss; soil water repellency; intense short rainfall; runoff amplification; debris flow initiation; boulders/ash/logs; channel avulsion; flash flood coupling; near-term after fire. Schlüsselwörter: Brandnarbe; Vegetationsverlust; wasserabweisender Boden; kurzer Starkregen; verstärkter Oberflächenabfluss; Auslösung von Muren/Schuttströmen (Mure vs Schuttstrom); Geröll/Asche/Holz; Rinnenverlagerung (Avulsion); Kopplung mit Sturzflut; v. a. kurz nach Brand. Sources: …

[Knowledge:155 hazards:Hazard_Rogue_Autonomous_Drone Rogue Autonomous Drone] HAZARD_ID: hazards:Hazard_Rogue_Autonomous_Drone
LABEL: Rogue Autonomous Drone
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: rogue drone, autonomous weapon, mis-targeting, friendly fire, autonomy failure; Rogue-Drohne, autonome Waffe, Fehlzielerfassung, Eigenbeschuss, Autonomiefehler
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard GNSS disruption (jamming/spoofing/outage)|hazards:hazard cloud service outage / systemic cloud dependency failure|hazards:hazard major ICT outage affecting critical services. Keywords: rogue drone, autonomous weapon, mis-targeting, friendly fire, autonomy failure. Schlüsselwörter: Rogue-Drohne, autonome Waffe, Fehlzielerfassung, Eigenbeschuss, Autonomiefehler. Sources: Wikipedia | https://en.wikipedia.org/wiki/Lethal_autonomous_weapon | BASiC UAV Sensor Failures Dataset (Zenodo) | https://doi.org/10.5281/zenodo.8195068. Sample data: ts_ms,GPS_Status,Lat_deg,Lon_deg,Alt_m,Mode,Vel_mps,Fail_Status
0,6,33.6845,73.0479,584.2,AUTO,4.1,0
200,6,33.6846,73.0480,584.3,AUTO,4.2,0
400,6,33.6847,73.0481,584.4,AUTO,4.1,0
600,1,33.6847,73.0481,584.4,LAND,0.8,1
800,1,33.6847,73.0481,584.2,LAND,0.4,1

Source description: Autonomous UAV flight log …

[Knowledge:19 hazards:Hazard_Bioengineering_Misuse_Accident Bioengineering Misuse/Accident] HAZARD_ID: hazards:Hazard_Bioengineering_Misuse_Accident
LABEL: Bioengineering Misuse/Accident
GROUP: Black Swan
SUBTYPE: Biological Incident
ALIASES: bioengineering; synthetic biology; genetic engineering; biosecurity; lab accident; Bioengineering; Synthetische Biologie; Gentechnik; Biosicherheit; Laborunfall
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: bioengineering; synthetic biology; genetic engineering; biosecurity; lab accident. Schlüsselwörter: Bioengineering; Synthetische Biologie; Gentechnik; Biosicherheit; Laborunfall. Sources: Wikipedia | https://en.wikipedia.org/wiki/Synthetic_biology | NIH OSP Incident Reporting | https://osp.od.nih.gov/policies/incident-reporting-december-2023/. Sample data: incident_id,report_date,facility_type,bs_level,agent_or_construct,incident_type,exposure_overt,route_of_exposure,primary_containment_breached,secondary_containment_breached,persons_exposed,medical_evaluation,corrective_actions
NIH-OSP-0001,2025-09-14,University Lab,BSL-2,rDNA plasmid (non-replicating),Spill,No,NA,Yes,No,0,No,"Decontaminated area; retrained staff; updated SOP"
NIH-OSP-0002,2025-11-02,Biotech Company,BSL-3,Engineered influenza …

[Knowledge:154 hazards:Hazard_Rockfall_Wet Rockfall (Wet)] HAZARD_ID: hazards:Hazard_Rockfall_Wet
LABEL: Rockfall (Wet)
GROUP: Hydrological
SUBTYPE: Mass Movement
ALIASES: rockfall (wet); Steinschlag (nass)
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: rockfall (wet). Schlüsselwörter: Steinschlag (nass). Sources: https://en.wikipedia.org/wiki/Rockfall_%28wet%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,landslide_type,trigger,fatality_count,notes
GLC000810,2021-12-01,Canada,Rock fall,Rain,0,"Wet-season rockfall after prolonged rainfall"
GLC000811,2024-01-17,Norway,Rock fall,Rain,1,"Rain-on-snow and thaw conditions"

Source description: Rockfall incident rows where trigger is rainfall-related; used for wet-condition rockfall sampling.
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: rockfall (wet). Schlüsselwörter: Steinschlag (nass). Sources: https://en.wikipedia.org/wiki/Rockfall_%28wet%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: …

[Knowledge:38 hazards:Hazard_Crowd_Crush_Stampede_Human_Crushing Crowd Crush / Stampede (Human Crushing)] HAZARD_ID: hazards:Hazard_Crowd_Crush_Stampede_Human_Crushing
LABEL: Crowd Crush / Stampede (Human Crushing)
GROUP: Societal
SUBTYPE: Mass Fatality
ALIASES: crowd surge; high density; bottlenecks; compressive asphyxia; trampling; egress failure; panic triggers; venue design; crowd management; mass gathering; Menschenandrang (Crowd Surge) (Begriff variiert); hohe Personendichte; Engstellen; Kompressionsasphyxie; Niedertrampeln; Versagen von Fluchtwegen; Panik-Auslöser; Veranstaltungsdesign; Crowd-Management (Begriff gebräuchlich); Großveranstaltung/Massenansammlung
BM25_TEXT_EN: Caused by hazard(s): Civil unrest. Keywords: crowd surge; high density; bottlenecks; compressive asphyxia; trampling; egress failure; panic triggers; venue design; crowd management; mass gathering. Schlüsselwörter: Menschenandrang (Crowd Surge) (Begriff variiert); hohe Personendichte; Engstellen; Kompressionsasphyxie; Niedertrampeln; Versagen von Fluchtwegen; Panik-Auslöser; Veranstaltungsdesign; Crowd-Management (Begriff gebräuchlich); Großveranstaltung/Massenansammlung. Sources: https://www.undrr.org/understanding-disaster-risk/terminology/hips/so0302 | Zenodo: List of past crowd crushes | …

[Knowledge:104 hazards:Hazard_Land_Use_Driven_Destabilization Land-use Driven Destabilization] HAZARD_ID: hazards:Hazard_Land_Use_Driven_Destabilization
LABEL: Land-use Driven Destabilization
GROUP: Environmental
SUBTYPE: Environmental Degradation
ALIASES: land use change; deforestation; erosion; destabilization; Landnutzungsänderung; Entwaldung; Erosion; Destabilisierung
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: land use change; deforestation; erosion; destabilization. Schlüsselwörter: Landnutzungsänderung; Entwaldung; Erosion; Destabilisierung. Sources: Hansen Global Forest Change 2000-2024 data download | https://storage.googleapis.com/earthenginepartners-hansen/GFC-2024-v1.12/download.html ; Google Earth Engine dataset description | https://developers.google.com/earth-engine/datasets/catalog/UMD_hansen_global_forest_change_2024_v1_12. Sample data: lat,lon,treecover2000_pct,loss_flag,lossyear,gain_flag
-3.120, -60.021, 78, 1, 18, 0
-3.125, -60.030, 65, 0, 0, 0
-3.130, -60.040, 82, 1, 23, 1

Source description: Pixel-level land-use change indicators from the Hansen/UMD Global Forest Change dataset (tree cover baseline, forest loss year, forest gain). Commonly used as a raw proxy for land-use-driven ecosystem destabilization (deforestation fronts, …

[Knowledge:183 hazards:Hazard_Submarine_Landslide_Submarine_Mass_Movement Submarine Landslide / Submarine Mass Movement] HAZARD_ID: hazards:Hazard_Submarine_Landslide_Submarine_Mass_Movement
LABEL: Submarine Landslide / Submarine Mass Movement
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: submarine gravitational mass movement; seafloor slope failure; triggers: earthquake/storm waves; turbidity current; sediment liquefaction; tsunami generation; cable/pipeline damage; fjords/canyons/deltas; rapid runout; submariner Hangrutsch (auch: untermeerischer); gravitativer Massenabgang am Meeresboden; Hangversagen; Auslöser: Erdbeben/Sturmwellen; Trübestrom (turbidity current); Sedimentverflüssigung; Tsunami-Auslösung; Schäden an Unterseekabeln/Pipelines; Fjorde/Canyons/Deltas; schneller Abgang
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: submarine gravitational mass movement; seafloor slope failure; triggers: earthquake/storm waves; turbidity current; sediment liquefaction; tsunami generation; cable/pipeline damage; fjords/canyons/deltas; rapid runout. Schlüsselwörter: submariner Hangrutsch (auch: untermeerischer); gravitativer Massenabgang am Meeresboden; Hangversagen; Auslöser: Erdbeben/Sturmwellen; Trübestrom (turbidity current); Sedimentverflüssigung; Tsunami-Auslösung; Schäden an …

[Knowledge:150 hazards:Hazard_Radiological_Dispersal Radiological Dispersal] HAZARD_ID: hazards:Hazard_Radiological_Dispersal
LABEL: Radiological Dispersal
GROUP: Radiological
SUBTYPE: Nuclear-Radiological Incident
ALIASES: radiological dispersal; contamination; radiation release; Radiologische Dispersion; Kontamination; Freisetzung radioaktiver Stoffe
BM25_TEXT_EN: Caused by hazard(s): War. Keywords: radiological dispersal; contamination; radiation release. Schlüsselwörter: Radiologische Dispersion; Kontamination; Freisetzung radioaktiver Stoffe. Sources: https://en.wikipedia.org/wiki/Radiological_contamination | IAEA INES database | https://www.iaea.org/resources/databases/international-nuclear-and-radiological-event-scale | IAEA Nuclear Events Web-based System (NEWS) | https://www.iaea.org/resources/databases/nuclear-events-web-based-system. Sample data: event_date,country,event_title,ines_level,mechanism,notes
2013-09-01,CountryX,"Radiological source damaged during transport; contamination contained",2,"Dispersion/contamination","Local decontamination required"
2016-05-22,CountryY,"Scrap yard orphan source ruptured; localized contamination",3,"Dispersion/contamination","Public exposure controlled"
2020-01-14,CountryZ,"Medical source mishandled; …

[Knowledge:138 hazards:Hazard_One_Sided_Violence_UCDP One-sided Violence (UCDP)] HAZARD_ID: hazards:Hazard_One_Sided_Violence_UCDP
LABEL: One-sided Violence (UCDP)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: violence against civilians, civilian targeting; einseitige Gewalt, Gewalt gegen Zivilpersonen, gezielte Angriffe
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: violence against civilians, civilian targeting. Schlüsselwörter: einseitige Gewalt, Gewalt gegen Zivilpersonen, gezielte Angriffe. Sources: https://en.wikipedia.org/wiki/Uppsala_Conflict_Data_Program | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Terrorism. Keywords: violence against civilians, civilian targeting. Schlüsselwörter: einseitige Gewalt, Gewalt gegen Zivilpersonen, gezielte Angriffe. …

[Knowledge:47 hazards:Hazard_Desertification Desertification] HAZARD_ID: hazards:Hazard_Desertification
LABEL: Desertification
GROUP: Climatological
SUBTYPE: Environmental Degradation
ALIASES: desertification; land degradation; aridification; Desertifikation; Landdegradation; Aridifizierung
BM25_TEXT_EN: Caused by hazard(s): Drought. Keywords: desertification; land degradation; aridification. Schlüsselwörter: Desertifikation; Landdegradation; Aridifizierung. Sources: UNCCD Data Dashboard | https://data.unccd.int/ ; UNCCD Drought Hotspots 2023-2025 report (context) | https://www.unccd.int/sites/default/files/2025-07/Drought%20Hotspots%202023-2025_ENG.pdf. Sample data: country_iso3,year,land_degraded_pct,aridity_index,notes
NER,2020,38.4,0.18,"Drylands; monitoring indicator export"
ESP,2020,12.7,0.45,"Semi-arid regions; monitoring indicator export"

Source description: National-level desertification/land degradation and drought-related indicators served via the UNCCD Data Dashboard (country/year metrics used for reporting and monitoring).
Source: UNCCD Data Dashboard | https://data.unccd.int/.
VERBALIZED_EN: Caused by hazard(s): Drought. Keywords: desertification; land degradation; aridification. Schlüsselwörter: Desertifikation; …

[Knowledge:31 hazards:Hazard_Coastal_Erosion_Shoreline_Retreat Coastal Erosion / Shoreline Retreat] HAZARD_ID: hazards:Hazard_Coastal_Erosion_Shoreline_Retreat
LABEL: Coastal Erosion / Shoreline Retreat
GROUP: Hydrological
SUBTYPE: Environmental Degradation
ALIASES: sediment loss; wave and current action; storm-driven erosion; shoreline retreat; cliff/bluff failure; sea-level rise interaction; coastal infrastructure undermining; beach narrowing; managed retreat/setbacks; littoral transport; Sedimentabtrag; Wellen- und Strömungswirkung; sturmgetriebene Erosion; Küstenrückgang/Strandrückzug; Kliff-/Steiluferabbrüche; Wechselwirkung mit Meeresspiegelanstieg; Unterminierung von Küsteninfrastruktur; Strandverengung; Managed Retreat/Bauabstände (Begriffe teils englisch); Längstransport (littoral)
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: sediment loss; wave and current action; storm-driven erosion; shoreline retreat; cliff/bluff failure; sea-level rise interaction; coastal infrastructure undermining; beach narrowing; managed retreat/setbacks; littoral transport. Schlüsselwörter: Sedimentabtrag; Wellen- und Strömungswirkung; sturmgetriebene Erosion; Küstenrückgang/Strandrückzug; Kliff-/Steiluferabbrüche; Wechselwirkung mit Meeresspiegelanstieg; Unterminierung von …

[Knowledge:6 hazards:Hazard_Antimicrobial_Resistance Antimicrobial Resistance] HAZARD_ID: hazards:Hazard_Antimicrobial_Resistance
LABEL: Antimicrobial Resistance
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: antimicrobial-resistant pathogens; antibiotic misuse/overuse; treatment failure; higher morbidity/mortality; healthcare-associated infections; One Health; surveillance systems; stewardship; resistance genes spread; antimikrobielle Resistenz (AMR); antibiotikaresistente Erreger; Fehl- und Übergebrauch von Antibiotika; Therapieversagen; höhere Morbidität/Mortalität; nosokomiale Infektionen; One-Health-Ansatz; Überwachung (Surveillance); Antibiotic-Stewardship (Begriff gebräuchlich); Verbreitung von Resistenzgenen
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: antimicrobial-resistant pathogens; antibiotic misuse/overuse; treatment failure; higher morbidity/mortality; healthcare-associated infections; One Health; surveillance systems; stewardship; resistance genes spread. Schlüsselwörter: antimikrobielle Resistenz (AMR); antibiotikaresistente Erreger; Fehl- und Übergebrauch von Antibiotika; Therapieversagen; höhere Morbidität/Mortalität; nosokomiale Infektionen; One-Health-Ansatz; Überwachung (Surveillance); Antibiotic-Stewardship (Begriff …

[Knowledge:142 hazards:Hazard_Pandemic Pandemic] HAZARD_ID: hazards:Hazard_Pandemic
LABEL: Pandemic
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: pandemic; global outbreak; infectious disease; Pandemie; weltweiter Ausbruch; Infektionskrankheit
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: pandemic; global outbreak; infectious disease. Schlüsselwörter: Pandemie; weltweiter Ausbruch; Infektionskrankheit. Sources: https://en.wikipedia.org/wiki/Pandemic | Our World in Data COVID dataset docs | https://docs.owid.io/projects/covid/en/latest/dataset.html | OWID COVID catalog CSV | https://catalog.ourworldindata.org/garden/covid/latest/compact/compact.csv. Sample data: date,iso_code,location,new_cases,new_deaths,icu_patients,reproduction_rate
2020-03-15,ITA,Italy,3590,368,NA,NA
2021-01-15,USA,United States,229494,3856,28792,0.93
2022-07-15,ZAF,South Africa,6813,37,NA,1.07

Source description: Pandemic surveillance time series (location-date rows) from OWID’s COVID-19 dataset (cases/deaths and related indicators). Useful as a generic pandemic-style ‘line list’ time series sample.
Source: Our World in Data COVID dataset docs | https://docs.owid.io/projects/covid/en/latest/dataset.html | OWID COVID catalog CSV | …

[Knowledge:55 hazards:Hazard_Eutrophication Eutrophication] HAZARD_ID: hazards:Hazard_Eutrophication
LABEL: Eutrophication
GROUP: Environmental
SUBTYPE: Environmental Degradation
ALIASES: nutrient loading (N/P); agricultural runoff; sewage effluent; algal blooms; hypoxia/anoxia; fish kills; harmful algal blooms (HABs); degraded water quality; coastal dead zones; Eutrophierung; Nährstoffeinträge (N/P); landwirtschaftlicher Abfluss; Abwassereinleitungen; Algenblüten; Hypoxie/Anoxie; Fischsterben; schädliche Algenblüten (HABs) (auch: toxische Algenblüten); Verschlechterung der Wasserqualität; Todeszonen im Küstenmeer (dead zones) (Begriff gebräuchlich)
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: nutrient loading (N/P); agricultural runoff; sewage effluent; algal blooms; hypoxia/anoxia; fish kills; harmful algal blooms (HABs); degraded water quality; coastal dead zones. Schlüsselwörter: Eutrophierung; Nährstoffeinträge (N/P); landwirtschaftlicher Abfluss; Abwassereinleitungen; Algenblüten; Hypoxie/Anoxie; Fischsterben; schädliche Algenblüten (HABs) (auch: toxische Algenblüten); Verschlechterung der Wasserqualität; Todeszonen im Küstenmeer (dead zones) (Begriff gebräuchlich). Sources: Water Quality Portal web services | …

[Knowledge:119 hazards:Hazard_Malfunctioning_Robot_System_Failure Malfunctioning Robot] HAZARD_ID: hazards:Hazard_Malfunctioning_Robot_System_Failure
LABEL: Malfunctioning Robot
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: robot malfunction, control system failure, unsafe motion, software fault; Roboterfehlfunktion, Steuerungsausfall, gefährliche Bewegung, Softwarefehler
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard cyber supply chain attack|hazards:hazard cloud service outage / systemic cloud dependency failure. Keywords: robot malfunction, control system failure, unsafe motion, software fault. Schlüsselwörter: Roboterfehlfunktion, Steuerungsausfall, gefährliche Bewegung, Softwarefehler. Sources: Wikipedia | https://en.wikipedia.org/wiki/Industrial_robot | UCI Robot Execution Failures | https://archive.ics.uci.edu/ml/datasets/Robot+Execution+Failures. Sample data: failure_id,timestep,Fx,Fy,Fz,Tx,Ty,Tz,failure_class
R01,1,-12.3,5.4,31.1,0.21,-0.10,0.05,collision
R01,2,-13.0,5.7,30.8,0.24,-0.12,0.06,collision
R01,3,-15.2,6.2,29.5,0.31,-0.15,0.09,collision
R01,4,-18.9,7.0,27.0,0.44,-0.20,0.12,collision
R01,5,-22.1,7.8,24.2,0.60,-0.28,0.18,collision

Source description: Time-series force/torque sensor readings (15 samples per failure) collected …

[Knowledge:180 hazards:Hazard_Storm_Surge Storm Surge] HAZARD_ID: hazards:Hazard_Storm_Surge
LABEL: Storm Surge
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: storm surge; Sturmflut
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event|hazards:hazard storm. Keywords: storm surge. Schlüsselwörter: Sturmflut. Sources: https://en.wikipedia.org/wiki/Storm_surge | https://tidesandcurrents.noaa.gov/api/. Sample data: datetime_utc,station_id,water_level_m,predicted_tide_m,residual_surge_m
2024-10-09T12:00Z,8724580,1.23,0.54,0.69
2024-10-09T12:06Z,8724580,1.27,0.55,0.72
2024-10-09T12:12Z,8724580,1.31,0.56,0.75

Source description: Time-series water-level observations and tide predictions from a NOAA tide gauge; storm-surge (residual) is computed as observed water level minus predicted tide.
Source: NOAA CO-OPS Data API | https://tidesandcurrents.noaa.gov/api/.
VERBALIZED_EN: Caused by hazard(s): Atmospheric river extreme precipitation event|hazards:hazard storm. Keywords: storm surge. Schlüsselwörter: Sturmflut. Sources: https://en.wikipedia.org/wiki/Storm_surge | https://tidesandcurrents.noaa.gov/api/. Sample data: …

[Knowledge:32 hazards:Hazard_Coastal_Flood Coastal Flood] HAZARD_ID: hazards:Hazard_Coastal_Flood
LABEL: Coastal Flood
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: coastal flood; Küstenhochwasser
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: coastal flood. Schlüsselwörter: Küstenhochwasser. Sources: Wikipedia | https://en.wikipedia.org/wiki/Coastal_flooding | NOAA NCEI Storm Events Database | https://www.ncei.noaa.gov/stormevents/ | NWS Charleston Coastal Flood Event Database (example CSV) | https://www.weather.gov/chs/coastalflood. Sample data: gauge_id,event_start_local,event_end_local,max_water_level_ft_mllw,minor_flood,moderate_flood,major_flood
CHS,2023-09-08 07:12,2023-09-08 10:45,7.32,1,0,0
CHS,2024-01-13 20:05,2024-01-14 01:30,7.89,1,1,0
CHS,2024-08-05 09:40,2024-08-05 15:10,8.41,1,1,1

Source description: Tide-gauge-based coastal flooding event log (start/end and peak water level vs. thresholds) useful for coastal flood frequency and severity.
Source: NWS Charleston Coastal Flood Event Database | https://www.weather.gov/chs/coastalflood.
VERBALIZED_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: coastal flood. Schlüsselwörter: Küstenhochwasser. …

[Knowledge:125 hazards:Hazard_Mass_Psychogenic_Illness Mass Psychogenic Illness] HAZARD_ID: hazards:Hazard_Mass_Psychogenic_Illness
LABEL: Mass Psychogenic Illness
GROUP: Societal
SUBTYPE: Psychogenic Incident
ALIASES: mass psychogenic illness; massenpsychogene erkrankung
BM25_TEXT_EN: Caused by hazard(s): Civil unrest. Keywords: mass psychogenic illness. Schlüsselwörter: massenpsychogene erkrankung. Sources: https://en.wikipedia.org/wiki/Mass_psychogenic_illness | Wikipedia list of mass panic cases | https://en.wikipedia.org/wiki/List_of_mass_panic_cases | Wikidata Query Service | https://query.wikidata.org/. Sample data: event_name,start_date,country,setting,affected_count,suspected_driver
"Tanganyika laughter epidemic",1962-01-30,Tanzania,Schools,1000,"psychogenic"
"Pokémon incident",1997-12-16,Japan,TV broadcast,685,"photosensitive seizures + social contagion"
"Iran schoolgirl illness reports",2022-11-01,Iran,Schools,1000,"possible psychogenic component"

Source description: Event-list style dataset of mass psychogenic / mass panic incidents (date/place/affected). Suitable as a historical incident table (compiled from public references and Wikidata-style event metadata).
Source: Wikipedia list of mass panic cases | …

[Knowledge:43 hazards:Hazard_Dancing_Plague Dancing Plague] HAZARD_ID: hazards:Hazard_Dancing_Plague
LABEL: Dancing Plague
GROUP: Black Swan
SUBTYPE: Psychogenic Incident
ALIASES: dance plague; dancing mania; mass psychogenic illness; choreomania; Tanzwut; Tanzplage; Massenpsychogene Erkrankung; Choreomanie
BM25_TEXT_EN: Caused by hazard(s): Critical infrastructure failure. Keywords: dance plague; dancing mania; mass psychogenic illness; choreomania. Schlüsselwörter: Tanzwut; Tanzplage; Massenpsychogene Erkrankung; Choreomanie. Sources: https://en.wikipedia.org/wiki/Dancing_plague_of_1518 | Wikidata Query Service | https://query.wikidata.org/ | Wikipedia mass psychogenic illness | https://en.wikipedia.org/wiki/Mass_psychogenic_illness. Sample data: event_name,start_date,location,estimated_affected,notes
"Dancing mania of 1518",1518-07-01,"Strasbourg (then Holy Roman Empire)",400,"Historical mass dancing episode"
"Aachen dancing mania",1374-06-01,"Aachen region",NA,"Part of 1374 dancing mania wave"

Source description: Historical event-list rows for dancing mania episodes (dates/locations/affected counts) as represented in public historical registries (e.g., Wikidata/Wikipedia-derived structured fields).
Source: Wikidata Query Service | …

[Knowledge:26 hazards:Hazard_Chemical_Spill Chemical Spill] HAZARD_ID: hazards:Hazard_Chemical_Spill
LABEL: Chemical Spill
GROUP: Chemical
SUBTYPE: Industrial Incident
ALIASES: chemical spill; hazardous materials spill; contamination; Chemieunfall; Chemikalienverschüttung; Kontamination
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Keywords: chemical spill; hazardous materials spill; contamination. Schlüsselwörter: Chemieunfall; Chemikalienverschüttung; Kontamination. Sources: https://en.wikipedia.org/wiki/Chemical_spill | https://github.com/data-liberation-project/phmsa-hazmat-incident-reports. Sample data: report_number,incident_date,mode,hazard_class,material_name,quantity_released,unit,waterway_affected,injuries,fatalities
2024-001234,2024-05-18,RAIL,2.3,Chlorine,2,car,Yes,0,0
2023-009876,2023-08-03,HWY,3,Gasoline,1200,gallon,No,1,0

Source description: Hazardous materials transportation incident reports (DOT Form 5800.1) with structured fields on mode, material, quantity released, and impacts; can be filtered for spills affecting waterways or communities.
Source: PHMSA Hazmat Transportation Incident Reports (Data Liberation Project) | …

[Knowledge:172 hazards:Hazard_Space_Warfare_Debris_ASAT Space Warfare Debris (ASAT)] HAZARD_ID: hazards:Hazard_Space_Warfare_Debris_ASAT
LABEL: Space Warfare Debris (ASAT)
GROUP: Extraterrestrial
SUBTYPE: Space Hazard
ALIASES: anti-satellite weapon; space debris; ASAT test; orbital debris; Antisatellitenwaffe; Weltraummüll; ASAT-Test; Orbittrümmer
BM25_TEXT_EN: Caused by hazard(s): Earthquake|hazards:hazard flood|hazards:hazard impact event. Keywords: anti-satellite weapon; space debris; ASAT test; orbital debris. Schlüsselwörter: Antisatellitenwaffe; Weltraummüll; ASAT-Test; Orbittrümmer. Sources: https://en.wikipedia.org/wiki/Space_debris | CelesTrak NORAD GP Element Sets (TLE) | https://www.celestrak.org/NORAD/elements/. Sample data: ISS (ZARYA)
1 25544U 98067A   26050.50000000  .00016717  00000-0  10270-3 0  9991
2 25544  51.6447  45.1234 0005123  82.3456  12.3456 15.50123456789012

Source description: Two-Line Element (TLE) sets provide orbital elements for tracked objects (satellites, rocket bodies, debris) derived from SGP4/SDP4 general perturbations..
VERBALIZED_EN: Caused by hazard(s): Earthquake|hazards:hazard flood|hazards:hazard impact event. Keywords: anti-satellite weapon; space debris; ASAT test; orbital debris. Schlüsselwörter: Antisatellitenwaffe; …

[Knowledge:59 hazards:Hazard_Extraterrestrial_Threat_Asteroid_Impact_Space_Weather Extraterrestrial Threat (Asteroid Impact/Space Weather)] HAZARD_ID: hazards:Hazard_Extraterrestrial_Threat_Asteroid_Impact_Space_Weather
LABEL: Extraterrestrial Threat (Asteroid Impact/Space Weather)
GROUP: Black Swan
SUBTYPE: Space Hazard
ALIASES: asteroid impact; near-Earth object; space weather; solar storm; Asteroideneinschlag; erdnahes Objekt; Weltraumwetter; Sonnensturm
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: asteroid impact; near-Earth object; space weather; solar storm. Schlüsselwörter: Asteroideneinschlag; erdnahes Objekt; Weltraumwetter; Sonnensturm. Sources: https://en.wikipedia.org/wiki/Impact_event | NASA JPL CNEOS Fireball and Bolide Reports (CSV/Excel) | https://cneos.jpl.nasa.gov/fireballs/ | NASA JPL CNEOS Sentry Impact Risk Table (machine-readable) | https://cneos.jpl.nasa.gov/sentry/ | NASA OMNIWeb (near-Earth solar wind & geomagnetic indices) | https://omniweb.gsfc.nasa.gov/. Sample data: datetime_utc,lat_deg,lon_deg,alt_km,vel_km_s,vx_km_s,vy_km_s,vz_km_s,impact_energy_kt
2013-02-15 03:20:26,54.4,61.1,23.3,18.6,-12.2,6.5,-12.2,440.0
2020-12-22 23:23:33,31.9,96.2,35.5,13.6,-10.1,2.0,-8.9,9.8

Source description: Chronological table of fireball/bolide events detected by U.S. Government sensors with …

[Knowledge:76 hazards:Hazard_Glacial_Lake_Outburst_Flood_GLOF Glacial Lake Outburst Flood (GLOF)] HAZARD_ID: hazards:Hazard_Glacial_Lake_Outburst_Flood_GLOF
LABEL: Glacial Lake Outburst Flood (GLOF)
GROUP: Black Swan
SUBTYPE: Marine Incident
ALIASES: glacial lake outburst flood; moraine dam; sudden flood; Gletscherseeausbruch; Moränendamm; Sturzflut
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: glacial lake outburst flood; moraine dam; sudden flood. Schlüsselwörter: Gletscherseeausbruch; Moränendamm; Sturzflut. Sources: https://en.wikipedia.org/wiki/Glacial_lake_outburst_flood | https://zenodo.org/records/7330345. Sample data: glof_id,event_year,country,region,dam_type,trigger,impact_type,reported_fatalities
GLOF-0123,2016,Nepal,Himalaya,Moraine,Rainfall/ice avalanche,Flood,0
GLOF-0456,1985,Peru,Cordillera Blanca,Moraine,Ice avalanche,Flood/debris flow,20

Source description: Global inventory of historical glacial lake outburst floods with standardized attributes on location, dam type, triggers, and impacts; supports event-based hazard modeling and frequency analysis.
Source: Glacier Lake Outburst Flood (GLOF) Database v3.0 (Zenodo) | https://zenodo.org/records/7330345.
VERBALIZED_EN: Caused by hazard(s): Atmospheric river extreme …

[Knowledge:127 hazards:Hazard_Mirage_Fata_Morgana Mirage / Fata Morgana] HAZARD_ID: hazards:Hazard_Mirage_Fata_Morgana
LABEL: Mirage / Fata Morgana
GROUP: Black Swan
SUBTYPE: Psychogenic Incident
ALIASES: mirage; Fata Morgana; superior mirage; optical illusion; refraction; Luftspiegelung; Überspiegelung; optische Täuschung; Brechung
BM25_TEXT_EN: Caused by hazard(s): Critical infrastructure failure. Keywords: mirage; Fata Morgana; superior mirage; optical illusion; refraction. Schlüsselwörter: Luftspiegelung; Fata Morgana; Überspiegelung; optische Täuschung; Brechung. Sources: https://en.wikipedia.org/wiki/Fata_Morgana_(mirage) | Wikidata Query Service | https://query.wikidata.org/. Sample data: obs_date,location,lat,lon,air_temp_c,sea_surface_temp_c,wind_mps,observer_report
2025-02-08,"Strait of Messina",38.19,15.56,12.4,15.1,3.2,"Fata Morgana reported; elevated images over horizon"
2025-03-17,"Arctic coast",69.65,18.95,-14.2,-1.0,5.8,"Superior mirage; inverted ship-like forms"
2025-07-03,"Great Lakes",43.07,-87.91,21.0,18.2,2.5,"Mirage over lake; refracted skyline"

Source description: Observation-style records for reported superior mirage/Fata Morgana events (date/location + met conditions). This is typically built from event reports; Wikidata can …

[Knowledge:94 hazards:Hazard_Internal_Conflict_UCDP_PRIO Internal Conflict (UCDP/PRIO)] HAZARD_ID: hazards:Hazard_Internal_Conflict_UCDP_PRIO
LABEL: Internal Conflict (UCDP/PRIO)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: intrastate conflict, civil war; innerstaatlicher Konflikt, Bürgerkrieg
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: intrastate conflict, civil war. Schlüsselwörter: innerstaatlicher Konflikt, Bürgerkrieg. Sources: https://en.wikipedia.org/wiki/Civil_war | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: intrastate conflict, civil war. Schlüsselwörter: innerstaatlicher Konflikt, Bürgerkrieg. Sources: https://en.wikipedia.org/wiki/Civil_war | UCDP Georeferenced Event Dataset …

[Knowledge:132 hazards:Hazard_Noise_Pollution Noise pollution] HAZARD_ID: hazards:Hazard_Noise_Pollution
LABEL: Noise pollution
GROUP: Chemical
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: noise pollution, excessive noise, industrial noise, traffic noise, construction noise, loud machinery, vibration, noise complaint, disruption, operational disruption, shutdown, curfew violation; Lärmbelastung, Lärmverschmutzung, übermäßiger Lärm, Industrielärm, Verkehrslärm, Baulärm, laute Maschinen, Vibrationen, Lärmbeschwerde, Störung, Betriebsstörung, Stilllegung
BM25_TEXT_EN: Caused by hazard(s): Critical infrastructure failure|hazards:hazard industrial explosion. Keywords: noise pollution, excessive noise, industrial noise, traffic noise, construction noise, loud machinery, vibration, noise complaint, disruption, operational disruption, shutdown, curfew violation. Schlüsselwörter: Lärmbelastung, Lärmverschmutzung, übermäßiger Lärm, Industrielärm, Verkehrslärm, Baulärm, laute Maschinen, Vibrationen, Lärmbeschwerde, Störung, Betriebsstörung, Stilllegung. Sources: https://en.wikipedia.org/wiki/Noise_pollution | https://www.eea.europa.eu/data-and-maps/data/data-on-noise-exposure-8. Sample data: …

[Knowledge:98 hazards:Hazard_Interstate_Conflict_UCDP_PRIO Interstate Conflict (UCDP/PRIO)] HAZARD_ID: hazards:Hazard_Interstate_Conflict_UCDP_PRIO
LABEL: Interstate Conflict (UCDP/PRIO)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: war between states, interstate war; zwischenstaatlicher Konflikt, Krieg zwischen Staaten
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: war between states, interstate war. Schlüsselwörter: zwischenstaatlicher Konflikt, Krieg zwischen Staaten. Sources: https://en.wikipedia.org/wiki/Interstate_war | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: war between states, interstate war. Schlüsselwörter: zwischenstaatlicher Konflikt, Krieg zwischen Staaten. Sources: …

[Knowledge:96 hazards:Hazard_Internationalized_Internal_Conflict_UCDP_PRIO Internationalized Internal Conflict (UCDP/PRIO)] HAZARD_ID: hazards:Hazard_Internationalized_Internal_Conflict_UCDP_PRIO
LABEL: Internationalized Internal Conflict (UCDP/PRIO)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: internal conflict with external states, foreign intervention; internationalisierter innerstaatlicher Konflikt, ausländische Intervention
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: internal conflict with external states, foreign intervention. Schlüsselwörter: internationalisierter innerstaatlicher Konflikt, ausländische Intervention. Sources: https://en.wikipedia.org/wiki/Proxy_war | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: internal …

[Knowledge:134 hazards:Hazard_Non_State_Conflict_UCDP Non-state Conflict (UCDP)] HAZARD_ID: hazards:Hazard_Non_State_Conflict_UCDP
LABEL: Non-state Conflict (UCDP)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: armed groups fighting, inter-group conflict; nichtstaatlicher Konflikt, Konflikt zwischen bewaffneten Gruppen
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: armed groups fighting, inter-group conflict. Schlüsselwörter: nichtstaatlicher Konflikt, Konflikt zwischen bewaffneten Gruppen. Sources: https://en.wikipedia.org/wiki/Uppsala_Conflict_Data_Program | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: armed groups fighting, inter-group conflict. Schlüsselwörter: nichtstaatlicher …

[Knowledge:92 hazards:Hazard_Industrial_Toxic_Release_Off_Site_Mass_Exposure Industrial Toxic Release (Off-site Mass Exposure)] HAZARD_ID: hazards:Hazard_Industrial_Toxic_Release_Off_Site_Mass_Exposure
LABEL: Industrial Toxic Release (Off-site Mass Exposure)
GROUP: Black Swan
SUBTYPE: Industrial Incident
ALIASES: toxic release; chemical leak; industrial accident; mass exposure; Giftfreisetzung; Chemikalienaustritt; Industrieunfall; Massenexposition
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Keywords: toxic release; chemical leak; industrial accident; mass exposure. Schlüsselwörter: Giftfreisetzung; Chemikalienaustritt; Industrieunfall; Massenexposition. Sources: https://en.wikipedia.org/wiki/Industrial_disaster | https://www.data-liberation-project.org/datasets/epa-risk-management-program-database/. Sample data: facility_id,accident_date,chemical,process,release_type,estimated_release_lb,offsite_impact,offsite_people_injured,offsite_people_evacuated
RMP-123456,2023-06-14,Chlorine,Water treatment,Gas release,800,Yes,3,250
RMP-234567,2021-09-02,Anhydrous ammonia,Refrigeration,Pipe rupture,1200,Yes,1,40

Source description: Structured accident-history and offsite-impact fields reported under EPA's Risk Management Program (112(r)) for facilities …

[Knowledge:176 hazards:Hazard_State_Based_Conflict_UCDP State-based Conflict (UCDP)] HAZARD_ID: hazards:Hazard_State_Based_Conflict_UCDP
LABEL: State-based Conflict (UCDP)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: government vs opponent, armed conflict with state party; staatlicher Konflikt, Regierungskonflikt, bewaffneter Konflikt mit Staat
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: government vs opponent, armed conflict with state party. Schlüsselwörter: staatlicher Konflikt, Regierungskonflikt, bewaffneter Konflikt mit Staat. Sources: https://en.wikipedia.org/wiki/War | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: government vs opponent, armed conflict with state party. …

[Knowledge:58 hazards:Hazard_Extrasystemic_Conflict_UCDP_PRIO Extrasystemic Conflict (UCDP/PRIO)] HAZARD_ID: hazards:Hazard_Extrasystemic_Conflict_UCDP_PRIO
LABEL: Extrasystemic Conflict (UCDP/PRIO)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: colonial conflict, anti-colonial war, external territory; extrasystemischer Konflikt, Kolonialkonflikt, antikolonialer Krieg
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: colonial conflict, anti-colonial war, external territory. Schlüsselwörter: extrasystemischer Konflikt, Kolonialkonflikt, antikolonialer Krieg. Sources: https://en.wikipedia.org/wiki/Colonial_war | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: colonial conflict, anti-colonial war, external …

[Knowledge:205 hazards:Hazard_Volcanic_Activity_General Volcanic Activity (General)] HAZARD_ID: hazards:Hazard_Volcanic_Activity_General
LABEL: Volcanic Activity (General)
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: volcanic activity; Vulkanische Aktivität
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic activity. Schlüsselwörter: Vulkanische Aktivität. Sources: https://en.wikipedia.org/wiki/Volcanic_activity | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic activity. Schlüsselwörter: Vulkanische Aktivität. Sources: https://en.wikipedia.org/wiki/Volcanic_activity | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: …

[Knowledge:139 hazards:Hazard_Organized_Violence_UCDP Organized Violence (UCDP)] HAZARD_ID: hazards:Hazard_Organized_Violence_UCDP
LABEL: Organized Violence (UCDP)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: organized violence, conflict data, UCDP; organisierte Gewalt, Konfliktdaten, UCDP
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: organized violence, conflict data, UCDP. Schlüsselwörter: organisierte Gewalt, Konfliktdaten, UCDP. Sources: https://en.wikipedia.org/wiki/Uppsala_Conflict_Data_Program | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Terrorism. Keywords: organized violence, conflict data, UCDP. Schlüsselwörter: organisierte Gewalt, Konfliktdaten, UCDP. Sources: https://en.wikipedia.org/wiki/Uppsala_Conflict_Data_Program | UCDP Georeferenced Event …

[Knowledge:89 hazards:Hazard_Induced_Seismicity Induced Seismicity] HAZARD_ID: hazards:Hazard_Induced_Seismicity
LABEL: Induced Seismicity
GROUP: Geophysical
SUBTYPE: Earthquake
ALIASES: human-induced earthquakes; wastewater injection; geothermal stimulation; reservoir impoundment; mining/extraction; fault reactivation; pore-pressure diffusion; delayed onset/distant events; traffic-light regulation; induzierte Seismizität; anthropogen ausgelöste Erdbeben; Abwasserverpressung; Geothermie-Stimulation; Stauseeaufstau; Bergbau/Förderung; Reaktivierung von Störungen; Porendruckausbreitung; zeitverzögerte/entfernte Ereignisse; Ampelsystem (Traffic-Light) (Begriff gebräuchlich)
BM25_TEXT_EN: Caused by hazard(s): Earthquake. Keywords: human-induced earthquakes; wastewater injection; geothermal stimulation; reservoir impoundment; mining/extraction; fault reactivation; pore-pressure diffusion; delayed onset/distant events; traffic-light regulation. Schlüsselwörter: induzierte Seismizität; anthropogen ausgelöste Erdbeben; Abwasserverpressung; Geothermie-Stimulation; Stauseeaufstau; Bergbau/Förderung; Reaktivierung von Störungen; Porendruckausbreitung; zeitverzögerte/entfernte Ereignisse; Ampelsystem (Traffic-Light) (Begriff gebräuchlich). Sources: USGS data …

[Knowledge:212 hazards:Hazard_Water_Supply_Contamination_Failure Water Supply Contamination / Failure] HAZARD_ID: hazards:Hazard_Water_Supply_Contamination_Failure
LABEL: Water Supply Contamination / Failure
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: water contamination; drinking water failure; water supply disruption; Wasserverschmutzung; Trinkwasserverunreinigung; Ausfall der Wasserversorgung
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: water contamination; drinking water failure; water supply disruption. Schlüsselwörter: Wasserverschmutzung; Trinkwasserverunreinigung; Ausfall der Wasserversorgung. Sources: https://en.wikipedia.org/wiki/Water_supply | https://echo.epa.gov/tools/data-downloads/sdwa-download-summary. Sample data: pwsid,system_name,state,violation_id,contaminant,violation_type,begin_date,end_date,health_based,affected_population
CA1234567,Example Water System,CA,VIOL-000123,Nitrate,MCL exceedance,2022-06-01,2022-09-30,Yes,35000
TX7654321,Example Utility,TX,VIOL-000987,E. coli,Acute RTCR,2023-08-14,2023-08-20,Yes,12000

Source description: Regulatory compliance/violation records for public water systems under the Safe Drinking Water Act (SDWIS), including contaminant, violation type, dates, and population served—useful for …

[Knowledge:75 hazards:Hazard_Glacial_Lake_Outburst_Flood Glacial Lake Outburst Flood] HAZARD_ID: hazards:Hazard_Glacial_Lake_Outburst_Flood
LABEL: Glacial Lake Outburst Flood
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: GLOF; glacial lake outburst flood; jökulhlaup; Gletscherseeausbruchflut; Jökulhlaup
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: GLOF; glacial lake outburst flood; jökulhlaup. Schlüsselwörter: Gletscherseeausbruchflut; GLOF; Jökulhlaup. Sources: Wikipedia | https://en.wikipedia.org/wiki/Glacial_lake_outburst_flood | Glacier Lake Outburst Flood Database (GLOFDB, Zenodo) | https://zenodo.org/records/7330345 | Earth System Science Data (GLOF inventory paper) | https://essd.copernicus.org/articles/15/2983/2023/. Sample data: glof_id,country,region,event_year,event_date,lake_name,dam_type,trigger,peak_discharge_m3s,impacts_summary
GLOF-000123,Nepal,Himalaya,2016,2016-06-23,Dig Tsho,Ice moraine,Ice avalanche,1600,"Bridge washed out; downstream sedimentation"
GLOF-000987,Peru,Cordillera Blanca,2010,2010-04-11,Lake 513,Moraine,Rock/ice fall,1200,"Flood wave damaged infrastructure"

Source description: Event-level GLOF inventory with standardized attributes (location, timing, dam type, triggers, and impacts) …

[Knowledge:202 hazards:Hazard_Violent_Political_Protest_UCDP Violent Political Protest (UCDP)] HAZARD_ID: hazards:Hazard_Violent_Political_Protest_UCDP
LABEL: Violent Political Protest (UCDP)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: violent riots, political unrest, clashes; gewaltsamer politischer Protest, Unruhen, Zusammenstöße
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: violent riots, political unrest, clashes. Schlüsselwörter: gewaltsamer politischer Protest, Unruhen, Zusammenstöße. Sources: https://en.wikipedia.org/wiki/Political_violence | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Terrorism. Keywords: violent riots, political unrest, clashes. Schlüsselwörter: gewaltsamer politischer Protest, Unruhen, Zusammenstöße. Sources: …

[Knowledge:170 hazards:Hazard_Solar_Flare Solar Flare] HAZARD_ID: hazards:Hazard_Solar_Flare
LABEL: Solar Flare
GROUP: Extraterrestrial
SUBTYPE: Space Weather
ALIASES: solar flare; Solar Flare
BM25_TEXT_EN: Caused by hazard(s): Space weather solar storm. Keywords: solar flare. Schlüsselwörter: Solar Flare. Sources: https://en.wikipedia.org/wiki/Solar_flare | NOAA SWPC GOES X-ray Flux (solar flare proxy) | https://www.swpc.noaa.gov/products/goes-x-ray-flux. Sample data: time_utc,xray_0p1_0p8nm_W_m2,flare_class
2024-05-10T00:00Z,2.1e-05,M2.1
2024-05-10T00:01Z,2.4e-05,M2.4
2024-05-10T00:02Z,3.6e-05,M3.6

Source description: GOES satellite X-ray sensor flux time series used to detect and classify solar flares (A/B/C/M/X) from 0.1–0.8 nm channel measurements..
VERBALIZED_EN: Caused by hazard(s): Space weather solar storm. Keywords: solar flare. Schlüsselwörter: Solar Flare. Sources: https://en.wikipedia.org/wiki/Solar_flare | NOAA SWPC GOES X-ray Flux (solar flare proxy) | https://www.swpc.noaa.gov/products/goes-x-ray-flux. Sample data: time_utc,xray_0p1_0p8nm_W_m2,flare_class
2024-05-10T00:00Z,2.1e-05,M2.1
2024-05-10T00:01Z,2.4e-05,M2.4
2024-05-10T00:02Z,3.6e-05,M3.6

Source description: GOES satellite X-ray sensor flux time series used …

[Knowledge:177 hazards:Hazard_State_Based_Conflict_UCDP_PRIO_ACD State-based Conflict (UCDP/PRIO ACD)] HAZARD_ID: hazards:Hazard_State_Based_Conflict_UCDP_PRIO_ACD
LABEL: State-based Conflict (UCDP/PRIO ACD)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: state-based conflict, civil war, interstate war, UCDP/PRIO; staatlicher Konflikt, Bürgerkrieg, zwischenstaatlicher Krieg, UCDP/PRIO
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: state-based conflict, civil war, interstate war, UCDP/PRIO. Schlüsselwörter: staatlicher Konflikt, Bürgerkrieg, zwischenstaatlicher Krieg, UCDP/PRIO. Sources: https://en.wikipedia.org/wiki/Uppsala_Conflict_Data_Program | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: state-based …

[Knowledge:213 hazards:Hazard_Waterborne_Diseases Waterborne Diseases] HAZARD_ID: hazards:Hazard_Waterborne_Diseases
LABEL: Waterborne Diseases
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: contaminated drinking water; fecal-oral transmission; inadequate sanitation; outbreaks after floods; cholera/typhoid/hepatitis A/E; diarrhoeal disease; WASH interventions; water treatment/disinfection; surveillance; wasserübertragene Krankheiten (auch: wasserbedingte); kontaminiertes Trinkwasser; fäkal-orale Übertragung; unzureichende Sanitärversorgung; Ausbrüche nach Überschwemmungen; Cholera/Typhus/Hepatitis A/E; Durchfallerkrankungen; WASH-Maßnahmen (Wasser/Sanitär/Hygiene); Wasseraufbereitung/Desinfektion; Überwachung/Surveillance (Begriffe teils englisch)
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: contaminated drinking water; fecal-oral transmission; inadequate sanitation; outbreaks after floods; cholera/typhoid/hepatitis A/E; diarrhoeal disease; WASH interventions; water treatment/disinfection; surveillance. Schlüsselwörter: wasserübertragene Krankheiten (auch: wasserbedingte); kontaminiertes Trinkwasser; fäkal-orale Übertragung; unzureichende Sanitärversorgung; Ausbrüche nach Überschwemmungen; Cholera/Typhus/Hepatitis A/E; …

[Knowledge:70 hazards:Hazard_Freezing_Rain Freezing rain] HAZARD_ID: hazards:Hazard_Freezing_Rain
LABEL: Freezing rain
GROUP: Meteorological
SUBTYPE: Extreme Temperature
ALIASES: freezing rain, glaze ice, icing, slippery conditions; gefrierender Regen, Glatteis, Eisregen, Glätte, Vereisung
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: freezing rain, glaze ice, icing, slippery conditions. Schlüsselwörter: gefrierender Regen, Glatteis, Eisregen, Glätte, Vereisung. Sources: Wikipedia | https://en.wikipedia.org/wiki/Freezing_rain | NOAA NCEI Storm Events Database | https://www.ncei.noaa.gov/stormevents/ | NOAA ASOS 1-minute observations | https://catalog.data.gov/dataset/1-minute-page-2-surface-weather-observations-from-the-automated-surface-observing-systems-asos-network. Sample data: ts_local,temp_C,dewpoint_C,precip_type,precip_mm,wind_kt,pressure_hPa
2024-02-22 18:01, -0.3, -0.6, FZRA,0.0,12,1016.8
2024-02-22 18:02, -0.2, -0.6, FZRA,0.0,13,1016.7
2024-02-22 18:03, -0.1, -0.5, FZRA,0.1,14,1016.6
2024-02-22 18:04,  0.0, -0.5, -RA,0.2,15,1016.5

Source description: Minute-resolution surface observations including precipitation type codes (e.g., FZRA) and near-freezing temperatures; useful for detecting onset/transition of freezing …

[Knowledge:206 hazards:Hazard_Volcanic_Explosivity_Index Volcanic Explosivity Index] HAZARD_ID: hazards:Hazard_Volcanic_Explosivity_Index
LABEL: Volcanic Explosivity Index
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: volcanic explosivity index; Volcanic explosivity index
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic explosivity index. Schlüsselwörter: Volcanic explosivity index. Sources: https://en.wikipedia.org/wiki/Volcanic_explosivity_index | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic explosivity index. Schlüsselwörter: Volcanic explosivity index. Sources: https://en.wikipedia.org/wiki/Volcanic_explosivity_index | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: …

[Knowledge:204 hazards:Hazard_Volcanic_Activity Volcanic Activity] HAZARD_ID: hazards:Hazard_Volcanic_Activity
LABEL: Volcanic Activity
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: volcanic eruption; lava; ashfall; pyroclastic flow; lahar; Vulkanausbruch; Lava; Aschenfall; pyroklastischer Strom; Lahar
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic eruption; lava; ashfall; pyroclastic flow; lahar. Schlüsselwörter: Vulkanausbruch; Lava; Aschenfall; pyroklastischer Strom; Lahar. Sources: https://en.wikipedia.org/wiki/Volcanic_eruption | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic eruption; lava; ashfall; pyroclastic flow; lahar. Schlüsselwörter: Vulkanausbruch; Lava; Aschenfall; pyroklastischer …

[Knowledge:17 hazards:Hazard_Belligerent_Occupation Belligerent Occupation] HAZARD_ID: hazards:Hazard_Belligerent_Occupation
LABEL: Belligerent Occupation
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: occupation, military occupation, occupied territory; Kriegsbesetzung, militärische Besetzung, besetztes Gebiet
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: occupation, military occupation, occupied territory. Schlüsselwörter: Kriegsbesetzung, militärische Besetzung, besetztes Gebiet. Sources: https://en.wikipedia.org/wiki/Military_occupation | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Terrorism. Keywords: occupation, military occupation, occupied territory. Schlüsselwörter: Kriegsbesetzung, militärische Besetzung, besetztes Gebiet. Sources: …

[Knowledge:171 hazards:Hazard_Space_Debris Space Debris] HAZARD_ID: hazards:Hazard_Space_Debris
LABEL: Space Debris
GROUP: Extraterrestrial
SUBTYPE: Space Hazard
ALIASES: orbital debris; defunct satellites; fragmentation; collision risk; conjunction alerts; Kessler syndrome cascade; tracking/catalogs; reentry risk; satellite service disruption; mitigation guidelines; Orbitalschrott (Weltraummüll); defekte Satelliten; Fragmentierung; Kollisionsrisiko; Annäherungswarnungen (Conjunction Alerts); Kessler-Syndrom (Kaskade); Verfolgung/Katalogisierung (Tracking); Wiedereintrittsrisiko; Störung von Satellitendiensten; Mitigationsrichtlinien
BM25_TEXT_EN: Caused by hazard(s): Earthquake|hazards:hazard flood|hazards:hazard impact event. Keywords: orbital debris; defunct satellites; fragmentation; collision risk; conjunction alerts; Kessler syndrome cascade; tracking/catalogs; reentry risk; satellite service disruption; mitigation guidelines. Schlüsselwörter: Orbitalschrott (Weltraummüll); defekte Satelliten; Fragmentierung; Kollisionsrisiko; Annäherungswarnungen (Conjunction Alerts); Kessler-Syndrom (Kaskade); Verfolgung/Katalogisierung (Tracking); Wiedereintrittsrisiko; Störung von Satellitendiensten; Mitigationsrichtlinien. Sources: …

[Knowledge:186 hazards:Hazard_Sun_Glare Sun glare] HAZARD_ID: hazards:Hazard_Sun_Glare
LABEL: Sun glare
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: sun glare; glare; low sun angle; dazzling sunlight; windshield glare; Sonnenblendung; Blendung; tiefer Sonnenstand; grelles Sonnenlicht; Windschutzscheibenblendung
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: sun glare; glare; low sun angle; dazzling sunlight; windshield glare. Schlüsselwörter: Sonnenblendung; Blendung; tiefer Sonnenstand; grelles Sonnenlicht; Windschutzscheibenblendung. Sources: https://en.wikipedia.org/wiki/Glare_(vision) | NHTSA Fatality Analysis Reporting System (FARS) | https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars. Sample data: state,st_case,year,month,day,hour,latitude,longitude,light_cond,weather,persons,killed
6,24680,2023,10,3,7,34.052,-118.244,Sunrise,Clear,2,1
48,13579,2023,11,20,16,29.760,-95.369,Sunset,Clear,1,1

Source description: FARS includes crash-level attributes such as lighting conditions (e.g., sunrise/sunset) that can be used as a proxy for sun-glare related crashes when combined with narratives or contributing factors.
Source: NHTSA Fatality Analysis Reporting System (FARS) | …

[Knowledge:105 hazards:Hazard_Landslide Landslide] HAZARD_ID: hazards:Hazard_Landslide
LABEL: Landslide
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: landslide; slope failure; rockfall; debris flow; Erdrutsch; Hangrutschung; Steinschlag; Murgang
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: landslide; slope failure; rockfall; debris flow. Schlüsselwörter: Erdrutsch; Hangrutschung; Steinschlag; Murgang. Sources: https://en.wikipedia.org/wiki/Landslide | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,location_description,landslide_type,trigger,fatality_count,injury_count
GLC000123,2020-08-10,India,"Himachal Pradesh",Landslide,Downpour,14,6
GLC000124,2021-11-03,Brazil,"Rio de Janeiro",Landslide,Rain,9,0

Source description: Media- and report-derived global landslide incident rows (date, location, type, trigger, casualties). Suitable for landslide / mass-movement hazard sampling.
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: landslide; slope failure; rockfall; debris flow. Schlüsselwörter: Erdrutsch; …

[Knowledge:52 hazards:Hazard_Earthquake Earthquake] HAZARD_ID: hazards:Hazard_Earthquake
LABEL: Earthquake
GROUP: Geophysical
SUBTYPE: Earthquake
ALIASES: earthquake; seismic event; ground shaking; fault rupture; Erdbeben; seismisches Ereignis; Bodenerschütterung; Bruch einer Verwerfung
BM25_TEXT_EN: Caused by hazard(s): Earthquake. Keywords: earthquake; seismic event; ground shaking; fault rupture. Schlüsselwörter: Erdbeben; seismisches Ereignis; Bodenerschütterung; Bruch einer Verwerfung. Sources: USGS Earthquake Catalog API | https://earthquake.usgs.gov/fdsnws/event/1/query ; USGS Earthquakes CSV feed format | https://earthquake.usgs.gov/earthquakes/feed/v1.0/csv.php. Sample data: time,latitude,longitude,depth_km,mag,magType,place,event_id
2026-02-18T22:14:12.340Z,37.766,-122.534,8.7,2.6,ml,"10 km WSW of San Francisco, CA",nc74123456
2026-02-18T23:01:44.120Z,34.052,-118.243,12.1,3.1,ml,"Los Angeles region, CA",ci41123456

Source description: Row-level earthquake event observations from the USGS Earthquake Catalog (exportable as CSV or GeoJSON). Includes time, hypocenter (lat/lon/depth), magnitude, and place metadata.
Source: USGS Earthquake Catalog API | …

[Knowledge:184 hazards:Hazard_Subsidence_Sinkhole Subsidence / Sinkhole] HAZARD_ID: hazards:Hazard_Subsidence_Sinkhole
LABEL: Subsidence / Sinkhole
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: ground subsidence; sinkhole; karst collapse; Bodensenkung; Sinkloch; Karsteinbruch
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: ground subsidence; sinkhole; karst collapse. Schlüsselwörter: Bodensenkung; Sinkloch; Karsteinbruch. Sources: https://en.wikipedia.org/wiki/Sinkhole | USGS sinkhole susceptibility dataset | https://www.usgs.gov/data/geospatial-files-and-tabular-exposure-estimates-sinkhole-susceptibility-counties-conterminous. Sample data: county_fips,county_name,state,sinkhole_susceptibility_class,mean_probability,pct_area_high
12011,Broward,FL,Moderate,0.26,4.1
12021,Collier,FL,High,0.51,18.7
21067,Fayette,KY,High,0.63,22.4

Source description: County-level sinkhole susceptibility/exposure estimates (tabular output) supporting USGS sinkhole susceptibility mapping. Includes susceptibility class/probability metrics that can be used as a sinkhole/subsidence hazard sample.
Source: USGS sinkhole susceptibility dataset | …

[Knowledge:67 hazards:Hazard_Foodborne_Outbreak Foodborne Outbreak] HAZARD_ID: hazards:Hazard_Foodborne_Outbreak
LABEL: Foodborne Outbreak
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: foodborne illness; food poisoning; outbreak; Lebensmittelbedingte Erkrankung; Lebensmittelvergiftung; Ausbruch
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: foodborne illness; food poisoning; outbreak. Schlüsselwörter: Lebensmittelbedingte Erkrankung; Lebensmittelvergiftung; Ausbruch. Sources: https://en.wikipedia.org/wiki/Foodborne_illness | CDC NORS dataset | https://data.cdc.gov/Foodborne-Waterborne-and-Related-Diseases/NORS/5xkq-dg7x | CDC NORS data overview | https://www.cdc.gov/nors/data/index.html. Sample data: report_id,year,primary_mode,etiology,setting,illnesses,hospitalizations,deaths,implicated_food
NORS-2019-000123,2019,Foodborne,Salmonella,Restaurant,27,4,0,"Chicken"
NORS-2020-000987,2020,Foodborne,Norovirus,Catered event,64,2,0,"Mixed foods"
NORS-2021-000456,2021,Foodborne,Listeria,Home,6,5,1,"Soft cheese"

Source description: Outbreak-level records from CDC’s National Outbreak Reporting System (NORS): each row summarizes one outbreak with etiology, setting, cases, and outcomes.
Source: CDC NORS dataset | …

[Knowledge:191 hazards:Hazard_Tanganyika_Laughter_Epidemic Tanganyika Laughter Epidemic] HAZARD_ID: hazards:Hazard_Tanganyika_Laughter_Epidemic
LABEL: Tanganyika Laughter Epidemic
GROUP: Black Swan
SUBTYPE: Psychogenic Incident
ALIASES: mass psychogenic illness; laughter epidemic; psychosomatic outbreak; Lach-Epidemie; Massenpsychogene Erkrankung; psychosomatischer Ausbruch
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: mass psychogenic illness; laughter epidemic; psychosomatic outbreak. Schlüsselwörter: Lach-Epidemie; Massenpsychogene Erkrankung; psychosomatischer Ausbruch. Sources: https://en.wikipedia.org/wiki/Tanganyika_laughter_epidemic | Wikipedia mass psychogenic illness | https://en.wikipedia.org/wiki/Mass_psychogenic_illness | Wikidata Query Service | https://query.wikidata.org/. Sample data: event_name,start_date,end_date,country,schools_affected,estimated_affected
"Tanganyika laughter epidemic",1962-01-30,1962-06-01,Tanzania,14,1000

Source description: Single-event structured row representing the 1962 Tanganyika laughter epidemic (school closures/affected counts) as a mass psychogenic illness case.
Source: Wikipedia mass psychogenic illness | https://en.wikipedia.org/wiki/Mass_psychogenic_illness | Wikidata Query Service | …

[Knowledge:35 hazards:Hazard_Collision Collision] HAZARD_ID: hazards:Hazard_Collision
LABEL: Collision
GROUP: Extraterrestrial
SUBTYPE: Space Hazard
ALIASES: collision; Kollision
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: collision. Schlüsselwörter: Kollision. Sources: https://en.wikipedia.org/wiki/Collision | CelesTrak NORAD GP Element Sets (TLE) | https://www.celestrak.org/NORAD/elements/. Sample data: ISS (ZARYA)
1 25544U 98067A   26050.50000000  .00016717  00000-0  10270-3 0  9991
2 25544  51.6447  45.1234 0005123  82.3456  12.3456 15.50123456789012

Source description: Two-Line Element (TLE) sets provide orbital elements for tracked objects (satellites, rocket bodies, debris) derived from SGP4/SDP4 general perturbations..
VERBALIZED_EN: Caused by hazard(s): Impact event. Keywords: collision. Schlüsselwörter: Kollision. Sources: https://en.wikipedia.org/wiki/Collision | CelesTrak NORAD GP Element Sets (TLE) | https://www.celestrak.org/NORAD/elements/. Sample data: ISS (ZARYA)
1 25544U 98067A   26050.50000000  .00016717  00000-0  10270-3 0  9991
2 25544  51.6447  45.1234 0005123  82.3456  12.3456 15.50123456789012

Source description: Two-Line Element (TLE) sets provide orbital elements for tracked objects …

[Knowledge:100 hazards:Hazard_Lahar Lahar] HAZARD_ID: hazards:Hazard_Lahar
LABEL: Lahar
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: lahar; Lahar
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: lahar. Schlüsselwörter: Lahar. Sources: https://en.wikipedia.org/wiki/Lahar | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: lahar. Schlüsselwörter: Lahar. Sources: https://en.wikipedia.org/wiki/Lahar | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source …

[Knowledge:145 hazards:Hazard_Power_Grid_Failure_Blackout Power Grid Failure / Blackout] HAZARD_ID: hazards:Hazard_Power_Grid_Failure_Blackout
LABEL: Power Grid Failure / Blackout
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: power outage; blackout; grid failure; cascading failure; Stromausfall; Blackout; Stromnetzausfall; Kaskadenausfall
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: power outage; blackout; grid failure; cascading failure. Schlüsselwörter: Stromausfall; Blackout; Stromnetzausfall; Kaskadenausfall. Sources: https://en.wikipedia.org/wiki/Power_outage | https://catalog.data.gov/dataset/eagle-i-outage-data. Sample data: timestamp_utc,fips,customers_out,customers_total,outage_pct
2024-02-16T18:15Z,12086,35214,873402,4.03
2024-02-16T18:30Z,12086,40110,873402,4.59

Source description: High-frequency (e.g., 15-minute) county-level electric outage snapshots with customers-out counts and totals; useful for modeling blackout onset, duration, and recovery.
Source: EAGLE-I Power Outage Data (ORNL) | https://catalog.data.gov/dataset/eagle-i-outage-data.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: power outage; blackout; grid failure; cascading failure. Schlüsselwörter: Stromausfall; Blackout; Stromnetzausfall; …

[Knowledge:101 hazards:Hazard_Lake_Nyos_Disaster Lake Nyos Disaster] HAZARD_ID: hazards:Hazard_Lake_Nyos_Disaster
LABEL: Lake Nyos Disaster
GROUP: Black Swan
SUBTYPE: Volcanic Activity
ALIASES: limnic eruption; carbon dioxide release; asphyxiation; Limnische Eruption; Kohlendioxid-Freisetzung; Erstickung
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: limnic eruption; carbon dioxide release; asphyxiation. Schlüsselwörter: Limnische Eruption; Kohlendioxid-Freisetzung; Erstickung. Sources: https://en.wikipedia.org/wiki/Lake_Nyos_disaster | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: limnic eruption; carbon dioxide release; asphyxiation. Schlüsselwörter: Limnische Eruption; Kohlendioxid-Freisetzung; Erstickung. Sources: …

[Knowledge:109 hazards:Hazard_Lava_Flow Lava Flow] HAZARD_ID: hazards:Hazard_Lava_Flow
LABEL: Lava Flow
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: lava flow; Lavastrom
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: lava flow. Schlüsselwörter: Lavastrom. Sources: https://en.wikipedia.org/wiki/Lava_flow | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: lava flow. Schlüsselwörter: Lavastrom. Sources: https://en.wikipedia.org/wiki/Lava_flow | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: …

[Knowledge:8 hazards:Hazard_Ash_Fall Ash Fall] HAZARD_ID: hazards:Hazard_Ash_Fall
LABEL: Ash Fall
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: ash fall; Ascheregen
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: ash fall. Schlüsselwörter: Ascheregen. Sources: https://en.wikipedia.org/wiki/Ash_fall | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: ash fall. Schlüsselwörter: Ascheregen. Sources: https://en.wikipedia.org/wiki/Ash_fall | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: …

[Knowledge:146 hazards:Hazard_Pyroclastic_Flow Pyroclastic Flow] HAZARD_ID: hazards:Hazard_Pyroclastic_Flow
LABEL: Pyroclastic Flow
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: pyroclastic flow; Pyroklastischer Strom
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: pyroclastic flow. Schlüsselwörter: Pyroklastischer Strom. Sources: https://en.wikipedia.org/wiki/Pyroclastic_flow | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: pyroclastic flow. Schlüsselwörter: Pyroklastischer Strom. Sources: https://en.wikipedia.org/wiki/Pyroclastic_flow | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: …

[Knowledge:102 hazards:Hazard_Laki_Eruption Laki Eruption] HAZARD_ID: hazards:Hazard_Laki_Eruption
LABEL: Laki Eruption
GROUP: Black Swan
SUBTYPE: Volcanic Activity
ALIASES: fissure eruption; volcanic haze; sulfur dioxide; lava flood; Spalteneruption; Vulkanischer Dunst; Schwefeldioxid; Lavaflut
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: fissure eruption; volcanic haze; sulfur dioxide; lava flood. Schlüsselwörter: Spalteneruption; Vulkanischer Dunst; Schwefeldioxid; Lavaflut. Sources: https://en.wikipedia.org/wiki/Laki | Smithsonian GVP Volcanoes of the World database | https://volcano.si.edu/. Sample data: volcano_number,volcano_name,eruption_number,start_date,end_date,vei,latitude,longitude
357020,Etna,12345,2021-02-16,2021-03-01,3,37.734,15.004
263250,Nyiragongo,67890,2021-05-22,2021-05-23,2,-1.52,29.25

Source description: Global Volcanism Program database of volcanoes and eruptions (Holocene and beyond), including VEI, dates, locations, and eruption characteristics; downloadable tables available via GVP..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: fissure eruption; volcanic haze; sulfur dioxide; lava flood. Schlüsselwörter: Spalteneruption; Vulkanischer Dunst; Schwefeldioxid; Lavaflut. …

[Knowledge:39 hazards:Hazard_Cyber_Supply_Chain_Attack Cyber Supply Chain Attack] HAZARD_ID: hazards:Hazard_Cyber_Supply_Chain_Attack
LABEL: Cyber Supply Chain Attack
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: compromised supplier; malicious update; dependency poisoning; code-signing abuse; third-party breach; downstream compromise; software bill of materials (SBOM); secure SDLC; supplier risk management; incident response; kompromittierter Lieferant; bösartiges Update; Dependency Poisoning (Begriff gebräuchlich); Missbrauch von Code-Signierung; Drittanbieter-Kompromittierung; Downstream-Kompromittierung; Software-Stückliste (SBOM) (auch: Software Bill of Materials); sicherer SDLC; Lieferantenrisikomanagement; Incident Response
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: compromised supplier; malicious update; dependency poisoning; code-signing abuse; third-party breach; downstream compromise; software bill of materials (SBOM); secure SDLC; supplier risk management; incident response. Schlüsselwörter: kompromittierter Lieferant; bösartiges Update; Dependency Poisoning (Begriff gebräuchlich); Missbrauch von Code-Signierung; Drittanbieter-Kompromittierung; Downstream-Kompromittierung; Software-Stückliste (SBOM) (auch: Software Bill of …

[Knowledge:16 hazards:Hazard_Ball_Lightning Ball Lightning] HAZARD_ID: hazards:Hazard_Ball_Lightning
LABEL: Ball Lightning
GROUP: Meteorological
SUBTYPE: Lightning
ALIASES: ball lightning; globular lightning; plasma ball; luminous sphere; atmospheric electricity; thunderstorm; electrical phenomenon; Kugelblitz; globusförmiger Blitz; Plasmakugel; leuchtende Kugel; atmosphärische Elektrizität; Gewitter; elektrisches Phänomen
BM25_TEXT_EN: Caused by hazard(s): Lightning. Keywords: ball lightning; globular lightning; plasma ball; luminous sphere; atmospheric electricity; thunderstorm; electrical phenomenon. Schlüsselwörter: Kugelblitz; globusförmiger Blitz; Plasmakugel; leuchtende Kugel; atmosphärische Elektrizität; Gewitter; elektrisches Phänomen. Sources: https://en.wikipedia.org/wiki/Ball_lightning | https://kestrel.nmt.edu/~rsonnenf/BL/. Sample data: report_id,report_year,location,observed_duration_s,color,diameter_cm,context,damage_reported
BL-0001,2018,UK,5,Orange,20,Indoors,No
BL-0002,2009,DE,12,Blue-white,15,Near window,Yes

Source description: Curated compilation of eyewitness ball-lightning reports with structured attributes (duration, color, size, context, damages); useful for rare-atmospheric-electrical phenomenology.
Source: Ball …

[Knowledge:77 hazards:Hazard_Global_Memory_Supply_Shortage Global Memory Supply Shortage] HAZARD_ID: hazards:Hazard_Global_Memory_Supply_Shortage
LABEL: Global Memory Supply Shortage
GROUP: Digital
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: RAMmageddon, RAMpocalypse; Chipkrise, Halbleiterkrise
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: RAMmageddon, RAMpocalypse. Schlüsselwörter: Chipkrise, Halbleiterkrise. Sources: https://en.wikipedia.org/wiki/2021–2023_global_supply_chain_crisis | https://oec.world/en/profile/hs/memories-854232. Sample data: year,exporter,trade_value_usd
2023,China,12500000000
2023,Chinese Taipei,9800000000
2023,South Korea,8700000000

Source description: Trade-value time series by exporter for memory integrated circuits (HS 854232), derived from UN Comtrade via the Observatory of Economic Complexity; can proxy global memory-supply concentration and shock exposure.
Source: OEC Trade Data (HS 854232 Memories) | https://oec.world/en/profile/hs/memories-854232.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: RAMmageddon, RAMpocalypse. Schlüsselwörter: Chipkrise, Halbleiterkrise. Sources: https://en.wikipedia.org/wiki/2021–2023_global_supply_chain_crisis | https://oec.world/en/profile/hs/memories-854232. Sample data: …

[Knowledge:198 hazards:Hazard_UAP_Focused_Defense_Contingency UAP-focused Defense Contingency] HAZARD_ID: hazards:Hazard_UAP_Focused_Defense_Contingency
LABEL: UAP-focused Defense Contingency
GROUP: Black Swan
SUBTYPE: Transport Incident
ALIASES: unidentified aerial phenomena; airspace safety; threat assessment; military reporting; Unidentifizierte anomale Phänomene; Luftraumsicherheit; Gefahrenbewertung; militärische Meldung
BM25_TEXT_EN: Caused by hazard(s): Critical infrastructure failure. Keywords: unidentified aerial phenomena; airspace safety; threat assessment; military reporting. Schlüsselwörter: Unidentifizierte anomale Phänomene; Luftraumsicherheit; Gefahrenbewertung; militärische Meldung. Sources: https://en.wikipedia.org/wiki/Unidentified_aerial_phenomena | DoD AARO UAP Reporting Trends (CSV download) | https://www.aaro.mil/UAP-Cases/UAP-Reporting-Trends/. Sample data: category,count,percentage
Above 60K,20,1.7
60K,40,3.3
55K,14,1.2

Source description: AARO publishes aggregate UAP reporting trend tables (e.g., altitudes, shapes) with downloadable CSV for analysis..
VERBALIZED_EN: Caused by hazard(s): Critical infrastructure failure. Keywords: unidentified aerial phenomena; airspace safety; threat assessment; military reporting. Schlüsselwörter: Unidentifizierte …

[Knowledge:197 hazards:Hazard_Tunguska_Event Tunguska Event] HAZARD_ID: hazards:Hazard_Tunguska_Event
LABEL: Tunguska Event
GROUP: Black Swan
SUBTYPE: Space Hazard
ALIASES: asteroid airburst; meteor explosion; impact event; Asteroiden-Luftexplosion; Meteorexplosion; Impaktereignis
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: asteroid airburst; meteor explosion; impact event. Schlüsselwörter: Asteroiden-Luftexplosion; Meteorexplosion; Impaktereignis. Sources: https://en.wikipedia.org/wiki/Tunguska_event | Wikidata Query Service | https://query.wikidata.org/ | NASA CNEOS Fireball Data API (for modern analogs) | https://ssd-api.jpl.nasa.gov/doc/fireball.html | NASA JPL CNEOS Fireball and Bolide Reports (CSV/Excel) | https://cneos.jpl.nasa.gov/fireballs/. Sample data: datetime_utc,lat_deg,lon_deg,alt_km,vel_km_s,vx_km_s,vy_km_s,vz_km_s,impact_energy_kt
2013-02-15 03:20:26,54.4,61.1,23.3,18.6,-12.2,6.5,-12.2,440.0
2020-12-22 23:23:33,31.9,96.2,35.5,13.6,-10.1,2.0,-8.9,9.8

Source description: Chronological table of fireball/bolide events detected by U.S. Government sensors with location, altitude, velocity components, and estimated impact energy; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Impact event. …

[Knowledge:129 hazards:Hazard_Mudslide Mudslide] HAZARD_ID: hazards:Hazard_Mudslide
LABEL: Mudslide
GROUP: Hydrological
SUBTYPE: Mass Movement
ALIASES: mudslide; Schlammlawine
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: mudslide. Schlüsselwörter: Schlammlawine. Sources: https://en.wikipedia.org/wiki/Mudslide | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,landslide_type,trigger,fatality_count,injury_count
GLC000710,2020-10-05,Philippines,Mudslide,Tropical Cyclone,6,12
GLC000711,2017-08-14,Sierra Leone,Mudslide,Rain,1141,0

Source description: Mudslide event rows (type=Mudslide) with triggers and casualties; suitable raw samples for mudslide hazard modeling.
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: mudslide. Schlüsselwörter: Schlammlawine. Sources: https://en.wikipedia.org/wiki/Mudslide | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: …

[Knowledge:29 hazards:Hazard_Climate_Change Climate Change] HAZARD_ID: hazards:Hazard_Climate_Change
LABEL: Climate Change
GROUP: Climatological
SUBTYPE: Environmental Degradation
ALIASES: anthropogenic warming; Klimawandel
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: anthropogenic warming. Schlüsselwörter: Klimawandel. Sources: NASA GISTEMP v4 | https://data.giss.nasa.gov/gistemp/ ; NOAA GML Mauna Loa CO2 daily means | https://gml.noaa.gov/ccgg/trends/data.html. Sample data: # Example 1: Global temperature anomaly (monthly)
year,month,temp_anomaly_C
2025,12,1.26
2026,01,1.18

# Example 2: Atmospheric CO2 (daily mean, Mauna Loa)
date,co2_ppm
2026-02-16,429.29
2026-02-17,430.47

Source description: Two core climate-change observables: (1) global surface temperature anomaly time series (NASA GISTEMP) and (2) atmospheric CO2 concentration time series (NOAA GML Mauna Loa). These are widely used as raw inputs for trend and attribution analyses.
Source: NASA GISTEMP | https://data.giss.nasa.gov/gistemp/ ; NOAA GML | https://gml.noaa.gov/ccgg/trends/data.html.
VERBALIZED_EN: Caused by hazard(s): Climate change. Keywords: anthropogenic warming. Schlüsselwörter: Klimawandel. Sources: NASA GISTEMP v4 | …

[Knowledge:210 hazards:Hazard_Wastewater_System_Failure Wastewater System Failure] HAZARD_ID: hazards:Hazard_Wastewater_System_Failure
LABEL: Wastewater System Failure
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: wastewater failure; sewage overflow; sewer system failure; Abwasserstörung; Überlauf von Abwasser; Kanalnetzstörung
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: wastewater failure; sewage overflow; sewer system failure. Schlüsselwörter: Abwasserstörung; Überlauf von Abwasser; Kanalnetzstörung. Sources: https://en.wikipedia.org/wiki/Sewerage | https://www.fema.gov/openfema-data-page/public-assistance-funded-projects-details-v1. Sample data: project_worksheet,disaster_number,state,project_title,category,project_amount_usd,facility_type,work_description
PA-1234-0001,4559,LA,Wastewater lift station repairs,B,1250000,Wastewater,"Replace pumps/electrical after flooding"
PA-5678-0002,4735,FL,WWTP generator installation,B,980000,Wastewater,"Install backup generation for treatment plant"

Source description: Project-level FEMA Public Assistance data for disaster recovery; can be filtered for wastewater facilities (lift stations/WWTPs) to represent system failures and recovery actions.
Source: OpenFEMA Public Assistance …

[Knowledge:87 hazards:Hazard_Impact Impact] HAZARD_ID: hazards:Hazard_Impact
LABEL: Impact
GROUP: Extraterrestrial
SUBTYPE: Space Hazard
ALIASES: meteor impact; asteroid impact; impact event; bolide; Meteoriteneinschlag; Asteroideneinschlag; Impaktereignis; Bolide
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: meteor impact; asteroid impact; impact event; bolide. Schlüsselwörter: Meteoriteneinschlag; Asteroideneinschlag; Impaktereignis; Bolide. Sources: https://en.wikipedia.org/wiki/Impact_event | NASA CNEOS Fireball Data API | https://ssd-api.jpl.nasa.gov/doc/fireball.html | NASA Fireball and Bolide Reports | https://data.nasa.gov/dataset/fireball-and-bolide-reports | NASA JPL CNEOS Fireball and Bolide Reports (CSV/Excel) | https://cneos.jpl.nasa.gov/fireballs/. Sample data: datetime_utc,lat_deg,lon_deg,alt_km,vel_km_s,vx_km_s,vy_km_s,vz_km_s,impact_energy_kt
2013-02-15 03:20:26,54.4,61.1,23.3,18.6,-12.2,6.5,-12.2,440.0
2020-12-22 23:23:33,31.9,96.2,35.5,13.6,-10.1,2.0,-8.9,9.8

Source description: Chronological table of fireball/bolide events detected by U.S. Government sensors with location, altitude, velocity components, and estimated impact energy; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by …

[Knowledge:33 hazards:Hazard_Coastal_Flooding Coastal Flooding] HAZARD_ID: hazards:Hazard_Coastal_Flooding
LABEL: Coastal Flooding
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: coastal flood; storm surge; coastal inundation; Küstenhochwasser; Sturmflut; Küstenüberflutung
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: coastal flood; storm surge; coastal inundation. Schlüsselwörter: Küstenhochwasser; Sturmflut; Küstenüberflutung. Sources: Wikipedia | https://en.wikipedia.org/wiki/Coastal_flooding | NOAA NCEI Storm Events Database | https://www.ncei.noaa.gov/stormevents/ | NWS Charleston Coastal Flood Event Database | https://www.weather.gov/chs/coastalflood. Sample data: gauge_id,event_start_local,event_end_local,max_water_level_ft_mllw,flood_category
CHS,2024-08-05 09:40,2024-08-05 15:10,8.41,major
CHS,2024-10-18 21:05,2024-10-19 03:20,7.66,moderate
CHS,2025-02-03 06:10,2025-02-03 09:55,7.18,minor

Source description: Coastal flooding event log derived from tide-gauge exceedance of minor/moderate/major thresholds; can be paired with storm surge and rainfall drivers.
Source: NWS Charleston Coastal Flood Event Database | https://www.weather.gov/chs/coastalflood.
VERBALIZED_EN: Caused by hazard(s): …

[Knowledge:83 hazards:Hazard_Heat_Wave Heat Wave] HAZARD_ID: hazards:Hazard_Heat_Wave
LABEL: Heat Wave
GROUP: Meteorological
SUBTYPE: Extreme Temperature
ALIASES: heat wave; Hitzewelle
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: heat wave. Schlüsselwörter: Hitzewelle. Sources: Wikipedia (Heat wave) | https://en.wikipedia.org/wiki/Heat_wave | NOAA NCEI (GHCN-Daily sample CSV) | https://www.ncei.noaa.gov/pub/data/cdo/samples/GHCND_sample_csv.csv | Copernicus CDS (ERA5 daily statistics) | https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics. Sample data: date,station_or_grid_id,tmax_C,tmin_C,heatwave_flag
2023-07-17,GHCND:USW00023174,44.0,28.3,1
2023-07-18,GHCND:USW00023174,43.2,29.1,1
2023-07-19,GHCND:USW00023174,42.7,28.9,1

Source description: Example derived heat-wave event table created from daily max/min temperature (e.g., GHCN-Daily station data or ERA5 daily stats). The heatwave_flag indicates consecutive-day exceedance of a chosen local threshold (definition varies by study/agency).
Source: Copernicus CDS (ERA5 daily statistics) | https://cds.climate.copernicus.eu/datasets/derived-era5-single-levels-daily-statistics.
VERBALIZED_EN: Caused by hazard(s): Climate change. …

[Knowledge:10 hazards:Hazard_Atmospheric_River_Extreme_Precipitation_Event Atmospheric River Extreme Precipitation Event] HAZARD_ID: hazards:Hazard_Atmospheric_River_Extreme_Precipitation_Event
LABEL: Atmospheric River Extreme Precipitation Event
GROUP: Meteorological
SUBTYPE: Extreme Precipitation
ALIASES: atmospheric river; narrow moisture corridor; integrated vapor transport (IVT); orographic precipitation enhancement; long-duration heavy rain/snow; rainfall-on-snow; river/flash flooding; debris flows/landslides; forecast via satellites/radar; atmosphärischer Fluss; schmaler Feuchte-/Wasserdampftransport; integrierter Wasserdampftransport (IVT); orographische Niederschlagsverstärkung; langanhaltender Starkregen/Schneefall; Regen-auf-Schnee (Rain-on-snow); Fluss-/Sturzfluten; Muren/Hangrutsche (Mure vs Schuttstrom); Vorhersage mittels Satellit/Radar
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: atmospheric river; narrow moisture corridor; integrated vapor transport (IVT); orographic precipitation enhancement; long-duration heavy rain/snow; rainfall-on-snow; river/flash flooding; debris flows/landslides; forecast via satellites/radar. Schlüsselwörter: atmosphärischer Fluss; schmaler Feuchte-/Wasserdampftransport; integrierter Wasserdampftransport (IVT); orographische Niederschlagsverstärkung; …

[Knowledge:189 hazards:Hazard_Supply_Chain_Issues Supply Chain Issues] HAZARD_ID: hazards:Hazard_Supply_Chain_Issues
LABEL: Supply Chain Issues
GROUP: Societal
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: supply chain issues; lieferkettenprobleme
BM25_TEXT_EN: Caused by hazard(s): Civil unrest. Keywords: supply chain issues. Schlüsselwörter: lieferkettenprobleme. Sources: https://www.xeneta.com/blog/the-biggest-global-supply-chain-risks-of-2025 | https://www.newyorkfed.org/research/policy/gscpi. Sample data: date,gscpi
2021-12-01,4.43
2022-05-01,3.28
2024-12-01,-0.45

Source description: Monthly composite index capturing global supply-chain stress (shipping, delivery times, backlogs, etc.); useful as a quantitative indicator for broad supply-chain disruption hazards.
Source: New York Fed Global Supply Chain Pressure Index (GSCPI) | https://www.newyorkfed.org/research/policy/gscpi.
VERBALIZED_EN: Caused by hazard(s): Civil unrest. Keywords: supply chain issues. Schlüsselwörter: lieferkettenprobleme. Sources: https://www.xeneta.com/blog/the-biggest-global-supply-chain-risks-of-2025 | https://www.newyorkfed.org/research/policy/gscpi. Sample data: date,gscpi
2021-12-01,4.43
2022-05-01,3.28
2024-12-01,-0.45

Source description: Monthly composite …

[Knowledge:163 hazards:Hazard_Seismic_Seiche Seismic Seiche] HAZARD_ID: hazards:Hazard_Seismic_Seiche
LABEL: Seismic Seiche
GROUP: Geophysical
SUBTYPE: Marine Incident
ALIASES: standing wave; enclosed waterbody; triggered by seismic waves; lake/reservoir sloshing; oscillating water levels; shoreline flooding; damage to docks/boats; possible far-field effects; distinct from tsunami; Seiche (stehende Welle); teilweise geschlossene Gewässer; ausgelöst durch seismische Wellen; Schwappen in See/Stausee; Wasserstandsschwingungen; Uferüberflutung; Schäden an Stegen/Booten; Fernwirkung möglich; Abgrenzung zum (Ozean-)Tsunami
BM25_TEXT_EN: Caused by hazard(s): Earthquake. Keywords: standing wave; enclosed waterbody; triggered by seismic waves; lake/reservoir sloshing; oscillating water levels; shoreline flooding; damage to docks/boats; possible far-field effects; distinct from tsunami. Schlüsselwörter: Seiche (stehende Welle); teilweise geschlossene Gewässer; ausgelöst durch seismische Wellen; Schwappen in See/Stausee; Wasserstandsschwingungen; Uferüberflutung; Schäden an Stegen/Booten; Fernwirkung möglich; Abgrenzung zum (Ozean-)Tsunami. Sources: https://www.usgs.gov/programs/earthquake-hazards/seismic-seiches | NOAA CO-OPS Water Level API | …

[Knowledge:88 hazards:Hazard_Impact_Event Impact Event] HAZARD_ID: hazards:Hazard_Impact_Event
LABEL: Impact Event
GROUP: Extraterrestrial
SUBTYPE: Space Hazard
ALIASES: impact event; einschlagsereignis
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: impact event. Schlüsselwörter: einschlagsereignis. Sources: https://en.wikipedia.org/wiki/Impact_event | NASA CNEOS Fireball Data API | https://ssd-api.jpl.nasa.gov/doc/fireball.html | NASA Fireball and Bolide Reports | https://data.nasa.gov/dataset/fireball-and-bolide-reports | NASA JPL CNEOS Fireball and Bolide Reports (CSV/Excel) | https://cneos.jpl.nasa.gov/fireballs/. Sample data: datetime_utc,lat_deg,lon_deg,alt_km,vel_km_s,vx_km_s,vy_km_s,vz_km_s,impact_energy_kt
2013-02-15 03:20:26,54.4,61.1,23.3,18.6,-12.2,6.5,-12.2,440.0
2020-12-22 23:23:33,31.9,96.2,35.5,13.6,-10.1,2.0,-8.9,9.8

Source description: Chronological table of fireball/bolide events detected by U.S. Government sensors with location, altitude, velocity components, and estimated impact energy; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Impact event. Keywords: impact event. Schlüsselwörter: einschlagsereignis. Sources: https://en.wikipedia.org/wiki/Impact_event | NASA CNEOS Fireball Data …

[Knowledge:24 hazards:Hazard_Chelyabinsk_Meteor Chelyabinsk Meteor] HAZARD_ID: hazards:Hazard_Chelyabinsk_Meteor
LABEL: Chelyabinsk Meteor
GROUP: Black Swan
SUBTYPE: Space Hazard
ALIASES: meteor airburst; shockwave; impact hazard; Meteor-Luftexplosion; Stoßwelle; Impaktgefahr
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: meteor airburst; shockwave; impact hazard. Schlüsselwörter: Meteor-Luftexplosion; Stoßwelle; Impaktgefahr. Sources: https://en.wikipedia.org/wiki/Chelyabinsk_meteor | NASA CNEOS Chelyabinsk details | https://cneos.jpl.nasa.gov/news/fireball_130301.html | NASA CNEOS Fireball Data API | https://ssd-api.jpl.nasa.gov/doc/fireball.html | NASA JPL CNEOS Fireball and Bolide Reports (CSV/Excel) | https://cneos.jpl.nasa.gov/fireballs/. Sample data: datetime_utc,lat_deg,lon_deg,alt_km,vel_km_s,vx_km_s,vy_km_s,vz_km_s,impact_energy_kt
2013-02-15 03:20:26,54.4,61.1,23.3,18.6,-12.2,6.5,-12.2,440.0
2020-12-22 23:23:33,31.9,96.2,35.5,13.6,-10.1,2.0,-8.9,9.8

Source description: Chronological table of fireball/bolide events detected by U.S. Government sensors with location, altitude, velocity components, and estimated impact energy; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Impact event. Keywords: meteor …

[Knowledge:130 hazards:Hazard_Natech_Accidents Natech Accidents] HAZARD_ID: hazards:Hazard_Natech_Accidents
LABEL: Natech Accidents
GROUP: Technological
SUBTYPE: Industrial Incident
ALIASES: natural hazard-triggered technological accident; industrial facilities; hazardous substances; fire/explosion/toxic release; safety barrier failure; cascading impacts; emergency response complexity; land-use/plant siting; risk assessment/Seveso linkage; long-term contamination; Natech-Unfälle; naturgefahrenausgelöste Technologiestörfälle; Industrieanlagen; Gefahrstoffe; Brand/Explosion/toxische Freisetzung; Versagen von Sicherheitsbarrieren; Kaskadeneffekte; komplexe Notfallbewältigung; Standortwahl/Anlagenplanung; Risikobewertung (z.B. Seveso) (Begriffe variieren); Langzeitkontamination
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Keywords: natural hazard-triggered technological accident; industrial facilities; hazardous substances; fire/explosion/toxic release; safety barrier failure; cascading impacts; emergency response complexity; land-use/plant siting; risk assessment/Seveso linkage; long-term contamination. Schlüsselwörter: Natech-Unfälle; naturgefahrenausgelöste Technologiestörfälle; …

[Knowledge:153 hazards:Hazard_Rockfall_Dry Rockfall (Dry)] HAZARD_ID: hazards:Hazard_Rockfall_Dry
LABEL: Rockfall (Dry)
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: rockfall (dry); Steinschlag (trocken)
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: rockfall (dry). Schlüsselwörter: Steinschlag (trocken). Sources: https://en.wikipedia.org/wiki/Rockfall_%28dry%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,landslide_type,trigger,road_closure,fatality_count
GLC000510,2019-06-14,USA,Rock fall,Earthquake,Yes,0
GLC000511,2022-07-02,Peru,Rock fall,Mining-related,No,2

Source description: Rockfall incident rows (type=Rock fall) with non-rain triggers; useful for dry rockfall hazard sampling and infrastructure impact fields (e.g., road closure).
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: rockfall (dry). Schlüsselwörter: Steinschlag (trocken). Sources: https://en.wikipedia.org/wiki/Rockfall_%28dry%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample …

[Knowledge:2 hazards:Hazard_AMOC_Collapse_Scenario AMOC Collapse] HAZARD_ID: hazards:Hazard_AMOC_Collapse_Scenario
LABEL: AMOC Collapse
GROUP: Black Swan
SUBTYPE: Environmental Degradation
ALIASES: Atlantic Meridional Overturning Circulation; abrupt climate change; ocean circulation; Atlantische meridionale Umwälzzirkulation; abrupter Klimawandel; Ozeanzirkulation
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: Atlantic Meridional Overturning Circulation; abrupt climate change; ocean circulation. Schlüsselwörter: Atlantische meridionale Umwälzzirkulation; abrupter Klimawandel; Ozeanzirkulation. Sources: RAPID 26N array data download | https://rapid.ac.uk/data/data-download ; Copernicus Marine AMOC 26.5N indicator | https://data.marine.copernicus.eu/product/GLOBAL_OMI_NATLANTIC_amoc_max26N_timeseries/description. Sample data: date,amoc_strength_Sv,method
2025-12-01,16.9,RAPID_26N
2026-01-01,15.7,RAPID_26N
2026-02-01,14.8,RAPID_26N

Source description: Time series of Atlantic Meridional Overturning Circulation (AMOC) strength at ~26.5°N from the RAPID array (observations) and related derived indicator products. Values are typically in Sverdrups (Sv) and used to study AMOC variability and collapse scenarios.
Source: RAPID data download …

[Knowledge:34 hazards:Hazard_Cold_Wave Cold Wave] HAZARD_ID: hazards:Hazard_Cold_Wave
LABEL: Cold Wave
GROUP: Climatological
SUBTYPE: Extreme Temperature
ALIASES: cold wave; extreme cold; cold spell; Kältewelle; Extremkälte; Kälteperiode
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: cold wave; extreme cold; cold spell. Schlüsselwörter: Kältewelle; Extremkälte; Kälteperiode. Sources: Wikipedia | https://en.wikipedia.org/wiki/Cold_wave | NOAA NCEI Storm Events Database | https://www.ncei.noaa.gov/stormevents/ | NOAA NCEI GHCN-Daily | https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily. Sample data: STATION,DATE,TMIN_C,TMAX_C,PRCP_mm,AWND_mps
USW00014819,2024-01-13,-27.2,-16.1,0.0,6.2
USW00014819,2024-01-14,-29.4,-18.3,0.0,7.1
USW00014819,2024-01-15,-26.7,-14.4,0.0,5.8

Source description: Daily station observations (e.g., Tmin/Tmax, precipitation, wind) suitable to characterize cold-wave intensity and duration; values follow GHCN-Daily-style daily summaries.
Source: NOAA NCEI GHCN-Daily | https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily.
VERBALIZED_EN: Caused by hazard(s): Climate change. Keywords: cold wave; extreme cold; …

[Knowledge:5 hazards:Hazard_Animal_Incident Animal Incident] HAZARD_ID: hazards:Hazard_Animal_Incident
LABEL: Animal Incident
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: animal incident; Tierereignis
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: animal incident. Schlüsselwörter: Tierereignis. Sources: https://en.wikipedia.org/wiki/Animal_incident | Data.gov Animal Control Incidents | https://catalog.data.gov/dataset/animal-control-incidents. Sample data: incident_date,incident_type,animal_type,outcome,city,zip
2025-05-21,Bite report,Dog,Quarantine,Baton Rouge,70802
2025-06-03,Stray pickup,Dog,Shelter intake,Baton Rouge,70805
2025-06-19,Aggressive animal,Wildlife,Released,Baton Rouge,70810

Source description: Municipal animal-control incident logs (time-stamped events such as bites, aggressive animals, pickups). Useful as a raw ‘animal incident’ sample.
Source: Data.gov Animal Control Incidents | https://catalog.data.gov/dataset/animal-control-incidents.
VERBALIZED_EN: Caused by hazard(s): Zoonotic spillover. Keywords: animal incident. Schlüsselwörter: Tierereignis. Sources: https://en.wikipedia.org/wiki/Animal_incident | Data.gov Animal Control Incidents | https://catalog.data.gov/dataset/animal-control-incidents. …

[Knowledge:12 hazards:Hazard_Avalanche_Dry Avalanche (Dry)] HAZARD_ID: hazards:Hazard_Avalanche_Dry
LABEL: Avalanche (Dry)
GROUP: Hydrological
SUBTYPE: Mass Movement
ALIASES: avalanche (dry); Lawine (trocken)
BM25_TEXT_EN: Caused by hazard(s): Landslide|hazards:hazard avalanche. Keywords: avalanche (dry). Schlüsselwörter: Lawine (trocken). Sources: https://en.wikipedia.org/wiki/Avalanche_%28dry%29 | WSL/SLF EnviDat: Fatal avalanche accidents (CH) | https://www.envidat.ch/metadata/fatal-avalanche-accidents-in-switzerland-since-1936-37. Sample data: date,region,canton,activity,avalanche_type,fatalities,injured,elevation_m
2017-02-11,Grisons,GR,Backcountry touring,Dry slab,1,0,2600
2020-01-05,Valais,VS,Off-piste,Dry slab,2,1,2300

Source description: Subset of avalanche accident records where avalanche type is dry-snow (e.g., dry slab). Useful for modeling conditions/impacts specific to dry avalanches.
Source: WSL/SLF EnviDat: Fatal avalanche accidents (CH) | https://www.envidat.ch/metadata/fatal-avalanche-accidents-in-switzerland-since-1936-37.
VERBALIZED_EN: Caused by hazard(s): Landslide|hazards:hazard avalanche. Keywords: avalanche (dry). Schlüsselwörter: Lawine (trocken). Sources: https://en.wikipedia.org/wiki/Avalanche_%28dry%29 | …

[Knowledge:107 hazards:Hazard_Landslide_Wet Landslide (Wet)] HAZARD_ID: hazards:Hazard_Landslide_Wet
LABEL: Landslide (Wet)
GROUP: Hydrological
SUBTYPE: Mass Movement
ALIASES: landslide (wet); Erdrutsch (nass)
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: landslide (wet). Schlüsselwörter: Erdrutsch (nass). Sources: https://en.wikipedia.org/wiki/Landslide_%28wet%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,landslide_type,trigger,rainfall_mm_24h,fatality_count
GLC000610,2020-10-05,Philippines,Landslide,Tropical Cyclone,210,6
GLC000611,2023-02-21,Colombia,Landslide,Rain,95,11

Source description: Subset of landslide incident rows emphasizing wet triggers (heavy rainfall/cyclones); rainfall fields can be joined from meteorological reanalysis if not present.
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: landslide (wet). Schlüsselwörter: Erdrutsch (nass). Sources: https://en.wikipedia.org/wiki/Landslide_%28wet%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. …

[Knowledge:168 hazards:Hazard_Soil_Contamination Soil contamination] HAZARD_ID: hazards:Hazard_Soil_Contamination
LABEL: Soil contamination
GROUP: Chemical
SUBTYPE: Environmental Degradation
ALIASES: soil contamination, soil pollution, contaminated soil, toxic soil, heavy metals, pesticides, herbicides, PFAS, hydrocarbons, industrial contamination, land degradation, brownfield; Bodenverunreinigung, Bodenverschmutzung, kontaminierter Boden, Giftstoffe im Boden, Schwermetalle, Pestizide, Herbizide, PFAS, Kohlenwasserstoffe, Altlasten, Bodendegradation, Industriebelastung
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure|hazards:hazard chronic pollution tipping event|hazards:hazard environmental pollution. Keywords: soil contamination, soil pollution, contaminated soil, toxic soil, heavy metals, pesticides, herbicides, PFAS, hydrocarbons, industrial contamination, land degradation, brownfield. Schlüsselwörter: Bodenverunreinigung, Bodenverschmutzung, kontaminierter Boden, Giftstoffe im Boden, Schwermetalle, Pestizide, Herbizide, PFAS, Kohlenwasserstoffe, Altlasten, Bodendegradation, Industriebelastung. Sources: Wikipedia (Soil contamination) | https://en.wikipedia.org/wiki/Soil_contamination | US …

[Knowledge:157 hazards:Hazard_Rogue_Planet Rogue Planet] HAZARD_ID: hazards:Hazard_Rogue_Planet
LABEL: Rogue Planet
GROUP: Black Swan
SUBTYPE: Space Hazard
ALIASES: rogue planet; interstellar planet; free-floating planet; Rogue-Planet; interstellarer Planet; frei schwebender Planet
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: rogue planet; interstellar planet; free-floating planet. Schlüsselwörter: Rogue-Planet; interstellarer Planet; frei schwebender Planet. Sources: https://en.wikipedia.org/wiki/Rogue_planet | Gaia DR3 Microlensing Events (CSV) | https://www.astrouw.edu.pl/~wyrzykow/GaiaDR3/GaiaDR3_microlensing.html. Sample data: event_id,ra_deg,dec_deg,t0_jd,tE_days,u0,chi2
GDR3-ML-001,266.416,-29.008,2459001.5,42.1,0.12,1.05
GDR3-ML-002,83.633,22.014,2459123.7,18.4,0.35,0.98

Source description: Catalog of candidate microlensing events from Gaia DR3 (can include lenses consistent with compact objects; used as proxy data for rogue planets/black holes via microlensing signatures).
Source: Gaia DR3 Microlensing Events (CSV) | https://www.astrouw.edu.pl/~wyrzykow/GaiaDR3/GaiaDR3_microlensing.html.
VERBALIZED_EN: Caused by hazard(s): Impact event. Keywords: rogue planet; interstellar planet; free-floating planet. …

[Knowledge:156 hazards:Hazard_Rogue_Black_Hole Rogue Black Hole] HAZARD_ID: hazards:Hazard_Rogue_Black_Hole
LABEL: Rogue Black Hole
GROUP: Black Swan
SUBTYPE: Space Hazard
ALIASES: black hole; rogue black hole; compact object; gravitational lensing; Schwarzes Loch; umherwanderndes Schwarzes Loch; kompaktes Objekt; Gravitationslinseneffekt
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: black hole; rogue black hole; compact object; gravitational lensing. Schlüsselwörter: Schwarzes Loch; umherwanderndes Schwarzes Loch; kompaktes Objekt; Gravitationslinseneffekt. Sources: https://en.wikipedia.org/wiki/Black_hole | Gaia DR3 Microlensing Events (CSV) | https://www.astrouw.edu.pl/~wyrzykow/GaiaDR3/GaiaDR3_microlensing.html. Sample data: event_id,ra_deg,dec_deg,t0_jd,tE_days,u0,chi2
GDR3-ML-001,266.416,-29.008,2459001.5,42.1,0.12,1.05
GDR3-ML-002,83.633,22.014,2459123.7,18.4,0.35,0.98

Source description: Catalog of candidate microlensing events from Gaia DR3 (can include lenses consistent with compact objects; used as proxy data for rogue planets/black holes via microlensing signatures).
Source: Gaia DR3 Microlensing Events (CSV) | https://www.astrouw.edu.pl/~wyrzykow/GaiaDR3/GaiaDR3_microlensing.html.
VERBALIZED_EN: Caused by hazard(s): …

[Knowledge:143 hazards:Hazard_Permafrost_Loss Permafrost Loss] HAZARD_ID: hazards:Hazard_Permafrost_Loss
LABEL: Permafrost Loss
GROUP: Geophysical
SUBTYPE: Extreme Temperature
ALIASES: permafrost thaw; ground-ice melt; thermokarst; ground subsidence; slope instability; infrastructure damage; hydrology shift; carbon release (CO2/CH4); long timescales; Permafrostverlust (auch: Permafrost-Auftauen); Schmelze von Bodeneis; Thermokarst; Bodensenkung; Hanginstabilität; Infrastrukturschäden; veränderte Hydrologie; Kohlenstofffreisetzung (CO2/CH4); lange Zeitskalen
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: permafrost thaw; ground-ice melt; thermokarst; ground subsidence; slope instability; infrastructure damage; hydrology shift; carbon release (CO2/CH4); long timescales. Schlüsselwörter: Permafrostverlust (auch: Permafrost-Auftauen); Schmelze von Bodeneis; Thermokarst; Bodensenkung; Hanginstabilität; Infrastrukturschäden; veränderte Hydrologie; Kohlenstofffreisetzung (CO2/CH4); lange Zeitskalen. Sources: Wikipedia | https://en.wikipedia.org/wiki/Permafrost#Permafrost_degradation | ESA CCI Permafrost (Active Layer Thickness) | https://catalogue.ceda.ac.uk/uuid/d34330ce3f604e368c06d76de1987ce5/ | PERMOS Data Portal | …

[Knowledge:113 hazards:Hazard_Liquefaction Liquefaction] HAZARD_ID: hazards:Hazard_Liquefaction
LABEL: Liquefaction
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: saturated loose sediments; pore-water pressure increase; loss of shear strength; earthquake shaking; ground settlement; lateral spreading; sand boils; foundation failure; lifeline rupture; wassergesättigte Lockersedimente; Porenwasserdruckanstieg; Verlust der Scherfestigkeit; Erdbebenerschütterung; Bodensetzung; laterale Ausbreitung; Sandvulkane (Sand boils) (auch: Sandaufbrüche); Fundamentversagen; Leitungsbrüche
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: saturated loose sediments; pore-water pressure increase; loss of shear strength; earthquake shaking; ground settlement; lateral spreading; sand boils; foundation failure; lifeline rupture. Schlüsselwörter: wassergesättigte Lockersedimente; Porenwasserdruckanstieg; Verlust der Scherfestigkeit; Erdbebenerschütterung; Bodensetzung; laterale Ausbreitung; Sandvulkane (Sand boils) (auch: Sandaufbrüche); Fundamentversagen; Leitungsbrüche. Sources: https://www.undrr.org/understanding-disaster-risk/terminology/hips/gh0307 | https://www.usgs.gov/faqs/what-liquefaction | California Geological Survey Liquefaction Zones …

[Knowledge:60 hazards:Hazard_Extreme_Temperature Extreme Temperature] HAZARD_ID: hazards:Hazard_Extreme_Temperature
LABEL: Extreme Temperature
GROUP: Climatological
SUBTYPE: Extreme Temperature
ALIASES: extreme temperature; Extreme Temperaturen
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: extreme temperature. Schlüsselwörter: Extreme Temperaturen. Sources: Wikipedia (Extreme temperature) | https://en.wikipedia.org/wiki/Extreme_temperature | NOAA NCEI (GHCN-Daily sample CSV) | https://www.ncei.noaa.gov/pub/data/cdo/samples/GHCND_sample_csv.csv. Sample data: STATION,STATION_NAME,ELEVATION,LATITUDE,LONGITUDE,DATE,TMAX,TMIN,PRCP
GHCND:USC00327027,PETERSBURG 2 N ND US,466.3,48.0355,-98.01,20100101,-178,-311,0
GHCND:USC00327027,PETERSBURG 2 N ND US,466.3,48.0355,-98.01,20100102,-167,-289,0

Source description: Station-based daily observations (maximum/minimum temperature and precipitation). Raw daily TMAX/TMIN series are a standard input for detecting extreme temperature events and heat-related thresholds.
Source: NOAA NCEI (GHCN-Daily sample CSV) | https://www.ncei.noaa.gov/pub/data/cdo/samples/GHCND_sample_csv.csv.
VERBALIZED_EN: Caused by hazard(s): Climate change. Keywords: extreme temperature. Schlüsselwörter: Extreme Temperaturen. …

[Knowledge:27 hazards:Hazard_Chronic_Pollution_Tipping_Event Chronic Pollution Tipping Event] HAZARD_ID: hazards:Hazard_Chronic_Pollution_Tipping_Event
LABEL: Chronic Pollution Tipping Event
GROUP: Environmental
SUBTYPE: Environmental Degradation
ALIASES: chronic pollution; ecological tipping point; contamination accumulation; Chronische Umweltverschmutzung; ökologischer Kipppunkt; Schadstoffanreicherung
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: chronic pollution; ecological tipping point; contamination accumulation. Schlüsselwörter: Chronische Umweltverschmutzung; ökologischer Kipppunkt; Schadstoffanreicherung. Sources: US EPA Air Quality System (AQS) API | https://aqs.epa.gov/aqsweb/documents/data_api.html ; EEA Air Quality download service | https://www.eea.europa.eu/en/datahub/datahubitem-view/778ef9f5-6293-4846-badd-56a29c70880d. Sample data: state_code,county_code,site_number,date_local,parameter_name,arithmetic_mean,unit
06,075,0003,2025-07-01,PM2.5 - Local Conditions,18.2,ug/m3
06,075,0003,2025-07-02,PM2.5 - Local Conditions,22.7,ug/m3
06,075,0003,2025-07-03,PM2.5 - Local Conditions,35.9,ug/m3

Source description: Row-level air pollution monitoring data (e.g., daily PM2.5 concentrations) from regulatory networks. Useful for modeling chronic …

[Knowledge:106 hazards:Hazard_Landslide_Dry Landslide (Dry)] HAZARD_ID: hazards:Hazard_Landslide_Dry
LABEL: Landslide (Dry)
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: landslide (dry); Erdrutsch (trocken)
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: landslide (dry). Schlüsselwörter: Erdrutsch (trocken). Sources: https://en.wikipedia.org/wiki/Landslide_%28dry%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,landslide_type,trigger,fatality_count
GLC000410,2018-01-22,Italy,Rock slide,Earthquake,3
GLC000411,2021-09-07,USA,Rock fall,Construction,0

Source description: Subset of landslide/mass-movement incident rows emphasizing dry triggers (seismic/anthropogenic) and rockfall/rockslide types.
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: landslide (dry). Schlüsselwörter: Erdrutsch (trocken). Sources: https://en.wikipedia.org/wiki/Landslide_%28dry%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: …

[Knowledge:123 hazards:Hazard_Mass_Movement_Dry Mass Movement (Dry)] HAZARD_ID: hazards:Hazard_Mass_Movement_Dry
LABEL: Mass Movement (Dry)
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: mass movement (dry); Massenbewegung (trocken)
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: mass movement (dry). Schlüsselwörter: Massenbewegung (trocken). Sources: https://en.wikipedia.org/wiki/Mass_movement_%28dry%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,landslide_type,trigger,fatality_count,notes
GLC000210,2019-06-14,USA,Rock fall,Earthquake,0,"Dry mass movement; boulder fall onto roadway"
GLC000211,2022-07-02,Peru,Rock fall,Mining-related,2,"Rockfall in dry conditions"

Source description: Mass-movement incident rows emphasizing relatively dry triggers (rockfall/rock slide, seismic/anthropogenic triggers) using landslide-type and trigger fields.
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: mass movement (dry). Schlüsselwörter: Massenbewegung (trocken). Sources: https://en.wikipedia.org/wiki/Mass_movement_%28dry%29 | …

[Knowledge:78 hazards:Hazard_Ground_Movement Ground Movement] HAZARD_ID: hazards:Hazard_Ground_Movement
LABEL: Ground Movement
GROUP: Geophysical
SUBTYPE: Earthquake
ALIASES: ground movement; Bodenbewegung
BM25_TEXT_EN: Caused by hazard(s): Earthquake. Keywords: ground movement. Schlüsselwörter: Bodenbewegung. Sources: LiCSAR InSAR products (CEDA catalogue) | https://catalogue.ceda.ac.uk/uuid/52cda2e0e6c04272ae15ac836c1e8493/ ; COMET LiCS Sentinel-1 InSAR Portal | https://comet.nerc.ac.uk/comet-lics-portal/. Sample data: frame_id,product_type,acquisition_start,acquisition_end,mean_los_displacement_mm,coherence_mean
014A_05201_131313,unwrapped_interferogram,2025-06-01,2025-06-13,-12.4,0.61
014A_05201_131313,unwrapped_interferogram,2025-06-13,2025-06-25,-8.1,0.58

Source description: Sentinel-1 InSAR-derived ground deformation products (interferograms/coherence/unwrapped phase) distributed by COMET LiCS/LiCSAR. Used to quantify ground movement such as subsidence, uplift, landslide motion, and tectonic deformation.
Source: CEDA LiCSAR dataset record | https://catalogue.ceda.ac.uk/uuid/52cda2e0e6c04272ae15ac836c1e8493/.
VERBALIZED_EN: Caused by hazard(s): Earthquake. Keywords: ground movement. Schlüsselwörter: Bodenbewegung. Sources: LiCSAR …

[Knowledge:140 hazards:Hazard_Orphan_Source_Incident_Lost_Radioactive_Source Orphan Source Incident (Lost Radioactive Source)] HAZARD_ID: hazards:Hazard_Orphan_Source_Incident_Lost_Radioactive_Source
LABEL: Orphan Source Incident (Lost Radioactive Source)
GROUP: Black Swan
SUBTYPE: Nuclear-Radiological Incident
ALIASES: orphan source; radioactive source; radiation exposure; contamination; herrenlose Quelle; radioaktive Quelle; Strahlenexposition; Kontamination
BM25_TEXT_EN: Caused by hazard(s): Critical infrastructure failure. Keywords: orphan source; radioactive source; radiation exposure; contamination. Schlüsselwörter: herrenlose Quelle; radioaktive Quelle; Strahlenexposition; Kontamination. Sources: https://en.wikipedia.org/wiki/Orphan_source | IAEA INES database | https://www.iaea.org/resources/databases/international-nuclear-and-radiological-event-scale | IAEA Nuclear Events Web-based System (NEWS) | https://www.iaea.org/resources/databases/nuclear-events-web-based-system. Sample data: event_date,country,event_title,ines_level,source_category,status
2024-11-18,Republic of Korea,"Worker exposure caused by a radiation-generating device",2,"Radiation generating device","Reported"
2023-06-07,CountryX,"Lost industrial gauge source; recovered later",1,"Industrial …

[Knowledge:161 hazards:Hazard_Sea_Level_Rise Sea Level Rise] HAZARD_ID: hazards:Hazard_Sea_Level_Rise
LABEL: Sea Level Rise
GROUP: Hydrological
SUBTYPE: Marine Incident
ALIASES: relative sea-level rise; thermal expansion; ice-sheet/glacier melt; coastal inundation; overtopping/overwash; exacerbated storm surge; saline flooding; shoreline change; adaptation thresholds; long-term trend; relativer Meeresspiegelanstieg; thermische Ausdehnung; Schmelze von Eisschilden/Gletschern; Küstenüberflutung; Überspülung (overwash); verstärkte Sturmflut; salzbedingte Überflutung; Veränderung der Küstenlinie; Anpassungsschwellen; langfristiger Trend
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: relative sea-level rise; thermal expansion; ice-sheet/glacier melt; coastal inundation; overtopping/overwash; exacerbated storm surge; saline flooding; shoreline change; adaptation thresholds; long-term trend. Schlüsselwörter: relativer Meeresspiegelanstieg; thermische Ausdehnung; Schmelze von Eisschilden/Gletschern; Küstenüberflutung; Überspülung (overwash); verstärkte Sturmflut; salzbedingte Überflutung; Veränderung der Küstenlinie; Anpassungsschwellen; langfristiger Trend. Sources: …

[Knowledge:185 hazards:Hazard_Sudden_Subsidence_Wet Sudden Subsidence (Wet)] HAZARD_ID: hazards:Hazard_Sudden_Subsidence_Wet
LABEL: Sudden Subsidence (Wet)
GROUP: Hydrological
SUBTYPE: Mass Movement
ALIASES: sudden subsidence (wet); Plötzliche Absenkung (nass)
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: sudden subsidence (wet). Schlüsselwörter: Plötzliche Absenkung (nass). Sources: https://en.wikipedia.org/wiki/Sudden_Subsidence_%28wet%29 | ASF HyP3 ARIA-S1 GUNW Product Guide | https://hyp3-docs.asf.alaska.edu/guides/gunw_product_guide/ | NASA Earthdata ARIA-S1-GUNW recipe | https://www.earthdata.nasa.gov/data/catalog/asf-aria-s1-gunw-1. Sample data: scene_id,acquisition_start_utc,acquisition_end_utc,center_lat,center_lon,los_displacement_cm,coherence
S1A_IW_SLC__1SDV_20251003T172233,2025-10-03T17:22:33Z,2025-10-03T17:22:58Z,31.215,35.012,-4.8,0.72
S1A_IW_SLC__1SDV_20251015T172233,2025-10-15T17:22:33Z,2025-10-15T17:22:58Z,31.215,35.012,-8.9,0.68
S1B_IW_SLC__1SDV_20251027T172233,2025-10-27T17:22:33Z,2025-10-27T17:22:58Z,31.215,35.012,-12.4,0.61

Source description: Example rows representing Sentinel‑1 InSAR (ARIA-S1-GUNW) line‑of‑sight displacement observations over a deforming area. Useful as a raw proxy for sudden/wet subsidence signals (rapid …

[Knowledge:28 hazards:Hazard_Civil_Unrest Civil Unrest] HAZARD_ID: hazards:Hazard_Civil_Unrest
LABEL: Civil Unrest
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: riots; collective violence; political instability; protest escalation; public order disruption; damage to assets; service disruption; policing strain; impeded emergency response; urban concentration; zivile Unruhen; Ausschreitungen; kollektive Gewalt; politische Instabilität; Eskalation von Protesten; Störung der öffentlichen Ordnung; Sachschäden; Ausfall von Dienstleistungen; Belastung der Sicherheitskräfte; Behinderung der Notfallhilfe; häufig urban
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: riots; collective violence; political instability; protest escalation; public order disruption; damage to assets; service disruption; policing strain; impeded emergency response; urban concentration. Schlüsselwörter: zivile Unruhen; Ausschreitungen; kollektive Gewalt; politische Instabilität; Eskalation von Protesten; Störung der öffentlichen Ordnung; Sachschäden; Ausfall von Dienstleistungen; Belastung der Sicherheitskräfte; Behinderung der Notfallhilfe; häufig urban. Sources: https://www.undrr.org/understanding-disaster-risk/terminology/hips/so0103 | UCDP …

[Knowledge:124 hazards:Hazard_Mass_Movement_Wet Mass Movement (Wet)] HAZARD_ID: hazards:Hazard_Mass_Movement_Wet
LABEL: Mass Movement (Wet)
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: mass movement (wet); Massenbewegung (nass)
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: mass movement (wet). Schlüsselwörter: Massenbewegung (nass). Sources: https://en.wikipedia.org/wiki/Mass_movement_%28wet%29 | NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export. Sample data: event_id,event_date,country_name,landslide_type,trigger,fatality_count,notes
GLC000310,2020-10-05,Philippines,Mudslide,Tropical Cyclone,6,"Rainfall-driven mass movement"
GLC000311,2023-02-21,Colombia,Debris flow,Rain,11,"Saturated-slope failure"

Source description: Mass-movement incident rows emphasizing wet triggers (heavy rainfall/cyclones) such as mudslides and debris flows; useful for wet-slope failure modeling.
Source: NASA Global Landslide Catalog (CSV) | https://data.nasa.gov/dataset/global-landslide-catalog-export.
VERBALIZED_EN: Caused by hazard(s): Landslide. Keywords: mass movement (wet). Schlüsselwörter: Massenbewegung (nass). Sources: https://en.wikipedia.org/wiki/Mass_movement_%28wet%29 | NASA Global Landslide …

[Knowledge:51 hazards:Hazard_Drought Drought] HAZARD_ID: hazards:Hazard_Drought
LABEL: Drought
GROUP: Climatological
SUBTYPE: Extreme Temperature
ALIASES: drought; water scarcity; prolonged dry period; Dürre; Wasserknappheit; langanhaltende Trockenheit
BM25_TEXT_EN: Caused by hazard(s): Drought. Keywords: drought; water scarcity; prolonged dry period. Schlüsselwörter: Dürre; Wasserknappheit; langanhaltende Trockenheit. Sources: Wikipedia (Drought) | https://en.wikipedia.org/wiki/Drought | U.S. Drought Monitor Data Download | https://droughtmonitor.unl.edu/DmData/DataDownload.aspx | Drought.gov Data Download (indices e.g., SPEI) | https://www.drought.gov/data-download. Sample data: week_start,area,none_pct,D0_pct,D1_pct,D2_pct,D3_pct,D4_pct,DSCI
2025-06-03,US,61.2,12.4,10.1,8.3,6.1,1.9,205
2025-06-10,US,60.5,12.8,10.4,8.6,6.0,1.7,210

Source description: Weekly U.S. Drought Monitor severity distribution and Drought Severity and Coverage Index (DSCI) time series (percent area in each drought class), downloadable as tabular data.
Source: Drought.gov Data Download (indices e.g., SPEI) | https://www.drought.gov/data-download.
VERBALIZED_EN: Caused by hazard(s): Drought. Keywords: drought; water scarcity; prolonged dry period. …

[Knowledge:115 hazards:Hazard_Lost_Abandoned_Radioactive_Source Lost/abandoned Radioactive Source] HAZARD_ID: hazards:Hazard_Lost_Abandoned_Radioactive_Source
LABEL: Lost/abandoned Radioactive Source
GROUP: Radiological
SUBTYPE: Nuclear-Radiological Incident
ALIASES: orphan source; lost source; abandoned radioactive source; Verwaiste Quelle; verlorene Strahlenquelle; aufgegebene Strahlenquelle
BM25_TEXT_EN: Caused by hazard(s): War. Keywords: orphan source; lost source; abandoned radioactive source. Schlüsselwörter: Verwaiste Quelle; verlorene Strahlenquelle; aufgegebene Strahlenquelle. Sources: https://en.wikipedia.org/wiki/Orphan_source | IAEA INES database | https://www.iaea.org/resources/databases/international-nuclear-and-radiological-event-scale | IAEA Nuclear Events Web-based System (NEWS) | https://www.iaea.org/resources/databases/nuclear-events-web-based-system. Sample data: event_date,country,event_title,ines_level,source_category,status
2024-11-18,Republic of Korea,"Worker exposure caused by a radiation-generating device",2,"Radiation generating device","Reported"
2023-06-07,CountryX,"Lost industrial gauge source; recovered later",1,"Industrial source","Reported"
2019-09-12,CountryY,"Orphan source found in scrap yard",2,"Orphan source","Reported"

Source description: …

[Knowledge:133 hazards:Hazard_Non_International_Armed_Conflict_NIAC Non-international Armed Conflict (NIAC)] HAZARD_ID: hazards:Hazard_Non_International_Armed_Conflict_NIAC
LABEL: Non-international Armed Conflict (NIAC)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: civil war, internal armed conflict, intrastate conflict; nichtinternationaler bewaffneter Konflikt, Bürgerkrieg, innerstaatlicher Konflikt
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: civil war, internal armed conflict, intrastate conflict. Schlüsselwörter: nichtinternationaler bewaffneter Konflikt, Bürgerkrieg, innerstaatlicher Konflikt. Sources: https://en.wikipedia.org/wiki/Non-international_armed_conflict | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. …

[Knowledge:95 hazards:Hazard_International_Armed_Conflict_IAC International Armed Conflict (IAC)] HAZARD_ID: hazards:Hazard_International_Armed_Conflict_IAC
LABEL: International Armed Conflict (IAC)
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: war between states, international war, interstate war; internationaler bewaffneter Konflikt, Krieg zwischen Staaten, zwischenstaatlicher Krieg
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: war between states, international war, interstate war. Schlüsselwörter: internationaler bewaffneter Konflikt, Krieg zwischen Staaten, zwischenstaatlicher Krieg. Sources: https://en.wikipedia.org/wiki/International_humanitarian_law | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: …

[Knowledge:7 hazards:Hazard_Armed_Conflict Armed Conflict] HAZARD_ID: hazards:Hazard_Armed_Conflict
LABEL: Armed Conflict
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: war, armed conflict; Krieg, bewaffneter Konflikt
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: war, armed conflict. Schlüsselwörter: Krieg, bewaffneter Konflikt. Sources: https://en.wikipedia.org/wiki/Armed_conflict | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: war, armed conflict. Schlüsselwörter: Krieg, bewaffneter Konflikt. Sources: https://en.wikipedia.org/wiki/Armed_conflict | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: …

[Knowledge:111 hazards:Hazard_Lightning Lightning] HAZARD_ID: hazards:Hazard_Lightning
LABEL: Lightning
GROUP: Meteorological
SUBTYPE: Lightning
ALIASES: lightning; lightning strike; thunderstorm; atmospheric electricity; electrical discharge; cloud-to-ground; intra-cloud; thunder; Blitz; Blitzeinschlag; Gewitter; atmosphärische Elektrizität; elektrische Entladung; Wolke-Boden; Wolke-Wolke; Donner
BM25_TEXT_EN: Caused by hazard(s): Lightning. Keywords: lightning; lightning strike; thunderstorm; atmospheric electricity; electrical discharge; cloud-to-ground; intra-cloud; thunder. Schlüsselwörter: Blitz; Blitzeinschlag; Gewitter; atmosphärische Elektrizität; elektrische Entladung; Wolke-Boden; Wolke-Wolke; Donner. Sources: https://en.wikipedia.org/wiki/Lightning | https://www.ncei.noaa.gov/access/metadata/landing-page/bin/iso?id=gov.noaa.ncdc:C01527. Sample data: flash_id,flash_time_utc,flash_lat,flash_lon,flash_area_km2,flash_energy_j
F123456789,2025-06-21T18:05:12Z,34.21,-97.43,112.5,3.8e5
F123456790,2025-06-21T18:05:14Z,34.19,-97.40,98.2,2.6e5

Source description: Satellite-based lightning detections (events/groups/flashes) from the GOES Geostationary Lightning Mapper (GLM) Level-2 product, including location and optical energy …

[Knowledge:219 hazards:Hazard_Worms_Infestation Worms Infestation] HAZARD_ID: hazards:Hazard_Worms_Infestation
LABEL: Worms Infestation
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: worms infestation; Wurmbefall
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: worms infestation. Schlüsselwörter: Wurmbefall. Sources: https://en.wikipedia.org/wiki/Worms_infestation | WHO GHO OData API | https://www.who.int/data/gho/info/gho-odata-api. Sample data: indicator_code,country,year,value,unit
NTD_STH_PREV,Kenya,2022,7.3,percent
NTD_STH_PREV,India,2022,2.1,percent
NTD_STH_PREV,Brazil,2022,0.8,percent

Source description: Example indicator-style rows (WHO GHO OData) representing helminth/soil-transmitted-helminth prevalence by country and year; usable as a worms/helminth infestation proxy dataset.
Source: WHO GHO OData API | https://www.who.int/data/gho/info/gho-odata-api.
VERBALIZED_EN: Caused by hazard(s): Zoonotic spillover. Keywords: worms infestation. Schlüsselwörter: Wurmbefall. Sources: https://en.wikipedia.org/wiki/Worms_infestation | WHO GHO OData API | https://www.who.int/data/gho/info/gho-odata-api. Sample data: …

[Knowledge:97 hazards:Hazard_Internationalized_Non_International_Armed_Conflict Internationalized Non-international Armed Conflict] HAZARD_ID: hazards:Hazard_Internationalized_Non_International_Armed_Conflict
LABEL: Internationalized Non-international Armed Conflict
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: NIAC with foreign involvement, external intervention; internationalisierter innerstaatlicher Konflikt, ausländische Einmischung
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. Keywords: NIAC with foreign involvement, external intervention. Schlüsselwörter: internationalisierter innerstaatlicher Konflikt, ausländische Einmischung. Sources: https://en.wikipedia.org/wiki/International_humanitarian_law | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism. …

[Knowledge:208 hazards:Hazard_War War] HAZARD_ID: hazards:Hazard_War
LABEL: War
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: armed conflict; Bewaffneter Konflikt
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: armed conflict. Schlüsselwörter: Bewaffneter Konflikt. Sources: https://en.wikipedia.org/wiki/War | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Terrorism. Keywords: armed conflict. Schlüsselwörter: Bewaffneter Konflikt. Sources: https://en.wikipedia.org/wiki/War | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of …

[Knowledge:126 hazards:Hazard_Meteotsunami Meteotsunami] HAZARD_ID: hazards:Hazard_Meteotsunami
LABEL: Meteotsunami
GROUP: Meteorological
SUBTYPE: Tsunami
ALIASES: meteorological tsunami; rapid air-pressure jump; squall line/thunderstorm; wind stress; resonance (harbor/bay); long-period wave; sudden coastal run-up; strong currents; short warning time; Meteotsunami (meteorologischer Tsunami); rascher Luftdrucksprung; Böenlinie/Squall Line; Windstress; Resonanz (Hafen/Bucht); langperiodische Welle; plötzlicher Küstenauflauf; starke Strömungen; kurze Vorwarnzeit
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: meteorological tsunami; rapid air-pressure jump; squall line/thunderstorm; wind stress; resonance (harbor/bay); long-period wave; sudden coastal run-up; strong currents; short warning time. Schlüsselwörter: Meteotsunami (meteorologischer Tsunami); rascher Luftdrucksprung; Böenlinie/Squall Line; Windstress; Resonanz (Hafen/Bucht); langperiodische Welle; plötzlicher Küstenauflauf; starke Strömungen; kurze Vorwarnzeit. Sources: https://oceanservice.noaa.gov/facts/meteotsunami.html | https://repository.library.noaa.gov/view/noaa/28470 | Adriatic Meteotsunami Catalogue | https://jadran.izor.hr/~sepic/meteotsunami_catalogue/. Sample …

[Knowledge:203 hazards:Hazard_Vog_Volcanic_Smog Vog (volcanic smog)] HAZARD_ID: hazards:Hazard_Vog_Volcanic_Smog
LABEL: Vog (volcanic smog)
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: vog; volcanic smog; sulfur dioxide plume; volcanic haze; sulfate aerosol; Vog; vulkanischer Smog; Schwefeldioxidfahne; Vulkan-Dunst; Sulfat-Aerosol
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: vog; volcanic smog; sulfur dioxide plume; volcanic haze; sulfate aerosol. Schlüsselwörter: Vog; vulkanischer Smog; Schwefeldioxidfahne; Vulkan-Dunst; Sulfat-Aerosol. Sources: https://en.m.wikipedia.org/wiki/Vog | Copernicus CAMS Global Reanalysis (EAC4) | https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4. Sample data: time_utc,lat,lon,dust_aod_550,total_aod_550,so2_kg_m2
2024-02-18T12:00Z,28.0,-15.0,0.65,0.80,0.00002
2024-02-18T12:00Z,30.0,-10.0,0.58,0.72,0.00001

Source description: Atmospheric composition reanalysis including aerosols (e.g., dust AOD) useful for sand/dust storms, Saharan dust and vog dispersion analyses..
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: vog; volcanic smog; sulfur dioxide plume; volcanic haze; sulfate aerosol. Schlüsselwörter: Vog; vulkanischer Smog; Schwefeldioxidfahne; …

[Knowledge:190 hazards:Hazard_Surface_Rupture_Fissuring Surface Rupture / Fissuring] HAZARD_ID: hazards:Hazard_Surface_Rupture_Fissuring
LABEL: Surface Rupture / Fissuring
GROUP: Geophysical
SUBTYPE: Mass Movement
ALIASES: fault surface rupture; permanent ground displacement; fissures/cracking; near-fault zone; infrastructure severance; pipeline/road offset; differential settlement; post-event ground hazard; land-use setbacks; Oberflächenbruch entlang Störung; bleibender Bodenversatz; Bodenrisse/Fissuren; störungsnahe Zone; Durchtrennung von Infrastruktur; Versatz an Pipelines/Straßen; differentielle Setzung; Bodenrisiko nach Ereignis; Bauabstände/Schutzzonen
BM25_TEXT_EN: Caused by hazard(s): Landslide. Keywords: fault surface rupture; permanent ground displacement; fissures/cracking; near-fault zone; infrastructure severance; pipeline/road offset; differential settlement; post-event ground hazard; land-use setbacks. Schlüsselwörter: Oberflächenbruch entlang Störung; bleibender Bodenversatz; Bodenrisse/Fissuren; störungsnahe Zone; Durchtrennung von Infrastruktur; Versatz an Pipelines/Straßen; differentielle Setzung; Bodenrisiko nach Ereignis; Bauabstände/Schutzzonen. Sources: https://www.undrr.org/understanding-disaster-risk/terminology/hips/gh0311 | USGS Surface …

[Knowledge:209 hazards:Hazard_War_Of_National_Liberation War Of National Liberation] HAZARD_ID: hazards:Hazard_War_Of_National_Liberation
LABEL: War Of National Liberation
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: anti-colonial war, self-determination conflict; nationaler Befreiungskrieg, antikolonialer Krieg, Selbstbestimmung
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: anti-colonial war, self-determination conflict. Schlüsselwörter: nationaler Befreiungskrieg, antikolonialer Krieg, Selbstbestimmung. Sources: https://en.wikipedia.org/wiki/War_of_national_liberation | UCDP Georeferenced Event Dataset (GED) | https://ucdp.uu.se/downloads/. Sample data: id,date_start,date_end,country,latitude,longitude,type_of_violence,side_a,side_b,best
3221001,2023-10-07,2023-10-07,Israel,31.78,34.76,1,Government of Israel,Hamas,1200
3221002,2023-10-08,2023-10-08,Israel,31.50,34.45,1,Government of Israel,Hamas,100

Source description: Event-level dataset on organized violence with date, location, actors, conflict type, and best-estimate fatalities; downloadable as CSV/Excel..
VERBALIZED_EN: Caused by hazard(s): Terrorism. Keywords: anti-colonial war, self-determination conflict. Schlüsselwörter: nationaler Befreiungskrieg, antikolonialer Krieg, …

[Knowledge:103 hazards:Hazard_Land_Fire_Brush_Bush_Pasture Land Fire (Brush, Bush, Pasture)] HAZARD_ID: hazards:Hazard_Land_Fire_Brush_Bush_Pasture
LABEL: Land Fire (Brush, Bush, Pasture)
GROUP: Climatological
SUBTYPE: Wildfire
ALIASES: land fire; brush; bush; pasture; Flächenbrand (Busch/Weide)
BM25_TEXT_EN: Caused by hazard(s): Wildfire. Keywords: land fire; brush; bush; pasture. Schlüsselwörter: Flächenbrand (Busch/Weide). Sources: https://en.wikipedia.org/wiki/Land_fire_%28Brush%2C_Bush%2C_Pasture%29 | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-121.456,2024-07-15,2030,N,nominal,12.5
37.130,-121.470,2024-07-15,2036,N,high,35.1

Source description: Near-real-time and archived satellite active fire/hotspot detections with location, acquisition time, brightness, and FRP; downloadable as CSV..
VERBALIZED_EN: Caused by hazard(s): Wildfire. Keywords: land fire; brush; bush; pasture. Schlüsselwörter: Flächenbrand (Busch/Weide). Sources: https://en.wikipedia.org/wiki/Land_fire_%28Brush%2C_Bush%2C_Pasture%29 | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: …

[Knowledge:18 hazards:Hazard_Biodiversity_Loss Biodiversity Loss] HAZARD_ID: hazards:Hazard_Biodiversity_Loss
LABEL: Biodiversity Loss
GROUP: Environmental
SUBTYPE: Environmental Degradation
ALIASES: species decline; local/global extinctions; habitat loss/fragmentation; ecosystem degradation; reduced ecosystem services; invasive species; overexploitation; pollution/climate drivers; tipping points; Biodiversitätsverlust; Artenrückgang; lokale/globale Aussterbeereignisse; Habitatverlust/-fragmentierung; Ökosystemdegradation; Rückgang von Ökosystemleistungen; invasive Arten; Übernutzung; Treiber: Verschmutzung/Klimawandel; Kipppunkte
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: species decline; local/global extinctions; habitat loss/fragmentation; ecosystem degradation; reduced ecosystem services; invasive species; overexploitation; pollution/climate drivers; tipping points. Schlüsselwörter: Biodiversitätsverlust; Artenrückgang; lokale/globale Aussterbeereignisse; Habitatverlust/-fragmentierung; Ökosystemdegradation; Rückgang von Ökosystemleistungen; invasive Arten; Übernutzung; Treiber: Verschmutzung/Klimawandel; Kipppunkte. Sources: GBIF Occurrence API | https://techdocs.gbif.org/en/openapi/v1/occurrence ; GBIF API downloads | …

[Knowledge:93 hazards:Hazard_Infestation Infestation] HAZARD_ID: hazards:Hazard_Infestation
LABEL: Infestation
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: infestation; pest outbreak; invasive species; locust swarm; Befall; Schädlingsausbruch; invasive Arten; Heuschreckenschwarm
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: infestation; pest outbreak; invasive species; locust swarm. Schlüsselwörter: Befall; Schädlingsausbruch; invasive Arten; Heuschreckenschwarm. Sources: https://en.wikipedia.org/wiki/Infestation | GBIF Occurrence API | https://techdocs.gbif.org/en/openapi/v1/occurrence. Sample data: key,eventDate,country,decimalLatitude,decimalLongitude,scientificName,basisOfRecord
4012345678,2025-06-12,Italy,45.464,9.190,"Tuta absoluta",HUMAN_OBSERVATION
4012345699,2025-06-15,Spain,41.385,2.173,"Aedes albopictus",HUMAN_OBSERVATION
4012345720,2025-06-18,Germany,52.520,13.405,"Agrilus planipennis",HUMAN_OBSERVATION

Source description: Example occurrence records (GBIF) for pest/invasive species as a general infestation proxy: each row is an observation with date, location, and taxon.
Source: GBIF Occurrence API | https://techdocs.gbif.org/en/openapi/v1/occurrence.
VERBALIZED_EN: Caused by hazard(s): Zoonotic …

[Knowledge:159 hazards:Hazard_Saltwater_Intrusion Saltwater Intrusion] HAZARD_ID: hazards:Hazard_Saltwater_Intrusion
LABEL: Saltwater Intrusion
GROUP: Hydrological
SUBTYPE: Environmental Degradation
ALIASES: seawater encroachment; coastal aquifer; groundwater overpumping; reduced freshwater head; well salinization; irrigation impact; drinking-water contamination; sea-level rise linkage; barrier management; Salzwasserintrusion (auch: Salzwassereinbruch); Meerwassereinbruch in Aquifere; Küstengrundwasserleiter; Übernutzung/Überpumpung; verminderter Süßwasserdruck; Versalzung von Brunnen; Auswirkungen auf Bewässerung; Kontamination des Trinkwassers; Verknüpfung mit Meeresspiegelanstieg; Management (Barrieren/Sperrbrunnen) (Begriffe variieren)
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: seawater encroachment; coastal aquifer; groundwater overpumping; reduced freshwater head; well salinization; irrigation impact; drinking-water contamination; sea-level rise linkage; barrier management. Schlüsselwörter: Salzwasserintrusion (auch: Salzwassereinbruch); Meerwassereinbruch in Aquifere; Küstengrundwasserleiter; Übernutzung/Überpumpung; verminderter Süßwasserdruck; Versalzung von Brunnen; Auswirkungen auf Bewässerung; Kontamination des …

[Knowledge:9 hazards:Hazard_Ash_Resuspension_Event Ash resuspension event] HAZARD_ID: hazards:Hazard_Ash_Resuspension_Event
LABEL: Ash resuspension event
GROUP: Geophysical
SUBTYPE: Visibility
ALIASES: resuspended ash; ash remobilization; windblown ash; ash haze; secondary ashfall; aufgewirbelte Asche; Asche-Remobilisierung; windverfrachtete Asche; Aschedunst; sekundärer Ascheniederschlag
BM25_TEXT_EN: Caused by hazard(s): Storm|hazards:hazard volcanic activity. Keywords: resuspended ash; ash remobilization; windblown ash; ash haze; secondary ashfall. Schlüsselwörter: aufgewirbelte Asche; Asche-Remobilisierung; windverfrachtete Asche; Aschedunst; sekundärer Ascheniederschlag. Sources: https://en.wikipedia.org/wiki/Volcanic_ash | Copernicus CAMS Global Reanalysis (EAC4) | https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4. Sample data: time_utc,lat,lon,dust_aod_550,total_aod_550,so2_kg_m2
2024-02-18T12:00Z,28.0,-15.0,0.65,0.80,0.00002
2024-02-18T12:00Z,30.0,-10.0,0.58,0.72,0.00001

Source description: Atmospheric composition reanalysis including aerosols (e.g., dust AOD) useful for sand/dust storms, Saharan dust and vog dispersion analyses..
VERBALIZED_EN: Caused by hazard(s): Storm|hazards:hazard volcanic activity. Keywords: …

[Knowledge:90 hazards:Hazard_Industrial_Explosion Industrial Explosion] HAZARD_ID: hazards:Hazard_Industrial_Explosion
LABEL: Industrial Explosion
GROUP: Chemical
SUBTYPE: Industrial Incident
ALIASES: industrial explosion; plant explosion; blast; refinery explosion; Industrieexplosion; Anlagenexplosion; Explosion; Raffinerieexplosion
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Keywords: industrial explosion; plant explosion; blast; refinery explosion. Schlüsselwörter: Industrieexplosion; Anlagenexplosion; Explosion; Raffinerieexplosion. Sources: https://en.wikipedia.org/wiki/Explosion | https://www.csb.gov/investigations/. Sample data: csb_case,incident_date,location,industry,incident_type,materials,workers_killed,workers_injured,public_injured
CSB-INV-2025-01,2025-10-10,McEwen TN,Explosives manufacturing,Explosion,Explosive compounds,1,0,0
CSB-INV-2023-07,2023-03-23,Baytown TX,Petrochemical,Explosion/Fire,Hydrocarbons,0,4,0

Source description: Investigation-level incident metadata for major industrial chemical incidents (often explosions and fires), including location, industry sector, materials involved, and casualty counts.
Source: U.S. Chemical Safety Board (CSB) Investigations | …

[Knowledge:158 hazards:Hazard_Saharan_Dust Saharan dust] HAZARD_ID: hazards:Hazard_Saharan_Dust
LABEL: Saharan dust
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: Saharan dust; dust transport; calima; transboundary dust; dust haze; Saharastaub; Staubtransport; Calima; Ferntransportstaub; Dunst/Staubdunst
BM25_TEXT_EN: Caused by hazard(s): Sand dust storm. Keywords: Saharan dust; dust transport; calima; transboundary dust; dust haze. Schlüsselwörter: Saharastaub; Staubtransport; Calima; Ferntransportstaub; Dunst/Staubdunst. Sources: https://en.wikipedia.org/wiki/Saharan_dust | Copernicus CAMS Global Reanalysis (EAC4) | https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4. Sample data: time_utc,lat,lon,dust_aod_550,total_aod_550,so2_kg_m2
2024-02-18T12:00Z,28.0,-15.0,0.65,0.80,0.00002
2024-02-18T12:00Z,30.0,-10.0,0.58,0.72,0.00001

Source description: Atmospheric composition reanalysis including aerosols (e.g., dust AOD) useful for sand/dust storms, Saharan dust and vog dispersion analyses..
VERBALIZED_EN: Caused by hazard(s): Sand dust storm. Keywords: Saharan dust; dust transport; calima; transboundary dust; dust haze. Schlüsselwörter: Saharastaub; Staubtransport; Calima; Ferntransportstaub; Dunst/Staubdunst. …

[Knowledge:79 hazards:Hazard_Haboob Haboob] HAZARD_ID: hazards:Hazard_Haboob
LABEL: Haboob
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: haboob; dust wall; dust storm front; thunderstorm outflow; sandstorm wall; Haboob; Staubwand; Staubsturmfront; Gewitterböenfront; Sandsturmwand
BM25_TEXT_EN: Caused by hazard(s): Sand dust storm. Keywords: haboob; dust wall; dust storm front; thunderstorm outflow; sandstorm wall. Schlüsselwörter: Haboob; Staubwand; Staubsturmfront; Gewitterböenfront; Sandsturmwand. Sources: https://en.m.wikipedia.org/wiki/Haboob | Copernicus CAMS Global Reanalysis (EAC4) | https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4. Sample data: time_utc,lat,lon,dust_aod_550,total_aod_550,so2_kg_m2
2024-02-18T12:00Z,28.0,-15.0,0.65,0.80,0.00002
2024-02-18T12:00Z,30.0,-10.0,0.58,0.72,0.00001

Source description: Atmospheric composition reanalysis including aerosols (e.g., dust AOD) useful for sand/dust storms, Saharan dust and vog dispersion analyses..
VERBALIZED_EN: Caused by hazard(s): Sand dust storm. Keywords: haboob; dust wall; dust storm front; thunderstorm outflow; sandstorm wall. Schlüsselwörter: Haboob; Staubwand; Staubsturmfront; Gewitterböenfront; Sandsturmwand. Sources: …

[Knowledge:85 hazards:Hazard_ICT_Outage_Impacting_Forecasting_Alerts ICT Outage Impacting Forecasting/Alerts] HAZARD_ID: hazards:Hazard_ICT_Outage_Impacting_Forecasting_Alerts
LABEL: ICT Outage Impacting Forecasting/Alerts
GROUP: Digital
SUBTYPE: Cyber Incident
ALIASES: ICT outage; forecasting disruption; alerting failure; communication outage; IKT-Ausfall; Störung der Wettervorhersage; Warnsystemausfall; Kommunikationsausfall
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: ICT outage; forecasting disruption; alerting failure; communication outage. Schlüsselwörter: IKT-Ausfall; Störung der Wettervorhersage; Warnsystemausfall; Kommunikationsausfall. Sources: Wikipedia | https://en.wikipedia.org/wiki/Information_and_communications_technology | RIPE Atlas Measurement Results | https://www.ripe.net/analyse/internet-measurements/ripe-atlas/. Sample data: ts_utc,probe_id,measurement_type,target,success,response_time_ms,error
2025-08-12T15:05:00Z,88421,http,https://alerts.example/cap.xml,0,NA,"timeout"
2025-08-12T15:10:00Z,88421,dns,api.weather.example,0,NA,"SERVFAIL"
2025-08-12T15:15:00Z,88421,http,https://api.weather.example/v1/forecast,1,842,""

Source description: Synthetic monitoring / measurement rows (HTTP/DNS/ping) to alerting and forecasting endpoints; captures outages that …

[Knowledge:147 hazards:Hazard_Pyrocumulus Pyrocumulus] HAZARD_ID: hazards:Hazard_Pyrocumulus
LABEL: Pyrocumulus
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: pyrocumulus; fire cloud; smoke plume; convection column; wildfire smoke; Pyrocumulus; Feuerwolke; Rauchfahne; Konvektionssäule; Waldbrandrauch
BM25_TEXT_EN: Caused by hazard(s): Storm|hazards:hazard wildfire. Keywords: pyrocumulus; fire cloud; smoke plume; convection column; wildfire smoke. Schlüsselwörter: Pyrocumulus; Feuerwolke; Rauchfahne; Konvektionssäule; Waldbrandrauch. Sources: https://en.wikipedia.org/wiki/Pyrocumulus | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-121.456,2024-07-15,2030,N,nominal,12.5
37.130,-121.470,2024-07-15,2036,N,high,35.1

Source description: Near-real-time and archived satellite active fire/hotspot detections with location, acquisition time, brightness, and FRP; downloadable as CSV..
VERBALIZED_EN: Caused by hazard(s): Storm|hazards:hazard wildfire. Keywords: pyrocumulus; fire cloud; smoke plume; convection column; wildfire smoke. Schlüsselwörter: Pyrocumulus; Feuerwolke; Rauchfahne; Konvektionssäule; …

[Knowledge:68 hazards:Hazard_Forest_Fire Forest Fire] HAZARD_ID: hazards:Hazard_Forest_Fire
LABEL: Forest Fire
GROUP: Climatological
SUBTYPE: Wildfire
ALIASES: forest fire; Waldbrand
BM25_TEXT_EN: Caused by hazard(s): Wildfire. Keywords: forest fire. Schlüsselwörter: Waldbrand. Sources: https://en.wikipedia.org/wiki/Forest_fire | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-121.456,2024-07-15,2030,N,nominal,12.5
37.130,-121.470,2024-07-15,2036,N,high,35.1

Source description: Near-real-time and archived satellite active fire/hotspot detections with location, acquisition time, brightness, and FRP; downloadable as CSV..
VERBALIZED_EN: Caused by hazard(s): Wildfire. Keywords: forest fire. Schlüsselwörter: Waldbrand. Sources: https://en.wikipedia.org/wiki/Forest_fire | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-121.456,2024-07-15,2030,N,nominal,12.5
37.130,-121.470,2024-07-15,2036,N,high,35.1

Source description: Near-real-time and archived satellite active fire/hotspot detections …

[Knowledge:200 hazards:Hazard_Urban_Fire_Major Urban Fire (Major)] HAZARD_ID: hazards:Hazard_Urban_Fire_Major
LABEL: Urban Fire (Major)
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: urban fire; major fire; conflagration; city fire; Stadtbrand; Großbrand; Feuersbrunst
BM25_TEXT_EN: Caused by hazard(s): Wildfire. Keywords: urban fire; major fire; conflagration; city fire. Schlüsselwörter: Stadtbrand; Großbrand; Feuersbrunst. Sources: https://en.wikipedia.org/wiki/Urban_fire | https://www.usfa.fema.gov/statistics/data-sets/. Sample data: incident_number,incident_date,city,state,property_use,area_of_origin,heat_source,fire_cause,estimated_loss_usd
2019123456,2019-07-04,Los Angeles,CA,1-2 family dwelling,Kitchen,Range top,Unattended cooking,85000
2020109876,2020-12-12,Chicago,IL,High-rise apartment,Bedroom,Smoking materials,Cigarette,420000

Source description: National Fire Incident Reporting System (NFIRS) public release data: structured fire incident records reported by fire departments, including property type, origin, cause, and losses.
Source: USFA NFIRS Public Data Release | https://www.usfa.fema.gov/statistics/data-sets/.
VERBALIZED_EN: Caused by hazard(s): Wildfire. Keywords: urban fire; major fire; conflagration; …

[Knowledge:65 hazards:Hazard_Flood_General Flood (General)] HAZARD_ID: hazards:Hazard_Flood_General
LABEL: Flood (General)
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: flood (general); Hochwasser
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: flood (general). Schlüsselwörter: Hochwasser. Sources: Wikipedia | https://en.wikipedia.org/wiki/Flood | Dartmouth Flood Observatory – Global Active Archive of Large Flood Events | https://data.humdata.org/dataset/global-active-archive-of-large-flood-events-dfo | NOAA NCEI Storm Events Database | https://www.ncei.noaa.gov/stormevents/. Sample data: dfo_id,country,region,event_start,event_end,main_cause,deaths,displaced,affected_area_km2
DFO-2024-001,India,Assam,2024-06-15,2024-07-02,Monsoon,52,300000,18500
DFO-2023-217,Brazil,Rio Grande do Sul,2023-09-04,2023-09-12,Heavy Rain,34,12000,6200

Source description: Global event-level large-flood archive (cause, impacts, dates, and rough spatial footprint) suitable as a generalized flood event dataset.
Source: Dartmouth Flood Observatory (DFO) – Global Active Archive | https://data.humdata.org/dataset/global-active-archive-of-large-flood-events-dfo.
VERBALIZED_EN: Caused by hazard(s): Atmospheric river extreme …

[Knowledge:149 hazards:Hazard_Radio_Jamming Radio jamming] HAZARD_ID: hazards:Hazard_Radio_Jamming
LABEL: Radio jamming
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: radio jamming, intentional interference, RF jamming, signal jammer, communications disruption, harmful interference, spectrum disruption, VHF interference, UHF interference, HF interference, amateur radio, ham radio, public safety radio, LMR disruption, TETRA interference, Wi-Fi jamming, Bluetooth jamming, SATCOM jamming, link loss, no service, dropped calls; Funkstörung, absichtliche Störung, HF-Störung, Funk-Jammer, Kommunikationsstörung, schädliche Störung, Spektrumstörung, VHF-Störung, UHF-Störung, Kurzwellenstörung, Amateurfunk, BOS-Funk, Einsatzfunk, TETRA-Störung, WLAN-Jamming, Bluetooth-Störung, SATCOM-Jamming, Link-Verlust, kein Empfang, Verbindungsabbrüche
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism|hazards:hazard war. Keywords: radio jamming, intentional interference, RF jamming, signal jammer, communications disruption, harmful interference, spectrum disruption, VHF interference, UHF interference, HF interference, amateur radio, ham radio, public safety radio, LMR disruption, TETRA interference, Wi-Fi jamming, Bluetooth jamming, …

[Knowledge:211 hazards:Hazard_Water_Pollution Water pollution] HAZARD_ID: hazards:Hazard_Water_Pollution
LABEL: Water pollution
GROUP: Chemical
SUBTYPE: Outbreak
ALIASES: water pollution, contaminated water, water contamination, sewage spill, wastewater, pathogens, bacteria, viruses, waterborne disease, drinking water contamination, boil water advisory, gastroenteritis outbreak; Wasserverschmutzung, Wasserverunreinigung, kontaminiertes Wasser, Abwasseraustritt, Abwasser, Krankheitserreger, Bakterien, Viren, wasserbedingte Krankheit, Trinkwasserverunreinigung, Abkochgebot, Magen-Darm-Ausbruch
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure|hazards:hazard wastewater system failure|hazards:hazard environmental pollution. Keywords: water pollution, contaminated water, water contamination, sewage spill, wastewater, pathogens, bacteria, viruses, waterborne disease, drinking water contamination, boil water advisory, gastroenteritis outbreak. Schlüsselwörter: Wasserverschmutzung, Wasserverunreinigung, kontaminiertes Wasser, Abwasseraustritt, Abwasser, Krankheitserreger, Bakterien, Viren, wasserbedingte Krankheit, Trinkwasserverunreinigung, Abkochgebot, Magen-Darm-Ausbruch. Sources: …

[Knowledge:53 hazards:Hazard_Environmental_Pollution Environmental pollution] HAZARD_ID: hazards:Hazard_Environmental_Pollution
LABEL: Environmental pollution
GROUP: Environmental
SUBTYPE: Pollution (environmental contamination)
ALIASES: pollution, environmental contamination, toxic substances, air pollution, water pollution, soil pollution, hazardous emissions; Umweltverschmutzung, Umweltbelastung, Schadstoffe, Luftverschmutzung, Wasserverschmutzung, Bodenverschmutzung, Emissionen
BM25_TEXT_EN: Caused by hazard(s): Chronic pollution tipping event|hazards:hazard industrial explosion|hazards:hazard critical infrastructure failure. Keywords: pollution, environmental contamination, toxic substances, air pollution, water pollution, soil pollution, hazardous emissions. Schlüsselwörter: Umweltverschmutzung, Umweltbelastung, Schadstoffe, Luftverschmutzung, Wasserverschmutzung, Bodenverschmutzung, Emissionen. Sources: https://en.wikipedia.org/wiki/Pollution | Water Quality Portal Web Services | https://www.waterqualitydata.us/webservices_documentation/ | Water Quality Portal | https://www.waterqualitydata.us/. Sample data: …

[Knowledge:201 hazards:Hazard_Vector_Borne_Outbreak Vector-borne Outbreak] HAZARD_ID: hazards:Hazard_Vector_Borne_Outbreak
LABEL: Vector-borne Outbreak
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: vector-borne disease; mosquito-borne; tick-borne; outbreak; Vektorübertragene Krankheit; mückenübertragen; zeckenübertragen; Ausbruch
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: vector-borne disease; mosquito-borne; tick-borne; outbreak. Schlüsselwörter: Vektorübertragene Krankheit; mückenübertragen; zeckenübertragen; Ausbruch. Sources: https://en.wikipedia.org/wiki/Vector-borne_disease | WHO GHO OData API | https://www.who.int/data/gho/info/gho-odata-api | WHO Malaria cases indicator group | https://www.who.int/data/gho/data/themes/topics/indicator-groups/indicator-group-details/GHO/malaria-cases. Sample data: disease,country,year,cases_estimated,incidence_per_1000_at_risk,deaths_estimated
Malaria,Nigeria,2024,68000000,260.4,170000
Malaria,India,2024,6500000,4.6,7300
Dengue,Brazil,2023,2100000,9.9,1200

Source description: Vector-borne disease burden rows (country-year) in the style of WHO indicator datasets (cases/incidence/deaths).
Source: WHO GHO OData API | https://www.who.int/data/gho/info/gho-odata-api | WHO Malaria cases indicator …

[Knowledge:196 hazards:Hazard_Tsunami Tsunami] HAZARD_ID: hazards:Hazard_Tsunami
LABEL: Tsunami
GROUP: Geophysical
SUBTYPE: Tsunami
ALIASES: tsunami; seismic sea wave; tsunami run-up; coastal inundation; Tsunami; Flutwelle; Küstenüberflutung
BM25_TEXT_EN: Caused by hazard(s): Earthquake. Keywords: tsunami; seismic sea wave; tsunami run-up; coastal inundation. Schlüsselwörter: Tsunami; Flutwelle; Küstenüberflutung. Sources: https://en.wikipedia.org/wiki/Tsunami | NOAA NCEI Global Historical Tsunami Database (HazEL) | https://www.ncei.noaa.gov/products/natural-hazards/tsunamis-earthquakes-volcanoes/tsunamis. Sample data: year,mo,dy,latitude,longitude,cause,max_height_m,deaths,country
2004,12,26,3.316,95.854,Earthquake,51,227898,Indonesia
2011,3,11,38.297,142.372,Earthquake,40.5,19900,Japan

Source description: Global historical tsunami event and run-up data with source parameters, maximum wave heights, and impacts; searchable/downloadable via HazEL..
VERBALIZED_EN: Caused by hazard(s): Earthquake. Keywords: tsunami; seismic sea wave; tsunami run-up; coastal inundation. Schlüsselwörter: Tsunami; Flutwelle; Küstenüberflutung. Sources: https://en.wikipedia.org/wiki/Tsunami | NOAA NCEI Global Historical Tsunami Database (HazEL) | …

[Knowledge:37 hazards:Hazard_Critical_Infrastructure_Failure Critical Infrastructure Failure] HAZARD_ID: hazards:Hazard_Critical_Infrastructure_Failure
LABEL: Critical Infrastructure Failure
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: infrastructure outage; Infrastrukturausfall
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: infrastructure outage. Schlüsselwörter: Infrastrukturausfall. Sources: https://en.wikipedia.org/wiki/Critical_infrastructure | https://www.oe.netl.doe.gov/OE417_annual_summary.aspx. Sample data: oe417_id,incident_start_utc,event_type,states_affected,customers_affected,major_system_impacts
OE417-2024-0156,2024-01-13T03:20Z,Transmission outage,"TX,LA",210000,Yes
OE417-2025-0091,2025-08-22T14:05Z,Severe weather,"FL",450000,Yes

Source description: Event-level reports of major electric grid incidents/disturbances (DOE Form OE-417) including timing, location, customer impacts, and system effects; can be used as a general critical-infrastructure failure dataset.
Source: U.S. DOE OE-417 Electric Emergency Incident and Disturbance Reports | https://www.oe.netl.doe.gov/OE417_annual_summary.aspx.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: infrastructure outage. Schlüsselwörter: Infrastrukturausfall. …

[Knowledge:162 hazards:Hazard_Sea_Smoke_Steam_Fog Sea smoke (steam fog)] HAZARD_ID: hazards:Hazard_Sea_Smoke_Steam_Fog
LABEL: Sea smoke (steam fog)
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: steam fog; sea smoke; arctic sea smoke; evaporation fog; sea smoke over water; Seenebel; Meeresrauch; arktischer Seenebel; Verdunstungsnebel
BM25_TEXT_EN: Caused by hazard(s): Fog. Keywords: steam fog; sea smoke; arctic sea smoke; evaporation fog; sea smoke over water. Schlüsselwörter: Seenebel; Meeresrauch; arktischer Seenebel; Verdunstungsnebel. Sources: https://en.wikipedia.org/wiki/Steam_fog | NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database. Sample data: station,datetime_utc,air_temp_c,dewpoint_c,wind_speed_m_s,visibility_m,present_weather
LSZH,2024-12-10T05:50Z,-1.0,-1.2,2.0,200,FG
LSZH,2024-12-10T06:20Z,-1.0,-1.2,2.5,300,FG

Source description: Hourly and synoptic surface observations (METAR/ASOS etc.) with present weather codes suitable for fog, sea smoke, snow, and other visibility-related hazards..
VERBALIZED_EN: Caused by hazard(s): Fog. Keywords: steam fog; sea smoke; arctic sea smoke; evaporation fog; sea smoke over water. Schlüsselwörter: Seenebel; …

[Knowledge:181 hazards:Hazard_Structural_Collapse Structural Collapse] HAZARD_ID: hazards:Hazard_Structural_Collapse
LABEL: Structural Collapse
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: structural collapse; building failure; bridge collapse; progressive collapse; Gebäudeeinsturz; Strukturversagen; Brückeneinsturz; progressiver Kollaps
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: structural collapse; building failure; bridge collapse; progressive collapse. Schlüsselwörter: Gebäudeeinsturz; Strukturversagen; Brückeneinsturz; progressiver Kollaps. Sources: https://en.wikipedia.org/wiki/Structural_failure | https://catalog.data.gov/dataset/construction-related-incidents. Sample data: incident_id,incident_date,borough,incident_type,building_class,injured_count,fatality_count,description
DOB-2024-000123,2024-04-07,MANHATTAN,Collapse,Residential,2,0,"Partial wall collapse during renovation"
DOB-2023-001987,2023-11-19,BROOKLYN,Collapse,Commercial,0,1,"Scaffold/structure collapse"

Source description: Municipal incident reports for construction-related events (including partial/total collapses) with structured fields on location, type, and casualties.
Source: NYC DOB Construction-Related Incidents | …

[Knowledge:187 hazards:Hazard_Superbolts Superbolts] HAZARD_ID: hazards:Hazard_Superbolts
LABEL: Superbolts
GROUP: Meteorological
SUBTYPE: Lightning
ALIASES: superbolt; extreme lightning; high-energy lightning; powerful lightning; lightning flash; thunderstorm; atmospheric electricity; Superblitz; extrem starker Blitz; hochenergetischer Blitz; starker Blitz; Blitzentladung; Gewitter; atmosphärische Elektrizität
BM25_TEXT_EN: Caused by hazard(s): Lightning. Keywords: superbolt; extreme lightning; high-energy lightning; powerful lightning; lightning flash; thunderstorm; atmospheric electricity. Schlüsselwörter: Superblitz; extrem starker Blitz; hochenergetischer Blitz; starker Blitz; Blitzentladung; Gewitter; atmosphärische Elektrizität. Sources: https://en.wikipedia.org/wiki/Superbolt | https://registry.opendata.aws/noaa-goes/. Sample data: flash_id,flash_time_utc,flash_lat,flash_lon,flash_energy_j,is_superbolt_candidate
F987654321,2024-10-28T03:11:22Z,12.44,-61.08,1.2e7,Yes
F987654322,2024-10-28T03:11:24Z,12.47,-61.05,9.8e6,Yes

Source description: GLM flash detections with optical energy; “superbolt” candidates can be defined by unusually high optical energy thresholds (research definitions vary), enabling extraction of …

[Knowledge:118 hazards:Hazard_Major_Road_Disaster Major Road Disaster] HAZARD_ID: hazards:Hazard_Major_Road_Disaster
LABEL: Major Road Disaster
GROUP: Transportation
SUBTYPE: Transport Incident
ALIASES: road accident; mass casualty crash; pile-up; Schwerer Verkehrsunfall; Massenkarambolage; Unfall mit vielen Opfern
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: road accident; mass casualty crash; pile-up. Schlüsselwörter: Schwerer Verkehrsunfall; Massenkarambolage; Unfall mit vielen Opfern. Sources: https://en.wikipedia.org/wiki/Traffic_collision | NHTSA Fatality Analysis Reporting System (FARS) | https://www.nhtsa.gov/research-data/fatality-analysis-reporting-system-fars. Sample data: state,st_case,year,month,day,hour,latitude,longitude,persons,killed
6,12345,2023,7,4,22,34.052,-118.244,3,2
36,54321,2023,12,15,7,40.712,-74.006,1,1

Source description: Census of U.S. fatal traffic crashes with crash circumstances, vehicles, and persons; downloadable yearly files..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: road accident; mass casualty crash; pile-up. Schlüsselwörter: Schwerer Verkehrsunfall; Massenkarambolage; Unfall mit vielen Opfern. Sources: https://en.wikipedia.org/wiki/Traffic_collision | NHTSA Fatality Analysis Reporting System …

[Knowledge:81 hazards:Hazard_Hazmat_Transport_Incident HazMat Transport Incident] HAZARD_ID: hazards:Hazard_Hazmat_Transport_Incident
LABEL: HazMat Transport Incident
GROUP: Chemical
SUBTYPE: Transport Incident
ALIASES: hazmat transport; dangerous goods accident; tanker spill; Gefahrguttransport; Unfall mit Gefahrgut; Tankerunfall
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Keywords: hazmat transport; dangerous goods accident; tanker spill. Schlüsselwörter: Gefahrguttransport; Unfall mit Gefahrgut; Tankerunfall. Sources: https://en.wikipedia.org/wiki/Hazardous_materials | PHMSA Hazardous Materials Incident Statistics (5800.1) | https://www.phmsa.dot.gov/hazmat-program-management-data-and-statistics/data-operations/incident-statistics. Sample data: report_year,incident_date,mode,packaging_type,material_name,quantity_released,injuries,fatalities,state
2023,2023-05-14,Highway,Cylinder,Anhydrous Ammonia,120,2,0,TX
2023,2023-09-02,Rail,Tank Car,Petroleum Crude Oil,50000,0,0,ND

Source description: Reported U.S. hazardous materials transportation incidents (DOT Form 5800.1) with mode, material, location, consequences; downloadable reports/data..
VERBALIZED_EN: Caused by hazard(s): Industrial …

[Knowledge:108 hazards:Hazard_Large_Scale_Disinformation_Disrupting_Emergency_Response Large-scale Disinformation Disrupting Emergency Response] HAZARD_ID: hazards:Hazard_Large_Scale_Disinformation_Disrupting_Emergency_Response
LABEL: Large-scale Disinformation Disrupting Emergency Response
GROUP: Black Swan
SUBTYPE: Cyber Incident
ALIASES: disinformation; misinformation; crisis communication; emergency management failure; Desinformation; Falschinformation; Krisenkommunikation; Versagen des Katastrophenschutzes
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: disinformation; misinformation; crisis communication; emergency management failure. Schlüsselwörter: Desinformation; Falschinformation; Krisenkommunikation; Versagen des Katastrophenschutzes. Sources: Wikipedia | https://en.wikipedia.org/wiki/Disinformation | EUvsDisinfo Disinformation Cases | https://euvsdisinfo.eu/disinformation-cases/. Sample data: case_id,date,country,crisis_type,claim,channel,engagement_proxy,emergency_response_impact_note
EUDIS-9001,2025-07-18,CountryX,wildfire,"False evacuation route info","social+blogs",0.78,"Call center overloaded; rerouting confusion reported"
EUDIS-9002,2025-09-02,CountryY,flood,"False shelter location list","messaging apps",0.64,"Misdirected evacuees; delayed assistance"

Source description: Crisis-related …

[Knowledge:54 hazards:Hazard_Epidemic Epidemic] HAZARD_ID: hazards:Hazard_Epidemic
LABEL: Epidemic
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: epidemic; outbreak; infectious disease spread; Epidemie; Ausbruch; Ausbreitung von Infektionskrankheiten
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: epidemic; outbreak; infectious disease spread. Schlüsselwörter: Epidemie; Ausbruch; Ausbreitung von Infektionskrankheiten. Sources: https://en.wikipedia.org/wiki/Epidemic | CDC NNDSS Weekly Data | https://data.cdc.gov/NNDSS/NNDSS-Weekly-Data/x9gk-5huc | CDC NNDSS weekly tables info | https://www.cdc.gov/nndss/infectious-disease/weekly-and-annual-disease-data-tables.html. Sample data: mmwr_year,mmwr_week,condition,reporting_area,case_count
2025,40,Measles,California,3
2025,40,Measles,Texas,1
2025,40,Meningococcal disease,Florida,2

Source description: Weekly notifiable disease counts (MMWR year/week) by condition and jurisdiction from CDC NNDSS. Useful for epidemic detection baselines and spikes.
Source: CDC NNDSS Weekly Data | https://data.cdc.gov/NNDSS/NNDSS-Weekly-Data/x9gk-5huc | CDC NNDSS weekly tables info | https://www.cdc.gov/nndss/infectious-disease/weekly-and-annual-disease-data-tables.html.
VERBALIZED_EN: …

[Knowledge:218 hazards:Hazard_Wind_Gust Wind gust] HAZARD_ID: hazards:Hazard_Wind_Gust
LABEL: Wind gust
GROUP: Meteorological
SUBTYPE: Storm
ALIASES: wind gust, strong wind, storm gusts, wind damage; Windböe, Sturmböen, starker Wind, Windschäden
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: wind gust, strong wind, storm gusts, wind damage. Schlüsselwörter: Windböe, Sturmböen, starker Wind, Windschäden. Sources: https://en.wikipedia.org/wiki/Wind_gust | NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database. Sample data: station,datetime_utc,wind_speed_m_s,wind_gust_m_s,wind_dir_deg,air_temp_c
KSFO,2024-01-04T10:56Z,15.4,26.2,280,12.2
KSFO,2024-01-04T11:56Z,14.9,24.7,285,11.8

Source description: Hourly surface observations including wind speed and gusts from METAR/ASOS stations; useful for wind gust extremes.
Source: NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database.
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: wind gust, strong wind, storm gusts, wind damage. Schlüsselwörter: Windböe, Sturmböen, starker Wind, Windschäden. Sources: …

[Knowledge:151 hazards:Hazard_Rail_Disaster Rail Disaster] HAZARD_ID: hazards:Hazard_Rail_Disaster
LABEL: Rail Disaster
GROUP: Transportation
SUBTYPE: Transport Incident
ALIASES: rail accident; train crash; derailment; Eisenbahnunfall; Zugunglück; Entgleisung
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: rail accident; train crash; derailment. Schlüsselwörter: Eisenbahnunfall; Zugunglück; Entgleisung. Sources: https://en.wikipedia.org/wiki/Rail_accident | FRA Rail Equipment Accident/Incident Data (Form 54) | https://data.transportation.gov/Railroads/Rail-Equipment-Accident-Incident-Data-Form-54-/85tf-25kj. Sample data: report_year,accident_month,accident_day,railroad,county,state,total_damage,primary_cause
2023,3,28,BNSF,Cass,ND,125000,Derailment
2023,8,12,UP,Los Angeles,CA,450000,Signal failure

Source description: U.S. rail equipment accident/incident reports with date, railroad, location, damage and causes; downloadable via data.transportation.gov..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: rail accident; train crash; derailment. Schlüsselwörter: Eisenbahnunfall; Zugunglück; Entgleisung. Sources: https://en.wikipedia.org/wiki/Rail_accident | FRA Rail Equipment Accident/Incident Data (Form 54) | …

[Knowledge:42 hazards:Hazard_Dam_Levee_Failure Dam / Levee Failure] HAZARD_ID: hazards:Hazard_Dam_Levee_Failure
LABEL: Dam / Levee Failure
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: dam failure; levee failure; dike breach; embankment failure; Dammbruch; Deichbruch; Dammversagen; Deichversagen
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: dam failure; levee failure; dike breach; embankment failure. Schlüsselwörter: Dammbruch; Deichbruch; Dammversagen; Deichversagen. Sources: https://en.wikipedia.org/wiki/Dam_failure | https://damsafety.org/incidents. Sample data: incident_id,incident_date,structure_type,location,cause,consequence,evacuation,damage_notes
ASDSO-INC-000345,2019-03-16,Dam,NE USA,Overtopping,Near-failure,Yes,"Emergency spillway used; downstream flooding"
ASDSO-INC-000912,2020-05-20,Levee,MI USA,Structural breach,Failure,Yes,"Widespread inundation reported"

Source description: Searchable incident database with exportable tables covering dam and levee failures/near-failures, including causes and downstream consequences.
Source: ASDSO Dam Incident Database | https://damsafety.org/incidents.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: dam failure; levee failure; dike breach; …

[Knowledge:169 hazards:Hazard_Solar_Eclipse Solar eclipse] HAZARD_ID: hazards:Hazard_Solar_Eclipse
LABEL: Solar eclipse
GROUP: Extraterrestrial
SUBTYPE: Visibility
ALIASES: solar eclipse; total lunar eclipse; partial lunar eclipse; penumbral eclipse; “blood moon”; Earth’s shadow; reduced moonlight; night-time darkness; astronomy event; Mondfinsternis; totale Mondfinsternis; partielle Mondfinsternis; Halbschattenfinsternis; Blutmond; Erdschatten; verringerte Mondhelligkeit; nächtliche Dunkelheit; astronomisches Ereignis
BM25_TEXT_EN: Caused by hazard(s): Storm|hazards:hazard space weather solar storm. Keywords: solar eclipse; total lunar eclipse; partial lunar eclipse; penumbral eclipse; “blood moon”; Earth’s shadow; reduced moonlight; night-time darkness; astronomy event. Schlüsselwörter: Mondfinsternis; totale Mondfinsternis; partielle Mondfinsternis; Halbschattenfinsternis; Blutmond; Erdschatten; verringerte Mondhelligkeit; nächtliche Dunkelheit; astronomisches Ereignis. Sources: https://en.wikipedia.org/wiki/Solar_eclipse | NASA GSFC Solar Eclipse Catalog (CSV) | https://eclipse.gsfc.nasa.gov/solar.html. Sample data: …

[Knowledge:128 hazards:Hazard_Miyake_Event Miyake Event] HAZARD_ID: hazards:Hazard_Miyake_Event
LABEL: Miyake Event
GROUP: Extraterrestrial
SUBTYPE: Space Weather
ALIASES: miyake event; Miyake Event
BM25_TEXT_EN: Caused by hazard(s): Space weather solar storm. Keywords: miyake event. Schlüsselwörter: Miyake Event. Sources: https://en.wikipedia.org/wiki/Miyake_event | IntCal Radiocarbon Calibration Curves (IntCal20) | https://intcal.org/curves.html. Sample data: calBP,c14_age,err
1000,  960, 17
995,   955, 17
990,   952, 17

Source description: Radiocarbon calibration curve data (IntCal20) providing calendar age vs 14C age and uncertainty; used as proxy data for cosmogenic isotope anomalies (e.g., Miyake events)..
VERBALIZED_EN: Caused by hazard(s): Space weather solar storm. Keywords: miyake event. Schlüsselwörter: Miyake Event. Sources: https://en.wikipedia.org/wiki/Miyake_event | IntCal Radiocarbon Calibration Curves (IntCal20) | https://intcal.org/curves.html. Sample data: calBP,c14_age,err
1000,  960, 17
995,   955, 17
990,   952, 17

Source description: Radiocarbon calibration curve data (IntCal20) providing calendar age vs 14C age and uncertainty; used as proxy data for cosmogenic isotope anomalies (e.g., Miyake events)..
LINKS: …

[Knowledge:91 hazards:Hazard_Industrial_Fire_Smoke_Plume_Response_Impact Industrial Fire Smoke Plume (Response Impact)] HAZARD_ID: hazards:Hazard_Industrial_Fire_Smoke_Plume_Response_Impact
LABEL: Industrial Fire Smoke Plume (Response Impact)
GROUP: Chemical
SUBTYPE: Industrial Incident
ALIASES: industrial fire; smoke plume; air quality emergency; response disruption; Industriebrand; Rauchfahne; Luftqualitätsnotlage; Beeinträchtigung der Einsatzkräfte
BM25_TEXT_EN: Caused by hazard(s): Wildfire. Keywords: industrial fire; smoke plume; air quality emergency; response disruption. Schlüsselwörter: Industriebrand; Rauchfahne; Luftqualitätsnotlage; Beeinträchtigung der Einsatzkräfte. Sources: https://en.wikipedia.org/wiki/Industrial_fire | https://www.ospo.noaa.gov/products/land/hms.html. Sample data: analysis_date,plume_id,density,area_km2,centroid_lat,centroid_lon,source_type
2025-07-15,SMK-000321,Medium,18450,35.8,-119.6,Industrial fire
2025-07-15,SMK-000322,High,5220,29.7,-95.2,Industrial fire

Source description: Satellite-derived daily smoke-plume polygons/attributes (density, extent) from NOAA HMS; can be used to represent and quantify smoke plumes from large industrial fires and their potential air-quality response impacts.
Source: NOAA Hazard Mapping System (HMS) Smoke Product | …

[Knowledge:15 hazards:Hazard_Aviation_Disaster Aviation Disaster] HAZARD_ID: hazards:Hazard_Aviation_Disaster
LABEL: Aviation Disaster
GROUP: Transportation
SUBTYPE: Transport Incident
ALIASES: aviation accident; plane crash; aircraft disaster; Flugunfall; Flugzeugabsturz; Luftfahrtkatastrophe
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: aviation accident; plane crash; aircraft disaster. Schlüsselwörter: Flugunfall; Flugzeugabsturz; Luftfahrtkatastrophe. Sources: https://en.wikipedia.org/wiki/Aviation_accident_and_incident | NTSB Aviation Accident Data (Census of US Civil Aviation Accidents) | https://www.ntsb.gov/safety/data/Pages/Data_Stats.aspx. Sample data: event_id,event_date,location,aircraft_make,aircraft_model,injury_severity,fatalities
NYC23FA001,2023-01-15,New York,NY,Cessna,172,Fatal,1
LAX24LA123,2024-07-03,Los Angeles,CA,Boeing,737,Non-Fatal,0

Source description: Downloadable NTSB aviation accident/incident dataset with event date, aircraft, injury severity, location, and narrative..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: aviation accident; plane crash; aircraft disaster. Schlüsselwörter: Flugunfall; Flugzeugabsturz; Luftfahrtkatastrophe. Sources: https://en.wikipedia.org/wiki/Aviation_accident_and_incident | …

[Knowledge:121 hazards:Hazard_Maritime_Disaster Maritime Disaster] HAZARD_ID: hazards:Hazard_Maritime_Disaster
LABEL: Maritime Disaster
GROUP: Transportation
SUBTYPE: Transport Incident
ALIASES: maritime accident; shipwreck; sinking; collision; Schiffsunglück; Seenot; Untergang; Kollision
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: maritime accident; shipwreck; sinking; collision. Schlüsselwörter: Schiffsunglück; Seenot; Untergang; Kollision. Sources: https://en.wikipedia.org/wiki/Maritime_disaster | NTSB Aviation Accident Data (Census of US Civil Aviation Accidents) | https://www.ntsb.gov/safety/data/Pages/Data_Stats.aspx. Sample data: event_id,event_date,location,aircraft_make,aircraft_model,injury_severity,fatalities
NYC23FA001,2023-01-15,New York,NY,Cessna,172,Fatal,1
LAX24LA123,2024-07-03,Los Angeles,CA,Boeing,737,Non-Fatal,0

Source description: Downloadable NTSB aviation accident/incident dataset with event date, aircraft, injury severity, location, and narrative..
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: maritime accident; shipwreck; sinking; collision. Schlüsselwörter: Schiffsunglück; Seenot; Untergang; Kollision. Sources: https://en.wikipedia.org/wiki/Maritime_disaster | NTSB Aviation Accident Data (Census of US …

[Knowledge:99 hazards:Hazard_Laboratory_Accident_Bio Laboratory Accident (Bio)] HAZARD_ID: hazards:Hazard_Laboratory_Accident_Bio
LABEL: Laboratory Accident (Bio)
GROUP: Biological
SUBTYPE: Biological Incident
ALIASES: laboratory accident; biosafety incident; lab leak; Laborunfall; Biosicherheitsvorfall; Laborleck
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: laboratory accident; biosafety incident; lab leak. Schlüsselwörter: Laborunfall; Biosicherheitsvorfall; Laborleck. Sources: Wikipedia | https://en.wikipedia.org/wiki/Laboratory_biosafety | Federal Select Agent Program (FSAP) Form 3 | https://www.selectagents.gov/forms/form3.htm. Sample data: report_id,report_type,agent_or_toxin,event_date,release_type,containment_level,ppe_worn,exposure_type,medical_followup,root_cause,corrective_actions
FSAP-00001,Release,Bacillus anthracis,2025-02-10,"Outside primary containment",BSL-3,"Gloves; Eye protection","Potential inhalation",Yes,"Procedure deviation","Revised SOP; fit-testing; refresher training"
FSAP-00002,Loss,Select toxin,2025-07-19,"Inventory discrepancy",BSL-2,"NA",NA,No,"Inventory control failure","Barcode inventory; dual verification"

Source description: Canonical data fields for reporting a select-agent release/loss/theft; usable as …

[Knowledge:152 hazards:Hazard_Riverine_Flood Riverine Flood] HAZARD_ID: hazards:Hazard_Riverine_Flood
LABEL: Riverine Flood
GROUP: Hydrological
SUBTYPE: Flood
ALIASES: river flood; fluvial flooding; overbank flooding; Flusshochwasser; Flusshochwasserereignis; Überflutung
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: river flood; fluvial flooding; overbank flooding. Schlüsselwörter: Flusshochwasser; Flusshochwasserereignis; Überflutung. Sources: Wikipedia | https://en.wikipedia.org/wiki/Riverine_flood | USGS Water Services Daily Values API | https://waterservices.usgs.gov/docs/dv-service/daily-values-service-details/ | USGS Water Services Instantaneous Values API | https://waterservices.usgs.gov/docs/instantaneous-values/instantaneous-values-details/. Sample data: site_no,date,mean_discharge_cfs,max_discharge_cfs,gage_height_ft
05536123,2024-04-02,12400,16800,16.2
05536123,2024-04-03,18100,24900,18.9
05536123,2024-04-04,22300,30100,20.4
05536123,2024-04-05,19800,26500,19.3

Source description: River gauge daily statistics (mean/max discharge, stage) suitable for riverine flood hydrograph reconstruction and threshold exceedance analysis.
Source: USGS Water Services Daily Values API | …

[Knowledge:120 hazards:Hazard_Marine_Heatwave Marine Heatwave] HAZARD_ID: hazards:Hazard_Marine_Heatwave
LABEL: Marine Heatwave
GROUP: Climatological
SUBTYPE: Marine Incident
ALIASES: marine heatwave; marine hitzewelle
BM25_TEXT_EN: Caused by hazard(s): Climate change. Keywords: marine heatwave. Schlüsselwörter: marine hitzewelle. Sources: https://en.wikipedia.org/wiki/Marine_heatwave | https://robwschlegel.github.io/heatwaveR/articles/OISST_preparation.html. Sample data: date,lat,lon,sst_c,mhw_category,mhw_intensity_c
2023-07-15,36.0,-123.0,19.8,2,2.1
2023-07-16,36.0,-123.0,20.1,2,2.4

Source description: Daily gridded sea-surface temperature (NOAA OISST) used to detect marine heatwaves (e.g., Hobday methodology); records can include derived MHW category/intensity at a grid point.
Source: NOAA OISST (via ERDDAP) for Marine Heatwaves | https://robwschlegel.github.io/heatwaveR/articles/OISST_preparation.html.
VERBALIZED_EN: Caused by hazard(s): Climate change. Keywords: marine heatwave. Schlüsselwörter: marine hitzewelle. Sources: https://en.wikipedia.org/wiki/Marine_heatwave | https://robwschlegel.github.io/heatwaveR/articles/OISST_preparation.html. Sample data: …

[Knowledge:214 hazards:Hazard_Weapon_Of_Mass_Destruction Weapon Of Mass Destruction] HAZARD_ID: hazards:Hazard_Weapon_Of_Mass_Destruction
LABEL: Weapon Of Mass Destruction
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: weapon of mass destruction, war; massenvernichtungswaffe
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: weapon of mass destruction, war. Schlüsselwörter: massenvernichtungswaffe. Sources: https://en.wikipedia.org/wiki/Weapon_of_mass_destruction | START Violent Non-State Actor CBRN Data Portal | https://www.start.umd.edu/data-tools/cbrn-violent-non-state-actor-chemical-biological-radiological-and-nuclear-data-portal. Sample data: incident_id,date,country,agent_type,delivery_method,fatalities,injuries,summary
CBRN-0001,1995-03-20,Japan,Chemical,Aerosol release,13,6000,"Sarin attack in Tokyo subway"
CBRN-0002,2001-10-04,USA,Biological,Mail,5,17,"Anthrax letters"

Source description: Portal hosting databases on chemical/biological/radiological/nuclear incidents involving violent non-state actors; provides structured incident records for research.
Source: START Violent Non-State Actor CBRN Data Portal | https://www.start.umd.edu/data-tools/cbrn-violent-non-state-actor-chemical-biological-radiological-and-nuclear-data-portal.
VERBALIZED_EN: …

[Knowledge:215 hazards:Hazard_Whiteout Whiteout] HAZARD_ID: hazards:Hazard_Whiteout
LABEL: Whiteout
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: whiteout; blowing snow; ground blizzard; flat light; near-zero visibility; Whiteout; Schneetreiben; Bodenblizzard; diffuses Licht; Nullsicht
BM25_TEXT_EN: Caused by hazard(s): Blizzard. Keywords: whiteout; blowing snow; ground blizzard; flat light; near-zero visibility. Schlüsselwörter: Whiteout; Schneetreiben; Bodenblizzard; diffuses Licht; Nullsicht. Sources: https://en.m.wikipedia.org/wiki/Whiteout_(weather) | NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database. Sample data: station,datetime_utc,air_temp_c,wind_speed_m_s,visibility_m,present_weather
KDEN,2024-03-14T03:53Z,-6.0,8.0,800,SN
KDEN,2024-03-14T04:53Z,-7.0,12.0,200,BLSN

Source description: ISD present weather/visibility fields can indicate snow, blowing snow (whiteout), freezing rain, etc.
Source: NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database.
VERBALIZED_EN: Caused by hazard(s): Blizzard. Keywords: whiteout; blowing snow; ground blizzard; …

[Knowledge:11 hazards:Hazard_Avalanche Avalanche] HAZARD_ID: hazards:Hazard_Avalanche
LABEL: Avalanche
GROUP: Hydrological
SUBTYPE: Mass Movement
ALIASES: avalanche; snow avalanche; slab avalanche; Lawine; Schneelawine; Schneebrettlawine
BM25_TEXT_EN: Caused by hazard(s): Landslide|hazards:hazard avalanche. Keywords: avalanche; snow avalanche; slab avalanche. Schlüsselwörter: Lawine; Schneelawine; Schneebrettlawine. Sources: https://en.wikipedia.org/wiki/Avalanche | WSL/SLF EnviDat: Fatal avalanche accidents (CH) | https://www.envidat.ch/metadata/fatal-avalanche-accidents-in-switzerland-since-1936-37. Sample data: date,region,canton,activity,avalanche_type,fatalities,injured,elevation_m
2018-01-13,Valais,VS,Backcountry touring,Dry slab,2,1,2450
2019-04-19,Bernese Oberland,BE,Off-piste,Wet snow,1,0,2100

Source description: Accident-level avalanche records (date/location/activity/casualties) from Swiss avalanche accident database; includes avalanche type enabling dry vs wet subsets.
Source: WSL/SLF EnviDat: Fatal avalanche accidents (CH) | https://www.envidat.ch/metadata/fatal-avalanche-accidents-in-switzerland-since-1936-37.
VERBALIZED_EN: Caused by hazard(s): Landslide|hazards:hazard avalanche. Keywords: avalanche; snow …

[Knowledge:199 hazards:Hazard_Unexploded_Ordnance Unexploded ordnance] HAZARD_ID: hazards:Hazard_Unexploded_Ordnance
LABEL: Unexploded ordnance
GROUP: Conflict
SUBTYPE: War / Civil Unrest
ALIASES: unexploded ordnance, UXO, bomb, explosive remnants of war, ammunition; Blindgänger, UXO, Weltkriegsbombe, Kampfmittel, Munition
BM25_TEXT_EN: Caused by hazard(s): War|hazards:hazard terrorism. Keywords: unexploded ordnance, UXO, bomb, explosive remnants of war, ammunition. Schlüsselwörter: Blindgänger, UXO, Weltkriegsbombe, Kampfmittel, Munition. Sources: https://en.wikipedia.org/wiki/Unexploded_ordnance | World Bank LC3D (Landmine Contamination, Casualties and Clearance) | https://databank.worldbank.org/source/landmine-contamination-casualties-and-clearance-%28lc3d%29. Sample data: country,year,erw_casualties_total,area_contaminated_km2,area_cleared_km2
Cambodia,2019,77,1035,41
Ukraine,2023,608,174000,1200

Source description: Country-level indicators on landmine/ERW contamination, casualties, and clearance used as proxy for UXO contamination risk.
Source: World Bank LC3D (Landmine Contamination, Casualties and Clearance) | https://databank.worldbank.org/source/landmine-contamination-casualties-and-clearance-%28lc3d%29.
VERBALIZED_EN: Caused by hazard(s): …

[Knowledge:182 hazards:Hazard_Submarine_Cable_Disruption Submarine Cable Disruption] HAZARD_ID: hazards:Hazard_Submarine_Cable_Disruption
LABEL: Submarine Cable Disruption
GROUP: Technological
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: subsea telecom cables; physical cable cut; anchoring/fishing damage; earthquake/landslide hazard; service outages/latency; single point of failure; repair time/permits; redundancy and route diversity; economic and security impacts; Telekommunikations-Unterseekabel; Kabelbruch/Beschädigung; Schäden durch Ankern/Fischerei; Naturgefahren: Erdbeben/Hangrutsch; Dienstausfälle/Latenz; Single-Point-of-Failure; Reparaturzeiten/Genehmigungen; Redundanz/Routenvielfalt; wirtschaftliche und sicherheitspolitische Folgen
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: subsea telecom cables; physical cable cut; anchoring/fishing damage; earthquake/landslide hazard; service outages/latency; single point of failure; repair time/permits; redundancy and route diversity; economic and security impacts. Schlüsselwörter: Telekommunikations-Unterseekabel; Kabelbruch/Beschädigung; Schäden durch Ankern/Fischerei; Naturgefahren: Erdbeben/Hangrutsch; Dienstausfälle/Latenz; Single-Point-of-Failure; Reparaturzeiten/Genehmigungen; …

[Knowledge:137 hazards:Hazard_Oil_Chemical_Spill_Into_Waterways Oil/Chemical Spill Into Waterways] HAZARD_ID: hazards:Hazard_Oil_Chemical_Spill_Into_Waterways
LABEL: Oil/Chemical Spill Into Waterways
GROUP: Chemical
SUBTYPE: Marine Incident
ALIASES: oil spill; chemical spill; waterway contamination; Ölunfall; Chemieunfall; Gewässerverunreinigung
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Keywords: oil spill; chemical spill; waterway contamination. Schlüsselwörter: Ölunfall; Chemieunfall; Gewässerverunreinigung. Sources: https://en.wikipedia.org/wiki/Oil_spill | https://www.phmsa.dot.gov/hazmat/incident-statistics. Sample data: report_number,incident_date,mode,material_name,quantity_released,unit,environmental_damage,waterway_affected,cleanup_cost_usd
2022-004321,2022-09-27,HWY,Diesel fuel,600,gallon,Yes,Yes,45000
2021-007654,2021-02-11,PIPE,Crude oil,1200,barrel,Yes,Yes,2100000

Source description: Hazmat incident reporting data with environmental impact indicators; can be filtered for oil/chemical releases where waterways are affected and cleanup costs are recorded.
Source: PHMSA Hazmat Incident Statistics / DOT Form 5800.1 | https://www.phmsa.dot.gov/hazmat/incident-statistics.
VERBALIZED_EN: Caused by hazard(s): …

[Knowledge:217 hazards:Hazard_Wildfire_General Wildfire] HAZARD_ID: hazards:Hazard_Wildfire_General
LABEL: Wildfire
GROUP: Climatological
SUBTYPE: Wildfire
ALIASES: wildfire (general); Waldbrand
BM25_TEXT_EN: Caused by hazard(s): Wildfire. Keywords: wildfire (general). Schlüsselwörter: Waldbrand. Sources: https://en.wikipedia.org/wiki/Wildfire | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-121.456,2024-07-15,2030,N,nominal,12.5
37.130,-121.470,2024-07-15,2036,N,high,35.1

Source description: Near-real-time and archived satellite active fire/hotspot detections with location, acquisition time, brightness, and FRP; downloadable as CSV..
VERBALIZED_EN: Caused by hazard(s): Wildfire. Keywords: wildfire (general). Schlüsselwörter: Waldbrand. Sources: https://en.wikipedia.org/wiki/Wildfire | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-121.456,2024-07-15,2030,N,nominal,12.5
37.130,-121.470,2024-07-15,2036,N,high,35.1

Source description: Near-real-time and archived satellite active …

[Knowledge:44 hazards:Hazard_Data_Breach Data Breach] HAZARD_ID: hazards:Hazard_Data_Breach
LABEL: Data Breach
GROUP: Digital
SUBTYPE: Cyber Incident
ALIASES: personal data leak; Datenleck
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: personal data leak. Schlüsselwörter: Datenleck. Sources: Wikipedia | https://en.wikipedia.org/wiki/Data_breach | Privacy Rights Clearinghouse (PRC) Data Breach Chronology | https://privacyrights.org/data-breaches. Sample data: breach_id,breach_date,org_name,breach_type,records_affected,location,description
PRC-0001,2025-02-14,"Org A","HACK",120000,"US-CA","Unauthorized access to customer database"
PRC-0002,2025-05-09,"Org B","PHYS",3400,"US-NY","Stolen laptop containing unencrypted files"

Source description: Breach-event rows (date, organization, breach type, affected records, narrative) usable as raw samples for data-breach hazards.
Source: Privacy Rights Clearinghouse (PRC) Data Breach Chronology | https://privacyrights.org/data-breaches.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: personal data leak. Schlüsselwörter: Datenleck. Sources: Wikipedia | https://en.wikipedia.org/wiki/Data_breach | Privacy Rights Clearinghouse (PRC) Data Breach Chronology | …

[Knowledge:66 hazards:Hazard_Fog Fog] HAZARD_ID: hazards:Hazard_Fog
LABEL: Fog
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: fog; nebel
BM25_TEXT_EN: Caused by hazard(s): Fog. Keywords: fog. Schlüsselwörter: nebel. Sources: https://en.wikipedia.org/wiki/Fog | NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database. Sample data: station,datetime_utc,air_temp_c,dewpoint_c,wind_speed_m_s,visibility_m,present_weather
LSZH,2024-12-10T05:50Z,-1.0,-1.2,2.0,200,FG
LSZH,2024-12-10T06:20Z,-1.0,-1.2,2.5,300,FG

Source description: Hourly and synoptic surface observations (METAR/ASOS etc.) with present weather codes suitable for fog, sea smoke, snow, and other visibility-related hazards..
VERBALIZED_EN: Caused by hazard(s): Fog. Keywords: fog. Schlüsselwörter: nebel. Sources: https://en.wikipedia.org/wiki/Fog | NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database. Sample data: station,datetime_utc,air_temp_c,dewpoint_c,wind_speed_m_s,visibility_m,present_weather
LSZH,2024-12-10T05:50Z,-1.0,-1.2,2.0,200,FG
LSZH,2024-12-10T06:20Z,-1.0,-1.2,2.5,300,FG

Source …

[Knowledge:192 hazards:Hazard_Terrorism Terrorism] HAZARD_ID: hazards:Hazard_Terrorism
LABEL: Terrorism
GROUP: Societal
SUBTYPE: Mass Fatality
ALIASES: politically motivated violence; terrorism; violent extremism; non-state actors; mass casualty attacks; attacks on civilians; critical infrastructure targeting; fear/terror effects; radicalization pathways; emergency response overload; politisch motivierte Gewalt; Terrorismus; gewalttätiger Extremismus; nichtstaatliche Akteure; Massenanschläge; Angriffe auf Zivilisten; Ziel kritischer Infrastrukturen; Terrorwirkung/Angst; Radikalisierungsprozesse; Überlastung von Rettung/Response
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: politically motivated violence; terrorism; violent extremism; non-state actors; mass casualty attacks; attacks on civilians; critical infrastructure targeting; fear/terror effects; radicalization pathways; emergency response overload. Schlüsselwörter: politisch motivierte Gewalt; Terrorismus; gewalttätiger Extremismus; nichtstaatliche Akteure; Massenanschläge; Angriffe auf Zivilisten; Ziel kritischer Infrastrukturen; Terrorwirkung/Angst; Radikalisierungsprozesse; Überlastung von Rettung/Response. Sources: …

[Knowledge:14 hazards:Hazard_Avian_Influenza Epizootic] HAZARD_ID: hazards:Hazard_Avian_Influenza
LABEL: Epizootic
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: epizootic, poultry, outbreak; Vogelgrippe, Aviäre Influenza, Geflügelpest, Tierseuche, Ausbruch
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: epizootic, poultry, outbreak. Schlüsselwörter: Vogelgrippe, Aviäre Influenza, Geflügelpest, Tierseuche, Ausbruch. Sources: https://en.wikipedia.org/wiki/Avian_influenza | EURL Avian Flu Data Portal (ADIS-based) | https://eurlaidata.izsvenezie.it/epidemio.php | ECDC avian influenza threats/outbreaks | https://www.ecdc.europa.eu/en/avian-influenza-humans/threats-and-outbreaks | FAO EMPRES-i+ | https://empres-i.apps.fao.org/. Sample data: report_date,country,species,subtype,setting,cases_outbreaks,control_measures
2025-11-20,Netherlands,Poultry,H5N1,Farm,1,"culling; movement restrictions"
2025-11-22,Germany,Wild birds,H5N1,Wildlife,12,"carcass surveillance"
2025-11-25,Italy,Poultry,H5,Farm,2,"biosecurity 강화; culling"

Source description: Avian influenza outbreak/event rows (poultry/wild birds) consistent with ADIS/EMPRES-i reporting: date, location, host, subtype, and control actions.
Source: EURL Avian Flu Data Portal …

[Knowledge:50 hazards:Hazard_Drone_Hijacking_GNSS_Spoofing Drone Hijacking] HAZARD_ID: hazards:Hazard_Drone_Hijacking_GNSS_Spoofing
LABEL: Drone Hijacking
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: drone hijacking, GNSS spoofing, navigation deception, command takeover; Drohnenübernahme, GNSS-Spoofing, Navigationsmanipulation, Kontrollübernahme
BM25_TEXT_EN: Caused by hazard(s): GNSS disruption (jamming/spoofing/outage)|hazards:hazard cyberattack|hazards:hazard data breach. Keywords: drone hijacking, GNSS spoofing, navigation deception, command takeover. Schlüsselwörter: Drohnenübernahme, GNSS-Spoofing, Navigationsmanipulation, Kontrollübernahme. Sources: Wikipedia | https://en.wikipedia.org/wiki/GNSS_spoofing | TEXBAT (Texas Spoofing Test Battery) | https://radionavlab.ae.utexas.edu/texbat/. Sample data: t_s,CN0_dBHz,Doppler_Hz,code_phase_chips,tracking_state,spoof_flag
0.0,45.2,-1320.5,1023.2,LOCK,0
1.0,45.1,-1320.7,1019.8,LOCK,0
2.0,44.9,-1321.0,1012.4,LOCK,0
3.0,47.8,-950.2,900.1,LOCK,1
4.0,48.0,-940.8,880.6,LOCK,1

Source description: Recorded GNSS spoofing scenarios (receiver observables like C/N0 and Doppler) used to evaluate anti-spoofing techniques; proxy for drone navigation hijacking via GNSS spoofing.
Source: TEXBAT (Texas Spoofing …

[Knowledge:148 hazards:Hazard_Radar_Jamming_and_Deception Radar jamming and deception] HAZARD_ID: hazards:Hazard_Radar_Jamming_and_Deception
LABEL: Radar jamming and deception
GROUP: Technological
SUBTYPE: Cyber Incident
ALIASES: radar jamming, electronic countermeasures, ECM, noise jamming, barrage jamming, spot jamming, deception jamming, false targets, spoofed returns, chaff, jamming pod, radar interference, radar outage, degraded tracking, reduced detection; Radar-Jamming, elektronische Gegenmaßnahmen, ECM, Rauschstörung, Sperrfeuerstörung, Punktstörung, Täuschstörung, falsche Ziele, manipulierte Echos, Düppel (Chaff), Störsender, Radarstörung, Radar-Ausfall, beeinträchtigte Verfolgung, verringerte Detektion
BM25_TEXT_EN: Caused by hazard(s): Cyberattack|hazards:hazard terrorism|hazards:hazard war. Keywords: radar jamming, electronic countermeasures, ECM, noise jamming, barrage jamming, spot jamming, deception jamming, false targets, spoofed returns, chaff, jamming pod, radar interference, radar outage, degraded tracking, reduced detection. Schlüsselwörter: Radar-Jamming, elektronische Gegenmaßnahmen, ECM, Rauschstörung, Sperrfeuerstörung, Punktstörung, Täuschstörung, falsche Ziele, manipulierte Echos, Düppel (Chaff), Störsender, Radarstörung, Radar-Ausfall, …

[Knowledge:160 hazards:Hazard_Sand_Dust_Storm Sand/Dust Storm] HAZARD_ID: hazards:Hazard_Sand_Dust_Storm
LABEL: Sand/Dust Storm
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: sand, dust storm; Sand-/Staubsturm
BM25_TEXT_EN: Caused by hazard(s): Sand dust storm|hazards:hazard storm. Keywords: sand, dust storm. Schlüsselwörter: Sand-/Staubsturm. Sources: https://en.wikipedia.org/wiki/Sand/Dust_storm | Copernicus CAMS Global Reanalysis (EAC4) | https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4. Sample data: time_utc,lat,lon,dust_aod_550,total_aod_550,so2_kg_m2
2024-02-18T12:00Z,28.0,-15.0,0.65,0.80,0.00002
2024-02-18T12:00Z,30.0,-10.0,0.58,0.72,0.00001

Source description: Atmospheric composition reanalysis including aerosols (e.g., dust AOD) useful for sand/dust storms, Saharan dust and vog dispersion analyses..
VERBALIZED_EN: Caused by hazard(s): Sand dust storm|hazards:hazard storm. Keywords: sand, dust storm. Schlüsselwörter: Sand-/Staubsturm. Sources: https://en.wikipedia.org/wiki/Sand/Dust_storm | Copernicus CAMS Global Reanalysis (EAC4) | https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4. Sample data: …

[Knowledge:135 hazards:Hazard_Nuclear_Plant_Accident Nuclear Plant Accident] HAZARD_ID: hazards:Hazard_Nuclear_Plant_Accident
LABEL: Nuclear Plant Accident
GROUP: Radiological
SUBTYPE: Nuclear-Radiological Incident
ALIASES: nuclear accident; nuclear power plant accident; core melt; Kernkraftwerksunfall; Nuklearunfall; Kernschmelze
BM25_TEXT_EN: Caused by hazard(s): War. Keywords: nuclear accident; nuclear power plant accident; core melt. Schlüsselwörter: Kernkraftwerksunfall; Nuklearunfall; Kernschmelze. Sources: https://en.wikipedia.org/wiki/Nuclear_and_radiation_accidents_and_incidents | IAEA INES database | https://www.iaea.org/resources/databases/international-nuclear-and-radiological-event-scale. Sample data: event_date,country,facility,event_title,ines_level,event_type
2011-03-11,Japan,Fukushima Daiichi,"Multiple reactor core damage following earthquake/tsunami",7,"NPP accident"
1986-04-26,Ukraine,Chernobyl,"Reactor accident during test; major release",7,"NPP accident"
1979-03-28,USA,Three Mile Island,"Loss-of-coolant accident; partial core melt",5,"NPP accident"

Source description: Iconic nuclear power plant accidents with INES level classifications. A practical ‘raw’ sample table for nuclear-plant-accident hazard event records.
Source: IAEA INES …

[Knowledge:216 hazards:Hazard_Wildfire Wildfire] HAZARD_ID: hazards:Hazard_Wildfire
LABEL: Wildfire
GROUP: Climatological
SUBTYPE: Wildfire
ALIASES: wildfire; forest fire; bushfire; firestorm; Waldbrand; Flächenbrand; Buschfeuer; Feuersturm
BM25_TEXT_EN: Caused by hazard(s): Wildfire. Keywords: wildfire; forest fire; bushfire; firestorm. Schlüsselwörter: Waldbrand; Flächenbrand; Buschfeuer; Feuersturm. Sources: https://en.wikipedia.org/wiki/Wildfire | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: latitude,longitude,acq_date,acq_time,satellite,confidence,frp
37.123,-121.456,2024-07-15,2030,N,nominal,12.5
37.130,-121.470,2024-07-15,2036,N,high,35.1

Source description: Near-real-time and archived satellite active fire/hotspot detections with location, acquisition time, brightness, and FRP; downloadable as CSV..
VERBALIZED_EN: Caused by hazard(s): Wildfire. Keywords: wildfire; forest fire; bushfire; firestorm. Schlüsselwörter: Waldbrand; Flächenbrand; Buschfeuer; Feuersturm. Sources: https://en.wikipedia.org/wiki/Wildfire | NASA FIRMS Active Fire (VIIRS/MODIS) | https://firms.modaps.eosdis.nasa.gov/active_fire/. Sample data: …

[Knowledge:62 hazards:Hazard_Financial_Shock Financial Shock] HAZARD_ID: hazards:Hazard_Financial_Shock
LABEL: Financial Shock
GROUP: Societal
SUBTYPE: Infrastructure Failure / Disruption
ALIASES: sudden loss of confidence; liquidity crisis; bank run; credit crunch; asset price collapse; contagion; insolvency risk; recession spillovers; early warning/monitoring; macroprudential policy; plötzlicher Vertrauensverlust; Liquiditätskrise; Bankenansturm (Bank Run); Kreditklemme; Preisverfall von Vermögenswerten; Ansteckungseffekte; Insolvenzrisiko; Rezessions-Spillover; Frühwarn- und Monitoring-Systeme; makroprudenzielle Politik
BM25_TEXT_EN: Caused by hazard(s): Civil unrest. Keywords: sudden loss of confidence; liquidity crisis; bank run; credit crunch; asset price collapse; contagion; insolvency risk; recession spillovers; early warning/monitoring; macroprudential policy. Schlüsselwörter: plötzlicher Vertrauensverlust; Liquiditätskrise; Bankenansturm (Bank Run); Kreditklemme; Preisverfall von Vermögenswerten; Ansteckungseffekte; Insolvenzrisiko; Rezessions-Spillover; Frühwarn- und Monitoring-Systeme; makroprudenzielle Politik. Sources: https://www.undrr.org/understanding-disaster-risk/terminology/hips/so0401 | …

[Knowledge:84 hazards:Hazard_Human_Capital_Flight_Brain_Drain Human Capital Flight (Brain Drain)] HAZARD_ID: hazards:Hazard_Human_Capital_Flight_Brain_Drain
LABEL: Human Capital Flight (Brain Drain)
GROUP: Societal
SUBTYPE: Psychogenic Incident
ALIASES: talent emigration; Abwanderung
BM25_TEXT_EN: Caused by hazard(s): Civil unrest. Keywords: talent emigration. Schlüsselwörter: Abwanderung. Sources: https://en.wikipedia.org/wiki/Human_capital_flight | World Bank WDI net migration indicator | https://data.worldbank.org/indicator/SM.POP.NETM | Fragile States Index indicator E3 | https://fragilestatesindex.org/indicators/e3/. Sample data: country,year,net_migration,net_migration_unit,brain_drain_score_fsi
Ireland,2013,33200,persons,2.8
Syria,2015,-1200000,persons,9.6
Philippines,2020,-250000,persons,6.1

Source description: Country-year migration balance (WDI net migration) combined with a brain-drain proxy score (Fragile States Index E3). Useful as a quantitative proxy dataset for human-capital flight.
Source: World Bank WDI net migration indicator | https://data.worldbank.org/indicator/SM.POP.NETM | Fragile States Index indicator E3 | https://fragilestatesindex.org/indicators/e3/.
VERBALIZED_EN: Caused by hazard(s): Civil unrest. Keywords: talent emigration. Schlüsselwörter: …

[Knowledge:48 hazards:Hazard_Disinformation Disinformation] HAZARD_ID: hazards:Hazard_Disinformation
LABEL: Disinformation
GROUP: Digital
SUBTYPE: Cyber Incident
ALIASES: misinformation; Desinformation
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: misinformation. Schlüsselwörter: Desinformation. Sources: Wikipedia | https://en.wikipedia.org/wiki/Disinformation | EUvsDisinfo Disinformation Cases | https://euvsdisinfo.eu/disinformation-cases/. Sample data: case_id,date,language,source,claim,disproof,topic
EUDIS-0001,2025-01-12,en,"Outlet X","False claim about vaccine harms","Official statistics contradict claim","health"
EUDIS-0002,2025-02-03,de,"Outlet Y","Fabricated story about election fraud","Explains inconsistencies + official results","elections"

Source description: Case-level disinformation entries (claim, channel/source, language, debunk/analysis, topic) suitable as raw samples for disinformation hazards.
Source: EUvsDisinfo Disinformation Cases | https://euvsdisinfo.eu/disinformation-cases/.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: misinformation. Schlüsselwörter: Desinformation. Sources: Wikipedia | https://en.wikipedia.org/wiki/Disinformation | EUvsDisinfo Disinformation Cases | …

[Knowledge:220 hazards:Hazard_Zoonotic_Spillover Zoonotic Spillover] HAZARD_ID: hazards:Hazard_Zoonotic_Spillover
LABEL: Zoonotic Spillover
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: zoonosis; spillover; animal-to-human transmission; Zoonose; Spillover; Übertragung Tier-zu-Mensch
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: zoonosis; spillover; animal-to-human transmission. Schlüsselwörter: Zoonose; Spillover; Übertragung Tier-zu-Mensch. Sources: https://en.wikipedia.org/wiki/Zoonosis | FAO EMPRES-i+ | https://empres-i.apps.fao.org/ | WHO Disease Outbreak News | https://www.who.int/emergencies/disease-outbreak-news. Sample data: event_date,country,animal_species,agent,humans_affected,signal_source,notes
2025-03-04,CountryX,Poultry,"H5N1 avian influenza",1,"EMPRES-i/WOAH reporting","Human infection linked to poultry exposure"
2025-07-18,CountryY,Bats,"Nipah-like virus",0,"Field investigation","Spillover risk investigation ongoing"
2025-10-02,CountryZ,Camels,"MERS-CoV",2,"National surveillance","Cluster investigated"

Source description: Zoonotic spillover proxy ‘event list’ combining animal-disease intelligence and human outbreak bulletins: each row is an animal reservoir + pathogen signal with human cases/alerts.
Source: FAO …

[Knowledge:110 hazards:Hazard_Light_Pollution Light pollution] HAZARD_ID: hazards:Hazard_Light_Pollution
LABEL: Light pollution
GROUP: Chemical
SUBTYPE: Visibility
ALIASES: light pollution, skyglow, glare, light trespass, over-illumination, bright lights, reduced visibility, night visibility, poor night vision, illumination disruption; Lichtverschmutzung, Himmelsaufhellung, Blendung, Lichtimmission, Überbeleuchtung, grelles Licht, Sichtbehinderung, Nachtsicht, eingeschränkte Nachtsicht, Beleuchtungsstörung
BM25_TEXT_EN: Caused by hazard(s): Critical infrastructure failure|hazards:hazard environmental pollution. Keywords: light pollution, skyglow, glare, light trespass, over-illumination, bright lights, reduced visibility, night visibility, poor night vision, illumination disruption. Schlüsselwörter: Lichtverschmutzung, Himmelsaufhellung, Blendung, Lichtimmission, Überbeleuchtung, grelles Licht, Sichtbehinderung, Nachtsicht, eingeschränkte Nachtsicht, Beleuchtungsstörung. Sources: https://en.wikipedia.org/wiki/Light_pollution | NOAA EOG VIIRS Nighttime Lights (VNL) | https://eogdata.mines.edu/products/vnl/. Sample data: tile_id,date_yyyymm,avg_radiance_nW_cm2_sr,cloud_free_obs
75N060W,202401,12.34,18
75N060W,202402,11.98,16

Source …

[Knowledge:207 hazards:Hazard_Volcanic_Winter Volcanic Winter] HAZARD_ID: hazards:Hazard_Volcanic_Winter
LABEL: Volcanic Winter
GROUP: Geophysical
SUBTYPE: Volcanic Activity
ALIASES: volcanic winter; Volcanic winter
BM25_TEXT_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic winter. Schlüsselwörter: Volcanic winter. Sources: https://en.wikipedia.org/wiki/Volcanic_winter | NOAA/WDS Paleoclimatology Volcanic Aerosol Forcing (Crowley & Unterman 2013) | https://www.ncei.noaa.gov/pub/data/paleo/climate_forcing/volcanic_aerosols/crowley2013/. Sample data: year,aod_global
1815,0.25
1816,0.18
1817,0.10

Source description: Ice-core-based reconstruction of volcanic aerosol optical depth / sulfate deposition used as volcanic climate forcing (proxy for volcanic winter conditions).
Source: NOAA/WDS Paleoclimatology Volcanic Aerosol Forcing (Crowley & Unterman 2013) | https://www.ncei.noaa.gov/pub/data/paleo/climate_forcing/volcanic_aerosols/crowley2013/.
VERBALIZED_EN: Caused by hazard(s): Volcanic activity. Keywords: volcanic winter. Schlüsselwörter: Volcanic winter. Sources: https://en.wikipedia.org/wiki/Volcanic_winter | NOAA/WDS Paleoclimatology Volcanic Aerosol Forcing (Crowley & Unterman 2013) | …

[Knowledge:188 hazards:Hazard_Supernova Supernova] HAZARD_ID: hazards:Hazard_Supernova
LABEL: Supernova
GROUP: Extraterrestrial
SUBTYPE: Space Weather
ALIASES: supernova
BM25_TEXT_EN: Caused by hazard(s): Impact event. Keywords: supernova. Schlüsselwörter: supernova. Sources: https://en.wikipedia.org/wiki/Supernova | Open Supernova Catalog (AstroCats OACAPI) | https://api.astrocats.space/. Sample data: name,ra,dec,redshift,claimedtype,discoverdate
SN2011fe,210.8023,54.3489,0.000804,Ia,2011-08-24
SN2020fqv,14.9117,29.1486,0.0020,II,2020-04-01

Source description: API-backed open catalog of supernovae with metadata and time-series photometry/spectra where available..
VERBALIZED_EN: Caused by hazard(s): Impact event. Keywords: supernova. Schlüsselwörter: supernova. Sources: https://en.wikipedia.org/wiki/Supernova | Open Supernova Catalog (AstroCats OACAPI) | https://api.astrocats.space/. Sample data: name,ra,dec,redshift,claimedtype,discoverdate
SN2011fe,210.8023,54.3489,0.000804,Ia,2011-08-24
SN2020fqv,14.9117,29.1486,0.0020,II,2020-04-01

Source description: API-backed open catalog of supernovae with metadata and time-series photometry/spectra where available..
LINKS: causedByHazard hazards:Hazard_Impact_Event
SOURCES: …

[Knowledge:114 hazards:Hazard_Locust_Infestation Locust Infestation] HAZARD_ID: hazards:Hazard_Locust_Infestation
LABEL: Locust Infestation
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: locust infestation; Heuschreckenplage
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: locust infestation. Schlüsselwörter: Heuschreckenplage. Sources: https://en.wikipedia.org/wiki/Locust_infestation | FAO Locust Hub | https://locust-hub-hqfao.hub.arcgis.com/ | FAO Locust Watch | https://www.fao.org/locust-watch/en. Sample data: obs_date,country,lat,lon,species,phase,locust_density_m2,control_action
2025-10-03,Mauritania,18.08,-15.98,"Schistocerca gregaria","gregar",120,"ground_spray"
2025-10-06,Somalia,2.04,45.34,"Schistocerca gregaria","gregar",65,"aerial_spray"
2025-10-08,Pakistan,27.55,68.21,"Schistocerca gregaria","transiens",18,"survey_only"

Source description: Field observation-style records used in locust monitoring (date/location/phase/density and control action), aligned to FAO desert locust early warning workflows.
Source: FAO Locust Hub | https://locust-hub-hqfao.hub.arcgis.com/ | FAO Locust Watch | https://www.fao.org/locust-watch/en.
VERBALIZED_EN: Caused by hazard(s): Zoonotic spillover. Keywords: locust infestation. Schlüsselwörter: …

[Knowledge:167 hazards:Hazard_Snow Snow] HAZARD_ID: hazards:Hazard_Snow
LABEL: Snow
GROUP: Meteorological
SUBTYPE: Visibility
ALIASES: snow, snowfall, winter weather, accumulation, reduced visibility; Schnee, Schneefall, Winterwetter, Neuschnee, Sichtbehinderung
BM25_TEXT_EN: Caused by hazard(s): Storm. Keywords: snow, snowfall, winter weather, accumulation, reduced visibility. Schlüsselwörter: Schnee, Schneefall, Winterwetter, Neuschnee, Sichtbehinderung. Sources: https://en.wikipedia.org/wiki/Snow | NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database. Sample data: station,datetime_utc,air_temp_c,wind_speed_m_s,visibility_m,present_weather
KDEN,2024-03-14T03:53Z,-6.0,8.0,800,SN
KDEN,2024-03-14T04:53Z,-7.0,12.0,200,BLSN

Source description: ISD present weather/visibility fields can indicate snow, blowing snow (whiteout), freezing rain, etc.
Source: NOAA Integrated Surface Database (Global Hourly / ISD) | https://www.ncei.noaa.gov/products/land-based-station/integrated-surface-database.
VERBALIZED_EN: Caused by hazard(s): Storm. Keywords: snow, snowfall, winter weather, accumulation, reduced visibility. Schlüsselwörter: Schnee, …

[Knowledge:194 hazards:Hazard_Toxic_Release Toxic Release] HAZARD_ID: hazards:Hazard_Toxic_Release
LABEL: Toxic Release
GROUP: Chemical
SUBTYPE: Industrial Incident
ALIASES: toxic release; hazardous release; chemical leak; Toxische Freisetzung; Gefahrstofffreisetzung; Chemieleck
BM25_TEXT_EN: Caused by hazard(s): Industrial explosion|hazards:hazard critical infrastructure failure. Keywords: toxic release; hazardous release; chemical leak. Schlüsselwörter: Toxische Freisetzung; Gefahrstofffreisetzung; Chemieleck. Sources: https://en.wikipedia.org/wiki/Toxic_substance | https://www.epa.gov/toxics-release-inventory-tri-program/tri-basic-data-files-calendar-years-1987-present. Sample data: year,tri_facility_id,facility_name,chemical,on_site_release_kg,air_release_kg,water_release_kg,land_release_kg
2023,12345ABCDEF1,Example Refinery,Benzene,8500,6200,120,2180
2023,67890GHIJKL2,Example Paper Mill,Ammonia,1400,300,45,1055

Source description: Annual facility-level pollutant release quantities reported to EPA's TRI, broken out by medium (air/water/land); useful for chronic or acute toxic-release hazard characterization.
Source: EPA Toxics Release Inventory (TRI) Basic Data Files | …

[Knowledge:4 hazards:Hazard_Algal_Bloom Algal Bloom] HAZARD_ID: hazards:Hazard_Algal_Bloom
LABEL: Algal Bloom
GROUP: Biological
SUBTYPE: Outbreak
ALIASES: algal bloom; harmful algal bloom; red tide; Algenblüte; schädliche Algenblüte; Rote Tide
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: algal bloom; harmful algal bloom; red tide. Schlüsselwörter: Algenblüte; schädliche Algenblüte; Rote Tide. Sources: https://en.wikipedia.org/wiki/Algal_bloom | NOAA HABSOS | https://habsos.noaa.gov/ | NOAA NCEI HABSOS product | https://www.ncei.noaa.gov/products/harmful-algal-blooms-observing-system. Sample data: sample_date,lat,lon,organism,cell_count_per_L,water_temp_c,salinity_psu
2025-08-12,27.02,-82.46,"Karenia brevis",1200000,30.1,34.8
2025-08-15,26.89,-82.53,"Karenia brevis",450000,29.6,35.1
2025-08-18,26.77,-82.61,"Karenia brevis",80000,29.2,35.4

Source description: Harmful algal bloom monitoring sample rows (cell counts + environmental variables) as distributed via NOAA’s HABSOS system.
Source: NOAA HABSOS | https://habsos.noaa.gov/ | NOAA NCEI HABSOS product | https://www.ncei.noaa.gov/products/harmful-algal-blooms-observing-system.
VERBALIZED_EN: Caused by hazard(s): Zoonotic spillover. Keywords: algal bloom; harmful …

[Knowledge:41 hazards:Hazard_Cyberattack_Causing_Physical_Disruption Cyberattack Causing Physical Disruption] HAZARD_ID: hazards:Hazard_Cyberattack_Causing_Physical_Disruption
LABEL: Cyberattack Causing Physical Disruption
GROUP: Black Swan
SUBTYPE: Cyber Incident
ALIASES: cyberattack; critical infrastructure; ICS; SCADA; sabotage; Cyberangriff; kritische Infrastruktur; Sabotage
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: cyberattack; critical infrastructure; ICS; SCADA; sabotage. Schlüsselwörter: Cyberangriff; kritische Infrastruktur; ICS; SCADA; Sabotage. Sources: Wikipedia | https://en.wikipedia.org/wiki/Cyberattack | VERIS Community Database (VCDB) | https://github.com/vz-risk/VCDB. Sample data: incident_id,sector,physical_process_impacted,impact_type,downtime_hours,initial_vector
VCDB-101,Energy,Yes,"ICS outage / operations halted",6,"Remote access compromise"
VCDB-102,Manufacturing,Yes,"Safety shutdown triggered",3,"Phishing -> ransomware"

Source description: Derived/flattened incident rows highlighting operational/physical disruption (e.g., ICS downtime) based on structured VCDB incidents.
Source: VERIS Community Database (VCDB) | https://github.com/vz-risk/VCDB.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. Keywords: cyberattack; critical infrastructure; ICS; …

[Knowledge:56 hazards:Hazard_Explosive_Remnants_Of_War_UXO_Contamination Explosive Remnants Of War / UXO Contamination] HAZARD_ID: hazards:Hazard_Explosive_Remnants_Of_War_UXO_Contamination
LABEL: Explosive Remnants Of War / UXO Contamination
GROUP: Societal
SUBTYPE: War / Civil Unrest
ALIASES: unexploded ordnance (UXO); abandoned explosive ordnance; landmine/cluster munition remnants; post-conflict contamination; accidental detonation; civilian casualties; blocked reconstruction/agriculture; clearance operations; marking/fencing; risk education; Blindgänger (UXO) (auch: nicht explodierte Munition); zurückgelassene Munition (AXO); Minen-/Streumunitionsreste; Kampfmittelbelastung nach Konflikt; unbeabsichtigte Detonation; zivile Opfer; blockierter Wiederaufbau/Landwirtschaft; Kampfmittelräumung; Markierung/Absperrung; Risikoaufklärung
BM25_TEXT_EN: Caused by hazard(s): Terrorism. Keywords: unexploded ordnance (UXO); abandoned explosive ordnance; landmine/cluster munition remnants; post-conflict contamination; accidental detonation; civilian casualties; blocked reconstruction/agriculture; clearance operations; marking/fencing; risk education. Schlüsselwörter: Blindgänger (UXO) (auch: nicht explodierte Munition); zurückgelassene Munition (AXO); Minen-/Streumunitionsreste; Kampfmittelbelastung nach …

[Knowledge:45 hazards:Hazard_Deliberate_Biological_Attack Deliberate Biological Attack] HAZARD_ID: hazards:Hazard_Deliberate_Biological_Attack
LABEL: Deliberate Biological Attack
GROUP: Biological
SUBTYPE: Biological Incident
ALIASES: bioterrorism; biological attack; biological weapon; Bioterrorismus; biologischer Angriff; Biowaffe
BM25_TEXT_EN: Caused by hazard(s): Zoonotic spillover. Keywords: bioterrorism; biological attack; biological weapon. Schlüsselwörter: Bioterrorismus; biologischer Angriff; Biowaffe. Sources: Wikipedia | https://en.wikipedia.org/wiki/Bioterrorism | Global Terrorism Database (GTD) | https://www.start.umd.edu/gtd/. Sample data: eventid,iyear,imonth,iday,country_txt,region_txt,city,attacktype1_txt,targtype1_txt,weaptype1_txt,nkill,nwound,summary
200101010001,2001,1,1,CountryX,RegionY,CityZ,Assassination,Government,Biological,0,2,"Suspected biological agent dissemination; symptoms reported; investigation opened"
201004150123,2010,4,15,CountryA,RegionB,CityC,Bombing/Explosion,Business,Biological,1,10,"Device used to spread harmful substance; responders affected"

Source description: Event-level terrorism incident records; filter/label for biological weapon/agent-related attacks to model deliberate biological attack scenarios.
Source: Global …

[Knowledge:175 hazards:Hazard_St_Elmos_Fire St. Elmo's fire] HAZARD_ID: hazards:Hazard_St_Elmos_Fire
LABEL: St. Elmo's fire
GROUP: Meteorological
SUBTYPE: Lightning
ALIASES: St. Elmo's fire; corona discharge; atmospheric electricity; electric field; glow discharge; thunderstorm; plasma; ship mast; aircraft wing, corposant, Hermes fire, furole, witchfire or witch's fire; Sankt-Elms-Feuer; Elmsfeuer, Koronaentladung; atmosphärische Elektrizität; elektrisches Feld; Glimmentladung; Gewitter; Plasma; Schiffsmast; Flugzeugflügel
BM25_TEXT_EN: Caused by hazard(s): Wildfire|hazards:hazard lightning. Keywords: St. Elmo's fire; corona discharge; atmospheric electricity; electric field; glow discharge; thunderstorm; plasma; ship mast; aircraft wing, corposant, Hermes fire, furole, witchfire or witch's fire. Schlüsselwörter: Sankt-Elms-Feuer; Elmsfeuer, Koronaentladung; atmosphärische Elektrizität; elektrisches Feld; Glimmentladung; Gewitter; Plasma; Schiffsmast; Flugzeugflügel. Sources: https://en.wikipedia.org/wiki/St._Elmo's_fire | https://madis.ncep.noaa.gov/madis_metar.shtml. Sample data: station,valid_time_utc,metar,remarks
KJFK,2024-09-12T02:51Z,"KJFK 120251Z 04018G28KT 10SM -RA SCT020 BKN035 18/16 A2992","RMK AO2 LTG DSNT …

[Knowledge:13 hazards:Hazard_Avalanche_Wet Avalanche (Wet)] HAZARD_ID: hazards:Hazard_Avalanche_Wet
LABEL: Avalanche (Wet)
GROUP: Hydrological
SUBTYPE: Mass Movement
ALIASES: avalanche (wet); Lawine (nass)
BM25_TEXT_EN: Caused by hazard(s): Landslide|hazards:hazard avalanche. Keywords: avalanche (wet). Schlüsselwörter: Lawine (nass). Sources: https://en.wikipedia.org/wiki/Avalanche_%28wet%29 | WSL/SLF EnviDat: Fatal avalanche accidents (CH) | https://www.envidat.ch/metadata/fatal-avalanche-accidents-in-switzerland-since-1936-37. Sample data: date,region,canton,activity,avalanche_type,fatalities,injured,elevation_m
2019-04-19,Bernese Oberland,BE,Off-piste,Wet snow,1,0,2100
2021-05-02,Grisons,GR,Hiking,Wet snow,1,0,1850

Source description: Subset of avalanche accident records where avalanche type is wet-snow. Useful for spring/temperature-driven avalanche hazard modeling.
Source: WSL/SLF EnviDat: Fatal avalanche accidents (CH) | https://www.envidat.ch/metadata/fatal-avalanche-accidents-in-switzerland-since-1936-37.
VERBALIZED_EN: Caused by hazard(s): Landslide|hazards:hazard avalanche. Keywords: avalanche (wet). Schlüsselwörter: Lawine (nass). Sources: https://en.wikipedia.org/wiki/Avalanche_%28wet%29 | WSL/SLF EnviDat: Fatal avalanche …

[Knowledge:122 hazards:Hazard_Mass_Fatality_Incident Mass Fatality Incident] HAZARD_ID: hazards:Hazard_Mass_Fatality_Incident
LABEL: Mass Fatality Incident
GROUP: Societal
SUBTYPE: Mass Fatality
ALIASES: mass fatality incident; mass deaths; mass casualty; disaster; fatality management; morgue surge; victim identification; incident response; Massensterbeereignis; Massenanfall von Toten; Massenunfall; Katastrophe; Totenmanagement; Kapazitätsengpass Leichenhalle; Opferidentifizierung; Einsatzmanagement
BM25_TEXT_EN: Caused by hazard(s): Civil unrest. Keywords: mass fatality incident; mass deaths; mass casualty; disaster; fatality management; morgue surge; victim identification; incident response. Schlüsselwörter: Massensterbeereignis; Massenanfall von Toten; Massenunfall; Katastrophe; Totenmanagement; Kapazitätsengpass Leichenhalle; Opferidentifizierung; Einsatzmanagement. Sources: https://en.wikipedia.org/wiki/Mass_fatality_incident | EM-DAT International Disaster Database | https://www.emdat.be/. Sample data: dis_no,year,event_name,disaster_group,disaster_type,country,total_deaths,total_affected,total_damages_usd
2025-0123,2025,"Severe storm outbreak",Natural,Meteorological,CountryX,312,120000,450000000
2024-0456,2024,"Ferry …

[Knowledge:116 hazards:Hazard_Major_Dam_Levee_Failure Major Dam/Levee Failure] HAZARD_ID: hazards:Hazard_Major_Dam_Levee_Failure
LABEL: Major Dam/Levee Failure
GROUP: Technological
SUBTYPE: Flood
ALIASES: dam failure; levee failure; flooding; infrastructure collapse; Dammbruch; Deichbruch; Überschwemmung; Infrastrukturversagen
BM25_TEXT_EN: Caused by hazard(s): Atmospheric river extreme precipitation event. Keywords: dam failure; levee failure; flooding; infrastructure collapse. Schlüsselwörter: Dammbruch; Deichbruch; Überschwemmung; Infrastrukturversagen. Sources: Wikipedia | https://en.wikipedia.org/wiki/Dam_failure | FEMA/USACE National Inventory of Dams (NID) | https://gis-fema.hub.arcgis.com/datasets/fedmaps::national-inventory-of-dams/about | USACE National Levee Database | https://levees.sec.usace.army.mil/ | USGS Water Services Instantaneous Values API | https://waterservices.usgs.gov/docs/instantaneous-values/instantaneous-values-details/. Sample data: structure_id,structure_type,name,state,lat,lon,hazard_potential,height_ft,storage_acft,owner_type,last_inspection_year
NID-IL00001,Dam,Example Dam,IL,39.78,-89.64,High,72,18500,Public,2023
NLD-IL-00012,Levee System,Example Levee,IL,39.80,-89.70,NA,NA,NA,Public,2022

Source description: Asset inventory …

[Knowledge:40 hazards:Hazard_Cyberattack Cyberattack] HAZARD_ID: hazards:Hazard_Cyberattack
LABEL: Cyberattack
GROUP: Digital
SUBTYPE: Cyber Incident
ALIASES: cyberattack; critical infrastructure; ICS/SCADA; physical disruption; Cyberangriff; kritische Infrastruktur; physische Störung
BM25_TEXT_EN: Caused by hazard(s): Cyberattack. Keywords: cyberattack; critical infrastructure; ICS/SCADA; physical disruption. Schlüsselwörter: Cyberangriff; kritische Infrastruktur; ICS/SCADA; physische Störung. Sources: Wikipedia | https://en.wikipedia.org/wiki/Cyberattack | VERIS Community Database (VCDB) | https://github.com/vz-risk/VCDB. Sample data: {"incident_id":"VCDB-001","timeline":{"discovery":"2025-03-02"},"actor":{"external":{"motive":"financial","variety":["organized crime"]}},"action":{"malware":true,"hacking":true},"asset":{"assets":[{"variety":"server","hosting":"on-prem"}]},"attribute":{"confidentiality":{"data":[{"variety":"personal"}]}},"victim":{"industry":"Healthcare"}}

Source description: Incident-level cyberattack records coded in VERIS (actor/action/asset/impact) for modeling general cyberattack hazards.
Source: VERIS Community Database (VCDB) | https://github.com/vz-risk/VCDB.
VERBALIZED_EN: Caused by hazard(s): Cyberattack. …

[Knowledge:20 hazards:Hazard_Blackout Blackout] HAZARD_ID: hazards:Hazard_Blackout
LABEL: Blackout
ALIASES: Blackout; Kaskadenausfall; Stromausfall; Stromnetzausfall; blackout; cascading failure; grid failure; power outage
BM25_TEXT_EN: Related activity: Itoperation. Caused by: Poor maintenance; Power grid collapse. Consequences: Data loss; Service interruption. Creates risk: Blackout impact. Sources: https://en.wikipedia.org/wiki/Power_outage. Sample data: SampleData for Blackout.
VERBALIZED_EN: Related activity: Itoperation. Caused by: Poor maintenance; Power grid collapse. Consequences: Data loss; Service interruption. Creates risk: Blackout impact. Sources: https://en.wikipedia.org/wiki/Power_outage. Sample data: SampleData for Blackout.
LINKS: relatedToActivity hazards:Activity_ITOperation causedBy hazards:Activity_PoorMaintenance hazards:Failure_PowerGridCollapse hasConsequence hazards:Consequence_DataLoss hazards:Consequence_ServiceInterruption createsRisk hazards:Risk_BlackoutImpact
RISK: id hazards:Risk_BlackoutImpact type hazards:Risk links exposes hazards:Agent_Hospital mitigatedBy hazards:Control_EmergencyGenerator hasAssessment hazards:Assessment_Blackout_2026_02 assessment hazards:RiskAssesment hasLikelihood …

[Knowledge:25 hazards:Hazard_ChemicalRelease Chemical release] HAZARD_ID: hazards:Hazard_ChemicalRelease
LABEL: Chemical release
ALIASES: Chemieunfall; Chemikalienverschüttung; Kontamination; chemical spill; contamination; hazardous materials spill
BM25_TEXT_EN: Caused by: Inadequate training. Consequences: Health impact. Creates risk: Chemical exposure. Sources: https://en.wikipedia.org/wiki/Chemical_spill. Sample data: Sample data for Chemical problem.
VERBALIZED_EN: Caused by: Inadequate training. Consequences: Health impact. Creates risk: Chemical exposure. Sources: https://en.wikipedia.org/wiki/Chemical_spill. Sample data: Sample data for Chemical problem.
LINKS: causedBy hazards:Activity_InadequateTraining hasConsequence hazards:Consequence_HealthImpact createsRisk hazards:Risk_ChemicalExposure
RISK: id hazards:Risk_ChemicalExposure type hazards:Risk links verbalized_en
SOURCES: https://en.wikipedia.org/wiki/Chemical_spill
SAMPLE_DATA: Sample data for Chemical problem
RAW_JSON_TAIL: {"id": "hazards:Hazard_ChemicalRelease", "type": "hazards:Hazard", "labels": {"en": "Chemical release"}, "links": {"causedBy": ["hazards:Activity_InadequateTraining"], "hasConsequence": ["hazards:Consequence_HealthImpact"], "createsRisk": …
```
