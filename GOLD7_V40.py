# ============================================================================
#  GOLDEN EDGE SUITE — BYBIT BOT  [Power Of Trading]   v1.40 (8 Sep 2026)
#   ► v1.34: TITIK ENTRY DIPERBAIKI — R1b flip dlm 3 bar · R2 cukup sentuh zona ·
#     zona min 4.0 (menu 1=6.5/2=5.5/3=4.0) · diag R2 hitung zona SEARAH saja.
#   ► v1.35: DOJI (menu 7) — BUG bar LIVE diperbaiki (doji = bar CLOSED i=len-2,
#     sebelumnya i=len-1 = bar berjalan -> syarat touch mustahil, 0 entry) ·
#     klasifikasi 4 TIPE: DRAGONFLY→BUY · GRAVESTONE→SELL · LONG-LEGGED/NEAR→
#     aturan video (sweep) · range 0.7xATR utk T/⊥ · diag & log tampilkan tipe.
#   ► v1.36: GATE + baris RESEP GOLDEN ZONE — posisi harga vs GZ (0.618-0.786)
#     per TF 15m/1H/4H + skor N/4 + bias arah (>=2 TF ABOVE → SHORT-bias,
#     >=2 TF BELOW → LONG-bias). HANYA tampilan — logika entry tidak berubah.
#   ► v1.37: GZ menampilkan sisi momentum (▲BULL/▼BEAR) · header & baris Aturan
#     memakai ambang zona EFEKTIF varian (E=5.5 · C/F=8.0) · legend GZ 1 baris.
#   ► v1.38: VARIAN G (menu G) — GZ-STOPPOOL: SHORT saat harga DI ATAS Golden
#     Zone (15m > 0.786) & SUDAH menyentuh STOP POOL di atas; LONG saat DI BAWAH
#     GZ (15m < 0.618) & sentuh STOP POOL di bawah. SL sisi luar zona · TP zona
#     lawan · RR >= 1.2. Berlaku SEMUA akun (DEMO & REAL).
#   ► v1.39: tampilan GZ di GATE DIHAPUS (panel kembali ringkas utk posisi) ·
#     mesin ZIGZAG scenario (trig/rev/ret/tgt/ext) di-port ke Python ·
#     VARIAN F = F-SMART (SL sisi luar TRIGGER · TP = TARGET · TP2 = EXTENSION) ·
#     VARIAN G ikut memakai TARGET zigzag bila searah & lebih dekat.
#   ► v1.40: VARIAN H = G-AMAN — seperti G (GZ-STOPPOOL) + syarat 1H WAJIB
#     searah arah entry: regime 1H = BULL TREND utk LONG · BEAR TREND utk
#     SHORT · ROTATION/data kurang = SKIP (demi keamanan, anti melawan tren).
#   ► WATCHDOG v1.33 = SELURUH universe, tampil maks WD_SHOW_MAX (10),
#     scan TETAP semua coin. PANEL TIDAK BEKU: error 1 simbol TIDAK
#     mematikan siklus (try/except per simbol + alasannya tampil).
#     Universe TIDAK turun ke 1 simbol saat get_tickers gagal sesaat.
#   ► Juga: WATCHDOG = cache antar-siklus (bukan hanya giliran scan kali ini);
#     simbol gagal data TETAP tampil + alasannya.
#  ► MENU 7 DIPERLUAS (XAUUSDT): pilih METODE dulu, lalu akun DEMO/REAL:
#      1 = DOJI 3m      (video ThisIsDaryl, seperti biasa)
#      2 = DOJI 30m     (doji breakout pada 30m)
#      3 = DOJI MTF 30m+60m (BARU): doji 30m + BIAS struktur 60m
#          (arah doji wajib searah tren 60m; melawan = SKIP + alasan).
#    Non-tty: GE_DOJI_M=1|2|3 (default 1). Pine TradingView-nya:
#    GOLDEN_EDGE_DOJI_TV.pine (baru) & GOLDEN_EDGE_FIB_TV.pine v3 (visual fix).
#  ► MENU 8 DIPERLUAS (XAUUSDT): pilih METODE dulu, lalu akun DEMO/REAL:
#      1 = FIB 30m        (struktur + zona fib di 30m — video 'Keep It Simple')
#      2 = FIB MTF 30m+60m (BARU): tren & zona fib 50-61.8% dari 60m,
#          konfirmasi struktur + timing mantul dari 30m; SL luar swing 60m.
#    Non-tty: GE_FIB_M=1|2 (default 1). Pine TradingView-nya: GOLDEN_EDGE_FIB_TV.pine.
#  ► AUDIT v1.33 — ALL COIN (menu 1): sema USDT perp terdeteksi otomatis
#    (linear, turnover24h > 0, urut turnover turun); menu 1 = turnover >= $5jt,
#    menu 2 = TOP 30 turnover tertinggi (+ XAUUSDT selalu ikut). FIX:
#    * SCAN CHUNK KINI DINAMIS (rotasi penuh <= ~8 siklus) — dulu 12 tetap:
#      di ALL COIN (ratusan simbol) satu simbol baru dicek tiap 15-25 mnt,
#      sering meleset dari bar 15m (flip R3) → 'belum pernah entry'.
#    * sleep antar-simbol 0.5s -> 0.25s; warning bila universe kosong.
#    Logika R1/R2/R3/RR & varians TIDAK berubah.
#  ► MENU 5 (TESTNET/DEMO) DIHAPUS — digabung ke MENU 4: di menu 4 kini
#    pilih pasar (1-3) + varian (A-H) + AKUN (1=DEMO / 2=REAL, wajib YES).
#    Ketik 5 di menu = otomatis diarahkan ke menu 4.
#  ► PANEL GATE BARU (diagnosa “kenapa belum pernah entry”): setiap simbol
#    menampilkan alasan gate terakhir (R1 GAGAL / R2 GAGAL / R3 GAGAL / RR)
#    di dashboard PRO & standalone, jadi terlihat jelas aturan mana yg
#    menahan sinyal (semua mode 1-4/6 pakai aturan video + Pine, 7/8 juga).
#  ► SEMUA MODE PILIH AKUN: mode 1-6 kini TANYA akun (1=DEMO, 2=AKUN REAL,
#    REAL wajib ketik YES) sebelum jalan — sama seperti 7/8. Sesi DEMO/TESTNET
#    dibangun GEHTTP (endpoint terkunci) lalu DIKAT ke session global, jadi
#    dashboard & menu 5 memakai kunci segar multi-lokasi (_fresh_*_key).
#  ► WATCHDOG CLONE DIPERBAIKI: dulu, bila universe kecil (mis. 2 coin),
#    pengisi scan round-robin mengulang simbol yg sama (XAUUSDT x 11) sehingga
#    tampak '12 coin kembar' di SEMUA mode PRO (1-6, real & demo - bug lama
#    yg sama, bukan akibat menu 5/7/8). Kini take di-cap len(rest) + WATCHDOG
#    dedupe per simbol: TIDAK PERNAH ada baris kembar lagi.
#  ► MENU 5 (TESTNET/DEMO) SALDO 0 DIPERBAIKI: sesi demo/testnet kini memakai
#    _fresh_demo_key()/_fresh_testnet_key() (cari ge_keys.json multi-lokasi,
#    SAMA seperti menu 7/8 yang sudah terbukti) - bukan DEMO_API_KEY modul
#    yang hanya membaca 1 lokasi. Dashboard PRO kini menampilkan DIAGNOSA
#    bila saldo 0 (retCode/retMsg Bybit), bukan diam-diam $0.00.
#  ► SESI 7/8 DIBANGUN ULANG DI BOT: pilihan akun DITANYA LAGI (pasti),
#    kunci demo dibaca SEGAR dari ge_keys.json (multi-lokasi), GEHTTP
#    murni (tanpa pybit, tanpa make_session, tanpa ENV_KIND).
#  ► AUDIT DIRI: kalau file tidak berisi sa_build_session/v1.40 -> TOLAK
#    jalan (exit 77). Perintah bukti: python3 GOLD7_V39.py --check
#  ► MODE 7/8 = GEHTTP PASTI (tanpa pybit): menu 7/8 kini MEMAKSA klien REST
#    langsung (HMAC v5, endpoint dikunci konstanta). Terbukti di GE_DIAG:
#    LOGIN OK @ api-demo + saldo $2.087.534,39. pybit TIDAK dipakai lagi
#    di mode 7/8 -> tidak ada lagi 'demo terdeteksi real'.
#  ► PENDETEKSI SALINAN LAMA: saat mulai, banner menampilkan file yang
#    dijalankan + salinan LAMA (doji.py/dog.py/doji7.py, ukuran beda) di
#    folder yang sama -> daftar + perintah hapus.
#    (dog.py yang menampilkan 'PENGAMAN-2' = v1.8 LAMA - bukan file ini!)
#  ► KLINEN REST BYBIT LANGSUNG (GEHTTP): tanda tangan HMAC v5 sendiri —
#    TIDAK bergantung pada pybit sama sekali. Endpoint DIKUNCI (demo =
#    api-demo.bybit.com), mustahil nyasar ke mainnet. pybit dipakai bila
#    sehat; bila rusak/salah endpoint -> otomatis ganti ke GEHTTP.
#  ► JALANKAN HANYA file 'GOLD7.py' — doji.py/dog.py/doji7.py adalah
#    salinan LAMA dan bukan ini!
#  ► ENDPOINT DIPAKSA LANGSUNG: sesi dibuat -> atribut 'endpoint' objek pybit
#    DITIMPA ke api-demo/testnet/mainnet sesuai pilihan, lalu dibaca balik.
#    Jadi DEMO PASTI api-demo.bybit.com di versi pybit APA PUN & koneksi
#    tidak bisa lagi nyasar ke mainnet.
#  ► SESI HTTP VERSI-AGNOSTIK: endpoint DEMO dipaksa benar di SEMUA versi
#    pybit (coba endpoint= lalu testnet/demo=). Deteksi pybit lokal yang
#    menutupi paket asli (folder pybit/ di direktori proyek) -> PERINGATAN.
#    SELFTEST kini menampilkan lokasi pybit + endpoint + saldo DEMO.
#  ► KUNCI PROSES TUNGGAL: hanya 1 bot boleh jalan. Proses lama (terminal
#    lain / doji7.py lama) -> ditolak, supaya tidak ada 'hantu' REAL.
#  ► SELFTEST: python3 GOLD7.py --selftest untuk membuktikan kunci demo
#    terhubung ke api-demo + saldo. Pengaman lapis-2 di main(): pilihan
#    DEMO wajib endpoint api-demo, selain itu HENTI (sys.exit 9).
#  ► KONFIRMASI AKUN BESAR sebelum mode 7/8 jalan: tampilkan DEMO/REAL +
#    endpoint + kunci yang dipakai. DEMO: Enter = lanjut; REAL: wajib YES.
#    Bila pilih REAL padahal kunci DEMO terisi -> PERINGATAN besar.
#    Versi dicetak di LIVE LOG (GOLDEN EDGE v1.7) -> bukti file terbaru.
#  ► AKUN TIDAK BISA SALAH: input eksplisit (1/Enter/D = DEMO; hanya 2+R=REAL,
#    sisanya diulang & dicatat) + PENGAMAN KERAS di standalone: pilih DEMO tapi
#    koneksi mainnet -> bot MATI otomatis (bukan diam-diam jalan di real).
#  ► PROBE AKUN: sesi dibuat → endpoint SESUNGGUHNYA dibaca dari objek pybit
#    (session.endpoint) lalu ditampilkan + saldo dicek live. Kunci demo TIDAK
#    lagi diam-diam jatuh ke kunci utama (sumber kebingungan demo/real).
#  ► MENU 7 (DOJI M3) & MENU 8 (FIB M30) = strategi BERDIRI SENDIRI:
#    XAUUSDT saja · TANPA mesin PRO (zona likuiditas, konfluensi MTF,
#    WATCHDOG 12 simbol, readiness, engine stats) · dashboard ringkas.
#  ── SINKRON TERVERIFIKASI dgn Pine v6 (7 Sep 2026) ─────────────────────────
#  MENU 7 (DOJI BREAKOUT, 3m)  <->  PINE_1_DOJI_BREAKOUT.pine
#     body <= 10% range · wick >= 30% tiap sisi · range >= 1x ATR(14)
#     sweep LOW prev-candle -> BUY-only · sweep HIGH -> SELL-only ·
#     dua-duanya -> bebas · tanpa sweep -> SKIP · entry = touch (close)
#     SL sisi lawan doji (min 0.30%) · TP1 1.5R · TP2 2.25R · cooldown 4m
#  MENU 8 (FIB TREND SCALP, 30m)  <->  PINE_2_FIB_TREND_SCALP.pine
#     swing fractal 3 · swing terakhir <= 24 bar · fib zona 0.50-0.618
#     SL luar swing terakhir +- 0.25xATR, clamp 0.25-1.0% · TP1 1R · TP2 1.5R
#     cooldown 4m · fallback struktur 60m (PINE_2: "adaptif 60m")
#     PINE_2 juga menuai "LIVE PLAN" visual (ENTRY@61.8%, SL/TP1/TP2) yang
#     diperbarui tiap bar — BOT tidak ikut menuai (plan = proyeksi; eksekusi
#     tetap hanya saat trigger real: sentuh zona & close mantul 61.8%).
# ============================================================================
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
# ================== KLINEN REST BYBIT LANGSUNG (tanpa pybit) ==================
# Dipakai bila pybit tidak ada / rusak / salah endpoint di perangkat.
# Endpoint DIKUNCI konstanta: DEMO = api-demo.bybit.com — mustahil mainnet.
import hmac as _hmac, hashlib as _hl, urllib.parse as _up


class GEAPIError(Exception):
    """Error API Bybit: 'retCode retMsg'."""


class GEHTTP:
    """Pengganti pybit HTTP — API v5 dengan tanda tangan HMAC langsung.
    Menyediakan metode yang dipakai bot, dengan bentuk respons sama pybit."""

    def __init__(self, api_key="", api_secret="", testnet=False, demo=False):
        self.api_key = str(api_key or "")
        self.api_secret = str(api_secret or "")
        self.endpoint = ("https://api-demo.bybit.com" if demo else
                         "https://api-testnet.bybit.com" if testnet else
                         "https://api.bybit.com")

    def _sign(self, ts, qs):
        s = f"{ts}{self.api_key}5000{qs}"
        return _hmac.new(self.api_secret.encode(), s.encode(), _hl.sha256).hexdigest()

    def _headers(self, ts, qs, private):
        h = {"X-BAPI-API-KEY": self.api_key, "X-BAPI-TIMESTAMP": str(ts),
             "X-BAPI-RECV-WINDOW": "5000"}
        if private:
            h["X-BAPI-SIGN"] = self._sign(ts, qs)
        return h

    def _req(self, method, path, private=False, strict=False, **params):
        params = {k: v for k, v in params.items() if v is not None}
        ts = int(time.time() * 1000)
        if method == "GET":
            qs = _up.urlencode(params)
            url = self.endpoint + path + ("?" + qs if qs else "")
            r = requests.get(url, headers=self._headers(ts, qs, private), timeout=15)
        else:
            body = json.dumps(params)
            url = self.endpoint + path
            h = self._headers(ts, body, private)
            h["Content-Type"] = "application/json"
            r = requests.post(url, data=body, headers=h, timeout=15)
        try:
            j = r.json()
        except Exception:
            raise GEAPIError(f"HTTP {r.status_code} bukan JSON: {r.text[:120]}")
        if strict and int(j.get("retCode", -1)) != 0:
            raise GEAPIError(f"{j.get('retCode')} {j.get('retMsg')}")
        return j

    def get_kline(self, category="linear", symbol=None, interval=None, limit=200, **kw):
        return self._req("GET", "/v5/market/kline", category=category, symbol=symbol,
                         interval=interval, limit=limit)

    def get_tickers(self, category="linear", symbol=None, **kw):
        # PENTING: symbol WAJIB diteruskan - kalau tidak, Bybit mengembalikan
        # SEMUA ticker & get_price mengambil coin pertama (harga XAU jadi salah).
        return self._req("GET", "/v5/market/tickers", category=category,
                         symbol=symbol)

    def get_instruments_info(self, category="linear", symbol=None, **kw):
        return self._req("GET", "/v5/market/instruments-info", category=category,
                         symbol=symbol)

    def get_wallet_balance(self, accountType="UNIFIED", **kw):
        return self._req("GET", "/v5/account/wallet-balance", private=True,
                         accountType=accountType)

    def get_positions(self, category="linear", symbol=None, **kw):
        return self._req("GET", "/v5/position/list", private=True,
                         category=category, symbol=symbol)

    def set_leverage(self, category="linear", symbol=None, buyLeverage=None,
                     sellLeverage=None, **kw):
        return self._req("POST", "/v5/position/set-leverage", private=True, strict=True,
                         category=category, symbol=symbol, buyLeverage=buyLeverage,
                         sellLeverage=sellLeverage)

    def place_order(self, category="linear", symbol=None, side=None, orderType=None,
                    qty=None, timeInForce=None, positionIdx=0, **kw):
        return self._req("POST", "/v5/order/create", private=True, strict=True,
                         category=category, symbol=symbol, side=side, orderType=orderType,
                         qty=qty, timeInForce=timeInForce, positionIdx=positionIdx)

    def set_trading_stop(self, category="linear", symbol=None, stopLoss=None,
                         takeProfit=None, tpslMode=None, tpSize=None, slTriggerBy=None,
                         tpTriggerBy=None, trailingStop=None, positionIdx=0, **kw):
        return self._req("POST", "/v5/position/trading-stop", private=True, strict=True,
                         category=category, symbol=symbol, stopLoss=stopLoss,
                         takeProfit=takeProfit, tpslMode=tpslMode, tpSize=tpSize,
                         slTriggerBy=slTriggerBy, tpTriggerBy=tpTriggerBy,
                         trailingStop=trailingStop, positionIdx=positionIdx)


try:
    from pybit.unified_trading import HTTP as _PYBIT_HTTP
except Exception:
    _PYBIT_HTTP = None
HTTP = _PYBIT_HTTP if _PYBIT_HTTP is not None else GEHTTP

# ==================== KONFIGURASI ====================
API_KEY    = "sZMhJOIisVPsSF9Zcc"
API_SECRET = "KSfxmCHY1cVHDFWBwaYUKEP5jlITopgrBN9g"
TELEGRAM_TOKEN = "8287171493:AAHyCOnwC7mHMSuYAd8grI6MoDEnNSnWBxU"
TELEGRAM_CHAT  = "5316317443"
USE_TESTNET    = False               # True = akun demo/testnet Bybit (uji aman dulu)

# ---- Simbol & mode (menu saat start) ----
FOCUS_SYMBOLS = ["XAUUSDT"]          # selalu diikutkan (emas per video)
# v1.33: universe CADANGAN bila get_tickers gagal (koneksi/rate-limit):
# daftar likuid tinggi perp USDT Bybit — bot TIDAK turun ke 1 simbol.
FALLBACK_UNIVERSE = [
    "BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT", "DOGEUSDT",
    "ADAUSDT", "AVAXUSDT", "LINKUSDT", "TONUSDT", "TRXUSDT", "SUIUSDT",
    "DOTUSDT", "LTCUSDT", "BCHUSDT", "NEARUSDT", "APTUSDT", "ARBUSDT",
    "OPUSDT", "INJUSDT", "ICPUSDT", "FILUSDT", "ATOMUSDT", "UNIUSDT",
    "ETCUSDT", "XLMUSDT", "HBARUSDT", "AAVEUSDT", "SEIUSDT", "TIAUSDT",
    "JUPUSDT", "HYPEUSDT", "ONDOUSDT", "ENAUSDT", "WLDUSDT", "MKRUSDT",
    "STXUSDT", "FETUSDT", "RENDERUSDT", "PENDLEUSDT", "PYTHUSDT",
    "JTOUSDT", "RUNEUSDT", "OKBUSDT"
]
_SRC_UNI        = "LIVE"     # v1.33: LIVE / FALLBACK (sumber universe)
_UNI_ERR        = ""        # v1.33: pesan error get_tickers terakhir
ALL_MIN_TURNOVER = 5_000_000         # mode ALL: turnover 24h >= $5jt
TOP_N_CAP      = 30                  # mode TOP: batas jumlah coin paling likuid
SCAN_CHUNK     = 12                  # minimum simbol/siklus (round-robin)
# v1.33: PENGATURAN TAMPILAN WATCHDOG:
WD_SHOW_MAX    = 10                  # maks BARIS WATCHDOG di layar (ganti bebas)
                                        # scan TETAP semua coin (15/siklus utk 119
                                        # coin ≈ 1-2 req/dtk << batas Bybit
                                        # public kline ~120 req/5 dtk)
                                        # (sisanya dihitung "+N lagi";
                                        # scan TETAP semua coin, hanya tampilan)
# v1.33: chunk DINAMIS — rotasi penuh ~8 siklus agar bar 15m (flip R3) tidak
# terlewat. ALL COIN bisa 250-400 simbol; chunk 12 tetap = dicek tiap 15-25mnt.
ROT_CYCLES     = 8                   # target siklus utk 1x putaran penuh
CHUNK_CAP      = 100                 # batas aman (rate-limit & latensi dashboard)

