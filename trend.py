import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------------------------
# LOAD CROWD DATA
# ------------------------------------------------

data = pd.read_csv("crowd_data.csv")

print("\nCrowd Data:")
print(data)


# ------------------------------------------------
# CROWD TREND
# ------------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    data["video_time_seconds"],
    data["zone1"],
    marker="o",
    label="Zone 1"
)

plt.plot(
    data["video_time_seconds"],
    data["zone2"],
    marker="o",
    label="Zone 2"
)

plt.plot(
    data["video_time_seconds"],
    data["zone3"],
    marker="o",
    label="Zone 3"
)

plt.plot(
    data["video_time_seconds"],
    data["total"],
    marker="o",
    label="Total"
)

plt.xlabel("Video Time (seconds)")
plt.ylabel("Number of People")

plt.title("OFFPEAK - Crowd Trend")

plt.legend()
plt.grid(True)

plt.tight_layout()

plt.show()


# ------------------------------------------------
# BASIC TREND ANALYSIS
# ------------------------------------------------

print("\n-----------------------------")
print("OFFPEAK CROWD TREND ANALYSIS")
print("-----------------------------")


if len(data) >= 2:

    # First and latest values
    first = data.iloc[0]
    latest = data.iloc[-1]

    print(
        f"\nTime analysed: "
        f"{first['video_time_seconds']}s "
        f"to "
        f"{latest['video_time_seconds']}s"
    )

    # Zone 1
    if latest["zone1"] > first["zone1"]:
        print("Zone 1: CROWD INCREASING")
    elif latest["zone1"] < first["zone1"]:
        print("Zone 1: CROWD DECREASING")
    else:
        print("Zone 1: CROWD STABLE")

    # Zone 2
    if latest["zone2"] > first["zone2"]:
        print("Zone 2: CROWD INCREASING")
    elif latest["zone2"] < first["zone2"]:
        print("Zone 2: CROWD DECREASING")
    else:
        print("Zone 2: CROWD STABLE")

    # Zone 3
    if latest["zone3"] > first["zone3"]:
        print("Zone 3: CROWD INCREASING")
    elif latest["zone3"] < first["zone3"]:
        print("Zone 3: CROWD DECREASING")
    else:
        print("Zone 3: CROWD STABLE")

    # Total
    if latest["total"] > first["total"]:
        print("TOTAL CROWD: INCREASING")
    elif latest["total"] < first["total"]:
        print("TOTAL CROWD: DECREASING")
    else:
        print("TOTAL CROWD: STABLE")

else:

    print(
        "\nNot enough data for trend analysis."
    )
    print(
        "Run the crowd detection for a longer video."
    )