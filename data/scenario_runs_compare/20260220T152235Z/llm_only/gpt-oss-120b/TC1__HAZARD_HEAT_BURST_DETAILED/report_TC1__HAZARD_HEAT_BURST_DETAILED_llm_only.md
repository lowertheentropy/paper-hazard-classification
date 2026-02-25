# Report

- Method: `llm_only`
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
{"hazard":"Heat Burst"}
```

**Detailed Operator‑Style Report**

- **Observed anomalies / signatures**
  - Multiple nighttime calls reporting a sudden, brief surge of extremely warm air (mid‑80s °F) followed by rapid cooling.【Memory:1】
  - Accompanying dry conditions and gusty, strong downslope winds described as a “hot blast.”【Memory:1】
  - Humidity drops sharply during the temperature spike; wind gusts are brief (minutes).【Memory:1】

- **Why “Heat Burst” matches**
  - A heat burst is defined by an abrupt rise in temperature, rapid humidity decrease, and strong, dry downdrafts occurring typically at night—exactly the pattern reported.【Memory:1】
  - The observed “hot blast” with downslope wind aligns with the classic katabatic‑type outflow of a heat burst.【Memory:1】

- **Close alternatives & why rejected**
  1. **Microburst/Dry Microburst** – also produces strong gusts, but usually associated with thunderstorms and precipitation; no storm activity or rainfall was reported.【Memory:1】
  2. **Downsloping Windstorm (e.g., Chinook)** – can cause warm, dry winds, yet those events are sustained over longer periods rather than the brief minutes‑long spike described.【Memory:1】
  3. **Wildfire‑induced fire wind** – generates hot gusts but would be accompanied by visible fire or smoke; witnesses reported no wildfire.【Memory:1】

- **What would confirm/deny**
  - **Confirm:** High‑resolution temperature and humidity logs showing a rapid ≥30 °F rise within minutes, followed by an equally swift drop; wind profilers indicating strong downdraft velocities without preceding convection.
  - **Deny:** Radar or satellite detection of convective storms at the time (suggesting a microburst) or evidence of ongoing fire activity.

- **Operator Recommendations**
  - Log the event as a confirmed heat burst in the hazard database.
  - Notify aviation and surface‑transport agencies of potential brief turbulence/visibility impacts during night hours.
  - Deploy portable weather stations to capture future high‑frequency thermodynamic data for verification.

- **Further Information Links**  
  (References from the hazard card sources used for classification – not provided in current context; consult standard meteorological hazard catalogs for “Heat Burst.”)