def auto_chunk(n_rest):
    """Chunk scan utk siklus ini: max(SCAN_CHUNK, ceil(n_rest/ROT_CYCLES)) cap CAP.
    n_rest = simbol tanpa posisi selain hero. Jika universe kecil -> SCAN_CHUNK."""
    c = max(SCAN_CHUNK, (n_rest + ROT_CYCLES - 1) // ROT_CYCLES)
    return min(n_rest, min(CHUNK_CAP, c)) if n_rest > 0 else 0
SKIP_RETRY_MIN = 30                  # cek ulang simbol yg di-skip (cap kurang)
DEFAULT_MODE   = 1                   # 1=ALL 2=TOP 3=EMAS (Enter / non-tty)
MODE_LABEL     = {1: "ALL COIN", 2: "TOP %d" % TOP_N_CAP, 3: "EMAS SAJA",
                   4: "PRO (pasar+varian \u00b7 AKUN)", 6: "SCALPER 5m",
                   7: "DOJI BREAKOUT 3m/30m/MTF (XAU)", 8: "FIB TREND 30m / MTF 30+60m (XAU)"}

# ---- MODE 7: DOJI BREAKOUT SCALP (XAUUSDT) ----
DOJI_TF          = "3"      # trigger 3 MENIT (M3 — sesuai video doji breakout)
DOJI_HTF1        = "5"      # konteks 5m
DOJI_HTF2        = "15"     # konteks 15m
DOJI_BODY_RATIO  = 0.10     # body <= 10% range — video: "rasio bodinya pokoknya kecil banget"
DOJI_WICK_RATIO  = 0.30     # tiap kaki/shadow >= 30% range — "lebih dominan kakinya"
DOJI_RANGE_ATR_MIN = 1.0    # range doji >= 1x ATR(14) — doji PANJANG (long-legged),
                            # bukan cross kecil/noise (literatur long-legged doji)
DOJI_WICK_RATIO_EXT = 0.15  # v1.35: sisi PENDEK ekstrem (dragonfly/gravestone)
DOJI_WICK_MAIN_EXT  = 0.50  # v1.35: kaki UTAMA dragonfly/gravestone >= 50% range
DOJI_RANGE_ATR_MIN_DF = 0.7 # v1.35: T/⊥ cukup >= 0.7xATR (tak sepanjang long-legged)
DOJI_SL_PCT      = 0.30     # SL minimal 0.30% (agar > biaya fee/slip)
DOJI_RR_TP1      = 1.5      # TP1 = 1.5R (video: "risk ratio 1 banding 1,5")
DOJI_RR_TP2      = 2.25     # TP2 = 2.25R (perpanjangan 'let it run')
DOJI30_TF        = "30"     # DOJI 30m (menu 7 metode 2)
DOJI30_HTF1      = "60"     # konteks 60m
DOJI30_HTF2      = "240"    # konteks 4H
# DOJI MTF (metode 3): doji 30m + BIAS struktur 60m (arah wajib searah).
DOJI_COOLDOWN_MIN= 4        # jeda antar trade doji (menit)
# ---- MODE 8: FIB RETRACEMENT TREND SCALP (XAUUSDT, video ThisIsDaryl) ----
FIB_TF           = "30"     # trigger 30 MENIT (M30 — sesuai video)
FIB_HTF1         = "60"     # struktur FALLBACK (adaptif) di 60m
FIB_HTF2         = "240"    # konteks 240m
FIB_SWING_AGE    = 24       # swing terakhir wajib <= 24 bar (titik TREN BARU;
                            # 24 bar x 30m = 12 jam) — lebih tua = skip / naik TF
FIB_SWING        = 3        # fractal lookback (bar kiri/kanan) utk swing
FIB_LO           = 0.50     # zona diskon: 50% - 61.8% (entry di bawah 50%)
FIB_HI           = 0.618
FIB_RR_TP1       = 1.0      # TP1 = 1R
FIB_RR_TP2       = 1.5      # TP2 = 1.5R
FIB_MIN_SL_PCT   = 0.25     # SL minimal 0.25%
FIB_MAX_SL_PCT   = 1.00     # SL maksimal 1.0% (scalp: jangan terlalu lebar)
FIB_COOLDOWN_MIN = 4        # jeda antar trade (menit)
MODE           = DEFAULT_MODE
SYMBOLS        = list(FOCUS_SYMBOLS)   # diisi refresh_symbols()/menu saat start
_LAST_CHUNK    = SCAN_CHUNK            # v1.33: chunk aktual siklus terakhir (display)
_DBG           = {"rest": 0, "pos": 0, "take": 0, "last_sym": 0,    # v1.33: diagnosa scan
                  "univ": 0, "state": 0}

# ---- VARIAN STRATEGI (Mode 4 = PRO: pilih pasar + varian) ----
#   A DASAR  : 3 aturan murni (perilaku default)
#   B REGIME : filter tren EMA50/200 (Pine): LONG saat BULL TREND,
#              SHORT saat BEAR TREND, SKIP saat ROTATION
#   C ELITE  : zona minimal 8.0/10 (bukan 6.5) — hanya zona ELITE
#   D RETEST : zona harus sudah diuji >= 2x (tests >= 2) — retest/teruji
VARIANT          = "A"      # env GE_VARIANT (berlaku utk semua mode 1-4)
SUBMODE          = ""       # "" | DEMO (4) | SCALPER (6) | DOJI7/DOJI30/DOJIM (7) | FIB8/FIB8M (8)
ACCT_CHOSEN      = ""       # akun terpilih di menu (demo/real) — diteruskan ke mode 7/8
ENV_KIND         = "real"   # "real" | "testnet" | "demo"  (target akun utk session)
REGIME_EMA_FAST  = 50
REGIME_EMA_SLOW  = 200
ELITE_THR        = 8.0
RETEST_MIN_TESTS = 2
VARIANTS = {"A": ("DASAR", "3 aturan murni"),
            "B": ("REGIME", "filter tren EMA50/200: skip ROTATION"),
            "C": ("ELITE", "zona >= 8.0/10 (bukan 6.5)"),
            "D": ("RETEST", "zona sudah diuji >= 2x (tests >= 2)"),
            "E": ("AGRESIF", "sinyal TF cukup 3/4 · zona >= 5.5 · RR >= 1.0 (lebih sering)"),
            "F": ("GABUNGAN", "A+B+C+D SERENTAK: regime searah · zona >= 8.0 · "
                  "teruji >= 2x · sig 4/4 · RR >= 1.2 (paling selektif)"),
            "G": ("GZ-STOPPOOL", "harga DI LUAR Golden Zone 15m (short>0.786 / "
                  "long<0.618) & SUDAH sentuh STOP POOL searah -> ENTRY (SL luar zona)"),
            "H": ("G-AMAN", "seperti G + syarat 1H WAJIB searah arah entry "
                  "(regime 1H BULL utk LONG / BEAR utk SHORT; ROTATION = SKIP)")}
# Parameter varian E (AGRESIF) — hanya dipakai saat varian E dipilih
E_SIG_MIN   = 3      # sinyal TF cukup 3 dari 4 kondisi (A-D tetap 4/4)
E_ZONE_MIN  = 5.5    # zona minimal (A-D tetap 6.5)
E_MIN_RR    = 1.0    # RR minimal (A-D tetap 1.2)

# ---- MODE 5: TESTNET (strategi sama, akun testnet Bybit) ----
# Kunci testnet: prioritas ENV (GE_TESTNET_KEY/SECRET) -> file ge_keys.json -> GANTI.
# Isi sekali lewat:  python3 set_testnet_key.py   (daftar dulu di testnet.bybit.com)
_KF_BASE = globals().get("__file__") or "ge_keys.json"   # aman saat di-exec (test)
KEYS_FILE = os.path.join(os.path.dirname(os.path.abspath(_KF_BASE)), "ge_keys.json")


def load_keys_file(path=None):
    """Baca ge_keys.json (opsional). Format: {"testnet": {"api_key": "...", "api_secret": "..."}}."""
    p = path or KEYS_FILE
    try:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                d = json.load(f)
            if isinstance(d, dict):
                return d
    except Exception:
        pass
    return {}


def _load_env_keys(which):
    """Resolusi kunci lingkungan (testnet|demo): env > ge_keys.json > GANTI.
    TESTNET -> GE_TESTNET_KEY/SECRET + keys["testnet"].
    DEMO    -> GE_DEMO_KEY/SECRET + keys["demo"] (kunci dibuat di akun prod
              dalam mode Demo Trading — BUKAN kunci testnet)."""
    kf = load_keys_file().get(which, {}) or {}
    ek = "GE_TESTNET_KEY" if which == "testnet" else "GE_DEMO_KEY"
    es = "GE_TESTNET_SECRET" if which == "testnet" else "GE_DEMO_SECRET"
    return (os.environ.get(ek, kf.get("api_key", "GANTI")),
            os.environ.get(es, kf.get("api_secret", "GANTI")))


def _load_tn_keys():
    """Backward-compat: kunci TESTNET (env > ge_keys.json > GANTI)."""
    return _load_env_keys("testnet")


TESTNET_API_KEY, TESTNET_API_SECRET = _load_tn_keys()
DEMO_API_KEY, DEMO_API_SECRET = _load_env_keys("demo")
# ---- MODE 6: SCALPER (TF cepat + TP/SL tetap %; mode 1-4 TIDAK berubah) ----
SCALP_TRIGGER    = "5"     # TF trigger 5 menit (bar tutup)
SCALP_HTF1       = "15"    # bias 15m
SCALP_HTF2       = "60"    # bias 60m
SCALP_TP_PCT     = 0.70    # TP tetap: +0.70% (net setelah fee 0.11%+slip ~ +0.53%)
SCALP_SL_PCT     = 0.45    # SL tetap: -0.45%
SCALP_MIN_RR     = 1.2     # RR minimal (0.70/0.45 = 1.56)
SCALP_LOOP_SLEEP = 10      # jeda antar siklus scan (detik)

def variant_label(v):
    return VARIANTS.get(v, VARIANTS["A"])[0]

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
# v1.34: ZONA MINIMUM = pilihan menu (1=6.5 video asli STRONG · 2=5.5 · 3=4.0 default).
# Analisis 1.308 bar: zona yang SEDANG disentuh harga selalu muda (tests=1) -> skor
# 2-5; ambang 6.5 praktis hanya utk zona JAUH yang tak pernah di-approach -> salah
# satu penyebab 0 entry 3 hari. 4.0 = zona kuat yang TERJANGKAU & tersentuh.
ZONE_MIN_SCORE = 4.0                 # minimal zona (default baru; 6.5 = video asli)
R1B_FLIP_WINDOW = 3                  # v1.34: "15m baru flip" = dlm N bar terakhir
R2_USE_TOUCH    = True               # v1.34: R2 cukup low/high MENYENTUH zona (video)
R2_REVIVE_BARS  = 3                  # v1.34: zona SWEPT <= N bar lalu boleh dipakai lagi
                                     # (sweep & reverse — reversal 15m lahir tepat stlh sweep)
APPROACH_ATR   = 0.35                # "price tapping zone" (dalam xATR dari tepi)
SL_BUFFER_ATR  = 0.50                # nafas SL di luar zona
MIN_RR         = 1.2                 # tolak setup bila RR < ini
FALLBACK_TP_ATR = 2.5                # TP cadangan bila tak ada zona lawan
# ---- Mesin ZIGZAG scenario (v1.39) — port 1:1 dari Pine (input default) ----
SCEN_MIN_SC     = 2.0    # Min Waypoint Score (f_pick/f_snap)
SCEN_SNAP_ATR   = 0.75   # Snap Waypoint To Zone Within (xATR)
SCEN_REV_PCT    = 55.0   # Reverse Retrace (% leg trigger)
SCEN_RETEST_PCT = 55.0   # Retest Recovery (% leg reverse)
SCEN_SNAP_TRIG  = False  # Auto (net pull) utk arah trigger

# ---- Risiko & eksekusi (gaya bot utama) ----
RISK_CAP_USD = 50.0  # rugi maks per trade (dolar) - DEMO: risiko 50/2.075.374 = 0.0024%
RISK_HARD_USD = 100.0 # plafon absolut per trade (pengaman keras)
# Ubah sesuai selera, mis. 25 / 50 / 100 / 250. Simpan lalu restart bot.
MARGIN_MAX_PCT = 100 # plafon margin per posisi (% saldo)
# v1.33: STANDAR LEVERAGE per kelas simbol (SAMA utk akun REAL & DEMO:
# aturan tunggal, tidak peduli akun mana yang dipakai):
#   MAJOR = BTC/ETH/SOL -> LEV_STD_MAJOR x
#   ALT   = lainnya      -> LEV_STD_ALT x
# Leverage terpakai = min(standar kelas, lev aman likuidasi) -> SL
# SELALU tersentuh duluan (keamanan menang).
MAJOR_SYMS     = {"BTCUSDT", "ETHUSDT", "SOLUSDT"}
LEV_STD_MAJOR  = 10
LEV_STD_ALT    = 5
MAX_LEVERAGE  = 50
MIN_LEVERAGE  = 1
MAX_POSITIONS = 10
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
MARGIN_TRADE_PCT = 90 # target margin per entry = % saldo (mis. $10 -> $2)
# v1.33: MODE R1 utk menu 1-6 (dipilih di menu; non-tty: GE_R1=1|2):
#   KETAT  = 1H & 4H HARUS searah (aturan video asli / default)
#   LONGGA = cukup 1H searah (4H diabaikan) — TAMBAHAN menu
R1_MODE        = "KETAT"
LEV_SL_GAP      = 1.5                  # jarak likuidasi = 1.5x jarak SL -> SL tersentuh DULU
LEV_MR_PCT      = 0.015                # cadangan maintenance margin + fee (~1.5%)
LEV_GUARD       = True                 # tutup posisi bila lev bursa ternyata > lev aman

# ---- NEWS GUARD (port bot utama) ----
NEWS_GUARD      = False   # DIMATIKAN user 2026-09-05
NEWS_BTC_FAST   = 0.40                 # shock bila BTC >= 0.20%/MENIT (0.08 = terlalu ketat)
NEWS_MIN_JUMP   = 0.25                 # lonjakan ABSOLUT minimal % (abaikan tick kecil/wiggle)
NEWS_MIN_WINDOW = 20                   # evaluasi hanya bila >= 20 detik sejak cek terakhir
NEWS_EXTEND     = False                # False = jeda TIDAK diperpanjang oleh shock beruntun
NEWS_PAUSE_MIN  = 5                   # jeda entry setelah shock (posisi aktif tetap dikelola)
CPI_GUARD_ON    = False   # DIMATIKAN user 2026-09-05
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
VOL_GUARD       = False   # DIMATIKAN user 2026-09-05
VOL_SPIKE_ATR   = 4.0                  # bar 15m >= 4x ATR15 = spike -> jeda entry
VOL_MOVE_PCT    = 3.00                 # ATAU loncat >= 3.0% dlm 1 bar tutup (1.0% terlalu berisik)
VOL_PAUSE_MIN   = 5                   # jeda entry (menit) setelah spike volatilitas

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

# Info AKUN AKTIF — diisi make_session(); dipakai dashboard agar jelas
# sedang terhubung ke akun mana (demo/real/testnet) & kunci apa yang dipakai.
_SESS = {"kind": "real", "host": "api.bybit.com", "key_src": "kunci utama"}
_wb_err = ""          # pesan error get_wallet_balance terakhir (diagnosa saldo 0)

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
    _sa_k = SUBMODE in ("DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M")
    if SUBMODE == "TESTNET" or (ENV_KIND == "testnet" and not _sa_k):
        _tk = "TERISI" if _fresh_testnet_key()[0] not in ("", "GANTI") else "BELUM"
        _akun_line = (f"  {B}Akun{X}       {Y}TESTNET{X} — api-testnet.bybit.com "
                      f"(uang virtual) · kunci {_tk}")
    elif SUBMODE == "DEMO" or (ENV_KIND == "demo" and not _sa_k):
        _dk = "TERISI" if _fresh_demo_key()[0] not in ("", "GANTI") else "BELUM"
        _akun_line = (f"  {B}Akun{X}       {Y}DEMO{X} — api-demo.bybit.com "
                      f"(Demo Trading, simulasi akun prod) · kunci {_dk}")
    else:
        _akun_line = None
    if SUBMODE == "SCALPER":
        L.append(_row(f"  {B}Enjin{X}      {Y}SCALPER{X} — TF {SCALP_TRIGGER}m/{SCALP_HTF1}m/"
                      f"{SCALP_HTF2}m · TP +{SCALP_TP_PCT}% · SL -{SCALP_SL_PCT}% · "
                      f"siklus {SCALP_LOOP_SLEEP}s"))
    elif SUBMODE in ("DOJI7", "DOJI30", "DOJIM"):
        _ek = "DEMO" if ENV_KIND == "demo" else "AKUN REAL"
        _dl = ("DOJI BREAKOUT MTF 30m+60m" if SUBMODE == "DOJIM" else
               "DOJI BREAKOUT 30m" if SUBMODE == "DOJI30" else "DOJI BREAKOUT 3m")
        L.append(_row(f"  {B}Enjin{X}      {Y}{_dl}{X} — XAUUSDT · "
                      f"akun {_ek} · DOJI PANJANG (body<=10% & kaki>=30% & range>=1xATR) - sweep candle sblmnya → "
                      f"touch high/low = entry · RR 1:1.5"))
    elif SUBMODE in ("FIB8", "FIB8M"):
        _ek = "DEMO" if ENV_KIND == "demo" else "AKUN REAL"
        _lb = ("FIB TREND MTF 30m+60m" if SUBMODE == "FIB8M"
               else "FIB TREND SCALP 30m")
        L.append(_row(f"  {B}Enjin{X}      {Y}{_lb}{X} — XAUUSDT · akun {_ek} · "
                      f"struktur HH/HL → fib 50-61.8% → TP 1R/1.5R"))
    if _akun_line:
        L.append(_row(_akun_line))
    L.append(_row(f"  {B}Timeframe{X}  trigger {TF_TRIGGER}m \u00b7 HTF {TF_HTF1}/{TF_HTF2}m"
                  f" \u00b7 ref {TF_REF}"))
    if VARIANT == "G":                       # v1.38: resep GZ-STOPPOOL
        L.append(_row(f"  {B}Aturan{X}     harga DI LUAR GZ 15m (short > 0.786 / "
                      f"long < 0.618) \u2192 SUDAH sentuh STOP POOL \u2192 ENTRY "
                      f"(SL sisi luar zona \u00b7 RR \u2265 {MIN_RR})"))
    else:
        L.append(_row(f"  {B}Aturan{X}     1H&4H searah \u2192 zona \u2265 {_eff_zthr():.1f}"
                      f" ({_stars(_eff_zthr())}) \u2192 flip 15m = ENTRY"))
    if SUBMODE in ("DOJI7", "DOJI30", "DOJIM"):
        _dmt = "bias 60m (MTF) + " if SUBMODE == "DOJIM" else ""
        L.append(_row(f"  {B}Metode{X}     {_dmt}doji nyapu low/high candle sblmnya → "
                      f"touch = entry → SL sisi lawan doji → RR {DOJI_RR_TP1:.1f}"))
    elif SUBMODE in ("FIB8", "FIB8M"):
        _sd = ("60m (tren+zona) + konfirmasi 30m"
               if SUBMODE == "FIB8M" else "30m (adaptif 60m)")
        L.append(_row(f"  {B}Metode{X}     struktur {_sd} (swing \u2264 {FIB_SWING_AGE} bar) "
                      f"→ fib 50-61.8% → SL luar swing → "
                      f"RR {FIB_RR_TP1:.1f}/{FIB_RR_TP2:.1f}"))
    else:
        L.append(_row(f"  {B}Varian{X}     {M}{VARIANT}-{variant_label(VARIANT)}{X} — "
                      f"{VARIANTS.get(VARIANT, VARIANTS['A'])[1]}"))
    L.append(_row(f"  {B}Pengaman{X}   cap ${RISK_CAP_USD:.2f}/trade \u00b7 margin "
                  f"{MARGIN_TRADE_PCT:g}% saldo \u00b7 max {MAX_POSITIONS} pos"))
    L.append(_row(f"  {B}Lev aman{X}   SL dulu, baru likuidasi (gap {LEV_SL_GAP}\u00d7SL "
                  f"+{LEV_MR_PCT*100:.1f}%) \u00b7 LEV-GUARD {'ON' if LEV_GUARD else 'OFF'}"))
    L.append(_row(f"  {B}Lev std{X}    MAJOR (BTC/ETH/SOL) {LEV_STD_MAJOR}x \u00b7 "
                  f"ALT {LEV_STD_ALT}x \u00b7 REAL = DEMO (aturan sama)"))
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


def _gate_pick(dg, d):
    """v1.33: pilih alasan GATE utk arah AKTIF d (sesuai 1H/4H), bukan arah
    lawan. (Diag diisi LONG dulu lalu SHORT; _dg[-1] = arah lawan -> menyesatkan,
    mis. 'SHORT: R1 GAGAL' padahal 1H/4H sedang UP.)"""
    try:
        if d in (1, -1):
            pre = "LONG: " if d == 1 else "SHORT: "
            for x in reversed(dg or []):
                if x.startswith(pre):
                    return x
        return (dg or [None])[-1]
    except Exception:
        return None


def _gate_view(dg, d, s1, s4):
    """v1.33: dua baris GATE (display): (alasan arah AKTIF, status arah LAWAN).
    d = arah aktif (1/-1/0) dari kesepakatan 1H&4H; s1/s4 = sinyal 1H/4H."""
    out = []
    act = _gate_pick(dg, d) if d in (1, -1) else (_gate_pick(dg, 0) or (dg or [None])[-1])
    if act:
        out.append(act)
    if d in (1, -1):
        opp = None
        for _x in reversed(dg or []):          # cari KETAT arah lawan
            if _x.startswith("SHORT: " if d == 1 else "LONG: "):
                opp = _x
                break
        if not opp:
            _od = "SHORT" if d == 1 else "LONG"
            _osig = -d
            _st = ("sebagian searah" if (s1 == _osig) != (s4 == _osig)
                   else "searah" if s1 == _osig and s4 == _osig else "belum searah")
            opp = f"{_od}: 1H {s1:+d} \u00b7 4H {s4:+d} \u2014 {_st}, menunggu flip {_od.lower()}"
        out.append(opp)
    if not out:
        out = [(dg or ["\u25b8 menunggu data arah"])[-1]]
    return out


def _eff_zthr():
    """v1.37: ambang zona EFEKTIF utk TAMPILAN — varian E memakai E_ZONE_MIN (5.5),
    C/F memakai ELITE_THR (8.0), A/B/D memakai ZONE_MIN_SCORE (menu 6.5/5.5/4.0)."""
    return (E_ZONE_MIN if VARIANT == "E" else
            (ELITE_THR if VARIANT in ("C", "F") else ZONE_MIN_SCORE))


def _zthr_lbl():
    """v1.38: label ambang utk header — varian G = GZ-STOPPOOL (tanpa skor zona)."""
    return "GZ\u2192STOPPOOL" if VARIANT == "G" else f"zona \u2265 {_eff_zthr():.1f}"


def _gz_line(con):
    """v1.36: baris GATE 'resep Golden Zone' (display-only).
    Per TF (15m/1H/4H): posisi harga vs GZ = ABOVE (>0.786) / IN (0.618-0.786) /
    BELOW (<0.618) + skor 4-kondisi N/4. Bias mean-reversion:
    >=2 TF ABOVE -> SHORT-bias (harga mahal, cari tolakan);
    >=2 TF BELOW -> LONG-bias  (harga murah, cari pantulan);
    selainnya EQUAL (kombinasi campur -> jangan asal entry)."""
    try:
        tf_out = []
        cnt_ab = cnt_bl = 0
        for key, lbl in (("15", "15m"), ("60", "1H"), ("240", "4H")):
            c = con.get(key)
            if not c or "gzl" not in c or len(c["gzl"]) < 2:
                return None
            gzl, gzh, cl = float(c["gzl"][-2]), float(c["gzh"][-2]), float(c["close"][-2])
            if gzl != gzl or gzh != gzh:
                return None
            if cl > gzh:
                pos, pc = "ABOVE", R
                cnt_ab += 1
            elif cl < gzl:
                pos, pc = "BELOW", G
                cnt_bl += 1
            else:
                pos, pc = "IN", Y
            b = int(c["bull"][-2]); be = int(c["bear"][-2])
            _sc = b if b >= be else be
            _arw = "\u25b2" if b >= be else "\u25bc"   # v1.37: sisi momentum dominan
            tf_out.append(f"{lbl} {pc}{pos}{X} {_arw}{_sc}/4")
        bias = ("SHORT-bias" if cnt_ab >= 2 else
                "LONG-bias" if cnt_bl >= 2 else "EQUAL")
        return " \u00b7 ".join(tf_out) + f" \u2192 {bias}"
    except Exception:
        return None


def render_dash(bal, ctx):
    """Dashboard 2-tingkat: WATCHDOG (semua coin 1 baris + bar kesiapan %)
    -> WATCHDOG seluruh coin + panel POSISI AKTIF."""
    if not UI_ON:
        return
    L = [f"{C}\u2554{'\u2550' * (WIDTH - 2)}\u2557{X}"]
    sp = SPIN[ctx.get("tick", 0) % len(SPIN)]
    tick = ctx.get("tick", 0)
    idr = usd_idr()
    _vtag = f"{D}|{X} var {M}{VARIANT}-{variant_label(VARIANT)}{X}" if VARIANT != "A" else ""
    if R1_MODE == "LONGGA":                                # v1.33: tampil mode R1
        _vtag += f"{D}|{X} {Y}R1 LONGGA{X}"
    L.append(_row(f"{FW}\u25c7 GOLDEN EDGE SUITE{X} {sp} "
                  f"{D}|{X} TF {TF_TRIGGER}/{TF_HTF1}/{TF_HTF2}m {D}|{X} {_zthr_lbl()}"
                  f" {D}|{X} cap ${RISK_CAP_USD:.2f}{_vtag} {D}|{X} "
                  f"{wib_now().strftime('%d %b %H:%M:%S WIB')}"))
    L.append(_row(f"  {D}kurs 1$ = Rp {fmt_rp(idr, 0)} (auto-refresh 30 mnt){X}"))
    bloc, why = entry_blocked()
    if bloc:
        L.append(_row(f"{R}\u26a0 GUARD AKTIF — {why} | ENTRY DIJEDA{X}"))
    if (bal or 0) <= 0:
        L.append(_row(f"{R}\u26a0 SALDO $0.00 — {_wb_err or 'tidak ada data saldo'}{X}"))
        L.append(_row(f"{R}   ▸ cek: python3 set_testnet_key.py --show (DEMO harus "
                      f"TERISI; kunci demo bukan kunci utama){X}"))
    _nvol = sum(1 for _st in STATES.values()
                if VOL_GUARD and time.time() < (_st.get("vol_until") or 0.0))
    if not bloc and _nvol:
        L.append(_row(f"{Y}\u26a0 VOLATILITY PER-SIMBOL: {_nvol} coin dijeda — "
                      f"simbol lain tetap bisa entry{X}"))
    L.append(_sep())
    syms = ctx.get("syms") or []
    # v1.33: WATCHDOG 1 baris per simbol - buang duplikat apa pun sumbernya
    _seen = set()
    syms = [e for e in syms
            if e.get("sym") not in _seen and not _seen.add(e.get("sym"))]
    # v1.33: WATCHDOG = SELURUH universe (cache _WD), bukan hanya giliran siklus
    # ini. Simbol yang belum/gagal terdata tetap tampil dgn status jelas.
    _wdview = {e.get("sym"): e for e in syms}
    for _sd in list(SYMBOLS) + [x for x in STATES if STATES[x].get("in_position")]:
        if _sd not in _wdview:
            _we = _WD.get(_sd)
            _wdview[_sd] = dict(_we) if _we else {"sym": _sd, "wait": True}
    syms = list(_wdview.values())
    # ---- HERO ----
    hero_sym = "XAUUSDT" if (MODE == 3 or SUBMODE in ("DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M")) else "BTCUSDT"
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
    _acc = f" · {ENV_KIND.upper()}" if ENV_KIND in ("demo", "testnet") else ""
    head_l = (f"{B}{hero_ic} {hsym}{X} {dcol}{darr}{X} {D}({bpx:,.2f}){X} "
              f"{D}[{MODE_LABEL.get(MODE, '?')} · {len(SYMBOLS)} simbol{_acc}]{X}")
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
        try:
            rdy, tag, col = readiness(con, zsc, px, atrv)
        except Exception as _re:
            rdy, tag, col = 0.0, "ERR", R
            e["err"] = "readiness err (%s)" % type(_re).__name__
        e["rdy"] = (rdy, tag, col)
        best = max((zs for zn, zs in zsc if zn.phase != 2), default=0.0)
        e["best"] = best
        enlist.append(e)
    enlist.sort(key=lambda e: -e["rdy"][0])
    # v1.33: cap baris layar (ALL COIN 250+); sisanya dicatat "+N lagi"
    _wd_hidden = max(0, len(enlist) - WD_SHOW_MAX)
    if _wd_hidden:
        enlist = enlist[:WD_SHOW_MAX]
    if len(SYMBOLS) == 1 and MODE in (1, 2):
        L.append(_row(f"{R}\u26a0 UNIVERSE KOSONG \u2014 hanya {SYMBOLS[0]}: "
                      f"detect_perp_universe gagal (get_tickers \u2192 cek koneksi "
                      f"& kunci / ge_bot.log){X}"))
    # ---- WATCHDOG: 1 baris per coin ----
    _DBG["univ"] = len(SYMBOLS)                       # v1.33: sinkron diagnosa
    _DBG["state"] = len(STATES)                       # dgn kebenaran saat render
    L.append(_sep(f"\u25c9 WATCHDOG ({len(enlist)} tampil dari {len(SYMBOLS)} "
                  f"coin \u00b7 urut kesiapan \u00b7 scan {_LAST_CHUNK}/siklus \u00b7 "
                  f"rotasi ~{ROT_CYCLES}x \u00b7 maks {WD_SHOW_MAX} \u00b7 "
                  f"sisa {_DBG.get('rest', 0)} \u00b7 posisi "
                  f"{_DBG.get('pos', 0)} \u00b7 ambil {_DBG.get('take', 0)} \u00b7 "
                  f"univ {_DBG.get('univ', len(SYMBOLS))} \u00b7 state "
                  f"{_DBG.get('state', len(STATES))}"))
    if enlist:
        for e in enlist:
            con = e.get("con") or {}
            st = e.get("state") or {}
            try:      # v1.33: 1 simbol con rusak TIDAK boleh mematikan panel
                s1 = int(con["60"]["sig"][-2]) if "60" in con else 0
                s4 = int(con["240"]["sig"][-2]) if "240" in con else 0
                s15 = int(con["15"]["sig"][-2]) if "15" in con else 0
            except Exception:
                s1 = s4 = s15 = 0
                e["err"] = "data con rusak"
            a1 = "\u25b2" if s1 == 1 else "\u25bc" if s1 == -1 else "\u2022"
            a4 = "\u25b2" if s4 == 1 else "\u25bc" if s4 == -1 else "\u2022"
            a15 = "\u25b2" if s15 == 1 else "\u25bc" if s15 == -1 else "\u2022"
            fv, fcol = e.get("fuel") or (50.0, Y)
            try:
                rdy, tag, col = e["rdy"]
            except Exception:
                rdy, tag, col = 0.0, "DATA…", D
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
            if e.get("err"):
                row += f" {R}\u25cc {e['err']}{X}"
            elif e.get("wait"):
                row += f" {D}\u25cc menunggu giliran scan{X}"
            L.append(_row(row))
    else:
        L.append(_row(f"  {D}menunggu data pertama\u2026{X}"))
    if _wd_hidden:
        L.append(_row(f"  {D}\u2026 +{_wd_hidden} coin lain (urut kesiapan \u2014 "
                      f"atur jumlah tampil: WD_SHOW_MAX di GOLD7.py){X}"))
    # ---- baris skip (cap kurang) ----
    for e in syms:
        if e.get("skip"):
            L.append(_row(f"  {D}\u2298 {e.get('sym','?')} — {e['skip']} "
                          f"(retry {SKIP_RETRY_MIN}m){X}"))
    # ---- GATE: kenapa tidak ada entry (R1/R2/R3/RR) — diagnosa transparan ----
    _gate_n = 0
    for e in enlist:
        if _gate_n >= 3:
            break
        _st = e.get("state") or {}
        _dg = _st.get("last_diag") or []
        if _dg and not _st.get("in_position"):
            _c = e.get("con") or {}
            _d = 0
            try:
                _s1 = int(_c["60"]["sig"][-2]) if "60" in _c and len(_c["60"]["sig"]) >= 2 else 0
                _s4 = int(_c["240"]["sig"][-2]) if "240" in _c and len(_c["240"]["sig"]) >= 2 else 0
                _d = _s1 if (_s1 == _s4 and _s1 != 0) else 0
            except Exception:
                _d = 0
            for _gl in _gate_view(_dg, _d, _s1, _s4):
                L.append(_row(f"{D}  \u25b8 GATE {e.get('sym','?')}: {_gl}{X}"))
            _gate_n += 1
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
    # ---- ENGINE (statistik zona ala Pine: zona/elite/tests/reaksi/regime) ----
    ztot = zact = zel = ztest = 0
    rhit = rtot = 0
    reg = None
    for e in syms:
        zz = e.get("zones") or []
        ztot += len(zz)
        for z, sc in zz:
            if z.phase != 2:
                zact += 1
            if sc >= ELITE_THR:
                zel += 1
            ztest += int(getattr(z, "tests", 0) or 0)
        st_ = e.get("state") or {}
        _r = st_.get("_react") or [0, 0]
        rhit += _r[0]
        rtot += _r[0] + _r[1]
        if reg is None and e.get("regime"):
            reg = e["regime"]
    if ztot or rtot:
        _rtxt = (f"{rhit}/{rtot} ({rhit / rtot * 100:.0f}%)" if rtot else "0/0")
        _rline = (f"{D}\u25c6 ENGINE: zona {ztot} \u00b7 aktif {zact} \u00b7 ELITE {zel}"
                  f" \u00b7 tests {ztest} \u00b7 REAKSI {_rtxt}{X}")
        if reg:
            _rc = G if reg == "BULL TREND" else (R if reg == "BEAR TREND" else Y)
            _rline += f" \u00b7 REGIME {_rc}{reg}{X}"
        L.append(_row(_rline))
        _vs = stats_variant_summary()
        if _vs:
            _parts = []
            for _vk in sorted(_vs):
                _o = _vs[_vk]
                _wr = _o["w"] / _o["n"] * 100 if _o["n"] else 0.0
                _pc = G if _o["pnl"] >= 0 else R
                _lab = _vk.replace("VAR", "") if _vk.startswith("VAR") else _vk
                _parts.append(f"{_lab} {_wr:.0f}%{_pc}{_o['pnl']:+6.2f}${X}/{_o['n']}")
            L.append(_row(f"{D}\u25c6 VARIAN: {X}" + " \u00b7 ".join(_parts)))
    # ---- SESI + LOG ----
    sh = wib_now().hour
    sn, sc = gold_session(sh)
    L.append(_row(f"{D}scan {_LAST_CHUNK} simbol/siklus (round-robin) \u00b7 total "
                  f"{len(SYMBOLS)} \u00b7 WATCHDOG terdata {len(_WD)}/{len(SYMBOLS)} "
                  f"\u00b7 uni {_SRC_UNI} \u00b7 R1 {R1_MODE} \u00b7 "
                  f"mode {MODE_LABEL.get(MODE, '?')}{X}"))
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
        lst = (r or {}).get("result", {}).get("list") or []
        px = None
        for t in lst:
            if t.get("symbol") == sym:
                px = float(t.get("lastPrice") or 0)
                break
        if px is None or px <= 0:              # endpoint abaikan symbol: cari manual
            for t in lst:
                if t.get("symbol") == sym:
                    px = float(t.get("lastPrice") or 0)
                    break
        if px is None or px <= 0:
            df = get_kline(sym, TF_TRIGGER, limit=3)
            if df is not None and len(df):
                px = float(df["close"].iloc[len(df) - 1])
        if px is None or px <= 0:
            return 0.0
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

def _wallet_rows():
    """Baris wallet dari get_wallet_balance. Coba UNIFIED → CONTRACT → SPOT.
    Akun testnet/classic sering tidak punya baris UNIFIED (-> terbaca 0 dulu).
    Error terakhir disimpan di _wb_err utk diagnosa saldo 0 di dashboard."""
    global _wb_err
    for at in ("UNIFIED", "CONTRACT", "SPOT"):
        try:
            r = session.get_wallet_balance(accountType=at)
            if isinstance(r, dict) and int(r.get("retCode", -1)) == 0:
                rows = r.get("result", {}).get("list") or []
                if rows:
                    _wb_err = ""
                    return at, rows
                _wb_err = f"{at}: baris kosong"
            else:
                _wb_err = f"{at}: retCode {r.get('retCode')} '{r.get('retMsg')}'"
        except Exception as e:
            _wb_err = f"{at}: {type(e).__name__} {e}"
    return None, []


def get_balance():
    global _wb_err
    try:
        at, rows = _wallet_rows()
        for row in rows:
            eq = row.get("totalEquity")
            if eq not in ("", None):
                return float(eq)
        for row in rows:
            wb = row.get("totalWalletBalance")
            if wb not in ("", None):
                return float(wb)
        _wb_err = _wb_err or f"{at}: tidak ada kolom saldo"
    except Exception as e:
        _wb_err = f"exception {type(e).__name__}: {e}"
    return 0.0


def get_available():
    try:
        _, rows = _wallet_rows()
        for row in rows:
            v = row.get("totalAvailableBalance") or ""
            if v not in ("", None):
                return float(v)
        for row in rows:
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

def market_regime(df):
    """Regime tren ala Pine: EMA50 > EMA200 & close > EMA50 -> BULL TREND;
    EMA50 < EMA200 & close < EMA50 -> BEAR TREND; selainnya ROTATION.
    Dinilai pd bar TUTUP (-2) pd TF 1H. Return None bila data < 210 bar."""
    try:
        c = pd.to_numeric(df["close"]).values
        if len(c) < 210:
            return None
        e50 = pd.Series(c).ewm(span=REGIME_EMA_FAST, adjust=False).mean().values[-2]
        e200 = pd.Series(c).ewm(span=REGIME_EMA_SLOW, adjust=False).mean().values[-2]
        ck = c[-2]
        if e50 > e200 and ck > e50:
            return "BULL TREND"
        if e50 < e200 and ck < e50:
            return "BEAR TREND"
        return "ROTATION"
    except Exception:
        return None


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
def sig_at(ctf, i, mc=None):
    """Sinyal TF pada index i. mc=None -> pakai sig asli (MIN_COND=4).
    mc=3 (varian E) -> hitung ulang dari bull/bear dgn ambang lebih longgar."""
    if mc is None:
        return int(ctf["sig"][i])
    b = int(ctf["bull"][i]); be = int(ctf["bear"][i])
    return 1 if b >= mc else (-1 if be >= mc else 0)


def scenario_calc(zones15, px, atrv15, volbase15):
    """v1.39 — MESIN ZIGZAG (port 1:1 dari modul scenario Pine):
    pullBias -> scDir (Auto=net pull) -> TRIGGER (zona searah terdekat, score>=2)
    -> REVERSE (retrace 55% + snap ke zona 0.75xATR) -> RETEST (55% leg reverse)
    -> TARGET (zona lawan skor tertinggi / projected mirror) -> EXTENSION.
    Return dict {dir,trig,trigS,rev,ret,tgt,tgtS,ext,anchored,snapped} / None."""
    try:
        leglen = LEFT_BARS + RIGHT_BARS
        # ---- pull bias (mass engine Pine: w = score*(1+log(1+|volAbs|/vBase))) ----
        vbase = volbase15 * max(leglen, 1)
        mass_up = mass_dn = 0.0
        for z in zones15:
            if z.phase == 2:
                continue
            sc = zone_score(z, 0, px, atrv15, volbase15)
            if sc < 0.0:
                continue                       # minScore Pine = 0.0 (hanya hide)
            w = sc * (1.0 + math.log(1.0 + abs(z.vol_abs) / max(vbase, 1.0)))
            if z.dir > 0:
                mass_up += w
            else:
                mass_dn += w
        mtot = mass_up + mass_dn
        share_up = (mass_up / mtot) if mtot > 0 else 0.5
        pull_bias = (share_up - 0.5) * 200.0
        sc_dir = 1 if pull_bias >= 0 else -1   # Auto (net pull)

        def _pick(lvl, side, by_score):
            best = None; bsc = 0.0
            for z in zones15:
                if z.phase == 2:
                    continue
                sc = zone_score(z, 0, px, atrv15, volbase15)
                if sc < SCEN_MIN_SC:
                    continue
                mid = (z.top0 + z.bot0) / 2.0
                ok = mid > lvl if side > 0 else mid < lvl
                if not ok:
                    continue
                better = (best is None or (sc > bsc if by_score
                           else (mid < best if side > 0 else mid > best)))
                if better:
                    best = mid; bsc = sc
            return (best, bsc)

        def _snap(lvl):
            tol = atrv15 * SCEN_SNAP_ATR
            best = None; bsc = 0.0
            if tol > 0:
                for z in zones15:
                    if z.phase == 2:
                        continue
                    sc = zone_score(z, 0, px, atrv15, volbase15)
                    if sc < SCEN_MIN_SC:
                        continue
                    mid = (z.top0 + z.bot0) / 2.0
                    if abs(mid - lvl) <= tol and (best is None
                                                  or abs(mid - lvl) < abs(best - lvl)):
                        best = mid; bsc = sc
            return (best, bsc)

        trig, trig_s = _pick(px, sc_dir, False)
        if trig is None:
            return None
        tgt, tgt_s = _pick(px, -sc_dir, True)
        anchored = tgt is not None
        if not anchored:
            tgt = px - sc_dir * abs(trig - px)
            tgt_s = 0.0
        leg_trig = abs(trig - px)
        rev_raw = trig - sc_dir * leg_trig * (SCEN_REV_PCT / 100.0)
        snap_px, _ = _snap(rev_raw)
        snapped = snap_px is not None
        rev = snap_px if snapped else rev_raw
        ret = rev + sc_dir * abs(trig - rev) * (SCEN_RETEST_PCT / 100.0)
        ext, _ = _pick(tgt, -sc_dir, False)
        return {"dir": sc_dir, "trig": trig, "trigS": trig_s, "rev": rev,
                "ret": ret, "tgt": tgt, "tgtS": tgt_s, "ext": ext,
                "anchored": anchored, "snapped": snapped}
    except Exception:
        return None


def _find_gz_setup(con, trg, zones15, px, atrv15, volbase15, diag=None,
                  variant="G", regime=None):
    """VARIAN G (menu G) — GZ-STOPPOOL (resep user, 2026-09-08):
    SHORT: harga DI ATAS Golden Zone (close 15m > 0.786) & SUDAH menyentuh
    STOP POOL di atas (likuiditas swing high) -> entry SHORT.
    LONG : harga DI BAWAH Golden Zone (close 15m < 0.618) & SUDAH menyentuh
    STOP POOL di bawah (likuiditas swing low) -> entry LONG.
    SL = sisi LUAR zona · TP = zona lawan terdekat (fallback 2.5xATR) · RR >= 1.2.
    Dipilih via menu Varian [G] / env GE_VARIANT=G — berlaku DEMO & REAL.
    v1.40: VARIAN H = G-AMAN = G + syarat 1H (regime) WAJIB searah arah entry
    (LONG butuh BULL TREND · SHORT butuh BEAR TREND · ROTATION/None = SKIP)."""
    try:
        c15 = con.get("15") or {}
        gzl = c15.get("gzl"); gzh = c15.get("gzh")
        if gzl is None or gzh is None or len(gzl) < 2 or len(gzh) < 2:
            if diag is not None:
                diag.append("G: data Golden Zone 15m kurang")
            return None
        gzl = float(gzl[-2]); gzh = float(gzh[-2]); cl = float(c15["close"][-2])
        if gzl != gzl or gzh != gzh or atrv15 <= 0:
            if diag is not None:
                diag.append("G: Golden Zone belum terbentuk / ATR 0")
            return None
        s15 = int(c15["sig"][-2]) if "sig" in c15 else 0
        _b = int(c15["bull"][-2]) if "bull" in c15 else 0
        _be = int(c15["bear"][-2]) if "bear" in c15 else 0
        try:
            s_h1 = (int(con["60"]["sig"][-2]) if con.get("60")
                    and len(con["60"].get("sig", [])) >= 2 else 0)
            s_h4 = (int(con["240"]["sig"][-2]) if con.get("240")
                    and len(con["240"].get("sig", [])) >= 2 else 0)
        except Exception:
            s_h1 = s_h4 = 0
        ap = APPROACH_ATR * atrv15
        idx = len(trg["close"]) - 2
        for d in (1, -1):                      # LONG dulu, lalu SHORT
            # v1.40: G4-AMAN — 1H (regime) WAJIB searah arah entry
            if variant == "H":
                if d == 1 and regime != "BULL TREND":
                    if diag is not None:
                        diag.append(f"LONG: G4-AMAN GAGAL \u2014 1H "
                                    f"{regime or '?'} tidak BULL TREND (syarat G-AMAN)")
                    continue
                if d == -1 and regime != "BEAR TREND":
                    if diag is not None:
                        diag.append(f"SHORT: G4-AMAN GAGAL \u2014 1H "
                                    f"{regime or '?'} tidak BEAR TREND (syarat G-AMAN)")
                    continue
            # R1-G: posisi harga terhadap Golden Zone (bar CLOSED)
            if d == 1:
                if cl >= gzl:
                    if diag is not None:
                        diag.append(f"LONG: G1 GAGAL — close {cl:.6g} belum DI BAWAH "
                                    f"GZ 0.618 ({gzl:.6g})")
                    continue
            else:
                if cl <= gzh:
                    if diag is not None:
                        diag.append(f"SHORT: G1 GAGAL — close {cl:.6g} belum DI ATAS "
                                    f"GZ 0.786 ({gzh:.6g})")
                    continue
            # R2-G: STOP POOL searah & harga SUDAH menyentuh zona
            if d == -1:   # SHORT: stop pool swing HIGH di atas harga
                cands = [z for z in zones15 if z.kind == 1 and z.dir == 1
                         and z.phase != 2
                         and (z.top0 + z.bot0) / 2.0 > px
                         and px >= z.bot - ap]
            else:         # LONG: stop pool swing LOW di bawah harga
                cands = [z for z in zones15 if z.kind == 1 and z.dir == -1
                         and z.phase != 2
                         and (z.top0 + z.bot0) / 2.0 < px
                         and px <= z.top + ap]
            if not cands:
                if diag is not None:
                    diag.append(f"{'SHORT' if d == -1 else 'LONG'}: G2 GAGAL — harga "
                                f"belum mencapai STOP POOL searah (px {px:.6g})")
                continue
            near = (min(cands, key=lambda z: (z.top0 + z.bot0) / 2.0) if d == -1
                    else max(cands, key=lambda z: (z.top0 + z.bot0) / 2.0))
            # R3-G: SL sisi luar zona · TP = zona lawan terdekat · RR
            if d == 1:
                ssl = near.bot - SL_BUFFER_ATR * atrv15
                opp = [z for z in zones15 if z.dir == 1 and z.phase != 2 and z.top0 > px]
                tp = min((z.bot for z in opp), default=None) if opp else None
            else:
                ssl = near.top + SL_BUFFER_ATR * atrv15
                opp = [z for z in zones15 if z.dir == -1 and z.phase != 2 and z.bot0 < px]
                tp = max((z.top for z in opp), default=None) if opp else None
            if tp is None:
                tp = px + d * FALLBACK_TP_ATR * atrv15
            # v1.39: varian G ikut TARGET zigzag (bila searah & lebih dekat -> realistis)
            try:
                _scG = scenario_calc(zones15, px, atrv15, volbase15)
            except Exception:
                _scG = None
            if _scG and _scG.get("dir") == d and _scG.get("tgt") is not None:
                _tg = float(_scG["tgt"])
                if abs(_tg - px) < abs(tp - px):
                    tp = _tg
            rr = abs(tp - px) / abs(px - ssl) if abs(px - ssl) > 0 else 0.0
            if rr < MIN_RR:
                if diag is not None:
                    diag.append(f"{'SHORT' if d == -1 else 'LONG'}: G3 GAGAL — rr {rr:.2f} "
                                f"< {MIN_RR} (TP {tp:.6g} / SL {ssl:.6g})")
                continue
            tp2 = None
            if d == 1:
                opp2 = [z for z in zones15 if z.dir == 1 and z.phase != 2 and z.bot > tp + 1e-12]
                tp2 = min((z.bot for z in opp2), default=None) if opp2 else None
            else:
                opp2 = [z for z in zones15 if z.dir == -1 and z.phase != 2 and z.top < tp - 1e-12]
                tp2 = max((z.top for z in opp2), default=None) if opp2 else None
            return {"dir": d, "zone": near, "sl": ssl, "tp": tp, "tp1": tp,
                    "tp2": tp2, "rr": rr, "sig15": s15,
                    "sig_h1": s_h1, "sig_h4": s_h4,
                    "variant": variant, "thr": 0.0, "conf15": max(_b, _be),
                    "zone_score": zone_score(near, idx, px, atrv15, volbase15),
                    "scalp": False}
    except Exception:
        log.exception("_find_gz_setup")
        return None


def find_setup(con, trg, zones15, px, atrv15, volbase15, prev_sig15,
               variant=None, regime=None, diag=None):
    """R1: 1H & 4H setuju. R2: zona STRONG (>=6.5) & harga mengetuk.
    R2_REVIVE: zona phase==2 boleh dipakai bila tersapu <=R2_REVIVE_BARS bar lalu.
    R3: 15M FLIP searah PADA BAR YG BERADA DI ZONA (hi/lo bar tutup menyentuh zona).
    Varian (mode 4 PRO): B=REGIME (filter tren), C=ELITE (>=8.0), D=RETEST (tests>=2),
    E=AGRESIF (sinyal TF 3/4, zona >=5.5, RR >=1.0), G=GZ-STOPPOOL (lihat _find_gz_setup),
    H=G-AMAN (G + regime 1H wajib searah arah entry).
    Return dict setup atau None.
    diag (opsional): list str — alasan GATE mana yg mematikan kandidat (utk diagnostik)."""
    v = variant if variant else VARIANT
    if v in ("G", "H"):                        # v1.38 G · v1.40 H=G-AMAN
        return _find_gz_setup(con, trg, zones15, px, atrv15, volbase15, diag,
                              v, regime)
    mc = E_SIG_MIN if v == "E" else None        # E: sinyal TF cukup 3/4
    zthr = E_ZONE_MIN if v == "E" else (ELITE_THR if v in ("C", "F") else ZONE_MIN_SCORE)
    rrmin = E_MIN_RR if v == "E" else MIN_RR
    for d in (1, -1):                 # cek LONG dulu, lalu SHORT
        sig_h1 = sig_at(con["60"], -2, mc)
        sig_h4 = sig_at(con["240"], -2, mc)
        sig15 = sig_at(con["15"], -2, mc)
        if R1_MODE == "LONGGA":
            # v1.33: R1 LONGGA — cukup 1H searah; 4H diabaikan (tambahan menu)
            if sig_h1 != d:
                if diag is not None:
                    diag.append(f"{'LONG' if d==1 else 'SHORT'}: R1 LONGGA GAGAL — 1H "
                                f"tidak searah (sig 1H {sig_h1:+d} · 4H "
                                f"{sig_h4:+d} diabaikan)")
                continue
        elif sig_h1 != d or sig_h4 != d:
            if diag is not None:
                diag.append(f"{'LONG' if d==1 else 'SHORT'}: R1 GAGAL — 1H/4H tidak searah "
                            f"(sig 1H {sig_h1:+d} · 4H {sig_h4:+d})")
            continue
        # ---- v1.34: R1b — 15m FLIP dalam R1B_FLIP_WINDOW bar terakhir ----
        # Video: "the 15-minute flips right there at the zone. Not before."
        # Fakta: sinyal 4/4 15m lahir 1-3 bar SETELAH bar reversal (low di zona),
        # jadi wajib "bar ini flip" membuang SEMUA kandidat valid -> 0 entry.
        _R1B_W = R1B_FLIP_WINDOW if R1B_FLIP_WINDOW > 0 else 0
        _flip_at = None
        _ns = len(con["15"]["sig"])
        if _R1B_W > 0:
            if sig15 == d:
                for _k in range(_ns - 2, max(_ns - 2 - _R1B_W, 0) - 1, -1):
                    if sig_at(con["15"], _k - _ns, mc) != d:
                        _flip_at = _k + 1          # bar flip = bar pertama setelah != d
                        break
            if _flip_at is None:
                if diag is not None:
                    diag.append(f"{'LONG' if d==1 else 'SHORT'}: R1 GAGAL — 15M belum "
                                f"FLIP dalam {_R1B_W} bar terakhir (sig15 {sig15:+d} · "
                                f"prev {prev_sig15:+d})")
                continue                  # 15M belum FLIP ke arah d (atau sudah lama)
        elif sig15 != d or prev_sig15 == d:
            if diag is not None:
                diag.append(f"{'LONG' if d==1 else 'SHORT'}: R1 GAGAL — 15M belum FLIP "
                            f"(sig15 {sig15:+d} · prev {prev_sig15:+d})")
            continue                  # 15M belum FLIP ke arah d (atau sudah lama)
        # ---- varian B: REGIME (tren EMA50/200, konteks resmi Pine) ----
        if v in ("B", "F"):
            if regime is None:
                if diag is not None:
                    diag.append(f"{'LONG' if d==1 else 'SHORT'}: varian B — data tren kurang")
                continue                        # data tak cukup -> jangan entry
            if d == 1 and regime != "BULL TREND":
                if diag is not None:
                    diag.append(f"LONG: {'varian B/F' if v == 'F' else 'varian B'} — "
                                f"regime bukan BULL TREND ({regime})")
                continue
            if d == -1 and regime != "BEAR TREND":
                if diag is not None:
                    diag.append(f"SHORT: {'varian B/F' if v == 'F' else 'varian B'} — "
                                f"regime bukan BEAR TREND ({regime})")
                continue
        # ---- R2: zona terdekat searah dgn skor >= threshold (6.5 / 8.0 utk C) ----
        thr = zthr
        _idxz = len(trg["close"]) - 2
        # v1.34: R2_REVIVE_BARS — zona yang BARU disapu (phase 2) tetap boleh dipakai
        # bila sweep terjadi <= R2_REVIVE_BARS bar lalu (sweep & reverse / liquidity
        # grab). Bukti simulasi: tanpa ini, pada momen flip+TF searah semua zona
        # dekat harga ber-phase 2 -> 0 entry. Pine display tetap menandai
        # FILLED/SWEPT; hanya aturan ENTRY yang memakai jendela revive.
        _rev = R2_REVIVE_BARS if R2_REVIVE_BARS > 0 else 0
        cands = [z for z in zones15
                 if z.dir == -d
                 and (z.phase != 2 or (_rev > 0 and z.phase == 2
                                       and (_idxz - z.last) <= _rev))
                 and zone_score(z, _idxz, px, atrv15, volbase15) >= thr]
        if v in ("D", "F"):
            cands = [z for z in cands if z.tests >= RETEST_MIN_TESTS]   # zona teruji (D & F)
        if not cands:
            if diag is not None:
                diag.append(f"{'LONG' if d==1 else 'SHORT'}: R2 GAGAL — tak ada zona "
                            f"searah skor >= {thr} (inkl. revive <= {R2_REVIVE_BARS} bar; "
                            f"semua zone skor maks "
                            f"{max([zone_score(z, len(trg['close'])-2, px, atrv15, volbase15) for z in zones15 if z.dir == -d], default=0.0):.1f})")
            continue
        if d == 1:
            near = max(cands, key=lambda z: (z.top0 + z.bot0) / 2.0)   # demand terdekat DI BAWAH
            if (near.top0 + near.bot0) / 2.0 > px:
                if diag is not None:
                    diag.append("LONG: R2 GAGAL — zona demand terdekat masih DI ATAS "
                                "harga (belum turun ke zona)")
                continue
        else:
            near = min(cands, key=lambda z: (z.top0 + z.bot0) / 2.0)   # supply terdekat DI ATAS
            if (near.top0 + near.bot0) / 2.0 < px:
                if diag is not None:
                    diag.append("SHORT: R2 GAGAL — zona supply terdekat masih DI BAWAH "
                                "harga (belum naik ke zona)")
                continue
        # harga (close) HARUS di/pada zona: +- APPROACH_ATR x ATR
        ap = APPROACH_ATR * atrv15
        if not R2_USE_TOUCH and not (near.bot - ap <= px <= near.top + ap):
            if diag is not None:
                diag.append(f"{'LONG' if d==1 else 'SHORT'}: R2 GAGAL — harga TIDAK "
                            f"mengetuk zona (jarak ke zona "
                            f"{(near.top-near.bot)/2 - px if d==1 else px - (near.top+near.bot)/2:+.2f} vs ambang {ap:.2f})")
            continue
        # VIDEO (presisi R3): bar 15M yang FLIP harus BERADA DI ZONA —
        # "the 15-minute flips right there at the zone. Not before."
        # LONG: low bar flip masuk ke zona demand; SHORT: high bar flip masuk ke zona supply.
        # (Sentuhan via hi/lo bar tutup = konsisten dgn update_zones & Pine touching.)
        if d == 1:
            if _R1B_W > 0 and _flip_at is not None:
                _low_flip = min(float(x) for x in con["15"]["lo"][_flip_at:_ns - 1])
            else:
                _low_flip = float(con["15"]["lo"][-2])
            if _low_flip > near.top + 1e-12:
                if diag is not None:
                    diag.append("LONG: R3 GAGAL — bar flip TIDAK menyentuh zona "
                                f"(low flip {_low_flip:.6g} > top zona {near.top:.6g})")
                continue                    # flip terjadi SEBELUM harga sampai di zona
        else:
            if _R1B_W > 0 and _flip_at is not None:
                _hi_flip = max(float(x) for x in con["15"]["hi"][_flip_at:_ns - 1])
            else:
                _hi_flip = float(con["15"]["hi"][-2])
            if _hi_flip < near.bot - 1e-12:
                if diag is not None:
                    diag.append("SHORT: R3 GAGAL — bar flip TIDAK menyentuh zona "
                                f"(high flip {_hi_flip:.6g} < bot zona {near.bot:.6g})")
                continue                    # flip terjadi SEBELUM harga sampai di zona
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
        # v1.39: VARIAN F = F-SMART — SL/TP mengikuti garis zigzag scenario:
        # SL = sisi luar TRIGGER · TP = TARGET · TP2 = EXTENSION (bila harga
        # sudah di TRIGGER/RETEST & RR masih layak — tetap klasik bila tidak).
        if v == "F":
            _scF = scenario_calc(zones15, px, atrv15, volbase15)
            if _scF and _scF.get("dir") == d and _scF.get("trig") is not None:
                _apF = APPROACH_ATR * atrv15
                _at_trig = abs(px - float(_scF["trig"])) <= _apF * 1.5
                _at_ret = (abs(px - float(_scF["ret"])) <= _apF * 1.5
                           if _scF.get("ret") is not None else False)
                _sls = float(_scF["trig"]) - d * SL_BUFFER_ATR * atrv15
                _tps = float(_scF["tgt"])
                _rrs = abs(_tps - px) / abs(px - _sls) if abs(px - _sls) > 0 else 0.0
                if (_at_trig or _at_ret) and _rrs >= rrmin and abs(px - _sls) > 0:
                    ssl, tp = _sls, _tps            # F-SMART: ikuti zigzag
        rr = abs(tp - px) / abs(px - ssl) if abs(px - ssl) > 0 else 0.0
        if rr < rrmin:
            if diag is not None:
                diag.append(f"{'LONG' if d==1 else 'SHORT'}: RR GAGAL — rr {rr:.2f} < "
                            f"{rrmin} (TP {tp:.6g} / SL {ssl:.6g})")
            continue
        # ---- TP2 utk RIDE: zona lawan KE-2; cadangan: TP1 + 1x jarak TP1 ----
        tp2 = None
        if v == "F" and (_scF is not None and _scF.get("dir") == d
                         and _scF.get("ext") is not None):
            tp2 = float(_scF["ext"])            # v1.39: TP2 = EXTENSION zigzag
        elif d == 1:
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
                "variant": v, "thr": thr,
                "conf15": con["15"]["bull"][-2] if d == 1 else con["15"]["bear"][-2],
                "zone_score": zone_score(near, len(trg["close"]) - 2, px, atrv15, volbase15)}
    return None

