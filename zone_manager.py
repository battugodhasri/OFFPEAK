
import json
import os

ZONE_FILE = "zones.json"

def save_zones(zones, width, height):

    data = {
        "width": width,
        "height": height,
        "zones": zones
    }

    with open(ZONE_FILE, "w") as file:
        json.dump(data, file, indent=4)

    print("Zones saved successfully!")


def load_zones(width, height):

    if not os.path.exists(ZONE_FILE):
        return None

    # Check if file is empty
    if os.path.getsize(ZONE_FILE) == 0:
        print("Zone file is empty. Please draw zones again.")
        return None

    try:
        with open(ZONE_FILE, "r") as file:
            data = json.load(file)

        # Validate video dimensions
        if data["width"] != width or data["height"] != height:
            print("Video dimensions changed. Redraw zones.")
            return None

        zones = data["zones"]

        # Validate all three zones
        required_zones = ["Zone 1", "Zone 2", "Zone 3"]

        for zone in required_zones:
            if zone not in zones or len(zones[zone]) < 3:
                print("Invalid saved zones. Please redraw.")
                return None

        print("Saved zones loaded successfully!")
        return zones

    except (json.JSONDecodeError, KeyError, TypeError):
        print("Invalid zones.json. Please redraw zones.")
        return None
