# ============================================================================
#  GOLDEN EDGE SUITE — BYBIT BOT  [Power Of Trading]   v1.0 (3 Sep 2026)
#  Port: "Golden Edge Suite | MTF Confluence + Liquidity Zones & Scenario Engine"
#  (Pine v6 — dokumen Google Docs user) + ATURAN 3-LANGKAH dari video
#  "This AI-Built Gold Trading Strategy Was Tested Live" (youtu.be/Dz4_1YBKP0o)
#
#  ── MATEMATIKA (port 1:1 dari Pine / MODULE 1 & 2) ─────────────────────────
#  MODULE 1 — MTF CONFLUENCE per TF (15m, 1H, 4H, 1D):
#     RSI(14) · Golden Zone fib 0.618–0.786 dari range 20 bar ·
#     posisi vs S/R midpoint · Volume USDT vs SMA(20).
#     Bull/Bear count 0–4; sinyal TF = LONG/SHORT bila count >= MIN_COND (4).
#  MODULE 2 — LIQUIDITY ZONES & SCENARIO ENGINE:
#     Zona IMBALANCE (gap) + STOP-POOL (pivot swing 12/4, kedalaman 0.45xATR),
#     digabung bila overlap >= 15%, skor 0–10 (bobot VOL .25 / SIZE .20 /
#     TEST .20 / CONF .20 / PROX .15), decay saat idle, bintang:
#     >=8.0 ELITE ★★★★ | >=6.5 STRONG ★★★ | >=5.0 ★★ | >=3.0 ★
#     Siklus: ACTIVE → CONSUMED (masuk zona) → FILLED/SWEPT (tembus sisi jauh)
#  ── ATURAN 3-LANGKAH (video, persis) ───────────────────────────────────────
#     R1: 1H & 4H HARUS setuju arah (sama LONG atau sama SHORT)
#     R2: harga menyentuh zona likuiditas SANGAT kuat (skor >= 6.5 = 3 bintang)
#     R3: 15m berbalik KE ARAH SAMA saat harga di zona → ENTRY
#     SL : di luar zona (sisi jauh + buffer ATR, + anti-hunt)
#     TP : zona BERLAWANAN terdekat di arah trade (target "next opposite zone")
#  ── EKSEKUSI (gaya bot utama, teruji) ──────────────────────────────────────
#     Risk cap keras, smart-leverage (liq >= 35% di luar SL), SL/TP di bursa,
#     BE (impas+biaya) di 1R, trailing 2.0xATR di 1.5R, guard posisi telanjang,
#     min-order $5, cooldown, Telegram, dashboard, file state/stats/mfe
#     terpisah: ge_state.json · ge_stats.json · ge_mfe.json · ge_bot.log
#
#  CATATAN JUJUR:
#   • Modul zona adalah port FUNGSIONAL (deteksi + skor + siklus persis
#     rumus Pine); fitur GAMBAR (box/label/slide dashboard) tidak dibuat —
#     bot tidak butuh menggambar.
#   • Video & penulis indikator: hasil backtest = alat BANTU keputusan,
#     bukan jaminan profit. Mulai dosis kecil, 1 mode = 1 eksperimen.
# ============================================================================
import json, math, os, sys, time, logging
from datetime import datetime, timezone, timedelta

import pandas as pd
import requests
from pybit.unified_trading import HTTP

# ==================== KONFIGURASI ====================
API_KEY    = "3KutSBJdpR9U3cGBB2"
API_SECRET = "8bmwecJDavuvqA6XKnt8xU6xUn56zdbdWOrU"
TELEGRAM_TOKEN = "8287171493:AAHyCOnwC7mHMSuYAd8grI6MoDEnNSnWBxU"
TELEGRAM_CHAT  = "5316317443"
USE_TESTNET    = False               # True = akun demo/testnet Bybit (uji aman dulu)

# ---- Simbol & mode (menu saat start) ----
FOCUS_SYMBOLS = ["XAUUSDT"]          # selalu diikutkan (emas per video)
ALL_MIN_TURNOVER = 5_000_000         # mode ALL: turnover 24h >= $5jt
TOP_N_CAP      = 30                  # mode TOP: batas jumlah coin paling likuid
SCAN_CHUNK     = 12                  # simbol diproses per siklus (round-robin)
SKIP_RETRY_MIN = 30                  # cek ulang simbol yg di-skip (cap kurang)
DEFAULT_MODE   = 1                   # 1=ALL 2=TOP 3=EMAS (Enter / non-tty)
MODE_LABEL     = {1: "ALL COIN", 2: "TOP %d" % TOP_N_CAP, 3: "EMAS SAJA"}
MODE           = DEFAULT_MODE
SYMBOLS        = list(FOCUS_SYMBOLS)   # diisi refresh_symbols()/menu saat start

# ---- TF strategi (video: 15m trigger, 1H & 4H konfirmasi, 1D referensi) ----
TF_TRIGGER = "15"                    # 15 menit
TF_HTF1    = "60"                    # 1 jam
TF_HTF2    = "240"                   # 4 jam
TF_REF     = "D"                     # 1 hari (info saja)
KF_BARS    = 500                     # jumlah bar kline yang ditarik

# ---- MODULE 1: parameter indikator ----
RSI_LEN    = 14
SR_LOOKBK  = 20                      # S/R & Golden Zone lookback
VOL_LEN    = 20                      # volume SMA
MIN_COND   = 4                       # kondisi minimal utk sinyal TF (1-4)

# ---- MODULE 2: parameter zona ----
USE_GAPS   = True
USE_POOLS  = True
MAX_ZONES  = 28
MIN_GAP_PCT = 0.0
MIN_GAP_ATR = 0.05
LEFT_BARS  = 12
RIGHT_BARS = 4
POOL_H     = 0.45
POOL_BUF   = 0.03
ZONE_ATR_LEN = 200
VOL_BASE_LEN = 50
MERGE_ON   = True
MERGE_PCT  = 15                      # overlap threshold %
STALE_DEV  = 6.0                     # retire bila harga menyimpang 6%
REACT_BARS = 20
REACT_ATR  = 1.0
DECAY_ON   = True
DECAY_BARS = 400
DECAY_FLOOR = 0.60
# skor (bobot)
W_VOL   = 0.25
W_SIZE  = 0.20
W_TEST  = 0.20
W_CONF  = 0.20
W_PROX  = 0.15
SIZE_NORM = 1.20
VOL_NORM  = 1.40
TEST_NORM = 3.0
CONF_NORM = 2.0
PROX_NORM = 6.0
# aturan video
ZONE_MIN_SCORE = 6.5                 # minimal 3 bintang (STRONG)
APPROACH_ATR   = 0.35                # "price tapping zone" (dalam xATR dari tepi)
SL_BUFFER_ATR  = 0.50                # nafas SL di luar zona
MIN_RR         = 1.2                 # tolak setup bila RR < ini
FALLBACK_TP_ATR = 2.5                # TP cadangan bila tak ada zona lawan

# ---- Risiko & eksekusi (gaya bot utama) ----
RISK_CAP_USD  = 0.30                 # rugi maks per trade (dolar keras)
RISK_HARD_USD = 0.30                 # plafon absolut per trade
MARGIN_MAX_PCT = 25.0                # plafon margin per posisi (% saldo)
MAX_LEVERAGE  = 50
MIN_LEVERAGE  = 1
MAX_POSITIONS = 3
COOLDOWN_MIN  = 30                   # jeda antar trade per simbol
MIN_ORDER_USD = 5.0
FEE_RT_PCT    = 0.11                 # fee round-trip %
SLIP_PCT      = 0.03
BE_AT_R       = 1.0                  # SL -> BE (impas+biaya) di 1R
TRAIL_AT_R    = 1.5                  # trailing aktif di 1.5R
TRAIL_ATR_MULT = 2.0
# ---- RIDE: TP1 (zona lawan, per video) -> scale out -> trailing kawal sisa ----
TP1_SCALE_PCT  = 50.0                # % posisi ditutup otomatis di TP1 (bila ada target lanjut)
TP_EXT_MULT    = 1.0                 # TP2 cadangan: TP1 + 1x jarak TP1 (bila tak ada zona lanjut)
TP2_MIN_RR     = 0.6                 # tolak TP2 bila RR-nya < ini (-> full close di TP1)
TRAIL_AFTER_TP1 = True               # trailing HANYA aktif SETELAH TP1 tercapai (guard momentum)

# ---- MARGIN & LEVERAGE (likuidasi TIDAK boleh mendahului SL) ----
MARGIN_TRADE_PCT = 20.0                # target margin per entry = % saldo (mis. $10 -> $2)
LEV_SL_GAP      = 1.5                  # jarak likuidasi = 1.5x jarak SL -> SL tersentuh DULU
LEV_MR_PCT      = 0.015                # cadangan maintenance margin + fee (~1.5%)
LEV_GUARD       = True                 # tutup posisi bila lev bursa ternyata > lev aman

# ---- NEWS GUARD (port bot utama) ----
NEWS_GUARD      = True
NEWS_BTC_FAST   = 0.20                 # shock bila BTC >= 0.20%/MENIT (0.08 = terlalu ketat)
NEWS_MIN_JUMP   = 0.10                 # lonjakan ABSOLUT minimal % (abaikan tick kecil/wiggle)
NEWS_MIN_WINDOW = 20                   # evaluasi hanya bila >= 20 detik sejak cek terakhir
NEWS_EXTEND     = False                # False = jeda TIDAK diperpanjang oleh shock beruntun
NEWS_PAUSE_MIN  = 10                   # jeda entry setelah shock (posisi aktif tetap dikelola)
CPI_GUARD_ON    = True
CPI_PRE_MIN     = 5                    # blok mulai 5 menit sebelum rilis
CPI_POST_MIN    = 20                   # blok sampai 20 menit setelah rilis
# Jadwal rilis CPI AS — sumber: https://www.bls.gov/schedule/news_release/cpi.htm
# (diverifikasi 2026-09-04): Agu'26 -> 11 Sep 08:30 ET(EDT)=19:30 WIB; Sep'26 ->
# 14 Okt (EDT)=19:30 WIB; Okt'26 -> 10 Nov 08:30 ET(EST)=20:30 WIB; Nov'26 ->
# 10 Des (EST)=20:30 WIB. PERBARUI manual tiap tahun (BLS rilis jadwal ~1 thn).
CPI_EVENTS_WIB = [                     # (tahun, bulan, tanggal, jam, menit) WIB
    (2026,  9, 11, 19, 30),  # CPI Agu — Jumat
    (2026, 10, 14, 19, 30),  # CPI Sep — Rabu
    (2026, 11, 10, 20, 30),  # CPI Okt — Selasa (winter time AS)
    (2026, 12, 10, 20, 30),  # CPI Nov — Kamis (winter time AS)
]

# ---- VOLATILITY GUARD ----
VOL_GUARD       = True
VOL_SPIKE_ATR   = 3.0                  # bar 15m > 3x ATR15 = spike -> jeda entry
VOL_MOVE_PCT    = 0.50                 # atau harga loncat > 0.5% dlm 1 bar tutup
VOL_PAUSE_MIN   = 10                   # jeda entry (menit) setelah spike volatilitas

# ---- File terpisah ----
STATE_FILE = "ge_state.json"
STATS_FILE = "ge_stats.json"
MFE_FILE   = "ge_mfe.json"
DAY_FILE   = "ge_day.json"
LOG_FILE   = "ge_bot.log"

WIB = timezone(timedelta(hours=7))
def wib_now():
    return datetime.now(timezone.utc).astimezone(WIB)

logging.Formatter.converter = lambda *a: wib_now().timetuple()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")])
log = logging.getLogger("gbbot")

session = HTTP(api_key=API_KEY, api_secret=API_SECRET, testnet=USE_TESTNET)

# ==================== UTIL BURSA ====================
_lot_cache, _lev_cache, _px_cache = {}, {}, {}
G, R, Y, C, M, B, D, X = ("\033[92m", "\033[91m", "\033[93m", "\033[96m",
                          "\033[95m", "\033[94m", "\033[90m", "\033[0m")

# ==================== UI — gaya bot utama (box + warna + angka raksasa) ====================
import re as _re
WIDTH = 96
UI_ON = True                    # False = tampilan ringkas (cocok utk pipa/log)
FW = "\033[97m\033[1m"
BG_G, BG_R = "\033[48;5;22m", "\033[48;5;52m"
SPIN = ["\u25d0", "\u25d3", "\u25d1", "\u25d2"]
_logbuf = []
_hero_prev = {"sym": "", "px": 0.0}

def _vlen(txt):
    """Panjang VISIBLE, menghitung wide char (emoji/CJK = 2 kolom terminal)."""
    import unicodedata as _ud
    s = _re.sub(r"\033\[[0-9;]*m", "", txt)
    n = 0
    for ch in s:
        n += 2 if _ud.east_asian_width(ch) in ("W", "F") else 1
    return n