# ==================== EKSEKUSI & MANAJEMEN ====================
ENTRY_MARGIN_DEFAULT = 1.0            # margin cadangan bila lev*SL% = 0

def find_scalp_setup(con, trg, zones15, px, atrv15, volbase15, prev_sig15, diag=None):
    """MODE 6 SCALPER: 3 aturan pada TF 5m/15m/60m (ambang longgar seperti varian E:
    sig 3/4 · zona >= 5.5 · RR >= 1.0 dari zona), lalu TP/SL di-override ke % TETAP
    (bukan zona lawan) agar keluar cepat & konsisten. find_setup A-E TIDAK diubah —
    fungsi ini memanggilnya di atas. Return setup (key "scalp": True) atau None."""
    base = find_setup(con, trg, zones15, px, atrv15, volbase15, prev_sig15,
                      "E", None, diag)
    if base is None:
        return None
    d = base["dir"]
    sl = px - d * (SCALP_SL_PCT / 100.0) * px
    tp = px + d * (SCALP_TP_PCT / 100.0) * px
    rr = SCALP_TP_PCT / SCALP_SL_PCT
    if rr < SCALP_MIN_RR:
        return None
    tp2 = tp + d * TP_EXT_MULT * abs(tp - px)
    base.update({"sl": sl, "tp": tp, "tp2": tp2, "rr": rr, "scalp": True})
    return base


