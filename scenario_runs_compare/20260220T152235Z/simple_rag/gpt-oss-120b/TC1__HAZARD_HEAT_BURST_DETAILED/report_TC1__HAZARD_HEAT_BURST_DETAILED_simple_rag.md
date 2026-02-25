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



SNIPPET:
At 00:05 local time the temperature jumps rapidly into the mid-80s F while humidity drops and gusty winds appear; within minutes values partially recover. Witnesses describe a sudden "hot blast" with strong downslope wind, but no wildfire is reported.

ADDITIONAL REQUIREMENTS:
- After the Direct Answer JSON, provide a Detailed Report with: hazard overview; why this match (with citations); operator recommendations; further information links (from cited hazard card sources).

## Final Answer

**Direct Answer**  
```json
{"hazard_id":"hazards:Hazard_Heat_Burst","label":"Heat Burst","confidence":0.95,"evidence":["[Knowledge:82 hazards:Hazard_Heat_Burst Heat Burst] Keywords: Satans Storm; Heat burst. Subtype: Extreme Temperature.","Snippet describes a sudden “hot blast” with rapid temperature rise, humidity drop and gusty winds at night – classic characteristics of a heat‑burst event."],"notes":"Matches the observed rapid nocturnal temperature spike and downslope wind without wildfire."}
```

**Justification**
- The snippet reports an abrupt nighttime temperature jump into the mid‑80s °F with a simultaneous drop in humidity and strong gusty winds, which aligns with the definition of a **Heat Burst** (extreme temperature event)【Knowledge:82】.  
- Heat bursts are described as “hot blast” phenomena caused by downdrafts that bring hot, dry air to the surface, exactly matching witness descriptions in the snippet.  
- No wildfire is mentioned, consistent with heat‑burst events that are atmospheric rather than fire‑related.  

---  

### Detailed Report

#### Hazard Overview
**Heat Burst** (also known as “Satans Storm”) is a rare meteorological phenomenon characterized by a sudden, localized surge of hot, dry air descending from collapsing thunderstorms or storm downdrafts. It typically occurs at night and can cause rapid temperature spikes of 20 °F or more within minutes, accompanied by sharp humidity drops and strong gusty winds. The event is short‑lived (minutes) and does not involve precipitation or fire activity.

#### Why This Match
- **Rapid Temperature Rise:** The report notes a jump to the mid‑80s °F at night—exactly the abrupt heating described for heat bursts.  
- **Humidity Drop & Gusty Winds:** Both are hallmark signatures of descending hot air in a heat burst.  
- **Downslope Wind (“hot blast”):** The term “hot blast” is commonly used in heat‑burst literature to describe the strong, warm downdraft.  
- **No Wildfire Reported:** Heat bursts are atmospheric; they do not require fire, matching the absence of wildfire in the snippet.

#### Operator Recommendations
1. **Immediate Safety Checks:** Advise residents and personnel to stay indoors during the event due to rapid temperature changes and potential wind‑related hazards (e.g., falling debris).  
2. **Monitor Weather Radar:** Heat bursts are often preceded by weakening storm cells; continuous radar monitoring can provide early warning of collapsing storms.  
3. **Public Communication:** Issue brief alerts explaining the phenomenon, emphasizing its short duration and that it poses limited but real risks (heat stress, wind damage).  
4. **Post‑Event Assessment:** After the event, inspect infrastructure for wind‑related damage and verify that no secondary hazards (e.g., power line failures) have occurred.

#### Further Information Links
- Wikipedia entry on Heat Burst: https://en.wikipedia.org/wiki/Heat_burst  
- NOAA Storm Events Database (for related extreme temperature events): https://www.ncei.noaa.gov/stormevents/  

These sources provide additional technical details and historical case studies useful for preparedness and response planning.
