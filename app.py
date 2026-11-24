# -*- coding: utf-8 -*-
"""
KlikStudio - Sistem Administrasi Booking Foto Studio
Jalankan:  streamlit run app.py
"""
import base64
import html
from datetime import date, datetime, time
from pathlib import Path

import streamlit as st
from PIL import Image

import database as dbx
from database import fmt_jam, rupiah, tgl_id

ASSETS = Path(__file__).parent / "assets"
SEED_CONTOH = True          # ubah ke False kalau tidak mau data contoh (Rina, Dimas, dst.)

logo_icon = ASSETS / "logo_icon_transparent.png"
st.set_page_config(page_title="KlikStudio",
                   page_icon=Image.open(logo_icon) if logo_icon.is_file() else "📷",
                   layout="wide", initial_sidebar_state="expanded")

# ====================================================================== TEMA
CSS = """
<style>
:root{
  --accent:#9C7A54; --accent-d:#80613F; --accent-l:#EFE5D9; --cream:#F3EFEA; --cream-2:#E6DFD5;
  --ink:#231F1E; --muted:#6E655F; --line:#DDD3C7;
}
.stApp{background:var(--cream); color:var(--ink);}
[data-testid="stHeader"]{background:transparent;}
.block-container{padding-top:2.2rem; padding-bottom:3rem; max-width:1180px;}
h1,h2,h3,h4,h5{color:var(--ink)!important; letter-spacing:-.01em;}

/* ---------- sidebar ---------- */
[data-testid="stSidebar"]{background:var(--cream-2); border-right:1px solid var(--line);}
[data-testid="stSidebar"] .block-container{padding-top:1.2rem;}
.side-logo{padding:.2rem .2rem 1rem .2rem; margin-bottom:1.2rem; border-bottom:1px solid var(--line);}
.side-logo img{width:100%; display:block;}
[data-testid="stSidebar"] div[role="radiogroup"]{gap:.45rem;}
[data-testid="stSidebar"] label[data-baseweb="radio"]{
  background:transparent; border-radius:13px; padding:.72rem .8rem; width:100%;
  border:1px solid transparent; border-left:3px solid transparent;
  transition:all .15s ease; cursor:pointer;}
[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child{display:none;}
[data-testid="stSidebar"] label[data-baseweb="radio"]:hover{background:rgba(255,255,255,.72);}
[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked){
  background:#fff; border-color:#D7C8B6; border-left-color:var(--accent);}
[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) *{color:var(--ink)!important; font-weight:650;}
[data-testid="stSidebar"] label[data-baseweb="radio"] p{font-size:.94rem; margin:0;}
.side-nav-label{margin:.25rem .8rem .55rem; color:var(--muted); font-size:.7rem;
  font-weight:700; letter-spacing:.12em;}
.side-admin{margin:0 .8rem .9rem; padding:.65rem .8rem; background:rgba(255,255,255,.55);
  border:1px solid var(--line); border-radius:12px;}
.side-admin span{display:block; color:var(--muted); font-size:.65rem; letter-spacing:.1em; font-weight:700;}
.side-admin b{display:block; margin-top:.15rem; color:var(--ink); font-size:.88rem;}

/* ---------- hero ---------- */
.hero{display:flex; align-items:center; justify-content:space-between; gap:1.5rem; flex-wrap:wrap;
  background:#fff; border:1px solid var(--line); border-left:5px solid var(--accent);
  border-radius:22px; padding:1.8rem 2rem; color:var(--ink);
  box-shadow:0 8px 26px rgba(35,31,30,.05); margin-bottom:1.4rem;}
.hero-copy{max-width:680px;}
.hero h1{color:var(--ink)!important; font-size:2.05rem; margin:.2rem 0 .55rem 0; font-weight:750;}
.hero p{margin:.1rem 0; color:var(--muted); font-size:.96rem;}
.hero .eyebrow{font-size:.76rem; letter-spacing:.13em; text-transform:uppercase; color:var(--accent-d); font-weight:700;}
.hero-date{display:inline-flex; margin-bottom:.45rem!important; padding:.32rem .7rem;
  background:var(--cream); color:var(--muted)!important; border-radius:999px; font-size:.8rem!important;}
.hero-logo{background:transparent; border-radius:0; padding:0; margin-left:auto;}
.hero-logo img{width:190px; max-width:100%; height:auto; display:block;}

/* ---------- login ---------- */
.login-logo{text-align:center; margin:2.8rem auto 1.4rem; max-width:300px;}
.login-logo img{width:100%; display:block;}
.login-title{text-align:center; margin-bottom:1.2rem;}
.login-title h1{font-size:2rem; margin:.2rem 0 .35rem;}
.login-title p{color:var(--muted); margin:0; font-size:.94rem;}
.login-note{text-align:center; color:var(--muted); font-size:.78rem; margin-top:1rem;}
.auth-form-title{text-align:center; margin-bottom:1.15rem;}
.auth-form-title h2{font-size:1.3rem; margin:0 0 .3rem;}
.auth-form-title p{color:var(--muted); font-size:.86rem; margin:0;}

.page-title h1{font-size:2rem; margin:0 0 .15rem 0; font-weight:700;}
.page-title p{color:var(--muted); margin:0 0 1.1rem 0;}

/* ---------- cards ---------- */
.kcard{background:#fff; border-radius:20px; padding:1.25rem 1.4rem; border:1px solid var(--line);
  box-shadow:0 2px 14px rgba(68,67,65,.05);}
.kcard.m-amber{border-left:3px solid #C6A16E;}
.kcard.m-bronze{border-left:3px solid var(--accent);}
.metric{display:flex; align-items:center; gap:1.1rem;}
.metric .ico{width:58px; height:58px; border-radius:18px; display:flex; align-items:center;
  justify-content:center; font-size:1.7rem; flex:0 0 auto;}
.metric .lbl{color:var(--muted); font-size:.92rem;}
.metric .val{font-size:2.4rem; font-weight:700; line-height:1.05; color:var(--ink);}
.metric .sub{color:var(--muted); font-size:.8rem;}
.m-bronze .ico{background:var(--accent-l);} .m-amber .ico{background:#E6DFD5;}
.sect{font-size:1.15rem; font-weight:650; margin:1.5rem 0 .6rem 0; color:var(--ink);}
.sect small{font-weight:400; color:var(--muted); font-size:.85rem; margin-left:.4rem;}

/* ---------- tabel ---------- */
.ktable-wrap{overflow-x:auto; border-radius:18px; border:1px solid var(--line); background:#fff;}
table.ktable{width:100%; border-collapse:collapse; font-size:.92rem;}
.ktable th{background:var(--cream-2); text-align:left; padding:.7rem .95rem; color:var(--muted);
  font-weight:600; font-size:.78rem; letter-spacing:.05em; text-transform:uppercase; border-bottom:1px solid var(--line);}
.ktable td{padding:.7rem .95rem; border-bottom:1px solid #F0ECE4; color:var(--ink);}
.ktable tr:last-child td{border-bottom:none;}
.ktable tbody tr:hover td{background:#FBFAF7;}
.empty{padding:1.4rem; text-align:center; color:var(--muted); background:#fff; border:1px dashed var(--line);
  border-radius:18px;}
.badge{display:inline-block; padding:.18rem .7rem; border-radius:999px; font-size:.78rem; font-weight:600;}
.b-menunggu{background:#F5E9D7; color:#80613F;} .b-dikonfirmasi{background:#E7E1D9; color:#5F554C;}
.b-selesai{background:#EEE8E1; color:#655B53;} .b-dibatalkan{background:#F3E2DE; color:#98584C;}
.b-tersedia{background:#E7E1D9; color:#5F554C;} .b-terpesan{background:#EFE5D9; color:#80613F;}
.b-nonaktif{background:#E6DFD5; color:#6E655F;}

/* ---------- nota / tiket ---------- */
.ticket{background:#fff; border:2px dashed var(--accent); border-radius:22px; padding:1.3rem 1.5rem; max-width:430px;}
.ticket-head{display:flex; align-items:center; gap:.8rem; padding-bottom:.8rem; border-bottom:1px solid var(--line);}
.ticket-head img{height:46px;} .ticket-head b{font-size:1.05rem; display:block;}
.ticket-head span{color:var(--muted); font-size:.82rem;}
.ticket-no{text-align:center; padding:.9rem 0 .5rem 0;}
.ticket-no span{color:var(--muted); font-size:.8rem; letter-spacing:.1em; text-transform:uppercase;}
.ticket-no h2{font-size:3.4rem; margin:0; color:var(--accent-d)!important; font-weight:800;}
.ticket-row{display:flex; justify-content:space-between; padding:.32rem 0; font-size:.92rem; gap:1rem;}
.ticket-row span{color:var(--muted);} .ticket-row b{text-align:right;}
.ticket-foot{margin-top:.8rem; padding-top:.7rem; border-top:1px dashed var(--line); text-align:center;
  color:var(--muted); font-size:.8rem;}

/* ---------- widget ---------- */
.stButton > button, [data-testid="stDownloadButton"] button, .stFormSubmitButton > button{
  width:100%; border-radius:14px; padding:.55rem 1rem; font-weight:600; border:1px solid var(--line);
  background:#fff; color:var(--ink); transition:all .15s ease;}
.stButton > button:hover, [data-testid="stDownloadButton"] button:hover, .stFormSubmitButton > button:hover{
  border-color:var(--accent); color:var(--accent-d); transform:translateY(-1px);}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"], button[data-testid="stBaseButton-primaryFormSubmit"]{
  background:var(--accent)!important; border:none!important; color:#fff!important;}
.stButton > button[kind="primary"]:hover, button[data-testid="stBaseButton-primary"]:hover{
  background:var(--accent-d)!important; color:#fff!important;}
button[data-baseweb="tab"]{font-weight:600; font-size:.98rem;}
div[data-baseweb="tab-highlight"]{background-color:var(--accent-d)!important;}
button[data-baseweb="tab"][aria-selected="true"]{color:var(--accent-d)!important;}
[data-testid="stVerticalBlockBorderWrapper"]{border-radius:18px!important; background:#fff;
  border-color:var(--line)!important;}
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="base-input"]{border-radius:12px!important;}
.foot{text-align:center; color:var(--muted); font-size:.8rem; margin-top:2.4rem;}
.group-card{max-width:680px; margin:2.4rem auto 0; padding:1.35rem 1.6rem; background:#fff;
  border:1px solid var(--line); border-top:3px solid var(--accent); border-radius:18px;
  box-shadow:0 2px 14px rgba(68,67,65,.05);}
.group-card h3{margin:0 0 .8rem; color:var(--accent-d)!important; font-size:1.05rem;}
.group-card ol{margin:0; padding-left:1.4rem; color:var(--ink); line-height:1.9;}
.group-card li{padding-left:.2rem;}
.group-card .nim{color:var(--muted);}
@media (max-width:640px){
  .hero{padding:1.35rem; gap:.7rem;}
  .hero h1{font-size:1.65rem;}
  .hero-logo img{width:140px;}
  .hero-logo{margin-left:0;}
  .metric .val{font-size:2rem;}
  .group-card{padding:1.1rem 1.2rem;}
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ====================================================================== HELPER UI
def H(s: str):
    """Render HTML (baris digabung supaya tidak dianggap code-block oleh markdown)."""
    st.markdown(" ".join(line.strip() for line in s.strip().splitlines()), unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def img_uri(name: str) -> str:
    image = ASSETS / name
    if image.is_file():
        return "data:image/png;base64," + base64.b64encode(image.read_bytes()).decode()

    wordmark = name == "logo_wordmark_transparent.png"
    text = '<text x="90" y="58" font-family="sans-serif" font-size="38" font-weight="700" fill="#80613F">KlikStudio</text>' if wordmark else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {"360" if wordmark else "72"} 72">'
           '<rect x="4" y="16" width="64" height="48" rx="10" fill="#9C7A54"/>'
           '<path d="M22 16l5-8h18l5 8" fill="#80613F"/>'
           '<circle cx="36" cy="40" r="15" fill="#F3EFEA"/>'
           '<circle cx="36" cy="40" r="8" fill="#9C7A54"/>'
           f'{text}</svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


def esc(x) -> str:
    return html.escape(str(x))


def badge(status: str) -> str:
    return f'<span class="badge b-{status.lower()}">{esc(status)}</span>'


def tabel(headers, data, badge_cols=(), kosong="Belum ada data."):
    if not data:
        H(f'<div class="empty">{esc(kosong)}</div>')
        return
    th = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = ""
    for row in data:
        tds = "".join(f"<td>{badge(c) if i in badge_cols else esc(c)}</td>" for i, c in enumerate(row))
        body += f"<tr>{tds}</tr>"
    H(f'<div class="ktable-wrap"><table class="ktable"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')


def judul(t: str, sub: str):
    H(f'<div class="page-title"><h1>{esc(t)}</h1><p>{esc(sub)}</p></div>')


def sect(t: str, small: str = ""):
    H(f'<div class="sect">{esc(t)}<small>{esc(small)}</small></div>')


def flash(kind: str, msg: str, nota_booking: int = None):
    st.session_state["flash"] = (kind, msg)
    if nota_booking:
        st.session_state["flash_nota"] = nota_booking


def show_flash():
    f = st.session_state.pop("flash", None)
    if f:
        {"success": st.success, "error": st.error, "warning": st.warning, "info": st.info}[f[0]](
            f[1], icon={"success": "✅", "error": "⛔", "warning": "⚠️", "info": "ℹ️"}[f[0]])
    idb = st.session_state.pop("flash_nota", None)
    if idb:
        b = dbx.get_booking(idb)
        if b and b["nomor_antrean"]:
            tampil_nota(b, key=f"flash_{idb}")


def ticket_html(b: dict) -> str:
    def row(k, v):
        return f'<div class="ticket-row"><span>{esc(k)}</span><b>{esc(v)}</b></div>'
    return (f'<div class="ticket"><div class="ticket-head"><img src="{img_uri("logo_icon_transparent.png")}">'
            f'<div><b>KLIK STUDIO</b><span>Nota Antrean Digital</span></div></div>'
            f'<div class="ticket-no"><span>Nomor Antrean</span><h2>{int(b["nomor_antrean"]):03d}</h2></div>'
            + row("Tanggal", tgl_id(b["tanggal"]))
            + row("Jam", f'{fmt_jam(b["jam_mulai"])} - {fmt_jam(b["jam_selesai"])}')
            + row("Nama", b["nama_pelanggan"]) + row("Telepon", b["no_telepon"])
            + row("Paket", f'{b["nama_paket"]} ({b["durasi_sesi"]} mnt)') + row("Harga", rupiah(b["harga"]))
            + row("Status", b["status_booking"])
            + f'<div class="ticket-foot">ID Booking {b["id_booking"]}</div></div>')


def tampil_nota(b: dict, key: str):
    H(ticket_html(b))
    st.write("")
    c, _ = st.columns([1, 2])
    with c:
        st.download_button("⬇️ Unduh Nota (.txt)", dbx.nota_txt(b).encode("utf-8"),
                           file_name=f"nota_antrean_{b['tanggal']}_{int(b['nomor_antrean']):03d}.txt",
                           mime="text/plain", key=f"dl_{key}")


def label_booking(b: dict) -> str:
    return (f"#{b['id_booking']} · {b['nama_pelanggan']} · {tgl_id(b['tanggal'])} "
            f"{fmt_jam(b['jam_mulai'])}-{fmt_jam(b['jam_selesai'])} · {b['status_booking']}")


def rentang_tanggal(v):
    if isinstance(v, (tuple, list)):
        if len(v) == 2:
            return v[0], v[1]
        if len(v) == 1:
            return v[0], v[0]
        return None, None
    return v, v


# ====================================================================== NAVIGASI & AUTENTIKASI
MENU = ["🏠  Beranda", "🗓️  Kelola Studio", "👥  Data Pelanggan", "📝  Booking", "🎟️  Nota Antrean"]
if "menu" not in st.session_state:
    st.session_state["menu"] = MENU[0]
if "admin" not in st.session_state:
    st.session_state["admin"] = None
if "auth_mode" not in st.session_state:
    st.session_state["auth_mode"] = "Sign In"
if "auth_choice" not in st.session_state:
    st.session_state["auth_choice"] = st.session_state["auth_mode"]


def goto(m: str):
    st.session_state["menu"] = m


def sync_auth_mode():
    st.session_state["auth_mode"] = st.session_state["auth_choice"]


def page_login():
    _, kolom, _ = st.columns([1, 1.35, 1])
    with kolom:
        H(f'<div class="login-logo"><img src="{img_uri("logo_wordmark_transparent.png")}"></div>')
        H('<div class="login-title"><h1>Akses Admin</h1><p>Pilih Sign In atau Sign Up untuk melanjutkan.</p></div>')
        if st.session_state["auth_choice"] != st.session_state["auth_mode"]:
            st.session_state["auth_choice"] = st.session_state["auth_mode"]
        st.segmented_control("Pilihan akses", ["Sign In", "Sign Up"], key="auth_choice",
                             on_change=sync_auth_mode)
        notice = st.session_state.pop("auth_notice", None)
        if notice:
            {"success": st.success, "error": st.error}[notice[0]](notice[1])
        with st.container(border=True):
            if st.session_state["auth_mode"] == "Sign Up":
                H('<div class="auth-form-title"><h2>Buat Akun Admin</h2>'
                  '<p>Daftarkan username dan password untuk mengakses dashboard.</p></div>')
                with st.form("form_daftar_admin", clear_on_submit=True):
                    username = st.text_input("Username", key="signup_username", max_chars=32,
                                             placeholder="contoh: admin_studio",
                                             help="3-32 karakter: huruf, angka, atau underscore.")
                    password = st.text_input("Password", key="signup_password", type="password",
                                             max_chars=128, placeholder="minimal 8 karakter")
                    konfirmasi = st.text_input("Konfirmasi Password", key="signup_confirm", type="password",
                                               max_chars=128, placeholder="ulangi password")
                    if st.form_submit_button("Daftar Akun", type="primary"):
                        if password != konfirmasi:
                            st.error("Konfirmasi password tidak sama.")
                        else:
                            ok, msg = dbx.daftar_admin(username, password)
                            if ok:
                                st.session_state["auth_notice"] = ("success", msg)
                                st.session_state["login_username"] = username.strip()
                                st.session_state["auth_mode"] = "Sign In"
                                st.rerun()
                            else:
                                st.error(msg)
            else:
                H('<div class="auth-form-title"><h2>Sign In</h2>'
                  '<p>Masuk menggunakan akun admin yang sudah terdaftar.</p></div>')
                with st.form("form_login_admin"):
                    username = st.text_input("Username", key="login_username", placeholder="masukkan username admin")
                    password = st.text_input("Password", key="login_password", type="password",
                                             placeholder="masukkan password admin")
                    if st.form_submit_button("Masuk Dashboard", type="primary"):
                        admin = dbx.autentikasi_admin(username, password)
                        if admin:
                            st.session_state["admin"] = admin
                            st.session_state["menu"] = MENU[0]
                            st.rerun()
                        else:
                            st.error("Username atau password salah.")
        H('<div class="login-note">Akun baru dapat dibuat melalui pilihan Sign Up.</div>')


dbx.init_db(SEED_CONTOH)
if not st.session_state.get("admin"):
    page_login()
    st.stop()

with st.sidebar:
    H(f'<div class="side-logo"><img src="{img_uri("logo_wordmark_transparent.png")}"></div>')
    admin = st.session_state["admin"]
    H(f'<div class="side-admin"><span>LOGIN SEBAGAI</span><b>{esc(admin["nama"] or admin["username"])}</b></div>')
    H('<div class="side-nav-label">MENU UTAMA</div>')
    st.radio("Menu", MENU, key="menu", label_visibility="collapsed")
    if st.button("Logout", key="tombol_logout", use_container_width=True):
        st.session_state["admin"] = None
        st.session_state["auth_mode"] = "Sign In"
        st.session_state["auth_choice"] = "Sign In"
        st.session_state["auth_notice"] = None
        for key in ("login_username", "login_password", "signup_username", "signup_password", "signup_confirm"):
            st.session_state.pop(key, None)
        st.rerun()


# ====================================================================== HALAMAN: BERANDA
def page_beranda():
    today = date.today()
    H(f'''<div class="hero"><div class="hero-copy"><div class="eyebrow">Dashboard Admin</div>
        <h1>Selamat datang di KlikStudio 👋</h1>
        <p class="hero-date">{esc(dbx.hari_tgl_id(today))}</p>
        <p>Kelola jadwal, paket foto, booking, dan nota antrean dari satu tempat.</p></div>
        <div class="hero-logo"><img src="{img_uri("logo_wordmark_transparent.png")}"></div></div>''')
    show_flash()

    menunggu = dbx.list_booking("b.status_booking='Menunggu'")
    menunggu.sort(key=lambda b: (b["tanggal"], b["jam_mulai"]))
    n_slot = dbx.one("SELECT COUNT(*) c FROM jadwal_studio WHERE tanggal=? AND status_jadwal='Tersedia'",
                     (today.isoformat(),))["c"]

    c1, c2 = st.columns(2, gap="medium")
    with c1:
        H(f'<div class="kcard metric m-amber"><div class="ico">⏳</div><div><div class="lbl">Booking Menunggu</div>'
          f'<div class="val">{len(menunggu)}</div><div class="sub">menunggu konfirmasi admin</div></div></div>')
    with c2:
        H(f'<div class="kcard metric m-bronze"><div class="ico">🕘</div><div><div class="lbl">Slot Tersedia Hari Ini</div>'
          f'<div class="val">{n_slot}</div><div class="sub">slot berstatus Tersedia</div></div></div>')

    sect("Akses cepat", "Pintasan menu")
    a, b, c = st.columns(3, gap="small")
    a.button("➕  Booking Baru", on_click=goto, args=(MENU[2],), type="primary", key="qa1")
    b.button("🗓️  Kelola Slot", on_click=goto, args=(MENU[1],), key="qa2")
    c.button("🎟️  Lihat Nota", on_click=goto, args=(MENU[3],), key="qa3")

    sect("Perlu segera diperhatikan", "Booking yang menunggu konfirmasi")
    if not menunggu:
        H('<div class="empty">🎉 Tidak ada booking yang menunggu. Semua sudah beres!</div>')
    for bk in menunggu:
        with st.container(border=True):
            ci, cb1, cb2 = st.columns([4, 1.3, 1.3], vertical_alignment="center")
            ci.markdown(f"**{bk['nama_pelanggan']}** · {bk['nama_paket']}  \n"
                        f"📅 {tgl_id(bk['tanggal'])} · 🕘 {fmt_jam(bk['jam_mulai'])}-{fmt_jam(bk['jam_selesai'])}"
                        f" · 📞 {bk['no_telepon']}")
            if cb1.button("✅ Konfirmasi", key=f"dk_{bk['id_booking']}", type="primary"):
                ok, msg = dbx.ubah_status(bk["id_booking"], "Dikonfirmasi")
                flash("success" if ok else "error", msg)
                st.rerun()
            if cb2.button("✖️ Batalkan", key=f"db_{bk['id_booking']}"):
                ok, msg = dbx.ubah_status(bk["id_booking"], "Dibatalkan")
                flash("success" if ok else "error", msg)
                st.rerun()

    sect("Jadwal hari ini", tgl_id(today.isoformat()))
    slots = dbx.rows("SELECT * FROM jadwal_studio WHERE tanggal=? ORDER BY jam_mulai", (today.isoformat(),))
    aktif = {x["id_jadwal"]: x for x in dbx.list_booking("b.status_booking IN ('Menunggu','Dikonfirmasi','Selesai')")}
    by_slot = {x["id_jadwal"]: x for x in aktif.values()}
    data = []
    for s in slots:
        bk = by_slot.get(s["id_jadwal"])
        data.append([f"{fmt_jam(s['jam_mulai'])} - {fmt_jam(s['jam_selesai'])}", s["status_jadwal"],
                     bk["nama_pelanggan"] if bk else "-", bk["nama_paket"] if bk else "-",
                     bk["status_booking"] if bk else "-"])
    if not data:
        H('<div class="empty">Belum ada slot untuk hari ini. Buat di menu Kelola Studio.</div>')
    else:
        th = "".join(f"<th>{h}</th>" for h in ["Jam", "Status Slot", "Pelanggan", "Paket", "Status Booking"])
        body = ""
        for r in data:
            sb = badge(r[4]) if r[4] != "-" else "-"
            body += (f"<tr><td>{esc(r[0])}</td><td>{badge(r[1])}</td><td>{esc(r[2])}</td>"
                     f"<td>{esc(r[3])}</td><td>{sb}</td></tr>")
        H(f'<div class="ktable-wrap"><table class="ktable"><thead><tr>{th}</tr></thead><tbody>{body}</tbody></table></div>')

    H('''<div class="group-card"><h3>Kelompok 7</h3><ol>
        <li>Elvalena Destyananta <span class="nim">(NIM 4.52.24.3.08)</span></li>
        <li>Elvira Febriani Putri <span class="nim">(NIM 4.52.24.3.09)</span></li>
        <li>Nadilah Nur Adha <span class="nim">(NIM 4.52.24.3.19)</span></li>
        <li>Ziyada Ilma Rizqina <span class="nim">(NIM 4.52.24.3.29)</span></li>
    </ol></div>''')


# ====================================================================== HALAMAN: KELOLA STUDIO
def tab_slot():
    cfg = dbx.get_settings()
    sect("Buat slot otomatis", "slot dibentuk dari jam operasional, durasi slot, dan jeda")
    with st.form("form_slot"):
        c1, c2, c3, c4 = st.columns(4)
        buka = c1.time_input("Jam buka", value=datetime.strptime(cfg["buka"], "%H:%M").time(), step=900)
        tutup = c2.time_input("Jam tutup", value=datetime.strptime(cfg["tutup"], "%H:%M").time(), step=900)
        durasi = c3.number_input("Durasi slot (menit)", min_value=15, max_value=240, value=cfg["durasi"], step=15)
        jeda = c4.number_input("Jeda antar slot (menit)", min_value=0, max_value=60, value=cfg["jeda"], step=5)
        rentang = st.date_input("Tanggal (pilih satu tanggal atau rentang)", value=(date.today(), date.today()))
        kirim = st.form_submit_button("✨ Buat Slot", type="primary")
    if kirim:
        a, b = rentang_tanggal(rentang)
        if not a:
            flash("warning", "Pilih tanggal dulu.")
        else:
            ok, msg, n, skip = dbx.buat_slot_rentang(a, b, buka.strftime("%H:%M"), tutup.strftime("%H:%M"),
                                                      int(durasi), int(jeda))
            if ok:
                extra = f" ({skip} slot dilewati karena sudah ada/beririsan)" if skip else ""
                flash("success", f"{n} slot baru dibuat{extra}.")
            else:
                flash("error", msg)
        st.rerun()

    sect("Ketersediaan slot per tanggal")
    tgl = st.date_input("Pilih tanggal", value=date.today(), key="tgl_kelola").isoformat()
    slots = dbx.rows("SELECT * FROM jadwal_studio WHERE tanggal=? ORDER BY jam_mulai", (tgl,))
    booking_slot = {b["id_jadwal"]: b for b in dbx.list_booking("b.status_booking IN ('Menunggu','Dikonfirmasi','Selesai')")}
    data = []
    for s in slots:
        bk = booking_slot.get(s["id_jadwal"])
        dur = dbx.to_min(s["jam_selesai"]) - dbx.to_min(s["jam_mulai"])
        data.append([f"{fmt_jam(s['jam_mulai'])} - {fmt_jam(s['jam_selesai'])}", f"{dur} menit",
                     s["status_jadwal"], bk["nama_pelanggan"] if bk else "-"])
    tabel(["Jam", "Durasi", "Status", "Dipesan oleh"], data, badge_cols=(2,),
          kosong="Belum ada slot di tanggal ini. Buat lewat form di atas.")

    if slots:
        st.write("")
        b1, b2 = st.columns(2)
        if b1.button("🔒 Tutup tanggal ini (nonaktifkan semua slot kosong)", key="tutup_tgl"):
            n = dbx.set_tanggal(tgl, buka=False)
            flash("success", f"{n} slot dinonaktifkan.")
            st.rerun()
        if b2.button("🔓 Buka tanggal ini (aktifkan semua slot nonaktif)", key="buka_tgl"):
            n = dbx.set_tanggal(tgl, buka=True)
            flash("success", f"{n} slot diaktifkan.")
            st.rerun()

        with st.container(border=True):
            st.markdown("**Kelola satu slot**")
            pilih = st.selectbox("Slot", [s["id_jadwal"] for s in slots], key=f"slot_pilih_{tgl}",
                                 format_func=lambda i: next(
                                     f"{fmt_jam(s['jam_mulai'])} - {fmt_jam(s['jam_selesai'])} · {s['status_jadwal']}"
                                     for s in slots if s["id_jadwal"] == i))
            x1, x2 = st.columns(2)
            if x1.button("🔁 Aktif / Nonaktifkan", key="tg_slot"):
                ok, msg = dbx.toggle_slot(pilih)
                flash("success" if ok else "error", msg)
                st.rerun()
            if x2.button("🗑️ Hapus slot", key="del_slot"):
                ok, msg = dbx.hapus_slot(pilih)
                flash("success" if ok else "error", msg)
                st.rerun()

    with st.expander("➕ Tambah slot manual"):
        with st.form("form_manual", clear_on_submit=True):
            m1, m2 = st.columns(2)
            jm = m1.time_input("Jam mulai", value=time(9, 0), step=900)
            js = m2.time_input("Jam selesai", value=time(10, 0), step=900)
            if st.form_submit_button("Tambah Slot", type="primary"):
                ok, msg = dbx.tambah_slot_manual(tgl, jm.strftime("%H:%M"), js.strftime("%H:%M"))
                flash("success" if ok else "error", msg)
                st.rerun()


def tab_paket():
    pakets = dbx.rows("SELECT * FROM paket_foto ORDER BY durasi_sesi, nama_paket")
    sect("Daftar paket foto")
    tabel(["ID", "Nama Paket", "Durasi", "Harga"],
          [[p["id_paket"], p["nama_paket"], f"{p['durasi_sesi']} menit", rupiah(p["harga"])] for p in pakets],
          kosong="Belum ada paket foto.")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        sect("Tambah paket")
        with st.form("form_paket", clear_on_submit=True):
            nama = st.text_input("Nama paket", placeholder="contoh: Paket Wisuda")
            durasi = st.number_input("Durasi sesi (menit)", min_value=15, max_value=300, value=60, step=15)
            harga = st.number_input("Harga (Rp)", min_value=0, value=250000, step=10000)
            if st.form_submit_button("Simpan Paket", type="primary"):
                ok, msg = dbx.simpan_paket(nama, int(durasi), int(harga))
                flash("success" if ok else "error", msg)
                st.rerun()
    with c2:
        sect("Ubah / hapus paket")
        if pakets:
            ids = [p["id_paket"] for p in pakets]
            pid = st.selectbox("Pilih paket", ids, key=f"pk_pilih_{hash(tuple(ids))}",
                               format_func=lambda i: next(p["nama_paket"] for p in pakets if p["id_paket"] == i))
            p = next(p for p in pakets if p["id_paket"] == pid)
            with st.container(border=True):
                n2 = st.text_input("Nama", value=p["nama_paket"], key=f"pk_n_{pid}")
                d2 = st.number_input("Durasi (menit)", 15, 300, p["durasi_sesi"], 15, key=f"pk_d_{pid}")
                h2 = st.number_input("Harga (Rp)", 0, value=p["harga"], step=10000, key=f"pk_h_{pid}")
                e1, e2 = st.columns(2)
                if e1.button("💾 Simpan", key=f"pk_s_{pid}", type="primary"):
                    ok, msg = dbx.simpan_paket(n2, int(d2), int(h2), pid)
                    flash("success" if ok else "error", msg)
                    st.rerun()
                if e2.button("🗑️ Hapus", key=f"pk_x_{pid}"):
                    ok, msg = dbx.hapus_paket(pid)
                    flash("success" if ok else "error", msg)
                    st.rerun()


def page_kelola():
    judul("Kelola Studio", "Atur jam operasional, slot per tanggal, dan paket foto.")
    show_flash()
    t1, t2 = st.tabs(["⏰  Jam Operasional & Slot", "📦  Paket Foto"])
    with t1:
        tab_slot()
    with t2:
        tab_paket()


# ====================================================================== HALAMAN: DATA PELANGGAN
def page_pelanggan():
    judul("Data Pelanggan", "Data master pelanggan: tambah, ubah, atau hapus nama dan nomor telepon.")
    show_flash()

    cari = st.text_input("Cari pelanggan", placeholder="nama atau nomor telepon...", key="pl_cari")
    daftar = dbx.list_pelanggan(cari.strip())
    sect("Daftar pelanggan", f"{len(daftar)} pelanggan")
    tabel(["ID", "Nama", "Nomor Telepon", "Booking"],
          [[p["id_pelanggan"], p["nama_pelanggan"], p["no_telepon"], p["jml_booking"]] for p in daftar],
          kosong="Pelanggan tidak ditemukan." if cari.strip() else "Belum ada data pelanggan.")

    c1, c2 = st.columns(2, gap="large")
    with c1:
        sect("Tambah pelanggan")
        with st.form("form_pelanggan", clear_on_submit=True):
            nama = st.text_input("Nama pelanggan", placeholder="contoh: Rina Amelia")
            telepon = st.text_input("Nomor telepon", placeholder="contoh: 081234567890")
            if st.form_submit_button("Simpan Pelanggan", type="primary"):
                ok, msg = dbx.simpan_pelanggan(nama, telepon)
                flash("success" if ok else "error", msg)
                st.rerun()
    with c2:
        sect("Ubah / hapus pelanggan")
        if daftar:
            ids = [p["id_pelanggan"] for p in daftar]
            pid = st.selectbox("Pilih pelanggan", ids, key=f"pl_pilih_{hash(tuple(ids))}",
                               format_func=lambda i: next(
                                   f"{p['nama_pelanggan']} · {p['no_telepon']}"
                                   for p in daftar if p["id_pelanggan"] == i))
            p = next(p for p in daftar if p["id_pelanggan"] == pid)
            with st.container(border=True):
                n2 = st.text_input("Nama", value=p["nama_pelanggan"], key=f"pl_n_{pid}")
                tp = st.text_input("Nomor telepon", value=p["no_telepon"], key=f"pl_t_{pid}")
                e1, e2 = st.columns(2)
                if e1.button("💾 Simpan", key=f"pl_s_{pid}", type="primary"):
                    ok, msg = dbx.simpan_pelanggan(n2, tp, pid)
                    flash("success" if ok else "error", msg)
                    st.rerun()
                if e2.button("🗑️ Hapus", key=f"pl_x_{pid}"):
                    ok, msg = dbx.hapus_pelanggan(pid)
                    flash("success" if ok else "error", msg)
                    st.rerun()


# ====================================================================== HALAMAN: BOOKING
def cb_simpan(konfirmasi: bool):
    """Dipanggil sebagai callback tombol supaya form bisa di-reset setelah tersimpan."""
    ss = st.session_state
    telp = dbx.norm_phone(ss.get("bk_telp", ""))
    nama = ss.get(f"bk_nama_{telp}", "")
    id_paket = ss.get("bk_paket")
    slot_key = f"bk_slot_{ss['bk_tgl'].isoformat()}_{id_paket}"
    id_slot = ss.get(slot_key)
    if not id_slot:
        flash("error", "Pilih slot yang tersedia dulu.")
        return
    ok, msg, idb = dbx.simpan_booking(nama, telp, id_paket, id_slot, konfirmasi)
    flash("success" if ok else "error", msg, idb if (ok and konfirmasi) else None)
    if ok:
        ss["bk_telp"] = ""
        ss.pop(slot_key, None)


def tab_booking_baru():
    pakets = dbx.rows("SELECT * FROM paket_foto ORDER BY durasi_sesi, nama_paket")
    if not pakets:
        st.warning("Tambahkan paket foto dulu di menu Kelola Studio.")
        return
    pk = {p["id_paket"]: p for p in pakets}
    kiri, kanan = st.columns(2, gap="large")

    with kiri:
        sect("1 · Pilih jadwal")
        tgl = st.date_input("Tanggal booking", value=date.today(), key="bk_tgl").isoformat()
        id_paket = st.selectbox("Paket foto", list(pk), key="bk_paket",
                                format_func=lambda i: f"{pk[i]['nama_paket']} · {pk[i]['durasi_sesi']} mnt · {rupiah(pk[i]['harga'])}")
        slots = dbx.slot_tersedia(tgl, pk[id_paket]["durasi_sesi"])
        if slots:
            sm = {s["id_jadwal"]: s for s in slots}
            st.selectbox("Slot tersedia (sudah disaring sesuai durasi paket)", list(sm),
                         key=f"bk_slot_{tgl}_{id_paket}",
                         format_func=lambda i: f"{fmt_jam(sm[i]['jam_mulai'])} - {fmt_jam(sm[i]['jam_selesai'])}")
            st.caption(f"✅ {len(slots)} slot tersedia untuk {pk[id_paket]['nama_paket']} pada {tgl_id(tgl)}.")
        else:
            st.warning("Tidak ada slot tersedia untuk paket & tanggal ini.")
            nxt = dbx.tanggal_berikut_tersedia(tgl, pk[id_paket]["durasi_sesi"])
            if nxt:
                st.info(f"Tanggal terdekat yang masih punya slot: **{tgl_id(nxt)}**.")

    with kanan:
        sect("2 · Data pelanggan")
        telp = st.text_input("Nomor telepon", placeholder="08xxxxxxxxxx", key="bk_telp")
        tn = dbx.norm_phone(telp)
        ada = dbx.cari_pelanggan(tn)
        if ada:
            st.success(f"Pelanggan terdaftar: **{ada['nama_pelanggan']}** — data tidak akan digandakan.", icon="🔎")
        elif tn:
            st.info("Nomor baru — data pelanggan dibuat otomatis saat booking disimpan.", icon="🆕")
        st.text_input("Nama pelanggan", value=ada["nama_pelanggan"] if ada else "", key=f"bk_nama_{tn}",
                      placeholder="Nama lengkap")

        sect("3 · Simpan")
        b1, b2 = st.columns(2)
        b1.button("💾 Simpan Booking", on_click=cb_simpan, args=(False,), key="btn_simpan",
                  disabled=not slots, help="Status Menunggu, belum ada nota.")
        b2.button("✅ Simpan & Konfirmasi", on_click=cb_simpan, args=(True,), type="primary",
                  key="btn_konfirm", disabled=not slots, help="Langsung Dikonfirmasi dan nota antrean terbit.")
        st.caption("Simpan Booking → status **Menunggu** (tanpa nota). Simpan & Konfirmasi → **Dikonfirmasi** + nota antrean.")


def tab_riwayat():
    semua = dbx.list_booking()
    f1, f2, f3 = st.columns([2, 2, 2], gap="medium")
    status_f = f1.multiselect("Filter status", dbx.STATUS_BOOKING, placeholder="Semua status")
    cari = f2.text_input("Cari nama / telepon", placeholder="mis. Rina atau 0812…")
    pakai_tgl = f3.checkbox("Filter rentang tanggal")
    rentang = None
    if pakai_tgl:
        rentang = f3.date_input("Rentang", value=(date.today(), date.today()), key="rw_rentang")
    data = semua
    if status_f:
        data = [b for b in data if b["status_booking"] in status_f]
    if cari.strip():
        k = cari.strip().lower()
        data = [b for b in data if k in b["nama_pelanggan"].lower() or k in b["no_telepon"]]
    if rentang:
        a, z = rentang_tanggal(rentang)
        if a:
            data = [b for b in data if a.isoformat() <= b["tanggal"] <= z.isoformat()]

    st.caption(f"Menampilkan {len(data)} dari {len(semua)} booking.")
    tabel(["ID", "Tanggal", "Jam", "Pelanggan", "Paket", "Status", "No. Antrean"],
          [[b["id_booking"], tgl_id(b["tanggal"]), f"{fmt_jam(b['jam_mulai'])}-{fmt_jam(b['jam_selesai'])}",
            b["nama_pelanggan"], b["nama_paket"], b["status_booking"],
            f"{b['nomor_antrean']:03d}" if b["nomor_antrean"] else "-"] for b in data],
          badge_cols=(5,), kosong="Tidak ada booking yang cocok dengan filter.")

    if not data:
        return
    sect("Kelola booking terpilih")
    ids = [b["id_booking"] for b in data]
    bm = {b["id_booking"]: b for b in data}
    pid = st.selectbox("Pilih booking", ids, key=f"rw_pilih_{hash(tuple(ids))}", format_func=lambda i: label_booking(bm[i]))
    b = bm[pid]
    with st.container(border=True):
        s1, s2 = st.columns([2, 1], vertical_alignment="bottom")
        pilihan = [s for s in dbx.STATUS_BOOKING if s != b["status_booking"]]
        baru = s1.selectbox(f"Ubah status (saat ini: {b['status_booking']})", pilihan, key=f"st_{pid}_{b['status_booking']}")
        if s2.button("Terapkan", key=f"ap_{pid}", type="primary"):
            ok, msg = dbx.ubah_status(pid, baru)
            flash("success" if ok else "error", msg)
            st.rerun()
        st.caption("Aturan: Menunggu → Dikonfirmasi → Selesai. Menunggu tidak boleh langsung Selesai. "
                   "Dibatalkan melepas slot.")

        if b["nomor_antrean"]:
            st.download_button("⬇️ Unduh Nota (.txt)", dbx.nota_txt(b).encode("utf-8"),
                               file_name=f"nota_antrean_{b['tanggal']}_{int(b['nomor_antrean']):03d}.txt",
                               mime="text/plain", key=f"rw_dl_{pid}")

    if b["status_booking"] in dbx.STATUS_AKTIF:
        with st.expander("✏️ Edit data booking"):
            pk = {p["id_paket"]: p for p in dbx.rows("SELECT * FROM paket_foto ORDER BY durasi_sesi")}
            en = st.text_input("Nama pelanggan", value=b["nama_pelanggan"], key=f"en_{pid}")
            et = st.text_input("Nomor telepon", value=b["no_telepon"], key=f"et_{pid}")
            ep = st.selectbox("Paket", list(pk), index=list(pk).index(b["id_paket"]), key=f"ep_{pid}",
                              format_func=lambda i: f"{pk[i]['nama_paket']} · {pk[i]['durasi_sesi']} mnt")
            if st.button("💾 Simpan perubahan", key=f"es_{pid}", type="primary"):
                ok, msg = dbx.edit_booking(pid, en, et, ep)
                flash("success" if ok else "error", msg)
                st.rerun()
    with st.expander("🗑️ Hapus booking"):
        yakin = st.checkbox("Saya yakin ingin menghapus booking ini (nota ikut terhapus, slot dilepas).", key=f"hy_{pid}")
        if st.button("Hapus Booking", key=f"hx_{pid}", disabled=not yakin):
            ok, msg = dbx.hapus_booking(pid)
            flash("success" if ok else "error", msg)
            st.rerun()


def page_booking():
    judul("Booking", "Catat pemesanan pelanggan, validasi jadwal, dan pantau status.")
    show_flash()
    t1, t2 = st.tabs(["➕  Booking Baru", "📋  Riwayat & Status"])
    with t1:
        tab_booking_baru()
    with t2:
        tab_riwayat()


# ====================================================================== HALAMAN: NOTA
def page_nota():
    judul("Nota Antrean", "Nota terbit setelah booking dikonfirmasi. Nomor antrean mulai dari 1 setiap tanggal booking.")
    show_flash()
    tgl = st.date_input("Tanggal booking", value=date.today(), key="nt_tgl").isoformat()
    notas = [b for b in dbx.list_booking("n.tanggal_antrean=?", (tgl,))]
    notas.sort(key=lambda b: b["nomor_antrean"])
    tabel(["No.", "Jam", "Pelanggan", "Paket", "Status"],
          [[f"{b['nomor_antrean']:03d}", f"{fmt_jam(b['jam_mulai'])}-{fmt_jam(b['jam_selesai'])}",
            b["nama_pelanggan"], b["nama_paket"], b["status_booking"]] for b in notas],
          badge_cols=(4,), kosong=f"Belum ada nota antrean pada {tgl_id(tgl)}.")
    if notas:
        sect("Pratinjau & unduh")
        bm = {b["id_booking"]: b for b in notas}
        pid = st.selectbox("Pilih nota", list(bm), key=f"nt_pilih_{tgl}_{len(bm)}",
                           format_func=lambda i: f"{bm[i]['nomor_antrean']:03d} · {bm[i]['nama_pelanggan']} · "
                                                 f"{fmt_jam(bm[i]['jam_mulai'])}")
        tampil_nota(bm[pid], key=f"nt_{pid}")


# ====================================================================== ROUTER
{MENU[0]: page_beranda, MENU[1]: page_kelola, MENU[2]: page_pelanggan,
 MENU[3]: page_booking, MENU[4]: page_nota}[st.session_state["menu"]]()
