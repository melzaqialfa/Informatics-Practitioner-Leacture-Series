"""Sesi 5 - Human-Computer Interaction & Data Visualization
Studi kasus: dashboard pemantauan kinerja sistem dengan antarmuka interaktif.
Menghasilkan output/dashboard.html (buka di browser). Prinsip HCI yang diterapkan:
- kartu per metrik (pengelompokan/Gestalt), status memakai warna + ikon + teks (tidak hanya warna)
- tombol diagnostik jelas (affordance) dengan umpan balik langsung (aria-live)"""
import os

METRIK = [  # nama, nilai, satuan, batas_waspada, batas_kritis (semakin tinggi semakin buruk)
    ("Penggunaan CPU", 62, "%", 70, 90),
    ("Penggunaan Memori", 81, "%", 75, 90),
    ("Latensi Respons", 420, "ms", 300, 800),
    ("Tingkat Error", 0.4, "%", 1, 3),
    ("Disk Terpakai", 93, "%", 80, 90),
]


def status(v, waspada, kritis):
    if v >= kritis:
        return "kritis", "⛔", "Kritis"
    if v >= waspada:
        return "waspada", "⚠️", "Waspada"
    return "optimal", "✅", "Optimal"


kartu = ""
for nama, v, sat, w, k in METRIK:
    cls, ikon, label = status(v, w, k)
    kartu += (f'<article class="card {cls}"><h2>{nama}</h2><p class="val">{v}<small>{sat}</small></p>'
              f'<p class="st">{ikon} {label}</p></article>\n')

HTML = f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Dashboard Kinerja Sistem</title>
<style>
body{{font-family:system-ui,sans-serif;margin:0;background:#f4f6f8;color:#1b1f23}}
header{{background:#1e3a5f;color:#fff;padding:16px 24px}}main{{padding:24px;max-width:1000px;margin:auto}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:16px}}
.card{{background:#fff;border-radius:12px;padding:16px;border-top:6px solid;box-shadow:0 1px 4px #0002}}
.card h2{{font-size:.95rem;margin:0;color:#444}}.val{{font-size:2rem;font-weight:700;margin:8px 0}}small{{font-size:1rem;margin-left:3px}}
.optimal{{border-color:#1a7f37}}.waspada{{border-color:#b7791f}}.kritis{{border-color:#c62828}}
button{{margin-top:20px;padding:12px 20px;font-size:1rem;border:0;border-radius:8px;background:#1e3a5f;color:#fff;cursor:pointer}}
button:hover,button:focus-visible{{background:#2c5282;outline:3px solid #90cdf4}}
#pesan{{margin-top:16px;padding:12px;border-radius:8px;background:#e8f0fe;min-height:24px}}
</style></head><body>
<header><h1 style="margin:0;font-size:1.3rem">Dashboard Kinerja Sistem</h1></header>
<main><section class="grid" aria-label="Indikator kinerja">{kartu}</section>
<button id="diag" type="button">Jalankan Diagnostik</button>
<div id="pesan" role="status" aria-live="polite">Tekan tombol untuk memeriksa kondisi sistem.</div></main>
<script>
const kartu=[...document.querySelectorAll('.card')];
document.getElementById('diag').addEventListener('click',()=>{{
  const k=kartu.filter(c=>c.classList.contains('kritis')).map(c=>c.querySelector('h2').textContent);
  const w=kartu.filter(c=>c.classList.contains('waspada')).map(c=>c.querySelector('h2').textContent);
  document.getElementById('pesan').textContent =
    k.length ? 'Diagnostik selesai. KRITIS: '+k.join(', ')+(w.length?' | Waspada: '+w.join(', '):'')+'. Segera tindak lanjuti.'
    : w.length ? 'Diagnostik selesai. Waspada: '+w.join(', ')+'.' : 'Diagnostik selesai. Semua metrik optimal.';
}});
</script></body></html>"""

os.makedirs("output", exist_ok=True)
with open("output/dashboard.html", "w", encoding="utf-8") as f:
    f.write(HTML)
print("Dashboard dibuat: output/dashboard.html")
