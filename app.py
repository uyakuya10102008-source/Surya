
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
import ast

st.set_page_config(
    page_title="ASTRA SECANT SURYA",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tampilan aplikasi

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&display=swap');

.stApp {
    background:
        radial-gradient(circle at 15% 15%, #25205a 0%, transparent 35%),
        radial-gradient(circle at 85% 80%, #102d50 0%, transparent 35%),
        #070b1b;
    color: #e8f4ff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #101631, #090e20);
    border-right: 1px solid #27365c;
}

h1, h2, h3 {
    font-family: 'Orbitron', sans-serif !important;
    color: #71eaff !important;
}

.hero {
    background: linear-gradient(135deg, #171d42, #25164c, #102c4b);
    border: 1px solid #3d5b91;
    border-radius: 20px;
    padding: 38px;
    text-align: center;
    box-shadow: 0 0 30px #243c7550;
    margin-bottom: 25px;
}

.hero-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: #8cecff;
    letter-spacing: 3px;
}

.hero-subtitle {
    color: #c5b7ff;
    font-size: 14px;
    letter-spacing: 4px;
    margin-top: 10px;
}

.panel {
    background: #111a34;
    border: 1px solid #30466e;
    border-radius: 15px;
    padding: 22px;
    margin-bottom: 18px;
}

.metric-card {
    background: linear-gradient(145deg, #172344, #211b45);
    border: 1px solid #42618d;
    border-radius: 14px;
    padding: 20px;
    text-align: center;
}

.metric-label {
    color: #aebedb;
    font-size: 13px;
}

.metric-value {
    color: #70eaff;
    font-family: 'Orbitron', sans-serif;
    font-size: 23px;
    font-weight: 700;
    margin-top: 8px;
}

.stButton > button {
    background: linear-gradient(90deg, #5544c8, #168eb5);
    color: white;
    border: 1px solid #70eaff;
    border-radius: 10px;
    font-weight: 700;
    width: 100%;
    padding: 10px;
}

.stButton > button:hover {
    border-color: white;
    color: white;
    box-shadow: 0 0 15px #48dfff80;
}

.stTextInput input,
.stNumberInput input {
    background: #101a32;
    color: white;
    border: 1px solid #40577f;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #30466e;
    border-radius: 10px;
}

hr {
    border-color: #34466c;
}

.footer {
    text-align: center;
    color: #8295b8;
    font-size: 12px;
    padding: 25px;
}
</style>
""", unsafe_allow_html=True)

# Fungsi matematika

fungsi = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "exp": math.exp,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "abs": abs
}

konstanta = {
    "pi": math.pi,
    "e": math.e
}

def hitung_fungsi(ekspresi, x):
    tree = ast.parse(ekspresi, mode="eval")

    def evaluasi(node):
        if isinstance(node, ast.Expression):
            return evaluasi(node.body)

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Nilai tidak valid")

        if isinstance(node, ast.Name):
            if node.id == "x":
                return x
            if node.id in konstanta:
                return konstanta[node.id]
            raise ValueError(f"Variabel tidak dikenal: {node.id}")

        if isinstance(node, ast.BinOp):
            kiri = evaluasi(node.left)
            kanan = evaluasi(node.right)

            if isinstance(node.op, ast.Add):
                return kiri + kanan
            if isinstance(node.op, ast.Sub):
                return kiri - kanan
            if isinstance(node.op, ast.Mult):
                return kiri * kanan
            if isinstance(node.op, ast.Div):
                return kiri / kanan
            if isinstance(node.op, ast.Pow):
                return kiri ** kanan
            if isinstance(node.op, ast.Mod):
                return kiri % kanan

        if isinstance(node, ast.UnaryOp):
            nilai = evaluasi(node.operand)

            if isinstance(node.op, ast.USub):
                return -nilai
            if isinstance(node.op, ast.UAdd):
                return nilai

        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Fungsi tidak valid")

            nama = node.func.id

            if nama not in fungsi:
                raise ValueError(f"Fungsi tidak dikenal: {nama}")

            if len(node.args) != 1:
                raise ValueError("Fungsi harus memiliki satu argumen")

            return fungsi[nama](evaluasi(node.args[0]))

        raise ValueError("Ekspresi matematika tidak didukung")

    hasil = evaluasi(tree)

    if not isinstance(hasil, (int, float)) or not math.isfinite(hasil):
        raise ValueError("Hasil perhitungan tidak valid")

    return float(hasil)

# Metode Secant

def metode_secant(ekspresi, x0, x1, toleransi, maks_iterasi):
    riwayat = []

    f0 = hitung_fungsi(ekspresi, x0)
    f1 = hitung_fungsi(ekspresi, x1)

    for i in range(1, maks_iterasi + 1):
        penyebut = f1 - f0

        if abs(penyebut) < 1e-15:
            raise ValueError("Penyebut terlalu kecil. Coba nilai awal yang berbeda.")

        x2 = x1 - (f1 * (x1 - x0) / penyebut)
        f2 = hitung_fungsi(ekspresi, x2)
        error = abs(x2 - x1)

        riwayat.append({
            "Iterasi": i,
            "x(i-1)": x0,
            "x(i)": x1,
            "f(x(i-1))": f0,
            "f(x(i))": f1,
            "x(i+1)": x2,
            "f(x(i+1))": f2,
            "Error": error
        })

        if error < toleransi:
            return riwayat, x2, f2, "Konvergen"

        x0, x1 = x1, x2
        f0, f1 = f1, f2

    return riwayat, x2, f2, "Maksimum iterasi tercapai"

# Navigasi

with st.sidebar:
    st.markdown("## 🌌 ASTRA STATION")
    st.caption("NUMERICAL COMPUTATION CENTER")
    st.divider()

    halaman = st.radio(
        "NAVIGATION",
        ["Dashboard", "Secant Calculator", "About"]
    )

    st.divider()
    st.markdown("### SYSTEM STATUS")
    st.success("SYSTEM ONLINE")
    st.caption("ASTRA SECANT SURYA v1.0")

# Dashboard

if halaman == "Dashboard":

    st.markdown("""
    <div class="hero">
        <div class="hero-title">ASTRA SECANT SURYA</div>
        <div class="hero-subtitle">SPACE STATION • COMPUTATION CENTER</div>
        <br>
        <p>NUMERICAL COMPUTATION LABORATORY</p>
        <p>SECANT METHOD • NONLINEAR EQUATION SOLVER</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🌠 Welcome to Astra Station")

    st.write(
        "Aplikasi ini digunakan untuk menyelesaikan persamaan "
        "nonlinear menggunakan Metode Secant."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">COMPUTATION METHOD</div>
            <div class="metric-value">SECANT</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">SYSTEM VERSION</div>
            <div class="metric-value">1.0</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">SYSTEM STATUS</div>
            <div class="metric-value">ONLINE</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🪐 About the System")

    st.markdown("""
    <div class="panel">
        <p><b>ASTRA SECANT SURYA</b> merupakan aplikasi komputasi
        numerik untuk mencari akar persamaan nonlinear.</p>
        <p>Pengguna dapat memasukkan fungsi matematika, nilai awal,
        toleransi, dan jumlah iterasi maksimum.</p>
        <p>Hasil perhitungan ditampilkan dalam bentuk tabel iterasi,
        nilai akar, dan grafik fungsi.</p>
    </div>
    """, unsafe_allow_html=True)

# Kalkulator Secant

elif halaman == "Secant Calculator":

    st.markdown("## 🚀 SECANT CALCULATOR")
    st.write("Masukkan parameter untuk memulai proses perhitungan.")

    with st.container(border=True):
        st.markdown("### INPUT PARAMETERS")

        col1, col2 = st.columns(2)

        with col1:
            ekspresi = st.text_input(
                "Fungsi f(x)",
                value="x**2 - 4",
                help="Contoh: x**2 - 4, sin(x), atau x**3 - 2*x - 5"
            )

            x0 = st.number_input(
                "Nilai awal x0",
                value=1.0,
                format="%.6f"
            )

            toleransi = st.number_input(
                "Toleransi",
                min_value=0.000000001,
                value=0.0001,
                format="%.9f"
            )

        with col2:
            x1 = st.number_input(
                "Nilai awal x1",
                value=3.0,
                format="%.6f"
            )

            maks_iterasi = st.number_input(
                "Maksimum iterasi",
                min_value=1,
                max_value=1000,
                value=20,
                step=1
            )

        st.caption(
            "Fungsi yang tersedia: sin, cos, tan, exp, sqrt, log, log10, abs, pi, e"
        )

        mulai = st.button("🚀 MULAI PERHITUNGAN SECANT")

    if mulai:
        try:
            if not ekspresi.strip():
                raise ValueError("Fungsi matematika tidak boleh kosong.")

            riwayat, akar, nilai_f, status = metode_secant(
                ekspresi,
                x0,
                x1,
                toleransi,
                int(maks_iterasi)
            )

            st.markdown("---")
            st.markdown("## 📊 COMPUTATION RESULTS")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("AKAR PERSAMAAN", f"{akar:.10f}")

            with col2:
                st.metric("f(x)", f"{nilai_f:.10e}")

            with col3:
                st.metric("JUMLAH ITERASI", len(riwayat))

            if status == "Konvergen":
                st.success("Perhitungan berhasil. Nilai toleransi telah tercapai.")
            else:
                st.warning(status)

            st.markdown("### 📋 Tabel Iterasi")

            df = pd.DataFrame(riwayat)
            st.dataframe(
                df.style.format({
                    "x(i-1)": "{:.10f}",
                    "x(i)": "{:.10f}",
                    "f(x(i-1))": "{:.10f}",
                    "f(x(i))": "{:.10f}",
                    "x(i+1)": "{:.10f}",
                    "f(x(i+1))": "{:.10f}",
                    "Error": "{:.10e}"
                }),
                use_container_width=True
            )

            st.markdown("### 🌌 Grafik Fungsi")

            rentang_awal = min(x0, x1, akar) - 3
            rentang_akhir = max(x0, x1, akar) + 3

            nilai_x = np.linspace(rentang_awal, rentang_akhir, 300)

            nilai_y = []

            for nilai in nilai_x:
                try:
                    nilai_y.append(hitung_fungsi(ekspresi, nilai))
                except Exception:
                    nilai_y.append(np.nan)

            fig, ax = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor("#111a34")
            ax.set_facecolor("#111a34")

            ax.plot(nilai_x, nilai_y, color="#65eaff", linewidth=2, label="f(x)")
            ax.axhline(0, color="white", linewidth=0.8)
            ax.axvline(0, color="white", linewidth=0.8)
            ax.scatter(akar, nilai_f, color="#ffca70", s=80, label="Akar pendekatan")

            ax.set_xlabel("x", color="white")
            ax.set_ylabel("f(x)", color="white")
            ax.set_title("Grafik Fungsi", color="white")
            ax.tick_params(colors="white")
            ax.grid(alpha=0.2)
            ax.legend()

            st.pyplot(fig)
            plt.close(fig)

            st.markdown("### 📉 Grafik Error")

            fig2, ax2 = plt.subplots(figsize=(10, 4))
            fig2.patch.set_facecolor("#111a34")
            ax2.set_facecolor("#111a34")

            nomor_iterasi = [item["Iterasi"] for item in riwayat]
            nilai_error = [item["Error"] for item in riwayat]

            ax2.plot(
                nomor_iterasi,
                nilai_error,
                marker="o",
                color="#b99aff",
                linewidth=2
            )

            ax2.set_xlabel("Iterasi", color="white")
            ax2.set_ylabel("Error", color="white")
            ax2.set_title("Grafik Konvergensi Error", color="white")
            ax2.tick_params(colors="white")
            ax2.grid(alpha=0.2)

            st.pyplot(fig2)
            plt.close(fig2)

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# About

elif halaman == "About":

    st.markdown("## 🪐 ABOUT ASTRA SECANT SURYA")

    st.markdown("""
    <div class="panel">
        <h3>ASTRA SECANT SURYA</h3>
        <p><b>Space Station Numerical Computation Center</b></p>
        <p>Aplikasi ini dibuat untuk membantu proses pembelajaran
        metode numerik, khususnya Metode Secant.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Metode Secant")

    st.write(
        "Metode Secant merupakan metode numerik terbuka yang "
        "menggunakan dua nilai tebakan awal untuk memperoleh "
        "pendekatan akar persamaan."
    )

    st.latex(
        r"x_{i+1}=x_i-"
        r"\frac{f(x_i)(x_i-x_{i-1})}"
        r"{f(x_i)-f(x_{i-1})}"
    )

    st.markdown("### Fitur Aplikasi")

    st.markdown("""
    - Input fungsi matematika
    - Pengaturan dua nilai awal
    - Pengaturan toleransi
    - Pengaturan maksimum iterasi
    - Tabel hasil iterasi
    - Grafik fungsi
    - Grafik error
    """)

    st.markdown("---")
    st.caption("ASTRA SECANT SURYA • SPACE STATION COMPUTATION CENTER")

# Footer

st.markdown("""
<div class="footer">
    ASTRA SECANT SURYA | SPACE STATION COMPUTATION CENTER<br>
    NUMERICAL COMPUTATION LABORATORY
</div>
""", unsafe_allow_html=True)
