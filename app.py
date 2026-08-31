import streamlit as st
import pandas as pd
import pydeck as pdk
import time
from datetime import datetime

import data
import model


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NER Suraksha",
    page_icon="⛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "live_mode" not in st.session_state:
    st.session_state.live_mode = True

if "last_update" not in st.session_state:
    st.session_state.last_update = datetime.now()


# ============================================================
# HEADER
# ============================================================

st.title("⛰️ NER Suraksha")

st.subheader(
    "AI-Powered Landslide Early Warning & Citizen Safety System"
)

st.caption(
    "Real-time monitoring • 6-hour early warning • "
    "Risk prediction • Critical-zone detection • Emergency response"
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Monitoring Control")

    st.session_state.live_mode = st.toggle(
        "🔴 Live Monitoring",
        value=True
    )

    refresh_time = st.slider(
        "Refresh Interval",
        min_value=5,
        max_value=60,
        value=10
    )

    st.divider()

    st.header("📍 Select Location")

    states = data.get_states()

    selected_state = st.selectbox(
        "State / Region",
        states
    )

    zones = data.get_zones(
        selected_state
    )

    zone_names = [
        zone["zone"]
        for zone in zones
    ]

    selected_zone = st.selectbox(
        "Location",
        zone_names
    )

    st.divider()

    st.markdown("### 🗺️ Risk Legend")

    st.markdown("🔴 **CRITICAL**")

    st.markdown("🟠 **HIGH**")

    st.markdown("🟡 **MEDIUM**")

    st.markdown("🟢 **LOW**")

    st.divider()

    st.info(
        "Select a location to view its current risk "
        "and predicted risk for the next 6 hours."
    )


# ============================================================
# LIVE STATUS
# ============================================================

now = datetime.now()

st.session_state.last_update = now

s1, s2, s3, s4 = st.columns(4)


with s1:

    if st.session_state.live_mode:
        st.success("🟢 SYSTEM ONLINE")
    else:
        st.warning("🟡 MONITORING PAUSED")


with s2:

    st.metric(
        "Last Update",
        now.strftime("%H:%M:%S")
    )


with s3:

    st.metric(
        "Selected State",
        selected_state
    )


with s4:

    st.metric(
        "Monitored Zones",
        len(zones)
    )


st.divider()


# ============================================================
# CURRENT AI RISK CALCULATION
# ============================================================

results = []


for zone in zones:

    zone_input = data.generate_zone_input(
        zone
    )

    current_risk = model.predict_risk(
        zone_input
    )

    current_level = model.risk_level(
        current_risk
    )

    exposed = model.population_exposure(
        current_risk,
        zone["population"]
    )

    emergency_score = model.emergency_priority(
        current_risk,
        zone["population"],
        zone["road_status"]
    )

    emergency_priority = model.priority_label(
        emergency_score
    )

    results.append(
        {
            "zone": zone["zone"],

            "lat": zone["lat"],
            "lon": zone["lon"],

            "risk": float(current_risk),

            "level": current_level,

            "population": int(
                zone["population"]
            ),

            "exposed": int(
                exposed
            ),

            "emergency_score": float(
                emergency_score
            ),

            "emergency_priority":
                emergency_priority,

            "rainfall": zone["rainfall"],

            "soil": zone["soil"],

            "slope": zone["slope"],

            "elevation": zone["elevation"],

            "historical": zone["historical"],

            "forecast": zone["forecast"],

            "road_status":
                zone["road_status"],

            "shelter":
                zone["shelter"],

            "shelter_lat":
                zone.get(
                    "shelter_lat",
                    zone["lat"] + 0.02
                ),

            "shelter_lon":
                zone.get(
                    "shelter_lon",
                    zone["lon"] + 0.02
                ),

            "route":
                zone["route"],

            "response_priority":
                zone["response_priority"]
        }
    )


risk_df = pd.DataFrame(
    results
)


# ============================================================
# SORT ZONES BY EMERGENCY PRIORITY
# ============================================================

risk_df = risk_df.sort_values(
    "emergency_score",
    ascending=False
).reset_index(
    drop=True
)


# ============================================================
# SELECTED LOCATION
# ============================================================

selected_rows = risk_df[
    risk_df["zone"] == selected_zone
]


if selected_rows.empty:

    st.error(
        "Selected location data is unavailable."
    )

    st.stop()


selected = selected_rows.iloc[0]


current_risk = float(
    selected["risk"]
)


current_level = selected[
    "level"
]


# ============================================================
# 6-HOUR EARLY WARNING PREDICTION
# ============================================================

future_rainfall = float(
    selected["forecast"]
)


future_input = {

    "rainfall":
        future_rainfall,

    "soil":
        selected["soil"],

    "slope":
        selected["slope"],

    "elevation":
        selected["elevation"],

    "historical":
        selected["historical"],

    "forecast":
        future_rainfall
}


six_hour_risk = model.predict_risk(
    future_input
)


six_hour_risk = float(
    six_hour_risk
)


six_hour_level = model.risk_level(
    six_hour_risk
)


risk_change = (
    six_hour_risk -
    current_risk
)


# ============================================================
# LOCATION STATUS
# ============================================================

st.header(
    f"📍 {selected_zone}"
)


if six_hour_risk >= 80:

    st.error(
        f"🚨 6-HOUR CRITICAL WARNING — "
        f"{six_hour_risk:.1f}% predicted risk"
    )

elif six_hour_risk >= 60:

    st.warning(
        f"🟠 6-HOUR HIGH WARNING — "
        f"{six_hour_risk:.1f}% predicted risk"
    )

elif six_hour_risk >= 35:

    st.warning(
        f"🟡 6-HOUR MODERATE WARNING — "
        f"{six_hour_risk:.1f}% predicted risk"
    )

else:

    st.success(
        f"🟢 6-HOUR LOW RISK — "
        f"{six_hour_risk:.1f}% predicted risk"
    )


# ============================================================
# MAIN METRICS
# ============================================================

m1, m2, m3, m4, m5 = st.columns(5)


with m1:

    st.metric(
        "Current Risk",
        f"{current_risk:.1f}%"
    )


with m2:

    st.metric(
        "Current Level",
        current_level
    )


with m3:

    st.metric(
        "6-Hour Risk",
        f"{six_hour_risk:.1f}%"
    )


with m4:

    st.metric(
        "Risk Change",
        f"{risk_change:+.1f}%"
    )


with m5:

    st.metric(
        "Population",
        f"{int(selected['population']):,}"
    )


st.divider()


# ============================================================
# 6-HOUR EARLY WARNING
# ============================================================

st.header(
    "⏱️ 6-Hour Early Warning System"
)

st.caption(
    "The prototype estimates how risk may change "
    "using forecast rainfall and current environmental "
    "conditions."
)


w1, w2, w3, w4 = st.columns(4)


with w1:

    st.metric(
        "Now",
        f"{current_risk:.1f}%"
    )


with w2:

    risk_2h = (
        current_risk +
        (six_hour_risk - current_risk) * 0.33
    )

    st.metric(
        "+2 Hours",
        f"{risk_2h:.1f}%"
    )


with w3:

    risk_4h = (
        current_risk +
        (six_hour_risk - current_risk) * 0.66
    )

    st.metric(
        "+4 Hours",
        f"{risk_4h:.1f}%"
    )


with w4:

    st.metric(
        "+6 Hours",
        f"{six_hour_risk:.1f}%"
    )


# ============================================================
# EARLY WARNING MESSAGE
# ============================================================

if six_hour_risk >= 80:

    st.error(
        f"""
        🚨 CRITICAL EARLY WARNING

        {selected_zone} is predicted to have CRITICAL
        landslide risk within the next 6 hours.

        Predicted risk: {six_hour_risk:.1f}%

        Recommended preventive actions:
        • Verify the prediction
        • Inspect vulnerable slopes
        • Check road connectivity
        • Prepare emergency response teams
        • Verify designated relief centres
        • Issue official warnings when appropriate
        """
    )


elif six_hour_risk >= 60:

    st.warning(
        f"""
        ⚠️ HIGH EARLY WARNING

        {selected_zone} is predicted to have HIGH
        landslide risk within the next 6 hours.

        Predicted risk: {six_hour_risk:.1f}%

        Increase monitoring and prepare response teams.
        """
    )


elif six_hour_risk >= 35:

    st.info(
        f"""
        🟡 MODERATE EARLY WARNING

        {selected_zone} shows elevated risk during
        the next 6 hours.

        Predicted risk: {six_hour_risk:.1f}%

        Continue monitoring weather and terrain.
        """
    )


else:

    st.success(
        f"""
        🟢 LOW 6-HOUR RISK

        {selected_zone} is currently predicted to remain
        below the elevated-risk threshold.

        Predicted risk: {six_hour_risk:.1f}%
        """
    )


# ============================================================
# 6-HOUR RISK CHART
# ============================================================

st.subheader(
    "📈 Next 6 Hours Risk Timeline"
)


timeline_df = pd.DataFrame(

    {
        "Time": [
            "Now",
            "+2 Hours",
            "+4 Hours",
            "+6 Hours"
        ],

        "Predicted Risk (%)": [
            round(current_risk, 1),
            round(risk_2h, 1),
            round(risk_4h, 1),
            round(six_hour_risk, 1)
        ]
    }
)


st.line_chart(

    timeline_df.set_index(
        "Time"
    )
)


st.dataframe(
    timeline_df,
    use_container_width=True,
    hide_index=True
)


st.divider()


# ============================================================
# HIGHEST RISK ZONE
# ============================================================

st.header(
    f"🚨 Highest-Risk Zone in {selected_state}"
)


highest = risk_df.iloc[0]


h1, h2, h3, h4 = st.columns(4)


with h1:

    st.metric(
        "Zone",
        highest["zone"]
    )


with h2:

    st.metric(
        "Risk",
        f"{float(highest['risk']):.1f}%"
    )


with h3:

    st.metric(
        "Population",
        f"{int(highest['population']):,}"
    )


with h4:

    st.metric(
        "Potentially Exposed",
        f"{int(highest['exposed']):,}"
    )


if highest["level"] == "CRITICAL":

    st.error(
        f"🚨 {highest['zone']} requires immediate "
        "attention according to the prototype model."
    )

elif highest["level"] == "HIGH":

    st.warning(
        f"⚠️ {highest['zone']} currently has the "
        "highest monitored risk."
    )

else:

    st.info(
        f"{highest['zone']} currently has the "
        "highest relative risk."
    )


st.divider()


# ============================================================
# LIVE GIS MAP
# ============================================================

st.header(
    f"🗺️ Live Landslide Risk Map — {selected_state}"
)

st.caption(
    "🔴 Critical • 🟠 High • 🟡 Medium • 🟢 Low • "
    "🔵 Selected location"
)


# ============================================================
# MAP COLORS
# ============================================================

def get_color(level):

    if level == "CRITICAL":

        return [220, 40, 40, 230]

    elif level == "HIGH":

        return [255, 140, 0, 230]

    elif level == "MEDIUM":

        return [245, 205, 40, 230]

    else:

        return [40, 180, 90, 230]


risk_df["color"] = risk_df[
    "level"
].apply(
    get_color
)


# ============================================================
# MAP RADIUS
# ============================================================

def get_radius(risk):

    if risk >= 80:

        return 15000

    elif risk >= 60:

        return 12000

    elif risk >= 35:

        return 9000

    else:

        return 6000


risk_df["radius"] = risk_df[
    "risk"
].apply(
    get_radius
)


# ============================================================
# RISK MAP LAYER
# ============================================================

risk_layer = pdk.Layer(

    "ScatterplotLayer",

    data=risk_df,

    get_position="[lon, lat]",

    get_radius="radius",

    get_fill_color="color",

    get_line_color=[255, 255, 255],

    get_line_width=2,

    filled=True,

    stroked=True,

    pickable=True,

    auto_highlight=True
)


# ============================================================
# SELECTED LOCATION LAYER
# ============================================================

selected_map = risk_df[
    risk_df["zone"] == selected_zone
].copy()


selected_layer = pdk.Layer(

    "ScatterplotLayer",

    data=selected_map,

    get_position="[lon, lat]",

    get_radius=20000,

    get_fill_color=[30, 100, 255, 35],

    get_line_color=[30, 100, 255, 255],

    get_line_width=5,

    filled=True,

    stroked=True
)


# ============================================================
# MAP VIEW
# ============================================================

map_view = pdk.ViewState(

    latitude=float(
        selected["lat"]
    ),

    longitude=float(
        selected["lon"]
    ),

    zoom=8
)


# ============================================================
# MAP TOOLTIP
# ============================================================

tooltip = {

    "html":
        "<b>{zone}</b><br/>"
        "Risk: {risk}%<br/>"
        "Level: {level}<br/>"
        "Population: {population}<br/>"
        "Potentially Exposed: {exposed}<br/>"
        "Road: {road_status}",

    "style": {
        "backgroundColor": "white",
        "color": "black"
    }
}


# ============================================================
# MAP
# ============================================================

deck = pdk.Deck(

    layers=[
        risk_layer,
        selected_layer
    ],

    initial_view_state=map_view,

    tooltip=tooltip,

    map_provider="carto",

    map_style="light"
)


st.pydeck_chart(
    deck,
    use_container_width=True
)


st.divider()


# ============================================================
# 🚨 PRE-DISASTER RESPONSE
# ============================================================

if six_hour_risk >= 80:

    st.header(
        "🆘 PRE-DISASTER RESPONSE MODE"
    )

    st.error(
        f"🚨 CRITICAL RISK EXPECTED WITHIN 6 HOURS"
    )


    # --------------------------------------------------------
    # RESPONSE METRICS
    # --------------------------------------------------------

    r1, r2, r3, r4 = st.columns(4)


    with r1:

        st.metric(
            "Predicted Risk",
            f"{six_hour_risk:.1f}%"
        )


    with r2:

        st.metric(
            "Population",
            f"{int(selected['population']):,}"
        )


    with r3:

        st.metric(
            "Potentially Exposed",
            f"{int(selected['exposed']):,}"
        )


    with r4:

        st.metric(
            "Priority",
            selected["emergency_priority"]
        )


    st.divider()


    # --------------------------------------------------------
    # PREVENTIVE ACTIONS
    # --------------------------------------------------------

    st.subheader(
        "🛡️ Recommended Preventive Actions"
    )


    a1, a2, a3 = st.columns(3)


    with a1:

        st.write(
            "### 🔍 1. Inspect"
        )

        st.write(
            "Inspect vulnerable slopes, roads, "
            "drainage systems and nearby infrastructure."
        )


    with a2:

        st.write(
            "### 🚑 2. Prepare"
        )

        st.write(
            "Prepare emergency teams, relief centres "
            "and communication systems."
        )


    with a3:

        st.write(
            "### 📢 3. Verify & Alert"
        )

        st.write(
            "Verify the AI prediction with field "
            "conditions before issuing official alerts."
        )


    st.divider()


    # --------------------------------------------------------
    # SAFE DESTINATION
    # --------------------------------------------------------

    route_left, route_right = st.columns(2)


    with route_left:

        st.subheader(
            "🏠 Designated Relief Centre"
        )

        st.success(
            selected["shelter"]
        )


    with route_right:

        st.subheader(
            "🧭 Prototype Route Guidance"
        )

        if selected["road_status"] == "Open":

            st.success(
                "🟢 Monitored road currently reported OPEN"
            )

        elif selected["road_status"] == "Caution":

            st.warning(
                "🟠 Monitored road currently requires CAUTION"
            )

        else:

            st.error(
                "🔴 Monitored road currently BLOCKED"
            )


        st.info(
            selected["route"]
        )


    st.divider()


    # --------------------------------------------------------
    # EMERGENCY ROUTE MAP
    # --------------------------------------------------------

    st.subheader(
        "🗺️ Emergency Destination Map"
    )


    danger_point = pd.DataFrame(

        [
            {
                "lat":
                    float(selected["lat"]),

                "lon":
                    float(selected["lon"]),

                "name":
                    selected_zone
            }
        ]
    )


    shelter_point = pd.DataFrame(

        [
            {
                "lat":
                    float(selected["shelter_lat"]),

                "lon":
                    float(selected["shelter_lon"]),

                "name":
                    selected["shelter"]
            }
        ]
    )


    danger_layer = pdk.Layer(

        "ScatterplotLayer",

        data=danger_point,

        get_position="[lon, lat]",

        get_radius=15000,

        get_fill_color=[
            220,
            40,
            40,
            90
        ],

        get_line_color=[
            220,
            40,
            40,
            255
        ],

        get_line_width=5,

        filled=True,

        stroked=True,

        pickable=True
    )


    shelter_layer = pdk.Layer(

        "ScatterplotLayer",

        data=shelter_point,

        get_position="[lon, lat]",

        get_radius=2500,

        get_fill_color=[
            30,
            170,
            80,
            255
        ],

        get_line_color=[
            255,
            255,
            255,
            255
        ],

        get_line_width=3,

        filled=True,

        stroked=True,

        pickable=True
    )


    # --------------------------------------------------------
    # ROUTE LINE
    # --------------------------------------------------------

    route_data = pd.DataFrame(

        [
            {
                "source_lon":
                    float(selected["lon"]),

                "source_lat":
                    float(selected["lat"]),

                "target_lon":
                    float(selected["shelter_lon"]),

                "target_lat":
                    float(selected["shelter_lat"])
            }
        ]
    )


    route_layer = pdk.Layer(

        "ArcLayer",

        data=route_data,

        get_source_position=
            "[source_lon, source_lat]",

        get_target_position=
            "[target_lon, target_lat]",

        get_width=8,

        get_source_color=[
            220,
            40,
            40,
            220
        ],

        get_target_color=[
            30,
            170,
            80,
            220
        ]
    )


    rescue_view = pdk.ViewState(

        latitude=float(
            selected["lat"]
        ),

        longitude=float(
            selected["lon"]
        ),

        zoom=10
    )


    rescue_deck = pdk.Deck(

        layers=[
            danger_layer,
            route_layer,
            shelter_layer
        ],

        initial_view_state=
            rescue_view,

        tooltip={
            "text": "{name}"
        },

        map_provider="carto",

        map_style="light"
    )


    st.pydeck_chart(
        rescue_deck,
        use_container_width=True
    )


    st.divider()


    # --------------------------------------------------------
    # CITIZEN SAFETY
    # --------------------------------------------------------

    st.subheader(
        "🛡️ Citizen Safety Guidance"
    )


    safety1, safety2 = st.columns(2)


    with safety1:

        st.markdown(
            """
            ### 🚶 Before an Emergency

            • Monitor official warnings.

            • Keep phones charged.

            • Keep important documents accessible.

            • Know the designated relief centre.

            • Avoid unnecessary travel near unstable slopes.
            """
        )


    with safety2:

        st.markdown(
            """
            ### 🚨 If Authorities Order Evacuation

            • Follow the official evacuation order.

            • Use verified evacuation routes.

            • Stay away from landslide areas.

            • Do not cross blocked roads.

            • Follow instructions from emergency personnel.
            """
        )


    st.error(
        "⚠️ The route shown by this prototype is not a "
        "guaranteed safe route. Real evacuation routes "
        "must be verified using current road, weather and "
        "disaster-management information."
    )


# ============================================================
# HIGH RISK PREPARATION
# ============================================================

elif six_hour_risk >= 60:

    st.header(
        "⚠️ HIGH-RISK PREPARATION MODE"
    )

    st.warning(
        f"{selected_zone} may experience HIGH landslide "
        f"risk within the next 6 hours."
    )


    p1, p2, p3 = st.columns(3)


    with p1:

        st.write(
            "🔍 Increase field monitoring"
        )


    with p2:

        st.write(
            "🚑 Prepare response teams"
        )


    with p3:

        st.write(
            "📢 Monitor official warnings"
        )


# ============================================================
# ENVIRONMENTAL CONDITIONS
# ============================================================

st.divider()

st.header(
    "🌧️ Environmental Conditions"
)


e1, e2, e3, e4, e5 = st.columns(5)


with e1:

    st.metric(
        "Rainfall",
        f"{int(selected['rainfall'])} mm"
    )


with e2:

    st.metric(
        "Next 6h Rain",
        f"{int(selected['forecast'])} mm"
    )


with e3:

    st.metric(
        "Soil Moisture",
        f"{int(selected['soil'])}%"
    )


with e4:

    st.metric(
        "Slope",
        f"{int(selected['slope'])}°"
    )


with e5:

    st.metric(
        "Elevation",
        f"{int(selected['elevation'])} m"
    )


st.divider()


# ============================================================
# EMERGENCY PRIORITY TABLE
# ============================================================

st.header(
    f"🚑 Emergency Priority — {selected_state}"
)


priority_df = risk_df[
    [
        "zone",
        "risk",
        "level",
        "population",
        "exposed",
        "emergency_priority",
        "road_status"
    ]
].copy()


priority_df.columns = [

    "Location",

    "Risk (%)",

    "Risk Level",

    "Population",

    "Potentially Exposed",

    "Emergency Priority",

    "Road Status"
]


st.dataframe(

    priority_df,

    use_container_width=True,

    hide_index=True
)


st.divider()


# ============================================================
# CITIZEN HAZARD REPORT
# ============================================================

st.header(
    "📸 Citizen Hazard Reporting"
)

st.write(
    "Report landslides, slope cracks, slope movement, "
    "blocked roads or flooding."
)


with st.form(
    "citizen_hazard_form"
):

    hazard_type = st.selectbox(

        "Hazard Type",

        [
            "Landslide",
            "Slope Crack",
            "Slope Movement",
            "Road Blockage",
            "Flash Flood",
            "Fallen Trees",
            "Other"
        ]
    )


    description = st.text_area(

        "Describe the hazard",

        placeholder=(
            "Describe what you observed..."
        )
    )


    uploaded_file = st.file_uploader(

        "Upload Photo / Video",

        type=[
            "jpg",
            "jpeg",
            "png",
            "mp4"
        ]
    )


    submit = st.form_submit_button(

        "📤 Submit Hazard Report",

        use_container_width=True
    )


if submit:

    report = data.add_citizen_report(

        selected_state,

        selected_zone,

        hazard_type,

        description,

        uploaded_file
    )


    st.success(
        "✅ Hazard report submitted for verification."
    )


    if (
        uploaded_file is not None
        and
        uploaded_file.type.startswith("image")
    ):

        st.image(
            uploaded_file,
            caption="Uploaded hazard",
            use_container_width=True
        )


st.divider()


# ============================================================
# SYSTEM INFORMATION
# ============================================================

with st.expander(
    "ℹ️ About NER Suraksha"
):

    st.write(
        """
        NER Suraksha is an AI-assisted prototype for
        landslide risk monitoring and early warning.

        The system analyses environmental conditions
        including rainfall, soil moisture, slope,
        elevation, historical landslide activity and
        forecast rainfall.

        The 6-hour module estimates future risk so that
        authorities can investigate conditions and prepare
        preventive actions before a possible disaster.

        In a real deployment, predictions should be validated
        against reliable weather, satellite, sensor, road
        and disaster-management data.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "⛰️ NER Suraksha | AI Landslide Early Warning Prototype"
)


# ============================================================
# AUTO REFRESH
# ============================================================

if st.session_state.live_mode:

    time.sleep(
        refresh_time
    )

    st.rerun()