import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="OFFPEAK",
    page_icon="🌐",
    layout="wide"
)

st.title("OFFPEAK")
st.subheader("Live Crowd Monitoring")

st.write(
    "Dashboard connected to the live YOLO crowd detection."
)


@st.fragment(run_every="2s")
def live_dashboard():

    try:
        data = pd.read_csv("live_data.csv")

    except FileNotFoundError:
        st.error("live_data.csv not found.")
        return

    if len(data) == 0:
        st.warning("Waiting for crowd data...")
        return


    # --------------------------------------------
    # LATEST DATA
    # --------------------------------------------

    latest = data.iloc[-1]

    zone1 = int(latest["zone1"])
    zone2 = int(latest["zone2"])
    zone3 = int(latest["zone3"])
    total = int(latest["total"])

    video_time = float(
        latest["video_time_seconds"]
    )


    # --------------------------------------------
    # LIVE COUNTS
    # --------------------------------------------

    st.header("🔴 Live Crowd")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Zone 1", zone1)

    with col2:
        st.metric("Zone 2", zone2)

    with col3:
        st.metric("Zone 3", zone3)

    with col4:
        st.metric("Total", total)

    st.write(
        f"Video time: **{video_time:.2f} seconds**"
    )


    # --------------------------------------------
    # CROWD MOVEMENT GRAPH
    # --------------------------------------------

    st.header("📈 Crowd Movement")

    chart_data = data[
        [
            "video_time_seconds",
            "zone1",
            "zone2",
            "zone3"
        ]
    ].copy()

    chart_data = chart_data.set_index(
        "video_time_seconds"
    )

    chart_data.columns = [
        "Zone 1",
        "Zone 2",
        "Zone 3"
    ]

    st.line_chart(chart_data)


    # --------------------------------------------
    # 30-SECOND PREDICTION
    # --------------------------------------------

    st.header("🔮 Crowd Prediction")

    prediction_columns = {
        "Zone 1": "zone1",
        "Zone 2": "zone2",
        "Zone 3": "zone3"
    }

    prediction_results = {}


    for zone_name, column in prediction_columns.items():

        zone_data = data[
            [
                "video_time_seconds",
                column
            ]
        ].dropna()


        if len(zone_data) < 3:

            prediction_results[zone_name] = {
                "current": int(latest[column]),
                "predicted": None,
                "change": None,
                "trend": "WAITING"
            }

            continue


        x = zone_data[
            "video_time_seconds"
        ].values

        y = zone_data[column].values


        # Calculate linear trend
        slope, intercept = np.polyfit(
            x,
            y,
            1
        )


        current = int(latest[column])

        current_time = video_time

        future_time = current_time + 30


        predicted = (
            slope * future_time
            + intercept
        )


        # Crowd cannot be negative
        predicted = max(
            0,
            round(predicted)
        )


        change = predicted - current


        if change > 2:
            trend = "INCREASING"

        elif change < -2:
            trend = "DECREASING"

        else:
            trend = "STABLE"


        prediction_results[zone_name] = {
            "current": current,
            "predicted": predicted,
            "change": change,
            "trend": trend
        }


    # --------------------------------------------
    # PREDICTION DISPLAY
    # --------------------------------------------

    col1, col2, col3 = st.columns(3)


    for col, zone_name in zip(
        [col1, col2, col3],
        ["Zone 1", "Zone 2", "Zone 3"]
    ):

        result = prediction_results[zone_name]

        with col:

            st.subheader(zone_name)

            st.metric(
                "Current Crowd",
                result["current"]
            )


            if result["predicted"] is None:

                st.info(
                    "Collecting more data..."
                )

            else:

                st.metric(
                    "Predicted in 30 sec",
                    result["predicted"],
                    delta=result["change"]
                )

                st.write(
                    f"Trend: **{result['trend']}**"
                )


    # --------------------------------------------
    # CAPACITY SETTINGS
    # --------------------------------------------

    capacities = {
        "Zone 1": 30,
        "Zone 2": 15,
        "Zone 3": 30
    }


    # --------------------------------------------
    # RISK LEVEL
    # --------------------------------------------

    st.header("🚦 Crowd Risk")

    risk_results = {}


    for zone_name in [
        "Zone 1",
        "Zone 2",
        "Zone 3"
    ]:

        result = prediction_results[zone_name]

        capacity = capacities[zone_name]


        if result["predicted"] is None:

            risk = "WAITING"
            percentage = 0

        else:

            predicted = result["predicted"]

            percentage = (
                predicted / capacity
            ) * 100


            if percentage >= 100:

                risk = "HIGH"

            elif percentage >= 70:

                risk = "MEDIUM"

            else:

                risk = "LOW"


        risk_results[zone_name] = {
            "risk": risk,
            "percentage": percentage,
            "capacity": capacity
        }


    # --------------------------------------------
    # RISK DISPLAY
    # --------------------------------------------

    col1, col2, col3 = st.columns(3)


    for col, zone_name in zip(
        [col1, col2, col3],
        ["Zone 1", "Zone 2", "Zone 3"]
    ):

        result = risk_results[zone_name]

        with col:

            st.subheader(zone_name)

            risk = result["risk"]

            if risk == "HIGH":

                st.error(
                    "🔴 HIGH RISK"
                )

            elif risk == "MEDIUM":

                st.warning(
                    "🟡 MEDIUM RISK"
                )

            elif risk == "LOW":

                st.success(
                    "🟢 LOW RISK"
                )

            else:

                st.info(
                    "Collecting data..."
                )


            st.write(
                f"Predicted crowd: "
                f"**{prediction_results[zone_name]['predicted']}**"
                if prediction_results[zone_name]["predicted"] is not None
                else "Predicted crowd: collecting..."
            )

            st.write(
                f"Capacity: **{result['capacity']}**"
            )

            st.write(
                f"Capacity usage: "
                f"**{result['percentage']:.1f}%**"
            )


    # --------------------------------------------
    # RISK TABLE
    # --------------------------------------------

    st.header("📊 Risk Summary")

    risk_table = []

    for zone_name in [
        "Zone 1",
        "Zone 2",
        "Zone 3"
    ]:

        prediction = prediction_results[zone_name]
        risk = risk_results[zone_name]

        risk_table.append({
            "Zone": zone_name,
            "Current": prediction["current"],
            "Predicted (30 sec)": prediction["predicted"],
            "Capacity": risk["capacity"],
            "Usage %": round(
                risk["percentage"],
                1
            ),
            "Risk": risk["risk"],
            "Trend": prediction["trend"]
        })


    risk_df = pd.DataFrame(
        risk_table
    )

    st.dataframe(
        risk_df,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------
    # RAW DATA
    # --------------------------------------------

    st.header("Latest Data")

    st.dataframe(
        data.tail(10),
        use_container_width=True,
        hide_index=True
    )


live_dashboard()