def _is_doji(o, h, l, c):
    """Doji LONG-LEGGED (video + literatur): body <= DOJI_BODY_RATIO x range,
    tiap kaki >= DOJI_WICK_RATIO x range; posisi body bebas (atas/bawah/tengah)."""
    rng = h - l
    if rng <= 0:
        return False
    body = abs(c - o)
    if body > DOJI_BODY_RATIO * rng:
        return False
    uw = h - max(o, c)
    lw = min(o, c) - l
    return uw >= DOJI_WICK_RATIO * rng and lw >= DOJI_WICK_RATIO * rng


def _doji_type(o, h, l, c):
    """v1.35: klasifikasi TIPE doji (referensi TradingView «The Doji Candle
    Pattern» — QuantVue). Semua relatif thd range = H-L:
    DRAGONFLY  : upper <=15% & lower >=50%  -> 'T'  , bias BUY (penjualan ditolak)
    GRAVESTONE : lower <=15% & upper >=50%  -> '⊥'  , bias SELL (pembelian ditolak)
    LONG-LEGGED: upper >=30% & lower >=30%  -> '✚'  (aturan lama _is_doji)
    NEAR       : salah satu kaki 15-30%     -> butuh arah via sweep (aturan video)
    None       : bukan doji (body > DOJI_BODY_RATIO x range)."""
    rng = h - l
    if rng <= 0:
        return None
    if abs(c - o) > DOJI_BODY_RATIO * rng:
        return None
    uw = h - max(o, c)
    lw = min(o, c) - l
    if uw <= DOJI_WICK_RATIO_EXT * rng and lw >= DOJI_WICK_MAIN_EXT * rng:
        return "DRAGONFLY"
    if lw <= DOJI_WICK_RATIO_EXT * rng and uw >= DOJI_WICK_MAIN_EXT * rng:
        return "GRAVESTONE"
    if uw >= DOJI_WICK_RATIO * rng and lw >= DOJI_WICK_RATIO * rng:
        return "LONG-LEGGED"
    if uw >= DOJI_WICK_RATIO_EXT * rng and lw >= DOJI_WICK_RATIO_EXT * rng:
        return "NEAR"
    return None


def _tf_structure_dir(df):
    """Arah struktur fractal satu TF (bias MTF): 1 up, -1 down, 0 netral/kurang data."""
    try:
        h = pd.to_numeric(df["high"]).values
        l = pd.to_numeric(df["low"]).values
        hs, ls = _swing_idx(h, l, FIB_SWING)
        if len(hs) < 2 or len(ls) < 2:
            return 0
        if l[ls[-1]] > l[ls[-2]] and h[hs[-1]] > h[hs[-2]]:
            return 1
        if l[ls[-1]] < l[ls[-2]] and h[hs[-1]] < h[hs[-2]]:
            return -1
        return 0
    except Exception:
        return 0


def find_doji_setup(trg, px, atrv, i, diag=None, bias=None):
    """MODE 7 (DOJI BREAKOUT, XAUUSDT 5m / M5 — video ThisIsDaryl
    'Bisa dipakai di tf entry'). Aturan PERSIS video:
    1) bar i = DOJI (bar CLOSED; body kecil, kaki dominan — posisi body bebas).
    2) KONFIRMASI (KRUSIAL) vs candle i-1: doji menyapu LOW candle sebelumnya
       -> HANYA BUY; menyapu HIGH -> HANYA SELL; menyapu DUA-DUANYA -> bebas;
       TIDAK menyapu sama sekali -> SKIP (video: 'kita gak boleh entry').
    3) Entry saat TOUCH (video: 'nyentuh aja, enggak usah tunggu close'): harga
       menyentuh high doji = BUY, low doji = SELL. 4) SL = sisi lawan doji
       (min DOJI_SL_PCT). 5) RR = 1:1.5 ('risk ratio 1 banding 1,5').
    Return dict setup (format try_entry) berisi doji_ts utk gate sekali-per-doji."""
    try:
        if i < 3 or atrv <= 0:
            if diag is not None:
                diag.append("data kurang (bar<3 / ATR 0)")
            return None
        o = float(trg["open"].iloc[i])
        h = float(trg["high"].iloc[i])
        l = float(trg["low"].iloc[i])
        c = float(trg["close"].iloc[i])
        ph = float(trg["high"].iloc[i - 1])
        pl = float(trg["low"].iloc[i - 1])
        typ = _doji_type(o, h, l, c)
        if typ is None:
            if diag is not None:
                diag.append("bar terakhir BUKAN doji (body>10% atau bentuk tak dikenali)")
            return None
        rng = h - l
        # v1.35: DRAGONFLY/GRAVESTONE cukup 0.7xATR; LONG-LEGGED/NEAR tetap 1xATR
        _rng_min = (DOJI_RANGE_ATR_MIN_DF if typ in ("DRAGONFLY", "GRAVESTONE")
                    else DOJI_RANGE_ATR_MIN)
        if rng < _rng_min * atrv:
            if diag is not None:
                diag.append(f"doji {typ} terlalu pendek (range < {_rng_min}xATR)")
            return None              # doji pendek utk tipe ini -> SKIP
        sweep_low = l < pl           # doji menyapu low candle sebelumnya
        sweep_high = h > ph          # doji menyapu high candle sebelumnya
        if not sweep_low and not sweep_high:
            if diag is not None:
                diag.append("doji TIDAK menyapu high/low candle sebelumnya (aturan video: SKIP)")
            return None              # di dalam range candle sblmnya -> SKIP
        px = float(px)
        # v1.35 (referensi TradingView QuantVue): DRAGONFLY -> bias BUY (penjualan
        # ditolak, rebound); GRAVESTONE -> bias SELL (pembelian berbalik jadi
        # jualan). LONG-LEGGED/NEAR -> aturan video (sweep low=BUY, high=SELL).
        if typ == "DRAGONFLY":
            d = 1
        elif typ == "GRAVESTONE":
            d = -1
        elif sweep_low and not sweep_high:
            d = 1
        elif sweep_high and not sweep_low:
            d = -1
        else:                        # sweep dua-duanya -> bebas, ikut posisi harga
            d = 0
        if d == 0:
            if px > h:
                d = 1                # sweep dua-duanya -> bebas
            elif px < l:
                d = -1
            else:
                if diag is not None:
                    diag.append("doji sweep dua-duanya; harga belum touch high/low doji")
                return None          # belum touch level mana pun
        if d == 1 and px <= h:       # TOUCH: harga harus sudah di atas high doji
            if diag is not None:
                diag.append(f"doji {typ} -> LONG; harga belum menyentuh high doji")
            return None
        if d == -1 and px >= l:
            if diag is not None:
                diag.append(f"doji {typ} -> SHORT; harga belum menyentuh low doji")
            return None
        if bias is not None and bias != 0 and d != bias:
            if diag is not None:
                diag.append(f"DOJI MTF: arah doji {'LONG' if d == 1 else 'SHORT'} vs "
                            f"tren 60m {'LONG' if bias == 1 else 'SHORT'} TIDAK searah "
                            f"— SKIP")
            return None
        sl_dist = max(rng, px * DOJI_SL_PCT / 100.0)
        entry = px
        sl = entry - d * sl_dist     # sisi lawan doji (min DOJI_SL_PCT)
        tp = entry + d * sl_dist * DOJI_RR_TP1
        tp2 = entry + d * sl_dist * DOJI_RR_TP2
        if d == 1:
            zone = Zone(0, -1, entry, sl, 0, 0.0, 0.0)
        else:
            zone = Zone(0, 1, sl, entry, 0, 0.0, 0.0)
        return {"dir": d, "zone": zone, "sl": sl, "tp": tp, "tp1": tp, "tp2": tp2,
                "rr": DOJI_RR_TP1, "sig15": d, "sig_h1": d, "sig_h4": d,
                "variant": "DOJI", "thr": 0.0, "conf15": 4, "zone_score": 8.0,
                "scalp": True, "doji_ts": int(trg["ts"].iloc[i]),
                "doji_type": typ}
    except Exception as e:
        log.error(f"find_doji_setup: {e}")
        return None


def _swing_idx(h, l, w):
    """Indeks pivot fractal (w bar kiri & kanan): swing high & swing low."""
    hs, ls = [], []
    n = len(h)
    for k in range(w, n - w):
        if h[k] == max(h[k - w:k + w + 1]) and h[k] > max(h[k - w:k]) and \
           h[k] > max(h[k + 1:k + w + 1]):
            hs.append(k)
        if l[k] == min(l[k - w:k + w + 1]) and l[k] < min(l[k - w:k]) and \
           l[k] < min(l[k + 1:k + w + 1]):
            ls.append(k)
    return hs, ls


def find_fib_setup(trg, struc, px, atrv, i, diag=None, struc2=None):
    """MODE 8 (FIB TREND SCALP, XAUUSDT 30m — video 'Keep It Simple, Make It Profitable'):
    1) Tren via STRUCTURE pada struc (30m; pemanggil fallback ke 60m bila
       struktur 30m sudah 'tua'): HH+HL = uptrend, LL+LH = downtrend.
    2) "TITIK TREN BARU": swing terakhir wajib <= FIB_SWING_AGE bar dari ujung —
       lebih tua berarti tren basi -> None (pemanggil boleh coba TF lebih tinggi).
    3) Fib ditarik low->high (uptrend); entry saat harga retrace KE ZONA DISKON
       50%-61.8% lalu tutup di atas 61.8% (video: 'entry below the 50% level').
    4) SL di luar swing low TERAKHIR; TP1 = 1R, TP2 = 1.5R ('let it run').
    SHORT = kebalikan (high->low). Return dict setup atau None."""
    try:
        h = pd.to_numeric(struc["high"]).values
        l = pd.to_numeric(struc["low"]).values
        hs, ls = _swing_idx(h, l, FIB_SWING)
        if len(hs) < 2 or len(ls) < 2:
            if diag is not None:
                diag.append("swing fractal < 2 (data struktur belum cukup)")
            return None
        # "titik tren baru": swing terakhir wajib fresh (bukan tren basi)
        if len(h) - 1 - max(hs[-1], ls[-1]) > FIB_SWING_AGE:
            if diag is not None:
                diag.append("swing terakhir TUA (>%d bar) - titik tren baru tidak valid" % FIB_SWING_AGE)
            return None
        H1, H2 = hs[-2], hs[-1]
        L1, L2 = ls[-2], ls[-1]
        uptrend = float(l[L2]) > float(l[L1]) and float(h[H2]) > float(h[H1])
        downtrend = float(l[L2]) < float(l[L1]) and float(h[H2]) < float(h[H1])
        if not uptrend and not downtrend:
            if diag is not None:
                diag.append("tidak ada struktur tren HH/HL (LONG) atau LL/LH (SHORT)")
            return None
        if struc2 is not None:
            # MTF (FIB8M): struktur TF 30m wajib TIDAK melawan tren 60m (zona/tren
            # utama dari 60m; 30m hanya timing). Beda arah = SKIP (bukan konfluensi).
            try:
                h2 = pd.to_numeric(struc2["high"]).values
                l2 = pd.to_numeric(struc2["low"]).values
                hs2, ls2 = _swing_idx(h2, l2, FIB_SWING)
                if len(hs2) >= 2 and len(ls2) >= 2:
                    _u2 = (float(l2[ls2[-1]]) > float(l2[ls2[-2]])
                           and float(h2[hs2[-1]]) > float(h2[hs2[-2]]))
                    _d2 = (float(l2[ls2[-1]]) < float(l2[ls2[-2]])
                           and float(h2[hs2[-1]]) < float(h2[hs2[-2]]))
                    if uptrend and _d2:
                        if diag is not None:
                            diag.append("MTF: struktur 30m DOWntrend melawan 60m "
                                        "uptrend — SKIP")
                        return None
                    if downtrend and _u2:
                        if diag is not None:
                            diag.append("MTF: struktur 30m UPtrend melawan 60m "
                                        "downtrend — SKIP")
                        return None
            except Exception:
                pass
        close = float(px)
        low_b = float(trg["low"].iloc[i])
        high_b = float(trg["high"].iloc[i])
        if uptrend:
            lo = min(float(l[L1]), float(l[L2]))
            hi = max(float(h[H1]), float(h[H2]))
            span = hi - lo
            if span <= 0:
                return None
            f618 = lo + span * FIB_HI
            if not (low_b <= f618 and close > f618):   # sentuh zona diskon & mantul
                if diag is not None:
                    diag.append("uptrend OK tapi harga belum sentuh zona diskon 50-61.8% lalu mantul")
                return None
            entry = close
            risk = entry - (float(l[L2]) - 0.25 * atrv)          # SL di luar low terakhir
            risk = max(min(risk, entry * FIB_MAX_SL_PCT / 100.0),
                       entry * FIB_MIN_SL_PCT / 100.0)
            sl = entry - risk
            tp = entry + risk * FIB_RR_TP1
            tp2 = entry + risk * FIB_RR_TP2
            zone = Zone(0, -1, entry, sl, 0, 0.0, 0.0)
            d = 1
        else:
            lo = min(float(l[L1]), float(l[L2]))
            hi = max(float(h[H1]), float(h[H2]))
            span = hi - lo
            if span <= 0:
                return None
            f618 = hi - span * FIB_HI
            if not (high_b >= f618 and close < f618):
                if diag is not None:
                    diag.append("downtrend OK tapi harga belum sentuh zona diskon 50-61.8% lalu mantul")
                return None
            entry = close
            risk = (float(h[H2]) + 0.25 * atrv) - entry
            risk = max(min(risk, entry * FIB_MAX_SL_PCT / 100.0),
                       entry * FIB_MIN_SL_PCT / 100.0)
            sl = entry + risk
            tp = entry - risk * FIB_RR_TP1
            tp2 = entry - risk * FIB_RR_TP2
            zone = Zone(0, 1, sl, entry, 0, 0.0, 0.0)
            d = -1
        return {"dir": d, "zone": zone, "sl": sl, "tp": tp, "tp1": tp, "tp2": tp2,
                "rr": FIB_RR_TP1, "sig15": d, "sig_h1": d, "sig_h4": d,
                "variant": "FIB", "thr": 0.0, "conf15": 4, "zone_score": 8.0,
                "scalp": True}
    except Exception as e:
        log.error(f"find_fib_setup: {e}")
        return None


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
            "realized": 0.0, "scale_mode": False,
            "pends": [], "_react": [0, 0],          # mekanisme reaksi Pine (reactHit/Tot)
            "vol_until": 0.0, "vol_reason": ""}     # GUARD VOLATILITAS PER-SIMBOL

STATES = {}
STATS = load_json(STATS_FILE, {})
if not isinstance(STATS, dict):
    STATS = {}
_orphan_seen = {}          # (sym, side, size) terakhir → peringatan ORPHAN sekali per keadaan
MFE_LOG = load_json(MFE_FILE, [])
if not isinstance(MFE_LOG, list):
    MFE_LOG = []
DAY = load_json(DAY_FILE, {"date": "", "n": 0, "w": 0, "pnl": 0.0})
if not isinstance(DAY, dict):
    DAY = {"date": "", "n": 0, "w": 0, "pnl": 0.0}

def trade_kind():
    """Kategori statistik: 'SCALP' (mode 6) | 'DOJI' (mode 7) | 'FIB' (mode 8)
    atau 'VAR<X>' (varian A-H, mode 1-5). Memisahkan win rate & PnL per strategi."""
    if SUBMODE == "SCALPER":
        return "SCALP"
    if SUBMODE in ("DOJI7", "DOJI30", "DOJIM"):
        return "DOJI"
    if SUBMODE in ("FIB8", "FIB8M"):
        return "FIB"
    return "VAR" + (VARIANT or "A")


def stats_variant_summary():
    """Agregat win rate & PnL PER VARIAN (VARA..VARF + SCALP) dari STATS.
    Return {var: {"n","w","pnl"}} hanya utk varian yang punya trade."""
    out = {}
    for k, v in STATS.items():
        if "|" not in k:
            continue
        kind = k.split("|", 1)[1]
        if not (kind.startswith("VAR") or kind in ("SCALP", "DOJI", "FIB")):
            continue
        o = out.setdefault(kind, {"n": 0, "w": 0, "pnl": 0.0})
        o["n"] += int(v.get("n", 0) or 0)
        o["w"] += int(v.get("w", 0) or 0)
        o["pnl"] = round(o["pnl"] + float(v.get("pnl", 0.0) or 0.0), 4)
    return out


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

def lev_standard(sym):
    """v1.33: STANDAR leverage kelas simbol (MAJOR = BTC/ETH/SOL, lainnya ALT).
    Aturan TUNGGAL -> berlaku SAMA untuk akun REAL maupun DEMO."""
    try:
        if (sym or "").upper() in MAJOR_SYMS:
            return LEV_STD_MAJOR, "MAJOR"
    except Exception:
        pass
    return LEV_STD_ALT, "ALT"


def smart_leverage(sym, entry, sl, std=None):
    """Leverage AMAN: jarak likuidasi = LEV_SL_GAP x jarak SL (+ 1.5% cadangan
    maintenance margin & fee) -> SL SELALU tersentuh duluan, bukan likuidasi.
    v1.33: std (opsional) = standar kelas simbol; hasil = min(aman, std) —
    keamanan tidak pernah dilanggar, hanya bisa lebih kecil (lebih konservatif)."""
    dist = abs(entry - sl) / entry if entry else 0.05
    if dist <= 0:
        dist = 0.05
    lev_aman = 1.0 / (dist * LEV_SL_GAP + LEV_MR_PCT)
    ex_min, ex_max = get_lev_limits(sym)
    hi = min(MAX_LEVERAGE, ex_max)
    lo = max(MIN_LEVERAGE, ex_min)
    lev = int(min(hi, max(lo, math.floor(lev_aman))))
    if std:
        lev = int(max(lo, min(lev, std)))
    return lev

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

