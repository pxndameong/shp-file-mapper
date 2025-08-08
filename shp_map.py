import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Konfigurasi halaman
st.set_page_config(layout="wide", page_title="Peta Interaktif Kota")

st.title("Peta Interaktif Kota dengan Streamlit")
st.markdown("Aplikasi web sederhana untuk menampilkan file SHP kota.")

# Menggunakan cache_data untuk performa yang lebih baik
@st.cache_data
def load_data(file_path):
    """Fungsi untuk memuat file SHP menggunakan GeoPandas."""
    try:
        gdf = gpd.read_file(file_path)
        return gdf
    except Exception as e:
        st.error(f"Error: Gagal memuat file SHP. Pastikan semua file pendukung (.dbf, .shx, .prj) ada. {e}")
        return None

# Ganti 'path/ke/file/kota.shp' dengan lokasi file SHP Anda
# Pastikan file SHP dan file pendukungnya berada di folder yang sama dengan app.py
shp_file_path = "path/ke/file/kota.shp"

# Muat data
gdf_kota = load_data(shp_file_path)

if gdf_kota is not None:
    # Perhitungan titik pusat peta dari data
    centroid = gdf_kota.geometry.unary_union.centroid
    start_location = [centroid.y, centroid.x]

    # Buat objek peta Folium
    m = folium.Map(location=start_location, zoom_start=11, tiles='cartodbpositron')

    # Tambahkan GeoDataFrame ke peta sebagai GeoJson
    # Anda bisa menambahkan tooltip untuk menampilkan informasi dari atribut
    # Misalnya, jika ada kolom 'nama_kecamatan' dan 'populasi' di SHP Anda
    folium.GeoJson(
        gdf_kota,
        tooltip=folium.features.GeoJsonTooltip(fields=["nama_kecamatan", "populasi"], aliases=["Kecamatan:", "Populasi:"])
    ).add_to(m)

    # Tampilkan peta menggunakan streamlit_folium
    st_folium(m, width=700, height=500)

    # Tambahkan informasi tambahan
    st.markdown("---")
    st.subheader("Data Atribut")
    st.dataframe(gdf_kota.head())