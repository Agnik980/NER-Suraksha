import math


# ============================================================
# AI LANDSLIDE RISK MODEL
# ============================================================

def predict_risk(data):
    """
    Prototype landslide-risk prediction.

    Inputs:
        rainfall
        soil
        slope
        elevation
        historical
        forecast

    Returns:
        Risk percentage from 0 to 99.
    """

    rainfall = float(data.get("rainfall", 0))
    soil = float(data.get("soil", 0))
    slope = float(data.get("slope", 0))
    elevation = float(data.get("elevation", 0))
    historical = float(data.get("historical", 0))
    forecast = float(data.get("forecast", 0))

    # Normalize values
    rainfall_score = min(rainfall / 200, 1.0)
    soil_score = min(soil / 100, 1.0)
    slope_score = min(slope / 45, 1.0)
    elevation_score = min(elevation / 2500, 1.0)
    historical_score = min(historical / 10, 1.0)
    forecast_score = min(forecast / 150, 1.0)

    # Weighted risk model
    risk = (
        rainfall_score * 25
        + soil_score * 15
        + slope_score * 20
        + elevation_score * 5
        + historical_score * 15
        + forecast_score * 20
    )

    return max(
        0,
        min(99, risk)
    )


# ============================================================
# RISK LEVEL
# ============================================================

def risk_level(risk):

    risk = float(risk)

    if risk >= 80:
        return "CRITICAL"

    elif risk >= 60:
        return "HIGH"

    elif risk >= 35:
        return "MEDIUM"

    return "LOW"


# ============================================================
# POPULATION EXPOSURE
# ============================================================

def population_exposure(
    risk,
    population
):
    """
    Estimates the population potentially exposed
    according to the current risk score.

    This is a prototype estimate, not an official
    population-at-risk calculation.
    """

    risk = max(
        0,
        min(100, float(risk))
    )

    population = max(
        0,
        int(population)
    )

    exposed = int(
        population * (risk / 100)
    )

    return exposed


# ============================================================
# EMERGENCY PRIORITY
# ============================================================

def emergency_priority(
    risk,
    population,
    road_status
):
    """
    Higher score = greater emergency priority.
    """

    risk = float(risk)

    population = max(
        0,
        int(population)
    )

    population_factor = min(
        population / 10000,
        1
    ) * 25

    road_factor = {

        "Blocked": 25,

        "Caution": 15,

        "Open": 5

    }.get(
        road_status,
        10
    )

    score = (
        risk * 0.70
        + population_factor
        + road_factor
    )

    return round(
        min(100, score),
        1
    )


# ============================================================
# PRIORITY LABEL
# ============================================================

def priority_label(score):

    score = float(score)

    if score >= 80:
        return "IMMEDIATE"

    elif score >= 60:
        return "VERY HIGH"

    elif score >= 40:
        return "HIGH"

    elif score >= 20:
        return "MEDIUM"

    return "LOW"


# ============================================================
# DISTANCE CALCULATION
# ============================================================

def calculate_distance(
    lat1,
    lon1,
    lat2,
    lon2
):
    """
    Calculates approximate distance between
    two GPS coordinates in kilometres.
    """

    earth_radius = 6371.0

    lat1 = math.radians(
        float(lat1)
    )

    lat2 = math.radians(
        float(lat2)
    )

    delta_lat = math.radians(
        float(lat2) - float(lat1)
    )

    delta_lon = math.radians(
        float(lon2) - float(lon1)
    )

    a = (
        math.sin(delta_lat / 2) ** 2
        +
        math.cos(lat1)
        * math.cos(lat2)
        * math.sin(delta_lon / 2) ** 2
    )

    c = 2 * math.atan2(
        math.sqrt(a),
        math.sqrt(1 - a)
    )

    return earth_radius * c


# ============================================================
# ROUTE SAFETY SCORE
# ============================================================

def route_safety_score(
    route_risk,
    distance_km,
    road_status,
    population_exposure_value=0
):
    """
    Calculates route safety.

    Higher score = safer route.

    Factors:
        - landslide risk
        - road condition
        - distance
        - exposed population
    """

    route_risk = max(
        0,
        min(100, float(route_risk))
    )

    distance_km = max(
        0,
        float(distance_km)
    )

    population_exposure_value = max(
        0,
        float(population_exposure_value)
    )

    # Risk component
    risk_score = 100 - route_risk

    # Distance component
    distance_score = max(
        0,
        100 - (distance_km * 5)
    )

    # Road condition
    road_score = {

        "Open": 100,

        "Caution": 55,

        "Blocked": 0

    }.get(
        road_status,
        40
    )

    # Population exposure
    exposure_score = max(
        0,
        100 - min(
            population_exposure_value / 100,
            100
        )
    )

    # Weighted final score
    score = (

        risk_score * 0.45

        + road_score * 0.30

        + distance_score * 0.15

        + exposure_score * 0.10
    )

    return round(
        max(0, min(100, score)),
        1
    )


