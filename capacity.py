import pandas as pd
import numpy as np


# ------------------------------------------------
# LOAD CROWD DATA
# ------------------------------------------------

data = pd.read_csv("crowd_data.csv")

if len(data) < 3:
    print("Not enough data.")
    print("Run main.py for a longer duration.")
    exit()


# ------------------------------------------------
# PREDICTION FUNCTION
# ------------------------------------------------

def predict_next(time_values, crowd_values, future_time):

    x = np.array(time_values, dtype=float)
    y = np.array(crowd_values, dtype=float)

    slope, intercept = np.polyfit(x, y, 1)

    prediction = slope * future_time + intercept

    return max(0, round(prediction))


# ------------------------------------------------
# ZONE CAPACITIES
# ------------------------------------------------

capacities = {
    "Zone 1": 30,
    "Zone 2": 15,
    "Zone 3": 30
}


zones = {
    "Zone 1": "zone1",
    "Zone 2": "zone2",
    "Zone 3": "zone3"
}


# ------------------------------------------------
# PREDICT CROWD
# ------------------------------------------------

latest_time = data["video_time_seconds"].iloc[-1]

future_time = latest_time + 30

predictions = {}

for zone_name, column in zones.items():

    predictions[zone_name] = predict_next(
        data["video_time_seconds"],
        data[column],
        future_time
    )


# ------------------------------------------------
# DISPLAY ZONE STATUS
# ------------------------------------------------

print("\n")
print("==========================================")
print("        OFFPEAK CAPACITY ANALYSIS")
print("==========================================")


for zone_name in zones:

    predicted = predictions[zone_name]
    capacity = capacities[zone_name]

    available = capacity - predicted

    utilization = (
        predicted / capacity
    ) * 100

    print("\n" + zone_name)
    print("------------------------------------------")

    print(
        f"Capacity           : {capacity}"
    )

    print(
        f"Predicted crowd    : {predicted}"
    )

    print(
        f"Available capacity : {max(0, available)}"
    )

    print(
        f"Utilization        : {round(utilization, 1)}%"
    )


    # ------------------------------------------------
    # CAPACITY STATUS
    # ------------------------------------------------

    if utilization >= 100:

        status = "OVER CAPACITY"

    elif utilization >= 80:

        status = "NEAR CAPACITY"

    elif utilization >= 50:

        status = "MODERATE"

    else:

        status = "AVAILABLE"

    print(
        f"Status             : {status}"
    )


# ------------------------------------------------
# FIND BEST AVAILABLE ZONE
# ------------------------------------------------

available_zones = []

for zone_name in zones:

    predicted = predictions[zone_name]
    capacity = capacities[zone_name]

    remaining = capacity - predicted

    if remaining > 0:

        available_zones.append(
            (zone_name, remaining)
        )


# Sort by most available capacity

available_zones.sort(
    key=lambda x: x[1],
    reverse=True
)


# ------------------------------------------------
# RECOMMENDATION
# ------------------------------------------------

print("\n")
print("==========================================")
print("        OFFPEAK SMART RECOMMENDATION")
print("==========================================")


# Find zones that need attention

for zone_name in zones:

    predicted = predictions[zone_name]
    capacity = capacities[zone_name]

    utilization = (
        predicted / capacity
    ) * 100

    if utilization >= 80:

        # Find another available zone
        alternative = None

        for candidate, remaining in available_zones:

            if candidate != zone_name:

                alternative = candidate

                break


        print("\n" + zone_name)

        if utilization >= 100:

            print(
                "WARNING: Zone is predicted to exceed capacity."
            )

        else:

            print(
                "WARNING: Zone is approaching capacity."
            )


        if alternative:

            print(
                f"Recommendation: Guide incoming "
                f"visitors towards {alternative}."
            )

        else:

            print(
                "Recommendation: No suitable "
                "alternative zone available."
            )


# ------------------------------------------------
# END
# ------------------------------------------------

print("\n")
print("==========================================")
print("        CAPACITY ANALYSIS COMPLETE")
print("==========================================")