"""Sesi 1 - Make Sense of Data with Analysis and AI
Studi kasus: Analisis risiko piutang dan penentuan strategi penanganan kredit (data simulasi).
Alur: data -> imputasi median -> analisis deskriptif -> diagnostik -> prediktif -> rekomendasi."""
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(7)
n = 1500

# 1. Dataset transaksi piutang (simulasi)
df = pd.DataFrame({
    "nilai_tagihan_juta": rng.lognormal(3.0, 0.6, n).round(2),
    "diskon_persen": rng.choice([0, 2, 5, 8, 10], n, p=[.35, .2, .2, .15, .1]),
    "tenor_hari": rng.choice([30, 45, 60], n),
    "lama_pelanggan_tahun": rng.integers(0, 15, n).astype(float),
    "riwayat_telat": rng.poisson(1.2, n).astype(float),
})
logit = (-2.0 + 0.015 * df.nilai_tagihan_juta + 0.55 * df.riwayat_telat
         + 0.02 * df.tenor_hari - 0.12 * df.lama_pelanggan_tahun - 0.10 * df.diskon_persen)
df["gagal_bayar"] = (rng.random(n) < 1 / (1 + np.exp(-logit))).astype(int)
for col in ["lama_pelanggan_tahun", "riwayat_telat"]:  # sisipkan data hilang
    df.loc[rng.random(n) < 0.08, col] = np.nan

# 2. Pengolahan data: cek nilai hilang lalu isi dengan median
print("Nilai hilang per kolom:\n", df.isna().sum()[df.isna().sum() > 0], "\n")
fitur = [c for c in df.columns if c != "gagal_bayar"]
df[fitur] = SimpleImputer(strategy="median").fit_transform(df[fitur])

# 3. Analisis deskriptif: kondisi piutang
print("== DESKRIPTIF ==")
print(f"Total tagihan: Rp {df.nilai_tagihan_juta.sum():,.0f} juta | gagal bayar: {df.gagal_bayar.mean():.1%}\n")

# 4. Analisis diagnostik: apakah diskon berkaitan dengan risiko?
print("== DIAGNOSTIK: tingkat gagal bayar per diskon ==")
print(df.groupby("diskon_persen").gagal_bayar.agg(["count", "mean"]).round(3), "\n")

# 5. Analisis prediktif: Logistic Regression
Xtr, Xte, ytr, yte = train_test_split(df[fitur], df.gagal_bayar, test_size=0.25,
                                      stratify=df.gagal_bayar, random_state=7)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, class_weight="balanced"))
model.fit(Xtr, ytr)
proba = model.predict_proba(Xte)[:, 1]
print("== PREDIKTIF ==")
print(f"ROC-AUC: {roc_auc_score(yte, proba):.3f}")
print(classification_report(yte, model.predict(Xte), zero_division=0))

# 6. Simulasi rekomendasi kebijakan berdasarkan probabilitas gagal bayar
def kebijakan(p):
    if p < 0.30: return "Lanjutkan kredit normal"
    if p < 0.60: return "Kirim pengingat & kurangi tenor"
    return "Tagih intensif / minta uang muka"

hasil = pd.DataFrame({"prob_gagal_bayar": proba.round(3)})
hasil["rekomendasi"] = hasil.prob_gagal_bayar.map(kebijakan)
print("== REKOMENDASI ==")
print(hasil.rekomendasi.value_counts())