def orphan_check(scan_syms):
    """Cek posisi di BURSA yang tidak dikenal STATE bot (entry gagal konfirmasi /
    order yatim / posisi manual). Peringatan besar di dashboard — sekali per
    keadaan (sym+side+size), supaya tidak spam, tapi TIDAK pernah diam-diam."""
    for sym in scan_syms:
        st = STATES.get(sym) or {}
        if st.get("in_position"):
            continue
        try:
            pl = session.get_positions(category="linear", symbol=sym)["result"]["list"]
            p = pl[0] if pl else None
            size = float((p or {}).get("size") or 0)
        except Exception:
            continue
        if size > 0:
            side = (p or {}).get("side", "?")
            _k = (sym, side, size)
            if _orphan_seen.get(sym) == _k:
                continue
            _orphan_seen[sym] = _k
            say(f"{R}⚠ ORPHAN {sym} — posisi {side} {size:.8g} ADA di bursa tapi "
                f"TIDAK dikenal bot (entry tak terkonfirmasi / manual). "
                f"Cek Bybit & pasang SL/TP — bot TIDAK mengelola posisi ini!{X}")
            log.error(f"ORPHAN {sym}: side {side} size {size} "
                      f"avg {(p or {}).get('avgPrice')} — tidak dikelola bot")
        else:
            _orphan_seen.pop(sym, None)


def try_entry(sym, s, setup, balance, n_open, atrv):
    if s["in_position"]:
        return
    _cd = DOJI_COOLDOWN_MIN if SUBMODE in ("DOJI7", "DOJI30", "DOJIM") else \
          (FIB_COOLDOWN_MIN if SUBMODE in ("FIB8", "FIB8M") else COOLDOWN_MIN)
    if time.time() - s.get("last_exit", 0) < _cd * 60:
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
    # ---- GUARD: news/CPI global + VOLATILITAS per-simbol -> entry dijeda ----
    bloc, why = entry_blocked(sym, s)
    if bloc:
        say(f"{R}⚠ {sym} entry ditunda — {why}{X}")
        return
    tp_pct = abs(tp - px) / px * 100
    _tpmin = 0.25 if SUBMODE in ("DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M") else (FEE_RT_PCT + 2 * SLIP_PCT) * 2
    if tp_pct < _tpmin:
        say(f"{Y}⊘ {sym} TP terlalu dekat ({tp_pct:.3f}%) — tak layak biaya{X}")
        return
    cap = min(RISK_CAP_USD, RISK_HARD_USD)
    balance = balance or 1.0
    _lstd, _ltier = lev_standard(sym)                      # v1.33: standar kelas
    lev = smart_leverage(sym, px, sl, _lstd)                # SL dulu + cap standar
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
            log.info(f"{sym} lev {lev}x (std {_ltier} {_lstd}x \u00b7 akun "
                     f"{ENV_KIND} \u00b7 REAL=DEMO)")
        except Exception:
            pass
        try:
            _ord = session.place_order(category="linear", symbol=sym, side=side,
                                       orderType="Market", qty=str(qty),
                                       timeInForce="GTC", positionIdx=0)
        except Exception as _e:
            log.error(f"order {sym}: {_e}")
            say(f"{R}✖ {sym} order Market DITOLAK bursa — {_e}.{X}")
            return
        # konfirmasi posisi: cek ulang beberapa kali (API Bybit kadang lambat);
        # kalau tetap tidak ada -> TAMPILKAN di dashboard (bukan cuma log file).
        p = None
        for _try in range(4):
            time.sleep(1.2)
            p = get_position(sym)
            if p:
                break
        if not p:
            say(f"{R}✖ {sym} order terkirim TAPI posisi TIDAK TERKONFIRMASI "
                f"({_try + 1}x cek / ~5s) — CEK aplikasi Bybit: kalau ada posisi, "
                f"itu TANPA SL/TP (tutup manual / pasang SL segera).{X}")
            log.error(f"✘ {sym} entry tidak terkonfirmasi (order: {_ord})")
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
                  "tp": tp, "kind": trade_kind(), "margin_used": margin, "lev": lev,
                  "risk0": abs(fill - sl), "zone_hi": setup["zone"].top,
                  "zone_lo": setup["zone"].bot, "be_done": False,
                  "trail_on": False, "riding": False,
                  "qty0": qty_fill, "tp1": tp, "tp2": setup.get("tp2") or 0.0,
                  "tp1_done": False, "tp2_done": False,
                  "realized": 0.0, "scale_mode": scale})
        save_json(STATE_FILE, STATES)
        arrow = "▲ LONG" if side == "Buy" else "▼ SHORT"
        say(f"{G if side=='Buy' else R}{arrow}{X} {B}{sym}{X} [{'DOJI-MTF' if SUBMODE == 'DOJIM' else 'DOJI-30' if SUBMODE == 'DOJI30' else 'DOJI-BK' if SUBMODE == 'DOJI7' else 'FIB-MTF' if SUBMODE == 'FIB8M' else 'FIB-TREND' if SUBMODE == 'FIB8' else 'GE-R3'}] @ {fill:.6g} "
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
_vol = {"until": 0.0, "reason": ""}   # legacy: guard volatilitas kini PER-SIMBOL (state)
_vol_batch = []                     # log volatilitas DI-BATCH (1 baris per detak)

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

def vol_guard_check(sym, df15, px15, atrv15, s=None):
    """Guard volatilitas PER-SIMBOL — deteksi pada bar 15m TUTUP (bukan bar live):
    spike satu coin HANYA menunda entry coin itu (simbol lain tetap jalan; posisi
    aktif tetap dikelola). SATU bar spike = SATU jeda (vol_bar) -> jeda benar2
    berakhir (tidak di-refresh terus oleh bar yang sama). Log DI-BATCH."""
    if not VOL_GUARD or atrv15 <= 0:
        return
    try:
        b = len(df15) - 1
        if b < 2:
            return
        cb = b - 1                       # bar 15m TERAKHIR YANG SUDAH TUTUP
        rng = float(df15["high"].iloc[cb] - df15["low"].iloc[cb])
        close = float(df15["close"].iloc[cb])
        prev = float(df15["close"].iloc[cb - 1])
        spike = rng / atrv15
        move = abs(close - prev) / (prev or 1) * 100
        if spike >= VOL_SPIKE_ATR or move >= VOL_MOVE_PCT:
            st = s if s is not None else {}
            now = time.time()
            bar_ts = int(df15["ts"].iloc[cb])
            if now >= (st.get("vol_until") or 0.0) and st.get("vol_bar") != bar_ts:
                st["vol_reason"] = f"{sym} loncat {move:.2f}% ({spike:.1f}xATR)"
                st["vol_bar"] = bar_ts
                st["vol_until"] = now + VOL_PAUSE_MIN * 60
                _vol_batch.append((sym, move, spike))
    except Exception as e:
        log.error(f"vol_guard: {e}")


def flush_vol_log():
    """Cetak SEMUA jeda volatilitas baru dalam SATU baris (anti berisik)."""
    if not _vol_batch:
        return
    n = len(_vol_batch)
    names = ", ".join(f"{sy} +{m:.2f}%" if sp < VOL_SPIKE_ATR
                      else f"{sy} {sp:.1f}xATR"
                      for sy, m, sp in _vol_batch[:3])
    if n > 3:
        names += f", +{n - 3} lagi"
    say(f"{R}⚠ VOLATILITY GUARD — {n} coin dijeda {VOL_PAUSE_MIN}m: {names} · "
        f"coin lain tetap jalan; posisi aktif tetap dikelola{X}")
    _vol_batch.clear()

def entry_blocked(sym=None, st=None):
    """(True, alasan) bila ENTRY BARU dijeda; posisi aktif tetap dikelola.
    NEWS & CPI = GLOBAL (pasar luas). VOLATILITAS = PER-SIMBOL:
    spike coin X hanya menunda entry coin X (st = state simbol tsb)."""
    if NEWS_GUARD and time.time() < _news["until"]:
        return True, (f"NEWS SHOCK ({_news['reason']}) · sisa "
                      f"{max(0, (_news['until'] - time.time()) / 60):.0f}m")
    if CPI_GUARD_ON:
        act, ket = cpi_guard_active()
        if act:
            return True, ket
    if VOL_GUARD and sym and st is not None:
        vt = st.get("vol_until") or 0.0
        if time.time() < vt:
            return True, (f"VOLATILITY ({st.get('vol_reason') or 'spike'}) · sisa "
                          f"{max(0, (vt - time.time()) / 60):.0f}m")
    return False, ""

def choose_mode():
    """Menu mode saat start: 1=ALL COIN, ... 8=FIB TREND SCALP. '0' = keluar.
    Non-tty: env GE_MODE (1-8) + GE_UNIVERSE (1-3) + GE_VARIANT (A-H) + GE_ENV."""
    try:
        if sys.stdin.isatty():
            print(f"\n{B}██ Pilih mode:{X}")
            print(f"   {Y}1{X} = ALL COIN — semua USDT perp likuid otomatis "
                  f"(turnover 24h ≥ ${ALL_MIN_TURNOVER / 1e6:g}jt) · pilih akun")
            print(f"   {Y}2{X} = TOP {TOP_N_CAP} — {TOP_N_CAP} coin USDT paling likuid "
                  f"(turnover tertinggi) · pilih akun")
            print(f"   {Y}3{X} = EMAS SAJA — XAUUSDT · pilih akun")
            print(f"   {Y}4{X} = PRO — pasar (1-3) + varian A-H · pilih akun (DEMO/REAL)")
            print(f"   {Y}6{X} = SCALPER — TF 5m · TP +{SCALP_TP_PCT}% · SL -{SCALP_SL_PCT}% "
                  f"(agresif) · pilih akun")
            print(f"   {Y}7{X} = DOJI BREAKOUT (3m / 30m / MTF 30m+60m) — "
                  f"XAUUSDT · demo / akun real")
            print(f"   {Y}8{X} = FIB TREND (30m / MTF 30m+60m) — XAUUSDT · "
                  f"demo / akun real")
            print(f"   {D}0 = keluar{X}")
            inp = input(f"   Pilihan [0-8] (default {DEFAULT_MODE}): ").strip()
            if inp == "0":
                return None
            if inp == "5":
                print(f"   {G}→ menu 5 dihapus (digabung ke menu 4){X} \u2014 di menu 4 "
                      f"pilih pasar + varian + akun (1=DEMO / 2=REAL).")
                return 4
            if inp in ("1", "2", "3", "4", "6", "7", "8"):
                return int(inp)
            return DEFAULT_MODE
        m = int(os.environ.get("GE_MODE", str(DEFAULT_MODE)))
        return 4 if m == 5 else m      # menu 5 -> 4 (PRO + pilih akun)
    except Exception:
        return DEFAULT_MODE


def ask_pro():
    """Sub-menu PRO: pilih pasar + varian. Return (universe 1-3, variant A-H)."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Pasar:{X}")
            print(f"      {Y}1{X} = ALL COIN          {Y}2{X} = TOP {TOP_N_CAP}          "
                  f"{Y}3{X} = EMAS SAJA")
            print(f"      {D}0 = kembali{X}")
            u = input(f"   Pasar [0/1/2/3] (default {DEFAULT_MODE}): ").strip()
            if u == "0":
                return None
            u = int(u) if u in ("1", "2", "3") else DEFAULT_MODE
            v = ask_variant("A")
            print(f"   \u2192 PRO: {MODE_LABEL[u]} \u00b7 varian {v}-{variant_label(v)} "
                  f"({VARIANTS[v][1]})")
            return u, v
        u = int(os.environ.get("GE_UNIVERSE", str(DEFAULT_MODE)))
        u = u if u in (1, 2, 3) else DEFAULT_MODE
        v = os.environ.get("GE_VARIANT", "A").upper()
        v = v if v in VARIANTS else "A"
        return u, v
    except Exception:
        return DEFAULT_MODE, "A"


def ask_doji_method():
    """Pilih METODE DOJI menu 7: 1 = 3m (video), 2 = 30m, 3 = MTF 30m+60m. Non-tty: GE_DOJI_M."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Metode DOJI:{X}")
            print(f"   {Y}1{X} = DOJI 3m — video ThisIsDaryl (asli)")
            print(f"   {Y}2{X} = DOJI 30m — doji breakout pada 30m")
            print(f"   {Y}3{X} = DOJI MTF 30m+60m — doji 30m + BIAS tren 60m (BARU)")
            print(f"   {D}0 = kembali{X}")
            inp = input("   Metode [0-3] (default 1): ").strip()
            if inp == "0":
                return None
            if inp in ("1", "2", "3"):
                return int(inp)
            return 1
        m = int(os.environ.get("GE_DOJI_M", "1") or "1")
        return None if m == 0 else (m if m in (1, 2, 3) else 1)
    except Exception:
        return 1


def ask_fib_method():
    """Pilih METODE FIB menu 8: 1 = 30m (video), 2 = MTF 30m+60m. Non-tty: GE_FIB_M."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Metode FIB:{X}")
            print(f"   {Y}1{X} = FIB 30m — struktur + zona fib di 30m "
                  f"(video 'Keep It Simple')")
            print(f"   {Y}2{X} = FIB MTF 30m+60m — tren & zona fib dari 60m, "
                  f"konfirmasi/timing 30m (BARU)")
            print(f"   {D}0 = kembali{X}")
            inp = input("   Metode [0-2] (default 1): ").strip()
            if inp == "0":
                return None
            if inp in ("1", "2"):
                return int(inp)
            return 1
        m = int(os.environ.get("GE_FIB_M", "1") or "1")
        return None if m == 0 else (2 if m == 2 else 1)
    except Exception:
        return 1


def ask_universe():
    """Pilih pasar 1-3 untuk SCALPER (mode 6). Non-tty: env GE_UNIVERSE."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Pasar:{X}")
            print(f"      {Y}1{X} = ALL COIN          {Y}2{X} = TOP {TOP_N_CAP}          "
                  f"{Y}3{X} = EMAS SAJA")
            print(f"      {D}0 = kembali{X}")
            u = input(f"   Pasar [0/1/2/3] (default {DEFAULT_MODE}): ").strip()
            if u == "0":
                return None
            return int(u) if u in ("1", "2", "3") else DEFAULT_MODE
        u = int(os.environ.get("GE_UNIVERSE", str(DEFAULT_MODE)))
        return u if u in (1, 2, 3) else DEFAULT_MODE
    except Exception:
        return DEFAULT_MODE


def testnet_selfcheck():
    """Mode 5: pastikan kunci TESTNET/DEMO TERISI & login ke server itu SUKSES.
    Kunci yang salah lingkungan (mis. kunci Demo dipakai di endpoint Testnet, atau
    sebaliknya) menghasilkan 'not support' / invalid key — bot menolak start
    supaya tidak tertukar akun asli. Return True=aman."""
    kind = ENV_KIND
    if SUBMODE == "TESTNET":
        kind = "testnet"
    elif SUBMODE == "DEMO":
        kind = "demo"
    if kind not in ("testnet", "demo"):
        return True
    env_name = "TESTNET" if kind == "testnet" else "DEMO"
    env_site = "https://testnet.bybit.com" if kind == "testnet" else \
               "Demo Trading (demo.bybit.com / akun utama dalam mode Demo)"
    k = (_fresh_testnet_key()[0] if kind == "testnet" else _fresh_demo_key()[0])
    if k in ("", "GANTI"):
        print(f"{R}┌─ AKUN {env_name} — TIDAK JALAN ───────────────────────────────┐{X}")
        print(f"{R}│  Kunci {env_name} BELUM diisi. ({env_site}){X}")
        print(f"{R}│  Isi sekali:  python3 set_testnet_key.py   (pilih {env_name}){X}")
        print(f"{R}└──────────────────────────────────────────────────────────────────┘{X}")
        return False
    try:
        at, rows = _wallet_rows()
        if not rows or True:   # selalu cek retMsg bila ada
            pass
        if not rows:
            print(f"{R}┌─ AKUN {env_name} — LOGIN GAGAL ─────────────────────────────┐{X}")
            print(f"{R}│  Tidak ada baris saldo (auth ditolak / 'not support').{X}")
            if kind == "testnet":
                print(f"{R}│  - Kunci testnet HARUS dari testnet.bybit.com (bukan Demo).{X}")
            else:
                print(f"{R}│  - Kunci Demo HARUS dibuat di akun utama saat mode Demo Trading,{X}")
                print(f"{R}│    lalu pilih lingkungan DEMO (bukan TESTNET).{X}")
            print(f"{R}│  Perbaiki: python3 set_testnet_key.py --clear lalu isi ulang.{X}")
            print(f"{R}└──────────────────────────────────────────────────────────────────┘{X}")
            return False
        eq = 0.0
        for row in rows:
            try:
                v = row.get("totalEquity")
                if v not in ("", None):
                    eq = float(v); break
            except Exception:
                continue
        if eq > 0:
            print(f"{G}✔ {env_name} TERHUBUNG — saldo ${eq:,.2f} "
                  f"(jenis akun {at}; akun uji coba, TIDAK menyentuh akun asli){X}")
        else:
            print(f"{Y}✔ {env_name} TERHUBUNG — saldo $0.00{X}")
            print("   ⚠ Dana testnet TIDAK otomatis ada — klaim dulu (sekali / 24 jam):")
            print("     • testnet.bybit.com → login → halaman Aset/Asset → 'Request "
                  "Testnet Funds' (USDT)")
            print("     • atau Bybit Demo Trading (demo.bybit.com) → UTA demo otomatis "
                  "50.000 USDT saat daftar")
            print("     • Setelah saldo masuk, restart bot — saldo akan terbaca.")
            print("   Bot tetap jalan, tapi entry ditolak selama margin 0.")
        return True
    except Exception as e:
        print(f"{R}┌─ AKUN {env_name} — LOGIN GAGAL ────────────────────────────────┐{X}")
        print(f"{R}│  {e}{X}")
        print(f"{R}│  Key akun asli TIDAK valid di testnet. Buat kunci baru di{X}")
        print(f"{R}│  https://testnet.bybit.com lalu: python3 set_testnet_key.py{X}")
        print(f"{R}└──────────────────────────────────────────────────────────────────┘{X}")
        return False


def ask_r1():
    """Pilih MODE R1 (menu 1-6): 1 = KETAT (1H & 4H searah, video asli),
    2 = LONGGA (cukup 1H searah). 0 = kembali. Non-tty: env GE_R1 (default 1)."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Mode R1 (konfluensi 1H/4H):{X}")
            print(f"   {Y}1{X} = KETAT  \u2014 1H & 4H HARUS searah (aturan video asli)")
            print(f"   {Y}2{X} = LONGGA \u2014 cukup 1H searah (4H diabaikan \u2014 tambahan)")
            print(f"   {D}0 = kembali{X}")
            inp = input("   R1 [1/2] (default 1): ").strip()
            if inp == "0":
                return None
            return "LONGGA" if inp == "2" else "KETAT"
        return "KETAT" if os.environ.get("GE_R1", "1") == "1" else "LONGGA"
    except Exception:
        return "KETAT"


def ask_zmin():
    """v1.34: ambang ZONA MINIMUM (varian A/B/D, menu 1-4): 1=6.5 (video asli STRONG),
    2=5.5, 3=4.0 (default v1.34). Non-tty: env GE_ZMIN=1|2|3 (default 3)."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Zona minimum R2 (varian A/B/D):{X}")
            print(f"   {Y}1{X} = STRONG 6.5 \u2014 aturan video asli (sangat selektif)")
            print(f"   {Y}2{X} = 5.5     \u2014 sedang")
            print(f"   {Y}3{X} = 4.0     \u2014 standar v1.34 (zona kuat terjangkau)")
            print(f"   {D}0 = kembali{X}")
            inp = input("   Zona [1/2/3] (default 3): ").strip()
            if inp == "0":
                return None
            return {1: 6.5, 2: 5.5}.get(int(inp), 4.0) if inp in ("1", "2", "3") else 4.0
        ge = os.environ.get("GE_ZMIN", "3")
        return {1: 6.5, 2: 5.5}.get(int(ge), 4.0)
    except Exception:
        return 4.0


def ask_variant(default="A"):
    """Tanya varian strategi (A-H). Non-tty: env GE_VARIANT. Return salah satu VARIANTS."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Varian strategi:{X}")
            print(f"      {Y}A{X} = DASAR    — 3 aturan murni (perilaku video)")
            print(f"      {Y}B{X} = REGIME   — filter tren EMA50/200 (skip ROTATION)")
            print(f"      {Y}C{X} = ELITE    — zona >= {ELITE_THR:.1f}/10 (bukan {ZONE_MIN_SCORE})")
            print(f"      {Y}D{X} = RETEST   — zona sudah diuji >= {RETEST_MIN_TESTS}x")
            print(f"      {Y}E{X} = AGRESIF  — sig {E_SIG_MIN}/4 · zona >= {E_ZONE_MIN} · "
                  f"RR >= {E_MIN_RR} (paling sering)")
            print(f"      {Y}F{X} = GABUNGAN — A+B+C+D serentak (paling selektif, "
                  f"kualitas tertinggi)")
            print(f"      {Y}G{X} = GZ-STOPPOOL — SHORT saat harga DI ATAS Golden Zone "
                  f"& SUDAH sentuh STOP POOL di atas; LONG saat DI BAWAH GZ & "
                  f"sentuh STOP POOL di bawah (SL sisi luar zona)")
            print(f"      {D}0 = kembali{X}")
            v = input(f"   Varian [0/A/B/C/D/E/F/G] (default {default}): ").strip().upper()
            if v == "0":
                return None
            return v if v in VARIANTS else default
        v = os.environ.get("GE_VARIANT", default).upper()
        return v if v in VARIANTS else default
    except Exception:
        return default


def confirm_real(what):
    """PENGAMAN: mode 7/8 pilih '2 = AKUN REAL' -> WAJIB ketik YES (huruf besar).
    Non-tty: env GE_YES=YES. Return True bila disetujui."""
    try:
        if sys.stdin.isatty():
            print(f"{R}\u26a0 Anda memilih AKUN REAL ({what}) — transaksi UANG ASLI.{X}")
            y = input(f"   Ketik {Y}YES{X} untuk konfirmasi, atau {Y}ENTER{X} untuk batal: ").strip()
            return y.upper() == "YES"
        return os.environ.get("GE_YES", "").strip().upper() == "YES"
    except Exception:
        return False


def confirm_env_choice(kind, what):
    """KONFIRMASI AKUN (mode 7/8) — tampilan BESAR sebelum bot jalan, supaya
    tidak mungkin lagi salah demo/real:
    DEMO : tekan Enter / y = LANJUT (pakai kunci DEMO, api-demo.bybit.com).
    REAL : WAJIB ketik YES — selain itu BATAL.
    Bila REAL tapi ge_keys.json punya kunci DEMO -> peringatan + tawaran batal."""
    kf = load_keys_file()
    dk = bool((kf.get("demo") or {}).get("api_key"))
    try:
        tty = sys.stdin.isatty()
    except Exception:
        tty = False
    if kind == "demo":
        keyline = ("kunci DEMO (prod-demo) \u2014 TERISI" if dk else
                   "\u26a0 kunci DEMO belum diisi \u2014 jalankan: "
                   "python3 set_testnet_key.py --env demo")
        print(f"{C}\u2554{'\u2550' * 58}\u2557{X}")
        print(f"{C}\u2551{X}  AKUN TERPILIH: {G}DEMO{X} \u00b7 {what}")
        print(f"{C}\u2551{X}  endpoint      : api-demo.bybit.com")
        print(f"{C}\u2551{X}  kunci dipakai : {Y}{keyline}{X}")
        print(f"{C}\u255a{'\u2550' * 58}\u255d{X}")
        if tty:
            y = input("   LANJUT [Enter=ya / 0=batal]: ").strip().lower()
            if y == "0":
                add_log("konfirmasi akun: DEMO dibatalkan (input '0')")
                return False
            add_log(f"konfirmasi akun: DEMO diterima (input {y!r})")
            print(f"{G}\u2192 MELANJUTKAN SEBAGAI DEMO @ api-demo.bybit.com \u2014 "
                  f"baris AKUN di dashboard HARUS 'DEMO'.{X}")
            return True
        add_log("konfirmasi akun: DEMO diterima (non-tty)")
        return True
    # ---- REAL ----
    print(f"{R}\u2554{'\u2550' * 58}\u2557{X}")
    print(f"{R}\u2551{X}{R}  AKUN TERPILIH: REAL \u00b7 {what} \u2014 UANG ASLI!{X}")
    print(f"{R}\u2551{X}  endpoint      : api.bybit.com \u00b7 kunci UTAMA")
    if dk:
        print(f"{R}\u2551{X}  \u26a0 ge_keys.json punya kunci DEMO \u2014 kalau")
        print(f"{R}\u2551{X}    maksudnya DEMO: tekan 0 sekarang, lalu pilih 1.{X}")
    print(f"{R}\u255a{'\u2550' * 58}\u255d{X}")
    if tty:
        y = input("   Ketik YES untuk melanjutkan (selain itu = BATAL): ").strip()
        if y.upper() == "YES":
            add_log("konfirmasi akun: REAL dikonfirmasi (YES)")
            print(f"{R}\u2192 MELANJUTKAN SEBAGAI REAL @ api.bybit.com \u2014 "
                  f"UANG ASLI!{X}")
            return True
        add_log(f"konfirmasi akun: REAL DITOLAK (input {y!r})")
        return False
    add_log("konfirmasi akun: REAL ditolak (non-tty tanpa GE_YES)")
    return os.environ.get("GE_YES", "").strip().upper() == "YES"


def ask_doji_env():
    """MODE 7 (DOJI): 1=DEMO · 2=AKUN REAL · 0=kembali.
    Non-tty: env GE_ENV = demo|real (default demo)."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Akun (mode 7 DOJI):{X}")
            print(f"      {Y}1{X} = DEMO — Bybit Demo Trading (uang virtual, kunci 'prod-demo')")
            print(f"      {Y}2{X} = AKUN REAL — uang asli (kunci utama bybit.com)")
            print(f"      {D}0 = kembali{X}")
            while True:
                e = input("   Pilihan [1=DEMO / 2=AKUN REAL] (default 1): ").strip().lower()
                if e == "0":
                    return None
                if e in ("", "1", "d", "demo"):
                    add_log(f"pilihan akun (mode {MODE}): {e!r} -> DEMO")
                    return "demo"
                if e in ("2", "r", "real"):
                    add_log(f"pilihan akun (mode {MODE}): {e!r} -> REAL (butuh ketik YES)")
                    return "real"
                print(f"{R}   '{e}' tidak dikenal — ketik 1 = DEMO atau 2 = AKUN REAL.{X}")
        e = os.environ.get("GE_ENV", "").strip().lower()
        if e in ("", "1", "d", "demo"):
            add_log(f"pilihan akun (mode {MODE}): non-tty -> DEMO")
            return "demo"
        add_log(f"pilihan akun (mode {MODE}): non-tty GE_ENV={e!r} -> REAL")
        return "real"
    except Exception:
        return "demo"


