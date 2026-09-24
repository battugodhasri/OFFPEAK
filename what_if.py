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

    print("Not enough data for simulation.")
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
# CURRENT DATA
# ------------------------------------------------

latest_time = data["video_time_seconds"].iloc[-1]

future_time = latest_time + 30


zone2_current = int(data["zone2"].iloc[-1])
zone3_current = int(data["zone3"].iloc[-1])


# ------------------------------------------------
# PREDICT CURRENT SITUATION
# ------------------------------------------------

zone2_predicted = predict_next(
    data["video_time_seconds"],
    data["zone2"],
    future_time
)

zone3_predicted = predict_next(
    data["video_time_seconds"],
    data["zone3"],
    future_time
)


# ------------------------------------------------
# WHAT-IF INPUT
# ------------------------------------------------

print("\n")
print("==========================================")
print("          OFFPEAK WHAT-IF SIMULATOR")
print("==========================================")

print("\nCurrent situation:")
print(f"Zone 2 current crowd : {zone2_current}")
print(f"Zone 3 current crowd : {zone3_current}")

print("\nPredicted in 30 seconds:")
print(f"Zone 2 : {zone2_predicted}")
print(f"Zone 3 : {zone3_predicted}")


# ------------------------------------------------
# USER INPUT
# ------------------------------------------------

print("\n------------------------------------------")
print("SIMULATION")
print("------------------------------------------")

try:

    diversion_percentage = float(
        input(
            "\nEnter percentage of Zone 3 visitors "
            "to redirect to Zone 2 (0-100): "
        )
    )

except ValueError:

    print("Please enter a valid number.")
    exit()


# Keep percentage within valid range

if diversion_percentage < 0:
    diversion_percentage = 0

if diversion_percentage > 100:
    diversion_percentage = 100


# ------------------------------------------------
# CALCULATE DIVERSION
# ------------------------------------------------

diverted_people = round(
    zone3_predicted * diversion_percentage / 100
)


# ------------------------------------------------
# SIMULATED CROWD
# ------------------------------------------------

simulated_zone3 = (
    zone3_predicted - diverted_people
)

simulated_zone2 = (
    zone2_predicted + diverted_people
)


# ------------------------------------------------
# RESULTS
# ------------------------------------------------

print("\n")
print("==========================================")
print("          SIMULATION RESULT")
print("==========================================")


print("\nWITHOUT INTERVENTION")

print(
    f"Zone 2 predicted : {zone2_predicted}"
)

print(
    f"Zone 3 predicted : {zone3_predicted}"
)


print("\nWITH INTERVENTION")

print(
    f"Visitors redirected : {diverted_people}"
)

print(
    f"Zone 2 simulated    : {simulated_zone2}"
)

print(
    f"Zone 3 simulated    : {simulated_zone3}"
)


# ------------------------------------------------
# IMPACT
# ------------------------------------------------

print("\n------------------------------------------")
print("IMPACT")
print("------------------------------------------")

print(
    f"Zone 3 crowd reduced by "
    f"{diverted_people} people."
)

print(
    f"Zone 2 crowd increased by "
    f"{diverted_people} people."
)


# ------------------------------------------------
# SIMPLE INTERPRETATION
# ------------------------------------------------

if diverted_people == 0:

    print(
        "\nNo intervention was applied."
    )

elif simulated_zone3 < zone3_predicted:

    print(
        "\nSimulation indicates reduced "
        "crowd pressure in Zone 3."
    )

    print(
        "Authority can compare this scenario "
        "before taking action."
    )


# ------------------------------------------------
# END
# ------------------------------------------------

print("\n")
print("==========================================")
print("       WHAT-IF SIMULATION COMPLETE")
print("==========================================")