def _strip(txt):
    return _re.sub(r"\033\[[0-9;]*m", "", txt)

def _fit(txt, width):
    """Potong teks (perhitungan panjang VISIBLE, ANSI dipertahankan) agar muat kotak."""
    if _vlen(txt) <= width:
        return txt
    out = []
    n = 0
    i = 0
    while i < len(txt) and n < width - 3:
        if txt[i] == "\x1b":
            j = txt.find("m", i)
            if j < 0:
                break
            out.append(txt[i:j + 1])
            i = j + 1
            continue
        out.append(txt[i])
        n += 1
        i += 1
    return "".join(out) + X + "..."

def _row(txt=""):
    txt = _fit(txt, WIDTH - 4)
    pad = max(0, WIDTH - 4 - _vlen(txt))
    return f"{C}\u2551{X} {txt}{' ' * pad} {C}\u2551{X}"

def _rowbg(txt, bg):
    txt = _fit(txt, WIDTH - 4)
    pad = max(0, WIDTH - 4 - _vlen(txt))
    return f"{C}\u2551{X} {bg}{txt}{' ' * pad}{X} {C}\u2551{X}"

_DM = {"\033[92m": "\033[38;2;0;130;0m",     # hijau gelap
       "\033[91m": "\033[38;2;150;0;0m",     # merah gelap
       "\033[93m": "\033[38;2;140;110;0m",   # kuning gelap
       "\033[96m": "\033[38;2;0;120;120m",   # cyan gelap
       "\033[95m": "\033[38;2;140;0;140m",   # magenta gelap
       "\033[94m": "\033[38;2;0;90;160m"}    # biru gelap
def _dim(col):
    return _DM.get(col, "\033[2m" + col)

def _bar(frac, width, col, anim=0):
    """Bar BERWARNA: sisi terisi = col terang, sisa = versi GELAP dari warna sama
    (bukan kelabu). anim bergantian (anim%2) -> efek berdenyut/realtime."""
    frac = max(0.0, min(1.0, frac))
    fill = int(round(frac * width))
    ch = "\u2593" if (anim % 2) else "\u2588"
    return f"{col}{ch * fill}{_dim(col)}{'\u2591' * (width - fill)}{X}"

def _sep(title=""):
    if not title:
        return f"{C}\u2560{'\u2550' * (WIDTH - 2)}\u2563{X}"
    vis = _vlen(title)
    return f"{C}\u2560\u2550 {Y}{title}{X} {C}{'\u2550' * max(0, WIDTH - 6 - vis)}\u2563{X}"

# font raksasa (sama dgn bot utama): digit utk harga/saldo, huruf utk judul
SLIMFONT = {
    '0': ("\u2584\u2580\u2584", "\u2588 \u2588", "\u2588 \u2588", " \u2580 "),
    '1': ("\u2584\u2588 ", " \u2588 ", " \u2588 ", "\u2584\u2588\u2584"),
    '2': ("\u2580\u2580\u2584", "\u2584\u2584\u2580", "\u2588  ", "\u2580\u2580\u2580"),
    '3': ("\u2580\u2580\u2584", " \u2584\u2580", "  \u2588", "\u2580\u2580 "),
    '4': ("\u2588 \u2588", "\u2588\u2584\u2588", "  \u2588", "  \u2588"),
    '5': ("\u2588\u2580\u2580", "\u2580\u2580\u2584", "  \u2588", "\u2580\u2580 "),
    '6': ("\u2584\u2580 ", "\u2588\u2584 ", "\u2588 \u2588", " \u2580 "),
    '7': ("\u2580\u2580\u2588", " \u2588 ", "\u2588  ", "\u2588  "),
    '8': ("\u2584\u2580\u2584", " \u2580 ", "\u2588 \u2588", " \u2580 "),
    '9': ("\u2584\u2580\u2584", " \u2580\u2588", "  \u2588", " \u2580 "),
    '.': (" ", " ", " ", "\u2584"),
}
BIGFONT = {
    'S': ("\u2584\u2580\u2580\u2580", "\u2580\u2580\u2580\u2584", "\u2584  \u2588", " \u2580\u2580 "),
    'H': ("\u2588  \u2588", "\u2588\u2580\u2580\u2588", "\u2588  \u2588", "\u2588  \u2588"),
    'O': ("\u2584\u2580\u2580\u2584", "\u2588  \u2588", "\u2588  \u2588", " \u2580\u2580 "),
    'R': ("\u2588\u2580\u2580\u2584", "\u2588\u2584\u2584\u2580", "\u2588 \u2580\u2584", "\u2588  \u2588"),
    'T': ("\u2580\u2580\u2580\u2580", " \u2588\u2588 ", " \u2588\u2588 ", " \u2588\u2588 "),
    'L': ("\u2588   ", "\u2588   ", "\u2588   ", "\u2588\u2584\u2584\u2584"),
    'N': ("\u2588\u2584 \u2588", "\u2588\u2580\u2584\u2588", "\u2588 \u2580\u2588", "\u2588  \u2588"),
    'G': ("\u2584\u2580\u2580\u2584", "\u2588   ", "\u2588 \u2580\u2588", " \u2580\u2580\u2580"),
    'D': ("\u2588\u2580\u2580\u2584", "\u2588  \u2588", "\u2588  \u2588", "\u2588\u2584\u2584\u2580"),
    'E': ("\u2588\u2580\u2580\u2584", "\u2588\u2584\u2584\u2580", "\u2588   ", "\u2588\u2584\u2584\u2584"),
}


# ---- kurs IDR (sama dengan bot utama) ----
_usd_idr = {"v": 16000.0, "t": 0.0}
def usd_idr():
    if time.time() - _usd_idr["t"] > 1800:
        try:
            r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=6)
            v = float(r.json()["rates"]["IDR"])
            if v > 1000:
                _usd_idr.update({"v": v, "t": time.time()})
        except Exception:
            _usd_idr["t"] = time.time() - 1500   # coba lagi ~5 mnt
    return _usd_idr["v"]

def fmt_rp(v, dec=2):
    """Rupiah gaya Indonesia: 16.278.720,00 (titik ribuan, koma desimal)."""
    s = f"{v:,.{dec}f}"
    return s.replace(",", "@").replace(".", ",").replace("@", ".")

def gold_session(h):
    if 6 <= h < 14:
        return "ASIA", D
    if 14 <= h < 22:
        return "LONDON", Y
    return "NEW YORK", G

def bar_countdown(con15):
    """Sisa waktu hingga bar 15m berjalan ditutup (mm:ss)."""
    try:
        t0 = int(con15["ts"][-1])
        rem = max(0, (t0 + 900000 - int(time.time() * 1000))) // 1000
        return f"{rem // 60:02d}:{rem % 60:02d}"
    except Exception:
        return "--:--"

def fuel_gauge(con):
    """FUEL = bahan bakar momentum: agregat skor bull vs bear (15m+1H+4H) -> 0..100."""
    b = s_ = 0
    for k in ("15", "60", "240"):
        c = con.get(k)
        if c:
            b += c["bull"][-2]
            s_ += c["bear"][-2]
    tot = b + s_
    f = 100.0 * b / tot if tot else 50.0
    col = G if f >= 60 else R if f <= 40 else Y
    return f, col

def scenario_status(con, zsc, px, st, i_now):
    """STATUS SKENARIO (doc: trigger -> target -> reverse -> retest), deskriptif.
    Bukan prediksi: hanya menandai fase pasar dari data nyata; entry tetap 3 aturan."""
    if not isinstance(con, dict) or "60" not in con or "240" not in con or "15" not in con:
        return ("\u25c9", "SCAN", "menunggu data TF (R1 belum bisa dinilai)", D)
    if st.get("in_position"):
        if st.get("tp1_done"):
            return ("\u25c6", "RIDE", f"TP1 tercapai \u00b7 trailing {TRAIL_ATR_MULT}\u00d7ATR "
                    f"mengawal sisa ke TP2 {st.get('tp2') or 0:.6g}", G)
        d = 1 if st["side"] == "Buy" else -1
        pnl = st.get("pos_pnl")
        r0 = st.get("risk0") or 1.0
        if pnl is not None and pnl >= 0.5 * r0:
            return ("\u25b6", "TARGET RUN", f"{'LONG' if d==1 else 'SHORT'} menuju zona lawan "
                    f"\u00b7 SL {st['sl']:.6g} \u00b7 TP {st['tp']:.6g}", G)
        return ("\u25b7", "TRIGGERED", f"{'LONG' if d==1 else 'SHORT'} aktif @ {st['entry']:.6g} "
                f"\u00b7 MFE {st.get('mfe_r') or 0:.2f}R", C)
    s1 = int(con["60"]["sig"][-2])
    s4 = int(con["240"]["sig"][-2])
    if s1 == 0 or s4 == 0 or s1 != s4:
        return ("\u25c9", "SCAN", "cari konfluens 1H & 4H (R1)", D)
    side = "LONG" if s1 == 1 else "SHORT"
    strong = [(z, s) for z, s in zsc if z.dir == -s1 and z.phase != 2 and s >= ZONE_MIN_SCORE]
    if not strong:
        return ("\u25cb", "WAIT", f"HTF searah {side} \u00b7 tunggu harga ke zona kuat "
                f"(skor \u2265 {ZONE_MIN_SCORE})", Y)
    sw = [z for z, s in zsc if z.phase == 2 and i_now - z.last <= REACT_BARS]
    if sw:
        return ("\u2194", "REVERSE", "zona tertembus \u00b7 alihkan pandangan ke sisi lawan", R)
    rt = [z for z, s in strong if z.tests >= 1]
    if rt:
        return ("\u25c9", "RETEST", f"zona sudah diuji {rt[0].tests}× \u00b7 pantau reaksi "
                f"({rt[0].top:.6g}–{rt[0].bot:.6g})", M)
    s15 = int(con["15"]["sig"][-2])
    if s15 == s1:
        return ("\u25c8", "ARM", f"zona {max(s for _, s in strong):.1f}/10 siap \u00b7 "
                f"flip 15m {side} terdeteksi \u00b7 cek RR/cooldown", Y)
    return ("\u25cf", "ARM", f"zona {max(s for _, s in strong):.1f}/10 \u00b7 "
            f"tunggu flip 15m {side} (R3)", Y)

def _bignum(txt):
    letters = [SLIMFONT[ch] for ch in txt if ch in SLIMFONT]
    return ["".join(l[i] for l in letters) for i in range(4)]

def bigword(word):
    rows = ["", "", "", ""]
    for ch in word:
        if ch == " ":
            for i in range(4):
                rows[i] += "   "
        elif ch in BIGFONT:
            for i in range(4):
                rows[i] += BIGFONT[ch][i] + " "
        else:
            for i in range(4):
                rows[i] += "\u2588" + " "
    return [r.rstrip() for r in rows]

def _stars(score):
    n = 4 if score >= 8.0 else 3 if score >= 6.5 else 2 if score >= 5.0 else 1 if score >= 3.0 else 0
    return f"{Y}{'\u2605' * n}{'\u2606' * (4 - n)}{X}"

def add_log(msg):
    log.info(_strip(msg))
    _logbuf.append(f"{D}{wib_now().strftime('%H:%M:%S')}{X} {msg}")
    while len(_logbuf) > 10:
        _logbuf.pop(0)

def say(msg):
    print(msg)
    add_log(msg)

def startup_banner(bal, mode=None):
    L = [f"{C}\u2554{'\u2550' * (WIDTH - 2)}\u2557{X}"]
    for r in bigword("GOLDEN EDGE"):
        L.append(_row(f"{Y}{r}{X}"))
    L.append(_sep("\u25c6 GOLDEN EDGE SUITE — Bybit Gold [Power Of Trading]"))
    _m = mode if mode is not None else MODE
    L.append(_row(f"  {B}Mode{X}       {MODE_LABEL.get(_m, '?')} — {len(SYMBOLS)} simbol "
                  f"{D}({', '.join(FOCUS_SYMBOLS)} selalu diikutkan){X}"))
    L.append(_row(f"  {B}Timeframe{X}  trigger {TF_TRIGGER}m \u00b7 HTF {TF_HTF1}/{TF_HTF2}m"
                  f" \u00b7 ref {TF_REF}"))
    L.append(_row(f"  {B}Aturan{X}     1H&4H searah \u2192 zona \u2265 {ZONE_MIN_SCORE}"
                  f" ({_stars(ZONE_MIN_SCORE)}) \u2192 flip 15m = ENTRY"))
    L.append(_row(f"  {B}Pengaman{X}   cap ${RISK_CAP_USD:.2f}/trade \u00b7 margin "
                  f"{MARGIN_TRADE_PCT:g}% saldo \u00b7 max {MAX_POSITIONS} pos"))
    L.append(_row(f"  {B}Lev aman{X}   SL dulu, baru likuidasi (gap {LEV_SL_GAP}\u00d7SL "
                  f"+{LEV_MR_PCT*100:.1f}%) \u00b7 LEV-GUARD {'ON' if LEV_GUARD else 'OFF'}"))
    L.append(_row(f"  {B}Guard{X}      NEWS {NEWS_PAUSE_MIN}m \u00b7 CPI 5/20m \u00b7 "
                  f"VOL {VOL_PAUSE_MIN}m ({'ON' if NEWS_GUARD and VOL_GUARD else 'OFF'} — dengan "
                  f"posisi aktif tetap dikelola)"))
    L.append(_row(f"  {B}Saldo{X}      {G}${bal:,.2f}{X} \u00b7 Telegram "
                  f"{'ON' if 'GANTI' not in TELEGRAM_TOKEN else 'OFF'}"))
    L.append(_row(f"  {D}Mulai dosis kecil — backtest bukan jaminan profit.{X}"))
    L.append(f"{C}\u255a{'\u2550' * (WIDTH - 2)}\u255d{X}")
    return L