def ask_fib_env():
    """MODE 8 (FIB): 1=DEMO · 2=AKUN REAL · 0=kembali.
    Non-tty: env GE_ENV = demo|real (default demo)."""
    try:
        if sys.stdin.isatty():
            print(f"   {B}Akun (mode 8 FIB):{X}")
            print(f"      {Y}1{X} = DEMO — Demo Trading (uang virtual, kunci 'prod-demo')")
            print(f"      {Y}2{X} = AKUN REAL — uang asli (kunci utama bybit.com)")
            print(f"      {D}0 = kembali{X}")
            while True:
                e = input("   Pilihan [1=DEMO / 2=AKUN REAL] (default 1): ").strip().lower()
                if e == "0":
                    return None
                if e in ("", "1", "d", "demo"):
                    add_log(f"pilihan akun (mode {MODE}): {e!r} -> DEMO")
                    return "demo"
                if e in ("2", "r", "real"):
                    add_log(f"pilihan akun (mode {MODE}): {e!r} -> REAL (butuh ketik YES)")
                    return "real"
                print(f"{R}   '{e}' tidak dikenal — ketik 1 = DEMO atau 2 = AKUN REAL.{X}")
        e = os.environ.get("GE_ENV", "").strip().lower()
        if e in ("", "1", "d", "demo"):
            add_log(f"pilihan akun (mode {MODE}): non-tty -> DEMO")
            return "demo"
        add_log(f"pilihan akun (mode {MODE}): non-tty GE_ENV={e!r} -> REAL")
        return "real"
    except Exception:
        return "demo"


def ask_account(what, default="demo", confirm=False):
    """PILIHAN AKUN untuk SEMUA mode (1-8): 1=DEMO (api-demo), 2=AKUN REAL (wajib
    YES bila confirm=True), 0=kembali. Non-tty: GE_ENV=demo|real (default default)."""
    try:
        kf = load_keys_file()
        _dm_k = ((kf.get("demo") or {}).get("api_key") or "").strip()
        dm_ok = _dm_k not in ("", "GANTI")
        if sys.stdin.isatty():
            print(f"   {B}Akun sesi ({what}):{X}")
            print(f"      {Y}1{X} = DEMO   · api-demo.bybit.com · kunci: "
                  f"{G if dm_ok else R}{'TERISI' if dm_ok else 'BELUM ISI'}{X}")
            print(f"      {Y}2{X} = AKUN REAL · api.bybit.com · UANG ASLI"
                  f"{' (wajib ketik YES)' if confirm else ''}")
            print(f"      {D}0 = kembali{X}")
            while True:
                a = input(f"   Pilihan [1=DEMO / 2=AKUN REAL] "
                          f"(default {'1' if default == 'demo' else '2'}): ").strip().lower()
                if a == "0":
                    return None
                if a == "":
                    acct = default
                elif a in ("1", "d", "demo"):
                    acct = "demo"
                elif a in ("2", "r", "real"):
                    acct = "real"
                else:
                    print(f"{R}   '{a}' tidak dikenal — 1 = DEMO atau 2 = AKUN REAL.{X}")
                    continue
                if acct == "real" and confirm and not confirm_real(what):
                    say("\u2192 dibatalkan (REAL tidak dikonfirmasi).")
                    return None
                add_log(f"pilihan akun ({what}): {a!r} -> {acct.upper()}")
                return acct
        e = os.environ.get("GE_ENV", default).strip().lower()
        acct = "real" if e in ("2", "r", "real") else "demo"
        add_log(f"pilihan akun ({what}): non-tty GE_ENV={e!r} -> {acct.upper()}")
        return acct
    except Exception:
        return default


EP_MAP = {"testnet": "https://api-testnet.bybit.com",
          "demo": "https://api-demo.bybit.com",
          "real": "https://api.bybit.com"}


def _pybit_id():
    """(lokasi file pybit, versi) — untuk mendeteksi pybit lokal yang menutupi
    paket asli (mis. folder pybit/ di direktori proyek, bukan site-packages)."""
    try:
        import pybit as _p
        import importlib.metadata as _md
        return getattr(_p, "__file__", "?"), _md.version("pybit")
    except Exception as e:
        return f"IMPORT ERROR: {e}", "?"


def _make_http(key, sec, kind_):
    """Sesi HTTP Bybit — TIDAK bergantung pada perilaku pybit:
    1) coba pybit (bila ada): konstruksi + paksa h.endpoint = target;
    2) baca balik: bila masih tidak cocok / gagal -> pakai GEHTTP (klien REST
       langsung, endpoint DIKUNCI konstanta — DEMO pasti api-demo)."""
    ep = EP_MAP.get(kind_, EP_MAP["real"])
    tn, dm = kind_ == "testnet", kind_ == "demo"
    h, last = None, None
    for kw in ({"api_key": key, "api_secret": sec, "testnet": tn, "demo": dm},
               {"api_key": key, "api_secret": sec, "endpoint": ep},
               {"api_key": key, "api_secret": sec}):
        try:
            h = HTTP(**kw)
            break
        except TypeError as e:
            last = e
    if h is not None:
        try:
            h.endpoint = ep                 # PAKSA endpoint
            got = getattr(h, "endpoint", "") or ""
            if got == ep:
                _SESS.update({"endpoint": got})
                return h
            say(f"{Y}\u26a0 pybit di perangkat ini tetap ke {got} (bukan {ep}) \u2014 "
                f"ganti ke klien REST langsung (tanpa pybit).{X}")
        except Exception as e:
            last = e
    try:
        h = GEHTTP(api_key=key, api_secret=sec, testnet=tn, demo=dm)
    except Exception as e:
        raise TypeError(f"sesi Bybit gagal dibuat: {e} (terakhir: {last})")
    _SESS.update({"endpoint": ep})
    return h


def make_session():
    """Sesi HTTP Bybit sesuai ENV_KIND (target akun):
    testnet -> api-testnet.bybit.com (testnet=True,  demo=False).
    demo    -> api-demo.bybit.com    (testnet=False, demo=True).
    real    -> api.bybit.com         (testnet=USE_TESTNET, demo=False).
    SUBMODE 'TESTNET'/'DEMO' (mode 5) tetap memaksa env masing-masing (backward-compat).
    Kunci salah lingkungan -> login ditolak server (selfcheck menangkapnya)."""
    kind = ENV_KIND
    if SUBMODE == "TESTNET":
        kind = "testnet"
    elif SUBMODE == "DEMO":
        kind = "demo"
    global session, USE_TESTNET, _SESS

    def _mk(kind_, key, secret, tn, dm, ksrc):
        # DEMO/TESTNET & mode 7/8 -> GEHTTP LANGSUNG (klien REST kita sendiri,
        # endpoint DIKUNCI): tanpa pybit = tanpa kemungkinan salah endpoint.
        if SUBMODE in ("DOJI7", "FIB8", "FIB8M", "TESTNET", "DEMO") or kind_ != "real":
            sess = GEHTTP(api_key=key, api_secret=secret, testnet=tn, demo=dm)
            _SESS.update({"kind": kind_,
                          "endpoint": getattr(sess, "endpoint", "") or EP_MAP[kind_],
                          "key_src": ksrc + " (GEHTTP, tanpa pybit)"})
            return sess
        sess = _make_http(key, secret, kind_)
        _SESS.update({"kind": kind_,
                      "endpoint": getattr(sess, "endpoint", "") or EP_MAP[kind_],
                      "key_src": ksrc})
        return sess

    if kind == "testnet":
        tk, ts, kp = _fresh_testnet_key()
        if tk in ("", "GANTI"):
            tk, ts = API_KEY, API_SECRET
            ksrc = "kunci UTAMA (kunci testnet belum diisi — cari di ge_keys.json)"
        else:
            ksrc = f"kunci TESTNET ({tk[:4]}***) dari {kp}"
        sess, tn = _mk("testnet", tk, ts, True, False, ksrc), True
    elif kind == "demo":
        tk, ts, kp = _fresh_demo_key()
        if tk in ("", "GANTI"):
            tk, ts = "GANTI", "GANTI"
            ksrc = "⚠ BELUM DIISI (cari multi-lokasi) — jalankan: python3 set_testnet_key.py --env demo"
        else:
            ksrc = f"kunci DEMO ({tk[:4]}***) dari {kp}"
        sess, tn = _mk("demo", tk, ts, False, True, ksrc), True
    else:
        sess, tn = _mk("real", API_KEY, API_SECRET, USE_TESTNET, False,
                   "kunci utama"), USE_TESTNET
    # v1.33: IKAT ke session global -> get_balance/get_kline/dll memakai sesi
    # akun yang dipilih (dulu menu 5 membuat sesi lokal yang TIDAK terpakai).
    session = sess
    USE_TESTNET = bool(tn)
    return sess, USE_TESTNET


_uni_cache = {"t": 0.0, "pool": []}

# v1.33: cache WATCHDOG — hasil scan tiap simbol DIPERTAHANKAN antar siklus
# (dulu: hanya siklus ini ditampilkan → panel terlihat kosong/sedikit).
_WD = {}        # sym -> entry {px, atr, con, zones, state, ...}
_VP = {"t": 0.0, "set": set()}  # v1.33: cache posisi bursa (verifikasi masal)



def _verify_positions():
    """v1.33: kembalikan SET simbol yang BENAR-BENAR punya posisi di bursa
    (1 panggilan get_positions tanpa symbol, cache 60 dtk). Dipakai utk
    membersihkan state 'in_position' basi supaya scan tidak tersedot."""
    try:
        now = time.time()
        if _VP.get("t") and now - _VP["t"] < 60:
            return _VP["set"]
        r = session.get_positions(category="linear")
        lst = (r or {}).get("result", {}).get("list") or []
        vp = {p.get("symbol") for p in lst if float((p.get("size") or 0)) > 0}
        _VP.update({"t": now, "set": vp})
        return vp
    except Exception as e:
        log.error(f"verify_positions: {e}")
        return None


def _wd_err(sym, why):
    """Tandai kegagalan scan — tampil di WATCHDOG, tidak hilang diam-diam."""
    try:
        e = _WD.setdefault(sym, {"sym": sym})
        e["err"] = why
    except Exception:
        pass

def _uni_pull():
    """1x ambil + parse semua ticker (tanpa cache). Return [(tv, sym), ...]."""
    global _UNI_ERR
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
    if not pool:
        _UNI_ERR = "response kosong"
    return pool


def detect_perp_universe():
    """Semua pair USDT perp linear Bybit, urut turnover 24h (besar->kecil).
    Di-cache 60 detik; KEGAGALAN juga di-cache 30 dtk (jangan pukul Bybit
    berulang saat jaringan/rate-limit salah) + 1x ulang sebelum menyerah."""
    if _uni_cache["pool"] and time.time() - _uni_cache["t"] < 60:
        return _uni_cache["pool"]
    if not _uni_cache["pool"] and _uni_cache.get("fail_t") \
            and time.time() - _uni_cache["fail_t"] < 30:
        return []
    try:
        pool = _uni_pull()
        _uni_cache.update({"t": time.time(), "pool": pool, "fail_t": 0.0})
        return pool
    except Exception as e:
        _UNI_ERR = "%s: %s" % (type(e).__name__, e)
        log.error(f"detect_perp_universe (coba 1): {e}")
        try:
            time.sleep(1.5)
            pool = _uni_pull()
            _uni_cache.update({"t": time.time(), "pool": pool, "fail_t": 0.0})
            return pool
        except Exception as e2:
            _UNI_ERR = "%s: %s" % (type(e2).__name__, e2)
            _uni_cache["fail_t"] = time.time()
            log.error(f"detect_perp_universe (coba 2): {e2}")
            return []


def react_push(s, zdir, px, atr, i):
    """Pine: zona yg baru FILLED/SWEPT -> array pends (dir, close, atr, bar)."""
    p = s.setdefault("pends", [])
    if len(p) >= 8:
        p.pop(0)
    p.append({"dir": int(zdir), "px": float(px), "atr": float(atr or 0.0),
              "bar": int(i)})


def react_track(s, px, i):
    """Pine (blok pends): harga harus KEMBALI >= reactMult x ATR (arah sesuai)
    dalam REACT_BARS agar dihitung reactHit; lewat jendela -> reactTot saja.
    Statistik kualitas zona — ditampilkan di panel ENGINE (bukan filter entry)."""
    p = s.get("pends") or []
    if not p:
        return
    st = s.setdefault("_react", [0, 0])
    keep = []
    for q in p:
        if q["atr"] > 0 and q["dir"] > 0 and px <= q["px"] - q["atr"] * REACT_ATR:
            st[0] += 1                       # supply tertembus -> turun balik = reaksi
        elif q["atr"] > 0 and q["dir"] < 0 and px >= q["px"] + q["atr"] * REACT_ATR:
            st[0] += 1                       # demand tertembus -> naik balik = reaksi
        elif i - q["bar"] >= REACT_BARS:
            st[1] += 1                       # jendela habis tanpa reaksi
        else:
            keep.append(q)
    s["pends"] = keep
    s["_react"] = [min(st[0], 9999), min(st[1], 9999)]


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
    if MODE in (7, 8):                       # DOJI/FIB: khusus XAUUSDT
        SYMBOLS = ["XAUUSDT"]
        return
    if MODE == 3:
        SYMBOLS = list(FOCUS_SYMBOLS)
        log.info(f"mode EMAS SAJA: {len(SYMBOLS)} simbol")
        return
    global _SRC_UNI
    pool = detect_perp_universe()
    if not pool:
        log.warning("universe KOSONG (get_tickers gagal/hampa) \u2014 coba ulang")
        for _ in range(2):
            time.sleep(2.0)
            pool = detect_perp_universe()
            if pool:
                break
    if not pool and MODE in (1, 2) and len(SYMBOLS) <= 1:
        # v1.33: get_tickers gagal -> universe CADANGAN likuid (tidak turun ke 1)
        pool = [(1e12, x) for x in FALLBACK_UNIVERSE]
        _SRC_UNI = "FALLBACK"
        log.warning("get_tickers gagal (%s) \u2014 pakai FALLBACK %d simbol "
                    "likuid (LIVE otomatis kembali)"
                    % (_UNI_ERR or "?", len(pool)))
        add_log(f"\u26a0 universe LIVE gagal ({_UNI_ERR or '?'}) \u2014 "
                f"FALLBACK {len(pool)} simbol likuid \u2014 LIVE kembali otomatis")
    elif pool:
        _SRC_UNI = "LIVE"
    if not pool:
        if len(SYMBOLS) > 1:
            # jangan turun ke 1 simbol: pertahankan universe terakhir yang valid
            log.warning("universe KOSONG \u2014 PERTAHANKAN %d simbol terakhir "
                        "(tidak turun ke XAUUSDT saja)" % len(SYMBOLS))
            _SRC_UNI = "CACHE"
            return
        log.warning("universe KOSONG (get_tickers gagal/hampa) \u2014 pakai FOCUS saja "
                    "\u2014 cek koneksi/akun (demo? kunci?)")
    if MODE == 1:
        add = [s for tv, s in pool if tv >= ALL_MIN_TURNOVER]
        if not add and pool:
            log.warning(f"mode ALL: 0 coin >= ${ALL_MIN_TURNOVER / 1e6:g}jt turnover "
                        f"(pool {len(pool)}) \u2014 fallback TOP {TOP_N_CAP}")
            add = [s for _, s in pool[:TOP_N_CAP]]
    else:
        add = [s for _, s in pool[:TOP_N_CAP]]
    SYMBOLS = list(dict.fromkeys(FOCUS_SYMBOLS + add))
    log.info(f"mode {MODE_LABEL.get(MODE, MODE)}: {len(SYMBOLS)} simbol "
             f"({len(add)} coin terdeteksi, emas selalu diikutkan)")

# ══════════════════ STANDALONE: MENU 7 (DOJI) & 8 (FIB) ══════════════════
# Menu 7 & 8 berdiri SENDIRI, BEDA dari PRO: XAUUSDT saja, tanpa zona
# likuiditas / konfluensi MTF / WATCHDOG / readiness / engine stats.
#   DOJI = M3 (video ThisIsDaryl, doji breakout)
#   FIB  = M30 + fallback struktur 60m (video 'Keep It Simple')

SA_TF    = {"DOJI7": DOJI_TF, "DOJI30": DOJI30_TF, "DOJIM": DOJI30_TF,
            "FIB8": FIB_TF, "FIB8M": FIB_TF}
SA_FB    = {"DOJI7": DOJI_HTF1, "DOJI30": DOJI30_HTF1, "DOJIM": DOJI30_HTF1,
            "FIB8": FIB_HTF1, "FIB8M": FIB_HTF1}
SA_SLEEP = {"DOJI7": 2.0, "DOJI30": 3.0, "DOJIM": 3.0,
            "FIB8": 3.0, "FIB8M": 3.0}
SA_LABEL = {"DOJI7": "DOJI BREAKOUT 3m (M3)", "DOJI30": "DOJI BREAKOUT 30m (M30)",
            "DOJIM": "DOJI BREAKOUT MTF 30m+60m",
            "FIB8": "FIB TREND SCALP 30m (M30)", "FIB8M": "FIB TREND MTF 30m+60m"}


def sa_atr(df, n=14):
    """ATR(14) sederhana dari bar CLOSED di df (tanpa library tambahan)."""
    try:
        h = pd.to_numeric(df["high"]).values
        l = pd.to_numeric(df["low"]).values
        c = pd.to_numeric(df["close"]).values
    except Exception:
        return 0.0
    trs = []
    for k in range(1, len(c)):
        trs.append(max(h[k] - l[k], abs(h[k] - c[k - 1]), abs(l[k] - c[k - 1])))
    if len(trs) < n:
        return 0.0
    return float(sum(trs[-n:]) / n)


def sa_settle(sym, s):
    """Posisi hilang (SL/TP bursa / manual) -> catat statistik standalone."""
    pnl = s.get("last_pnl") or 0.0
    st = STATS.setdefault(sym, {"n": 0, "w": 0, "pnl": 0.0})
    st["n"] += 1
    st["w"] += 1 if pnl > 0 else 0
    st["pnl"] += pnl
    today = wib_now().strftime("%Y-%m-%d")
    if DAY.get("date") != today:
        DAY.update({"date": today, "n": 0, "w": 0, "pnl": 0.0})
    DAY["n"] += 1
    DAY["w"] += 1 if pnl > 0 else 0
    DAY["pnl"] += pnl
    save_json(STATS_FILE, STATS)
    save_json(DAY_FILE, DAY)
    say(f"\u25c6 {sym} posisi ditutup \u2014 PnL {pnl:+.2f}$ \u00b7 Rp {fmt_rp(pnl * usd_idr())}")
    s.update({"in_position": False, "side": None, "entry": 0.0, "sl": 0.0,
              "tp": 0.0, "tp1": 0.0, "tp2": 0.0, "qty0": 0.0,
              "tp1_done": False, "tp2_done": False, "be_done": False,
              "trail_on": False, "riding": False, "last_pnl": None,
              "last_exit": time.time(),
              "realized": s.get("realized", 0.0) + pnl})


def sa_manage(sym, s, px, atrv):
    """Kelola posisi standalone: pantau TP1 (SL->BE, sisa ke TP2) & TP2."""
    p = get_position(sym)
    if not p:
        if s["in_position"]:
            sa_settle(sym, s)
        return
    s["last_pnl"] = p.get("pnl")
    s["pos_pnl"] = p.get("pnl")
    d = 1 if s["side"] == "Buy" else -1
    tp1 = s.get("tp1") or 0.0
    tp2 = s.get("tp2") or 0.0
    if not s.get("tp1_done") and tp1 > 0 and (px - tp1) * d >= 0:
        s["tp1_done"] = True
        try:
            session.set_trading_stop(category="linear", symbol=sym,
                                     stopLoss=fmt_px(s["entry"]),
                                     takeProfit=fmt_px(tp2) if tp2 > 0 else fmt_px(tp1),
                                     slTriggerBy="LastPrice", tpTriggerBy="LastPrice",
                                     positionIdx=0)
            s["sl"] = s["entry"]           # BE
        except Exception as _e:
            log.error(f"sa be {sym}: {_e}")
        say(f"{G}[BE]{X} {sym} TP1 {tp1:.6g} tercapai \u2014 SL pindah ke entry (BE) "
            f"\u00b7 sisa jalan ke TP2 {tp2:.6g}")
    if s.get("tp1_done") and tp2 > 0 and not s.get("tp2_done") \
            and (px - tp2) * d >= 0:
        try:
            cs = "Sell" if s["side"] == "Buy" else "Buy"
            session.place_order(category="linear", symbol=sym, side=cs,
                                orderType="Market", qty=fmt_px(p["size"]),
                                reduceOnly=True, positionIdx=0)
            s["tp2_done"] = True
            say(f"\u25c6 {sym} TP2 {tp2:.6g} tercapai \u2014 sisa ditutup (RIDE selesai)")
        except Exception as _e:
            log.error(f"sa tp2 {sym}: {_e}")


