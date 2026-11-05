"""Synthesize an original background track + SFX for the 42 s SALYSS Commerce promo.
Problem section (0-15 s): tense, sparse.  Riser -> impact at 15 s.
Solution section (15-37 s): upbeat groove.  End card (37-42 s): resolve + fade."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
DUR = 42.0
N = int(SR * DUR)
BPM = 100
BEAT = 60 / BPM
rng = np.random.default_rng(7)
L = np.zeros(N); R = np.zeros(N)

def t_arr(d): return np.arange(int(d * SR)) / SR
def midi(m): return 440 * 2 ** ((m - 69) / 12)
def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)

def add(sig, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= N: return
    sig = sig[:N - i]
    gl = gain * np.sqrt(0.5 * (1 - pan)); gr = gain * np.sqrt(0.5 * (1 + pan))
    L[i:i + len(sig)] += sig * gl; R[i:i + len(sig)] += sig * gr

def env(n, a, d_total, rel=None):
    e = np.ones(n)
    na = min(n, max(1, int(a * SR))); e[:na] = np.linspace(0, 1, na)
    if rel:
        nr = min(n, max(1, int(rel * SR))); e[-nr:] *= np.linspace(1, 0, nr)
    return e

# ---------- instruments ----------
def kick(g=1.0):
    t = t_arr(0.45); f = 48 + 110 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return g * np.sin(ph) * np.exp(-t * 7.5) + 0.25 * g * np.exp(-t * 200) * rng.standard_normal(len(t))

def clap():
    t = t_arr(0.3); n = rng.standard_normal(len(t))
    e = np.exp(-t * 22) * (1 + 0.6 * (np.sin(2 * np.pi * 90 * t) > 0) * (t < 0.03))
    return bp(n, 900, 5000) * e * 0.6

def hat(open_=False):
    t = t_arr(0.25 if open_ else 0.06); n = rng.standard_normal(len(t))
    return hp(n, 7000, 4) * np.exp(-t * (14 if open_ else 70)) * 0.35

def saw(f, t, det=0.0):
    out = 0
    for d in (-det, 0, det):
        ph = (f * (1 + d) * t) % 1.0
        out = out + (2 * ph - 1)
    return out / 3

def pad(notes, d, g=0.12, cutoff=1800):
    t = t_arr(d); s = sum(saw(midi(m), t, 0.004) for m in notes) / len(notes)
    s = lp(s, cutoff, 2) * env(len(t), 0.35, d, rel=0.6)
    return s * g

def pluck(m, d=0.5, g=0.18, bright=3500):
    t = t_arr(d); s = saw(midi(m), t, 0.002) + 0.5 * np.sin(2 * np.pi * midi(m + 12) * t)
    return lp(s, bright) * np.exp(-t * 7) * g

def bass(m, d, g=0.3):
    t = t_arr(d); s = np.sin(2 * np.pi * midi(m) * t) + 0.3 * saw(midi(m), t)
    return lp(s, 400) * env(len(t), 0.01, d, rel=0.08) * g

def bell(m, d=1.2, g=0.2):
    t = t_arr(d); f = midi(m)
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 6) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 12)
    return s * np.exp(-t * 3.2) * g

def whoosh(d=0.6, g=0.25, up=True):
    t = t_arr(d); n = rng.standard_normal(len(t))
    out = np.zeros_like(n); seg = 512
    for i in range(0, len(n), seg):
        x = i / len(n); fc = 300 + (5000 if up else 3000) * (x if up else 1 - x)
        out[i:i + seg] = bp(n[i:i + seg + 0][:seg], max(100, fc * 0.6), min(18000, fc * 1.6), 1)
    e = np.sin(np.pi * np.linspace(0, 1, len(t))) ** 2
    return lp(out, 9000) * e * g

def riser(d, g=0.3):
    t = t_arr(d); n = rng.standard_normal(len(t))
    sweep = np.sin(2 * np.pi * np.cumsum(200 + 900 * (t / d) ** 2) / SR)
    out = np.zeros_like(n); seg = 1024
    for i in range(0, len(n), seg):
        x = i / len(n); fc = 400 + 7000 * x ** 2
        out[i:i + seg] = bp(n[i:i + seg], fc * 0.7, min(19000, fc * 1.4), 1)
    return (out * 0.8 + sweep * 0.25) * (t / d) ** 2.2 * g

def impact(g=0.9):
    t = t_arr(2.5); f = 38 + 60 * np.exp(-t * 10)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.2)
    n = lp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 5) * 0.5
    return (sub + n) * g

def click(g=0.35):
    t = t_arr(0.05); return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 160) * g + hp(rng.standard_normal(len(t)), 3000) * np.exp(-t * 300) * g * 0.5

def ping(m=88, g=0.18):
    t = t_arr(0.5); f = midi(m)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)) * np.exp(-t * 9) * g

# ---------- arrangement ----------
# Problem: A minor tension (0-15)
for k in range(int(15 / BEAT)):
    tt = k * BEAT
    if tt >= 14.6: break
    add(bass(33 if (k // 8) % 2 == 0 else 31, BEAT * 0.5, 0.22 + 0.05 * (tt > 6)), tt)       # pulsing low A / G
    if tt >= 3.0: add(hat(), tt + BEAT / 2, 0.6, 0.3)
    if tt >= 6.0 and k % 2 == 0: add(kick(0.55), tt)
    if tt >= 9.0 and k % 4 == 2: add(clap(), tt, 0.5)
tension_chords = [[57, 60, 64], [55, 59, 62], [53, 57, 60], [52, 56, 59]]   # Am G F E
for i, ch in enumerate(tension_chords * 2):
    st = i * BEAT * 4 * 0.5 * 2
    if st >= 14.6: break
    add(pad(ch, min(BEAT * 4, 14.6 - st), 0.07, 1100), st, 1.0, 0)
arp_m = [69, 72, 76, 72]
for k in range(int(3.0 / (BEAT / 2)), int(14.4 / (BEAT / 2))):
    add(pluck(arp_m[k % 4] - (2 if (k // 16) % 2 else 0), 0.35, 0.07, 2200), k * BEAT / 2, 1, 0.35 * (1 if k % 2 else -1))
add(riser(1.4, 0.35), 13.6)
add(impact(0.85), 15.0)
add(whoosh(1.2, 0.18, up=False), 15.0)

# Solution: hopeful groove C - G - Am - F (15-37)
start = 15.0
prog = [[60, 64, 67, 72], [55, 59, 62, 67], [57, 60, 64, 69], [53, 57, 60, 65]]
roots = [36, 31, 33, 29]
bar = BEAT * 4
nb = int((37.0 - start) / bar) + 1
for b in range(nb):
    bt = start + b * bar
    if bt >= 37.0: break
    ch, rt = prog[b % 4], roots[b % 4]
    add(pad(ch, min(bar, 37.0 - bt) + 0.3, 0.075, 2400), bt)
    for k in range(4):
        tt = bt + k * BEAT
        if tt >= 37.0: break
        if not (b == 0 and k == 0): add(kick(0.9), tt)
        if k in (1, 3): add(clap(), tt, 0.8)
        add(bass(rt, BEAT * 0.45), tt); add(bass(rt + 12, BEAT * 0.3, 0.12), tt + BEAT / 2)
        add(hat(), tt + BEAT / 2, 0.8, 0.25); add(hat(), tt + BEAT / 4, 0.35, -0.25)
        if k == 3: add(hat(True), tt + BEAT / 2, 0.4, 0.3)
    arp = [ch[0] + 12, ch[1] + 12, ch[2] + 12, ch[1] + 12]
    for k in range(8):
        tt = bt + k * BEAT / 2
        if tt >= 37.0: break
        add(pluck(arp[k % 4], 0.4, 0.08, 4200), tt, 1, 0.4 * (1 if k % 2 else -1))

# End card (37-42): resolve on C major, bell motif, fade
add(impact(0.5), 37.0)
add(pad([48, 60, 64, 67, 72], 5.0, 0.11, 2600), 37.0)
add(bass(36, 3.5, 0.3), 37.0)
for i, m in enumerate([72, 76, 79, 84]):
    add(bell(m, 2.0, 0.13), 37.4 + i * 0.32, 1, (-0.3, 0.1, 0.3, 0)[i])

# ---------- SFX synced to visuals ----------
for c in [3.0, 6.0, 9.0, 12.0, 18.0, 22.0, 26.0, 30.0, 34.0]:
    add(whoosh(0.55, 0.13), c - 0.25, 1, 0)
for i in range(5):                       # notifications
    add(ping(86 + (i % 2) * 3, 0.13), 3.0 + 0.35 + i * 0.42, 1, 0.2)
add(riser(0.5, 0.12), 13.8 - 0.1)
for tt in [20.5, 27.7]:                  # taps
    add(click(0.35), tt)
add(bell(84, 1.0, 0.12), 27.9); add(bell(88, 1.0, 0.1), 28.0)   # collected
for i in range(4):                        # timeline steps
    add(ping(79 + i * 2, 0.08), 22.55 + i * 0.75)
add(bell(79, 1.0, 0.1), 32.35); add(bell(84, 1.2, 0.1), 32.45)  # accounts match
for i in range(4):                        # flow chips
    add(ping(76 + i * 3, 0.06), 34.6 + i * 0.45)

# ---------- reverb + master ----------
ir_t = t_arr(1.6)
ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t * 3.2); ir = lp(ir, 6000); ir /= np.abs(ir).sum() / 6
wetL = fftconvolve(L, ir)[:N]; wetR = fftconvolve(R, np.roll(ir, 37))[:N]
L2 = L + 0.18 * wetL; R2 = R + 0.18 * wetR
mix = np.stack([L2, R2], 1)
mix = hp(mix.T, 30).T
fade = np.ones(N); nf = int(1.6 * SR); fade[-nf:] = np.linspace(1, 0, nf) ** 1.5
fade[:int(0.05 * SR)] = np.linspace(0, 1, int(0.05 * SR))
mix *= fade[:, None]
mix = np.tanh(mix * 1.4) / np.tanh(1.4)          # gentle saturation / limiting
mix *= 0.89 / np.max(np.abs(mix))
wavfile.write('music.wav', SR, (mix * 32767).astype(np.int16))
print('music.wav written', mix.shape)
