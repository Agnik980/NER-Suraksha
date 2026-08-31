import pandas as pd
from datetime import datetime


# ============================================================
# NER SURAKSHA - DEMONSTRATION LOCATION DATABASE
# ============================================================
#
# IMPORTANT:
# These values are DEMONSTRATION DATA for a prototype.
#
# A real deployment should connect:
# - IMD rainfall/weather
# - Satellite data
# - Soil moisture sensors
# - DEM / slope data
# - Historical landslide database
# - Official population data
# - Official shelters
# - Live road/bridge status
# ============================================================


ZONE_DATA = {

    # ========================================================
    # SIKKIM
    # ========================================================

    "Sikkim": [

        {
            "zone": "Mangan",
            "lat": 27.5099,
            "lon": 88.5367,

            "rainfall": 245,
            "soil": 91,
            "slope": 48,
            "elevation": 950,
            "historical": 11,
            "forecast": 145,

            "population": 18500,

            "road_status": "Caution",

            "shelter": "Mangan Community Relief Centre",

            "route": "Use only officially confirmed open roads toward the designated relief centre.",

            "response_priority": "Immediate field assessment"
        },

        {
            "zone": "Gangtok",
            "lat": 27.3389,
            "lon": 88.6065,

            "rainfall": 210,
            "soil": 86,
            "slope": 42,
            "elevation": 1650,
            "historical": 9,
            "forecast": 125,

            "population": 100000,

            "road_status": "Open",

            "shelter": "Gangtok District Relief Centre",

            "route": "Follow official evacuation directions and use only roads confirmed open by authorities.",

            "response_priority": "High monitoring"
        },

        {
            "zone": "Gyalshing",
            "lat": 27.2895,
            "lon": 88.2644,

            "rainfall": 185,
            "soil": 81,
            "slope": 39,
            "elevation": 2072,
            "historical": 7,
            "forecast": 110,

            "population": 42000,

            "road_status": "Open",

            "shelter": "Gyalshing Relief Centre",

            "route": "Follow local authority directions to the designated relief centre.",

            "response_priority": "Preparedness"
        },

        {
            "zone": "Namchi",
            "lat": 27.1667,
            "lon": 88.3500,

            "rainfall": 150,
            "soil": 76,
            "slope": 34,
            "elevation": 1315,
            "historical": 6,
            "forecast": 90,

            "population": 12000,

            "road_status": "Open",

            "shelter": "Namchi Community Hall",

            "route": "Remain alert and follow official local evacuation information.",

            "response_priority": "Routine monitoring"
        },

        {
            "zone": "Pakyong",
            "lat": 27.2300,
            "lon": 88.6200,

            "rainfall": 135,
            "soil": 70,
            "slope": 28,
            "elevation": 1100,
            "historical": 4,
            "forecast": 75,

            "population": 8000,

            "road_status": "Open",

            "shelter": "Pakyong Relief Centre",

            "route": "Continue normal travel while monitoring official alerts.",

            "response_priority": "Routine monitoring"
        }
    ],


    # ========================================================
    # ARUNACHAL PRADESH
    # ========================================================

    "Arunachal Pradesh": [

        {
            "zone": "Itanagar",
            "lat": 27.0844,
            "lon": 93.6053,

            "rainfall": 230,
            "soil": 89,
            "slope": 43,
            "elevation": 350,
            "historical": 10,
            "forecast": 140,

            "population": 60000,

            "road_status": "Caution",

            "shelter": "Itanagar District Relief Centre",

            "route": "Follow officially announced evacuation routes.",

            "response_priority": "Immediate field assessment"
        },

        {
            "zone": "Tawang",
            "lat": 27.5860,
            "lon": 91.8590,

            "rainfall": 195,
            "soil": 78,
            "slope": 49,
            "elevation": 3048,
            "historical": 8,
            "forecast": 125,

            "population": 11000,

            "road_status": "Caution",

            "shelter": "Tawang Relief Centre",

            "route": "Use only authority-confirmed open routes.",

            "response_priority": "High monitoring"
        },

        {
            "zone": "West Kameng",
            "lat": 27.3000,
            "lon": 92.4000,

            "rainfall": 215,
            "soil": 85,
            "slope": 46,
            "elevation": 1500,
            "historical": 9,
            "forecast": 130,

            "population": 22000,

            "road_status": "Caution",

            "shelter": "West Kameng Relief Centre",

            "route": "Follow local authority evacuation directions.",

            "response_priority": "Immediate field assessment"
        },

        {
            "zone": "Lower Subansiri",
            "lat": 27.6000,
            "lon": 93.8000,

            "rainfall": 175,
            "soil": 77,
            "slope": 37,
            "elevation": 800,
            "historical": 6,
            "forecast": 105,

            "population": 18000,

            "road_status": "Open",

            "shelter": "District Relief Centre",

            "route": "Follow official instructions if conditions worsen.",

            "response_priority": "Preparedness"
        },

        {
            "zone": "Dibang Valley",
            "lat": 28.7000,
            "lon": 95.7000,

            "rainfall": 240,
            "soil": 90,
            "slope": 51,
            "elevation": 1200,
            "historical": 10,
            "forecast": 150,

            "population": 9000,

            "road_status": "Caution",

            "shelter": "Dibang Valley Relief Centre",

            "route": "Use only routes verified as open by local authorities.",

            "response_priority": "Immediate field assessment"
        }
    ],


    # ========================================================
    # MEGHALAYA
    # ========================================================

    "Meghalaya": [

        {
            "zone": "Cherrapunji",
            "lat": 25.2640,
            "lon": 91.7362,

            "rainfall": 285,
            "soil": 94,
            "slope": 39,
            "elevation": 1484,
            "historical": 11,
            "forecast": 160,

            "population": 15000,

            "road_status": "Caution",

            "shelter": "Cherrapunji Relief Centre",

            "route": "Follow official evacuation instructions and avoid closed roads.",

            "response_priority": "Immediate field assessment"
        },

        {
            "zone": "Shillong",
            "lat": 25.5788,
            "lon": 91.8933,

            "rainfall": 225,
            "soil": 88,
            "slope": 33,
            "elevation": 1496,
            "historical": 8,
            "forecast": 135,

            "population": 140000,

            "road_status": "Open",

            "shelter": "Shillong District Relief Centre",

            "route": "Follow official evacuation information.",

            "response_priority": "High monitoring"
        },

        {
            "zone": "Mawsynram",
            "lat": 25.3000,
            "lon": 91.5800,

            "rainfall": 295,
            "soil": 95,
            "slope": 36,
            "elevation": 1400,
            "historical": 10,
            "forecast": 165,

            "population": 12000,

            "road_status": "Caution",

            "shelter": "Mawsynram Relief Centre",

            "route": "Follow verified local authority routes only.",

            "response_priority": "Immediate field assessment"
        },

        {
            "zone": "West Khasi Hills",
            "lat": 25.5000,
            "lon": 91.3000,

            "rainfall": 195,
            "soil": 80,
            "slope": 35,
            "elevation": 1100,
            "historical": 6,
            "forecast": 115,

            "population": 25000,

            "road_status": "Open",

            "shelter": "West Khasi Hills Relief Centre",

            "route": "Follow official local guidance.",

            "response_priority": "Preparedness"
        }
    ],


    # ========================================================
    # NAGALAND
    # ========================================================

    "Nagaland": [

        {
            "zone": "Kohima",
            "lat": 25.6751,
            "lon": 94.1086,

            "rainfall": 195,
            "soil": 82,
            "slope": 41,
            "elevation": 1444,
            "historical": 7,
            "forecast": 115,

            "population": 35000,

            "road_status": "Open",

            "shelter": "Kohima Relief Centre",

            "route": "Follow official local evacuation information.",

            "response_priority": "High monitoring"
        },

        {
            "zone": "Mokokchung",
            "lat": 26.3200,
            "lon": 94.5200,

            "rainfall": 175,
            "soil": 76,
            "slope": 35,
            "elevation": 1325,
            "historical": 5,
            "forecast": 100,

            "population": 25000,

            "road_status": "Open",

            "shelter": "Mokokchung Relief Centre",

            "route": "Monitor official weather and disaster alerts.",

            "response_priority": "Preparedness"
        },

        {
            "zone": "Mon",
            "lat": 26.7300,
            "lon": 95.0300,

            "rainfall": 210,
            "soil": 84,
            "slope": 43,
            "elevation": 900,
            "historical": 8,
            "forecast": 125,

            "population": 15000,

            "road_status": "Caution",

            "shelter": "Mon Relief Centre",

            "route": "Use only authority-confirmed routes.",

            "response_priority": "Immediate field assessment"
        }
    ],


    # ========================================================
    # MIZORAM
    # ========================================================

    "Mizoram": [

        {
            "zone": "Aizawl",
            "lat": 23.7271,
            "lon": 92.7176,

            "rainfall": 240,
            "soil": 91,
            "slope": 48,
            "elevation": 1132,
            "historical": 11,
            "forecast": 145,

            "population": 60000,

            "road_status": "Caution",

            "shelter": "Aizawl Relief Centre",

            "route": "Follow official evacuation directions.",

            "response_priority": "Immediate field assessment"
        },

        {
            "zone": "Lunglei",
            "lat": 22.8900,
            "lon": 92.7400,

            "rainfall": 225,
            "soil": 87,
            "slope": 46,
            "elevation": 722,
            "historical": 9,
            "forecast": 135,

            "population": 30000,

            "road_status": "Caution",

            "shelter": "Lunglei Relief Centre",

            "route": "Use only verified open roads.",

            "response_priority": "High monitoring"
        },

        {
            "zone": "Champhai",
            "lat": 23.4600,
            "lon": 93.3300,

            "rainfall": 190,
            "soil": 79,
            "slope": 42,
            "elevation": 1678,
            "historical": 7,
            "forecast": 115,

            "population": 18000,

            "road_status": "Open",

            "shelter": "Champhai Relief Centre",

            "route": "Follow official local guidance.",

            "response_priority": "Preparedness"
        }
    ],


    # ========================================================
    # MANIPUR
    # ========================================================

    "Manipur": [

        {
            "zone": "Imphal",
            "lat": 24.8170,
            "lon": 93.9368,

            "rainfall": 135,
            "soil": 70,
            "slope": 22,
            "elevation": 786,
            "historical": 4,
            "forecast": 75,

            "population": 250000,

            "road_status": "Open",

            "shelter": "Imphal Relief Centre",

            "route": "Monitor official disaster information.",

            "response_priority": "Routine monitoring"
        },

        {
            "zone": "Senapati",
            "lat": 25.2700,
            "lon": 94.0200,

            "rainfall": 190,
            "soil": 82,
            "slope": 43,
            "elevation": 1061,
            "historical": 8,
            "forecast": 115,

            "population": 22000,

            "road_status": "Caution",

            "shelter": "Senapati Relief Centre",

            "route": "Follow authority-confirmed evacuation routes.",

            "response_priority": "High monitoring"
        },

        {
            "zone": "Churachandpur",
            "lat": 24.3330,
            "lon": 93.6700,

            "rainfall": 170,
            "soil": 78,
            "slope": 37,
            "elevation": 914,
            "historical": 6,
            "forecast": 100,

            "population": 30000,

            "road_status": "Open",

            "shelter": "Churachandpur Relief Centre",

            "route": "Follow official instructions.",

            "response_priority": "Preparedness"
        }
    ],


    # ========================================================
    # ASSAM
    # ========================================================

    "Assam": [

        {
            "zone": "Guwahati",
            "lat": 26.1445,
            "lon": 91.7362,

            "rainfall": 145,
            "soil": 72,
            "slope": 18,
            "elevation": 55,
            "historical": 5,
            "forecast": 85,

            "population": 1100000,

            "road_status": "Open",

            "shelter": "Guwahati District Relief Centre",

            "route": "Follow official disaster management instructions.",

            "response_priority": "Preparedness"
        },

        {
            "zone": "Dima Hasao",
            "lat": 25.5000,
            "lon": 93.0000,

            "rainfall": 230,
            "soil": 87,
            "slope": 44,
            "elevation": 900,
            "historical": 9,
            "forecast": 140,

            "population": 12000,

            "road_status": "Caution",

            "shelter": "Dima Hasao Relief Centre",

            "route": "Use only officially confirmed open roads.",

            "response_priority": "Immediate field assessment"
        },

        {
            "zone": "Karbi Anglong",
            "lat": 26.0000,
            "lon": 93.5000,

            "rainfall": 180,
            "soil": 79,
            "slope": 35,
            "elevation": 500,
            "historical": 6,
            "forecast": 105,

            "population": 25000,

            "road_status": "Open",

            "shelter": "Karbi Anglong Relief Centre",

            "route": "Follow official local guidance.",

            "response_priority": "Preparedness"
        }
    ],


    # ========================================================
    # TRIPURA
    # ========================================================

    "Tripura": [

        {
            "zone": "Agartala",
            "lat": 23.8315,
            "lon": 91.2868,

            "rainfall": 120,
            "soil": 65,
            "slope": 12,
            "elevation": 16,
            "historical": 2,
            "forecast": 65,

            "population": 400000,

            "road_status": "Open",

            "shelter": "Agartala Relief Centre",

            "route": "Monitor official weather and emergency alerts.",

            "response_priority": "Routine monitoring"
        },

        {
            "zone": "Dhalai",
            "lat": 23.9000,
            "lon": 91.8500,

            "rainfall": 165,
            "soil": 75,
            "slope": 27,
            "elevation": 300,
            "historical": 4,
            "forecast": 90,

            "population": 18000,

            "road_status": "Open",

            "shelter": "Dhalai Relief Centre",

            "route": "Follow official instructions if conditions change.",

            "response_priority": "Preparedness"
        }
    ]
}


# ============================================================
# GET STATES
# ============================================================

def get_states():

    return list(
        ZONE_DATA.keys()
    )


# ============================================================
# GET ZONES
# ============================================================

def get_zones(state):

    return ZONE_DATA.get(
        state,
        []
    )


# ============================================================
# GET SINGLE ZONE
# ============================================================

def get_zone(
    state,
    zone_name
):

    for zone in get_zones(state):

        if zone["zone"] == zone_name:

            return zone.copy()

    return None


# ============================================================
# AI INPUT
# ============================================================

def generate_zone_input(zone):

    return {

        "rainfall": zone["rainfall"],

        "soil": zone["soil"],

        "slope": zone["slope"],

        "elevation": zone["elevation"],

        "historical": zone["historical"],

        "forecast": zone["forecast"]
    }


# ============================================================
# CITIZEN REPORT
# ============================================================

def add_citizen_report(
    state,
    zone,
    incident_type,
    description,
    photo=None
):

    return {

        "state": state,

        "zone": zone,

        "incident_type": incident_type,

        "description": description,

        "photo_uploaded": (
            photo is not None
        ),

        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "status": "Submitted for verification"
    }