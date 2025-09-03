import yaml
import os

# Input and output paths
SOURCE_FILE = "automations.yaml"           # adjust if in another path
OUTPUT_DIR = "automations"

# Categories based on alias keywords
CATEGORIES = {
    "ac_control.yaml": ["AC When", "AC ", "Thermostat", "Cooling", "Heating", "Sleep"],
    "battery_protection.yaml": ["battery", "overloading", "Power Spiking", "Kitchen Overloading"],
    "solar.yaml": ["Solar", "Precharge", "Charging", "DC Input Voltage"],
    "windows.yaml": ["Windows", "window"],
    "ups.yaml": ["UPS"],
    "fans.yaml": ["Fan"],
    "fridge.yaml": ["Fridge"],
    "misc.yaml": []  # default catch-all
}

def categorize(alias):
    """Return filename based on alias keywords."""
    for filename, keywords in CATEGORIES.items():
        for word in keywords:
            if word.lower() in alias.lower():
                return filename
    return "misc.yaml"

def main():
    # Make output dir if not exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load automations.yaml
    with open(SOURCE_FILE, "r") as f:
        automations = yaml.safe_load(f)

    # Prepare buckets
    buckets = {f: [] for f in CATEGORIES.keys()}

    # Sort automations into categories
    for auto in automations:
        alias = auto.get("alias", "Unnamed")
        filename = categorize(alias)
        buckets[filename].append(auto)

    # Write each group to its file
    for filename, items in buckets.items():
        if not items:
            continue
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, "w") as f:
            yaml.dump(items, f, sort_keys=False)
        print(f"✅ Wrote {len(items)} automations to {path}")

if __name__ == "__main__":
    main()