def render_dash_sa(kind, bal, px, atrv, s, tick):
    """Dashboard RINGKAS khusus standalone (tanpa elemen PRO)."""
    if not UI_ON:
        return
    L = [f"{C}\u2554{'\u2550' * (WIDTH - 2)}\u2557{X}"]
    sp = SPIN[tick % len(SPIN)]
    idr = usd_idr()
    L.append(_row(f"{FW}\u25c7 {SA_LABEL[kind]} \u00b7 STANDALONE{X} {sp} {D}|{X} "
                  f"{wib_now().strftime('%d %b %H:%M:%S WIB')}"))
    L.append(_row(f"{D}XAUUSDT saja \u00b7 bebas mesin PRO (zona/MTF/WATCHDOG) \u00b7 "
                  f"kurs 1$ = Rp {fmt_rp(idr, 0)}{X}"))
    L.append(_sep())
    # ---- hero XAUUSDT ----
    hsym = "XAUUSDT"
    bpx = float(px or 0.0)
    darr, dcol = "\u2022", D
    if _hero_prev.get("sym") == hsym and _hero_prev.get("px"):
        dq = (bpx - _hero_prev["px"]) / _hero_prev["px"] * 100
        dcol = G if dq > 0 else R if dq < 0 else Y
        darr = "\u25b2" if dq > 0 else "\u25bc" if dq < 0 else "\u2022"
    _hero_prev.update({"sym": hsym, "px": bpx})
    btxt = f"{bpx:.2f}" if bpx >= 100 else f"{bpx:.6g}" if bpx > 0 else "0"
    big_p = _bignum(btxt)
    big_i = _bignum(f"{bal * idr:.0f}")
    half = (WIDTH - 4) // 2
    tfg = SA_TF.get(kind, "?")
    head_l = (f"{B}\u25c6 {hsym}{X} {dcol}{darr}{X} {D}({bpx:,.2f}){X} "
              f"{D}[TF {tfg}m \u00b7 ATR14 {atrv:.3f}]{X}")
    head_r = f"\u25c8 USDT {G}${bal:,.2f}{X} {D}=\u00b7 Rp{X}"
    head_l = _fit(head_l, WIDTH - 6 - _vlen(head_r))
    L.append(_row(head_l + " " * max(1, half - _vlen(head_l)) + head_r))
    for i in range(4):
        L.append(_row(f"{Y}{big_p[i]}{X}" + " " * max(1, half - 4) + f"{G}{big_i[i]}{X}"))
    _ep = _SESS.get("endpoint") or _SESS.get("host") or "?"
    L.append(_row(f"  {B}AKUN{X}  : {Y}{_SESS.get('kind','?').upper()}{X} \u2014 "
                  f"{_ep} {D}\u00b7 {_SESS.get('key_src','?')}{X}"))
    _kind = _SESS.get("kind")
    if _kind == "demo" and "api-demo.bybit.com" not in _ep:
        L.append(_row(f"{R}\u26a0 MISMATCH: pilihan DEMO tapi endpoint {_ep} "
                      f"\u2014 upgrade pybit: pip install -U pybit{X}"))
    if _kind == "real" and "api.bybit.com" not in _ep.replace("api-testnet", "api.bybit"):
        L.append(_row(f"{R}\u26a0 MISMATCH: pilihan REAL tapi endpoint {_ep}{X}"))
    if _kind == "real" and dk_demo_key():
        L.append(_row(f"{Y}\u2139 kunci DEMO terisi di ge_keys.json \u2014 kalau tadi "
                      f"maksudnya DEMO: Ctrl+C, mulai lagi, pilih 1 = DEMO.{X}"))
    if (bal or 0) <= 0:
        L.append(_row(f"{R}\u26a0 SALDO $0.00 — semua entry DITOLAK (margin 0).{X}"))
        if _SESS.get("kind") == "demo":
            L.append(_row(f"{R}   \u25b8 Kunci demo BELUM TERISI / salah: jalankan "
                          f"{Y}python3 set_testnet_key.py{X}{R} (pilih DEMO).{X}"))
            L.append(_row(f"{R}   \u25b8 Akun demo kosong: buka demo.bybit.com \u2192 "
                          f"Aset \u2192 dana virtual (biasanya otomatis 50.000 USDT "
                          f"saat daftar demo).{X}"))
        else:
            L.append(_row(f"{R}   \u25b8 Akun REAL kosong / dana bukan USDT \u2014 "
                          f"deposit USDT, atau pilih {Y}1 = DEMO{X}{R} saat mulai.{X}"))
        if _wb_err:
            L.append(_row(f"{D}   diagnosa API: {_wb_err}{X}"))
    L.append(_sep())
    # ---- status: posisi / menunggu ----
    if s.get("in_position"):
        cc = G if s["side"] == "Buy" else R
        d = "LONG" if s["side"] == "Buy" else "SHORT"
        entry = s.get("entry") or 0.0
        sl = s.get("sl") or 0.0
        tp1 = s.get("tp1") or 0.0
        tp2 = s.get("tp2") or 0.0
        pnl = s.get("pos_pnl")
        pc = G if (pnl or 0) >= 0 else R
        roi = (pnl or 0) / (s.get("margin_used") or 1.0) * 100.0
        L.append(_row(f"{cc}\u25cf{X} {cc}{d:<6}{X}{B}{hsym}{X} @ {entry:.6g} "
                      f"{D}\u2192 SL {sl:.6g} \u00b7 TP1 {tp1:.6g} \u00b7 TP2 {tp2:.6g}{X}"))
        L.append(_row(f"    PnL {pc}{pnl:+.2f}$" if pnl is not None else "    PnL \u2026",
                      ))
        L.append(_row(f"    Rp {fmt_rp((pnl or 0) * idr)} \u00b7 ROI {pc}{roi:+.0f}%{X} "
                      f"{D}|{X} MFE {s.get('mfe_r') or 0:.2f}R"))
        _den = (tp1 - entry) if d == "LONG" else (entry - tp1)
        prog = ((bpx - entry) if d == "LONG" else (entry - bpx)) / _den if _den > 0 else 0.0
        prog = max(0.0, min(1.0, prog))
        L.append(_row(f"     {_bar(prog * 100.0, 16, pc, anim=tick)} "
                      f"{pc}{prog * 100.0:3.0f}% menuju TP1{X}"))
        if s.get("tp1_done"):
            L.append(_row(f"     {G}\u25c6 RIDE{X} TP1 \u2713 \u00b7 BE aktif \u00b7 "
                          f"sisa \u2192 TP2 {tp2:.6g}"))
    else:
        if kind in ("DOJI7", "DOJI30", "DOJIM"):
            _dtf = "3m" if kind == "DOJI7" else ("30m + bias 60m" if kind == "DOJIM" else "30m")
            L.append(_row(f"{Y}\u25c9 STATUS{X} {Y}MENUNGGU DOJI{X} \u2014 doji {_dtf} "
                          f"valid belum terbentuk (gambar akan tampil di Pine)"))
            L.append(_row(f"{D}   syarat: body \u226410% range \u00b7 kaki \u226530% "
                          f"tiap sisi \u00b7 range \u22651\u00d7ATR \u00b7 sweep "
                          f"low/high candle sblmnya{X}"))
            L.append(_row(f"{D}   entry TOUCH (tanpa tunggu close) \u00b7 SL sisi "
                          f"lawan doji \u00b7 TP1 1.5R \u00b7 TP2 2.25R \u00b7 "
                          f"cooldown 4m{X}"))
        else:
            L.append(_row(f"{Y}\u25c9 STATUS{X} {Y}MENUNGGU ZONA FIB{X} \u2014 "
                          f"tren {'60m' if kind == 'FIB8M' else '30m'} + mantul "
                          f"50\u201361.8% belum terjadi"))
            L.append(_row(f"{D}   struktur HH/HL (LONG) atau LL/LH (SHORT) \u00b7 "
                          f"swing \u2264{FIB_SWING_AGE} bar \u00b7 SL luar swing \u00b7 "
                          f"TP1 1R \u00b7 TP2 1.5R \u00b7 "
                          f"{'konfirmasi 30m (MTF)' if kind == 'FIB8M' else 'fallback 60m'}{X}"))
    _gd = s.get("last_diag") or []
    if _gd and not s.get("in_position"):
        L.append(_row(f"{D}  \u25b8 GATE: {_gd[-1]}{X}"))
    bloc, why = entry_blocked()
    if bloc:
        L.append(_row(f"{R}\u26a0 GUARD AKTIF \u2014 {why} | ENTRY DIJEDA{X}"))
    L.append(_sep("\u2261 LIVE LOG"))
    if _logbuf:
        for ln in _logbuf[-6:]:
            L.append(_row(ln))
    L.append(_row(f"{D}Ctrl+C utk berhenti \u00b7 log: {LOG_FILE}{X}"))
    L.append(f"{C}\u255a{'\u2550' * (WIDTH - 2)}\u255d{X}")
    frame = "\n".join(ln + "\033[K" for ln in L)
    if sys.stdout.isatty():
        sys.stdout.write("\033[?25l\033[H" + frame + "\033[J")
    else:
        sys.stdout.write("\n" + "\n".join(_strip(ln) for ln in L) + "\n")
    sys.stdout.flush()


def dk_demo_key():
    """True bila ge_keys.json punya kunci demo terisi."""
    return bool(((load_keys_file().get("demo") or {}).get("api_key")))


def sa_probe(sym="XAUUSDT"):
    """Verifikasi LIVE: endpoint yang BENAR-BENAR dipakai pybit + kunci yang
    terbaca + saldo + (bila gagal) kode error Bybit. Dipanggil saat standalone
    mulai — hasilnya tampil di baris pertama supaya akun salah kelihatan."""
    global _SESS
    ep = _SESS.get("endpoint") or _SESS.get("host") or "?"
    kf = load_keys_file()
    kstat = " \u00b7 ".join(
        f"{k}:{'TERISI' if (kf.get(k) or {}).get('api_key') else 'kosong'}"
        for k in ("testnet", "demo"))
    say(f"\u25b8 AKUN AKTIF: {_SESS.get('kind', '?').upper()} \u00b7 endpoint "
        f"{ep} \u00b7 {_SESS.get('key_src', '?')}")
    say(f"\u25b8 ge_keys.json \u2192 {kstat}")
    try:
        _, rows = _wallet_rows()
        b = get_balance()
    except Exception as e:
        say(f"{R}\u2716 PROBE AKUN GAGAL — {type(e).__name__}: {e}{X}")
        return 0.0
    if not rows:
        say(f"{R}\u2716 PROBE AKUN GAGAL — {_wb_err}{X}")
        say(f"{R}   \u25b8 SOLUSI: 1) python3 set_testnet_key.py --env demo "
            f"(kunci dibuat DI AKUN DEMO)  2) saldo demo di demo.bybit.com{X}")
        if _SESS.get("kind") == "real" and dk_demo_key():
            say(f"{Y}   \u25b8 TIP: ge_keys.json punya kunci DEMO, tapi run ini REAL. "
                f"Kalau tadi maksudnya DEMO: Ctrl+C, mulai lagi, pilih 1 = DEMO.{X}")
        return 0.0
    say(f"{G}\u2714 PROBE AKUN OK \u2014 saldo ${b:,.2f} (jenis akun {rows[0].get('accountType', '?')}){X}")
    return b


def _keys_candidates():
    """Lokasi ge_keys.json yang mungkin (multi-lokasi — tak bergantung CWD)."""
    cand = []
    _f = globals().get("__file__") or ""
    if _f:
        _d = os.path.dirname(os.path.abspath(_f))
        cand += [os.path.join(_d, "ge_keys.json"),
                 os.path.join(_d, "..", "ge_keys.json")]
    cand += [os.path.join(os.getcwd(), "ge_keys.json"),
             os.path.expanduser("~/ge_keys.json"),
             os.path.expanduser("~/project/ge_keys.json"),
             os.path.expanduser("~/projects/ge_keys.json")]
    seen, out = set(), []
    for p in cand:
        ap = os.path.abspath(p)
        if ap not in seen:
            seen.add(ap); out.append(ap)
    return out


def _fresh_demo_key():
    """Baca kunci DEMO SEGAR: ge_keys.json (multi-lokasi) > env GE_DEMO_KEY.
    TIDAK pernah fallback ke kunci utama. Return (key, secret, sumber)."""
    for p in _keys_candidates():
        try:
            if os.path.exists(p):
                d = json.load(open(p, encoding="utf-8"))
                k = ((d.get("demo") or {}).get("api_key") or "").strip()
                sec = ((d.get("demo") or {}).get("api_secret") or "").strip()
                if k and k != "GANTI":
                    return k, sec, os.path.abspath(p)
        except Exception:
            continue
    ek = os.environ.get("GE_DEMO_KEY", "").strip()
    if ek and ek != "GANTI":
        return ek, os.environ.get("GE_DEMO_SECRET", "").strip(), "ENV GE_DEMO_KEY"
    return "GANTI", "GANTI", "?"


def _fresh_testnet_key():
    """Baca kunci TESTNET segar (multi-lokasi + env) - mirror _fresh_demo_key."""
    for p in _keys_candidates():
        try:
            if os.path.exists(p):
                d = json.load(open(p, encoding="utf-8"))
                k = ((d.get("testnet") or {}).get("api_key") or "").strip()
                sec = ((d.get("testnet") or {}).get("api_secret") or "").strip()
                if k and k != "GANTI":
                    return k, sec, os.path.abspath(p)
        except Exception:
            continue
    ek = os.environ.get("GE_TESTNET_KEY", "").strip()
    if ek and ek != "GANTI":
        return ek, os.environ.get("GE_TESTNET_SECRET", "").strip(), "ENV GE_TESTNET_KEY"
    return "GANTI", "GANTI", "?"


def sa_ask_acct(kind):
    """PILIHAN AKUN PASTI — langsung dipakai membuat sesi (tidak bergantung
    pada ENV_KIND/state lain yang bisa salah di file campuran)."""
    if sys.stdin.isatty():
        print(f"   {{B}}PILIHAN AKUN SESI ({SA_LABEL[kind]}):{{X}}")
        a = input(f"   {{Y}}1{{X}}=DEMO (api-demo.bybit.com) \u00b7 "
                  f"{{Y}}2{{X}}=AKUN REAL (uang asli) [1]: ").strip().lower()
        acct = "real" if a in ("2", "r", "real") else "demo"
        if acct == "real":
            if not confirm_real(SA_LABEL[kind]):
                say("\u2192 dibatalkan (REAL tidak dikonfirmasi).")
                sys.exit(6)
        add_log(f"SESI terpilih: {acct.upper()}")
        return acct
    acct = "real" if os.environ.get("GE_ACCT", "").strip().lower() in ("2", "r", "real") else "demo"
    add_log(f"SESI terpilih: {acct.upper()} (non-tty)")
    return acct


def sa_build_session(acct):
    """Bangun sesi GEHTTP MURNI (tanpa pybit / make_session / ENV_KIND):
    DEMO -> kunci segar dari ge_keys.json + api-demo.bybit.com (terkunci).
    REAL -> kunci utama tertanam + api.bybit.com. Balas (session, USE_TESTNET)."""
    global _SESS
    if acct == "demo":
        dk, ds, kp = _fresh_demo_key()
        if dk in ("", "GANTI"):
            say(f"{R}\u2716 KUNCI DEMO tidak ditemukan (dicari: "
                f"{', '.join(_keys_candidates())}).{X}")
            say(f"{R}\u2716 Jalankan: python3 set_testnet_key.py --env demo{X}")
            sys.exit(5)
        sess = GEHTTP(api_key=dk, api_secret=ds, testnet=False, demo=True)
        _SESS.update({"kind": "demo", "endpoint": getattr(sess, "endpoint", "?"),
                      "key_src": f"kunci DEMO ({dk[:4]}***) dari {kp} \u2014 GEHTTP murni"})
        say(f"\u25c9 SESI FINAL: {G}GEHTTP \u00b7 DEMO \u00b7 {dk[:4]}*** \u00b7 "
            f"{getattr(sess, 'endpoint', '?')}{X}")
        return sess, True
    sess = GEHTTP(api_key=API_KEY, api_secret=API_SECRET, testnet=False, demo=False)
    _SESS.update({"kind": "real", "endpoint": getattr(sess, "endpoint", "?"),
                  "key_src": "kunci utama (tertanam di file) \u2014 GEHTTP murni"})
    say(f"{R}\u25c9 SESI FINAL: GEHTTP \u00b7 REAL \u00b7 {API_KEY[:4]}*** \u00b7 "
        f"{getattr(sess, 'endpoint', '?')} \u2014 UANG ASLI!{X}")
    return sess, False


def _check_cmd():
    """python3 GOLD7_V39.py --check — bukti identitas file (bukan tebakan)."""
    import hashlib as _h
    _f = globals().get("__file__") or "GOLD7.py"
    src = open(_f, encoding="utf-8").read()
    print("\u2500\u2500 AUDIT FILE GOLDEN EDGE \u2500\u2500")
    print("file   :", os.path.abspath(_f))
    print("size   :", os.path.getsize(_f), "byte")
    print("md5    :", _h.md5(src.encode()).hexdigest())
    print("versi  :", "v1.40" if "v1.40" in src[:4000] else "?? (BUKAN v1.40)")
    print("GEHTTP :", "YA" if "class GEHTTP" in src else "TIDAK")
    print("sesi   :", "YA" if "def sa_build_session" in src else "TIDAK")
    print("audit  :", "YA" if "def _check_cmd" in src else "TIDAK")
    ok = all(k in src for k in ("v1.40", "class GEHTTP", "def sa_build_session",
                                "def _fresh_demo_key", "def sa_ask_acct"))
    print("HASIL  :", f"{G}PAS \u2014 file ini v1.40 ASLI{X}" if ok
          else f"{R}TIDAK PAS \u2014 file ini BUKAN v1.40, unduh ulang{X}")
    # temukan salinan lama di folder
    try:
        _d = os.path.dirname(os.path.abspath(_f)) or "."
        for b in sorted(os.listdir(_d)):
            if b.lower().endswith(".py") and b.lower() != os.path.basename(_f).lower():
                p = os.path.join(_d, b)
                try:
                    t = open(p, encoding="utf-8", errors="ignore").read(2000)
                    if "GOLDEN EDGE" in t:
                        print(f"salinan : {b} ({{R}}LAIN \u2014 hapus: rm -f {b}{{X}})")
                except Exception:
                    pass
    except Exception:
        pass


def standalone_loop(kind, acct=None):
    """Loop STANDALONE menu 7/8: XAUUSDT saja, logika murni DOJI/FIB.
    acct: 'demo'/'real' dari menu (bila None -> tanya lagi, perilaku lama)."""
    global SYMBOLS, session, USE_TESTNET
    sym = "XAUUSDT"
    SYMBOLS = [sym]
    s = STATES.setdefault(sym, new_state())
    tf, tf_fb = SA_TF[kind], SA_FB[kind]
    # buat ULANG sesi sesuai pilihan tadi (demo/real) — pastikan tidak ada
    # sesi lama yang tertinggal; lalu PROBE: endpoint + kunci + saldo live.
    _old_pid = _ensure_single()
    if _old_pid:
        say(f"{R}\u2716 PROSES BOT LAIN MASIH JALAN (PID {_old_pid}) \u2014 "
            f"kemungkinan terminal/run LAMA yang belum mati.{X}")
        say(f"{R}\u2716 Itulah yang tampil 'REAL' tanpa lewat menu. Solusi:{X}")
        say(f"{Y}   pkill -f python3   \u00b7 lalu tutup SEMUA terminal \u00b7 "
            f"mulai lagi hanya 1{X}")
        say(f"{R}\u2716 Jangan pakai doji.py/dog.py lama \u2014 pakai: "
            f"{os.path.basename(globals().get('__file__') or 'GOLD7.py')}{X}")
        sys.exit(3)
    # ---- PILIHAN AKUN PASTI + SESI GEHTTP MURNI (tanpa pybit) ----
    if not acct:
        acct = sa_ask_acct(kind)
    session, USE_TESTNET = sa_build_session(acct)
    _pv, _pf = _pybit_id()
    if _pf and "site-packages" not in _pf:
        say(f"{Y}\u26a0 pybit {_pv} dari {_pf} (bukan site-packages) \u2014 "
            f"TIDAK dipakai di mode 7/8.{X}")
    _bn = os.path.basename(globals().get("__file__") or "GOLD7.py")
    # AUDIT DIRI: file ini wajib v1.33 asli, selain itu TOLAK jalan
    _src = open(globals().get("__file__") or "GOLD7.py", encoding="utf-8",
                errors="ignore").read()
    if "sa_build_session" not in _src or "v1.40" not in _src[:4000]:
        say(f"{R}\u2716 FILE '{_bn}' BUKAN GOLDEN EDGE v1.40 \u2014 unduh ulang "
            f"GOLD7_V39.py & jalankan ITU (bukan file ini).{X}")
        sys.exit(77)
    add_log(f"{FW}GOLDEN EDGE v1.40{X} \u00b7 {SA_LABEL[kind]} \u2014 STANDALONE "
            f"(tanpa mesin PRO) \u00b7 file {_bn} \u00b7 PID {os.getpid()} \u00b7 "
            f"pybit {_pv} ({_pf}) \u00b7 SESI {acct.upper()} \u00b7 {sym} \u00b7 "
            f"TF {tf}m" + (f" + struktur {tf_fb}m" if kind in ("FIB8", "FIB8M") else ""))
    bal = sa_probe(sym)
    _tick = 0
    while True:
        try:
            bal = get_balance() or bal
            df = get_kline(sym, tf)
            if df is None or len(df) < 60:
                render_dash_sa(kind, bal, None, 0.0, s, _tick)
                _tick += 1
                time.sleep(2.0)
                continue
            px = get_price(sym)
            pxc = float(df["close"].iloc[len(df) - 1])
            atrv = sa_atr(df, 14)
            i = len(df) - 1
            ido = len(df) - 2              # v1.35: bar DOJI = bar CLOSED terakhir
                                           # (bar terakhir Bybit = LIVE/berjalan)
            orphan_check([sym])            # posisi yatim di bursa -> tampil
            if s["in_position"]:
                sa_manage(sym, s, px or pxc, atrv)
            else:
                if kind in ("DOJI7", "DOJI30", "DOJIM"):
                    s["last_diag"] = []
                    if kind == "DOJIM":
                        # MTF: doji 30m + BIAS struktur 60m (arah wajib searah)
                        df60 = get_kline(sym, tf_fb)
                        if df60 is None or len(df60) >= 60:
                            dset = find_doji_setup(df, px or pxc, atrv, ido,
                                                   s["last_diag"],
                                                   _tf_structure_dir(df60))
                        else:
                            s["last_diag"].append(
                                "DOJI MTF: data 60m belum cukup (>= 60 bar) \u2014 SKIP")
                            dset = None
                    else:
                        dset = find_doji_setup(df, px or pxc, atrv, ido,
                                               s["last_diag"])
                    if dset:
                        dts = int(dset.get("doji_ts", 0))
                        if dts != s.get("doji_seen"):
                            s["doji_seen"] = dts
                            _dtag = {"DOJIM": "DOJI-MTF", "DOJI30": "DOJI-30"}.get(kind,
                                                                                   "DOJI-BK")
                            say(f"\u25c8 {sym} {_dtag} "
                                f"{dset.get('doji_type', 'DOJI')} "
                                f"{'LONG' if dset['dir'] == 1 else 'SHORT'} | sweep "
                                f"{'low' if dset['dir'] == 1 else 'high'} candle "
                                f"sblmnya \u00b7 SL {dset['sl']:.6g} \u00b7 "
                                f"TP {dset['tp']:.6g} (RR {dset['rr']:.2f})")
                            try:
                                try_entry(sym, s, dset, bal, 0, atrv)
                            except Exception as _e:
                                log.exception(f"sa entry {sym}")
                                say(f"{R}\u2716 {sym} error saat entry \u2014 {_e}{X}")
                else:                      # FIB8 / FIB8M: sekali per bar tutup 30m
                    bt = int(df["ts"].iloc[i])
                    if bt != s.get("last_bar"):
                        s["last_bar"] = bt
                        s["last_diag"] = []
                        if kind == "FIB8M":
                            # MTF: tren + ZONA FIB 50-61.8% dari 60m; bar 30m =
                            # timing (mantul di zona). 60m wajib ada.
                            df60 = get_kline(sym, tf_fb)
                            if df60 is not None and len(df60) >= 60:
                                setup = find_fib_setup(df, df60, pxc, atrv, i,
                                                       s["last_diag"], struc2=df)
                            else:
                                s["last_diag"].append(
                                    "MTF: data 60m belum cukup (>= 60 bar) — SKIP")
                        else:
                            setup = find_fib_setup(df, df, pxc, atrv, i, s["last_diag"])
                            if setup is None:
                                df60 = get_kline(sym, tf_fb)
                                if df60 is not None and len(df60) >= 60:
                                    d2 = []
                                    setup = find_fib_setup(df, df60, pxc, atrv, i, d2)
                                    if setup is None and d2:
                                        s["last_diag"] = d2
                        if setup:
                            _fibtag = "FIB-MTF" if kind == "FIB8M" else "FIB-TREND"
                            say(f"\u25c8 {sym} {_fibtag} "
                                f"{'LONG' if setup['dir'] == 1 else 'SHORT'} | "
                                f"fib 50\u201361.8% + mantul \u00b7 "
                                f"SL {setup['sl']:.6g} \u00b7 "
                                f"TP1 {setup['tp1']:.6g} \u00b7 TP2 {setup['tp2']:.6g}")
                            try:
                                try_entry(sym, s, setup, bal, 0, atrv)
                            except Exception as _e:
                                log.exception(f"sa entry {sym}")
                                say(f"{R}\u2716 {sym} error saat entry \u2014 {_e}{X}")
            save_json(STATE_FILE, STATES)
            render_dash_sa(kind, bal, px, atrv, s, _tick)
            _tick += 1
            time.sleep(SA_SLEEP[kind])
        except KeyboardInterrupt:
            say("\n\u25a0 GOLDEN EDGE dihentikan.")
            break
        except Exception:
            log.exception("sa loop fatal:")
            say("\u26a0 error loop \u2014 lihat ge_bot.log")
            time.sleep(5)


def _alive(pid):
    """Cek proses pid masih hidup (lewat /proc - jalan di Termux/Android)."""
    try:
        return os.path.exists("/proc/%d" % int(pid))
    except Exception:
        return False


def _ensure_single():
    """KUNCI PROSES TUNGGAL (ge_run.pid): kalau ada proses bot lain yang masih
    hidup -> kembalikan PID-nya (pemanggil HENTIKAN bot ini). Kalau tidak,
    tulis PID sendiri dan kembalikan 0."""
    try:
        if os.path.exists("ge_run.pid"):
            with open("ge_run.pid", encoding="utf-8") as f:
                old = int((f.read().strip() or "0") or 0)
            if old and old != os.getpid() and _alive(old):
                return old
        with open("ge_run.pid", "w", encoding="utf-8") as f:
            f.write(str(os.getpid()))
    except Exception:
        pass
    return 0


def _endpoint_matches(kind):
    """True bila endpoint sesi cocok dgn pilihan akun (demo<->api-demo, real<->mainnet)."""
    ep = _SESS.get("endpoint") or ""
    if kind == "demo":
        return "api-demo.bybit.com" in ep
    return "api-demo.bybit.com" not in ep and "api.bybit.com" in ep


