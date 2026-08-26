# ============================================================================
#  MODERN VWAP BOT [GBB-port] — v1.0 (5 Agu 2026)
#  Port Python dari indikator Pine "Modern VWAP [GBB]"
#  (video: "VWAP Is Outdated — Here's The 2026 Overhaul", 4 Agu 2026)
#
#  ⚠⚠ PERINGATAN JUJUR (dari PEMBUAT indikatornya sendiri) ⚠⚠
#  Backtest 6 tahun (BTC/ETH/SOL perp 1H, ~50.000 bar, in/out-sample,
#  koreksi multiple-testing 72 sel): "The result was ZERO. As a
#  standalone system this will not make you money."
#  Bot ini dibuat atas permintaan & kesadaran penuh user — dijalankan
#  dengan RISK CAP ketat + catatan statistik per-sinyal supaya dalam
#  30-50 trade kita punya vonis sendiri.
#
#  STRATEGI (persis logika Pine):
#   - VWAP anchored (Session UTC / Week / Month / Swing pivot-10 strict)
#     + band ±1/2/3 sigma (volume-weighted), adaptif KER opsional
#   - REGIME: KER(20) & ATR%(14) vs median 200-bar → 4 kuadran
#   - MR  (mean-reversion, HANYA saat RANGING): close keluar band 2σ
#     lalu close kembali ke dalam → entry, target VWAP
#   - TC  (trend-continuation, HANYA saat TRENDING): 8/10 close di satu
#     sisi VWAP, pullback sentuh VWAP, close balik ≤3 bar → entry,
#     target band 2σ searah
#  EKSEKUSI (pagar dari bot utama):
#   - RISK CAP $ (rugi maks/trade), smart-leverage (liq jauh dari SL)
#   - BE di 1R, trailing ATR di 1.5R, TIME GUARD 00-04 WIB
#   - One-Way mode (positionIdx=0), jam WIB, file terpisah dari bot utama
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

# ==================== SCAN MASSAL (8 Agu, permintaan user) ====================
# 3 coin TF 1H = sepi entry (2 trade/14 jam). Kini: daftar simbol DINAMIS
# dari Bybit (semua perpetual linear USDT ber-turnover layak), di-scan
# bergilir. TF 1H ramah rate-limit: indikator hanya perlu dihitung ULANG
# saat bar baru tutup; antar-jam cukup pantau posisi aktif & harga.
# CORE_SYMBOLS selalu diprioritaskan (paling likuid, sesuai backtest).
DYN_SYMBOLS   = True
SYM_MIN_TURN  = 5_000_000    # turnover 24h min $5jt (spread sehat utk 1H)
SYM_MAX_N     = 220          # batas jumlah simbol
SYM_REFRESH_H = 6            # refresh daftar tiap 6 jam
SCAN_BATCH    = 25           # simbol dihitung per siklus (rotasi adil)
CORE_SYMBOLS  = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
SYMBOLS       = list(CORE_SYMBOLS)   # akan diperluas saat start (DYN)
SYM_BLACKLIST = set()   # simbol terlarang sesi ini (mis. 110125 Crude Oil)
INTERVAL      = "60"        # 1H — timeframe yang diuji di video
ENTRY_MARGIN  = 11.0         # margin dasar (USDT) — DOSIS MINI 11 Agu (saldo $5)
# ==================== MODE RISIKO (7 Agu, permintaan user) ====================
# OPSI 1 — KLASIK  : SL = indikator (anti-hunt hanya koreksi bila SL jatuh
#                    di kolam stop) | rugi maks = RISK_CAP_USD dolar TETAP.
# OPSI 2 — STOPHUNT: SL SELALU diparkir di luar zona sweep kolam stop
#                    terdekat (indikator jadi cadangan bila kolam tak ada) |
#                    rugi maks = RISK_PCT_BAL % dari SALDO BERJALAN (smart
#                    saldo: cap ikut tumbuh/menyusut bersama saldo) |
#                    leverage tetap smart-lev.
# RISK_MODE: 0 = tanya menu saat start | 1 | 2 (langsung tanpa menu)
RISK_MODE     = 0           # 0=menu | 1=KLASIK 2=STOPHUNT 3=ZF+SMC 4=PURE-OB (langsung)
RISK_CAP_USD  = 1.20        # rugi maks OPSI 1 (dolar tetap)
RISK_PCT_BAL  = 5.0         # rugi maks OPSI 2 (% saldo berjalan) — DIKUNCI 5%
# ===== DOSIS MINI (11 Agu — kesepakatan LIVE dosis mini, saldo $5) =====
# Rugi maks per trade DIPATOK dolar keras, apapun mode & saldo.
RISK_HARD_USD = 0.30        # plafon rugi absolut per trade
MARGIN_MAX_PCT = 25.0       # plafon margin per posisi: maks 25% saldo
#   (fix kasus XLMUSDT 9 Agu: SL ketat 0.45% -> margin $9 dari saldo $11
#    = 79% saldo tersedot satu posisi -> hujan error 110007 sesudahnya)
# LEVERAGE (5 Agu, permintaan user): BTC/ETH/SOL adalah kontrak paling
# likuid di Bybit — batas bursa jauh lebih tinggi drpd altcoin receh
# (BTC/ETH sampai 100x+, SOL ±75x). Bot TIDAK perlu setinggi itu:
# smart-leverage tetap menghitung dari jarak SL (liq >=35% di luar SL),
# angka di bawah hanyalah PAGAR ATAS yang wajar per karakter coin +
# klem otomatis ke maxLeverage RESMI simbol dari API (leverageFilter).
LEV_CAP = {                  # pagar atas per coin (likuiditas & volatilitas)
    "BTCUSDT": 50,           # paling likuid, gerak paling halus
    "ETHUSDT": 50,
    "SOLUSDT": 25,           # lebih volatil dari BTC/ETH
}
MAX_LEVERAGE  = 25           # pagar default simbol lain (jika SYMBOLS ditambah)
MIN_LEVERAGE  = 1            # majors boleh 1x (SL lebar tetap bisa entry;
                             # dulu 2 -> SL >±36% tertolak, kini fleksibel)
MAX_POSITIONS = 2           # DOSIS MINI 11 Agu (dari 7; satu luka per waktu)
COOLDOWN_MIN  = 15

# ZONA WAKTU (inti video GBB): pasar crypto 24/7 TIDAK punya bel buka.
# "Session" = reset di tengah malam UTC = konvensi JAM, bukan peristiwa
# pasar — band kolaps & reset di "tebing" arbitrer. Video menganjurkan
# SWING ANCHOR utk pasar tanpa bel: VWAP di-reset di setiap swing
# high/low TERKONFIRMASI (pivot 10 bar kiri-kanan) = harga rata-rata
# sejak pasar terakhir BERUBAH ARAH, bukan sejak jam 00:00 UTC.
# Konsekuensi jujur (by design): pivot baru diketahui 10 bar kemudian,
# garis redraw mundur SEKALI saat konfirmasi, setelah itu tak repaint.
# KOREKSI 5 Agu (cek deskripsi resmi TradingView): "the signals and the
# regime colour ALWAYS READ INSTANCE A" — dan DEFAULT resmi: A = SESSION,
# B = Swing (hanya konteks visual). Label MR/TC di chart Anda lahir dari
# anchor SESSION. Supaya bot membaca PERSIS sama dgn chart:
ANCHOR_MODE   = "Session"   # keputusan sinyal = Instance A default resmi
SWING_INFO    = True        # VWAP Swing dihitung sbg INFO pembanding di log
                            # (meniru Instance B hijau di chart — konteks,
                            #  bukan pengambil keputusan)
PIVOT_LEN     = 10          # panjang pivot swing (strict, 10 kiri-kanan)
ADAPTIVE      = False       # KOREKSI 5 Agu: default resmi OFF ("off by default") — band bot kini = band chart default
KER_WEIGHT    = 0.5
KER_LEN, ATR_LEN, REGIME_LEN = 20, 14, 200
OCC_WINDOW, OCC_MIN, HOLD_BARS = 10, 8, 3

BE_AT_R       = 1.0         # SL → BE+fee saat profit 1R
TRAIL_AT_R    = 1.5         # trailing aktif 1.5R (2.0xATR)
TRAIL_ATR_MULT = 2.0
FEE_RT_PCT    = 0.11        # taker round-trip ~0.11% (0.055%/sisi)
SLIP_PCT      = 0.03        # slippage rata2 per SISI (market order) — BE
                            # wajib menutup fee + slippage 2 sisi agar exit
                            # BE benar2 >= 0, bukan minus halus

def be_price(entry, side):
    """TRUE BREAK-EVEN: entry + fee RT + slippage 2 sisi.
    Exit di harga ini = benar-benar impas (fee & slippage terbayar).
    (8 Agu, permintaan user: 'saat BE harus benar-benar 0/impas')"""
    buf = entry * (FEE_RT_PCT + 2 * SLIP_PCT) / 100.0
    return entry + buf if side == "Buy" else entry - buf
# ==================== SMART RIDE MAX (7 Agu, permintaan user) ====================
# Saat harga hampir menyentuh TP dan momentum MASIH searah -> TP DILEPAS,
# profit dibiarkan lari. Pengaman ganda (warisan pro_v15, fix laporan user
# "RIDE dulu bisa exit minus"):
#   1. LANTAI SL dikunci di 60% profit yang SUDAH diraih (ratchet: hanya
#      naik mengikuti puncak baru, tak pernah turun) — mustahil minus.
#   2. Trailing dirapatkan ke RIDE_TRAIL_ATR (lebih ketat dr TS biasa).
# Momentum diukur TANPA indikator tambahan (sistem GBB tetap murni):
# posisi harga vs VWAP + ctx occupancy 8/10 dari indikator yang sama.
# ==================== NEWS GUARD + VOL FILTER (8 Agu, port dari pro_v15) ====
# NEWS SHOCK: berita besar dideteksi dari GEJALANYA — BTC (barometer)
# bergerak mendadak. Saat shock: entry BARU dijeda NEWS_PAUSE_MIN menit
# (posisi aktif tetap dikelola penuh: BE/TS/RIDE jalan terus).
# VOL FILTER: candle 1H dgn ATR meledak > VOL_THRESHOLD x rata-rata =
# pasar sedang kesetanan (news/likuidasi massal) -> skip entry simbol itu.
NEWS_GUARD     = True
NEWS_BTC_FAST  = 0.8         # BTC bergerak >= 0.8% per menit = shock

# ===== CPI GUARD (14 Agu, permintaan user) =====
# NEWS GUARD lama = REAKTIF (bereaksi setelah BTC meledak). CPI jadwalnya
# DIKETAHUI di muka -> blok entry TERJADWAL: 45 mnt sebelum s/d 60 mnt
# sesudah rilis. Posisi aktif TETAP dikelola penuh (BE/TS/RIDE jalan).
# Jadwal resmi BLS 2026, dikonversi ke WIB (8:30 ET; Nov-Des winter time):
CPI_GUARD_ON   = True
CPI_PRE_MIN    = 45          # menit blok SEBELUM rilis
CPI_POST_MIN   = 60          # menit blok SESUDAH rilis
CPI_EVENTS_WIB = [           # (tahun, bulan, tanggal, jam, menit) WIB
    (2026,  9, 11, 19, 30),  # CPI Agu — Jumat
    (2026, 10, 14, 19, 30),  # CPI Sep — Rabu
    (2026, 11, 10, 20, 30),  # CPI Okt — Selasa (winter time AS)
    (2026, 12, 10, 20, 30),  # CPI Nov — Kamis (winter time AS)
]

