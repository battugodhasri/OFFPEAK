import pandas as pd
import numpy as np


# ------------------------------------------------
# LOAD CROWD DATA
# ------------------------------------------------

data = pd.read_csv("crowd_data.csv")

print("\nOFFPEAK CROWD PREDICTION")
print("------------------------")


# ------------------------------------------------
# CHECK DATA
# ------------------------------------------------

if len(data) < 3:

    print("\nNot enough data for prediction.")
    print("Run the crowd detection for a longer video.")
    exit()


# ------------------------------------------------
# SIMPLE LINEAR REGRESSION
# ------------------------------------------------

def predict_next(time_values, crowd_values, future_time):

    x = np.array(time_values, dtype=float)
    y = np.array(crowd_values, dtype=float)

    # Calculate slope and intercept
    slope, intercept = np.polyfit(x, y, 1)

    # Prediction
    prediction = slope * future_time + intercept

    return prediction


# ------------------------------------------------
# PREDICTION SETTINGS
# ------------------------------------------------

latest_time = data["video_time_seconds"].iloc[-1]

future_time = latest_time + 30


# ------------------------------------------------
# PREDICT EACH ZONE
# ------------------------------------------------

zones = {
    "Zone 1": "zone1",
    "Zone 2": "zone2",
    "Zone 3": "zone3"
}


for zone_name, column in zones.items():

    current_crowd = data[column].iloc[-1]

    predicted_crowd = predict_next(
        data["video_time_seconds"],
        data[column],
        future_time
    )

    predicted_crowd = max(
        0,
        round(predicted_crowd)
    )

    print(f"\n{zone_name}")

    print(
        f"Current crowd: {current_crowd}"
    )

    print(
        f"Predicted crowd after 30 seconds: "
        f"{predicted_crowd}"
    )


    # ------------------------------------------------
    # TREND
    # ------------------------------------------------

    if predicted_crowd > current_crowd:

        increase = predicted_crowd - current_crowd

        print(
            f"Trend: INCREASING (+{increase})"
        )

    elif predicted_crowd < current_crowd:

        decrease = current_crowd - predicted_crowd

        print(
            f"Trend: DECREASING (-{decrease})"
        )

    else:

        print(
            "Trend: STABLE"
        )


# ------------------------------------------------
# END
# ------------------------------------------------

print("\n------------------------")
print("Prediction completed.")
print("------------------------")