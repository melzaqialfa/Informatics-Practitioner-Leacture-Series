"""Sesi 3 - Career and Competition in Industrial Era with GIS
Studi kasus: pemantauan kondisi aset infrastruktur berdasarkan informasi geografis (data simulasi).
Alur: data aset -> jarak Haversine ke zona bahaya -> skor prioritas -> ekspor GeoJSON."""
import json
import math
import os
import random

random.seed(3)
JENIS = ["jembatan", "jalan", "drainase", "gorong-gorong", "tanggul"]
PUSAT_BAHAYA = (-3.80, 102.26)   # contoh: pusat zona rawan banjir (sekitar Kota Bengkulu)
RADIUS_KM = 3.0


def haversine_km(lat1, lon1, lat2, lon2):
    r = 6371.0088
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(a))


# 1. Data aset: identitas, jenis, koordinat, usia, kerusakan
aset = [{
    "id": f"AST-{i:03d}",
    "jenis": random.choice(JENIS),
    "lat": -3.80 + random.uniform(-0.06, 0.06),
    "lon": 102.26 + random.uniform(-0.06, 0.06),
    "usia_tahun": random.randint(1, 45),
    "kerusakan_persen": random.randint(0, 80),
} for i in range(1, 41)]

# 2. Perhitungan spasial + penilaian prioritas (bobot dapat disesuaikan)
for a in aset:
    a["jarak_km"] = round(haversine_km(a["lat"], a["lon"], *PUSAT_BAHAYA), 2)
    a["dalam_zona"] = a["jarak_km"] <= RADIUS_KM
    skor = 0.4 * (a["usia_tahun"] / 45) + 0.4 * (a["kerusakan_persen"] / 100) \
        + 0.2 * max(0, 1 - a["jarak_km"] / RADIUS_KM)
    a["skor_prioritas"] = round(skor * 100, 1)

aset.sort(key=lambda a: a["skor_prioritas"], reverse=True)
print(f"{sum(a['dalam_zona'] for a in aset)} dari {len(aset)} aset berada dalam radius {RADIUS_KM} km zona bahaya\n")
print("Top 5 prioritas inspeksi:")
for a in aset[:5]:
    print(f"  {a['id']} {a['jenis']:<14} skor {a['skor_prioritas']:5.1f} | {a['jarak_km']} km | rusak {a['kerusakan_persen']}%")

# 3. Ekspor GeoJSON (urutan koordinat: [lon, lat]) agar bisa dibuka di QGIS / geojson.io
fitur = [{"type": "Feature",
          "geometry": {"type": "Point", "coordinates": [a["lon"], a["lat"]]},
          "properties": {k: v for k, v in a.items() if k not in ("lat", "lon")}} for a in aset]
os.makedirs("output", exist_ok=True)
with open("output/aset_infrastruktur.geojson", "w", encoding="utf-8") as f:
    json.dump({"type": "FeatureCollection", "features": fitur}, f, indent=2)
print("\nTersimpan: output/aset_infrastruktur.geojson")
