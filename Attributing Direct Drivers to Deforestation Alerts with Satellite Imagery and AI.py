"""Sesi 6 - Attributing Direct Drivers to Deforestation Alerts with Satellite Imagery and AI
Studi kasus: identifikasi penyebab deforestasi dari fitur satelit dengan Random Forest (data simulasi).
Catatan: label awal dibuat dari ATURAN, jadi model belajar meniru aturan itu. Pada kasus nyata,
gunakan label hasil interpretasi visual/lapangan."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(21)
n = 2500

# 1. Dataset simulasi peringatan deforestasi
df = pd.DataFrame({
    "delta_ndvi": -rng.uniform(0.05, 0.7, n).round(3),   # penurunan vegetasi (negatif)
    "delta_nbr": -rng.uniform(0.0, 0.8, n).round(3),     # penurunan NBR besar -> indikasi bekas terbakar
    "jarak_jalan_km": rng.exponential(4, n).round(2),
    "luas_ha": rng.lognormal(1.5, 1.0, n).round(2),
})


# 2. Label awal berdasarkan aturan
def label(r):
    if r.delta_nbr < -0.45:
        return "kebakaran"
    if r.luas_ha > 12 and r.jarak_jalan_km < 8:
        return "perkebunan"
    if r.jarak_jalan_km < 1.0:
        return "infrastruktur_jalan"
    return "perambahan_kecil"


df["penyebab"] = df.apply(label, axis=1)
print("Distribusi label:\n", df.penyebab.value_counts(), "\n")

# 3. Latih Random Forest
X, y = df.drop(columns="penyebab"), df.penyebab
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.25, stratify=y, random_state=21)
model = RandomForestClassifier(n_estimators=200, random_state=21).fit(Xtr, ytr)
print(classification_report(yte, model.predict(Xte), zero_division=0))

# 4. Klasifikasi peringatan baru
baru = pd.DataFrame([
    dict(delta_ndvi=-0.60, delta_nbr=-0.70, jarak_jalan_km=6.0, luas_ha=12.0),
    dict(delta_ndvi=-0.50, delta_nbr=-0.10, jarak_jalan_km=3.0, luas_ha=80.0),
    dict(delta_ndvi=-0.30, delta_nbr=-0.05, jarak_jalan_km=0.4, luas_ha=2.5),
    dict(delta_ndvi=-0.20, delta_nbr=-0.10, jarak_jalan_km=12.0, luas_ha=1.2),
])
proba = model.predict_proba(baru)
for i, (pred, p) in enumerate(zip(model.predict(baru), proba.max(axis=1)), 1):
    print(f"Peringatan {i}: {pred:<20} (keyakinan {p:.0%})")
