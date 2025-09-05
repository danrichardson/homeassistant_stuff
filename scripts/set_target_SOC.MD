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

## Summary
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

# Battery Charge Calculation at 5 AM

## Assumptions

- **Battery capacity:** 21.36 kWh  
- **Current SOC:** 10.0 kWh  
- **House load:** 0.5 kW  
- **Max charge rate:** 3 kW  
- **Solar forecast (remaining today):** 5.0 kWh  
- **Peak hours end:** 9:00 PM  

---

## Step-by-Step Calculation

### Step 1 — Hours left until 9 PM
21 - 5 = 16 hours  
`hours_remaining = 16`

### Step 2 — Reserve at end of peak
reserve_at_end_of_peak = 2 * (hours_remaining / max_hours_possible)  
= 2 * (16 / 19)  
≈ 1.68 kWh

### Step 3 — Daytime load demand
day_drain = load_kw * hours_remaining  
= 0.5 * 16  
= 8.0 kWh

### Step 4 — Net required energy (load minus solar)
required_energy = day_drain - usable_solar  
= 8.0 - 5.0  
= 3.0 kWh

### Step 5 — Add reserve margin
total_energy_required = required_energy + reserve_at_end_of_peak  
= 3.0 + 1.68  
≈ 4.68 kWh

### Step 6 — Compare to current SOC
charge_needed_raw = total_energy_required - current_soc  
= 4.68 - 10.0  
= -5.32  

Clamp at 0:  
`charge_needed_clamped = 0`

### Step 7 — Time to fill
Since no charging is needed:  
`time_to_fill = 0`

### Step 8 — Adjusted total energy
total_energy_required_adj = max(total_energy_required + (time_to_fill * load_kw), 0)  
= max(4.68 + 0, 0)  
= 4.68

### Step 9 — Target SOC
target_soc = min(total_energy_required_adj, battery_capacity)  
= min(4.68, 21.36)  
= 4.68 kWh

---

## Final Values

| Variable                             | Value                           |
|--------------------------------------|---------------------------------:|
| `input_number.target_soc_kwh`        | 4.7                             |
| `input_number.required_energy_today` | 9.7 (8.0 load + 1.7 reserve)    |
| `input_number.charge_needed`         | 0.0                             |

---

**Interpretation:**  
At 5 AM, since the battery already has 10 kWh stored (well above the ~4.7 kWh target needed), the script decides **no charging is needed today**.

