# ============================================================
# NER SURAKSHA - DATA MODULE
# North Eastern Region Landslide Early Warning System
# ============================================================

import hashlib
from copy import deepcopy


# ============================================================
# NORTH EASTERN REGION STATES & MONITORED LOCATIONS
# ============================================================

NER_STATES = {
    "Arunachal Pradesh": [
        "Tawang",
        "Itanagar",
        "West Kameng",
        "Dibang Valley",
    ],

    "Assam": [
        "Dima Hasao",
        "Karbi Anglong",
        "Guwahati",
        "Cachar",
    ],

    "Manipur": [
        "Senapati",
        "Ukhrul",
        "Tamenglong",
        "Churachandpur",
    ],

    "Meghalaya": [
        "Cherrapunji",
        "Shillong",
        "West Khasi Hills",
        "East Jaintia Hills",
    ],

    "Mizoram": [
        "Aizawl",
        "Lunglei",
        "Champhai",
        "Kolasib",
    ],

    "Nagaland": [
        "Kohima",
        "Mokokchung",
        "Dimapur",
        "Mon",
    ],

    "Sikkim": [
        "Gangtok",
        "Mangan",
        "Namchi",
        "Gyalshing",
    ],

    "Tripura": [
        "Agartala",
        "Dhalai",
        "North Tripura",
        "Jampui Hills",
    ],
}


# ============================================================
# APPROXIMATE MONITORING INFORMATION
# Prototype/demo geographic data
# ============================================================

