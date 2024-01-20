import os
import json
import requests
import polyline

def get_route_by_address(ori, dest, key, mode="DRIVE"):
    data = {
        "origin": {"address": ori},
        "destination": {"address": dest},
        "travelMode": mode,
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "IMPERIAL"
    }

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    return requests.post(url, json=data, headers=headers).json()


def get_route_by_location(ori, dest, key, mode="DRIVE"):
    data = {
        "origin": {"location": {"latLng": ori}},
        "destination": {"location": {"latLng": dest}},
        "travelMode": mode,
        "computeAlternativeRoutes": False,
        "routeModifiers": {
            "avoidTolls": False,
            "avoidHighways": False,
            "avoidFerries": False
        },
        "languageCode": "en-US",
        "units": "IMPERIAL"
    }
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": key,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.polyline.encodedPolyline"
    }
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes'
    return requests.post(url, json=data, headers=headers).json()


def convert_to_geojson(encodedPolyline, fName='result'):
    l = polyline.decode(encodedPolyline)
    l = [list(i)[::-1] for i in l]
    geojs = {
                "type": "FeatureCollection",
                "features": [{"type": "Feature", "geometry": {"type":"LineString","coordinates":l}}]
            }
    output_file = open(f"results/{fName}.geojson", "w", encoding="utf-8")
    json.dump(geojs, output_file)
    output_file.close()
    return geojs