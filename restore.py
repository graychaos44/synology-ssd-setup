#!/usr/bin/env python3
"""Restore Synology compatibility DB from backup."""

import shutil
import sys

NAS_MODEL = "ds925+"
DB_PATHS = [
    f"/var.defaults/lib/disk-compatibility/{NAS_MODEL}_host_v7.db",
    f"/var/lib/disk-compatibility/{NAS_MODEL}_host_v7.db",
]

def main():
    for path in DB_PATHS:
        bak = path + ".bak"
        try:
            shutil.copy2(bak, path)
            print(f"Restored: {path}")
        except FileNotFoundError:
            print(f"No backup: {bak}")
        except PermissionError:
            print(f"Need sudo: {path}")

    print("\nDone! Reboot NAS to apply.")

if __name__ == "__main__":
    main()
