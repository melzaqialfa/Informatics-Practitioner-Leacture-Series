"""Sesi 2 - Bridging Global Infrastructure to Address Local Challenges with HPC
Studi kasus: pemodelan penyebaran polusi PM2.5 (difusi 2D) dengan pemrosesan paralel.
Domain grid dibagi per baris; tiap proses mengerjakan k langkah waktu dengan 'halo' k+1 baris
(mengurangi komunikasi). Hasil paralel diverifikasi sama dengan sekuensial."""
import os
import time
from multiprocessing import Pool

import numpy as np

ALPHA, DECAY = 0.2, 0.0005  # koefisien difusi (<=0.25 agar stabil) dan peluruhan


def step(u, s):
    """Satu langkah waktu; tepi array dianggap tetap (batas konsentrasi nol)."""
    n = u.copy()
    c = u[1:-1, 1:-1]
    n[1:-1, 1:-1] = (c + ALPHA * (u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * c)
                     - DECAY * c + s[1:-1, 1:-1])
    return n


def run_sequential(u, s, steps):
    for _ in range(steps):
        u = step(u, s)
    return u


def _worker(args):
    strip, s_strip, k, a, b = args
    for _ in range(k):
        strip = step(strip, s_strip)
    return strip[a:b]


def run_parallel(u, s, steps, workers, k=25):
    h = u.shape[0]
    bounds = np.linspace(0, h, workers + 1).astype(int)
    with Pool(workers) as pool:
        done = 0
        while done < steps:
            kk = min(k, steps - done)
            tasks = []
            for a, b in zip(bounds[:-1], bounds[1:]):
                lo, hi = max(a - kk - 1, 0), min(b + kk + 1, h)
                tasks.append((u[lo:hi], s[lo:hi], kk, a - lo, b - lo))
            u = np.vstack(pool.map(_worker, tasks))
            done += kk
    return u


def main(size=600, steps=300):
    s = np.zeros((size, size))                      # sumber emisi (mis. pabrik, kebakaran)
    for (i, j, q) in [(150, 150, 0.8), (350, 400, 1.2), (450, 200, 0.6)]:
        s[i, j] = q
    u0 = np.zeros((size, size))

    t = time.perf_counter(); ref = run_sequential(u0, s, steps); t_seq = time.perf_counter() - t
    cores = os.cpu_count() or 1
    print(f"Grid {size}x{size}, {steps} langkah | core tersedia: {cores}")
    print(f"Sekuensial : {t_seq:6.2f} s | PM2.5 maks = {ref.max():.2f}")

    for w in sorted({2, 4, cores} - {1}):
        t = time.perf_counter(); out = run_parallel(u0, s, steps, w); dt = time.perf_counter() - t
        print(f"Paralel {w:>2}  : {dt:6.2f} s | speedup {t_seq/dt:4.2f}x | hasil sama: {np.allclose(ref, out)}")
    if cores == 1:
        print("Catatan: hanya 1 core, jadi paralel tidak akan lebih cepat.")


if __name__ == "__main__":  # wajib untuk multiprocessing di Windows/macOS
    main()
