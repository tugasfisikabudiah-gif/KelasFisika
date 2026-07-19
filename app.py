import streamlit as st
from supabase import create_client, Client
import datetime
import uuid
import pandas as pd
from streamlit_calendar import calendar
import random

# Daftar kutipan motivasi Fisika (Bisa Bapak tambah sendiri nanti)
kutipan_fisika = [
    "🚀 'Imajinasi lebih penting daripada pengetahuan.' – Albert Einstein",
    "🍎 'Apa yang kita ketahui hanyalah setetes air, apa yang tidak kita ketahui adalah lautan.' – Isaac Newton",
    "⚡ 'Fisika itu asyik! Jangan lupa senyum saat praktikum ya.'",
    "🌌 'Alam semesta tidak hanya aneh, tapi lebih aneh dari yang kita bayangkan.'",
    "📡 'Tetap semangat! Fisika adalah kunci memahami cara kerja dunia.'",
    "🔬 'Kesalahan dalam percobaan adalah awal dari penemuan besar.'"
]

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Portal KBM FISIKA KELAS XII A-F", page_icon="✨", layout="wide")

# --- 2. KONEKSI SUPABASE ---
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# --- 3. CUSTOM CSS (MERAH PUTIH & KONTRAS) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF !important; }
    h1, h2, h3, p, label, .stMarkdown, .stSelectbox p, [data-baseweb="tab"] p { color: #1A365D !important; }
    h1 { text-align: center !important; }

    /* TOMBOL MERAH PUTIH */
    button, a[data-testid="stLinkButton"], .stButton > button, div[data-testid="stLinkButton"] > a {
        background-color: #E53E3E !important;
        border: none !important; border-radius: 12px !important;
        height: 3.5em !important; width: 100% !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        text-decoration: none !important; opacity: 1 !important;
    }
    button *, a[data-testid="stLinkButton"] *, .stButton > button *, div[data-testid="stLinkButton"] a * {
        color: #FFFFFF !important; font-weight: bold !important; font-size: 18px !important;
    }

    /* TAB MERAH */
    [data-baseweb="tab"] { background-color: #E53E3E !important; border-radius: 12px 12px 0px 0px !important; margin-right: 5px !important; }
    [data-baseweb="tab"] * { color: #FFFFFF !important; font-weight: bold !important; }

    /* KARTU MENU */
    .option-card { 
        background-color: #FFFFFF !important; border: 4px solid #1A365D !important; 
        border-radius: 25px !important; padding: 40px !important; text-align: center !important;
        margin-bottom: 15px;
    }
    
    .stTextInput>div>div, .stSelectbox>div>div, .stTextArea>div>div { border: 2px solid #1A365D !important; border-radius: 10px !important; }

    /* PESAN GURU */
    .pesan-guru {
        background-color: #fff5f5; padding: 20px; border-radius: 15px;
        border-left: 10px solid #E53E3E; margin-bottom: 25px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    }

    /* PERBAIKAN TEKS UPLOAD */
    [data-testid="stFileUploaderFileName"] { color: #000000 !important; font-weight: bold !important; }
    .st-emotion-cache-1erivf3, .st-emotion-cache-1kyx9m7 p, .st-emotion-cache-nu742z p { color: #000000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNGSI UPLOAD ---
def upload_to_storage(file, bucket_name, folder):
    today_str = datetime.date.today().strftime("%Y%m%d")
    ext = file.name.split('.')[-1]
    filename = f"{folder}/{today_str}_{uuid.uuid4().hex[:5]}.{ext}"
    try:
        supabase.storage.from_(bucket_name).upload(filename, file.read())
        return supabase.storage.from_(bucket_name).get_public_url(filename)
    except Exception as e:
        st.error(f"Gagal upload: {e}"); return None

# --- JUDUL UTAMA ---
st.markdown("<h1>✨ Portal KBM FISIKA KELAS XII ✨</h1>", unsafe_allow_html=True)

# ========================================================
# --- 5. LOGIKA NAVIGASI (GERBANG UTAMA) ---
# ========================================================

if 'menu_pilihan' not in st.session_state:
# --- PESAN TERSEMAT DARI GURU (REVISI INSTRUKSI) ---
    # --- PILIH KUTIPAN ACAK ---
    quote_hari_ini = random.choice(kutipan_fisika)
# --- PESAN TERSEMAT DARI GURU (VERSI KOMPAK) ---
    st.markdown(f"""
        <div class="pesan-guru" style="padding: 15px 25px; margin-bottom: 15px;">
            <h4 style="margin:0; color:#E53E3E; font-size: 24px; display: flex; align-items: center;">
                📢 <span style="margin-left: 10px;">Instruksi Bu Diah Hari Ini:</span>
            </h4>
            <div style="margin-top: 5px; color:#1A365D; font-size:18px; line-height: 1.4;">
                <ol style="margin-bottom: 8px; padding-left: 20px;">
                    <li style="margin-bottom: 4px;"><b>Ketua Kelas / PJ Kelas</b> WAJIB mengisi presensi & unggah foto bukti KBM.</li>
                    <li><b>Tiap Kelompok</b> WAJIB unduh, cetak, kerjakan LKPD & kirim laporan progress.</li>
                </ol>
                <hr style="border: 0.5px solid #E53E3E; opacity: 0.2; margin: 8px 0;">
                <p style="font-style: italic; font-size: 17px; color: #4A5568; text-align: center; margin: 0;">
                    "{quote_hari_ini}"
                </p>
            </div>
        </div>
        <!-- 🌟 TOMBOL SEKARANG BERADA DI SINI ( FIX CENTERED) 🌟 -->
        <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 25px; width: 100%;">
            <a href="https://drive.google.com/drive/folders/1-Vjpis7D2IrWm-sOr_Pxk6aebfp8a5lg?usp=share_link" target="_blank" style="text-decoration: none; width: 100%; max-width: 500px; text-align: center;">
                <button style="background-color: #1A365D; color: white; border: none; padding: 12px 20px; font-size: 15px; border-radius: 8px; cursor: pointer; font-weight: bold; width: 100%; transition: 0.3s; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
                    📁 Buka Seluruh Perangkat Pembelajaran Fisika XII
                </button>
            </a>
        </div>
    """, unsafe_allow_html=True)

    

    # --- PILIHAN MENU ---
    # Cari baris ini di kode Bapak:
    st.markdown("<h4 style='text-align: center; margin-top: 20px; font-size: 24px;'>Selamat datang! Silakan pilih menu di bawah ini:</h4>", unsafe_allow_html=True)
    #st.markdown("<p style='text-align: center; margin-top:24px;'>Selamat datang! Silakan pilih menu PORTAL SISWA di bawah ini:</p>", unsafe_allow_html=True)
    col_sis, col_gur = st.columns(2)
    
    with col_sis:
        st.markdown('<div class="option-card"><h1 style="font-size: 50px; margin:0;">👨‍🎓</h1><h3>PORTAL SISWA</h3><p>Materi, Presensi & Progress Kelompok</p></div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1, 3, 1])
        with c2:
            if st.button("MASUK SEBAGAI SISWA", key="btn_siswa", use_container_width=True):
                st.session_state.menu_pilihan = 'siswa'; st.rerun()
                
    with col_gur:
        st.markdown('<div class="option-card"><h1 style="font-size: 50px; margin:0;">👩‍🏫</h1><h3>PORTAL GURU</h3><p>Rekap & Monitoring</p></div>', unsafe_allow_html=True)
        g1, g2, g3 = st.columns([1, 3, 1])
        with g2:
            if st.button("MASUK SEBAGAI GURU", key="btn_guru", use_container_width=True):
                st.session_state.menu_pilihan = 'guru'; st.rerun()

    st.write("---")
    
    # --- DASHBOARD REKAPITULASI ---
    st.markdown("<h2 style='text-align: center; color: #1A365D;'>🏆 Dashboard Monitoring KBM FISIKA XII</h2>", unsafe_allow_html=True)
    try:
        res_hadir = supabase.table("laporan_kehadiran").select("id, jml_hadir, jml_sakit, jml_izin, jml_alpha, jadwal_id").execute()
        res_jadwal = supabase.table("jadwal_kbm").select("id, nama_kelas").execute()
        res_progres = supabase.table("progres_kelompok").select("laporan_id, persentase").execute()
        
        if res_hadir.data and res_jadwal.data:
            df_jadwal = pd.DataFrame(res_jadwal.data)
            df_hadir = pd.DataFrame(res_hadir.data)
            df_merge = pd.merge(df_hadir, df_jadwal, left_on="jadwal_id", right_on="id")
            df_progres = pd.DataFrame(res_progres.data) if res_progres.data else pd.DataFrame(columns=["laporan_id", "persentase"])

            c1, c2 = st.columns(2)
            with c1: st.bar_chart(df_merge.groupby("nama_kelas")["jml_hadir"].sum(), color="#E53E3E")
            with c2: st.bar_chart(df_merge.groupby("nama_kelas")[["jml_sakit", "jml_izin", "jml_alpha"]].sum(), color=["#ECC94B", "#4299E1", "#1A365D"])

            st.write(" ")
            unique_kelas = sorted(df_jadwal['nama_kelas'].unique())
            cols = st.columns(len(unique_kelas))
            for i, kelas in enumerate(unique_kelas):
                with cols[i]:
                    dk = df_merge[df_merge['nama_kelas'] == kelas]
                    h, s, z, a = dk['jml_hadir'].sum(), dk['jml_sakit'].sum(), dk['jml_izin'].sum(), dk['jml_alpha'].sum()
                    ids = dk['id_x'].tolist() if 'id_x' in dk.columns else dk['id'].tolist()
                    
                    # LOGIKA AGAR TIDAK NAN
                    raw_p = df_progres[df_progres['laporan_id'].isin(ids)]['persentase'].mean() if not df_progres.empty else 0
                    avg_p = 0 if pd.isna(raw_p) else raw_p

                    st.markdown(f"""<div style="background-color: #FFFFFF; border: 2px solid #1A365D; border-radius: 12px; padding: 10px; text-align: center; min-height: 150px;">
                        <h4 style="margin: 0; color: #E53E3E; font-size: 14px;">{kelas}</h4>
                        <p style="margin: 5px 0; font-size: 12px; font-weight: bold; background: #EDF2F7; border-radius: 5px;">📊 Progres: {avg_p:.0f}%</p>
                        <p style="margin: 0; font-size: 10px; text-align: left;">✅H:{h} 🤒S:{s} ✉️I:{z} 🚫A:{a}</p>
                    </div>""", unsafe_allow_html=True)
    except Exception as e: st.error(f"Error Dashboard: {e}")

else:
    if st.button("⬅️ Kembali ke Menu Utama"):
        del st.session_state.menu_pilihan; st.rerun()

    # --- PORTAL SISWA ---
    if st.session_state.menu_pilihan == 'siswa':
        st.markdown("## 📖 PORTAL BELAJAR SISWA")

        st.markdown("""
            <div style="background-color: #EDF2F7; padding: 20px; border-radius: 15px; border-left: 5px solid #1A365D; margin-bottom: 20px;">
                <p style="margin: 0; font-size: 24px; color: #1A365D;">
                    Selamat datang di ruang belajar digital! Silakan gunakan portal ini dengan panduan berikut:
                </p>
                <ul style="margin-top: 10px; font-size: 20px; color: #1A365D;">
                    <li><b>📚 Materi & Presensi:</b> (WAJIB) Pilih kelas dan tanggal untuk mengakses materi, melakukan presensi (Ketua Kelas), dan mengirim laporan progres (Kelompok).</li>
                    <li><b>📅 Kalender Akademik:</b> Kamu dapat melihat jadwal rencana pembelajaran Fisika selama satu semester untuk persiapan belajar kamu.</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)


        tab_utama, tab_kalender = st.tabs(["📚 Materi & Presensi", "📅 Kalender Akademik"])

        with tab_utama:

            # --- TABEL JADWAL MINGGUAN (SISIPKAN DI SINI) ---
            st.markdown("""
                <div style="background-color: #FFFFFF; border: 2px solid #1A365D; border-radius: 15px; padding: 15px; margin-bottom: 25px;">
                    <h4 style="margin: 0 0 10px 0; color: #E53E3E; text-align: center; font-size: 20px;">📅 Jadwal KBM Fisika Minggu Ini</h4>
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px; color: #1A365D;">
                        <thead>
                            <tr style="background-color: #1A365D; color: white; text-align: center;">
                                <th style="padding: 8px; border: 1px solid #cbd5e0;">Senin</th>
                                <th style="padding: 8px; border: 1px solid #cbd5e0;">Selasa</th>
                                <th style="padding: 8px; border: 1px solid #cbd5e0;">Rabu</th>
                                <th style="padding: 8px; border: 1px solid #cbd5e0;">Kamis</th>
                                <th style="padding: 8px; border: 1px solid #cbd5e0;">Jumat</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr style="text-align: center;">
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #FEFCBF;"><b>XII A</b><br>(12:50 - 14:10)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #C6F6D5;"><b>XII B</b><br>(14:10 - 15:30)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #EBF8FF;"><b>XII D</b><br>(07:00 - 08:20)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #FEW0BC; background-color: #FED7D7;"><b>XII E</b><br>(07:00 - 08:20)</td>
                            </tr>
                            <tr style="text-align: center; background-color: #F7FAFC;">
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #FEEBC8;"><b>XII C</b><br>(14:10 - 15:30)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #FED7D7;"><b>XII E</b><br>(08:20 - 09:40)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #EDW4FF; background-color: #E9D8FD;"><b>XII F</b><br>(08:20 - 09:40)</td>
                            </tr>
                            <tr style="text-align: center; background-color: #F7FAFC;">
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #FEFCBF;"><b>XII A</b><br>(09:55 - 11:15)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #FEEBC8;"><b>XII C</b><br>(09:55 - 11:15)</td>
                            </tr>
                            <tr style="text-align: center; background-color: #F7FAFC;">
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #E9D8FD;"><b>XII F</b><br>(11:15 - 13:30)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #EBF8FF;"><b>XII D</b><br>(13:25 - 14:45)</td>
                            </tr>
                            <tr style="text-align: center; background-color: #F7FAFC;">
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; background-color: #C6F6D5;"><b>XII B</b><br>(13:30 - 14:50)</td>
                                <td style="padding: 8px; border: 1px solid #cbd5e0; color: #a0aec0;">-</td>
                            </tr>
                        </tbody>
                    </table>
                    <p style="margin: 8px 0 0 0; font-size: 12px; font-style: italic; color: #718096; text-align: center;">
                        *Jadwal di atas adalah waktu utama pengerjaan LKPD & Presensi.
                    </p>
                </div>
            """, unsafe_allow_html=True)

            col_kls, col_tgl = st.columns(2)
            with col_kls: 
                kls_siswa = st.selectbox("Pilih Kelas Kamu:", ["-- Pilih Kelas --", "XII A", "XII B", "XII C", "XII D", "XII E", "XII F"])
            with col_tgl: 
                tgl_pilihan = st.date_input("Pilih Tanggal Materi:", datetime.date.today())

            if kls_siswa != "-- Pilih Kelas --":
                tgl_str = tgl_pilihan.isoformat()
                res = supabase.table("jadwal_kbm").select("*, materi(*)").eq("nama_kelas", kls_siswa).eq("tanggal", tgl_str).execute()
                
                if res.data and res.data[0].get('materi'):
                    data_kbm = res.data[0]
                    materi = data_kbm['materi']
                    
                    tab_materi, tab_presensi, tab_progres = st.tabs(["📄 Konten Materi", "🙋 Presensi Kelas", "👥 Progres Kelompok"])
                    
                    with tab_materi:
                        st.markdown(f"### {materi['judul']}")
                        st.write(materi['deskripsi'])
                        if materi.get('url_pdf'):
                            st.write("---")
                            st.markdown("**📂 Modul Pembelajaran / LKPD. Tiap kelompok WAJIB UNDUH & CETAK LKPD ini melalui tombol di bawah:**")
                            emb = materi['url_pdf'].replace("/view", "/preview") if "drive.google.com" in materi['url_pdf'] else materi['url_pdf']
                            st.markdown(f'<iframe src="{emb}" width="100%" height="700" style="border: 2px solid #1A365D; border-radius: 10px;"></iframe>', unsafe_allow_html=True)
                            st.link_button("📂 Unduh LKPD", materi['url_pdf'])
                        if materi.get('url_video'):
                            st.write("---")
                            tv = materi.get('teks_video', "Video di bawah ini adalah video yang harus kamu simak, Instruksi rinci sudah ada di LKPD ya:")
                            st.markdown(f'<div style="background-color:#fff5f5;padding:15px;border-radius:10px;border-left:5px solid #FF6B6B;"><b>📺 Tonton & Pahami</b><br>{tv}</div>', unsafe_allow_html=True)
                            for v in materi['url_video'].split(','): st.video(v.strip())
                        if materi.get('url_simulasi'):
                            st.write("---")
                            ts = materi.get('teks_simulasi', "Gunakan simulasi interaktif di bawah ini untuk mengisi LKPD:")
                            st.markdown(f"<b>🧪 {ts}</b>", unsafe_allow_html=True)
                            st.markdown(f'<iframe src="{materi["url_simulasi"]}" width="100%" height="500" style="border: 2px solid #1A365D; border-radius: 10px;"></iframe>', unsafe_allow_html=True)
                    
                    with tab_presensi:
                        if tgl_pilihan == datetime.date.today():
                            res_s = supabase.table("siswa").select("nama").eq("nama_kelas", kls_siswa).order("nama").execute()
                            if res_s.data:
                                with st.form("form_presensi_siswa"):
                                    n_pel = st.text_input("Nama Pelapor (Ketua Kelas)")
                                    stats = {}
                                    for s in res_s.data:
                                        c1, c2 = st.columns([2, 3])
                                        c1.write(s['nama'])
                                        stats[s['nama']] = c2.radio(f"Status_{s['nama']}", ["Hadir", "Sakit", "Izin", "Alpha"], horizontal=True, label_visibility="collapsed", key=f"p_{s['nama']}")
                                    foto = st.file_uploader("📸 Foto Bukti Live KBM", type=['jpg', 'png'])
                                    if st.form_submit_button("Kirim Presensi Utama"):
                                        if n_pel and foto:
                                            url_f = upload_to_storage(foto, "presensi", kls_siswa)
                                            if url_f:
                                                vals = list(stats.values())
                                                detail_absen = [f"{n} ({s})" for n, s in stats.items() if s != "Hadir"]
                                                ket_otomatis = ", ".join(detail_absen) if detail_absen else "Semua Hadir"
                                                supabase.table("laporan_kehadiran").insert({
                                                    "jadwal_id": data_kbm['id'], "nama_pelapor": n_pel,
                                                    "jml_hadir": vals.count("Hadir"), "jml_sakit": vals.count("Sakit"),
                                                    "jml_izin": vals.count("Izin"), "jml_alpha": vals.count("Alpha"), 
                                                    "foto_kbm_url": url_f, "keterangan_absen": ket_otomatis
                                                }).execute()
                                                st.success("Presensi Berhasil!"); st.balloons()
                        else:
                            st.write("---")
                            st.warning("⚠️ **Akses Terkunci:** Presensi kelas hanya dapat dilakukan pada hari H jadwal KBM.")
                            st.info("Jika ada kendala terkait presensi susulan, silakan hubungi guru pengampu.")

                    with tab_progres:
                        if tgl_pilihan == datetime.date.today():
                            with st.form("form_progres_siswa"):
                                ca, cp = st.columns(2)
                                nk = ca.selectbox("Nomor Kelompok", [1,2,3,4,5,6])
                                ps = cp.slider("Persentase Capaian (%)", 0, 100, 50)
                                cat = st.text_area("Laporan Kerja Kelompok (Sebutkan kendala jika ada)")
                                
                                st.write("---")
                                # INPUT FOTO 1: ANGGOTA
                                f_anggota = st.file_uploader("📸 1. Foto Anggota Kelompok (Saat mengerjakan LKPD)", type=['jpg', 'png'], help="Pastikan semua anggota yang hadir terlihat di foto")
                                
                                # INPUT FOTO 2: LKPD
                                f_lkpd = st.file_uploader("📸 2. Foto Halaman Terakhir LKPD (Hasil pengerjaan hari ini)", type=['jpg', 'png'], help="Pastikan tulisan terbaca dengan jelas")
                                
                                if st.form_submit_button("Simpan Progres"):
                                    check = supabase.table("laporan_kehadiran").select("id").eq("jadwal_id", data_kbm['id']).execute()
                                    
                                    if check.data and f_anggota and f_lkpd:
                                        # Upload kedua foto
                                        url_anggota = upload_to_storage(f_anggota, "progres", f"K{nk}_{kls_siswa}_ANGGOTA")
                                        url_lkpd = upload_to_storage(f_lkpd, "progres", f"K{nk}_{kls_siswa}_LKPD")
                                        
                                        if url_anggota and url_lkpd:
                                            supabase.table("progres_kelompok").insert({
                                                "laporan_id": check.data[0]['id'], 
                                                "nomor_kelompok": nk, 
                                                "capaian_lkpd": cat, 
                                                "persentase": ps, 
                                                "foto_progres_url": url_lkpd,       # URL LKPD (untuk dashboard)
                                                "foto_anggota_url": url_anggota     # Pastikan kolom ini sudah ada di database Supabase Bapak
                                            }).execute()
                                            st.success(f"Laporan Kelompok {nk} Berhasil Terkirim!"); st.snow()
                                    else:
                                        st.error("Wajib mengunggah KEDUA FOTO (Anggota & LKPD)")
                        else:
                            st.write("---")
                            st.warning("⚠️ **Akses Terkunci:** Pengiriman laporan progres kelompok hanya dibuka pada hari H jadwal KBM.")
                            st.info("Pastikan kelompok kamu mengerjakan tugas sesuai waktu yang telah ditentukan.")
                else:
                    st.write("---")
                    st.warning(f"⚠️ Tidak ada jadwal KBM Fisika untuk kelas **{kls_siswa}** pada tanggal **{tgl_pilihan.strftime('%d %B %Y')}**.")
                    st.info("Silakan cek kembali tanggal yang dipilih atau hubungi Guru jika ada kekeliruan.")

        with tab_kalender: # --- TAB KALENDER (KONTRAS TINGGI) ---
            st.markdown("### 🗓️ Jadwal Interaktif Fisika XII")
            
            calendar_events = [
                {"title": "MPLS / Orientasi", "start": "2026-07-13", "end": "2026-07-19", "color": "#718096"},
                {"title": "Bab 1: Listrik Statis", "start": "2026-07-20", "end": "2026-07-26", "color": "#E53E3E"},
                {"title": "Bab 1: Listrik Dinamis", "start": "2026-07-27", "end": "2026-08-02", "color": "#E53E3E"},
                {"title": "Bab 1: Proyek Audit Energi", "start": "2026-08-03", "end": "2026-08-09", "color": "#E53E3E"},
                {"title": "Asesmen Sumatif 1", "start": "2026-08-10", "end": "2026-08-16", "color": "#1A365D"},
                {"title": "HUT RI (Libur)", "start": "2026-08-17", "end": "2026-08-18", "color": "#718096"},
                {"title": "Bab 2: Medan Magnet", "start": "2026-08-24", "end": "2026-08-30", "color": "#E53E3E"},
                {"title": "Bab 2: GGL Induksi", "start": "2026-08-31", "end": "2026-09-06", "color": "#E53E3E"},
                {"title": "Bab 2: Arus AC & GEM", "start": "2026-09-07", "end": "2026-09-13", "color": "#E53E3E"},
                {"title": "STS (Tengah Semester)", "start": "2026-09-14", "end": "2026-09-20", "color": "#D69E2E"},
                {"title": "Asesmen Sumatif 2", "start": "2026-09-21", "end": "2026-09-27", "color": "#1A365D"},
                {"title": "Pendalaman Ganjil", "start": "2026-10-01", "end": "2026-11-15", "color": "#E53E3E"},
                {"title": "SAS (Ujian Akhir)", "start": "2026-11-23", "end": "2026-12-06", "color": "#1A365D"},
                {"title": "Bab 3: Dualisme Gel.", "start": "2027-01-04", "end": "2027-01-10", "color": "#E53E3E"},
                {"title": "Bab 3: Relativitas", "start": "2027-01-11", "end": "2027-01-17", "color": "#E53E3E"},
                {"title": "Bab 3: Inti & Radioaktif", "start": "2027-01-18", "end": "2027-01-24", "color": "#E53E3E"},
                {"title": "Bab 4: Gerbang Logika", "start": "2027-02-01", "end": "2027-02-07", "color": "#E53E3E"},
                {"title": "Bab 4: Aljabar Boolean", "start": "2027-02-08", "end": "2027-02-14", "color": "#E53E3E"},
                {"title": "Asesmen Madrasah (AM)", "start": "2027-03-01", "end": "2027-03-14", "color": "#1A365D"},
            ]

            calendar(events=calendar_events, options={"height": 600, "initialView": "dayGridMonth", "headerToolbar": {"left": "prev,next today", "center": "title", "right": "dayGridMonth,dayGridWeek"}}, custom_css="""
                .fc-toolbar-title { color: #FFFFFF !important; font-size: 22px !important; font-weight: bold; }
                .fc-col-header-cell-cushion { color: #FFFFFF !important; }
                .fc-button-primary { background-color: #E53E3E !important; border: none !important; }
            """, key='calendar_siswa_vfinal')

# --- PORTAL GURU (VERSI FINAL DENGAN ISI LAPORAN DI TABEL) ---
    elif st.session_state.menu_pilihan == 'guru':
        st.markdown("## 🔐 Portal Guru")
        kode = st.text_input("Masukkan Kode Rahasia:", type="password")
        
        if kode == "CERIA2024":
            import pandas as pd
            from io import BytesIO
            
            t1, t2 = st.columns(2)
            t_awal = t1.date_input("Mulai:", datetime.date.today() - datetime.timedelta(days=7))
            t_akhir = t2.date_input("Sampai:", datetime.date.today())
            
            # Mengambil data dari Supabase
            res_data = supabase.table("laporan_kehadiran").select("*, jadwal_kbm(nama_kelas), progres_kelompok(*)").gte("tanggal", t_awal.isoformat()).lte("tanggal", t_akhir.isoformat()).execute()

            if res_data.data:
                # --- 1. BAGIAN REKAP TABEL UTAMA & EXCEL ---
                rekap_list = []
                for r in res_data.data:
                    klp_info = {f"Klp_{i}": "-" for i in range(1, 7)}
                    if r.get('progres_kelompok'):
                        for p in r['progres_kelompok']:
                            klp_info[f"Klp_{p['nomor_kelompok']}"] = f"{p['persentase']}% - {p['capaian_lkpd']}"
                    
                    row = {
                        "Tanggal": r['tanggal'], 
                        "Kelas": r['jadwal_kbm']['nama_kelas'], 
                        "Absen": r.get('keterangan_absen', "-"), 
                        "Pelapor": r['nama_pelapor']
                    }
                    row.update(klp_info)
                    rekap_list.append(row)
                
                df_guru = pd.DataFrame(rekap_list)
                st.dataframe(df_guru, use_container_width=True, hide_index=True)
                
                buf = BytesIO()
                with pd.ExcelWriter(buf) as writer: 
                    df_guru.to_excel(writer, index=False)
                st.download_button("📥 Unduh Excel Rekap Komplit", buf.getvalue(), f"Rekap_Fisika_{t_awal}.xlsx")

                st.divider()

                # --- 2. MONITORING VISUAL HARI INI ---
                st.subheader("🔍 Monitoring Visual Hari Ini")
                today_str = datetime.date.today().strftime('%Y-%m-%d')
                data_hari_ini = [r for r in res_data.data if str(r['tanggal']) == today_str]

                if data_hari_ini:
                    for lap in data_hari_ini:
                        with st.expander(f"📊 LAPORAN: {lap['jadwal_kbm']['nama_kelas']}", expanded=True):
                            # Pembagian Kolom: Kiri (Data & Tabel), Kanan (Foto-foto)
                            c1, c2 = st.columns([4, 3])
                            
                            with c1:
                                st.info(f"**👤 Pelapor:** {lap['nama_pelapor']}")
                                st.error(f"**📝 Rincian Absen:**\n{lap.get('keterangan_absen', 'Semua Hadir')}")
                                
                                st.write("**📋 Ringkasan Laporan Kelompok:**")
                                # Membuat data tabel dinamis dengan isi laporan
                                data_tabel = []
                                for i in range(1, 7):
                                    progres = next((p for p in lap['progres_kelompok'] if p['nomor_kelompok'] == i), None)
                                    if progres:
                                        data_tabel.append({
                                            "Klp": i,
                                            "Status": "✅",
                                            "Progress": f"{progres['persentase']}%",
                                            "Isi Laporan/Catatan": progres.get('capaian_lkpd', '-')
                                        })
                                    else:
                                        data_tabel.append({
                                            "Klp": i, "Status": "❌", "Progress": "0%", "Isi Laporan/Catatan": "Belum Lapor"
                                        })
                                
                                df_st = pd.DataFrame(data_tabel)
                                st.table(df_st)

                            with c2:
                                # Foto Bukti KBM dari Ketua Kelas
                                if lap.get('foto_kbm_url'):
                                    st.image(lap['foto_kbm_url'], caption=f"Bukti KBM {lap['jadwal_kbm']['nama_kelas']}", use_container_width=True)
                                
                                # Foto Dokumentasi (Anggota & LKPD)
                                if lap.get('progres_kelompok'):
                                    st.write("---")
                                    st.write("**📸 Dokumentasi Kelompok:**")
                                    for p in lap['progres_kelompok']:
                                        st.markdown(f"**Kelompok {p['nomor_kelompok']}** ({p['persentase']}%)")
                                        img_col1, img_col2 = st.columns(2)
                                        with img_col1:
                                            if p.get('foto_anggota_url'):
                                                st.image(p['foto_anggota_url'], caption="Anggota")
                                        with img_col2:
                                            if p.get('foto_progres_url'):
                                                st.image(p['foto_progres_url'], caption="Halaman LKPD")
                else:
                    st.info(f"Belum ada laporan masuk untuk hari ini ({today_str}).")
