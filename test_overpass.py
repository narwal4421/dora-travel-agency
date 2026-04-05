import requests
import json

lat, lon = "48.8566", "2.3522" # Paris
query = f"""
[out:json];
(
  node["tourism"~"museum|gallery|theme_park|zoo"](around:5000,{lat},{lon});
  way["historic"~"monument|castle|ruins"](around:5000,{lat},{lon});
  node["historic"~"monument|castle|ruins"](around:5000,{lat},{lon});
);
out center 15;
"""
url = "http://overpass-api.de/api/interpreter"
resp = requests.post(url, data={'data': query})
if resp.status_code == 200:
    data = resp.json()
    places = [el.get('tags', {}).get('name') for el in data.get('elements', []) if el.get('tags', {}).get('name')]
    print(list(set(places)))
else:
    print("Error", resp.status_code, resp.text)