def selftest():
    """python3 GOLD7.py --selftest
    Bukti langsung: kunci demo -> endpoint apa? login OK? saldo berapa?
    (Tanpa dashboard - satu kali jalan, langsung kelihatan benar/salah.)"""
    print("== SELFTEST AKUN - GOLDEN EDGE v1.33 ==")
    _f = globals().get("__file__") or "GOLD7.py"
    _pf, _pv = _pybit_id()
    print("file :", os.path.abspath(_f))
    print("pybit:", _pv, "->", _pf)
    if _pf and "site-packages" not in _pf:
        print(f"{R}  \u26a0 pybit TIDAK dari site-packages \u2014 kemungkinan folder "
              f"pybit/ lokal menutupi paket asli! Rename: mv pybit pybit_bak "
              f"lalu: pip install -U pybit{X}")
    kf = load_keys_file()
    print("ge_keys.json:", ", ".join(
        f"{k}={'TERISI' if (v or {}).get('api_key') else 'kosong'}"
        for k, v in kf.items()))
    cases = [("DEMO", DEMO_API_KEY, DEMO_API_SECRET, False, True),
             ("REAL", API_KEY, API_SECRET, False, False)]
    for name, k, sec, tn, dm in cases:
        if not k or k == "GANTI":
            print(f"\n[{name}] kunci belum diisi - dilewati. "
                  f"Isi: python3 set_testnet_key.py --env demo")
            continue
        try:
            try:
                _raw = HTTP(api_key=k, api_secret=sec, testnet=tn, demo=dm)
                _raw_ep = getattr(_raw, "endpoint", "?")
            except Exception:
                _raw_ep = "(konstruksi raw gagal)"
            c = _make_http(k, sec, "demo" if dm else "real")
            ep = getattr(c, "endpoint", "?")
            print(f"\n[{name}] kunci {k[:6]}***  ->  pybit-raw: {_raw_ep}")
            print(f"     dipaksa ke : {ep}")
            r = c.get_wallet_balance(accountType="UNIFIED")
            code = int((r or {}).get("retCode", -1))
            msg = (r or {}).get("retMsg", "")
            if code == 0:
                rows = ((r or {}).get("result") or {}).get("list") or []
                eq = rows[0].get("totalEquity") if rows else None
                if eq not in (None, ""):
                    print(f"   \u2714 LOGIN OK - saldo ${float(eq):,.2f} "
                          f"(akun {rows[0].get('accountType','?')})")
                else:
                    print("   \u2714 LOGIN OK - baris kosong (saldo tidak terbaca)")
                try:
                    qa = c.query_api()
                    qr = ((qa or {}).get("result") or {})
                    ro = bool(qr.get("readOnly"))
                    perms = qr.get("permissions") or {}
                    _tr = any(perms.get(k) for k in
                              ("contractTrade", "spotTrade", "optionsTrade"))
                    _ok = _tr and not ro
                    print(f"   \u25b8 izin kunci: readOnly={ro} "
                          f"\u00b7 izin TRADE={'ADA' if _ok else 'TIDAK ADA'}")
                    if not _ok:
                        print(f"   \u26a0 penyebab error 10003 (order ditolak): kunci "
                              f"TIDAK punya izin TRADE")
                        print(f"     \u2192 Bybit \u2192 API Management \u2192 nyalakan "
                              f"izin Trade (Read-Write); utk DEMO buat kunci di "
                              f"demo-trading.bybit.com")
                except Exception as _qe:
                    print(f"   (query-api dilewati: {type(_qe).__name__})")
            else:
                print(f"   \u2716 GAGAL - retCode {code} {msg}")
                print(f"     DEMO: kunci HARUS dibuat di mode Demo Trading "
                      f"(bukan kunci mainnet). REAL: kunci utama bybit.com.")
        except Exception as e:
            print(f"   \u2716 EXCEPTION {type(e).__name__}: {e}")
    print("\nSELESAI - untuk menu 7/8 baris [DEMO] harus 'LOGIN OK' "
          "di endpoint api-demo.bybit.com.")


def _scan_copies():
    """Cari SALINAN LAMA GOLD7.py di folder yang sama (doji.py/dog.py/ge*.py
    dan sejenis) yang ukurannya berbeda dari file ini -> daftar untuk dihapus."""
    try:
        me = os.path.abspath(globals().get("__file__") or "GOLD7.py")
        d = os.path.dirname(me) or "."
        me_sz = os.path.getsize(me) if os.path.exists(me) else 0
        out = []
        # hanya SALINAN BOT (berisi penanda GOLDEN EDGE) — bukan file bantu
        for f in sorted(os.path.join(d, b) for b in os.listdir(d)
                        if b.lower().endswith(".py")):
            b = os.path.basename(f)
            if os.path.abspath(f) == me:
                continue
            try:
                with open(f, encoding="utf-8", errors="ignore") as _fh:
                    head = _fh.read(8000)
            except Exception:
                continue
            # penanda khas BOT (bukan file bantu/diagnostik)
            if b.lower() in ("ge_diag.py", "gen_diagrams.py", "gen_preview.py",
                             "patch_mfe.py", "setup_gold7.py", "test_ge.py"):
                continue
            if any(k in head for k in ("def GEHTTP", "def standalone_loop",
                                       "def confirm_env_choice", "def sa_probe")) \
                    and os.path.getsize(f) != me_sz:
                out.append(f"{b} ({os.path.getsize(f)} byte)")
        return out
    except Exception:
        return []


def main():
    # v1.33: SUBMODE/ENV_KIND/VARIANT/MODE WAJIB global — tanpa ini sesi/banner
    # membaca nilai lama (dulu menu 5 nyasar ke sesi REAL)
    global TF_TRIGGER, TF_HTF1, TF_HTF2, session, USE_TESTNET, ACCT_CHOSEN, \
           MODE, VARIANT, SUBMODE, ENV_KIND, SYMBOLS, _scan_i, _SRC_UNI, _UNI_ERR, \
           R1_MODE, ZONE_MIN_SCORE
    _me = os.path.basename(globals().get("__file__") or "GOLD7.py")
    print(f"{C}{'=' * 90}{X}")
    print(f"{C}||{X}  MENJALANKAN: {Y}{_me}{X}  \u2014  {FW}GOLDEN EDGE v1.40{X}")
    _copies = _scan_copies()
    if _copies:
        print(f"{R}{'!' * 3} SALINAN LAMA DITEMUKAN (jangan dijalankan):{X}")
        for c in _copies:
            print(f"{R}   x {c}{X}")
        print(f"{R}   Hapus: rm -f doji.py dog.py doji7.py gold7.py{X}")
    else:
        print(f"{G}   OK: tidak ada salinan lama di folder ini{X}")
    print(f"{C}{'=' * 90}{X}")
    while True:
        MODE = choose_mode()
        if MODE is None:                    # 0 = keluar
            say("\n■ GOLDEN EDGE ditutup — sampai jumpa.")
            return
        if MODE not in (1, 2, 3, 4, 6, 7, 8):
            MODE = DEFAULT_MODE
        if MODE in (1, 2, 3):
            # pasar langsung + pilihan VARIAN A-H (menu kembali: 0)
            v = ask_variant("A")
            if v is None:
                continue                    # kembali ke menu mode
            r1 = ask_r1()                   # v1.33: R1 KETAT / LONGGA
            if r1 is None:
                continue
            R1_MODE = r1
            zmin = ask_zmin()               # v1.34: zona minimum 6.5/5.5/4.0
            if zmin is None:
                continue
            ZONE_MIN_SCORE = zmin
            acct = ask_account(MODE_LABEL.get(MODE, "PRO"), default="real", confirm=True)
            if acct is None:
                continue
            VARIANT, SUBMODE, ENV_KIND = v, "", acct
            session, USE_TESTNET = make_session()
            if acct != "real" and not testnet_selfcheck():
                sys.exit(1)              # kunci demo salah -> berhenti
            break
        if MODE == 4:
            r = ask_pro()                   # PRO: pasar + varian
            if r is None:
                continue
            MODE, VARIANT = r
            r1 = ask_r1()                   # v1.33: R1 KETAT / LONGGA
            if r1 is None:
                continue
            R1_MODE = r1
            zmin = ask_zmin()               # v1.34: zona minimum 6.5/5.5/4.0
            if zmin is None:
                continue
            ZONE_MIN_SCORE = zmin
            acct = ask_account(f"PRO {MODE_LABEL[MODE]}", default="real", confirm=True)
            if acct is None:
                continue
            SUBMODE, ENV_KIND = "", acct
            session, USE_TESTNET = make_session()
            if acct != "real" and not testnet_selfcheck():
                sys.exit(1)              # kunci demo salah -> berhenti
            break
        # v1.33: MENU 5 DIHAPUS — cukup menu 4 (pasar + varian + akun DEMO/REAL).
        if MODE == 6:
            # SCALPER: TF 5m/15m/60m + TP/SL tetap % (pilih akun REAL/DEMO)
            u = ask_universe()
            if u is None:
                continue
            r1 = ask_r1()                   # v1.33: R1 KETAT / LONGGA
            if r1 is None:
                continue
            R1_MODE = r1
            acct = ask_account("SCALPER", default="real", confirm=True)
            if acct is None:
                continue
            MODE = u
            SUBMODE, ENV_KIND = "SCALPER", acct
            TF_TRIGGER, TF_HTF1, TF_HTF2 = SCALP_TRIGGER, SCALP_HTF1, SCALP_HTF2
            VARIANT = "E"                   # ambang internal scalper (3/4 · 5.5 · 1.0)
            session, USE_TESTNET = make_session()
            if acct != "real" and not testnet_selfcheck():
                sys.exit(1)              # kunci demo salah -> berhenti
            break
        if MODE == 7:
            # DOJI BREAKOUT (XAUUSDT): pilih METODE -> lalu akun DEMO / REAL
            dm = ask_doji_method()
            if dm is None:
                continue
            _nm = {1: "DOJI BREAKOUT 3m", 2: "DOJI BREAKOUT 30m",
                   3: "DOJI BREAKOUT MTF 30m+60m"}[dm]
            e = ask_account(_nm, default="demo")
            if e is None:
                continue
            if not confirm_env_choice(e, _nm):
                say("\u2192 dibatalkan \u2014 kembali ke menu (tanpa mulai apa pun).")
                continue
            SUBMODE = {1: "DOJI7", 2: "DOJI30", 3: "DOJIM"}[dm]
            ENV_KIND = e
            ACCT_CHOSEN = e
            TF_TRIGGER, TF_HTF1, TF_HTF2 = (DOJI_TF, DOJI_HTF1, DOJI_HTF2) if dm == 1 else \
                                           (DOJI30_TF, DOJI30_HTF1, DOJI30_HTF2)
            VARIANT = "F"                   # label saja (strategi doji, bukan varian)
            # SESI DIBANGUN oleh standalone_loop: pilihan akun PASTI + GEHTTP murni
            break
        if MODE == 8:
            # FIB TREND (XAUUSDT): pilih METODE -> lalu akun DEMO / REAL
            fm = ask_fib_method()
            if fm is None:
                continue
            _nm = "FIB MTF 30m+60m" if fm == 2 else "FIB TREND SCALP 30m"
            e = ask_account(_nm, default="demo")
            if e is None:
                continue
            if not confirm_env_choice(e, _nm):
                say("\u2192 dibatalkan \u2014 kembali ke menu (tanpa mulai apa pun).")
                continue
            SUBMODE, ENV_KIND = ("FIB8M" if fm == 2 else "FIB8"), e
            ACCT_CHOSEN = e
            TF_TRIGGER, TF_HTF1, TF_HTF2 = FIB_TF, FIB_HTF1, FIB_HTF2
            VARIANT = "F"
            # SESI DIBANGUN oleh standalone_loop: pilihan akun PASTI + GEHTTP murni
            break
    SYMBOLS = list(FOCUS_SYMBOLS)
    # v1.33/1.29: refresh START diulang 2x; bila get_tickers tetap gagal,
    # FALLBACK universe likuid dipakai -> TIDAK ada "1 simbol" (kecuali menu 3/7/8).
    for _ra in range(2):
        refresh_symbols(MODE)
        if len(SYMBOLS) > 1 or MODE in (3, 7, 8):
            break
        time.sleep(2)
    # v1.33: JAMINAN — menu 1/2 TIDAK PERNAH mulai dengan universe 1 simbol.
    if MODE in (1, 2) and len(SYMBOLS) <= 1:
        SYMBOLS = list(dict.fromkeys(list(FOCUS_SYMBOLS) + list(FALLBACK_UNIVERSE)))
        _SRC_UNI = "FALLBACK"
        _ms = (f"{R}\u26a0 get_tickers gagal ({_UNI_ERR or '?'}) \u2014 "
               f"universe CADANGAN dipakai ({len(SYMBOLS)} simbol likuid) \u2014 "
               f"LIVE otomatis kembali{X}")
        say(_ms)
        add_log(f"{Y}\u26a0 get_tickers gagal ({_UNI_ERR or '?'}) \u2014 "
                f"universe CADANGAN ({len(SYMBOLS)} simbol likuid) \u2014 LIVE "
                f"otomatis kembali{X}")
    log.info(f"mode {MODE_LABEL.get(MODE, MODE)} · varian {VARIANT}-{variant_label(VARIANT)}")
    for sym in SYMBOLS:
        base = new_state()
        base.update({k: v for k, v in load_json(STATE_FILE, {}).get(sym, {}).items() if k in base})
        STATES[sym] = base
    bal = get_balance()
    if SUBMODE in ("DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M"):
        log.info(f"\u25b6 {SA_LABEL.get(SUBMODE, SUBMODE)} — STANDALONE — saldo ${bal:,.2f} | XAUUSDT")
    else:
        log.info(f"▶ GOLDEN EDGE BOT dimulai — saldo ${bal:,.2f} | {len(SYMBOLS)} simbol | "
                 f"TF {TF_TRIGGER}/{TF_HTF1}/{TF_HTF2}m | zona min {ZONE_MIN_SCORE}/10 | "
                 f"cap ${RISK_CAP_USD:.2f}")
    bn = startup_banner(bal, MODE)
    if sys.stdout.isatty():
        print("\n".join(bn))
    else:
        print("\n".join(_strip(x) for x in bn))
    if SUBMODE in ("DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M"):
        add_log(f"{SA_LABEL.get(SUBMODE, SUBMODE)} — STANDALONE — saldo ${bal:,.2f}")
    else:
        add_log(f"GOLDEN EDGE BOT dimulai — saldo ${bal:,.2f} | {len(SYMBOLS)} simbol | "
                f"TF {TF_TRIGGER}/{TF_HTF1}/{TF_HTF2}m | zona ≥ {ZONE_MIN_SCORE} | cap ${RISK_CAP_USD:.2f}")
    if ENV_KIND in ("demo", "testnet"):
        _fk = (_fresh_testnet_key() if ENV_KIND == "testnet" else _fresh_demo_key())[0]
        if _fk in ("", "GANTI"):
            add_log(f"{Y}\u26a0 {ENV_KIND.upper()}: isi kunci sekali lewat "
                    f"'python3 set_testnet_key.py' (env GE_{ENV_KIND.upper()}_KEY/SECRET "
                    f"juga bisa){X}")
    _nx = cpi_next_event_days()
    if _nx is None or _nx > 120:
        log.warning("CPI_EVENTS_WIB kedaluwarsa — perbarui dari jadwal BLS "
                    "(bls.gov/schedule/news_release/cpi.htm)")
        add_log(f"{Y}⚠ daftar CPI_EVENTS_WIB tidak punya event mendatang "
                f"(>120 hari) — perbarui sesuai jadwal BLS{X}")
    if SUBMODE in ("DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M"):
        # Menu 7 & 8 = berdiri SENDIRI, beda dari PRO: loop khusus XAUUSDT
        # (tanpa zona/MTF/WATCHDOG/engine). Dashboard ringkas sendiri.
        standalone_loop(SUBMODE, ACCT_CHOSEN)
        return
    _tick = 0
    _scan_i = 0
    while True:
        try:
            refresh_symbols(MODE)
            news_shock_check()
            bal = get_balance()
            dsyms = []
            hero_sym = "XAUUSDT" if (MODE == 3 or SUBMODE in ("DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M")) else "BTCUSDT"
            # posisi terbuka (semua STATE, termasuk koin yang keluar universe)
            # + hero selalu diprioritaskan tiap siklus; sisanya round-robin
            # v1.33: SELEKSI SCAN DETERMINISTIK — satu sumber kebenaran = SYMBOLS.
            # 1) SETIAP simbol universe PASTI punya state (tidak ada state
            #    kosong/tertinggal) -> rest & posisi selalu akurat, mustahil
            #    macet "sisa 1" akibat state tidak lengkap.
            for _x in SYMBOLS:
                if not isinstance(STATES.get(_x), dict):
                    STATES[_x] = new_state()
            pos_syms = [x for x in SYMBOLS
                        if STATES.get(x, {}).get("in_position")]
            # 2) HEAL posisi basi: pemicu MUTLAK >8 posisi ATAU "sisa
            #    mencurigakan" (universe besar tapi sisa jauh < SCAN_CHUNK)
            #    -> verifikasi bursa (1x/menit) & bersihkan yang tak nyata.
            _min_sisa = min(SCAN_CHUNK, max(4, len(SYMBOLS) // 8))
            _sus = (len(pos_syms) > 8 or
                    (len(SYMBOLS) > 24 and
                     len(SYMBOLS) - len(pos_syms) - 1 < _min_sisa))
            if _sus:
                _vp = _verify_positions()
                if _vp is not None:
                    for _x in [x for x in SYMBOLS
                               if STATES.get(x, {}).get("in_position")]:
                        if _x not in _vp:
                            _st = STATES.get(_x)
                            if isinstance(_st, dict):
                                _st.update({"in_position": False, "side": None,
                                            "entry": 0.0, "sl": 0.0, "tp": 0.0,
                                            "tp1": 0.0, "tp2": 0.0})
                                say(f"{D}\u21ba {_x} state basi dibersihkan "
                                    f"(tidak ada posisi di bursa){X}")
                    pos_syms = [x for x in SYMBOLS
                                if STATES.get(x, {}).get("in_position")]
                elif len(pos_syms) > 0:
                    log.warning("verifikasi posisi gagal \u2014 "
                                "posisi tidak bisa dipastikan (%d)" % len(pos_syms))
            rest = [x for x in SYMBOLS
                    if not STATES.get(x, {}).get("in_position") and x != hero_sym]
            scan = list(pos_syms)
            if hero_sym not in scan:
                scan.append(hero_sym)
            if rest:
                # v1.33: chunk DINAMIS (rotasi penuh <= ~8 siklus); take TIDAK
                # pernah 0 dan TIDAK tergantung jumlah posisi (fix v1.33).
                global _LAST_CHUNK
                _LAST_CHUNK = auto_chunk(len(rest))
                take = min(len(rest), max(SCAN_CHUNK,
                                          (len(rest) + ROT_CYCLES - 1) // ROT_CYCLES))
                if take < 1:
                    take = 1
                scan += [rest[(_scan_i + j) % len(rest)] for j in range(take)]
                _scan_i = (_scan_i + take) % len(rest)
            else:
                _LAST_CHUNK = len(scan)
                take = 0
            _DBG.update({"rest": len(rest), "pos": len(pos_syms), "take": take,
                         "last_sym": len(scan), "univ": len(SYMBOLS),
                         "state": len(STATES)})
            # posisi "yatim" di bursa (entry tak terkonfirmasi / manual) — sekali
            # per keadaan selalu tampil besar; bot tidak mengelola posisi ini.
            orphan_check(scan)
            for sym in scan:
                try:
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
                        _wd_err(sym, "data <60 bar (kline \u2716)")
                        continue
                    con = {}
                    for key, dfs in (("15", df15), ("60", df60), ("240", df240)):
                        c = compute_tf_confluence(dfs)
                        if c is None:
                            break
                        con[key] = c
                    if len(con) != 3:
                        _wd_err(sym, "konfluensi MTF gagal")
                        continue
                    i15 = len(df15) - 2
                    px15 = float(df15["close"].iloc[-1])       # live: tampilan & manage posisi
                    px_closed = float(df15["close"].iloc[i15])  # bar TUTUP: keputusan R1-R3
                    atrv15, volbase15 = zone_sample_at(df15, len(df15) - 1)
                    vol_guard_check(sym, df15, px15, atrv15, s)
                    s["prev_sig15"] = s.get("prev_sig15", 0)
                    sig15_now = sig_at(con["15"], i15,
                                        E_SIG_MIN if (VARIANT == "E" or SUBMODE == "SCALPER")
                                        else None)
                    # ----- zona pada 15m (bar tutup) -----
                    _prev_ph = {(z.get("kind"), z.get("dir"), z.get("born_ts")): z
                                for z in (s.get("zones") or [])}
                    zones15 = build_zones(df15)
                    zones15 = restore_zones(zones15, s.get("zones") or [])
                    zones15 = update_zones(zones15, df15, px_closed, atrv15,
                                           REACT_ATR * atrv15)
                    # Pine pends: zona yang BARU tersweep -> antrean reaksi
                    for z in zones15:
                        if z.phase == 2 and z.born_ts is not None:
                            _pz = _prev_ph.get((z.kind, z.dir, z.born_ts)) or {}
                            if _pz.get("phase", 0) < 2:
                                react_push(s, z.dir, px_closed, atrv15, i15)
                    react_track(s, px_closed, i15)
                    s["zones"] = [z.to_dict() for z in zones15]   # resolved tetap ada (Pine keepDone)
                    # ----- manajemen posisi -----
                    if s["in_position"]:
                        manage(sym, s, atrv15)
                    # ----- ATURAN 3-LANGKAH (sekali per bar tutup 15m) -----
                    bar_ts = int(df15["ts"].iloc[i15])
                    regime = None
                    if bar_ts != s.get("last_bar") and not s["in_position"]:
                        s["last_bar"] = bar_ts
                        regime = market_regime(df60)      # ditampilkan & dipakai varian B
                        if SUBMODE == "SCALPER":
                            s["last_diag"] = []
                            setup = find_scalp_setup(con, df15, zones15, px_closed,
                                                     atrv15, volbase15,
                                                     s.get("prev_sig15", 0), s["last_diag"])
                        elif SUBMODE == "DOJI7":
                            setup = None        # entry DOJI: blok TOUCH per-pass di bawah
                        elif SUBMODE == "FIB8":
                            # struktur utama di chart 30m (video); bila swing terakhir
                            # sudah tua/tak valid -> fallback ADAPTIF ke 60m
                            s["last_diag"] = []
                            setup = find_fib_setup(df15, df15, px_closed, atrv15, i15,
                                                   s["last_diag"])
                            if setup is None:
                                setup = find_fib_setup(df15, df60, px_closed, atrv15, i15,
                                                       s["last_diag"])
                        else:
                            s["last_diag"] = []
                            setup = find_setup(con, df15, zones15, px_closed, atrv15,
                                               volbase15, s.get("prev_sig15", 0),
                                               VARIANT, regime, s["last_diag"])
                        if setup:
                            s["last_diag"] = []   # setup ditemukan -> GATE kosong
                            _tag = "DOJI-BK" if SUBMODE == "DOJI7" else \
                                   ("FIB-TREND" if SUBMODE == "FIB8" else
                                    ("SCALP" if SUBMODE == "SCALPER" else "GE-R3"))
                            say(f"◈ {B}{sym}{X} {_tag} {'LONG' if setup['dir']==1 else 'SHORT'} "
                                  f"| 15M {setup['conf15']}/4 · 1H {setup['sig_h1']:+d} · "
                                  f"4H {setup['sig_h4']:+d} | zona {'▼D' if setup['dir']==1 else '▲S'} "
                                  f"{setup['zone_score']:.1f}/10 @ {setup['zone'].top:.6g}-{setup['zone'].bot:.6g} "
                                  f"| RR {setup['rr']:.2f}")
                            log.info(f"{sym} setup GE-R3 "
                                     f"{'LONG' if setup['dir']==1 else 'SHORT'} "
                                     f"zone {setup['zone_score']:.1f}/10 rr {setup['rr']:.2f}")
                            _n_open = sum(1 for st in STATES.values() if st["in_position"])
                            try_entry(sym, s, setup, bal, _n_open, atrv15)
                    # MODE 7 (DOJI): entry TOUCH tiap pass — video: "nyentuh aja,
                    # enggak usah tunggu close". Doji wajib bar CLOSED terakhir
                    # (i15); sekali doji diproses -> jangan diulang (doji_seen).
                    if SUBMODE == "DOJI7" and not s["in_position"]:
                        s["last_diag"] = []
                        dset = find_doji_setup(df15, px15, atrv15, i15, s["last_diag"])
                        if dset:
                            s["last_diag"] = []   # gate bersih: doji valid → boleh entry
                            dts = int(dset.get("doji_ts", 0))
                            if dts != s.get("doji_seen"):
                                s["doji_seen"] = dts
                                say(f"\u25c8 {B}{sym}{X} DOJI-BK "
                                    f"{'LONG' if dset['dir']==1 else 'SHORT'} | "
                                    f"sweep {'low' if dset['dir']==1 else 'high'} "
                                    f"candle sblmnya \u00b7 SL {dset['sl']:.6g} \u00b7 "
                                    f"TP {dset['tp']:.6g} (RR {dset['rr']:.2f})")
                                log.info(f"{sym} doji-breakout "
                                         f"{'LONG' if dset['dir']==1 else 'SHORT'} "
                                         f"sl {dset['sl']:.6g} tp {dset['tp']:.6g}")
                                _n_open = sum(1 for st in STATES.values()
                                              if st["in_position"])
                                try_entry(sym, s, dset, bal, _n_open, atrv15)
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
                                  "cd": bar_countdown(con["15"]),
                                  "regime": regime})
                    _WD[sym] = dsyms[-1]      # v1.33: cache WATCHDOG penuh
                    save_json(STATE_FILE, STATES)
                    time.sleep(0.25 if SUBMODE in ("SCALPER", "DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M")
                               else (0.25 if len(SYMBOLS) > 5 else 0.2))

                except Exception as _e:
                    log.exception(f"scan {sym} error:")
                    _wd_err(sym, "error: %s: %s" % (type(_e).__name__, _e))
            flush_vol_log()
            try:
                render_dash(bal, {"syms": dsyms, "tick": _tick})
            except Exception:
                log.exception("render_dash:")
                add_log("\u26a0 render dashboard error \u2014 lihat ge_bot.log")
            _tick += 1
            time.sleep(SCALP_LOOP_SLEEP if SUBMODE in ("SCALPER", "DOJI7", "DOJI30", "DOJIM", "FIB8", "FIB8M")
                       else 20)
        except KeyboardInterrupt:
            say("\n■ GOLDEN EDGE bot dihentikan.")
            break
        except Exception:
            log.exception("loop fatal:")     # traceback lengkap utk debugging
            time.sleep(10)

if __name__ == "__main__":
    if "--check" in sys.argv:
        _check_cmd()
    elif "--selftest" in sys.argv:
        selftest()
    else:
        main()
