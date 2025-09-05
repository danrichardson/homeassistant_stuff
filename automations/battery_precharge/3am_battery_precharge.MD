### 3am Battery Precharge Calculation - AC500

**Purpose:**  
Automatically decides whether the AC500 battery should precharge from the grid in the early morning, based on current state of charge (SOC), solar forecast, and daily energy requirements.

**Triggers: (any of the following)**  
- Time-based: 03:00, 04:00, 05:00, 06:00  
- Sensor update: `sensor.solcast_pv_forecast_forecast_remaining_today`  

**Conditions: (and has to be all of these)**  
- Weekdays only (Monday–Friday)  
- Between 04:00 and 15:59  

**Actions:**  
1. Calls `script.set_target_soc` to calculate the battery target SOC and required energy.  
2. Stores relevant variables: current SOC, solar forecast, required energy, and target SOC.  
3. Decision logic:
   - **If target SOC > current SOC** → charging is required:
     - Sends a mobile notification with SOC, forecast, required energy, and target SOC.  
     - Sets AC500 UPS mode to `STANDARD` (grid charging allowed).  
   - **Else** → enough charge available:
     - Optionally sends a notification (currently disabled).  
     - Sets AC500 UPS mode to `PV_PRIORITY` (solar-only charging).  

**Mode:** `single` – prevents overlapping runs.

**Summary:**  
This automation ensures your battery is precharged as needed before peak hours, prioritizing grid charging only when necessary and otherwise using solar generation efficiently.
