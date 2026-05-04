#!/usr/bin/env python3
"""Add unofficial NVMe SSD to Synology DS925+ compatibility database.

Tested on DSM 7.3.2-86009-3 with Samsung PM9A1 MZVLQ128HBHQ-000 x2.

Note: 007revad/Synology_HDD_db script fails on DS925+ v7 DB (parse error).
      This script directly edits the JSON DB files as a workaround.
"""

import json
import shutil
import sys

NAS_MODEL = "ds925+"
SSD_MODEL = "SAMSUNG MZVLQ128HBHQ-000"
SSD_FW = "FXV70K0Q"
SSD_SIZE_GB = 128

DB_PATHS = [
    f"/var.defaults/lib/disk-compatibility/{NAS_MODEL}_host_v7.db",
    f"/var/lib/disk-compatibility/{NAS_MODEL}_host_v7.db",
]

# Exact entry that worked on DSM 7.3.2
SSD_ENTRY = {
    SSD_MODEL: {
        SSD_FW: {
            "size_gb": SSD_SIZE_GB,
            "compatibility_interval": [
                {
                    "compatibility": "compatible",
                    "not_after": "",
                    "fw_dsm_update_status": "not_required",
                    "not_before": ""
                }
            ],
            "support_m2_volume": True,
            "support_ssd_cache": True,
            "support_trim": True
        }
    }
}


def backup(path):
    bak = path + ".bak"
    if not shutil.exists(bak):
        shutil.copy2(path, bak)
        print(f"Backed up: {bak}")


def add_ssd(path):
    try:
        with open(path, "r") as f:
            db = json.load(f)
    except json.JSONDecodeError as e:
        print(f"ERROR: {path} is corrupt: {e}")
        # Try restoring from backup
        bak = path + ".bak"
        if shutil.exists(bak):
            print(f"Restoring from {bak}...")
            shutil.copy2(bak, path)
            with open(path, "r") as f:
                db = json.load(f)
        else:
            return False

    if SSD_MODEL in db.get("disk_compatbility_info", {}):
        print(f"Already exists: {SSD_MODEL} in {path}")
        return True

    db.setdefault("disk_compatbility_info", {}).update(SSD_ENTRY)

    with open(path, "w") as f:
        json.dump(db, f)

    # Verify
    with open(path, "r") as f:
        d = json.load(f)
    if SSD_MODEL in d.get("disk_compatbility_info", {}):
        print(f"OK: {SSD_MODEL} added to {path}")
        return True
    else:
        print(f"FAILED: {path}")
        return False


def main():
    print(f"Adding {SSD_MODEL} ({SSD_FW}) to {NAS_MODEL} compatibility DB...")
    success = True
    for path in DB_PATHS:
        try:
            backup(path)
            if not add_ssd(path):
                success = False
        except FileNotFoundError:
            print(f"SKIP: {path} not found")
        except PermissionError:
            print(f"ERROR: Need sudo for {path}")
            success = False

    if success:
        print("\nDone! Reboot NAS to apply changes.")
    else:
        print("\nSome errors occurred. Check output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
