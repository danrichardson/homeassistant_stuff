import json
import shutil
from pathlib import Path

# --- CONFIGURATION ---
entity_registry_path = Path("./temp/core.entity_registry")

# --- BACKUP ---
backup_path = entity_registry_path.with_suffix(".backup.json")
shutil.copy(entity_registry_path, backup_path)
print(f"Backup created at {backup_path}")

# --- LOAD JSON ---
with open(entity_registry_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# --- REMOVE ENTITIES WITH disabled_by: "integration" ---
original_count = len(data.get("entities", []))
data["entities"] = [
    entity for entity in data.get("entities", [])
    if entity.get("disabled_by") != "integration"
]
removed_count = original_count - len(data["entities"])
print(f"Removed {removed_count} entities with 'disabled_by: integration'.")

# --- SAVE MODIFIED FILE ---
with open(entity_registry_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Entity registry updated. Please restart Home Assistant.")