LOCATION_DATA = {

    # --------------------------------------------------------
    # ARUNACHAL PRADESH
    # --------------------------------------------------------

    "Tawang": {
        "lat": 27.5860,
        "lon": 91.8590,
        "population": 11000,
        "base_risk": 72,
        "road_status": "Caution",
        "shelter": "Tawang Relief Centre",
    },

    "Itanagar": {
        "lat": 27.0844,
        "lon": 93.6053,
        "population": 59000,
        "base_risk": 44,
        "road_status": "Open",
        "shelter": "Itanagar Community Hall",
    },

    "West Kameng": {
        "lat": 27.4000,
        "lon": 92.5000,
        "population": 15000,
        "base_risk": 68,
        "road_status": "Caution",
        "shelter": "Bomdila Relief Centre",
    },

    "Dibang Valley": {
        "lat": 28.7000,
        "lon": 95.7000,
        "population": 8000,
        "base_risk": 76,
        "road_status": "Caution",
        "shelter": "Dibang Valley Relief Centre",
    },


    # --------------------------------------------------------
    # ASSAM
    # --------------------------------------------------------

    "Dima Hasao": {
        "lat": 25.3478,
        "lon": 93.0176,
        "population": 22000,
        "base_risk": 64,
        "road_status": "Caution",
        "shelter": "Haflong Relief Centre",
    },

    "Karbi Anglong": {
        "lat": 26.0200,
        "lon": 93.4500,
        "population": 31000,
        "base_risk": 55,
        "road_status": "Open",
        "shelter": "Diphu Community Hall",
    },

    "Guwahati": {
        "lat": 26.1445,
        "lon": 91.7362,
        "population": 120000,
        "base_risk": 48,
        "road_status": "Caution",
        "shelter": "Guwahati Emergency Shelter",
    },

    "Cachar": {
        "lat": 24.8333,
        "lon": 92.7789,
        "population": 50000,
        "base_risk": 46,
        "road_status": "Open",
        "shelter": "Cachar Community Hall",
    },


    # --------------------------------------------------------
    # MANIPUR
    # --------------------------------------------------------

    "Senapati": {
        "lat": 25.2670,
        "lon": 94.0200,
        "population": 15000,
        "base_risk": 70,
        "road_status": "Caution",
        "shelter": "Senapati Relief Centre",
    },

    "Ukhrul": {
        "lat": 25.0967,
        "lon": 94.3614,
        "population": 18000,
        "base_risk": 68,
        "road_status": "Caution",
        "shelter": "Ukhrul Relief Centre",
    },

    "Tamenglong": {
        "lat": 24.9750,
        "lon": 93.5300,
        "population": 12000,
        "base_risk": 73,
        "road_status": "Caution",
        "shelter": "Tamenglong Relief Centre",
    },

    "Churachandpur": {
        "lat": 24.3333,
        "lon": 93.6833,
        "population": 28000,
        "base_risk": 52,
        "road_status": "Open",
        "shelter": "Churachandpur Community Hall",
    },


    # --------------------------------------------------------
    # MEGHALAYA
    # --------------------------------------------------------

    "Cherrapunji": {
        "lat": 25.2840,
        "lon": 91.7210,
        "population": 12000,
        "base_risk": 78,
        "road_status": "Caution",
        "shelter": "Sohra Relief Centre",
    },

    "Shillong": {
        "lat": 25.5788,
        "lon": 91.8933,
        "population": 143000,
        "base_risk": 60,
        "road_status": "Caution",
        "shelter": "Shillong Emergency Shelter",
    },

    "West Khasi Hills": {
        "lat": 25.5000,
        "lon": 91.3000,
        "population": 20000,
        "base_risk": 67,
        "road_status": "Caution",
        "shelter": "West Khasi Hills Relief Centre",
    },

    "East Jaintia Hills": {
        "lat": 25.4500,
        "lon": 92.3500,
        "population": 18000,
        "base_risk": 63,
        "road_status": "Caution",
        "shelter": "Jowai Relief Centre",
    },


    # --------------------------------------------------------
    # MIZORAM
    # --------------------------------------------------------

    "Aizawl": {
        "lat": 23.7271,
        "lon": 92.7176,
        "population": 98000,
        "base_risk": 68,
        "road_status": "Caution",
        "shelter": "Aizawl Relief Centre",
    },

    "Lunglei": {
        "lat": 22.8900,
        "lon": 92.7500,
        "population": 24000,
        "base_risk": 74,
        "road_status": "Caution",
        "shelter": "Lunglei Relief Centre",
    },

    "Champhai": {
        "lat": 23.4670,
        "lon": 93.3260,
        "population": 16000,
        "base_risk": 51,
        "road_status": "Open",
        "shelter": "Champhai Community Hall",
    },

    "Kolasib": {
        "lat": 24.2230,
        "lon": 92.6780,
        "population": 14000,
        "base_risk": 56,
        "road_status": "Caution",
        "shelter": "Kolasib Relief Centre",
    },


    # --------------------------------------------------------
    # NAGALAND
    # --------------------------------------------------------

    "Kohima": {
        "lat": 25.6751,
        "lon": 94.1086,
        "population": 41000,
        "base_risk": 65,
        "road_status": "Caution",
        "shelter": "Kohima Relief Centre",
    },

    "Mokokchung": {
        "lat": 26.3300,
        "lon": 94.5300,
        "population": 17000,
        "base_risk": 46,
        "road_status": "Open",
        "shelter": "Mokokchung Community Hall",
    },

    "Dimapur": {
        "lat": 25.9000,
        "lon": 93.7300,
        "population": 30000,
        "base_risk": 58,
        "road_status": "Caution",
        "shelter": "Dimapur Relief Centre",
    },

    "Mon": {
        "lat": 26.7200,
        "lon": 95.0000,
        "population": 12000,
        "base_risk": 62,
        "road_status": "Caution",
        "shelter": "Mon Relief Centre",
    },


    # --------------------------------------------------------
    # SIKKIM
    # --------------------------------------------------------

    "Gangtok": {
        "lat": 27.3389,
        "lon": 88.6065,
        "population": 100000,
        "base_risk": 70,
        "road_status": "Caution",
        "shelter": "Gangtok Emergency Shelter",
    },

    "Mangan": {
        "lat": 27.5000,
        "lon": 88.5300,
        "population": 14000,
        "base_risk": 82,
        "road_status": "Caution",
        "shelter": "Mangan Relief Centre",
    },

    "Namchi": {
        "lat": 27.1667,
        "lon": 88.3500,
        "population": 13000,
        "base_risk": 49,
        "road_status": "Open",
        "shelter": "Namchi Community Hall",
    },

    "Gyalshing": {
        "lat": 27.2900,
        "lon": 88.2600,
        "population": 12000,
        "base_risk": 65,
        "road_status": "Caution",
        "shelter": "Gyalshing Relief Centre",
    },


    # --------------------------------------------------------
    # TRIPURA
    # --------------------------------------------------------

    "Agartala": {
        "lat": 23.8315,
        "lon": 91.2868,
        "population": 70000,
        "base_risk": 39,
        "road_status": "Open",
        "shelter": "Agartala Community Hall",
    },

    "Dhalai": {
        "lat": 24.0500,
        "lon": 91.8500,
        "population": 12000,
        "base_risk": 45,
        "road_status": "Open",
        "shelter": "Dhalai Community Hall",
    },

    "North Tripura": {
        "lat": 24.1800,
        "lon": 92.1000,
        "population": 18000,
        "base_risk": 54,
        "road_status": "Caution",
        "shelter": "North Tripura Relief Centre",
    },

    "Jampui Hills": {
        "lat": 24.0800,
        "lon": 92.2500,
        "population": 9000,
        "base_risk": 61,
        "road_status": "Caution",
        "shelter": "Jampui Relief Centre",
    },
}


# ============================================================
# BASIC STATE FUNCTIONS
# ============================================================

def get_states():
    """
    Return all North Eastern Region states.
    """
    return list(NER_STATES.keys())


def get_locations(state):
    """
    Return monitored locations for the selected state.
    """
    return list(NER_STATES.get(state, []))


# ============================================================
# COMPATIBILITY FUNCTION
# IMPORTANT:
# app.py expects data.get_zones(state)
# ============================================================