def readiness(con, zsc, px, atrv):
    """Skor KESIAPAN 0-100 utk PERINGKAT (bukan sinyal eksekusi):
    R1 arah HTF 35 + R2 kekuatan zona 35 + R3 flip 15m 15 + RR 15."""
    if "60" not in con or "240" not in con or "15" not in con:
        return 0.0, "DATA\u2026", D
    s1 = int(con["60"]["sig"][-2]); s4 = int(con["240"]["sig"][-2])
    s15 = int(con["15"]["sig"][-2])
    d = s1 if (s1 == s4 and s1 != 0) else 0
    sc = 0.0
    if d != 0:
        sc += 35.0
        cands = [(z, zs) for z, zs in zsc if z.dir == -d and z.phase != 2]
        if cands:
            best = max(zs for _, zs in cands)
            sc += 35.0 * min(best / ZONE_MIN_SCORE, 1.0)
            near = max(cands, key=lambda t: (t[0].top0 + t[0].bot0) / 2) if d == 1 else \
                   min(cands, key=lambda t: (t[0].top0 + t[0].bot0) / 2)
            z = near[0]
            sl = (z.bot - SL_BUFFER_ATR * atrv) if d == 1 else (z.top + SL_BUFFER_ATR * atrv)
            opp = [z2 for z2, _ in zsc if z2.dir == d and z2.phase != 2]
            tp = ((min(z2.bot for z2 in opp) if d == 1 else
                   max(z2.top for z2 in opp)) if opp
                  else px + d * FALLBACK_TP_ATR * atrv)
            rr = abs(tp - px) / max(abs(px - sl), 1e-12)
            sc += 15.0 * min(rr / MIN_RR, 1.0)
        if s15 == d:
            sc += 15.0
    elif s1 == 0 and s4 == 0:
        sc += 5.0
    else:
        sc += 10.0
    sc = round(min(sc, 100.0), 1)
    if sc >= 85:
        return sc, "SIAP", G
    if sc >= 65:
        return sc, "DEKAT", Y
    if sc >= 40:
        return sc, "PANTAU", C
    return sc, "JAUH", D


def _tfmini(c, key, idx):
    sg = int(c["sig"][idx])
    col = G if sg == 1 else R if sg == -1 else D
    ar = "\u25b2" if sg == 1 else "\u25bc" if sg == -1 else "\u2022"
    return f"{col}{ar}{X}{D}{'H' if key != '15' else 'm'}{X}" if key != "15" else f"{col}{ar}{X}"


def _zchip(z, zs):
    dg = "\u25bc" if z.dir == -1 else "\u25b2"
    kd = "\u25c6" if z.kind == 0 else "\u25c8"
    col = G if zs >= ZONE_MIN_SCORE else (Y if zs >= 5.0 else D)
    return f"{col}{kd}{dg}{z.top:.4g}{X}"


def render_dash(bal, ctx):
    """Dashboard 2-tingkat: WATCHDOG (semua coin 1 baris + bar kesiapan %)
    -> WATCHDOG seluruh coin + panel POSISI AKTIF."""
    if not UI_ON:
        return
    L = [f"{C}\u2554{'\u2550' * (WIDTH - 2)}\u2557{X}"]
    sp = SPIN[ctx.get("tick", 0) % len(SPIN)]
    tick = ctx.get("tick", 0)
    idr = usd_idr()
    L.append(_row(f"{FW}\u25c7 GOLDEN EDGE SUITE{X} {sp} "
                  f"{D}|{X} TF {TF_TRIGGER}/{TF_HTF1}/{TF_HTF2}m {D}|{X} zona \u2265 {ZONE_MIN_SCORE}"
                  f" {D}|{X} cap ${RISK_CAP_USD:.2f} {D}|{X} "
                  f"{wib_now().strftime('%d %b %H:%M:%S WIB')}"))
    L.append(_row(f"  {D}kurs 1$ = Rp {fmt_rp(idr, 0)} (auto-refresh 30 mnt){X}"))
    bloc, why = entry_blocked()
    if bloc:
        L.append(_row(f"{R}\u26a0 GUARD AKTIF — {why} | ENTRY DIJEDA{X}"))
    L.append(_sep())
    syms = ctx.get("syms") or []
    # ---- HERO ----
    hero_sym = "BTCUSDT" if MODE != 3 else "XAUUSDT"
    hero = next((e for e in syms if e.get("sym") == hero_sym), None) or (syms[0] if syms else {})
    hsym = hero.get("sym", hero_sym)
    bpx = float(hero.get("px") or 0.0)
    darr, dcol = "\u2022", D
    if _hero_prev.get("sym") == hsym and _hero_prev.get("px"):
        dq = (bpx - _hero_prev["px"]) / _hero_prev["px"] * 100
        dcol = G if dq > 0 else R if dq < 0 else Y
        darr = "\u25b2" if dq > 0 else "\u25bc" if dq < 0 else "\u2022"
    _hero_prev.update({"sym": hsym, "px": bpx})
    btxt = f"{bpx:,.0f}" if hsym == "BTCUSDT" and bpx >= 100 else (
        f"{bpx:.2f}" if bpx >= 100 else f"{bpx:.6g}" if bpx > 0 else "0")
    big_p = _bignum(btxt)
    big_i = _bignum(f"{bal * idr:.0f}")
    half = (WIDTH - 4) // 2
    hero_ic = "\u25c6"
    head_l = (f"{B}{hero_ic} {hsym}{X} {dcol}{darr}{X} {D}({bpx:,.2f}){X} "
              f"{D}[{MODE_LABEL.get(MODE, '?')} \u00b7 {len(SYMBOLS)} simbol]{X}")
    head_r = f"\u25c8 USDT {G}${bal:,.2f}{X} {D}=\u00b7 Rp{X}"
    head_l = _fit(head_l, WIDTH - 6 - _vlen(head_r))
    L.append(_row(head_l + " " * max(1, half - _vlen(head_l)) + head_r))
    for i in range(4):
        lp = f"{Y}{big_p[i]}{X}"
        rp = f"{G}{big_i[i]}{X}"
        L.append(_row(lp + " " * max(1, half - _vlen(lp)) + rp))
    foot_l = f"{D}hero {hsym} \u00b7 live 15m{X}"
    foot_r = f"{G}= Rp {fmt_rp(bal * idr)}{X}"
    L.append(_row(foot_l + " " * max(1, half - _vlen(foot_l)) + foot_r))
    # ---- enlist semua coin (watchdog) + hitung kesiapan ----
    enlist = []
    for e in syms:
        if e.get("skip"):
            continue
        con = e.get("con") or {}
        zsc = e.get("zones") or []
        atrv = e.get("atr") or 0.0
        px = float(e.get("px") or 0.0)
        rdy, tag, col = readiness(con, zsc, px, atrv)
        e["rdy"] = (rdy, tag, col)
        best = max((zs for zn, zs in zsc if zn.phase != 2), default=0.0)
        e["best"] = best
        enlist.append(e)
    enlist.sort(key=lambda e: -e["rdy"][0])
    # ---- WATCHDOG: 1 baris per coin ----
    L.append(_sep(f"\u25c9 WATCHDOG ({len(enlist)} coin \u00b7 urut kesiapan \u00b7 "
                  f"scan {SCAN_CHUNK}/siklus)"))
    if enlist:
        for e in enlist:
            con = e.get("con") or {}
            st = e.get("state") or {}
            s1 = int(con["60"]["sig"][-2]) if "60" in con else 0
            s4 = int(con["240"]["sig"][-2]) if "240" in con else 0
            s15 = int(con["15"]["sig"][-2]) if "15" in con else 0
            a1 = "\u25b2" if s1 == 1 else "\u25bc" if s1 == -1 else "\u2022"
            a4 = "\u25b2" if s4 == 1 else "\u25bc" if s4 == -1 else "\u2022"
            a15 = "\u25b2" if s15 == 1 else "\u25bc" if s15 == -1 else "\u2022"
            fv, fcol = e.get("fuel") or (50.0, Y)
            rdy, tag, col = e["rdy"]
            star = "\u2605" * (4 if e["best"] >= 8.0 else 3 if e["best"] >= 6.5
                                else 2 if e["best"] >= 5.0 else 1 if e["best"] >= 3.0 else 0)
            pf = f"{G}\u25c6{X}" if st.get("in_position") else " "
            row = (f"{pf} {B}{e.get('sym','?'):9s}{X} "
                   f"{G if s1==1 else R if s1==-1 else D}{a1}{X}{D}H{X} "
                   f"{G if s4==1 else R if s4==-1 else D}{a4}{X}{D}H{X} "
                   f"{G if s15==1 else R if s15==-1 else D}{a15}{X}{D}m{X} "
                   f"{fcol}F{fv:3.0f}%{X} "
                   f"{_bar(rdy / 100.0, 18, col, anim=tick)} "
                   f"{col}{rdy:3.0f}% {tag}{X} {Y}{star}{X}")
            L.append(_row(row))
    else:
        L.append(_row(f"  {D}menunggu data pertama\u2026{X}"))
    # ---- baris skip (cap kurang) ----
    for e in syms:
        if e.get("skip"):
            L.append(_row(f"  {D}\u2298 {e.get('sym','?')} — {e['skip']} "
                          f"(retry {SKIP_RETRY_MIN}m){X}"))
    # ---- POSISI AKTIF (gaya script lama: blok warna + % progres Bybit) ----
    act = [e for e in enlist if (e.get("state") or {}).get("in_position")]
    if act:
        L.append(_sep(f"\u25c6 POSISI AKTIF ({len(act)})"))
        for e in act:
            st = e.get("state") or {}
            d = "LONG" if st["side"] == "Buy" else "SHORT"
            cc = G if st["side"] == "Buy" else R
            bgc = BG_G if st["side"] == "Buy" else BG_R
            entry = st.get("entry") or 0.0
            sl = st.get("sl") or 0.0
            tp = st.get("tp") or 0.0
            ppx = float(e.get("px") or 0.0) or entry
            pnl = st.get("pos_pnl")
            pc = G if (pnl or 0) >= 0 else R
            pnl_txt = f"{pnl:+.2f}$" if pnl is not None else "\u2026"
            roi = (pnl or 0) / (st.get("margin_used") or 1.0) * 100.0
            # progres ENTRY -> TP ala Bybit (arah LONG/SHORT diperhitungkan)
            if d == "LONG":
                num, denom = (ppx - entry), (tp - entry)
            else:
                num, denom = (entry - ppx), (entry - tp)
            prog = num / denom if denom > 0 else 0.0
            prog = max(0.0, min(1.0, prog))
            sl_pct = abs(ppx - sl) / (ppx or 1.0) * 100.0
            tp_pct = abs(tp - ppx) / (ppx or 1.0) * 100.0
            badges = ("[BE] " if st.get("be_done") else "") + ("[TRAIL] " if st.get("trail_on") else "")
            _levv = max(st.get("lev") or 1, 1)
            _dist = (st.get("risk0") or 0) / max(entry or 1, 1e-12)
            _lgap = (1.0 / _levv - LEV_MR_PCT) / max(_dist, 1e-9)
            liq_tag = "SL\u2713" if _lgap >= 1.1 else "SL\u26a0"
            mr = st.get("mfe_r") or 0.0
            l1 = (f"{cc}\u25cf{X} {cc}{d:<6}{X}{B}{e.get('sym', '?')}{X} @ {entry:.6g} "
                  f"{D}\u2192 SL {sl:.6g} \u00b7 TP {tp:.6g}{X} {D}|{X} px {ppx:.6g}")
            l2 = (f"    PnL {pc}{pnl_txt}{X} \u00b7 Rp {fmt_rp((pnl or 0) * idr)} \u00b7 "
                  f"ROI {pc}{roi:+.0f}%{X} {D}|{X} SL {sl_pct:.2f}% \u00b7 TP {tp_pct:.2f}% "
                  f"{D}|{X} {cc}{liq_tag}{X} {badges}{D}MFE {mr:.2f}R{X}")
            L.append(_rowbg(l1, bgc))
            L.append(_row(l2))
            L.append(_row(f"     {_bar(prog * 100.0, 16, pc, anim=tick)} "
                          f"{pc}{prog * 100.0:3.0f}% menuju TP{X} "
                          f"{D}(entry \u2192 TP Bybit){X}"))
            if st.get("tp1_done"):
                L.append(_row(f"     {G}\u25c6 RIDE{X} TP1 {st.get('tp1') or 0:.6g} \u2713 \u00b7 "
                              f"trailing {TRAIL_ATR_MULT}\u00d7ATR {D}\u2192 TP2 {st.get('tp2') or 0:.6g}{X}"))
    # ---- PERFORMANCE ----
    tot_n = sum(v["n"] for v in STATS.values()) if STATS else 0
    tot_w = sum(v["w"] for v in STATS.values()) if STATS else 0
    tot_p = sum(v["pnl"] for v in STATS.values()) if STATS else 0.0
    if tot_n or DAY.get("n"):
        L.append(_sep("\u2605 PERFORMANCE"))
        if DAY.get("date") == wib_now().strftime("%Y-%m-%d") and DAY.get("n"):
            dc = G if DAY["pnl"] >= 0 else R
            L.append(_row(f"\u25c6 HARI INI: {DAY['n']} trade \u00b7 "
                          f"W{DAY['w']}/L{DAY['n'] - DAY['w']} \u00b7 {dc}{DAY['pnl']:+.2f}${X} "
                          f"{D}\u00b7 Rp {fmt_rp(DAY['pnl'] * idr)}{X}"))
        if tot_n:
            tc = G if tot_p >= 0 else R
            L.append(_row(f"TOTAL: {tot_n} trade \u00b7 WR {tot_w / tot_n * 100:.0f}% \u00b7 "
                          f"{tc}{tot_p:+.2f}${X} {D}\u00b7 Rp {fmt_rp(tot_p * idr)}{X} "
                          f"{_bar(tot_w / tot_n, 14, tc, anim=tick)}"))
            for k in sorted(STATS, key=lambda x: -abs(STATS[x]["pnl"]))[:4]:
                v = STATS[k]
                wr = v["w"] / v["n"] * 100 if v["n"] else 0
                pc = G if v["pnl"] >= 0 else R
                L.append(_row(f"  {D}{k:<22}{X} n={v['n']:<3} WR {wr:3.0f}% "
                              f"{pc}{v['pnl']:+7.2f}${X} {_bar(wr / 100, 12, pc, anim=tick)}"))
    # ---- SESI + LOG ----
    sh = wib_now().hour
    sn, sc = gold_session(sh)
    L.append(_row(f"{D}scan {SCAN_CHUNK} simbol/siklus (round-robin) \u00b7 total "
                  f"{len(SYMBOLS)} \u00b7 mode {MODE_LABEL.get(MODE, '?')}{X}"))
    L.append(_sep(f"\u25c6 SESI EMAS: {sc}{sn}{X}"))
    L.append(_sep("\u2261 LIVE LOG"))
    if _logbuf:
        for ln in _logbuf[-8:]:
            L.append(_row(ln))
    else:
        L.append(_row(f"{D}menunggu aktivitas\u2026{X}"))
    L.append(_row(f"{D}Ctrl+C utk berhenti \u00b7 log: {LOG_FILE}{X}"))
    L.append(f"{C}\u255a{'\u2550' * (WIDTH - 2)}\u255d{X}")
    frame = "\n".join(ln + "\033[K" for ln in L)
    if sys.stdout.isatty():
        sys.stdout.write("\033[?25l\033[H" + frame + "\033[J")
    else:
        sys.stdout.write("\n" + "\n".join(_strip(ln) for ln in L) + "\n")
    sys.stdout.flush()


