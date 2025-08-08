import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
import tempfile

# Konfigurasi halaman
st.set_page_config(layout="wide", page_title="Peta Interaktif SHP")

st.title("Peta Interaktif dari File SHP")
st.markdown("Unggah file SHP beserta file pendukungnya (.shx, .dbf, .prj) untuk menampilkan peta.")

# Kolom untuk mengunggah file
uploaded_files = st.file_uploader(
    "Pilih file-file SHP (shp, shx, dbf, prj, dll.)",
    type=["shp", "shx", "dbf", "prj", "cpg"],
    accept_multiple_files=True
)

if uploaded_files:
    # Buat direktori temporer untuk menyimpan file yang diunggah
    with tempfile.TemporaryDirectory() as tmpdir:
        shp_path = ""
        for uploaded_file in uploaded_files:
            # Simpan file yang diunggah ke direktori temporer
            file_path = os.path.join(tmpdir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())

            # Cari file .shp untuk dibaca oleh GeoPandas
            if uploaded_file.name.endswith(".shp"):
                shp_path = file_path

        if shp_path:
            try:
                # Muat data SHP dari direktori temporer
                gdf = gpd.read_file(shp_path)

                # --- Visualisasi Peta ---
                
                # Hitung titik pusat peta dari data
                centroid = gdf.geometry.unary_union.centroid
                start_location = [centroid.y, centroid.x]

                # Buat objek peta Folium
                m = folium.Map(location=start_location, zoom_start=11, tiles='cartodbpositron')

                # Tambahkan GeoDataFrame ke peta sebagai GeoJson
                tooltip_fields = list(gdf.columns[~gdf.columns.isin(['geometry'])])
                
                folium.GeoJson(
                    gdf,
                    tooltip=folium.features.GeoJsonTooltip(fields=tooltip_fields, aliases=tooltip_fields)
                ).add_to(m)

                # Tampilkan peta menggunakan streamlit_folium
                st_folium(m, width=800, height=600)

                # Tampilkan informasi tambahan
                st.markdown("---")
                st.subheader("Data Atribut dari SHP")
                st.dataframe(gdf.head())

            except Exception as e:
                st.error(f"Error: Gagal memproses file SHP. Pastikan semua file yang diperlukan sudah diunggah. Detail error: {e}")
        else:
            st.error("Silakan unggah file `.shp` bersama dengan file pendukungnya.")