def get_zones(state):
    """
    Return complete monitoring information for all
    locations in the selected state.

    This function prevents:
        AttributeError:
        module 'data' has no attribute 'get_zones'
    """

    zones = []

    for location in NER_STATES.get(state, []):

        info = deepcopy(
            LOCATION_DATA.get(
                location,
                {
                    "lat": 25.5,
                    "lon": 92.0,
                    "population": 10000,
                    "base_risk": 50,
                    "road_status": "Caution",
                    "shelter": f"{location} Relief Centre",
                }
            )
        )

        info["zone"] = location
        info["name"] = location

        zones.append(info)

    return zones


# ============================================================
# DETERMINISTIC DEMO DATA GENERATOR
# ============================================================

def _stable_number(location, minimum, maximum, salt=""):
    """
    Generate stable pseudo-random demo values.

    The same location produces the same values after
    restarting Streamlit.
    """

    text = f"{location}-{salt}".encode("utf-8")

    digest = hashlib.sha256(text).hexdigest()

    number = int(digest[:12], 16) / float(16 ** 12 - 1)

    return minimum + number * (maximum - minimum)


def generate_zone_input(zone):
    """
    Generate environmental inputs for the ML model.

    These values are DEMO / PROTOTYPE values.
    Replace them with real IMD, sensor, satellite and
    GIS data for real deployment.
    """

    location = zone.get("zone", zone.get("name", "Unknown"))

    base_risk = float(zone.get("base_risk", 50))

    rainfall_24h = _stable_number(
        location,
        50,
        220,
        "rainfall24"
    )

    rainfall_6h = _stable_number(
        location,
        15,
        120,
        "rainfall6"
    )

    soil_moisture = _stable_number(
        location,
        35,
        92,
        "soil"
    )

    slope = _stable_number(
        location,
        12,
        48,
        "slope"
    )

    elevation = _stable_number(
        location,
        100,
        2800,
        "elevation"
    )

    historical = int(
        _stable_number(
            location,
            1,
            10,
            "history"
        )
    )

    forecast = _stable_number(
        location,
        20,
        150,
        "forecast"
    )

    # Increase environmental values slightly for
    # naturally higher-risk prototype locations.
    risk_factor = base_risk / 100.0

    rainfall_24h = min(
        300,
        rainfall_24h + risk_factor * 35
    )

    rainfall_6h = min(
        180,
        rainfall_6h + risk_factor * 25
    )

    soil_moisture = min(
        100,
        soil_moisture + risk_factor * 8
    )

    forecast = min(
        220,
        forecast + risk_factor * 25
    )

    return {
        # ML model feature names
        "rainfall_24h": round(rainfall_24h, 2),
        "rainfall_6h": round(rainfall_6h, 2),
        "soil_moisture": round(soil_moisture, 2),
        "slope": round(slope, 2),
        "elevation": round(elevation, 2),
        "historical_landslides": historical,
        "forecast_rainfall_6h": round(forecast, 2),

        # Easy dashboard aliases
        "rainfall": round(rainfall_24h, 2),
        "soil": round(soil_moisture, 2),
        "historical": historical,
        "forecast": round(forecast, 2),
    }


# ============================================================
# DATA COLLECTION
# ============================================================

def collect_data(
    rainfall,
    soil_moisture,
    slope,
    elevation,
    historical_landslides,
    forecast_rainfall,
    rainfall_6h=None,
):
    """
    Collect environmental and historical parameters.

    Compatible with both the simple prototype UI and
    the ML prediction module.
    """

    if rainfall_6h is None:
        rainfall_6h = min(
            float(rainfall),
            float(rainfall) * 0.45
        )

    return {
        # Original names
        "rainfall": float(rainfall),
        "soil": float(soil_moisture),
        "slope": float(slope),
        "elevation": float(elevation),
        "historical": int(historical_landslides),
        "forecast": float(forecast_rainfall),

        # ML-compatible names
        "rainfall_24h": float(rainfall),
        "rainfall_6h": float(rainfall_6h),
        "soil_moisture": float(soil_moisture),
        "historical_landslides": int(historical_landslides),
        "forecast_rainfall_6h": float(forecast_rainfall),
    }


# ============================================================
# FIND A LOCATION
# ============================================================

def find_location(location):
    """
    Return complete information for one monitored location.
    """

    info = LOCATION_DATA.get(location)

    if info is None:
        return None

    result = deepcopy(info)
    result["zone"] = location
    result["name"] = location

    return result


# ============================================================
# FIND STATE OF A LOCATION
# ============================================================

def get_state_for_location(location):
    """
    Return the NER state containing the given location.
    """

    for state, locations in NER_STATES.items():

        if location in locations:
            return state

    return None


# ============================================================
# ALL MONITORED ZONES
# ============================================================

def get_all_zones():
    """
    Return all monitored locations across Northeast India.
    """

    zones = []

    for state in get_states():

        for zone in get_zones(state):

            zone["state"] = state

            zones.append(zone)

    return zones


# ============================================================
# HIGHEST BASE-RISK LOCATION
# ============================================================

def get_highest_base_risk_zone(state):
    """
    Return the highest base-risk monitored location
    within the selected state.
    """

    zones = get_zones(state)

    if not zones:
        return None

    return max(
        zones,
        key=lambda zone: float(
            zone.get("base_risk", 0)
        )
    )