def fmt_px(v):
    s = f"{v:.10f}".rstrip("0").rstrip(".")
    return s if s else "0"

def get_lot_filter(sym):
    if sym in _lot_cache:
        return _lot_cache[sym]
    try:
        r = session.get_instruments_info(category="linear", symbol=sym)
        info = r["result"]["list"][0]
        f = info["lotSizeFilter"]
        _lot_cache[sym] = (float(f["minOrderQty"]), float(f["qtyStep"]))
        lf = info.get("leverageFilter", {})
        _lev_cache[sym] = (float(lf.get("minLeverage", 1) or 1),
                           float(lf.get("maxLeverage", 100) or 100))
    except Exception as e:
        log.error(f"lot filter {sym}: {e}")
        _lot_cache[sym] = (0.001, 0.001)
    return _lot_cache[sym]

def get_lev_limits(sym):
    if sym not in _lev_cache:
        get_lot_filter(sym)
    return _lev_cache.get(sym, (1.0, 100.0))

def get_kline(sym, interval, limit=KF_BARS):
    try:
        r = session.get_kline(category="linear", symbol=sym,
                              interval=interval, limit=limit)
        rows = r["result"]["list"]
        rows.reverse()
        df = pd.DataFrame(rows, columns=["ts", "open", "high", "low",
                                         "close", "volume", "turnover"])
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = pd.to_numeric(df[c])
        df["ts"] = pd.to_numeric(df["ts"])
        return df
    except Exception as e:
        log.error(f"kline {sym}/{interval}: {e}")
        return pd.DataFrame()

def get_price(sym):
    try:
        c = _px_cache.get(sym)
        if c and time.time() - c[1] < 2.0:
            return c[0]
        r = session.get_tickers(category="linear", symbol=sym)
        px = float(r["result"]["list"][0]["lastPrice"])
        _px_cache[sym] = (px, time.time())
        return px
    except Exception:
        return 0.0

def get_position(sym):
    try:
        p = session.get_positions(category="linear", symbol=sym)["result"]["list"][0]
        size = float(p.get("size") or 0)
        if size <= 0:
            return None
        return {"side": p["side"], "size": size,
                "entry": float(p.get("avgPrice") or 0),
                "sl": float(p.get("stopLoss") or 0),
                "tp": float(p.get("takeProfit") or 0),
                "lev": float(p.get("leverage") or 1),
                "pnl": float(p.get("unrealisedPnl") or 0)}
    except Exception:
        return None

def get_balance():
    try:
        r = session.get_wallet_balance(accountType="UNIFIED")
        return float(r["result"]["list"][0]["totalEquity"])
    except Exception:
        return 0.0

def get_available():
    try:
        r = session.get_wallet_balance(accountType="UNIFIED")
        row = r["result"]["list"][0]
        v = row.get("totalAvailableBalance") or ""
        if v not in ("", None):
            return float(v)
        for c in row.get("coin", []):
            if c.get("coin") == "USDT":
                w = c.get("availableToWithdraw") or c.get("walletBalance") or 0
                return float(w or 0)
    except Exception:
        pass
    return None

def send_tg(msg):
    if "GANTI" in TELEGRAM_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": TELEGRAM_CHAT, "text": msg,
                                     "parse_mode": "Markdown"}, timeout=5)
        if not r.ok:
            # Markdown v1 rawan gagal parse (* _ ` [ ] dll) — kirim ulang polos
            requests.post(url, json={"chat_id": TELEGRAM_CHAT, "text": msg}, timeout=5)
    except Exception:
        pass

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path) as f:
                d = json.load(f)
            if isinstance(d, type(default)):
                return d
        except Exception:
            pass
    return default

def save_json(path, data):
    try:
        tmp = path + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f, indent=1)
        os.replace(tmp, path)          # atomic: file tak pernah korup saat crash
    except Exception:
        pass

# ==================== INDIKATOR MTF (MODULE 1) ====================
def _wild(a, n):
    """Wilder RMA seed SMA (identik Pine ta.rma): rata-rata n bar pertama sbg
    seed, lalu rekursi alpha = 1/n. ewm(adjust=False) hanya beda SEED (delta
    < 1e-12 di bar ke-500), tapi ini membuat RSI persis seperti Pine."""
    out = [float("nan")] * len(a)
    if len(a) < n:
        return out
    out[n - 1] = sum(a[:n]) / n
    for i in range(n, len(a)):
        out[i] = (out[i - 1] * (n - 1) + a[i]) / n
    return out

def _atr_list(h, l, c, n):
    tr = [h[0] - l[0]]
    for i in range(1, len(c)):
        tr.append(max(h[i] - l[i], abs(h[i] - c[i - 1]), abs(l[i] - c[i - 1])))
    atr = [float("nan")] * len(c)
    if len(c) > n:
        atr[n] = sum(tr[1:n + 1]) / n
        for i in range(n + 1, len(c)):
            atr[i] = (atr[i - 1] * (n - 1) + tr[i]) / n
    return atr

def compute_tf_confluence(df):
    """MODULE 1 utk satu TF. Return dict (dibaca di index -2 = bar tutup)."""
    n = len(df)
    if n < SR_LOOKBK + VOL_LEN + 5:
        return None
    c = pd.to_numeric(df["close"]).values
    h = pd.to_numeric(df["high"]).values
    l = pd.to_numeric(df["low"]).values
    v = pd.to_numeric(df["volume"]).values
    d = [0.0] + [c[i] - c[i - 1] for i in range(1, n)]
    up = [max(x, 0.0) for x in d]
    dn = [max(-x, 0.0) for x in d]
    ru = _wild(up, RSI_LEN)
    rd = _wild(dn, RSI_LEN)
    rsi = [50.0] * n
    for i in range(n):
        if ru[i] == ru[i] and rd[i] == rd[i]:
            if rd[i] > 0:
                rsi[i] = 100.0 - 100.0 / (1.0 + ru[i] / rd[i])
            elif ru[i] > 0:
                rsi[i] = 100.0
    hi = [float("nan")] * n
    lo = [float("nan")] * n
    for i in range(SR_LOOKBK - 1, n):
        hi[i] = max(h[i - SR_LOOKBK + 1: i + 1])
        lo[i] = min(l[i - SR_LOOKBK + 1: i + 1])
    gzl = [float("nan")] * n
    gzh = [float("nan")] * n
    mid = [float("nan")] * n
    volu = [0.0] * n
    avgv = [float("nan")] * n
    for i in range(n):
        volu[i] = v[i] * c[i]
        if i >= VOL_LEN - 1:
            avgv[i] = sum(volu[i - VOL_LEN + 1: i + 1]) / VOL_LEN
        if hi[i] == hi[i] and lo[i] == lo[i]:
            rng = hi[i] - lo[i]
            gzl[i] = lo[i] + rng * 0.618
            gzh[i] = lo[i] + rng * 0.786
            mid[i] = (hi[i] + lo[i]) / 2.0
    bull = [0] * n
    bear = [0] * n
    sig = [0] * n
    for i in range(n):
        if gzl[i] != gzl[i]:
            continue
        b = (1 if rsi[i] > 50 else 0) + (1 if c[i] >= gzl[i] else 0) + \
            (1 if c[i] > mid[i] else 0) + (1 if (avgv[i] == avgv[i] and volu[i] > avgv[i]) else 0)
        s_ = (1 if rsi[i] < 50 else 0) + (1 if c[i] < gzl[i] else 0) + \
             (1 if c[i] < mid[i] else 0) + (1 if (avgv[i] == avgv[i] and volu[i] > avgv[i]) else 0)
        bull[i], bear[i] = b, s_
        sig[i] = 1 if b >= MIN_COND else (-1 if s_ >= MIN_COND else 0)
    return {"rsi": rsi, "hi": hi, "lo": lo, "gzl": gzl, "gzh": gzh,
            "mid": mid, "volu": volu, "avgv": avgv, "bull": bull,
            "bear": bear, "sig": sig, "close": c, "ts": df["ts"].values}

# ==================== MODULE 2: ZONA LIKUIDITAS ====================
class Zone:
    """Port struct 'magnet' Pine: zona likuiditas dengan siklus & skor."""
    __slots__ = ("kind", "dir", "top", "bot", "top0", "bot0", "born",
                 "born_ts", "last", "tests", "vol_abs", "vol_dir", "conf",
                 "phase", "score", "pen", "inside")
    def __init__(self, kind, dir_, top, bot, born, vabs, vdir, born_ts=None):
        self.kind = kind            # 0 = IMBALANCE, 1 = STOP POOL
        self.dir = dir_             # +1 = supply di atas, -1 = demand di bawah
        self.top = self.top0 = top
        self.bot = self.bot0 = bot
        self.born = born
        self.born_ts = int(born_ts) if born_ts is not None else None
        self.last = born
        self.tests = 0
        self.vol_abs = vabs
        self.vol_dir = vdir
        self.conf = 1
        self.phase = 0              # 0 aktif, 1 consumed, 2 filled/swept
        self.score = 0.0
        self.pen = 0.0
        self.inside = False
    def to_dict(self):
        return {"kind": self.kind, "dir": self.dir, "top": self.top, "bot": self.bot,
                "top0": self.top0, "bot0": self.bot0, "born": self.born,
                "born_ts": self.born_ts,
                "last": self.last, "tests": self.tests, "vol_abs": self.vol_abs,
                "vol_dir": self.vol_dir, "conf": self.conf, "phase": self.phase,
                "score": self.score, "pen": self.pen, "inside": self.inside}

