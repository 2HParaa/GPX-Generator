"""
Genere une trace GPX suivant les sentiers reels a partir d'une liste de points
de passage, via l'API de routing pedestre d'OpenRouteService (profil foot-hiking).

Usage:
    python generate_hiking_gpx.py

Necessite une cle API ORS dans une variable d'environnement ORS_API_KEY
(voir .env.example). Cree un compte gratuit sur https://openrouteservice.org/dev/#/signup
"""
import os
import json
import requests
from dataclasses import dataclass

ORS_BASE_URL = "https://api.openrouteservice.org/v2/directions/foot-hiking"


@dataclass
class Waypoint:
    name: str
    lat: float
    lon: float


def route_between(waypoints: list[Waypoint], api_key: str) -> dict:
    """Appelle ORS pour router entre une sequence de points (>= 2), en
    respectant l'ordre, et renvoie le GeoJSON de la reponse (avec geometrie +
    distance/denivele/duree)."""
    coords = [[wp.lon, wp.lat] for wp in waypoints]  # ORS attend [lon, lat]
    resp = requests.post(
        ORS_BASE_URL + "/geojson",
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
        },
        json={"coordinates": coords, "elevation": True},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def geojson_to_gpx(geojson: dict, track_name: str, waypoints: list[Waypoint]) -> str:
    """Convertit la reponse GeoJSON ORS (LineString avec altitude) en GPX."""
    import gpxpy
    import gpxpy.gpx

    gpx = gpxpy.gpx.GPX()
    gpx.name = track_name

    for wp in waypoints:
        gpx.waypoints.append(gpxpy.gpx.GPXWaypoint(wp.lat, wp.lon, name=wp.name))

    track = gpxpy.gpx.GPXTrack(name=track_name)
    gpx.tracks.append(track)
    seg = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(seg)

    coords = geojson["features"][0]["geometry"]["coordinates"]  # [lon, lat, ele]
    for c in coords:
        lon, lat = c[0], c[1]
        ele = c[2] if len(c) > 2 else None
        seg.points.append(gpxpy.gpx.GPXTrackPoint(lat, lon, elevation=ele))

    return gpx.to_xml()


def main():
    api_key = os.environ.get("ORS_API_KEY")
    if not api_key:
        raise SystemExit(
            "Variable d'environnement ORS_API_KEY manquante. "
            "Copie .env.example vers .env, renseigne ta cle, puis "
            "`export $(cat .env | xargs)` avant de relancer."
        )

    try:
        from waypoints import TRIPS
    except ImportError:
        raise SystemExit(
            "waypoints.py manquant. Copie waypoints.example.py vers waypoints.py "
            "et renseigne tes propres points de passage."
        )

    for track_name, waypoints, out_path in TRIPS:
        geojson = route_between(waypoints, api_key)
        gpx_xml = geojson_to_gpx(geojson, track_name, waypoints)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(gpx_xml)

        summary = geojson["features"][0]["properties"]["summary"]
        print(f"OK -> {out_path}")
        print(f"Distance: {summary['distance']/1000:.1f} km, "
              f"Duree estimee: {summary['duration']/3600:.1f} h")


if __name__ == "__main__":
    main()