def cpi_guard_active():
    """True bila SEKARANG (WIB) di dalam jendela blok CPI terdekat.
    Return (aktif, keterangan)."""
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
NEWS_PAUSE_MIN = 10          # jeda entry baru (menit) setelah shock
VOL_FILTER     = True
VOL_THRESHOLD  = 2.5         # ATR kini > 2.5x rata2 50 bar = skip entry

RIDE_ON        = True
RIDE_TRIGGER   = 0.85       # aktif saat harga capai 85% jarak entry->TP
RIDE_TRAIL_ATR = 1.5        # trailing rapat saat riding (xATR)
RIDE_LOCK_PCT  = 0.60       # lantai profit: 60% dari puncak yang diraih

TIME_GUARD_ON = False       # OFF (7 Agu, keputusan user): bukti jam merah 00-04 WIB berasal dari bot utama (TF 5m, ratusan coin) — belum tentu berlaku utk sistem GBB TF 1H BTC/ETH/SOL. Diuji polos dulu; nyalakan lagi jika audit vwap_stats menunjukkan jam rawan yang sama
TIME_GUARD_HOURS = {0, 1, 2, 3, 4}

# SL ANTI-HUNT (5 Agu, konsep Stop Hunt Radar [GBB]): stop menumpuk di
# luar swing high/low; wick sweep tipikal menusuk ±0.5-1 ATR melewatinya.
# Jika SL rencana jatuh DI DALAM zona sweep kolam stop -> geser ke luar:
# nafas lebih lebar, dan RISK CAP menjaga rugi maks tetap sama.
AH_ON        = True
AH_PIVOT     = 3            # pivot kiri-kanan deteksi swing (bar 1H)
AH_DEPTH_ATR = 0.75         # kedalaman sweep tipikal (median jurnal SHR)
AH_MAX_WIDEN = 1.8          # pelebaran maks vs jarak SL asli

STATE_FILE = "vwap_state.json"
STATS_FILE = "vwap_stats.json"       # rapor per sinyal & simbol (brain mini)
LOG_FILE   = "vwap_bot.log"

WIB = timezone(timedelta(hours=7))
def wib_now():
    return datetime.now(timezone.utc).astimezone(WIB)

logging.Formatter.converter = lambda *a: wib_now().timetuple()
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")])
log = logging.getLogger("vwapbot")

session = HTTP(api_key=API_KEY, api_secret=API_SECRET)

# ==================== DASHBOARD TERMINAL (gaya pro_v15) ====================
G, R, Y, C, M, B, D, X = ("\033[92m", "\033[91m", "\033[93m", "\033[96m",
                          "\033[95m", "\033[94m", "\033[90m", "\033[0m")
WIDTH = 96
_logbuf = []
MKT = {}          # info pasar per simbol utk dashboard (jarak sinyal, countdown)
SPIN = ["◐", "◓", "◑", "◒"]
SCAN = {"sym": "-", "idx": 0, "total": 0, "cycle_t": 0.0, "tick": 0,
        "sweep_done": 0, "sweep_total": 1, "last_px": {}}   # status scanner live
def add_log(msg):
    """Log ke file + buffer 10 baris utk panel LIVE LOG."""
    import re as _re
    log.info(_re.sub(r"\033\[\d+m", "", msg))
    _logbuf.append(f"{D}{wib_now().strftime('%H:%M:%S')}{X} {msg}")
    while len(_logbuf) > 10:
        _logbuf.pop(0)

_usd_idr = {"v": 16000.0, "t": 0.0}
def usd_idr():
    if time.time() - _usd_idr["t"] > 1800:
        try:
            r = requests.get("https://open.er-api.com/v6/latest/USD", timeout=6)
            v = float(r.json()["rates"]["IDR"])
            if v > 1000:
                _usd_idr.update({"v": v, "t": time.time()})
        except Exception:
            _usd_idr["t"] = time.time() - 1500   # coba lagi 5 mnt
    return _usd_idr["v"]

_news = {"until": 0.0, "reason": ""}

def news_active():
    return NEWS_GUARD and time.time() < _news["until"]

_btc_watch = {"px": 0.0, "t": 0.0}
def news_shock_check():
    """Pantau harga BTC antar-cek; lonjakan cepat = shock -> jeda entry."""
    if not NEWS_GUARD:
        return
    try:
        px = get_price("BTCUSDT")
        now = time.time()
        if px and _btc_watch["px"] and now > _btc_watch["t"]:
            mins = max((now - _btc_watch["t"]) / 60.0, 0.5)
            rate = (px - _btc_watch["px"]) / _btc_watch["px"] * 100 / mins
            if abs(rate) >= NEWS_BTC_FAST:
                first = now > _news["until"]
                _news["until"] = now + NEWS_PAUSE_MIN * 60
                _news["reason"] = f"BTC {rate:+.2f}%/menit"
                if first:
                    add_log(f"{R}🚨 NEWS SHOCK! {_news['reason']} — entry "
                            f"dijeda {NEWS_PAUSE_MIN}m (posisi aktif tetap dikelola){X}")
        if px:
            _btc_watch.update({"px": px, "t": now})
    except Exception as e:
        log.error(f"news_shock: {e}")

_btc = {"dir": "FLAT", "px": 0.0, "t": 0.0}
def btc_view():
    """Arah BTC dari EMA20 vs EMA50 candle 1H tutup (BULL/BEAR/FLAT)."""
    if time.time() - _btc["t"] > 120:
        try:
            df = get_kline("BTCUSDT", "60", 120)
            if not df.empty and len(df) > 60:
                c = df["close"].iloc[:-1]
                e20 = c.ewm(span=20, adjust=False).mean().iloc[-1]
                e50 = c.ewm(span=50, adjust=False).mean().iloc[-1]
                gap = (e20 - e50) / e50 * 100
                _btc["dir"] = "BULL" if gap > 0.15 else "BEAR" if gap < -0.15 else "FLAT"
                _btc["px"] = float(df["close"].iloc[-1])
                _btc["t"] = time.time()
        except Exception:
            _btc["t"] = time.time() - 60
    return _btc["dir"], _btc["px"]

BG_G, BG_R = "\033[48;5;22m", "\033[48;5;52m"   # blok hijau/merah gelap
FW = "\033[97m\033[1m"                            # teks putih tebal

def _vlen(txt):
    import re as _re
    return len(_re.sub(r"\033\[[0-9;]*m", "", txt))

def _row(txt=""):
    pad = max(0, WIDTH - 4 - _vlen(txt))
    return f"{C}║{X} {txt}{' ' * pad} {C}║{X}"

def _rowbg(txt, bg):
    """Baris dengan blok warna latar penuh (posisi aktif)."""
    pad = max(0, WIDTH - 4 - _vlen(txt))
    return f"{C}║{X} {bg}{txt}{' ' * pad}{X} {C}║{X}"

def _bar(frac, width, col):
    frac = max(0.0, min(1.0, frac))
    fill = int(round(frac * width))
    return f"{col}{'█' * fill}{D}{'░' * (width - fill)}{X}"

def _liq_pct(lev):
    return (1.0 / lev - 0.006) * 100 if lev else 0.0

BIGFONT = {
    'S': ("▄▀▀▀", "▀▀▀▄", "▄  █", " ▀▀ "),
    'H': ("█  █", "█▀▀█", "█  █", "█  █"),
    'O': ("▄▀▀▄", "█  █", "█  █", " ▀▀ "),
    'R': ("█▀▀▄", "█▄▄▀", "█ ▀▄", "█  █"),
    'T': ("▀▀▀▀", " ██ ", " ██ ", " ██ "),
    'L': ("█   ", "█   ", "█   ", "█▄▄▄"),
    'N': ("█▄ █", "█▀▄█", "█ ▀█", "█  █"),
    'G': ("▄▀▀▄", "█   ", "█ ▀█", " ▀▀▀"),
}

def bigword(word):
    """Kata -> 4 baris huruf raksasa (font pro_v15)."""
    letters = [BIGFONT[c] for c in word if c in BIGFONT]
    return [" ".join(l[i] for l in letters) for i in range(4)]

def _rowbg_word(txt, bg, wrow, wcol):
    """Baris blok warna + huruf raksasa rata-kanan (gaya pro_v15).
    Jika konten terlalu panjang, spasi dikompres; konten diutamakan."""
    avail = WIDTH - 4 - _vlen(txt) - _vlen(wrow)
    if avail < 2:
        compact = txt.replace('  │  ', ' │ ').replace('   ', ' ')
        if WIDTH - 4 - _vlen(compact) - _vlen(wrow) >= 2:
            txt = compact
            avail = WIDTH - 4 - _vlen(txt) - _vlen(wrow)
    if avail >= 2:
        txt = txt + ' ' * avail + f"\033[1m{wcol}{wrow}{X}"
    return _rowbg(txt, bg)

SLIMFONT = {
    '0': ("▄▀▄", "█ █", "█ █", " ▀ "),
    '1': ("▄█ ", " █ ", " █ ", "▄█▄"),
    '2': ("▀▀▄", "▄▄▀", "█  ", "▀▀▀"),
    '3': ("▀▀▄", " ▄▀", "  █", "▀▀ "),
    '4': ("█ █", "█▄█", "  █", "  █"),
    '5': ("█▀▀", "▀▀▄", "  █", "▀▀ "),
    '6': ("▄▀ ", "█▄ ", "█ █", " ▀ "),
    '7': ("▀▀█", " █ ", "█  ", "█  "),
    '8': ("▄▀▄", " ▀ ", "█ █", " ▀ "),
    '9': ("▄▀▄", " ▀█", "  █", " ▀ "),
    '.': (" ", " ", " ", "▄"),
}

def _bignum(txt):
    """Angka -> 4 baris huruf raksasa (3 kolom/digit, font pro_v15)."""
    letters = [SLIMFONT[ch] for ch in txt if ch in SLIMFONT]
    return ["".join(l[i] for l in letters) for i in range(4)]

def fmt_rp(v, dec=2):
    """Format Rupiah gaya Indonesia: 301.277,00 (titik ribuan, koma desimal)."""
    s = f"{v:,.{dec}f}"
    return s.replace(",", "@").replace(".", ",").replace("@", ".")

def big_panel(bal, idr, bdir, bpx):
    """6 baris: harga BTC RAKSASA (kiri) BERSANDING saldo Rp RAKSASA penuh
    (kanan) — Rp 301.277 tampil utuh, bukan '301 ribu'."""
    bcol = G if bdir == "BULL" else R if bdir == "BEAR" else Y
    tag = "▲BULL" if bdir == "BULL" else "▼BEAR" if bdir == "BEAR" else "•FLAT"
    btc_txt = f"{bpx:.0f}" if bpx >= 1000 else (f"{bpx:.2f}" if bpx > 0 else "0")
    idr_val = bal * idr
    idr_txt = f"{idr_val:.0f}"               # ANGKA PENUH: 301277
    big_b = _bignum(btc_txt)
    big_i = _bignum(idr_txt)
    half = (WIDTH - 4) // 2
    rows = []
    head_l = f"👑 BTC/USDT {bcol}{tag}{X}"
    head_r = f"💰 SALDO {G}${bal:,.2f}{X}"
    rows.append(head_l + " " * max(1, half - _vlen(head_l)) + head_r)
    for i in range(4):
        lpart = f"{bcol}{big_b[i]}{X}"
        rpart = f"{G}{big_i[i]}{X}"
        rows.append(lpart + " " * max(1, half - _vlen(lpart)) + rpart)
    foot_l = f"{D}1$ = Rp {fmt_rp(idr, 0)}{X}"
    foot_r = f"{G}= Rp {fmt_rp(idr_val)}{X}"
    rows.append(foot_l + " " * max(1, half - _vlen(foot_l)) + foot_r)
    return rows