def restore_zones(zones, old):
    """Sambungkan zona baru (dari build) dgn riwayat siklus sebelumnya.
    Tanpa ini: tests/phase zona RESET ke 0 tiap siklus 20 detik -> faktor TEST
    skor & lifecycle CONSUMED/SWEPT tidak pernah terbentuk (BUG besar).
    Pencocokkan via (kind, dir, born_ts) = IDENTITAS bar historis (stempel waktu),
    tahan pergeseran jendela kline; file state lama di-fallback ke (kind, dir, born)."""
    if not old:
        return zones
    by = {}
    for oz in old:
        k = (oz.get("kind"), oz.get("dir"), oz.get("born_ts"))
        if k[2] is None:
            k = (oz.get("kind"), oz.get("dir"), oz.get("born"))   # file lama
        by[k] = oz
    for z in zones:
        if z.born_ts is not None:
            oz = by.get((z.kind, z.dir, z.born_ts))   # identitas waktu (anti-geser bar)
        else:
            oz = by.get((z.kind, z.dir, z.born))      # hanya utk zona lama yg sama2 tanpa ts
        if oz:
            z.tests = max(z.tests, oz.get("tests", 0))
            z.phase = max(z.phase, oz.get("phase", 0))
            z.inside = oz.get("inside", z.inside)
            z.pen = max(z.pen, oz.get("pen", 0.0))
            z.last = max(z.last, oz.get("last", 0))
            z.conf = max(z.conf, oz.get("conf", 1))
    return zones

def zone_sample_at(df, i):
    """Nilai ATR & baseline volume pada bar i (utk deteksi & skor)."""
    c = df["close"].values[:i + 1]
    h = df["high"].values[:i + 1]
    l = df["low"].values[:i + 1]
    v = df["volume"].values[:i + 1]
    n = len(c)
    atr = _atr_list(h, l, c, min(ZONE_ATR_LEN, max(14, n - 1)))
    a = atr[-1]
    if a != a or a <= 0:
        a = (h[-1] - l[-1]) or 0.0
    vb = sum(v[-VOL_BASE_LEN:]) / min(VOL_BASE_LEN, n) if n else 0.0
    return a, vb

def build_zones(df):
    """Deteksi + merge zona (IMBALANCE & STOP-POOL) dari bar TUTUP.
    Baris terakhir df dianggap bar berjalan -> keputusan di index -2."""
    n = len(df)
    c = df["close"].values
    h = df["high"].values
    l = df["low"].values
    v = df["volume"].values
    o = df["open"].values
    zones = []
    warm = max(LEFT_BARS + RIGHT_BARS + 2, 30)
    if n < warm + 20:
        return zones
    last_closed = n - 2

    def _merge(z):
        # PINE 1:1: overlap dihitung dari top0/bot0 (batas ORISINAL, bukan batas
        # aktif yg menyusut); top/bot aktif diperluas terpisah + vol/conf/lastBar.
        if MERGE_ON:
            for e in zones:
                if e.phase == 2 or e.dir != z.dir:
                    continue
                ov = min(e.top0, z.top0) - max(e.bot0, z.bot0)
                minh = min(e.top0 - e.bot0, z.top0 - z.bot0)
                if minh > 0 and ov / minh >= MERGE_PCT / 100.0:
                    e.top0 = max(e.top0, z.top0)
                    e.bot0 = min(e.bot0, z.bot0)
                    e.top = max(e.top, z.top)
                    e.bot = min(e.bot, z.bot)
                    e.vol_abs += z.vol_abs
                    e.vol_dir += z.vol_dir
                    e.conf += 1
                    e.last = z.born
                    return True
        return False

    def _dv(k):
        """dvol Pine: volume*(close-open)/range, 0 bila doji (rng<=0)."""
        r = h[k] - l[k]
        return v[k] * (c[k] - o[k]) / r if r > 0 else 0.0

    def _legsum(nbar):
        """legVolAbs/legVolDir Pine: sum(volume, legLen) & sum(dvol, legLen)
        dihitung pada bar DETEKSI (nbar = born + RIGHT_BARS, saat pivot
        terkonfirmasi), bukan pada bar pivot -> jendela v[nbar-15 .. nbar]."""
        j0 = max(0, nbar - (LEFT_BARS + RIGHT_BARS) + 1)
        return (sum(v[j0:nbar + 1]), sum(_dv(jj) for jj in range(j0, nbar + 1)))

    i = warm
    while i <= last_closed:
        a, _vb = zone_sample_at(df, i)
        if USE_GAPS and a > 0 and i < last_closed:
            # IMBALANCE: celah tak seimbang (bidang gap).
            # PINE 1:1: deteksi di bar n=born+1 -> volAbs = sum(volume,2) di bar n
            # = v[born] + v[born+1]; dvol pun jendela sama (born..born+1).
            gap = l[i] - h[i - 1]
            if gap > 0 and gap >= MIN_GAP_PCT * c[i] and gap >= MIN_GAP_ATR * a:
                # gap naik -> demand tertinggal di bawah (dir -1)
                top, bot = l[i], h[i - 1]
                if not _merge(Zone(0, -1, top, bot, i, v[i] + v[i + 1],
                                   _dv(i) + _dv(i + 1))):
                    zones.append(Zone(0, -1, top, bot, i, v[i] + v[i + 1],
                                      _dv(i) + _dv(i + 1),
                                      int(df["ts"].values[i])))
            gap2 = l[i - 1] - h[i]
            if gap2 > 0 and gap2 >= MIN_GAP_PCT * c[i] and gap2 >= MIN_GAP_ATR * a:
                # gap turun -> supply tertinggal di atas (dir +1)
                top, bot = l[i - 1], h[i]
                if not _merge(Zone(0, 1, top, bot, i, v[i] + v[i + 1],
                                   _dv(i) + _dv(i + 1))):
                    zones.append(Zone(0, 1, top, bot, i, v[i] + v[i + 1],
                                      _dv(i) + _dv(i + 1),
                                      int(df["ts"].values[i])))
        if USE_POOLS and a > 0:
            # STOP-POOL: pivot swing (kiri/kanan) -> rak likuiditas.
            # Pine: base = pivot +- poolBuf*ATR; lalu top/bot = base (+-) poolH*ATR
            # (JADI sisi jauh = pivot +- (poolBuf+poolH)*ATR — bukan hanya poolH).
            # Volume = sum(volume, legLen=16) + sum(dvol,16) (legVolAbs/legVolDir).
            j = i - RIGHT_BARS          # kandidat pivot terkonfirmasi di bar i
            if j - LEFT_BARS >= 1 and j >= LEFT_BARS and j + RIGHT_BARS <= last_closed:
                is_hi = all(h[j] > h[k] for k in range(j - LEFT_BARS, j + RIGHT_BARS + 1) if k != j)
                is_lo = all(l[j] < l[k] for k in range(j - LEFT_BARS, j + RIGHT_BARS + 1) if k != j)
                if is_hi:
                    top = h[j] + (POOL_H + POOL_BUF) * a
                    bot = h[j] + POOL_BUF * a
                    if not _merge(Zone(1, 1, top, bot, j, *_legsum(i))):
                        zones.append(Zone(1, 1, top, bot, j, *_legsum(i),
                                          int(df["ts"].values[j])))
                elif is_lo:
                    top = l[j] - POOL_BUF * a
                    bot = l[j] - (POOL_H + POOL_BUF) * a
                    if not _merge(Zone(1, -1, top, bot, j, *_legsum(i))):
                        zones.append(Zone(1, -1, top, bot, j, *_legsum(i),
                                          int(df["ts"].values[j])))
        i += 1
    # f_prune Pine: selama > MAX_ZONES, buang zona phase-2 (resolved) yang
    # ditemukan paling awal; bila tak ada, buang zona TERTUA (index 0).
    while len(zones) > MAX_ZONES:
        vi = next((k for k, z in enumerate(zones) if z.phase == 2), None)
        zones.pop(0 if vi is None else vi)
    return zones

def zone_score(z, i, px, atrv, volbase):
    """f_score Pine: 0-10, bobot VOL/SIZE/TEST/CONF/PROX + decay."""
    hgt = z.top0 - z.bot0
    sizeF = min(hgt / (atrv * SIZE_NORM), 1.0) if atrv > 0 else 0.0
    vbase = volbase * (LEFT_BARS + RIGHT_BARS)
    volF = min(abs(z.vol_abs) / (vbase * VOL_NORM), 1.0) if vbase > 0 else 0.0
    testF = min(z.tests / TEST_NORM, 1.0)
    confF = min((z.conf - 1) / CONF_NORM, 1.0)
    dist = abs((z.top0 + z.bot0) / 2.0 - px)
    proxF = max(1.0 - dist / (atrv * PROX_NORM), 0.0) if atrv > 0 else 0.0
    raw = (volF * W_VOL + sizeF * W_SIZE + testF * W_TEST +
           confF * W_CONF + proxF * W_PROX) / (W_VOL + W_SIZE + W_TEST + W_CONF + W_PROX)
    age = max(i - z.last, 0)
    decay = max(1.0 - (1.0 - DECAY_FLOOR) * min(age / max(DECAY_BARS, 1), 1.0), DECAY_FLOOR) if DECAY_ON else 1.0
    return min(max(raw * 10.0 * decay, 0.0), 10.0)

def update_zones(zones, df, px, atrv, react_thr):
    """Siklus hidup 1:1 dgn PINE (sumber: Google Doc Golden Edge Suite):
    - SENTUHAN dinilai dari high/low bar TUTUP (bukan close live) -> no-repaint;
    - tests += 1 pada SENTUHAN PERTAMA (bukan saat harga keluar zona) -> T-02;
    - zona MENYUSUT saat penetrasi parsial (bot/top bergeser, persis Pine);
    - phase 2 bila menembus sisi jauh; lastBar di-update saat disentuh (decay reset);
    - retire bila deviasi harga dari MID > staleDev% (Pine math.abs)."""
    h = df["high"].values
    l = df["low"].values
    c = df["close"].values
    n = len(c)
    i = n - 2                        # bar tutup terakhir (keputusan no-repaint)
    # react_thr kini tak dipakai (reaksi = statistik pends di Pine, bukan tests)
    for z in zones:
        if z.phase == 2:
            continue
        hgt = z.top0 - z.bot0
        # ---- touching (Pine: supply high >= bot0 / demand low <= top0) ----
        if z.dir > 0:
            touching = h[i] >= z.bot0
        else:
            touching = l[i] <= z.top0
        if touching:
            p = 1.0
            if hgt > 0:
                p = (min((h[i] - z.bot0) / hgt, 1.0) if z.dir > 0
                     else min((z.top0 - l[i]) / hgt, 1.0))
            if p > z.pen:
                z.pen = p
                if z.dir > 0:                     # zona menyusut (Pine)
                    z.bot = min(z.bot0 + p * hgt, z.top0)
                else:
                    z.top = max(z.top0 - p * hgt, z.bot0)
            if not z.inside:
                z.tests += 1                      # T-02: sentuh PERTAMA = 1 test
            z.inside = True
            z.last = i                            # reset decay (Pine lastBar)
            z.phase = 2 if ((h[i] >= z.top0) if z.dir > 0 else (l[i] <= z.bot0)) else 1
        else:
            z.inside = False
        # ---- retire (Pine: |close - mid|/mid*100 > staleDev) ----
        if STALE_DEV >= 0 and z.phase != 2:
            mid = (z.top0 + z.bot0) / 2.0
            if mid > 0 and abs(px - mid) / mid * 100.0 > STALE_DEV:
                z.phase = 2
    return zones