# ============================================================
# ROUTE STATUS
# ============================================================

def route_status(
    safety_score,
    road_status
):

    if road_status == "Blocked":

        return "AVOID"

    if safety_score >= 75:

        return "SAFEST"

    elif safety_score >= 55:

        return "ALTERNATIVE"

    elif safety_score >= 35:

        return "CAUTION"

    return "AVOID"


# ============================================================
# FIND SAFEST ROUTE
# ============================================================

def find_safest_route(
    routes,
    current_lat,
    current_lon
):
    """
    Selects the safest route from a list of
    available evacuation routes.

    Each route should contain:

        name
        lat
        lon
        risk
        road_status
        population_exposure
        shelter
    """

    evaluated_routes = []

    for route in routes:

        route_lat = float(
            route.get("lat", current_lat)
        )

        route_lon = float(
            route.get("lon", current_lon)
        )

        distance = calculate_distance(

            current_lat,
            current_lon,

            route_lat,
            route_lon
        )

        risk = float(
            route.get("risk", 50)
        )

        road_status = route.get(
            "road_status",
            "Caution"
        )

        exposure = float(
            route.get(
                "population_exposure",
                0
            )
        )

        score = route_safety_score(

            risk,

            distance,

            road_status,

            exposure
        )

        status = route_status(

            score,

            road_status
        )

        evaluated_routes.append({

            **route,

            "distance_km":
                round(distance, 2),

            "safety_score":
                score,

            "route_status":
                status
        })

    # Remove blocked routes from recommendation
    available_routes = [

        route

        for route in evaluated_routes

        if route["road_status"] != "Blocked"
    ]

    if not available_routes:

        return None, evaluated_routes

    safest = max(

        available_routes,

        key=lambda x:
            x["safety_score"]
    )

    return safest, evaluated_routes


# ============================================================
# BUILD ROUTES FROM ZONES
# ============================================================

def generate_evacuation_routes(
    current_zone,
    all_zones
):
    """
    Creates prototype evacuation-route candidates.

    In a real deployment, replace this with a
    road-network routing engine and live GIS data.
    """

    routes = []

    for zone in all_zones:

        if zone["zone"] == current_zone["zone"]:
            continue

        route = {

            "name":
                f"Route via {zone['zone']}",

            "lat":
                zone["lat"],

            "lon":
                zone["lon"],

            "risk":
                zone.get("risk", 50),

            "road_status":
                zone.get(
                    "road_status",
                    "Caution"
                ),

            "population_exposure":
                zone.get(
                    "exposed",
                    0
                ),

            "shelter":
                zone.get(
                    "shelter",
                    "Designated Relief Centre"
                )
        }

        routes.append(route)

    return routes


# ============================================================
# COMPLETE SAFE ROUTE ANALYSIS
# ============================================================

def calculate_safe_routes(
    current_zone,
    all_zones
):
    """
    Complete route analysis for the selected
    location.
    """

    routes = generate_evacuation_routes(

        current_zone,

        all_zones
    )

    safest, evaluated = find_safest_route(

        routes,

        current_zone["lat"],

        current_zone["lon"]
    )

    return {

        "safest_route":
            safest,

        "all_routes":
            sorted(

                evaluated,

                key=lambda x:
                    x["safety_score"],

                reverse=True
            )
    }


# ============================================================
# CITIZEN SAFETY RECOMMENDATION
# ============================================================

def citizen_recommendation(
    risk,
    route
):

    risk = float(risk)

    if route is None:

        return (
            "🚨 No currently available route "
            "can be recommended. Follow official "
            "emergency instructions."
        )

    if risk >= 80:

        return (
            "🚨 CRITICAL RISK: Follow official "
            "evacuation instructions and use only "
            "a route verified by emergency authorities."
        )

    elif risk >= 60:

        return (
            "⚠️ HIGH RISK: Stay alert, monitor "
            "official warnings and prepare for "
            "possible evacuation."
        )

    else:

        return (
            "🟢 Continue monitoring conditions "
            "and follow official safety guidance."
        )