def _sep(title=""):
    if not title:
        return f"{C}╠{'═' * (WIDTH - 2)}╣{X}"
    import re as _re
    vis = len(_re.sub(r"\033\[\d+m", "", title))
    return f"{C}╠═ {Y}{title}{X} {C}{'═' * max(0, WIDTH - 6 - vis)}╣{X}"

def render_dash(bal, regimes):
    L = [f"{C}╔{'═' * (WIDTH - 2)}╗{X}"]
    idr = usd_idr()
    bdir, bpx = btc_view()
    bcol = G if bdir == "BULL" else R if bdir == "BEAR" else Y
    mode_txt = {1: f"cap ${RISK_CAP_USD:.2f} [M1-KLASIK]",
                2: f"cap {RISK_PCT_BAL:g}%saldo [M2-STOPHUNT]",
                3: f"cap ${RISK_HARD_USD:.2f} [M3-ZF+SMC]",
                4: f"cap ${RISK_HARD_USD:.2f} [M4-PURE-OB]"}.get(
                    RISK_MODE_ACTIVE, "?")
    L.append(_row(f"{B}📊 VWAP BOT [GBB-port]{X}  {D}|{X}  TF {INTERVAL}m  "
                  f"{D}|{X}  anchor {ANCHOR_MODE}  {D}|{X}  {mode_txt}  "
                  f"{D}|{X}  {wib_now().strftime('%d %b %H:%M:%S WIB')}"))
    L.append(_sep())
    for pr in big_panel(bal, idr, bdir, bpx):
        L.append(_row(pr))
    if news_active():
        L.append(_row(f"{R}🚨 NEWS SHOCK AKTIF — {_news['reason']} | entry dijeda "
                      f"{max(0,(_news['until']-time.time())/60):.0f} menit lagi{X}"))
    _cpi_d, _cpi_ket_d = cpi_guard_active()
    if _cpi_d:
        L.append(_row(f"{R}📰 CPI GUARD AKTIF — {_cpi_ket_d} | entry baru diblokir{X}"))
    tg_txt = ("OFF (uji polos)" if not TIME_GUARD_ON else
              "🔴 SEDANG MEMBLOKIR (00-04 WIB)" if wib_now().hour in TIME_GUARD_HOURS
              else "siaga (blokir 00-04 WIB)")
    L.append(_row(f"🌙 TimeGuard {tg_txt}   "
                  f"{D}max {MAX_POSITIONS} posisi | cooldown {COOLDOWN_MIN}m | "
                  f"margin ${ENTRY_MARGIN:g} | scan {len(SYMBOLS)} coin{X}"))
    n_act = sum(1 for s in STATES.values() if s.get("in_position"))
    L.append(_sep(f"🔴 POSISI AKTIF ({n_act}/{MAX_POSITIONS})"))
    if n_act == 0:
        L.append(_row(f"{D}Menunggu eksekusi…{X}"))
    # FIX (8 Agu, laporan user "7/7 tapi tampil 4"): iterasi dari STATES,
    # bukan SYMBOLS — posisi di coin yang keluar dari daftar dinamis
    # (turnover turun) tetap WAJIB tampil & terkelola.
    for sym in sorted(STATES.keys()):
        s = STATES.get(sym, {})
        if not s.get("in_position"):
            continue
        # detail posisi gaya pro_v15: blok warna + 4 baris info lengkap
        side = s.get("side")
        e, sl, tp = s.get("entry", 0), s.get("sl", 0), s.get("tp", 0)
        lev = s.get("lev") or 1
        m_used = s.get("margin_used") or 0
        pnl = s.get("last_pnl") or 0.0
        px = get_price(sym) or e
        roi = pnl / m_used * 100 if m_used else 0
        risk = abs(e - sl) if sl else 0
        rr = ((px - e) if side == "Buy" else (e - px)) / risk if risk else 0
        tp_m = abs(tp - e) / e * 100 * lev if e and tp else 0
        sl_m = abs(e - sl) / e * 100 * lev if e and sl else 0
        span = abs(tp - sl) if tp and sl else 0
        prog = abs(px - sl) / span if span else 0
        if side != "Buy":
            prog = 1 - prog
        blok = BG_G if pnl >= 0 else BG_R
        arrow = "▲ LONG " if side == "Buy" else "▼ SHORT"
        badges = f"  {Y}[{s.get('kind','?')}]{X}"
        if s.get("be_done"):
            badges += f"  {C}[BE ✔]{X}"
        if s.get("trail_on"):
            badges += f"  {M}[TS ✔]{X}"
        if s.get("riding"):
            badges += f"  {G}{FW}[🚀 RIDE]{X}"
        if s.get("ah"):
            badges += f"  {C}[🛡🎣]{X}"
        WROWS = bigword("LONG" if side == "Buy" else "SHORT")
        wcol = G if side == "Buy" else R
        L.append(_rowbg_word(f"\033[1m{wcol}{arrow}{X} {FW}{sym:<10} "
                             f"{pnl:+8.2f}$ ({roi:+7.2f}%)  "
                             f"RR {rr:+.2f}R{X}{badges}", blok, WROWS[0], wcol))
        L.append(_rowbg_word(f"{FW}  SL {X}{_bar(prog, 24, G if pnl >= 0 else R)}"
                             f"{FW} TP   Live {px:.8g}{X}", blok, WROWS[1], wcol))
        tp_disp = "TP ∞ RIDE MAX" if s.get("riding") else f"TP {tp:.8g} ({tp_m:+.1f}%)"
        L.append(_rowbg_word(f"{FW}  Entry {e:.8g}   {tp_disp}   "
                             f"SL {sl:.8g} ({-sl_m:.1f}%){X}", blok, WROWS[2], wcol))
        lqp = _liq_pct(lev)
        slp = abs(e - sl) / e * 100 if e and sl else 0
        L.append(_rowbg_word(f"{FW}  IDR {pnl * idr:+,.0f}  │  Margin ${m_used:.2f}  │  "
                             f"Lev {lev:.0f}x  │  Liq~{lqp:.1f}% "
                             f"{'✔' if lqp > slp else '⚠'}{X}", blok, WROWS[3], wcol))
        L.append(_row())
    # ── SCANNER LIVE: coin yang SEDANG dipindai + progress sweep ──
    SCAN["tick"] += 1
    L.append(_sep("⚙ SCANNER"))
    _idle_left = SCAN.get("idle_until", 0) - time.time()
    _sw = SCAN["sweep_done"] / max(SCAN["sweep_total"], 1)
    if _idle_left > 0 and SCAN["idx"] >= SCAN["total"]:
        # jeda antar siklus: tampilkan countdown, bukan simbol beku
        _pi = 1.0 - _idle_left / 30.0
        L.append(_row(f"{Y}{SPIN[SCAN['tick'] % 4]}{X}  "
                      f"{D}batch selesai ({SCAN['total']} coin, {SCAN['cycle_t']:.1f}s) — "
                      f"siklus berikut dlm{X} {FW}{_idle_left:2.0f}s{X} "
                      f"{_bar(_pi, 20, Y)}"))
    else:
        _pct = SCAN["idx"] / SCAN["total"] if SCAN["total"] else 0
        L.append(_row(f"{Y}{SPIN[SCAN['tick'] % 4]}{X}  {FW}{SCAN['sym']:<14}{X} "
                      f"{_bar(_pct, 20, G)} {B}{SCAN['idx']:>3}/{SCAN['total']}{X}  "
                      f"{D}batch {SCAN['cycle_t']:.1f}s{X}"))
    L.append(_row(f"   {D}sweep semua coin:{X} {_bar(_sw, 20, C)} "
                  f"{D}{SCAN['sweep_done']}/{SCAN['sweep_total']} — full ±5 mnt, "
                  f"tiap coin tercek tiap bar 1H{X}"))
    # ── MARKET PULSE: skor kondisi pasar gabungan (0-100) dlm bar ──
    # Bahan: arah BTC (EMA20/50) + rata2 posisi harga vs VWAP semua simbol
    # + porsi simbol trending. Murni dari data yang SUDAH ada (nol API).
    pulse = 50.0
    try:
        pulse = 50.0 + (15.0 if bdir == "BULL" else -15.0 if bdir == "BEAR" else 0.0)
        above = tot_s = trend_n = 0
        for sym2, mk2 in MKT.items():
            if mk2.get("px") and mk2.get("vwap"):
                tot_s += 1
                if mk2["px"] > mk2["vwap"]:
                    above += 1
                if regimes.get(sym2) == "TRENDING":
                    trend_n += 1
        if tot_s:
            pulse += (above / tot_s - 0.5) * 40.0      # dominasi sisi VWAP
            pulse += (trend_n / tot_s) * 10.0          # pasar berenergi
        pulse = max(0.0, min(100.0, pulse))
    except Exception:
        pass
    pcol = G if pulse >= 60 else R if pulse <= 40 else Y
    plabel = ("GREED/BULL" if pulse >= 65 else "OPTIMIS" if pulse >= 55 else
              "FEAR/BEAR" if pulse <= 35 else "PESIMIS" if pulse <= 45 else "NETRAL")
    L.append(_sep("🌡 MARKET PULSE"))
    L.append(_row(f"  {pcol}{_bar(pulse / 100.0, 34, pcol)} {pulse:3.0f}/100 "
                  f"{FW}{plabel}{X}  {D}(BTC + posisi vs VWAP + energi trend){X}"))
    # countdown candle 1H (sama utk semua simbol TF 60m)
    cdl = ""
    for v in MKT.values():
        rem = v.get("bar_end", 0) - time.time()
        if rem > 0:
            m, sec = int(rem // 60), int(rem % 60)
            cdl = f"{D}⏱ candle {INTERVAL}m tutup dlm {m:02d}:{sec:02d}{X}"
        break
    L.append(_sep("PASAR & STATUS" + ("  " if cdl else "")))
    if cdl:
        L.append(_row(cdl))
    # dgn 200+ simbol: tampilkan CORE + 7 kandidat TERDEKAT ke sinyal saja
    def _dist_key(sym2):
        mk2 = MKT.get(sym2)
        if not mk2 or not mk2.get("px"):
            return 9e9
        px2, vw2, u22, l22 = mk2["px"], mk2["vwap"], mk2["up2"], mk2["lo2"]
        rg2 = regimes.get(sym2, "?")
        if rg2 == "RANGING" and u22 and l22:
            return min(abs(px2 - l22), abs(u22 - px2)) / px2
        if rg2 == "TRENDING" and vw2 and mk2.get("ctx") in (1, -1):
            return abs(px2 - vw2) / px2
        return 9e9
    idle_sorted = sorted([s2 for s2 in regimes if not STATES.get(s2, {}).get("in_position")],
                         key=_dist_key)
    show_list = list(dict.fromkeys(CORE_SYMBOLS +
                                   [s2 for s2 in idle_sorted if _dist_key(s2) < 9e9][:7]))
    for sym in show_list:
        s = STATES.get(sym, {})
        if s.get("in_position"):
            continue
        rg = regimes.get(sym, "?")
        rgc = M if rg == "TRENDING" else Y if rg == "RANGING" else D
        cd = max(0, COOLDOWN_MIN * 60 - (time.time() - s.get("last_exit", 0)))
        # jarak ke pemicu sinyal terdekat (persen dari harga)
        info = ""
        mk = MKT.get(sym)
        if mk and mk["px"] > 0:
            px, vw, u2, l2 = mk["px"], mk["vwap"], mk["up2"], mk["lo2"]
            # bar kedekatan: jarak 0% = penuh (siap meledak), >=2% = kosong
            def _near(dpct):
                return _bar(max(0.0, 1.0 - dpct / 2.0), 10,
                            G if dpct < 0.5 else Y if dpct < 1.2 else D)
            if rg == "RANGING" and u2 and l2:
                d_lo = (px - l2) / px * 100
                d_up = (u2 - px) / px * 100
                if d_lo <= d_up:
                    info = f"{G}MR-long {X}{_near(d_lo)} {D}{d_lo:.2f}% ke band{X}"
                else:
                    info = f"{R}MR-short{X} {_near(d_up)} {D}{d_up:.2f}% ke band{X}"
            elif rg == "TRENDING" and vw:
                dv = abs(px - vw) / px * 100
                if mk["ctx"] == 1:
                    info = f"{G}TC-long {X}{_near(dv)} {D}{dv:.2f}% ke VWAP{X}"
                elif mk["ctx"] == -1:
                    info = f"{R}TC-short{X} {_near(dv)} {D}{dv:.2f}% ke VWAP{X}"
                else:
                    info = f"{D}dominasi 8/10 belum ada (ctx 0){X}"
        st = (f"{Y}⏳ cooldown {cd/60:.0f}m {_bar(1 - cd/(COOLDOWN_MIN*60), 10, Y)}{X}"
              if cd > 0 else (info or f"{D}scan…{X}"))
        L.append(_row(f"  {B}{sym:9s}{X} {rgc}{rg:9s}{X} {st}"))
    # ── PERFORMANCE: rapor per sinyal|coin dari vwap_stats.json ──
    if STATS or DAYSTATS["n"]:
        L.append(_sep("🏆 PERFORMANCE (per sinyal)"))
        if DAYSTATS["date"] == wib_now().strftime("%Y-%m-%d") and DAYSTATS["n"]:
            dc = G if DAYSTATS["pnl"] >= 0 else R
            L.append(_row(f"📅 HARI INI: {DAYSTATS['n']} trade | W{DAYSTATS['w']}/L{DAYSTATS['n']-DAYSTATS['w']} | {dc}{DAYSTATS['pnl']:+.2f}${X}"))
        tot_n = sum(v["n"] for v in STATS.values()) if STATS else 0
        tot_w = sum(v["w"] for v in STATS.values()) if STATS else 0
        tot_p = sum(v["pnl"] for v in STATS.values()) if STATS else 0.0
        tc = G if tot_p >= 0 else R
        if tot_n:
            L.append(_row(f"TOTAL: {tot_n} trade | WR "
                          f"{(tot_w/tot_n*100 if tot_n else 0):.0f}% | PnL {tc}{tot_p:+.2f}${X}"))
        for k in sorted(STATS, key=lambda x: -abs(STATS[x]["pnl"]))[:6]:
            v = STATS[k]
            pc2 = G if v["pnl"] >= 0 else R
            wr = v["w"] / v["n"] * 100 if v["n"] else 0
            L.append(_row(f"  {D}{k:<16}{X} n={v['n']:<3} WR {wr:3.0f}%  "
                          f"{pc2}{v['pnl']:+7.2f}${X} {_bar(wr/100, 12, pc2)}"))
    L.append(_sep("📝 LIVE LOG"))
    if _logbuf:
        for ln in _logbuf:
            L.append(_row(ln))
    else:
        L.append(_row(f"{D}menunggu aktivitas…{X}"))
    L.append(f"{C}╚{'═' * (WIDTH - 2)}╝{X}")
    frame = "\n".join(ln + "\033[K" for ln in L)
    sys.stdout.write("\033[?25l\033[H" + frame + "\033[J")
    sys.stdout.flush()

# ==================== UTIL BURSA ====================
_lot_cache = {}
_lev_cache = {}
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
    """(min, max) leverage RESMI simbol dari bursa (cache)."""
    if sym not in _lev_cache:
        get_lot_filter(sym)
    return _lev_cache.get(sym, (1.0, 100.0))

def get_kline(sym, interval, limit=500):
    try:
        r = session.get_kline(category="linear", symbol=sym,
                              interval=interval, limit=limit)
        rows = r["result"]["list"]
        rows.reverse()                      # tua → baru
        df = pd.DataFrame(rows, columns=["ts", "open", "high", "low",
                                         "close", "volume", "turnover"])
        for c in ["open", "high", "low", "close", "volume"]:
            df[c] = pd.to_numeric(df[c])
        df["ts"] = pd.to_numeric(df["ts"])
        return df
    except Exception as e:
        log.error(f"kline {sym}: {e}")
        return pd.DataFrame()

_px_cache = {}   # sym -> (harga, ts) — cache 2 dtk utk dashboard real-time
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
    """Saldo yang BENAR-BENAR tersedia utk margin baru (fix spam 110007).
    Equity total menghitung margin yang sudah terpakai posisi aktif —
    order berdasarkan equity = ditolak bursa 'ab not enough'."""
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
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
                      json={"chat_id": TELEGRAM_CHAT, "text": msg,
                            "parse_mode": "Markdown"}, timeout=5)
    except Exception:
        pass