# ==================== STRATEGY 3-ATURAN (video) ====================
def find_setup(con, trg, zones15, px, atrv15, volbase15, prev_sig15):
    """R1: 1H & 4H setuju. R2: zona STRONG (>=6.5). R3: 15M flip searah di zona.
    Return dict setup atau None."""
    for d in (1, -1):                 # cek LONG dulu, lalu SHORT
        sig_h1 = con["60"]["sig"][-2]
        sig_h4 = con["240"]["sig"][-2]
        sig15 = con["15"]["sig"][-2]
        if sig_h1 != d or sig_h4 != d:
            continue
        if sig15 != d or prev_sig15 == d:
            continue                  # 15M belum FLIP ke arah d (atau sudah lama)
        # ---- R2: zona terdekat searah dgn skor >= 6.5 ----
        cands = [z for z in zones15
                 if z.dir == -d and z.phase != 2
                 and zone_score(z, len(trg["close"]) - 2, px, atrv15, volbase15) >= ZONE_MIN_SCORE]
        if not cands:
            continue
        if d == 1:
            near = max(cands, key=lambda z: (z.top0 + z.bot0) / 2.0)   # demand terdekat DI BAWAH
            if (near.top0 + near.bot0) / 2.0 > px:
                continue
        else:
            near = min(cands, key=lambda z: (z.top0 + z.bot0) / 2.0)   # supply terdekat DI ATAS
            if (near.top0 + near.bot0) / 2.0 < px:
                continue
        # harga HARUS di zona (atau sangat dekat: +- APPROACH_ATR x ATR)
        ap = APPROACH_ATR * atrv15
        if not (near.bot - ap <= px <= near.top + ap):
            continue
        # ---- SL di luar zona; TP = zona lawan terdekat (video) ----
        if d == 1:
            ssl = near.bot - SL_BUFFER_ATR * atrv15          # di bawah demand
            opp = [z for z in zones15 if z.dir == 1 and z.phase != 2 and z.top0 > px]
            tp = min((z.bot for z in opp), default=None) if opp else None
        else:
            ssl = near.top + SL_BUFFER_ATR * atrv15          # di atas supply
            opp = [z for z in zones15 if z.dir == -1 and z.phase != 2 and z.bot0 < px]
            tp = max((z.top for z in opp), default=None) if opp else None
        if tp is None:
            tp = px + d * FALLBACK_TP_ATR * atrv15
        rr = abs(tp - px) / abs(px - ssl) if abs(px - ssl) > 0 else 0.0
        if rr < MIN_RR:
            continue
        # ---- TP2 utk RIDE: zona lawan KE-2; cadangan: TP1 + 1x jarak TP1 ----
        tp2 = None
        if d == 1:
            opp2 = [z for z in zones15 if z.dir == 1 and z.phase != 2 and z.bot > tp + 1e-12]
            tp2 = min((z.bot for z in opp2), default=None) if opp2 else None
        else:
            opp2 = [z for z in zones15 if z.dir == -1 and z.phase != 2 and z.top < tp - 1e-12]
            tp2 = max((z.top for z in opp2), default=None) if opp2 else None
        if tp2 is None:
            tp2 = tp + d * TP_EXT_MULT * abs(tp - px)
        if abs(tp2 - px) < abs(tp - px) + 1e-12:
            tp2 = None
        if tp2 is not None:
            rr2 = abs(tp2 - px) / abs(px - ssl) if abs(px - ssl) > 0 else 0.0
            if rr2 < TP2_MIN_RR:
                tp2 = None
        return {"dir": d, "zone": near, "sl": ssl, "tp": tp, "tp1": tp, "tp2": tp2, "rr": rr,
                "sig15": sig15, "sig_h1": sig_h1, "sig_h4": sig_h4,
                "conf15": con["15"]["bull"][-2] if d == 1 else con["15"]["bear"][-2],
                "zone_score": zone_score(near, len(trg["close"]) - 2, px, atrv15, volbase15)}
    return None

# ==================== EKSEKUSI & MANAJEMEN ====================
ENTRY_MARGIN_DEFAULT = 1.0            # margin cadangan bila lev*SL% = 0

def new_state():
    return {"in_position": False, "side": None, "entry": 0.0, "sl": 0.0,
            "tp": 0.0, "margin_used": 0.0, "lev": 1, "risk0": 0.0,
            "be_done": False, "trail_on": False, "riding": False,
            "peak": 0.0, "mfe_r": 0.0, "last_exit": 0.0,
            "last_pnl": None, "pos_miss": 0, "kind": None,
            "zone_hi": 0.0, "zone_lo": 0.0, "last_bar": 0,
            "prev_sig15": 0, "last_sig15_bar": -10 ** 9,
            "skip_t": 0.0, "skip_reason": "",
            "zones": [],           # riwayat zona (tests/fase) antar siklus
            "qty0": 0.0, "tp1": 0.0, "tp2": 0.0,
            "tp1_done": False, "tp2_done": False,
            "realized": 0.0, "scale_mode": False}

STATES = {}
STATS = load_json(STATS_FILE, {})
if not isinstance(STATS, dict):
    STATS = {}
MFE_LOG = load_json(MFE_FILE, [])
if not isinstance(MFE_LOG, list):
    MFE_LOG = []
DAY = load_json(DAY_FILE, {"date": "", "n": 0, "w": 0, "pnl": 0.0})
if not isinstance(DAY, dict):
    DAY = {"date": "", "n": 0, "w": 0, "pnl": 0.0}

def stats_record(sym, kind, pnl):
    k = f"{sym}|{kind}"
    s = STATS.setdefault(k, {"n": 0, "w": 0, "pnl": 0.0})
    s["n"] += 1
    s["pnl"] = round(s["pnl"] + pnl, 4)
    if pnl > 0:
        s["w"] += 1
    save_json(STATS_FILE, STATS)

def mfe_record(sym, s, pnl):
    try:
        tp_dist = abs(s.get("tp", 0) - s.get("entry", 0))
        risk0 = s.get("risk0") or 0
        peak_r = s.get("mfe_r", 0.0)
        pct = min(100.0, peak_r * risk0 / tp_dist * 100.0) if (tp_dist > 0 and risk0 > 0) else 0.0
        MFE_LOG.append({"t": wib_now().strftime("%Y-%m-%d %H:%M"),
                        "sym": sym, "kind": s.get("kind"), "side": s.get("side"),
                        "pnl": round(pnl, 4), "mfe_r": round(peak_r, 2),
                        "mfe_tp_pct": round(pct, 1)})
        save_json(MFE_FILE, MFE_LOG[-500:])
    except Exception:
        pass

def day_record(pnl):
    today = wib_now().strftime("%Y-%m-%d")
    if DAY["date"] != today:
        DAY.update({"date": today, "n": 0, "w": 0, "pnl": 0.0})
    DAY["n"] += 1
    DAY["pnl"] = round(DAY["pnl"] + pnl, 4)
    if pnl > 0:
        DAY["w"] += 1
    save_json(DAY_FILE, DAY)

def be_price(entry, side):
    buf = entry * (FEE_RT_PCT + 2 * SLIP_PCT) / 100.0
    return entry + buf if side == "Buy" else entry - buf

def smart_leverage(sym, entry, sl):
    """Leverage AMAN: jarak likuidasi = LEV_SL_GAP x jarak SL (+ 1.5% cadangan
    maintenance margin & fee) -> SL SELALU tersentuh duluan, bukan likuidasi."""
    dist = abs(entry - sl) / entry if entry else 0.05
    if dist <= 0:
        dist = 0.05
    lev_aman = 1.0 / (dist * LEV_SL_GAP + LEV_MR_PCT)
    ex_min, ex_max = get_lev_limits(sym)
    hi = min(MAX_LEVERAGE, ex_max)
    lo = max(MIN_LEVERAGE, ex_min)
    return int(min(hi, max(lo, math.floor(lev_aman))))

def close_trade(sym, s, pnl, label):
    stats_record(sym, s.get("kind") or "GE", pnl)
    day_record(pnl)
    mfe_record(sym, s, pnl)
    roi = pnl / s["margin_used"] * 100 if s["margin_used"] else 0
    mark = G if pnl >= 0 else R
    say(f"{mark}■ {sym} {label} ditutup — PnL {pnl:+.2f}$ (ROI {roi:+.1f}%){X}")
    log.info(f"{sym} {label} ditutup — PnL {pnl:+.2f}$ (ROI {roi:+.1f}%)")
    send_tg(f"*GOLDEN EDGE HASIL* {'🟢' if pnl > 0 else '🔴'} #{sym} ({label}) "
            f"\u2192 *{pnl:+.2f}$* (ROI {roi:+.1f}%)")
    s.clear(); s.update(new_state()); s["last_exit"] = time.time()
    save_json(STATE_FILE, STATES)

def manage(sym, s, atrv):
    p = get_position(sym)
    if s["in_position"] and not p:
        s["pos_miss"] += 1
        if s["pos_miss"] < 2:
            return
        px = get_price(sym)
        if not px:
            # API koneksi bermasalah — jangan salah tutup posisi yang masih ada
            log.error(f"{sym} posisi tak terlihat & harga tak dapat — tunggu siklus berikut")
            return
        pnl = s.get("realized", 0.0) + (s.get("last_pnl") or 0.0)
        close_trade(sym, s, pnl, "closed-ex")
        return
    if not p:
        return
    s["pos_miss"] = 0
    s["last_pnl"] = p["pnl"]
    s["pos_pnl"] = p["pnl"]
    px = get_price(sym) or s["entry"]
    # ---- TP1 tercapai (bursa menutup sebagian) -> RIDE: BE + trailing ----
    if not s.get("tp1_done") and s.get("qty0") and p["size"] < s["qty0"] * 0.9999:
        qty_part = s["qty0"] - p["size"]
        d_ = 1 if s["side"] == "Buy" else -1
        tp1 = s.get("tp1") or s["entry"]
        s["realized"] = s.get("realized", 0.0) + d_ * (tp1 - s["entry"]) * qty_part
        s["tp1_done"] = True
        s["qty0"] = p["size"]
        say(f"◆ {sym} TP1 {tp1:.6g} tercapai — {qty_part:.8g} ditutup "
            f"({s['realized']:+.2f}$ terkunci) → RIDE aktif")
        try:
            be = be_price(s["entry"], s["side"])
            session.set_trading_stop(category="linear", symbol=sym,
                                     stopLoss=fmt_px(be), positionIdx=0)
            s["sl"], s["be_done"] = be, True
            if atrv > 0:
                session.set_trading_stop(category="linear", symbol=sym,
                                         trailingStop=fmt_px(atrv * TRAIL_ATR_MULT),
                                         positionIdx=0)
                s["trail_on"] = True
                say(f"» {sym} TRAILING {TRAIL_ATR_MULT}xATR aktif — mengawal sisa "
                    f"{p['size']:.8g} ke TP2 {s.get('tp2') or 0:.6g}")
        except Exception as _e:
            log.error(f"ride {sym}: {_e}")
    if not s["in_position"]:           # adopsi restart
        _sl_b = p["sl"] or 0.0
        _r0 = abs(p["entry"] - _sl_b) if _sl_b else 0.0
        if _r0 <= 0:
            _r0 = (atrv * 1.5) if atrv > 0 else p["entry"] * 0.02
        s.update({"in_position": True, "side": p["side"], "entry": p["entry"],
                  "sl": _sl_b, "tp": p["tp"] or 0.0, "tp1": p["tp"] or 0.0,
                  "qty0": float(p["size"]), "lev": p["lev"] or 1,
                  "kind": s.get("kind") or "GE",
                  "risk0": s.get("risk0") or _r0,
                  "margin_used": s["margin_used"] or
                                 (p["size"] * p["entry"] / max(p["lev"], 1))})
        say(f"{Y}[ADOPT] {sym} diadopsi (restart){X}")
    # guard posisi telanjang
    if not p["sl"] and s["entry"] and atrv > 0 and not s.get("trail_on"):
        try:
            _sl_new = (s["entry"] - atrv * 1.5 if s["side"] == "Buy"
                       else s["entry"] + atrv * 1.5)
            _px = get_price(sym) or px
            if s["side"] == "Buy" and _sl_new >= _px:
                _sl_new = _px - atrv * 1.5
            elif s["side"] == "Sell" and _sl_new <= _px:
                _sl_new = _px + atrv * 1.5
            if (_sl_new < _px) if s["side"] == "Buy" else (_sl_new > _px):
                session.set_trading_stop(category="linear", symbol=sym,
                                         stopLoss=fmt_px(_sl_new), positionIdx=0)
                s["sl"] = _sl_new
                say(f"{R}⚠ {sym} POSISI TANPA SL — dipasang ulang @ {_sl_new:.6g}{X}")
        except Exception as e:
            log.error(f"naked {sym}: {e}")
    risk = s.get("risk0") or (abs(s["entry"] - s["sl"]) if s["sl"] else 0)
    if risk <= 0 or not s["entry"]:
        return
    profit = (px - s["entry"]) if s["side"] == "Buy" else (s["entry"] - px)
    r_now = profit / risk
    if r_now > s.get("mfe_r", 0.0):
        s["mfe_r"] = r_now
    try:
        if not s["be_done"] and r_now >= BE_AT_R:
            be = be_price(s["entry"], s["side"])
            ok = be < px if s["side"] == "Buy" else be > px
            if ok:
                session.set_trading_stop(category="linear", symbol=sym,
                                         stopLoss=fmt_px(be), positionIdx=0)
                s["sl"], s["be_done"] = be, True
                say(f"{G}[BE] {sym} BE @ {be:.6g} ({r_now:.2f}R){X}")
        _trail_ok = (s.get("tp1_done") and s.get("scale_mode")) \
            if TRAIL_AFTER_TP1 else (r_now >= TRAIL_AT_R)
        if not s["trail_on"] and _trail_ok and atrv > 0:
            dist = atrv * TRAIL_ATR_MULT
            session.set_trading_stop(category="linear", symbol=sym,
                                     trailingStop=fmt_px(dist), positionIdx=0)
            s["trail_on"] = True
            say(f"{M}» {sym} trailing @ {r_now:.2f}R{X}")
    except Exception as e:
        log.error(f"manage {sym}: {e}")
    # ---- TP2 tercapai: tutup sisa posisi (RIDE selesai) ----
    if s.get("tp1_done") and s.get("tp2") and not s.get("tp2_done"):
        d_ = 1 if s["side"] == "Buy" else -1
        if (px - s["tp2"]) * d_ >= 0:
            try:
                close_side = "Sell" if s["side"] == "Buy" else "Buy"
                session.place_order(category="linear", symbol=sym, side=close_side,
                                    orderType="Market", qty=fmt_px(p["size"]),
                                    reduceOnly=True, positionIdx=0)
                s["tp2_done"] = True
                say(f"◆ {sym} TP2 {s['tp2']:.6g} tercapai — sisa ditutup (RIDE selesai)")
                send_tg(f"*GOLDEN EDGE RIDE* ✅ #{sym} TP1 \u2192 TP2 {s['tp2']:.6g} "
                        f"(momentum lanjut, sisa ditutup)")
            except Exception as _e:
                log.error(f"tp2 close {sym}: {_e}")
    save_json(STATE_FILE, STATES)

