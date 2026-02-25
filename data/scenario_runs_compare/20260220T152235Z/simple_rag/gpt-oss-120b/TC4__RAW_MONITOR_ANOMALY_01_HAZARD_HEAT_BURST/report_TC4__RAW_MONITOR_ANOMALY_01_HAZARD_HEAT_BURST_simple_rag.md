# Report

- Method: `simple_rag`
- Model: `gpt-oss-120b`

## Question

Hazard classification (Top-1). Use ONLY CONTEXT as evidence.

    Output requirements:
    - Direct Answer: ONE-LINE JSON as specified by the simple-rag prompt.
    - After the JSON, write a detailed, operator-style report:
      * Observed anomalies / signatures (bullet list)
      * Why the chosen hazard matches (cite specific retrieved fields: sampleData, keywords/altLabel, triggers/causes, impacts)
      * 1–3 close alternatives and why they were rejected (with citations)
      * What would confirm/deny (additional measurements / logs).

    No natural-language hints are provided. Treat the snippet as raw telemetry; infer the most plausible hazard label from the pattern.

    SNIPPET:
    temp_F,dewpoint_F,RH_pct,wind_sust_mph,wind_gust_mph,pressure_hPa,precip_in
00:00,84.2,66.1,56,6,10,1009.9,0.00
00:05,84.0,66.0,56,6,10,1010.0,0.00
00:10,83.6,65.8,57,6,10,1010.0,0.00
00:15,83.2,65.6,57,6,11,1010.1,0.00
00:20,82.9,65.5,58,6,11,1010.1,0.00
00:25,82.6,65.4,58,6,10,1010.2,0.00
00:30,82.3,65.2,59,6,10,1010.2,0.00
00:35,86.8,58.0,40,10,18,1010.6,0.00
00:40,92.9,49.5,26,14,26,1011.0,0.00
00:45,97.6,42.8,17,17,33,1011.5,0.00
00:50,100.1,38.7,13,19,37,1011.8,0.00
00:55,101.2,35.6,11,20,40,1012.0,0.00
01:00,100.4,36.8,12,19,38,1011.9,0.00
01:05,97.2,41.7,17,16,31,1011.6,0.00
01:10,93.1,48.9,25,13,24,1011.2,0.00
01:15,89.0,55.7,35,10,18,1010.9,0.00

ADDITIONAL REQUIREMENTS:
- After the Direct Answer JSON, provide a Detailed Report with: hazard overview; why this match (with citations); operator recommendations; further information links (from cited hazard card sources).

## Final Answer

**Direct Answer**
```json
{"hazard_id":"hazards:Hazard_Heat_Burst","label":"Heat Burst","confidence":0.95,"evidence":["[Memory:1 #000091 Dispatch center/call] Multiple calls reporting sudden heat/wind gusts during the night. Reports of briefly extremely warm air, dry, gusty wind; after a few minutes, cooling.","[Knowledge:82 hazards:Hazard_Heat_Burst Heat Burst] HAZARD_ID: hazards:Hazard_Heat_Burst LABEL: Heat Burst ... Keywords: Satans Storm."] ,"notes":"Rapid temperature rise with concurrent wind gusts and humidity drop matches classic heat‑burst signatures."}
```

**Detailed Report**

**1. Hazard Overview**  
- **Name / Label:** Heat Burst (also known as “Satans Storm”).  
- **Group / Subtype:** Meteorological – Extreme Temperature.  
- **Typical Characteristics:** Sudden, short‑duration spikes in temperature (often >30 °C increase) accompanied by strong wind gusts and a rapid drop in relative humidity and dew point. Occurs usually at night after rain‑related downdrafts dissipate.  

**2. Why this snippet matches the Heat Burst hazard**  
- **Rapid Temperature Increase:** The observations show temperature climbing from ~82 °F (27.8 °C) at 00:30 to a peak of 101 °F (38.3 °C) by 00:55 – an increase of ≈19 °F (≈10 °C) within 25 minutes, exactly the abrupt heating described for heat bursts.  
- **Wind Gust Spike:** Wind gusts rise from a steady ~6 mph to 20 mph at the temperature peak, matching the “gusty wind” component of heat bursts.  
- **Humidity & Dew‑point Drop:** Relative humidity falls from ~59 % to 11 % and dew point drops from 65 °F to 35 °F, indicating rapid drying of the air column – a hallmark of descending, evaporatively cooled air that then compresses and heats.  
- **Temporal Pattern:** The event occurs during nighttime hours (00:00‑01:15), consistent with heat bursts which are most common after nocturnal rain showers.  

These observations align directly with the definition and keywords in the Heat Burst hazard card ([Knowledge:82]).

**3. Operator Recommendations**  
| Action | Rationale |
|--------|-----------|
| **Issue Immediate Public Advisory** warning of sudden temperature spikes and strong gusts, especially for outdoor workers and vulnerable populations. | Rapid heating can cause heat‑related stress or equipment failure. |
| **Monitor Nearby Radar/Weather Sensors** for residual precipitation that may have triggered the downdraft. | Heat bursts are often linked to dissipating rain showers; confirming this helps forecast recurrence. |
| **Activate Wind‑Related Safety Protocols** (e.g., secure loose objects, advise pilots of sudden gusts). | Gusts up to 20 mph can affect low‑flying aircraft and unsecured structures. |
| **Log the Event in Hazard Database** with precise timestamps for future climatological analysis. | Heat bursts are rare; detailed records improve statistical understanding. |
| **Prepare Cooling Measures** (e.g., hydration stations) if the event persists or repeats. | Even short‑duration extreme heat can pose health risks. |

**4. Further Information Links**  
- Wikipedia entry on Heat Burst: https://en.wikipedia.org/wiki/Heat_burst  
- Eric’s Weather Library overview of Heat Bursts (sample data): https://www.ericsweatherlibrary.com  
- NOAA Storm Events Database for related nocturnal downdraft events.  

These resources provide deeper scientific background and historical case studies useful for training, risk assessment, and public communication.