# ==================== INDIKATOR (port 1:1 dari Pine) ====================
def compute_indicator(df, mode=ANCHOR_MODE, pl=PIVOT_LEN):
    """Hitung seri vwap, sigma, KER, ATR%, regime, ctx utk seluruh df.
    Semua keputusan memakai bar SUDAH TUTUP (baris terakhir df dianggap
    bar berjalan → sinyal dibaca di index -2)."""
    n = len(df)
    if n < REGIME_LEN + KER_LEN + 5:
        return None
    close, high, low, vol = (df["close"].values, df["high"].values,
                             df["low"].values, df["volume"].values)
    tp = (high + low + close) / 3.0
    ts = df["ts"].values

    # --- KER(20) ---
    ker = [float("nan")] * n
    for i in range(KER_LEN, n):
        path = sum(abs(close[j] - close[j - 1]) for j in range(i - KER_LEN + 1, i + 1))
        ker[i] = 0.0 if path == 0 else abs(close[i] - close[i - KER_LEN]) / path

    # --- ATR% (Wilder RMA, seed SMA — sama dgn ta.atr) ---
    tr = [high[0] - low[0]]
    for i in range(1, n):
        tr.append(max(high[i] - low[i], abs(high[i] - close[i - 1]),
                      abs(low[i] - close[i - 1])))
    atr = [float("nan")] * n
    if n > ATR_LEN:
        seed = sum(tr[1:ATR_LEN + 1]) / ATR_LEN
        atr[ATR_LEN] = seed
        for i in range(ATR_LEN + 1, n):
            atr[i] = (atr[i - 1] * (ATR_LEN - 1) + tr[i]) / ATR_LEN
    atrpct = [a / close[i] if a == a else float("nan") for i, a in enumerate(atr)]

    # --- median 200 (genap: rata-rata 2 nilai tengah — persis f_median) ---
    def med200(series, i):
        w = series[i - REGIME_LEN + 1: i + 1]
        if any(x != x for x in w):
            return float("nan")
        s = sorted(w)
        m = REGIME_LEN // 2
        return (s[m - 1] + s[m]) / 2.0

    # --- anchor events ---
    def utc_dt(ms):
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)
    anchor = [False] * n
    anchor[0] = True
    if mode in ("Session", "Week", "Month"):
        for i in range(1, n):
            a, b = utc_dt(ts[i - 1]), utc_dt(ts[i])
            if mode == "Session":
                anchor[i] = a.date() != b.date()
            elif mode == "Week":
                anchor[i] = a.isocalendar()[1] != b.isocalendar()[1]
            else:
                anchor[i] = a.month != b.month
    else:  # Swing: pivot strict terkonfirmasi pl bar kemudian
        for i in range(2 * pl, n):
            c = i - pl                       # bar pivot kandidat
            ch, cl = high[c], low[c]
            ph = all(ch > high[j] for j in range(i - 2 * pl, i + 1) if j != c)
            pw = all(cl < low[j] for j in range(i - 2 * pl, i + 1) if j != c)
            if ph or pw:
                anchor[i] = True             # konfirmasi di bar i

    # --- akumulator VWAP + sigma (backfill swing dari bar pivot) ---
    vwap = [float("nan")] * n
    sigma = [float("nan")] * n
    sPv = sV = sP2v = 0.0
    for i in range(n):
        if anchor[i]:
            sPv = sV = sP2v = 0.0
            if mode == "Swing" and i >= pl:
                for j in range(i - pl, i):   # pivot..konfirmasi-1
                    sPv += tp[j] * vol[j]
                    sV += vol[j]
                    sP2v += tp[j] * tp[j] * vol[j]
        sPv += tp[i] * vol[i]
        sV += vol[i]
        sP2v += tp[i] * tp[i] * vol[i]
        if sV > 0:
            v = sPv / sV
            vwap[i] = v
            sigma[i] = math.sqrt(max(sP2v / sV - v * v, 0.0))

    # --- regime & band per bar ---
    regime = [-1] * n
    up2 = [float("nan")] * n
    lo2 = [float("nan")] * n
    for i in range(REGIME_LEN + KER_LEN, n):
        mk, ma = med200(ker, i), med200(atrpct, i)
        if mk == mk and ma == ma:
            regime[i] = 2 * (1 if ker[i] > mk else 0) + (1 if atrpct[i] > ma else 0)
        adapt = 1.0 + KER_WEIGHT * (1.0 - ker[i]) if (ADAPTIVE and ker[i] == ker[i]) else 1.0
        if sigma[i] == sigma[i]:
            up2[i] = vwap[i] + 2.0 * adapt * sigma[i]
            lo2[i] = vwap[i] - 2.0 * adapt * sigma[i]

    # --- ctx occupancy (window = OCC_WINDOW bar SEBELUM bar kini) ---
    last_anchor = [0] * n
    la = 0
    for i in range(n):
        if anchor[i]:
            la = i
        last_anchor[i] = la
    ctx = [0] * n
    for i in range(OCC_WINDOW + 1, n):
        if i - last_anchor[i] >= OCC_WINDOW:
            cnt = sum(1 for j in range(i - OCC_WINDOW, i)
                      if vwap[j] == vwap[j] and close[j] > vwap[j])
            ctx[i] = 1 if cnt >= OCC_MIN else (-1 if (OCC_WINDOW - cnt) >= OCC_MIN else 0)

    return {"close": close, "high": high, "low": low, "vwap": vwap,
            "sigma": sigma, "up2": up2, "lo2": lo2, "regime": regime,
            "ctx": ctx, "atr": atr, "anchor": anchor, "ts": list(ts)}

