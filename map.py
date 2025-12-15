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

    gpx_cache = {}

    for j in journeys:
        gpx_path = j.get("gpxPath")

        if not gpx_path:
            continue

        if gpx_path not in gpx_cache:
            try:
                points = loadGPXPoints(gpx_path)
            except Exception:
                continue

            if not points:
                continue

            gpx_cache[gpx_path] = points
        else:
            points = gpx_cache[gpx_path]

        folium.PolyLine(
            points,
            tooltip=f"{j['originStation']} → {j['destinationStation']}",
            weight=4
        ).add_to(m)

        bounds.extend(points)

    if bounds:
        m.fit_bounds(bounds)

    return m