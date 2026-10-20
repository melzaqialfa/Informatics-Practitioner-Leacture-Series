"""Sesi 4 - Introduction to Machine Learning
Studi kasus: prediksi kelayakan pinjaman dengan Random Forest (data simulasi)."""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

rng = np.random.default_rng(11)
n = 2000

# 1. Dataset pemohon pinjaman
df = pd.DataFrame({
    "pendapatan_juta": rng.normal(8, 3, n).clip(2, 30).round(1),
    "jumlah_pinjaman_juta": rng.normal(60, 25, n).clip(5, 200).round(1),
    "skor_kredit": rng.normal(650, 80, n).clip(300, 850).round(),
    "usia": rng.integers(21, 66, n),
    "rasio_utang": rng.uniform(0.05, 0.8, n).round(2),
})
skor = (0.012 * (df.skor_kredit - 650) + 0.25 * (df.pendapatan_juta - 8)
        - 0.02 * (df.jumlah_pinjaman_juta - 60) - 4 * (df.rasio_utang - 0.4))
df["disetujui"] = (skor + rng.normal(0, 1, n) > 0).astype(int)
print(f"Proporsi disetujui: {df.disetujui.mean():.1%}\n")

# 2. Pisah data: 80% latih, 20% uji
X, y = df.drop(columns="disetujui"), df.disetujui
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=11)

# 3. Latih Random Forest
model = RandomForestClassifier(n_estimators=200, random_state=11).fit(Xtr, ytr)

# 4. Evaluasi
pred = model.predict(Xte)
print(f"Akurasi: {accuracy_score(yte, pred):.3f}")
print("Confusion matrix [baris=aktual, kolom=prediksi]:\n", confusion_matrix(yte, pred))
print(classification_report(yte, pred, target_names=["ditolak", "disetujui"]))
print("Fitur terpenting:\n", pd.Series(model.feature_importances_, X.columns).sort_values(ascending=False).round(3), "\n")

# 5. Coba pada pemohon baru
baru = pd.DataFrame([
    dict(pendapatan_juta=12, jumlah_pinjaman_juta=40, skor_kredit=740, usia=35, rasio_utang=0.15),
    dict(pendapatan_juta=4, jumlah_pinjaman_juta=120, skor_kredit=520, usia=24, rasio_utang=0.65),
])
for i, p in enumerate(model.predict_proba(baru)[:, 1], 1):
    print(f"Pemohon {i}: probabilitas disetujui {p:.0%} -> {'SETUJU' if p >= 0.5 else 'TOLAK'}")
