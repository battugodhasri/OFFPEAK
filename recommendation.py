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

    print("Not enough data for recommendations.")
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
print("==========================================")
print("       OFFPEAK RECOMMENDATION ENGINE")
print("==========================================")


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
    # RISK
    # ------------------------------------------------

    if predicted_crowd >= HIGH_THRESHOLD:

        risk = "HIGH"

    elif predicted_crowd >= MEDIUM_THRESHOLD:

        risk = "MEDIUM"

    else:

        risk = "LOW"


    # ------------------------------------------------
    # TREND
    # ------------------------------------------------

    if change > 0:

        trend = "INCREASING"

    elif change < 0:

        trend = "DECREASING"

    else:

        trend = "STABLE"


    # ------------------------------------------------
    # RECOMMENDATION
    # ------------------------------------------------

    if risk == "HIGH" and trend == "INCREASING":

        recommendation = (
            "Activate crowd-control measures. "
            "Redirect visitors towards lower-density zones "
            "and increase monitoring."
        )

    elif risk == "MEDIUM" and trend == "INCREASING":

        recommendation = (
            "Increase monitoring in this zone. "
            "Consider guiding incoming visitors "
            "towards lower-density areas."
        )

    elif risk == "MEDIUM" and trend == "STABLE":

        recommendation = (
            "Maintain monitoring and keep crowd-management "
            "resources ready."
        )

    elif risk == "LOW" and trend == "DECREASING":

        recommendation = (
            "No immediate intervention required. "
            "Crowd is currently clearing."
        )

    elif risk == "LOW" and trend == "INCREASING":

        recommendation = (
            "Continue monitoring because crowd levels "
            "are beginning to increase."
        )

    else:

        recommendation = (
            "Maintain normal monitoring."
        )


    # ------------------------------------------------
    # DISPLAY
    # ------------------------------------------------

    print(f"\n{zone_name}")
    print("------------------------------------------")

    print(
        f"Current crowd      : {current_crowd}"
    )

    print(
        f"Predicted crowd    : {predicted_crowd}"
    )

    print(
        f"Expected change    : {change:+d}"
    )

    print(
        f"Trend              : {trend}"
    )

    print(
        f"Risk level         : {risk}"
    )

    print(
        f"Recommendation     : {recommendation}"
    )


# ------------------------------------------------
# END
# ------------------------------------------------

print("\n")
print("==========================================")
print("       RECOMMENDATION COMPLETE")
print("==========================================")