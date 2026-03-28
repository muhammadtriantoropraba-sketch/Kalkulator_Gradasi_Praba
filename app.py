import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="MTP Sieve Analyzer", layout="wide", page_icon="🏗️")

# 2. SIDEBAR (Identitas Project)
with st.sidebar:
    st.header("👤 Identitas Pengembang")
    st.success("Nama: **Muhammad Triantoropraba**")
    st.info("Project: **KAKUKA 2026**")
    st.divider()
    st.write("Aplikasi ini otomatis menghitung distribusi ukuran butir dan menampilkan kurva gradasi semi-log.")

# 3. HEADER UTAMA
st.title("🏗️ MTP-Sieve Analyzer")
st.subheader("Developed by: Muhammad Triantoropraba") # Nama kamu di bawah judul utama
st.caption("Solusi Otomatisasi Analisis Saringan untuk Teknik Sipil")
st.divider()

# 4. DATA AWAL (Default)
if 'df_data' not in st.session_state:
    data = {
        'No. Saringan': ['4', '8', '16', '35', '50', '120', '200', 'Pan'],
        'Diameter (mm)': [4.75, 2.36, 1.18, 0.5, 0.3, 0.125, 0.075, 0.0],
        'Berat Saringan (gr)': [500.0, 450.0, 420.0, 380.0, 350.0, 330.0, 310.0, 300.0],
        'Berat Tanah + Saringan (gr)': [550.0, 525.0, 520.0, 480.0, 425.0, 380.0, 345.0, 315.0]
    }
    st.session_state.df_data = pd.DataFrame(data)

# 5. LAYOUT KOLOM
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📝 Input Data")
    df_input = st.data_editor(st.session_state.df_data, num_rows="dynamic", use_container_width=True)
    
    try:
        df_input['Tertahan (gr)'] = df_input['Berat Tanah + Saringan (gr)'] - df_input['Berat Saringan (gr)']
        total_berat = df_input['Tertahan (gr)'].sum()
        
        if total_berat > 0:
            df_input['% Tertahan'] = (df_input['Tertahan (gr)'] / total_berat) * 100
            df_input['% Lolos'] = 100 - df_input['% Tertahan'].cumsum()
            df_input.loc[df_input.index[-1], '% Lolos'] = 0 
            
            st.write("**Tabel Perhitungan Otomatis:**")
            st.dataframe(df_input[['No. Saringan', 'Diameter (mm)', 'Tertahan (gr)', '% Lolos']].style.format(precision=2), use_container_width=True)
            
            # Tombol Download
            st.download_button("💾 Simpan ke CSV (Excel)", df_input.to_csv(index=False), "Hasil_MTP_Analyzer.csv")
    except:
        st.error("Periksa kembali input angka Anda.")

with col2:
    st.subheader("📊 Grafik Gradasi")
    if 'total_berat' in locals() and total_berat > 0:
        fig, ax = plt.subplots(figsize=(8, 5))
        plot_df = df_input[df_input['Diameter (mm)'] > 0]
        ax.plot(plot_df['Diameter (mm)'], plot_df['% Lolos'], marker='o', color='#FF8C00', linewidth=2, markersize=8)
        
        ax.set_xscale('log')
        ax.invert_xaxis()
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.set_xticks([10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05])
        
        ax.grid(True, which="both", ls="-", alpha=0.3)
        ax.set_xlabel("Diameter Saringan (mm)")
        ax.set_ylabel("Persen Lolos (%)")
        ax.set_ylim(0, 105)
        
        for x, y in zip(plot_df['Diameter (mm)'], plot_df['% Lolos']):
            ax.text(x, y + 3, f'{y:.1f}%', ha='center', fontsize=8, fontweight='bold')
        
        st.pyplot(fig)
        st.metric("Total Berat Sampel", f"{total_berat:.2f} gr")

# 6. FOOTER
st.divider()
st.caption("© 2026 Muhammad Triantoropraba | Civil Engineering Automation")