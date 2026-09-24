import pandas as pd
import numpy as np


# ------------------------------------------------
# LOAD CROWD DATA
# ------------------------------------------------

data = pd.read_csv("crowd_data.csv")


# ------------------------------------------------
# CHECK DATA
# ------------------------------------------------

if len(data) < 3:

    print("Not enough data for risk analysis.")
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
# SETTINGS
# ------------------------------------------------

latest_time = data["video_time_seconds"].iloc[-1]

future_time = latest_time + 30


# Crowd thresholds
MEDIUM_THRESHOLD = 20
HIGH_THRESHOLD = 30


# ------------------------------------------------
# ZONES
# ------------------------------------------------

zones = {
    "Zone 1": "zone1",
    "Zone 2": "zone2",
    "Zone 3": "zone3"
}


# ------------------------------------------------
# HEADER
# ------------------------------------------------

print("\n")
print("====================================")
print("       OFFPEAK RISK ANALYSIS")
print("====================================")


# ------------------------------------------------
# ANALYZE EACH ZONE
# ------------------------------------------------

for zone_name, column in zones.items():

    current_crowd = int(
        data[column].iloc[-1]
    )

    predicted_crowd = predict_next(
        data["video_time_seconds"],
        data[column],
        future_time
    )

    change = predicted_crowd - current_crowd


    # ------------------------------------------------
    # DETERMINE RISK
    # ------------------------------------------------

    if predicted_crowd >= HIGH_THRESHOLD:

        risk = "HIGH"

    elif predicted_crowd >= MEDIUM_THRESHOLD:

        risk = "MEDIUM"

    else:

        risk = "LOW"


    # ------------------------------------------------
    # DETERMINE TREND
    # ------------------------------------------------

    if change > 0:

        trend = "INCREASING"

    elif change < 0:

        trend = "DECREASING"

    else:

        trend = "STABLE"


    # ------------------------------------------------
    # DISPLAY RESULT
    # ------------------------------------------------

    print("\n" + zone_name)

    print("----------------------------")

    print(
        f"Current crowd     : {current_crowd}"
    )

    print(
        f"Predicted crowd   : {predicted_crowd}"
    )

    print(
        f"Expected change   : {change:+d}"
    )

    print(
        f"Trend             : {trend}"
    )

    print(
        f"Risk level        : {risk}"
    )


    # ------------------------------------------------
    # BOTTLENECK WARNING
    # ------------------------------------------------

    if risk == "HIGH" and trend == "INCREASING":

        print(
            "WARNING: Potential bottleneck developing!"
        )

    elif risk == "MEDIUM" and trend == "INCREASING":

        print(
            "WARNING: Crowd is building up."
        )

    elif risk == "LOW" and trend == "DECREASING":

        print(
            "Status: Crowd is clearing."
        )

    else:

        print(
            "Status: Crowd currently manageable."
        )


# ------------------------------------------------
# END
# ------------------------------------------------

print("\n")
print("====================================")
print("       RISK ANALYSIS COMPLETE")
print("====================================")