def read_signal(ind, st):
    """Baca sinyal MR/TC pada bar TUTUP terakhir (index -2).
    st menyimpan deadline TC antar-pemanggilan (persis var Pine)."""
    i = len(ind["close"]) - 2                # bar sudah tutup
    if i < 1:
        return None
    rg = ind["regime"][i]
    ranging, trending = rg in (0, 1), rg in (2, 3)
    c, c1 = ind["close"][i], ind["close"][i - 1]
    u2, u2p, l2, l2p = ind["up2"][i], ind["up2"][i - 1], ind["lo2"][i], ind["lo2"][i - 1]
    vw = ind["vwap"][i]
    sig = None
    # --- MR ---
    if all(x == x for x in (u2, u2p, l2, l2p)):
        if c1 < l2p and l2 <= c <= u2 and ranging:
            sig = ("MR", "Buy", vw)              # target: VWAP
        elif c1 > u2p and l2 <= c <= u2 and ranging:
            sig = ("MR", "Sell", vw)
    # --- TC (stateful deadline, episode mati saat ctx flip / anchor) ---
    # FIX AUDIT (7 Agu): deadline dulu pakai INDEKS ARRAY — dgn kline
    # limit tetap 500, bar tutup SELALU index 498 → deadline 501 >= 498
    # SELAMANYA → jendela "3 bar" tak pernah kedaluwarsa! Kini pakai
    # NOMOR BAR ABSOLUT dari timestamp (kebal geser array & restart).
    bar_ms = int(INTERVAL) * 60 * 1000
    bno = int(ind["ts"][i] // bar_ms)            # nomor bar absolut
    ctx = ind["ctx"][i]
    if ind["anchor"][i] or vw != vw:
        st["longDl"] = st["shortDl"] = -1
    else:
        if ctx != 1:
            st["longDl"] = -1
        if ctx != -1:
            st["shortDl"] = -1
        if ctx == 1 and ind["low"][i] <= vw:
            st["longDl"] = max(st.get("longDl", -1), bno + HOLD_BARS)
        if ctx == -1 and ind["high"][i] >= vw:
            st["shortDl"] = max(st.get("shortDl", -1), bno + HOLD_BARS)
        if st.get("longDl", -1) >= bno and c > vw and trending and sig is None:
            sig = ("TC", "Buy", u2)              # target: band +2σ
            st["longDl"] = -1
        if st.get("shortDl", -1) >= bno and c < vw and trending and sig is None:
            sig = ("TC", "Sell", l2)
            st["shortDl"] = -1
    if sig:
        atr_i = ind["atr"][i]
        return {"kind": sig[0], "side": sig[1], "target": sig[2],
                "close": c, "vwap": vw, "atr": atr_i if atr_i == atr_i else 0.0,
                "up2": u2, "lo2": l2, "bar_i": i}
    return None

# ==================== MODE 3: ZF + SMC Sweep & Momentum ====================
# Port 1:1 dari Pine user "ZF + SMC: Sweep & Momentum" (12 Agu):
#   - kolam likuiditas = pivot high/low periode 5 (strict, bar tutup)
#   - SWEEP: low tembus swingLow tapi CLOSE balik di atasnya (dan sebaliknya)
#   - MOMENTUM: body candle > 1.5x SMA(14) body
#   - entry = sweep + momentum SEARAH; SL = ujung ekor candle sweep
#     (± 10 tick); TP = RR 2.0 dari jarak SL. Anti-repaint: bar tutup (-2).
ZF_SWING      = 5
ZF_VOL_MULT   = 1.5
ZF_RR         = 2.0

def read_signal_zfsmc(df, st):
    o = pd.to_numeric(df["open"]).values
    h, l, c = df["high"].values, df["low"].values, df["close"].values
    n = len(c); i = n - 2                     # bar tutup terakhir
    if i < ZF_SWING * 2 + 20:
        return None
    # pivot terakhir yang SUDAH terkonfirmasi pada bar i (pivot butuh
    # ZF_SWING bar kanan → kandidat terakhir adalah i-ZF_SWING)
    lastH = lastL = float("nan")
    for j in range(i - ZF_SWING, ZF_SWING - 1, -1):
        ph = all(h[j] > h[j - k] for k in range(1, ZF_SWING + 1)) and \
             all(h[j] > h[j + k] for k in range(1, ZF_SWING + 1))
        if ph and lastH != lastH:
            lastH = h[j]
        pl_ = all(l[j] < l[j - k] for k in range(1, ZF_SWING + 1)) and \
              all(l[j] < l[j + k] for k in range(1, ZF_SWING + 1))
        if pl_ and lastL != lastL:
            lastL = l[j]
        if lastH == lastH and lastL == lastL:
            break
    body = abs(c[i] - o[i])
    avg_body = pd.Series(abs(pd.Series(c[max(0, i-13):i+1]).values -
                             pd.Series(o[max(0, i-13):i+1]).values)).mean()
    if avg_body != avg_body or avg_body <= 0:
        return None
    mom_bull = c[i] > o[i] and body > avg_body * ZF_VOL_MULT
    mom_bear = o[i] > c[i] and body > avg_body * ZF_VOL_MULT
    tick = c[i] * 0.0001                       # proxy 10-tick buffer
    if lastL == lastL and l[i] < lastL and c[i] > lastL and mom_bull:
        sl = l[i] - tick
        tp = c[i] + (c[i] - sl) * ZF_RR
        return {"kind": "ZF", "side": "Buy", "target": tp, "sl": sl,
                "close": c[i], "vwap": float("nan"), "atr": 0.0,
                "up2": float("nan"), "lo2": float("nan"), "bar_i": i}
    if lastH == lastH and h[i] > lastH and c[i] < lastH and mom_bear:
        sl = h[i] + tick
        tp = c[i] - (sl - c[i]) * ZF_RR
        return {"kind": "ZF", "side": "Sell", "target": tp, "sl": sl,
                "close": c[i], "vwap": float("nan"), "atr": 0.0,
                "up2": float("nan"), "lo2": float("nan"), "bar_i": i}
    return None

# ==================== MODE 4: Pure Order Block SMC ====================
# Port 1:1 dari Pine user "Pure Order Block SMC" (12 Agu). Pine aslinya
# VISUALISASI kotak OB; utk bot dijadikan sinyal dgn aturan minimal:
#   bull FVG: low[i] > high[i-2] dan candle i-1 hijau; OB = candle i-2
#   merah → BUY saat pola terkonfirmasi (bar tutup). SL = bawah kotak OB
#   (low[i-2]) − buffer; TP = RR 2.0 (aturan tambahan, dicatat jujur —
#   Pine asli tidak mendefinisikan entry/exit).
OB_RR = 2.0

def read_signal_pureob(df, st):
    o = pd.to_numeric(df["open"]).values
    h, l, c = df["high"].values, df["low"].values, df["close"].values
    n = len(c); i = n - 2
    if i < 5:
        return None
    tick = c[i] * 0.0001
    bull_fvg = l[i] > h[i - 2] and c[i - 1] > o[i - 1]
    bear_fvg = h[i] < l[i - 2] and c[i - 1] < o[i - 1]
    if bull_fvg and c[i - 2] < o[i - 2]:       # BULL OB
        sl = l[i - 2] - tick
        if sl < c[i]:
            tp = c[i] + (c[i] - sl) * OB_RR
            return {"kind": "OB", "side": "Buy", "target": tp, "sl": sl,
                    "close": c[i], "vwap": float("nan"), "atr": 0.0,
                    "up2": float("nan"), "lo2": float("nan"), "bar_i": i}
    if bear_fvg and c[i - 2] > o[i - 2]:       # BEAR OB
        sl = h[i - 2] + tick
        if sl > c[i]:
            tp = c[i] - (sl - c[i]) * OB_RR
            return {"kind": "OB", "side": "Sell", "target": tp, "sl": sl,
                    "close": c[i], "vwap": float("nan"), "atr": 0.0,
                    "up2": float("nan"), "lo2": float("nan"), "bar_i": i}
    return None

# ==================== EKSEKUSI (pagar bot utama) ====================
def fmt_px(v):
    """Angka -> string desimal polos (anti e-notation '7.1e-07' yang
    ditolak Bybit). Kelas bug ts_price_dist pro_v15 (26 Jul)."""
    s = f"{v:.10f}".rstrip("0").rstrip(".")
    return s if s else "0"

def antihunt_adjust(side, entry, sl, ind):
    """Geser SL keluar zona sweep kolam stop terdekat (data bar tutup)."""
    if not AH_ON or ind is None:
        return sl, None
    try:
        hi = ind["high"][:-1]
        lo = ind["low"][:-1]
        i_last = len(ind["close"]) - 1
        atr = ind["atr"][i_last] if ind["atr"][i_last] == ind["atr"][i_last] else 0.0
        if atr <= 0:
            return sl, None
        n = len(lo)
        pv = AH_PIVOT
        dist0 = abs(entry - sl)
        if dist0 <= 0 or n < pv * 2 + 5:
            return sl, None
        best = None
        if side == "Buy":
            for i in range(max(pv, n - 80), n - pv):
                c = lo[i]
                if c >= entry:
                    continue
                if all(c < lo[j] for j in range(i - pv, i + pv + 1) if j != i):
                    if (c - AH_DEPTH_ATR * atr) < sl <= c + 0.1 * atr:
                        if best is None or c > best:
                            best = c
            if best is not None:
                new_sl = best - AH_DEPTH_ATR * atr
                if abs(entry - new_sl) <= dist0 * AH_MAX_WIDEN and new_sl < sl:
                    return new_sl, f"kolam stop @ {best:.6g}"
        else:
            for i in range(max(pv, n - 80), n - pv):
                c = hi[i]
                if c <= entry:
                    continue
                if all(c > hi[j] for j in range(i - pv, i + pv + 1) if j != i):
                    if c - 0.1 * atr <= sl < (c + AH_DEPTH_ATR * atr):
                        if best is None or c < best:
                            best = c
            if best is not None:
                new_sl = best + AH_DEPTH_ATR * atr
                if abs(new_sl - entry) <= dist0 * AH_MAX_WIDEN and new_sl > sl:
                    return new_sl, f"kolam stop @ {best:.6g}"
        return sl, None
    except Exception as e:
        log.error(f"antihunt: {e}")
        return sl, None

def stophunt_sl(side, entry, ind):
    """OPSI 2: SL langsung dari peta kolam stop — cari swing pool terdekat
    di sisi rugi, parkir SL di luar zona sweep (pool ± AH_DEPTH_ATR x ATR).
    Return sl atau None bila tak ada kolam layak (fallback ke indikator)."""
    try:
        hi = ind["high"][:-1]
        lo = ind["low"][:-1]
        i_last = len(ind["close"]) - 1
        atr = ind["atr"][i_last] if ind["atr"][i_last] == ind["atr"][i_last] else 0.0
        if atr <= 0:
            return None
        n = len(lo)
        pv = AH_PIVOT
        best = None
        if side == "Buy":
            for i in range(max(pv, n - 80), n - pv):
                c = lo[i]
                if c >= entry:
                    continue
                if all(c < lo[j] for j in range(i - pv, i + pv + 1) if j != i):
                    if best is None or c > best:      # kolam TERDEKAT di bawah
                        best = c
            if best is not None:
                sl = best - AH_DEPTH_ATR * atr
                # pagar: jarak SL 0.3%..6% dari entry (tolak yang absurd)
                d = (entry - sl) / entry
                if 0.003 <= d <= 0.06:
                    return sl
        else:
            for i in range(max(pv, n - 80), n - pv):
                c = hi[i]
                if c <= entry:
                    continue
                if all(c > hi[j] for j in range(i - pv, i + pv + 1) if j != i):
                    if best is None or c < best:
                        best = c
            if best is not None:
                sl = best + AH_DEPTH_ATR * atr
                d = (sl - entry) / entry
                if 0.003 <= d <= 0.06:
                    return sl
        return None
    except Exception as e:
        log.error(f"stophunt_sl: {e}")
        return None

def calc_sl(sigobj):
    """SL: MR = di luar band 3σ-ekuivalen (1.5x jarak band dari close);
    TC = seberang VWAP + 1 ATR."""
    c, atr = sigobj["close"], sigobj["atr"]
    if sigobj["kind"] == "MR":
        if sigobj["side"] == "Buy":
            return min(sigobj["lo2"], c) - max(atr * 0.5, c * 0.002)
        return max(sigobj["up2"], c) + max(atr * 0.5, c * 0.002)
    if sigobj["side"] == "Buy":
        return sigobj["vwap"] - max(atr, c * 0.003)
    return sigobj["vwap"] + max(atr, c * 0.003)

def smart_leverage(sym, entry, sl):
    """Leverage dari jarak SL (liq >= 35% di luar SL), diklem 3 lapis:
    (1) pagar per-coin LEV_CAP, (2) batas RESMI bursa (leverageFilter),
    (3) MIN dari bursa. Majors dgn SL lebar tetap bisa entry di 1-2x."""
    dist = abs(entry - sl) / entry if entry else 0.05
    if dist <= 0:
        dist = 0.05
    lev_aman = 1.0 / (dist * 1.35 + 0.006)   # liq >= 35% di luar SL (+MMR)
    cap_coin = LEV_CAP.get(sym, MAX_LEVERAGE)
    ex_min, ex_max = get_lev_limits(sym)
    hi = min(cap_coin, ex_max)
    lo = max(MIN_LEVERAGE, ex_min)
    return int(min(hi, max(lo, math.floor(lev_aman))))

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
        with open(path, "w") as f:
            json.dump(data, f, indent=1)
    except Exception:
        pass

def stats_record(stats, sym, kind, pnl):
    k = f"{sym}|{kind}"
    s = stats.setdefault(k, {"n": 0, "w": 0, "pnl": 0.0})
    s["n"] += 1
    s["pnl"] = round(s["pnl"] + pnl, 4)
    if pnl > 0:
        s["w"] += 1
    save_json(STATS_FILE, stats)

def new_sym_state():
    return {"in_position": False, "side": None, "entry": 0.0, "sl": 0.0,
            "tp": 0.0, "kind": None, "margin_used": 0.0, "lev": 0, "risk0": 0.0, "ah": False,
            "riding": False, "peak": 0.0, "mfe_r": 0.0,
            "be_done": False, "trail_on": False, "last_exit": 0.0,
            "pos_miss": 0, "last_pnl": None, "longDl": -1, "shortDl": -1,
            "last_bar": 0}

# ===== PEREKAM MFE (11 Agu — murni PASIF, nol efek keputusan) =====
# Menjawab keluhan user "TP belum kena sudah balik arah" dgn DATA:
# tiap trade dicatat puncak profit tertinggi (dlm R & % jarak ke TP)
# yang SEMPAT diraih sebelum ditutup. Audit 30 trade menjawab sendiri
# apakah TP perlu didekatkan / partial TP dibuka sbg fase resmi.
MFE_FILE = "vwap_mfe.json"
MFE_LOG = load_json(MFE_FILE, [])   # FIX 15 Agu: dimuat ulang saat start —
# dulu selalu [] -> tiap RESTART sejarah MFE terhapus (file cuma 3 record
# padahal ZF sudah 19 trade). Data audit TP/TS kini selamat dari restart.
if not isinstance(MFE_LOG, list):
    MFE_LOG = []

def mfe_record(sym, s, pnl):
    try:
        tp_dist = abs(s.get("tp", 0) - s.get("entry", 0))
        risk0 = s.get("risk0") or 0
        peak_r = s.get("mfe_r", 0.0)
        peak_tp_pct = 0.0
        if tp_dist > 0 and risk0 > 0:
            peak_tp_pct = min(100.0, peak_r * risk0 / tp_dist * 100.0)
        MFE_LOG.append({"t": wib_now().strftime("%Y-%m-%d %H:%M"),
                        "sym": sym, "kind": s.get("kind"),
                        "side": s.get("side"), "pnl": round(pnl, 4),
                        "mfe_r": round(peak_r, 2),
                        "mfe_tp_pct": round(peak_tp_pct, 1)})
        save_json(MFE_FILE, MFE_LOG[-500:])
    except Exception:
        pass

def manage(sym, s, ind):
    p = get_position(sym)
    if s["in_position"] and not p:
        s["pos_miss"] += 1
        if s["pos_miss"] < 2:
            return
        px = get_price(sym) or s["entry"]
        d = 1 if s["side"] == "Buy" else -1
        pnl = (s["margin_used"] * s["lev"] * d * (px - s["entry"]) / s["entry"]
               if s["entry"] else 0.0)
        lp = s.get("last_pnl")
        if lp is not None and abs(lp) < s["margin_used"] * s["lev"] * 0.5:
            pnl = lp
        stats_record(STATS, sym, s.get("kind") or "?", pnl)
        day_record(pnl)
        mfe_record(sym, s, pnl)     # rekam puncak profit (pasif)
        roi = pnl / s["margin_used"] * 100 if s["margin_used"] else 0
        add_log(f"{G if pnl>=0 else R}■ {sym} {s.get('kind')} ditutup — PnL {pnl:+.2f}$ (ROI {roi:+.1f}%){X}")
        send_tg(f"*VWAP BOT HASIL*\n{'🟢' if pnl>0 else '🔴'} #{sym} {s.get('kind')} "
                f"{s['side']} → *{pnl:+.2f}$* (ROI {roi:+.1f}%)")
        base = new_sym_state()
        base["last_exit"] = time.time()
        s.clear(); s.update(base)
        save_json(STATE_FILE, STATES)
        return
    if not p:
        return
    s["pos_miss"] = 0
    s["last_pnl"] = p["pnl"]
    i = len(ind["close"]) - 1
    atr = ind["atr"][i] if ind["atr"][i] == ind["atr"][i] else 0.0
    px = ind["close"][i]
    if not s["in_position"]:               # adopsi ringan (restart)
        # FIX (8 Agu, kasus ETHUSDT [None] & BSB RR 43R): risk0 adopsi
        # JANGAN dari |entry-sl| bursa — SL bisa 0 (telanjang) atau sudah
        # di BE (risk0 mikroskopis -> RR meledak, TS/BE kacau).
        # Fallback sehat: 1.5xATR sbg risiko acuan.
        _sl_b = p["sl"] or 0.0
        _r0 = abs(p["entry"] - _sl_b) if _sl_b else 0.0
        if _r0 <= 0 or (atr > 0 and _r0 < atr * 0.30):
            _r0 = (atr * 1.5) if atr > 0 else p["entry"] * 0.02
        s.update({"in_position": True, "side": p["side"], "entry": p["entry"],
                  "sl": _sl_b, "tp": p["tp"], "lev": p["lev"] or 1,
                  "kind": s.get("kind") or "ADOPT",
                  "risk0": s.get("risk0") or _r0,
                  "margin_used": s["margin_used"] or (p["size"] * p["entry"] / max(p["lev"], 1))})
        add_log(f"{Y}👁 {sym} posisi diadopsi (restart) — risk0 {_r0:.6g}{X}")
    # ===== GUARD POSISI TELANJANG (8 Agu, kasus ETHUSDT SL 0 TP 0): =====
    # posisi tanpa SL di bursa = bahaya maksimal -> pasang ulang otomatis
    if not p["sl"] and s["entry"] and atr > 0 and not s.get("trail_on"):
        try:
            _sl_new = (s["entry"] - atr * 1.5 if s["side"] == "Buy"
                       else s["entry"] + atr * 1.5)
            # KLEM (fix 10001 TUTUSDT 9 Agu): harga bisa lari jauh dari
            # entry — SL wajib valid thd harga TERKINI. Kalau SL rencana
            # sudah di sisi salah, geser ke 1.5xATR dari harga sekarang.
            _px_now = get_price(sym) or px
            if s["side"] == "Buy" and _sl_new >= _px_now:
                _sl_new = _px_now - atr * 1.5
            elif s["side"] == "Sell" and _sl_new <= _px_now:
                _sl_new = _px_now + atr * 1.5
            _ok = _sl_new < _px_now if s["side"] == "Buy" else _sl_new > _px_now
            if _ok:
                session.set_trading_stop(category="linear", symbol=sym,
                                         stopLoss=fmt_px(_sl_new), positionIdx=0)
                s["sl"] = _sl_new
                add_log(f"{R}🚨 {sym} POSISI TANPA SL! Dipasang ulang @ "
                        f"{_sl_new:.6g} (1.5xATR){X}")
        except Exception as e:
            log.error(f"naked guard {sym}: {e}")
    # --- BE & trailing ---
    # FIX (7 Agu): R dihitung dari RISIKO AWAL (risk0). Dulu pakai SL
    # berjalan -> setelah BE, risk menyusut ke ~0 -> r_now meledak 18R
    # -> trailing aktif prematur di 1R. Persis kelas bug pro_v15 dulu.
    risk = s.get("risk0") or (abs(s["entry"] - s["sl"]) if s["sl"] else 0)
    if risk <= 0 or not s["entry"]:
        return
    profit = (px - s["entry"]) if s["side"] == "Buy" else (s["entry"] - px)
    r_now = profit / risk
    if r_now > s.get("mfe_r", 0.0):     # rekam puncak (pasif, utk audit MFE)
        s["mfe_r"] = r_now
    try:
        if not s["be_done"] and r_now >= BE_AT_R:
            be = be_price(s["entry"], s["side"])   # fee + slippage 2 sisi
            ok = be < px if s["side"] == "Buy" else be > px
            if ok:
                session.set_trading_stop(category="linear", symbol=sym,
                                         stopLoss=fmt_px(be), positionIdx=0)
                s["sl"], s["be_done"] = be, True
                add_log(f"{G}🔒 {sym} BE terpasang @ {be:.6g} ({r_now:.2f}R){X}")
        if not s["trail_on"] and r_now >= TRAIL_AT_R and atr > 0:
            dist = atr * TRAIL_ATR_MULT
            session.set_trading_stop(category="linear", symbol=sym,
                                     trailingStop=fmt_px(dist), positionIdx=0)
            s["trail_on"] = True
            add_log(f"{M}⚡ {sym} trailing aktif @ {r_now:.2f}R{X}")

        # ===== SMART RIDE MAX =====
        if RIDE_ON and not s["riding"] and s["tp"] and s["entry"]:
            span = abs(s["tp"] - s["entry"])
            reach = (px - s["entry"]) if s["side"] == "Buy" else (s["entry"] - px)
            if span > 0 and reach / span >= RIDE_TRIGGER:
                # momentum masih searah? (harga di sisi benar VWAP + ctx tak melawan)
                i2 = len(ind["close"]) - 2
                vw = ind["vwap"][i2] if ind["vwap"][i2] == ind["vwap"][i2] else 0.0
                ctx2 = int(ind["ctx"][i2])
                mom_ok = ((s["side"] == "Buy" and px > vw and ctx2 >= 0) or
                          (s["side"] == "Sell" and px < vw and ctx2 <= 0)) if vw else False
                if mom_ok and atr > 0:
                    lock = max(reach * RIDE_LOCK_PCT, 0.0)
                    bepx = be_price(s["entry"], s["side"])
                    floor_px = (max(s["entry"] + lock, bepx)
                                if s["side"] == "Buy"
                                else min(s["entry"] - lock, bepx))
                    # lantai wajib di sisi benar dari harga (anti-10001)
                    valid = floor_px < px if s["side"] == "Buy" else floor_px > px
                    if valid:
                        session.set_trading_stop(
                            category="linear", symbol=sym, takeProfit="0",
                            trailingStop=fmt_px(atr * RIDE_TRAIL_ATR),
                            stopLoss=fmt_px(floor_px), positionIdx=0)
                        s.update({"riding": True, "trail_on": True,
                                  "sl": floor_px, "peak": reach})
                        add_log(f"{G}🚀 {sym} RIDE MAX! TP dilepas — lantai "
                                f"{RIDE_LOCK_PCT*100:.0f}% profit @ {floor_px:.6g} "
                                f"+ trailing rapat{X}")
                else:
                    # momentum melemah dekat TP -> biarkan TP dieksekusi normal
                    pass
        elif s["riding"]:
            # RATCHET: lantai naik mengikuti puncak profit baru (tak pernah turun)
            reach_now = (px - s["entry"]) if s["side"] == "Buy" else (s["entry"] - px)
            if reach_now > s.get("peak", 0.0):
                s["peak"] = reach_now
                lock = reach_now * RIDE_LOCK_PCT
                cand = (s["entry"] + lock if s["side"] == "Buy"
                        else s["entry"] - lock)
                better = (cand > s["sl"] + atr * 0.05 if s["side"] == "Buy"
                          else cand < s["sl"] - atr * 0.05)
                valid = cand < px if s["side"] == "Buy" else cand > px
                if better and valid:
                    session.set_trading_stop(category="linear", symbol=sym,
                                             stopLoss=fmt_px(cand), positionIdx=0)
                    s["sl"] = cand
                    add_log(f"{G}🚀 {sym} RIDE ratchet — lantai naik ke "
                            f"{cand:.6g} ({RIDE_LOCK_PCT*100:.0f}% dr puncak){X}")
    except Exception as e:
        log.error(f"manage {sym}: {e}")
    save_json(STATE_FILE, STATES)

def try_entry(sym, s, sigobj, balance, n_open, ind=None):
    if s["in_position"]:
        return
    if sym in SYM_BLACKLIST:
        return
    if time.time() - s.get("last_exit", 0) < COOLDOWN_MIN * 60:
        return
    n_open_now = sum(1 for s2 in STATES.values() if s2.get("in_position"))
    if n_open_now >= MAX_POSITIONS:
        add_log(f"{Y}⊘ {sym} slot penuh ({n_open_now}/{MAX_POSITIONS}) — sinyal dilewati{X}")
        return
    if TIME_GUARD_ON and wib_now().hour in TIME_GUARD_HOURS:
        add_log(f"{Y}🌙 {sym} TIME GUARD 00-04 WIB — sinyal {sigobj['kind']} dilewati{X}")
        return
    if news_active():
        add_log(f"{R}🚨 {sym} entry ditunda — NEWS SHOCK ({_news['reason']}), "
                f"sisa {max(0, (_news['until']-time.time())/60):.0f}m{X}")
        return
    _cpi, _cpi_ket = cpi_guard_active()
    if _cpi:
        add_log(f"{R}📰 {sym} entry diblokir — {_cpi_ket}{X}")
        return
    if VOL_FILTER and ind is not None:
        try:
            _atrs = [a for a in ind["atr"][-51:-1] if a == a]
            _anow = ind["atr"][len(ind["close"]) - 2]
            if _atrs and _anow == _anow:
                _ratio = _anow / (sum(_atrs) / len(_atrs))
                if _ratio > VOL_THRESHOLD:
                    add_log(f"{R}⛔ {sym} volatilitas ekstrem (ATR {_ratio:.1f}x "
                            f"> {VOL_THRESHOLD}x) — entry dilewati{X}")
                    return
        except Exception:
            pass
    px = get_price(sym)
    if not px:
        return
    _ah_used = False
    if sigobj.get("sl") is not None and sigobj["kind"] in ("ZF", "OB"):
        # MODE 3/4: SL bawaan resep (ekor sweep / bawah kotak OB) —
        # tetap dikoreksi anti-hunt bila jatuh di zona sweep kolam.
        sl = sigobj["sl"]
        sl2, ah_info = antihunt_adjust(sigobj["side"], px, sl, ind)
        if ah_info:
            sl = sl2; _ah_used = True
            add_log(f"{C}🛡🎣 {sym} SL ANTI-HUNT — {ah_info}: SL keluar zona sweep{X}")
    elif RISK_MODE_ACTIVE == 2:
        # OPSI 2: SL langsung dari kolam stop; indikator jadi cadangan
        sl = stophunt_sl(sigobj["side"], px, ind)
        if sl is not None:
            _ah_used = True
            add_log(f"{C}🛡🎣 {sym} SL STOP-HUNT (opsi 2) @ {sl:.6g} — di luar "
                    f"zona sweep kolam terdekat{X}")
        else:
            sl = calc_sl(sigobj)
            add_log(f"{D}{sym} tak ada kolam layak — SL indikator dipakai{X}")
    else:
        # OPSI 1: SL indikator + koreksi anti-hunt bila perlu
        sl = calc_sl(sigobj)
        sl, ah_info = antihunt_adjust(sigobj["side"], px, sl, ind)
        _ah_used = bool(ah_info)
        if ah_info:
            add_log(f"{C}🛡🎣 {sym} SL ANTI-HUNT — {ah_info}: SL keluar zona sweep{X}")
    tp = sigobj["target"]
    side = sigobj["side"]
    if (side == "Buy" and (sl >= px or tp <= px)) or \
       (side == "Sell" and (sl <= px or tp >= px)):
        log.info(f"⊘ {sym} level tidak valid (px {px:.6g} sl {sl:.6g} tp {tp:.6g})")
        return
    # ANTI-FEE (8 Agu, kasus ETHUSDT MR: TP 0.087% < fee RT 0.11% ->
    # menang pun dimakan fee): jarak TP wajib >= 2x fee round-trip.
    tp_pct = abs(tp - px) / px * 100
    _min_tp = (FEE_RT_PCT + 2 * SLIP_PCT) * 2      # 2x (fee+slippage RT)
    if tp_pct < _min_tp:
        add_log(f"{Y}⊘ {sym} TP terlalu dekat ({tp_pct:.3f}% < {_min_tp:.2f}% "
                f"= 2x fee+slippage) — sinyal dilewati, tak layak biaya{X}")
        return
    lev = smart_leverage(sym, px, sl)
    sl_pct = abs(px - sl) / px * 100
    margin = ENTRY_MARGIN
    cap = (RISK_CAP_USD if RISK_MODE_ACTIVE == 1
           else max(0.30, balance * RISK_PCT_BAL / 100.0))   # smart saldo (min $0.30)
    # DOSIS MINI (11 Agu): plafon rugi absolut, apapun mode/saldo
    cap = min(cap, RISK_HARD_USD)
    risk_usd = margin * lev * sl_pct / 100
    if risk_usd > cap:
        margin = round(cap / (lev * sl_pct / 100), 2)
        add_log(f"{C}🧯 {sym} RISK CAP ${cap:.2f} — risiko ${risk_usd:.2f} → margin ${margin:.2f}{X}")
    # PLAFON MARGIN (fix XLMUSDT $9/79%-saldo 9 Agu): satu posisi tidak
    # boleh menyedot lebih dari MARGIN_MAX_PCT% saldo — SL super-ketat
    # tak lagi bisa meledakkan ukuran posisi.
    _mcap = balance * MARGIN_MAX_PCT / 100.0
    if margin > _mcap:
        add_log(f"{Y}🧯 {sym} margin ${margin:.2f} > plafon {MARGIN_MAX_PCT:g}% saldo "
                f"(${_mcap:.2f}) — dipangkas{X}")
        margin = round(_mcap, 2)
    min_qty, step = get_lot_filter(sym)
    qty = max(min_qty, math.floor((margin * lev / px) / step) * step)
    qty = round(qty, 8)
    # GUARD MIN-QTY (13 Agu, temuan USER: BTC dosis mini dibulatkan NAIK
    # ke 0.001 BTC -> notional 2x rencana -> risiko riil $0.53 > cap $0.30
    # + dashboard % ngaco). Risiko dihitung dari QTY FINAL; kalau jebol
    # cap >20%, sinyal dilewati — coin ini terlalu "kasar" utk dosis mini.
    real_risk = qty * abs(px - sl)
    if real_risk > cap * 1.2:
        add_log(f"{Y}⊘ {sym} min-qty bursa memaksa risiko ${real_risk:.2f} "
                f"> cap ${cap:.2f} — sinyal dilewati (kontrak terlalu besar "
                f"utk dosis){X}")
        return
    # FIX 110094 (12 Agu): Bybit menolak order bernilai < $5. Dosis mini
    # sering memangkas margin sampai nilai order di bawah ambang → dulu
    # ERROR berisik (TUT/CAP/BMT), kini dilewati dgn log rapi.
    if qty * px < 5.0:
        add_log(f"{Y}⊘ {sym} nilai order ${qty*px:.2f} < min $5 Bybit — "
                f"sinyal dilewati (dosis terlalu kecil utk kontrak ini){X}")
        return
    # PRE-CHECK SALDO TERSEDIA (fix spam 110007): pakai availableBalance
    # (saldo dikurangi margin posisi aktif), BUKAN equity total.
    _avail = get_available()
    _need = (qty * px) / lev
    if _avail is not None and _need > _avail * 0.9:
        add_log(f"{Y}⊘ {sym} margin tersedia kurang (butuh ${_need:.2f}, "
                f"tersedia ${_avail:.2f}) — order tidak dikirim{X}")
        return
    if (qty * px) / lev > balance * 0.9:
        add_log(f"{Y}⊘ {sym} saldo tidak cukup{X}")
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
        fill = p["entry"] or px
        # FIX % DASHBOARD (13 Agu, temuan USER): margin dicatat dari QTY
        # FINAL yang benar-benar terpasang di bursa (min-qty/step bisa
        # membulatkan) — ROI & bar TP kini sinkron dgn Bybit.
        margin = round((p["size"] * fill) / max(lev, 1), 4) or margin
        session.set_trading_stop(category="linear", symbol=sym,
                                 stopLoss=fmt_px(sl),
                                 takeProfit=fmt_px(tp),
                                 slTriggerBy="LastPrice", tpTriggerBy="LastPrice",
                                 positionIdx=0)
        s.update({"in_position": True, "side": side, "entry": fill, "sl": sl,
                  "tp": tp, "kind": sigobj["kind"], "margin_used": margin,
                  "lev": lev, "be_done": False, "trail_on": False,
                  "ah": _ah_used,
                  "risk0": abs(fill - sl)})   # risiko AWAL (baku utk hitung R)
        save_json(STATE_FILE, STATES)
        arrow = "▲ LONG" if side == "Buy" else "▼ SHORT"
        add_log(f"{G if side=='Buy' else R}{arrow}{X} {B}{sym}{X} [{sigobj['kind']}] @ {fill:.6g} {lev}x TP {tp:.6g} SL {sl:.6g} m ${margin}")
        send_tg(f"*VWAP BOT SIGNAL*\n{'🟢 LONG' if side=='Buy' else '🔴 SHORT'} "
                f"#{sym} {lev}x — sinyal *{sigobj['kind']}* "
                f"({'mean-reversion' if sigobj['kind']=='MR' else 'trend-continuation'})\n"
                f"Entry : `{fill:.6g}`\nSL    : `{sl:.6g}`\nTP    : `{tp:.6g}`")
    except Exception as e:
        log.error(f"✘ {sym} gagal entry: {e}")
        s["last_exit"] = time.time()       # jeda agar tidak spam
        # BLACKLIST simbol yang butuh persetujuan khusus (fix CLUSDT
        # 110125 Crude Oil terms 10 Agu) — jangan dicoba lagi sesi ini.
        if "110125" in str(e) or "must agree" in str(e).lower():
            SYM_BLACKLIST.add(sym)
            add_log(f"{R}⛔ {sym} butuh persetujuan khusus di Bybit — "
                    f"di-blacklist sesi ini{X}")

# ==================== LOOP UTAMA ====================
STATES = {}
STATS = {}
DAYSTATS = {"date": "", "n": 0, "w": 0, "pnl": 0.0}

def day_record(pnl):
    today = wib_now().strftime("%Y-%m-%d")
    if DAYSTATS["date"] != today:
        DAYSTATS.update({"date": today, "n": 0, "w": 0, "pnl": 0.0})
    DAYSTATS["n"] += 1
    DAYSTATS["pnl"] = round(DAYSTATS["pnl"] + pnl, 4)
    if pnl > 0:
        DAYSTATS["w"] += 1

_sym_last_refresh = {"t": 0.0}

def refresh_symbols():
    """Tarik semua kontrak linear-USDT layak dari Bybit (turnover >= min)."""
    global SYMBOLS
    if not DYN_SYMBOLS:
        return
    if time.time() - _sym_last_refresh["t"] < SYM_REFRESH_H * 3600:
        return
    try:
        r = session.get_tickers(category="linear")
        rows = r["result"]["list"]
        pool = []
        for t_ in rows:
            sym = t_.get("symbol", "")
            if not sym.endswith("USDT") or "-" in sym:
                continue
            try:
                turn = float(t_.get("turnover24h") or 0)
            except (TypeError, ValueError):
                continue
            if turn >= SYM_MIN_TURN:
                pool.append((turn, sym))
        pool.sort(reverse=True)
        new_syms = list(CORE_SYMBOLS)
        for _, sym in pool:
            if sym not in new_syms:
                new_syms.append(sym)
            if len(new_syms) >= SYM_MAX_N:
                break
        added = len([s_ for s_ in new_syms if s_ not in SYMBOLS])
        SYMBOLS = new_syms
        for sym in SYMBOLS:
            if sym not in STATES:
                STATES[sym] = new_sym_state()
        _sym_last_refresh["t"] = time.time()
        add_log(f"🌐 SYMBOLS diperbarui: {len(SYMBOLS)} kontrak "
                f"(+{added} baru, turnover ≥ ${SYM_MIN_TURN/1e6:.0f}jt)")
    except Exception as e:
        log.error(f"refresh_symbols: {e}")

RISK_MODE_ACTIVE = 1

def pilih_mode():
    """Menu 2 opsi sebelum start (dilewati bila RISK_MODE=1/2 di konfig)."""
    global RISK_MODE_ACTIVE
    if RISK_MODE in (1, 2):
        RISK_MODE_ACTIVE = RISK_MODE
        return
    print(f"\n{C}╔══════════════ PILIH MODE STRATEGI ═════════════╗{X}")
    print(f"{C}║{X} {G}[1]{X} KLASIK   : GBB, SL indikator + anti-hunt    {C}║{X}")
    print(f"{C}║{X} {Y}[2]{X} STOPHUNT : GBB, SL di luar kolam stop        {C}║{X}")
    print(f"{C}║{X} {M}[3]{X} ZF+SMC   : Sweep likuiditas + momentum RR2  {C}║{X}")
    print(f"{C}║{X} {B}[4]{X} PURE-OB  : Order Block + FVG RR2            {C}║{X}")
    print(f"{C}║{X}  ⚠ rugi maks SEMUA mode dipatok ${RISK_HARD_USD:.2f}/trade   {C}║{X}")
    print(f"{C}║{X}  ⚠ 1 mode = 1 eksperimen — JANGAN campur data  {C}║{X}")
    print(f"{C}╚════════════════════════════════════════════════╝{X}")
    try:
        pilih = input("Pilihan [1/2/3/4] (default 2): ").strip()
    except EOFError:
        pilih = "2"                       # non-interaktif (tmux detach dsb)
    RISK_MODE_ACTIVE = int(pilih) if pilih in ("1", "2", "3", "4") else 2
    nama = {1: "1 KLASIK", 2: "2 STOPHUNT", 3: "3 ZF+SMC", 4: "4 PURE-OB"}
    print(f"Mode {nama[RISK_MODE_ACTIVE]} dipilih.\n")
    time.sleep(1)

def run():
    global STATES, STATS
    pilih_mode()
    STATES = load_json(STATE_FILE, {})
    STATS = load_json(STATS_FILE, {})
    for sym in SYMBOLS:
        base = new_sym_state()
        base.update({k: v for k, v in STATES.get(sym, {}).items() if k in base})
        STATES[sym] = base
    bal = get_balance()
    log.info(f"▶ VWAP BOT dimulai — saldo ${bal:,.2f} | {ANCHOR_MODE} anchor | "
             f"TF {INTERVAL}m | {len(SYMBOLS)} simbol | cap ${RISK_CAP_USD}")
    log.info("⚠ CATATAN JUJUR: backtest pembuat indikator = NOL sebagai sistem "
             "tunggal. Bot ini uji coba sadar-risiko dgn risk cap ketat.")
    regimes = {}
    scan_idx = 0
    while True:
        try:
            refresh_symbols()
            news_shock_check()
            bal = get_balance()
            n_open = sum(1 for s in STATES.values() if s["in_position"])
            # ===== ROTASI BATCH: posisi aktif + core SETIAP siklus; sisanya
            # bergilir SCAN_BATCH per siklus (adil & hemat rate-limit) =====
            # posisi aktif dari STATES (bukan SYMBOLS) — coin yang keluar
            # daftar dinamis tetap dikawal sampai posisinya selesai
            actives = [s2 for s2, st2 in STATES.items() if st2.get("in_position")]
            rest = [s2 for s2 in SYMBOLS if s2 not in actives and s2 not in CORE_SYMBOLS]
            batch = list(dict.fromkeys(
                actives + CORE_SYMBOLS +
                [rest[(scan_idx + k) % len(rest)] for k in range(min(SCAN_BATCH, len(rest)))]
                if rest else actives + CORE_SYMBOLS))
            scan_idx = (scan_idx + SCAN_BATCH) % max(1, len(rest))
            _t_batch = time.time()
            _rest_n = max(len(SYMBOLS) - len(CORE_SYMBOLS), 1)
            SCAN["sweep_total"] = _rest_n
            SCAN["sweep_done"] = min(scan_idx if scan_idx > 0 else _rest_n, _rest_n)
            for _bi, sym in enumerate(batch):
                SCAN.update({"sym": sym, "idx": _bi + 1, "total": len(batch),
                             "cycle_t": time.time() - _t_batch})
                if _bi % 4 == 0:                     # refresh layar tiap 4 simbol
                    render_dash(bal, regimes)
                s = STATES.setdefault(sym, new_sym_state())
                df = get_kline(sym, INTERVAL, 500)
                if df.empty or len(df) < REGIME_LEN + KER_LEN + 10:
                    continue
                ind = compute_indicator(df)
                if ind is None:
                    continue
                _rg = ind["regime"][len(ind["close"]) - 2]
                regimes[sym] = ("TRENDING" if _rg in (2, 3) else
                                "RANGING" if _rg in (0, 1) else "WARMUP")
                _i2 = len(ind["close"]) - 2
                MKT[sym] = {
                    "px": float(ind["close"][-1]),
                    "vwap": float(ind["vwap"][_i2]) if ind["vwap"][_i2] == ind["vwap"][_i2] else 0.0,
                    "up2": float(ind["up2"][_i2]) if ind["up2"][_i2] == ind["up2"][_i2] else 0.0,
                    "lo2": float(ind["lo2"][_i2]) if ind["lo2"][_i2] == ind["lo2"][_i2] else 0.0,
                    "ctx": int(ind["ctx"][_i2]),
                    "bar_end": (int(df["ts"].iloc[-1]) / 1000) + int(INTERVAL) * 60,
                }
                manage(sym, s, ind)
                # sinyal hanya dievaluasi SEKALI per bar tutup
                bar_ts = int(df["ts"].iloc[-2])
                if bar_ts != s.get("last_bar"):
                    s["last_bar"] = bar_ts
                    if RISK_MODE_ACTIVE == 3:
                        sig = read_signal_zfsmc(df, s)
                    elif RISK_MODE_ACTIVE == 4:
                        sig = read_signal_pureob(df, s)
                    else:
                        sig = read_signal(ind, s)
                    if sig:
                        rg = ind["regime"][sig["bar_i"]]
                        extra = ""
                        if SWING_INFO and ANCHOR_MODE != "Swing":
                            ind_s = compute_indicator(df, mode="Swing")
                            if ind_s:
                                vs = ind_s["vwap"][sig["bar_i"]]
                                if vs == vs:
                                    side_s = "atas" if sig["close"] > vs else "bawah"
                                    setuju = ((sig["side"] == "Buy" and side_s == "atas")
                                              or (sig["side"] == "Sell" and side_s == "bawah"))
                                    extra = (f" | swingVWAP {vs:.6g} ({side_s}"
                                             f"{', searah ✔' if setuju else ', beda sisi ⚠'})")
                        add_log(f"◈ {B}{sym}{X} sinyal {Y}{sig['kind']}{X} {sig['side']} @ {sig['close']:.6g}{extra}")
                        try_entry(sym, s, sig, bal, n_open, ind)
                    save_json(STATE_FILE, STATES)
                time.sleep(0.15)
            SCAN["idle_until"] = time.time() + 30
            render_dash(bal, regimes)
            # REAL-TIME (14 Agu, permintaan user): refresh tiap 1 dtk saat
            # idle — harga posisi dari cache 2 dtk => beban API tetap
            # ~0.5 req/dtk per posisi (limit publik Bybit 600 req/5dtk,
            # jauh dari rate limit). Layar hidup, tanpa kedip (anti-flicker
            # \033[H + \033[K sudah ada di render_dash).
            for _ in range(30):
                time.sleep(1)
                render_dash(bal, regimes)
        except KeyboardInterrupt:
            print("\033[?25h\n▪ VWAP bot dihentikan.")
            break
        except Exception as e:
            log.error(f"loop: {e}")
            time.sleep(10)

if __name__ == "__main__":
    run()
