import json
import yaml
import os

SOURCE_FILE = "core.config_entries"
OUTPUT_DIR = "./helpers"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(SOURCE_FILE, "r") as f:
    data = json.load(f)

entries = data.get("data", {}).get("entries", [])

for entry in entries:
    domain = entry.get("domain", "unknown")
    # Create a directory for this domain
    domain_dir = os.path.join(OUTPUT_DIR, domain)
    os.makedirs(domain_dir, exist_ok=True)

    # Use title or unique_id or entry_id as the filename
    name = entry.get("title") or entry.get("unique_id") or entry.get("entry_id")
    filename_safe = "".join(c if c.isalnum() or c in "_-" else "_" for c in name)
    file_path = os.path.join(domain_dir, f"{filename_safe}.json")

    # Save pretty-printed JSON
    with open(file_path, "w") as f:
        json.dump(entry, f, indent=2, sort_keys=False)

    print(f"✅ Saved entry '{name}' in domain folder '{domain}'")

print(f"✅ Done! {len(entries)} entries exported into {len(set(e.get('domain','unknown') for e in entries))} domain folders.")
