"""
Modele pour waypoints.py (cp waypoints.example.py waypoints.py).
waypoints.py est dans .gitignore : ton itineraire personnel n'y est jamais commite.
"""
from generate_hiking_gpx import Waypoint

TRIPS = [
    (
        "Jour 1 - Exemple",
        [
            Waypoint("Point de depart", 45.000000, 6.000000),
            Waypoint("Point intermediaire", 45.010000, 6.010000),
            Waypoint("Point d'arrivee", 45.020000, 6.020000),
        ],
        "jour1_exemple.gpx",
    ),
]