def try_entry(sym, s, setup, balance, n_open, atrv):
    if s["in_position"]:
        return
    if time.time() - s.get("last_exit", 0) < COOLDOWN_MIN * 60:
        return
    if n_open >= MAX_POSITIONS:
        say(f"{Y}⊘ {sym} slot penuh {n_open}/{MAX_POSITIONS}{X}")
        return
    px = get_price(sym)
    if not px:
        return
    side = "Buy" if setup["dir"] == 1 else "Sell"
    sl, tp = setup["sl"], setup["tp"]
    if (side == "Buy" and (sl >= px or tp <= px)) or \
       (side == "Sell" and (sl <= px or tp >= px)):
        return
    # ---- GUARD: news/CPI/volatilitas -> entry baru dijeda ----
    bloc, why = entry_blocked()
    if bloc:
        say(f"{R}⚠ {sym} entry ditunda — {why}{X}")
        return
    tp_pct = abs(tp - px) / px * 100
    if tp_pct < (FEE_RT_PCT + 2 * SLIP_PCT) * 2:
        say(f"{Y}⊘ {sym} TP terlalu dekat ({tp_pct:.3f}%) — tak layak biaya{X}")
        return
    cap = min(RISK_CAP_USD, RISK_HARD_USD)
    balance = balance or 1.0
    lev = smart_leverage(sym, px, sl)                       # SL dulu, baru likuidasi
    sl_pct = abs(px - sl) / px * 100
    sl_dist = sl_pct / 100.0
    # target margin = % saldo (mis. $10 -> $2), dibatasi plafon saldo
    margin_target = round(balance * MARGIN_TRADE_PCT / 100.0, 2)
    _mcap = balance * MARGIN_MAX_PCT / 100.0
    margin_target = min(margin_target, _mcap)
    # jika margin target x lev x SL melebihi cap risiko, KECILKAN margin (bukan lev!)
    _mr = cap / (lev * sl_dist) if (lev * sl_dist) > 0 else margin_target
    margin = round(min(margin_target, _mr or 0.0), 2)
    if margin < 0.05:
        say(f"{Y}⊘ {sym} SL {sl_dist*100:.2f}% terlalu lebar utk cap ${cap:.2f} "
            f"— dilewati{X}")
        return
    min_qty, step = get_lot_filter(sym)
    _min_notional = min_qty * px
    if _min_notional > (balance or 0):
        mark_skip(s, f"min order ~${_min_notional:.0f} > saldo ${(balance or 0):.2f} — cap tak cukup")
        say(f"{Y}⊘ {sym} min order ${_min_notional:.2f} > saldo ${(balance or 0):.2f} "
            f"— di-skip (retry {SKIP_RETRY_MIN}m){X}")
        return
    qty = max(min_qty, math.floor((margin * lev / px) / step) * step)
    qty = round(qty, 8)
    real_risk = qty * abs(px - sl)
    if real_risk > cap:
        mark_skip(s, f"min-qty risiko ${real_risk:.2f} > cap ${cap:.2f}")
        say(f"{Y}⊘ {sym} min-qty memaksa risiko ${real_risk:.2f} > cap — "
            f"di-skip (retry {SKIP_RETRY_MIN}m){X}")
        return
    if qty * px < MIN_ORDER_USD:
        mark_skip(s, f"cap ${cap:.2f} tak cukup (order ${qty*px:.2f} < min ${MIN_ORDER_USD:.0f})")
        say(f"{Y}⊘ {sym} nilai order ${qty*px:.2f} < min ${MIN_ORDER_USD:.0f} "
            f"— di-skip (retry {SKIP_RETRY_MIN}m){X}")
        return
    _avail = get_available()
    _need = (qty * px) / lev
    if _avail is not None and _need > _avail * 0.9:
        mark_skip(s, "margin tersedia kurang")
        say(f"{Y}⊘ {sym} margin tersedia kurang — di-skip (retry {SKIP_RETRY_MIN}m){X}")
        return
    try:
        try:
            session.set_leverage(category="linear", symbol=sym,
                                 buyLeverage=str(lev), sellLeverage=str(lev))
        except Exception:
            pass
        session.place_order(category="linear", symbol=sym, side=side,
                            orderType="Market", qty=str(qty),
                            timeInForce="GTC", positionIdx=0)
        time.sleep(1)
        p = get_position(sym)
        if not p:
            log.error(f"✘ {sym} entry tidak terkonfirmasi")
            return
        lev_act = float(p.get("lev") or lev)
        if LEV_GUARD and lev_act > lev:
            # bahaya: likuidasi bisa mendahului SL -> tutup segera (reduceOnly)
            try:
                close_side = "Sell" if side == "Buy" else "Buy"
                session.place_order(category="linear", symbol=sym, side=close_side,
                                    orderType="Market", qty=fmt_px(p["size"]),
                                    reduceOnly=True, positionIdx=0)
            except Exception as _e:
                log.error(f"lev-guard close {sym}: {_e}")
            say(f"{R}⚠ {sym} LEV-GUARD: lev bursa {lev_act:.0f}x > aman {lev}x — "
                f"likuidasi bisa mendahului SL, posisi langsung ditutup{X}")
            send_tg(f"*GOLDEN EDGE LEV-GUARD* 🚨 #{sym} lev aktual {lev_act:.0f}x "
                    f"> aman {lev}x — posisi ditutup (liq sebelum SL)")
            return
        lev = int(lev_act) if lev_act <= lev else lev
        fill = p["entry"] or px
        margin = round((p["size"] * fill) / max(lev, 1), 4) or margin
        # TP1 = zona lawan (video). Bila ada target lanjut: tutup sebagian di TP1
        # (tpslMode Partial di bursa), sisa posisi di-RIDE dgn trailing setelahnya.
        scale = False
        qty_fill = float(p.get("size") or qty)
        if setup.get("tp2"):
            tp_size = math.floor(qty_fill * TP1_SCALE_PCT / 100.0 / step) * step
            tp_size = round(tp_size, 8)
            if 0 < tp_size < qty_fill - step * 0.5:
                try:
                    session.set_trading_stop(category="linear", symbol=sym,
                                             stopLoss=fmt_px(sl), takeProfit=fmt_px(tp),
                                             tpslMode="Partial", tpSize=fmt_px(tp_size),
                                             slTriggerBy="LastPrice", tpTriggerBy="LastPrice",
                                             positionIdx=0)
                    scale = True
                except Exception as _e:
                    log.error(f"partial tp {sym}: {_e}")
        if not scale:
            session.set_trading_stop(category="linear", symbol=sym,
                                     stopLoss=fmt_px(sl), takeProfit=fmt_px(tp),
                                     slTriggerBy="LastPrice", tpTriggerBy="LastPrice",
                                     positionIdx=0)
        s["skip_t"], s["skip_reason"] = 0.0, ""
        s.update({"in_position": True, "side": side, "entry": fill, "sl": sl,
                  "tp": tp, "kind": "GE", "margin_used": margin, "lev": lev,
                  "risk0": abs(fill - sl), "zone_hi": setup["zone"].top,
                  "zone_lo": setup["zone"].bot, "be_done": False,
                  "trail_on": False, "riding": False,
                  "qty0": qty_fill, "tp1": tp, "tp2": setup.get("tp2") or 0.0,
                  "tp1_done": False, "tp2_done": False,
                  "realized": 0.0, "scale_mode": scale})
        save_json(STATE_FILE, STATES)
        arrow = "▲ LONG" if side == "Buy" else "▼ SHORT"
        say(f"{G if side=='Buy' else R}{arrow}{X} {B}{sym}{X} [GE-R3] @ {fill:.6g} "
              f"{lev}x | 15M {setup['conf15']}/4 {Y}{setup['zone_score']:.1f}/10{X} "
              f"RR {setup['rr']:.2f} TP {tp:.6g} SL {sl:.6g}")
        log.info(f"{sym} ENTRY {side} @ {fill:.6g} {lev}x TP {tp:.6g} SL {sl:.6g} "
                 f"zone {setup['zone_score']:.1f}/10 rr {setup['rr']:.2f}")
        send_tg(f"*GOLDEN EDGE SIGNAL* {'🟢 LONG' if side=='Buy' else '🔴 SHORT'} #{sym}\n"
                f"Entry : `{fill:.6g}`\nSL    : `{sl:.6g}`\nTP    : `{tp:.6g}`\n"
                f"Zona  : {setup['zone_score']:.1f}/10 (≥6.5) · RR {setup['rr']:.2f}\n"
                f"15M {setup['conf15']}/4 · 1H/4H searah")
    except Exception as e:
        log.error(f"✘ {sym} gagal entry: {e}")
        s["last_exit"] = time.time()

# ==================== LOOP UTAMA ====================
# ==================== GUARD: NEWS & VOLATILITAS (port bot utama) ====================
_news = {"until": 0.0, "reason": ""}
_btc_watch = {"px": 0.0, "t": 0.0}
_vol = {"until": 0.0, "reason": ""}

def cpi_next_event_days():
    """Hari menuju event CPI WIB terdekat; None bila tidak ada (daftar kedaluwarsa)."""
    now = wib_now()
    best = None
    for (y, mo, d, h, mi) in CPI_EVENTS_WIB:
        try:
            ev = now.replace(year=y, month=mo, day=d, hour=h, minute=mi,
                             second=0, microsecond=0)
        except ValueError:
            continue
        dd = (ev - now).total_seconds() / 86400.0
        if dd >= 0 and (best is None or dd < best):
            best = dd
    return best


def cpi_guard_active():
    """True bila sekarang (WIB) di jendela blok CPI terdekat. Return (aktif, ket)."""
    if not CPI_GUARD_ON:
        return False, ""
    now = wib_now()
    for (y, mo, d, h, mi) in CPI_EVENTS_WIB:
        ev = now.replace(year=y, month=mo, day=d, hour=h, minute=mi,
                         second=0, microsecond=0)
        delta = (now - ev).total_seconds() / 60.0
        if -CPI_PRE_MIN <= delta <= CPI_POST_MIN:
            sisa = CPI_POST_MIN - delta
            return True, (f"CPI AS {d}/{mo} {h:02d}:{mi:02d} WIB — "
                          f"jendela blok sisa {max(0, sisa):.0f}m")
    return False, ""

