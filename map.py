import gpxpy
import folium

def loadGPXPoints(gpx_path):
    """
    Reads a GPX file and returns a list of (lat, lon) tuples.
    """
    with open(gpx_path, "r") as f:
        gpx = gpxpy.parse(f)

    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))

    return points

def createMap(journeys):
    """
    journeys: list of dicts from fetch_all_journeys()
    """
    # Fallback center (only used if no GPX exists)
    m = folium.Map(location=[0, 0], zoom_start=2)

    bounds = []

    for j in journeys:
        if not j.get("gpxPath"):
            continue

        try:
            points = loadGPXPoints(j["gpxPath"])
        except Exception:
            continue  # Skip broken GPX files safely

        if not points:
            continue

        folium.PolyLine(
            points,
            tooltip=f"{j['originStation']} → {j['destinationStation']}",
            weight=4
        ).add_to(m)

        bounds.extend(points)

    # Auto-fit map to all routes
    if bounds:
        m.fit_bounds(bounds)

    return m
