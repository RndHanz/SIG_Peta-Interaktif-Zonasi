import streamlit as st
import folium
from folium.plugins import MiniMap
from streamlit_folium import st_folium

# ---------------------------------------------------------
# 1. KONFIGURASI HALAMAN WEBPAGE
# ---------------------------------------------------------
st.set_page_config(
    page_title="Peta Interaktif Zonasi Konservasi Situs Purbakala",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# 2. CUSTOM CSS UTAMA (MODERN DASHBOARD & LEAFLET STYLING)
# ---------------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Header Card Styling */
    .header-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
        color: #ffffff;
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .header-subtitle {
        color: #94A3B8;
        font-size: 0.95rem;
        line-height: 1.5;
    }

    /* Executive Summary Card */
    .summary-card {
        background-color: #F8FAFC;
        border-left: 5px solid #2563EB;
        padding: 1.25rem 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .summary-title {
        font-weight: 700;
        color: #0F172A;
        font-size: 1.05rem;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 3. HEADER & SUMMARY EXECUTIVE
# ---------------------------------------------------------
st.markdown("""
<div class="header-card">
    <div class="header-title">🏛️ Peta Interaktif Zonasi Konservasi & Wisata Edukasi Situs Purbakala</div>
    <div class="header-subtitle">
        Sistem Informasi Geografis Pelestarian Cagar Budaya & Mitigasi Risiko Kerusakan Struktural (Kawasan Prambanan - DIY/Jateng)
    </div>
</div>
""", unsafe_allow_html=True)

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Situs Purbakala Terdaftar", value="7 Candi", delta="Kawasan Prambanan & Sambirejo")
with col2:
    st.metric(label="Radius Kerentanan Getaran", value="500m & 1 KM", delta="High Alert Radius", delta_color="inverse")
with col3:
    st.metric(label="Fasilitas Informasi Wisata", value="2 Unit", delta="Pusat Edukasi & Tiketing")
with col4:
    st.metric(label="Pos Pemantauan BPK", value="2 Pos", delta="Piyungan & Prambanan Guard")

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="summary-card">
    <div class="summary-title">📋 Ringkasan Eksekutif Analisis Ancaman Kawasan Cagar Budaya</div>
    <p style="color: #334155; margin: 0; font-size: 0.95rem; line-height: 1.6;">
    Berdasarkan hasil analisis spasial kerentanan kawasan cagar budaya di klaster Prambanan dan sekitarnya, perluasan alih fungsi lahan dan ekspansi pemukiman modern di sekitar 
    <b>zonasi penyangga (buffer zone)</b> menimbulkan ancaman nyata terhadap kelestarian struktur candi purbakala. Getaran akibat aktivitas 
    transportasi jalan raya utama dan pembangunan fisik dalam radius <b>500m hingga 1 KM</b> berisiko tinggi mempercepat degradasi struktural situs.
    <br><br>
    Melalui pemetaan interaktif ini, Balai Pelestarian Kebudayaan (BPK) dan pemangku kebijakan pariwisata dapat memantau batas aman 
    zonasi inti serta membatasi aktivitas pariwisata massal. Penguatan pos pemantauan di jalur Piyungan/Prambanan dan penyediaan fasilitas edukasi wisata terpadu 
    diharapkan mampu menyeimbangkan potensi ekonomi pariwisata dengan perlindungan cagar budaya secara berkelanjutan.
    </p>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. SIDEBAR FILTER & CONTROL
# ---------------------------------------------------------
st.sidebar.markdown("### 🔍 Filter & Kontrol Layer")
st.sidebar.markdown("Gunakan kontrol di bawah untuk memfilter data pada peta interaktif.")

period_filter = st.sidebar.selectbox(
    "Filter Periodisasi Situs:",
    ["Semua Periodisasi", "Hindu", "Buddha"],
    index=0
)

st.sidebar.divider()
st.sidebar.markdown("""
### 🎨 Panduan Layer Warna
- 🔴 **Merah:** Situs Utama / Zonasi Inti Candi
- 🟠 **Oranye:** Zonasi Penyangga (*Buffer Zone*)
- ⚠️ **Merah/Kuning Transparan:** Buffer Kerentanan Getaran (500m & 1KM)
- 🟢 **Hijau:** Pusat Informasi & Wisata Edukasi
- 🔵 **Biru:** Pos Pemantauan Guard BPK
""")

# ---------------------------------------------------------
# 5. DATA SPASIAL ASLI QGIS (Kawasan Prambanan & Sekitarnya)
# ---------------------------------------------------------
situs_data = [
    {
        "nama": "Candi Prambanan",
        "lat": -7.7520, "lon": 110.4914,
        "periode": "Hindu",
        "abad": "Abad ke-9 M",
        "dinasti": "Mataram Kuno (Rakai Pikatan)",
        "status": "Terpelihara Baik / UNESCO World Heritage",
        "risiko": "Tinggi (Getaran Jalan Raya Utama & Pariwisata Massal)"
    },
    {
        "nama": "Candi Sewu",
        "lat": -7.7438, "lon": 110.4928,
        "periode": "Buddha",
        "abad": "Abad ke-8 M",
        "dinasti": "Syailendra (Rakai Panangkaran)",
        "status": "Terpelihara Baik",
        "risiko": "Sedang (Risiko Getaran Kendaraan)"
    },
    {
        "nama": "Candi Bubrah",
        "lat": -7.7461, "lon": 110.4933,
        "periode": "Buddha",
        "abad": "Abad ke-9 M",
        "dinasti": "Syailendra",
        "status": "Terpelihara / Selesai Pemugaran",
        "risiko": "Sedang"
    },
    {
        "nama": "Candi Lumbung",
        "lat": -7.7478, "lon": 110.4938,
        "periode": "Buddha",
        "abad": "Abad ke-9 M",
        "dinasti": "Syailendra",
        "status": "Terpelihara",
        "risiko": "Sedang"
    },
    {
        "nama": "Candi Sojiwan",
        "lat": -7.7615, "lon": 110.4952,
        "periode": "Buddha",
        "abad": "Abad ke-9 M",
        "dinasti": "Mataram Kuno",
        "status": "Terpelihara Baik",
        "risiko": "Tinggi (Dekat Pemukiman Penduduk)"
    },
    {
        "nama": "Candi Barong",
        "lat": -7.7735, "lon": 110.4908,
        "periode": "Hindu",
        "abad": "Abad ke-9 M",
        "dinasti": "Mataram Kuno",
        "status": "Rentan (Perbukitan)",
        "risiko": "Sangat Tinggi (Erosi Lereng & Longsor)"
    },
    {
        "nama": "Candi Ijo",
        "lat": -7.7838, "lon": 110.5119,
        "periode": "Hindu",
        "abad": "Abad ke-10 M",
        "dinasti": "Mataram Kuno",
        "status": "Terpelihara Baik (Titik Tertinggi)",
        "risiko": "Tinggi (Aktivitas Wisata Lereng)"
    }
]

fasilitas_data = [
    {"nama": "Pusat Informasi Wisata Prambanan", "lat": -7.7535, "lon": 110.4890, "kapasitas": "3000 Orang/Hari", "layanan": "Edukasi Arkeologi, Museum, & Tiketing Utama"},
    {"nama": "Fasilitas Edukasi Candi Ijo", "lat": -7.7845, "lon": 110.5110, "kapasitas": "500 Orang/Hari", "layanan": "Pos Informasi Geo-Heritage"}
]

pos_data = [
    {"nama": "Pos Pemantauan Utama BPK Prambanan", "lat": -7.7420, "lon": 110.4910, "petugas": "6 Guard BPK", "kontak": "Sektor Utara Prambanan"},
    {"nama": "Pos Pemantauan Piyungan - Candi Ijo", "lat": -7.8300, "lon": 110.4700, "petugas": "4 Guard BPK", "kontak": "Sektor Selatan Perbukitan"}
]

# ---------------------------------------------------------
# 6. INISIALISASI PETA BASEMAP TERPUSAT DI KAWASAN PRAMBANAN
# ---------------------------------------------------------
carto_voyager = folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    attr="&copy; <a href='https://www.openstreetmap.org/copyright'>OpenStreetMap</a> &copy; <a href='https://carto.com/attributions'>CARTO</a>",
    name="CartoDB Voyager"
)

# Pusat Koordinat Peta Set ke Tengah Kompleks Prambanan - Candi Ijo (-7.7620, 110.4980)
m = folium.Map(
    location=[-7.7620, 110.4980],
    zoom_start=13,
    tiles=carto_voyager,
    control_scale=True
)

minimap_tile = folium.TileLayer(
    tiles="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png",
    attr="&copy; CARTO"
)
minimap = MiniMap(tile_layer=minimap_tile, toggle_display=True)
m.add_child(minimap)

# Feature Groups (Tersedia Checkbox Layer Control)
fg_candi = folium.FeatureGroup(name="🔴 Situs Utama / Zonasi Inti Candi")
fg_buffer_zonasi = folium.FeatureGroup(name="🟠 Zonasi Penyangga (Buffer Zone)")
fg_getaran = folium.FeatureGroup(name="⚠️ Buffer Kerentanan Getaran (500m & 1KM)")
fg_fasilitas = folium.FeatureGroup(name="🟢 Pusat Informasi & Fasilitas Edukasi")
fg_pos = folium.FeatureGroup(name="🔵 Pos Pemantauan/Penjaga Situs")

# ---------------------------------------------------------
# 7. POPUP & FEATURE STYLING
# ---------------------------------------------------------

# A. Render Buffer 500m & 1KM untuk SELURUH CANDI ASLI
for item in situs_data:
    # Buffer 500m (Lingkaran Merah Transparan)
    folium.Circle(
        location=[item["lat"], item["lon"]],
        radius=500,
        color="#DC2626",
        weight=1.5,
        fill=True,
        fill_color="#EF4444",
        fill_opacity=0.35,
        popup=f"<b>⚠️ Buffer Getaran 500m ({item['nama']}):</b> Zona Kerentanan Tinggi"
    ).add_to(fg_getaran)

    # Buffer 1KM (Lingkaran Oranye Transparan)
    folium.Circle(
        location=[item["lat"], item["lon"]],
        radius=1000,
        color="#D97706",
        weight=1,
        dash_array="4, 4",
        fill=True,
        fill_color="#F59E0B",
        fill_opacity=0.15,
        popup=f"<b>⚠️ Buffer Getaran 1KM ({item['nama']}):</b> Zona Batas Pemantauan Transportasi"
    ).add_to(fg_getaran)

# B. Render Poligon Zonasi Penyangga Kawasan Kompleks Candi
folium.Polygon(
    locations=[
        [-7.7400, 110.4850], [-7.7400, 110.5000],
        [-7.7680, 110.5020], [-7.7680, 110.4870]
    ],
    color="#D97706",
    weight=2,
    fill=True,
    fill_color="#FBBF24",
    fill_opacity=0.20,
    popup="<b>🟠 Zonasi Penyangga Kawasan Candi Prambanan-Sojiwan:</b> Area Pembangunan Terbatas"
).add_to(fg_buffer_zonasi)

# C. Render Situs Candi (Disesuaikan Filter Periodisasi)
for item in situs_data:
    if period_filter == "Semua Periodisasi" or item["periode"] == period_filter:
        popup_html = f"""
        <div style="font-family: 'Plus Jakarta Sans', sans-serif; width: 240px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
            <div style="background: linear-gradient(135deg, #DC2626 0%, #991B1B 100%); color: white; padding: 10px 14px; font-weight: 700; font-size: 13px;">
                🏛️ {item['nama']}
            </div>
            <div style="padding: 12px; background-color: #FFFFFF; font-size: 12px; color: #1E293B; line-height: 1.6;">
                <div style="margin-bottom: 4px;"><b>Abad Pembuatan:</b> {item['abad']}</div>
                <div style="margin-bottom: 4px;"><b>Kerajaan/Dinasti:</b> {item['dinasti']}</div>
                <div style="margin-bottom: 6px;"><b>Periodisasi:</b> <span style="background-color: #F1F5F9; color: #334155; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">{item['periode']}</span></div>
                <div style="margin-bottom: 6px;"><b>Status Konservasi:</b> <span style="color: #059669; font-weight: 600;">{item['status']}</span></div>
                <div style="border-top: 1px solid #E2E8F0; margin-top: 8px; padding-top: 8px;">
                    <b style="color: #DC2626;">Tingkat Risiko Kerusakan:</b><br>
                    <span style="color: #991B1B; font-weight: 600;">{item['risiko']}</span>
                </div>
            </div>
        </div>
        """
        folium.Marker(
            location=[item["lat"], item["lon"]],
            popup=folium.Popup(popup_html, max_width=270),
            tooltip=item["nama"],
            icon=folium.Icon(color="red", icon="landmark", prefix="fa")
        ).add_to(fg_candi)

# D. Render Pusat Informasi & Fasilitas Edukasi
for fas in fasilitas_data:
    popup_fas = f"""
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; width: 230px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <div style="background: linear-gradient(135deg, #16A34A 0%, #15803D 100%); color: white; padding: 10px 14px; font-weight: 700; font-size: 13px;">
            ℹ️ {fas['nama']}
        </div>
        <div style="padding: 12px; background-color: #FFFFFF; font-size: 12px; color: #1E293B; line-height: 1.5;">
            <b>Kapasitas Pengunjung:</b><br>{fas['kapasitas']}<br><br>
            <b>Jenis Layanan:</b><br>{fas['layanan']}
        </div>
    </div>
    """
    folium.Marker(
        location=[fas["lat"], fas["lon"]],
        popup=folium.Popup(popup_fas, max_width=260),
        tooltip=fas["nama"],
        icon=folium.Icon(color="green", icon="info-circle", prefix="fa")
    ).add_to(fg_fasilitas)

# E. Render Pos Pemantauan Guard BPK
for pos in pos_data:
    popup_pos = f"""
    <div style="font-family: 'Plus Jakarta Sans', sans-serif; width: 220px; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
        <div style="background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%); color: white; padding: 10px 14px; font-weight: 700; font-size: 13px;">
            🛡️ {pos['nama']}
        </div>
        <div style="padding: 12px; background-color: #FFFFFF; font-size: 12px; color: #1E293B; line-height: 1.5;">
            <b>Personil Guard:</b> {pos['petugas']}<br>
            <b>Sektor Pengawasan:</b> {pos['kontak']}
        </div>
    </div>
    """
    folium.Marker(
        location=[pos["lat"], pos["lon"]],
        popup=folium.Popup(popup_pos, max_width=240),
        tooltip=pos["nama"],
        icon=folium.Icon(color="blue", icon="shield-alt", prefix="fa")
    ).add_to(fg_pos)

# ---------------------------------------------------------
# 8. FLOATING LEAFLET LEGEND
# ---------------------------------------------------------
legend_html = """
<div style="
    position: fixed; 
    bottom: 30px; right: 30px; width: 230px; height: auto; 
    z-index:9999; font-size:11px; font-weight: 500;
    background-color: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(4px);
    border-radius: 12px;
    padding: 12px 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    border: 1px solid #E2E8F0;
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1E293B;
">
    <div style="font-weight: 700; margin-bottom: 8px; font-size: 12px; color: #0F172A;">Legenda Spasial QGIS</div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="background-color: #DC2626; width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px;"></span> Situs Utama (7 Candi)</div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="background-color: #FBBF24; border: 1px solid #D97706; width: 12px; height: 12px; border-radius: 2px; display: inline-block; margin-right: 8px;"></span> Zonasi Penyangga</div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="background-color: rgba(239, 68, 68, 0.4); border: 1px solid #DC2626; width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px;"></span> Buffer Getaran 500m</div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="background-color: rgba(245, 158, 11, 0.2); border: 1px dashed #D97706; width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px;"></span> Buffer Getaran 1KM</div>
    <div style="display: flex; align-items: center; margin-bottom: 6px;"><span style="background-color: #16A34A; width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px;"></span> Pusat Informasi Wisata</div>
    <div style="display: flex; align-items: center;"><span style="background-color: #2563EB; width: 12px; height: 12px; border-radius: 50%; display: inline-block; margin-right: 8px;"></span> Pos Pemantauan Guard BPK</div>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))

# ---------------------------------------------------------
# 9. RENDER PETA KE STREAMLIT
# ---------------------------------------------------------
fg_candi.add_to(m)
fg_buffer_zonasi.add_to(m)
fg_getaran.add_to(m)
fg_fasilitas.add_to(m)
fg_pos.add_to(m)

# Layer Control Checkbox
folium.LayerControl(collapsed=False, position="topright").add_to(m)

# Render Full Width Map
st_folium(m, use_container_width=True, height=650)