def news_shock_check():
    """Pantau BTC antar-cek. Shock HANYA bila:
    1. sudah lewat NEWS_MIN_WINDOW detik (hindari tick kecil memicu),
    2. lonjakan ABSOLUT >= NEWS_MIN_JUMP % (wiggle mikron diabaikan),
    3. kecepatan >= NEWS_BTC_FAST %/menit (0.20, tidak 0.08).
    Jeda TIDAK diperpanjang oleh shock beruntun (NEWS_EXTEND=False) -> tidak
    bikin bot diam berjam-jam hanya karena BTC sedang bergerak.""" 
    if not NEWS_GUARD:
        return
    try:
        px = get_price("BTCUSDT")
        now = time.time()
        if px and _btc_watch["px"]:
            dt = now - _btc_watch["t"]
            if dt >= NEWS_MIN_WINDOW:
                jump = (px - _btc_watch["px"]) / _btc_watch["px"] * 100.0
                if abs(jump) >= NEWS_MIN_JUMP:
                    rate = jump / (dt / 60.0)
                    if abs(rate) >= NEWS_BTC_FAST and (NEWS_EXTEND or now >= _news["until"]):
                        _news["until"] = now + NEWS_PAUSE_MIN * 60
                        _news["reason"] = f"BTC {rate:+.2f}%/mnt ({jump:+.2f}%)"
                        say(f"{R}⚠ NEWS SHOCK! {_news['reason']} — entry dijeda "
                            f"{NEWS_PAUSE_MIN}m (posisi aktif tetap dikelola){X}")
                _btc_watch.update({"px": px, "t": now})
        elif px:
            _btc_watch.update({"px": px, "t": now})
    except Exception as e:
        log.error(f"news_shock: {e}")

def vol_guard_check(sym, df15, px15, atrv15):
    """Bar 15m > VOL_SPIKE_ATR x ATR atau loncat > VOL_MOVE_PCT -> jeda entry 10m."""
    if not VOL_GUARD or atrv15 <= 0:
        return
    try:
        b = len(df15) - 1
        rng = float(df15["high"].iloc[b] - df15["low"].iloc[b])
        close = float(df15["close"].iloc[b])
        prev = float(df15["close"].iloc[b - 1]) if b >= 1 else close
        spike = rng / atrv15
        move = abs(close - prev) / (prev or 1) * 100
        if spike >= VOL_SPIKE_ATR or move >= VOL_MOVE_PCT:
            now = time.time()
            if now >= _vol["until"]:
                _vol["reason"] = f"{sym} loncat {move:.2f}% ({spike:.1f}xATR)"
                say(f"{R}⚠ VOLATILITY GUARD — {_vol['reason']} · entry dijeda "
                    f"{VOL_PAUSE_MIN}m (posisi aktif tetap dikelola){X}")
            _vol["until"] = now + VOL_PAUSE_MIN * 60
    except Exception as e:
        log.error(f"vol_guard: {e}")

def entry_blocked():
    """(True, alasan) bila ENTRY BARU harus dijeda; posisi aktif tetap dikelola."""
    if NEWS_GUARD and time.time() < _news["until"]:
        return True, (f"NEWS SHOCK ({_news['reason']}) · sisa "
                      f"{max(0, (_news['until'] - time.time()) / 60):.0f}m")
    if CPI_GUARD_ON:
        act, ket = cpi_guard_active()
        if act:
            return True, ket
    if VOL_GUARD and time.time() < _vol["until"]:
        return True, (f"VOLATILITY ({_vol['reason']}) · sisa "
                      f"{max(0, (_vol['until'] - time.time()) / 60):.0f}m")
    return False, ""

def choose_mode():
    """Menu mode simbol saat start: 1=ALL COIN, 2=TOP30, 3=EMAS SAJA."""
    try:
        if sys.stdin.isatty():
            print(f"\n{B}██ Pilih mode simbol:{X}")
            print(f"   {Y}1{X} = ALL COIN — semua USDT perp likuid otomatis "
                  f"(turnover 24h \u2265 ${ALL_MIN_TURNOVER / 1e6:g}jt)")
            print(f"   {Y}2{X} = TOP {TOP_N_CAP} — {TOP_N_CAP} coin USDT paling likuid "
                  f"(turnover tertinggi)")
            print(f"   {Y}3{X} = EMAS SAJA — XAUUSDT (mode sebelumnya)")
            inp = input(f"   Pilihan [1/2/3] (default {DEFAULT_MODE}): ").strip()
            if inp in ("1", "2", "3"):
                return int(inp)
            return DEFAULT_MODE
        return int(os.environ.get("GE_MODE", str(DEFAULT_MODE)))
    except Exception:
        return DEFAULT_MODE


_uni_cache = {"t": 0.0, "pool": []}

def detect_perp_universe():
    """Semua pair USDT perp linear Bybit, urut turnover 24h (besar->kecil).
    Di-cache 60 detik (panggilan get_tickers penuh per siklus = boros rate limit)."""
    if _uni_cache["pool"] and time.time() - _uni_cache["t"] < 60:
        return _uni_cache["pool"]
    try:
        r = session.get_tickers(category="linear")
        pool = []
        for t in r.get("result", {}).get("list", []):
            sym = t.get("symbol", "")
            if not sym.endswith("USDT"):
                continue
            try:
                tv = float(t.get("turnover24h") or 0)
            except Exception:
                tv = 0.0
            if tv > 0:
                pool.append((tv, sym))
        pool.sort(key=lambda x: -x[0])
        _uni_cache.update({"t": time.time(), "pool": pool})
        return pool
    except Exception as e:
        log.error(f"detect_perp_universe: {e}")
        return []


def track_flip(s, sig15_now):
    """Ikuti sinyal 15M bar tutup. Netral mereset -> re-flip netral->d tetap dihitung R3."""
    s["prev_sig15"] = int(sig15_now)


def mark_skip(s, reason):
    s["skip_t"] = time.time()
    s["skip_reason"] = reason


def refresh_symbols(mode=None):
    global SYMBOLS, MODE
    if mode is not None:
        MODE = mode
    if MODE == 3:
        SYMBOLS = list(FOCUS_SYMBOLS)
        log.info(f"mode EMAS SAJA: {len(SYMBOLS)} simbol")
        return
    pool = detect_perp_universe()
    if MODE == 1:
        add = [s for tv, s in pool if tv >= ALL_MIN_TURNOVER]
    else:
        add = [s for _, s in pool[:TOP_N_CAP]]
    if not add:
        add = [s for _, s in pool[:TOP_N_CAP]]
    SYMBOLS = list(dict.fromkeys(FOCUS_SYMBOLS + add))
    log.info(f"mode {MODE_LABEL.get(MODE, MODE)}: {len(SYMBOLS)} simbol "
             f"({len(add)} coin terdeteksi, emas selalu diikutkan)")

def main():
    global SYMBOLS, MODE
    MODE = choose_mode()
    SYMBOLS = list(FOCUS_SYMBOLS)
    refresh_symbols(MODE)
    for sym in SYMBOLS:
        base = new_state()
        base.update({k: v for k, v in load_json(STATE_FILE, {}).get(sym, {}).items() if k in base})
        STATES[sym] = base
    bal = get_balance()
    log.info(f"▶ GOLDEN EDGE BOT dimulai — saldo ${bal:,.2f} | {len(SYMBOLS)} simbol | "
             f"TF {TF_TRIGGER}/{TF_HTF1}/{TF_HTF2}m | zona min {ZONE_MIN_SCORE}/10 | "
             f"cap ${RISK_CAP_USD:.2f}")
    bn = startup_banner(bal, MODE)
    if sys.stdout.isatty():
        print("\n".join(bn))
    else:
        print("\n".join(_strip(x) for x in bn))
    add_log(f"GOLDEN EDGE BOT dimulai — saldo ${bal:,.2f} | {len(SYMBOLS)} simbol | "
            f"TF {TF_TRIGGER}/{TF_HTF1}/{TF_HTF2}m | zona ≥ {ZONE_MIN_SCORE} | cap ${RISK_CAP_USD:.2f}")
    _nx = cpi_next_event_days()
    if _nx is None or _nx > 120:
        log.warning("CPI_EVENTS_WIB kedaluwarsa — perbarui dari jadwal BLS "
                    "(bls.gov/schedule/news_release/cpi.htm)")
        add_log(f"{Y}⚠ daftar CPI_EVENTS_WIB tidak punya event mendatang "
                f"(>120 hari) — perbarui sesuai jadwal BLS{X}")
    _tick = 0
    _scan_i = 0
    while True:
        try:
            refresh_symbols(MODE)
            news_shock_check()
            bal = get_balance()
            dsyms = []
            hero_sym = "BTCUSDT" if MODE != 3 else "XAUUSDT"
            # posisi terbuka (semua STATE, termasuk koin yang keluar universe)
            # + hero selalu diprioritaskan tiap siklus; sisanya round-robin
            pos_syms = [x for x in STATES if STATES[x].get("in_position")]
            rest = [x for x in SYMBOLS
                    if not STATES.get(x, {}).get("in_position") and x != hero_sym]
            scan = list(pos_syms)
            if hero_sym not in scan:
                scan.append(hero_sym)
            if rest:
                take = max(0, SCAN_CHUNK - len(scan))
                scan += [rest[(_scan_i + j) % len(rest)] for j in range(take)]
                _scan_i = (_scan_i + take) % len(rest)
            for sym in scan:
                s = STATES.setdefault(sym, new_state())
                # ---- skip cap: modal belum cukup, retry berkala ----
                if (not s["in_position"] and s.get("skip_t")
                        and time.time() - s["skip_t"] < SKIP_RETRY_MIN * 60):
                    dsyms.append({"sym": sym, "skip": s.get("skip_reason", "cap")})
                    continue
                # ----- MTF confluence (tiap TF, bar tutup) -----
                df15 = get_kline(sym, TF_TRIGGER)
                df60 = get_kline(sym, TF_HTF1)
                df240 = get_kline(sym, TF_HTF2)
                if min(len(x) for x in (df15, df60, df240)) < 60:
                    continue
                con = {}
                for key, dfs in (("15", df15), ("60", df60), ("240", df240)):
                    c = compute_tf_confluence(dfs)
                    if c is None:
                        break
                    con[key] = c
                if len(con) != 3:
                    continue
                i15 = len(df15) - 2
                px15 = float(df15["close"].iloc[-1])       # live: tampilan & manage posisi
                px_closed = float(df15["close"].iloc[i15])  # bar TUTUP: keputusan R1-R3
                atrv15, volbase15 = zone_sample_at(df15, len(df15) - 1)
                vol_guard_check(sym, df15, px15, atrv15)
                s["prev_sig15"] = s.get("prev_sig15", 0)
                sig15_now = int(con["15"]["sig"][i15])
                # ----- zona pada 15m (bar tutup) -----
                zones15 = build_zones(df15)
                zones15 = restore_zones(zones15, s.get("zones") or [])
                zones15 = update_zones(zones15, df15, px_closed, atrv15,
                                       REACT_ATR * atrv15)
                s["zones"] = [z.to_dict() for z in zones15]   # resolved tetap ada (Pine keepDone)
                # ----- manajemen posisi -----
                if s["in_position"]:
                    manage(sym, s, atrv15)
                # ----- ATURAN 3-LANGKAH (sekali per bar tutup 15m) -----
                bar_ts = int(df15["ts"].iloc[i15])
                if bar_ts != s.get("last_bar") and not s["in_position"]:
                    s["last_bar"] = bar_ts
                    setup = find_setup(con, df15, zones15, px_closed, atrv15,
                                       volbase15, s.get("prev_sig15", 0))
                    if setup:
                        say(f"◈ {B}{sym}{X} GE-R3 {'LONG' if setup['dir']==1 else 'SHORT'} "
                              f"| 15M {setup['conf15']}/4 · 1H {setup['sig_h1']:+d} · "
                              f"4H {setup['sig_h4']:+d} | zona {'▼D' if setup['dir']==1 else '▲S'} "
                              f"{setup['zone_score']:.1f}/10 @ {setup['zone'].top:.6g}-{setup['zone'].bot:.6g} "
                              f"| RR {setup['rr']:.2f}")
                        log.info(f"{sym} setup GE-R3 "
                                 f"{'LONG' if setup['dir']==1 else 'SHORT'} "
                                 f"zone {setup['zone_score']:.1f}/10 rr {setup['rr']:.2f}")
                        _n_open = sum(1 for st in STATES.values() if st["in_position"])
                        try_entry(sym, s, setup, bal, _n_open, atrv15)
                # simpan flip 15M utk deteksi "baru flip" berikutnya (R3).
                # Netral (0) SEKALIGUS mereset: re-flip dari netral adalah flip sah.
                track_flip(s, sig15_now)
                # data dashboard
                zsc = [(z, zone_score(z, i15, px_closed, atrv15, volbase15))
                       for z in zones15]
                dsyms.append({"sym": sym, "px": px15, "atr": atrv15, "con": con,
                              "zones": zsc, "state": s,
                              "scen": scenario_status(con, zsc, px15, s, i15),
                              "fuel": fuel_gauge(con),
                              "cd": bar_countdown(con["15"])})
                save_json(STATE_FILE, STATES)
                time.sleep(0.5 if len(SYMBOLS) > 5 else 0.3)
            render_dash(bal, {"syms": dsyms, "tick": _tick})
            _tick += 1
            time.sleep(20)
        except KeyboardInterrupt:
            say("\n■ GOLDEN EDGE bot dihentikan.")
            break
        except Exception:
            log.exception("loop fatal:")     # traceback lengkap utk debugging
            time.sleep(10)

if __name__ == "__main__":
    main()
