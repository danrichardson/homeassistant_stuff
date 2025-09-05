# Home Assistant Battery Charging Automation

This script is a Home Assistant automation that **dynamically calculates how much energy your battery should target for charging today**, based on solar forecast, household load, and the time left until peak hours end.

---

## How It Works

### 1. Constants
- **battery_capacity**: `21.36` → Total usable battery capacity (kWh).  
- **efficiency**: `1` → Assumed charging/discharging efficiency (100%).  
- **load_kw**: `0.5` → Expected constant household load (kW).  
- **fill_rate**: `3` → Max charge rate (kW).  
- **end_of_peak_hour**: `21` → Peak pricing ends at 9 PM.  
- **max_hours_possible**: `19` → Max possible considered daylight/usage hours.  

---

### 2. Time Calculations
- **hours_remaining** → How many hours remain until 9 PM.  
- **reserve_at_end_of_peak** → Small reserve energy to leave in the battery at 9 PM, scaled by hours remaining.  

---

### 3. Energy Balance
- **current_soc** → Current stored energy (kWh).  
- **solar_forecast_ROD** → Forecasted solar generation for the rest of today.  
- **usable_solar** → Forecasted solar, adjusted for efficiency.  
- **day_drain** → Expected energy consumed by the load until 9 PM.  
- **required_energy** = `day_drain - usable_solar` → Extra energy needed beyond solar.  
- **total_energy_required** = `required_energy + reserve_at_end_of_peak`.  

---

### 4. Charging Requirement
- **charge_needed_raw** → Energy required to meet the target.  
- **charge_needed_clamped** → Same, but never negative.  
- **time_to_fill** → Time needed to charge enough (accounts for load).  
- **total_energy_required_adj** → Adjusted requirement including load during charging.  
- **target_soc** → Final target battery state (never exceeding capacity).  

---

### 5. Writes Values into Helpers
- `input_number.target_soc_kwh` → Battery charge target (kWh).  
- `input_number.required_energy_today` → Total energy needed today (load + reserve).  
- `input_number.charge_needed` → Charge amount required from grid/solar.  

---

## ✅ Summary
This automation calculates how much your battery should be charged to make it through the day until **9 PM (end of peak hours)**, considering:
- Current SOC  
- Expected solar generation  
- Household load  
- A reserve margin  

It then updates three input numbers that can be used in other automations:  
1. **Charge target (kWh)**  
2. **Required energy (kWh)**  
3. **Needed charge amount (kWh)**  

---

⚡ Tip: For clarity, you can run an example calculation (e.g., with `10 kWh` left in the battery, `8 hours` remaining, and `5 kWh` forecasted solar).  
