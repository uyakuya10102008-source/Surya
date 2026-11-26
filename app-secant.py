
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ast
import math

# Konfigurasi halaman
st.set_page_config(
    page_title="ASTRA SECANT SURYA",
    page_icon="🌌",
    layout="wide"
)

# Tampilan futuristik
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #070b1c, #111a34, #241442);
    color: white;
}
section[data-testid="stSidebar"] {
    background: #0b1025;
}
h1, h2, h3, p, label {
    color: #eaf6ff !important;
}
.neon {
    color: #65eaff;
    text-shadow: 0 0 12px #00d9ff;
}
.metric-card {
    background: #151f3d;
    padding: 20px;
    border: 1px solid #315a91;
    border-radius: 12px;
    text-align: center;
}
.stButton button {
    background: linear-gradient(90deg, #087ea4, #7137b8);
    color: white;
    border: none;
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Judul aplikasi
st.markdown(
    "<h1 class='neon'>🌌 ASTRA SECANT SURYA</h1>",
    unsafe_allow_html=True
)
st.caption("NUMERICAL COMPUTATION SYSTEM | METODE SECANT")

# Fungsi matematika yang diizinkan
FUNGSI = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "abs": abs
}

# Evaluasi ekspresi secara aman
def hitung_fungsi(ekspresi, x):
    node = ast.parse(ekspresi, mode="eval")

    def evaluasi(n):
        if isinstance(n, ast.Expression):
            return evaluasi(n.body)

        if isinstance(n, ast.Constant):
            if isinstance(n.value, (int, float)):
                return n.value
            raise ValueError("Konstanta tidak valid")

        if isinstance(n, ast.Name):
            if n.id == "x":
                return x
            if n.id == "pi":
                return math.pi
            if n.id == "e":
                return math.e
            raise ValueError("Variabel tidak dikenal")

        if isinstance(n, ast.BinOp):
            a = evaluasi(n.left)
            b = evaluasi(n.right)

            if isinstance(n.op, ast.Add):
                return a + b
            if isinstance(n.op, ast.Sub):
                return a - b
            if isinstance(n.op, ast.Mult):
                return a * b
            if isinstance(n.op, ast.Div):
                return a / b
            if isinstance(n.op, ast.Pow):
                return a ** b
            if isinstance(n.op, ast.Mod):
                return a % b

        if isinstance(n, ast.UnaryOp):
            a = evaluasi(n.operand)
            if isinstance(n.op, ast.USub):
                return -a
            if isinstance(n.op, ast.UAdd):
                return a

        if isinstance(n, ast.Call):
            if (
                isinstance(n.func, ast.Name)
                and n.func.id in FUNGSI
                and len(n.args) == 1
                and not n.keywords
            ):
                return FUNGSI[n.func.id](evaluasi(n.args[0]))

        raise ValueError("Format persamaan tidak didukung")

    return float(evaluasi(node))


# Metode Secant
def metode_secant(fungsi, x0, x1, toleransi, maks_iterasi):
    riwayat = []

    for i in range(1, maks_iterasi + 1):
        f0 = hitung_fungsi(fungsi, x0)
        f1 = hitung_fungsi(fungsi, x1)

        penyebut = f1 - f0

        if abs(penyebut) < 1e-15:
            raise ZeroDivisionError(
                "Penyebut mendekati nol. Pilih nilai awal berbeda."
            )

        x2 = x1 - (f1 * (x1 - x0) / penyebut)
        f2 = hitung_fungsi(fungsi, x2)
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

        if not math.isfinite(x2) or not math.isfinite(f2):
            raise ValueError("Hasil perhitungan tidak valid.")

        if error < toleransi:
            return riwayat, x2, f2, "Konvergen"

        x0 = x1
        x1 = x2

    return riwayat, x2, f2, "Maksimum iterasi tercapai"


# Navigasi
with st.sidebar:
    st.markdown("## 🌌 ASTRA CONTROL")
    halaman = st.radio(
        "Navigasi",
        ["Dashboard", "Secant Calculator", "About"]
    )
    st.markdown("---")
    st.caption("ASTRA SECANT SURYA")
    st.caption("Numerical Method Project")

# Dashboard
if halaman == "Dashboard":
    st.markdown("## 🚀 Dashboard")
    st.write(
        "Selamat datang di sistem komputasi numerik "
        "ASTRA SECANT SURYA."
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            "<div class='metric-card'>"
            "<h3>01</h3><p>Metode Secant</p></div>",
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            "<div class='metric-card'>"
            "<h3>02</h3><p>Iterasi Numerik</p></div>",
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            "<div class='metric-card'>"
            "<h3>03</h3><p>Analisis Grafik</p></div>",
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("### Fitur Sistem")
    st.write("- Menghitung akar persamaan nonlinier.")
    st.write("- Menggunakan metode numerik Secant.")
    st.write("- Menampilkan tabel hasil setiap iterasi.")
    st.write("- Menampilkan grafik konvergensi dan error.")

# Kalkulator Secant
elif halaman == "Secant Calculator":
    st.markdown("## 🧮 Secant Calculator")
    st.write("Masukkan persamaan dan parameter perhitungan.")

    col1, col2 = st.columns(2)

    with col1:
        fungsi = st.text_input(
            "Persamaan f(x)",
            value="x**2 - 4"
        )

        x0 = st.number_input(
            "Nilai awal x0",
            value=1.0,
            format="%.6f"
        )

        x1 = st.number_input(
            "Nilai awal x1",
            value=3.0,
            format="%.6f"
        )

    with col2:
        toleransi = st.number_input(
            "Toleransi error",
            min_value=0.000000001,
            value=0.0001,
            format="%.9f"
        )

        maks_iterasi = st.number_input(
            "Maksimum iterasi",
            min_value=1,
            max_value=1000,
            value=20
        )

    mulai = st.button("🚀 HITUNG AKAR PERSAMAAN")

    if mulai:
        try:
            if x0 == x1:
                st.error("Nilai x0 dan x1 tidak boleh sama.")
            else:
                riwayat, akar, nilai_f, status = metode_secant(
                    fungsi, x0, x1, toleransi, maks_iterasi
                )

                st.markdown("---")
                st.markdown("## 📊 Hasil Perhitungan")

                c1, c2, c3 = st.columns(3)

                c1.metric("Akar Persamaan", f"{akar:.10f}")
                c2.metric("f(x)", f"{nilai_f:.3e}")
                c3.metric("Jumlah Iterasi", len(riwayat))

                if status == "Konvergen":
                    st.success("Perhitungan berhasil mencapai toleransi.")
                else:
                    st.warning(status)

                st.markdown("### 📋 Tabel Iterasi")

                df = pd.DataFrame(riwayat)
                st.dataframe(
                    df.style.format("{:.10f}", subset=[
                        "x(i-1)", "x(i)", "f(x(i-1))",
                        "f(x(i))", "x(i+1)",
                        "f(x(i+1))", "Error"
                    ]),
                    use_container_width=True
                )

                # Grafik fungsi
                st.markdown("### 📈 Grafik Fungsi")

                rentang = max(abs(x0), abs(x1), 5)
                rentang = min(rentang * 2, 1000)
                x_plot = np.linspace(-rentang, rentang, 400)

                y_plot = []
                for nilai in x_plot:
                    try:
                        hasil = hitung_fungsi(fungsi, nilai)
                        y_plot.append(
                            hasil if math.isfinite(hasil) else np.nan
                        )
                    except Exception:
                        y_plot.append(np.nan)

                fig, ax = plt.subplots(figsize=(10, 4))
                fig.patch.set_facecolor("#111a34")
                ax.set_facecolor("#111a34")

                ax.plot(x_plot, y_plot, color="#65eaff", label="f(x)")
                ax.axhline(0, color="white", linewidth=0.8)
                ax.axvline(0, color="white", linewidth=0.8)
                ax.scatter(akar, nilai_f, color="#ffcc66",
                           label="Akar pendekatan")

                ax.set_title("Grafik Persamaan", color="white")
                ax.set_xlabel("x", color="white")
                ax.set_ylabel("f(x)", color="white")
                ax.tick_params(colors="white")
                ax.grid(alpha=0.2)
                ax.legend()

                st.pyplot(fig)
                plt.close(fig)

                # Grafik x(i+1)
                st.markdown("### 📈 Grafik Nilai x(i+1)")

                nomor_iterasi = [item["Iterasi"] for item in riwayat]
                nilai_x = [item["x(i+1)"] for item in riwayat]

                fig_x, ax_x = plt.subplots(figsize=(10, 4))
                fig_x.patch.set_facecolor("#111a34")
                ax_x.set_facecolor("#111a34")

                ax_x.plot(
                    nomor_iterasi,
                    nilai_x,
                    marker="o",
                    color="#65eaff",
                    linewidth=2,
                    label="x(i+1)"
                )

                ax_x.set_xlabel("Iterasi", color="white")
                ax_x.set_ylabel("Nilai x(i+1)", color="white")
                ax_x.set_title(
                    "Grafik Konvergensi Nilai x(i+1)",
                    color="white"
                )
                ax_x.tick_params(colors="white")
                ax_x.grid(alpha=0.2)
                ax_x.legend()

                st.pyplot(fig_x)
                plt.close(fig_x)

                # Grafik error
                st.markdown("### 📉 Grafik Error")

                error = [item["Error"] for item in riwayat]

                fig_e, ax_e = plt.subplots(figsize=(10, 4))
                fig_e.patch.set_facecolor("#111a34")
                ax_e.set_facecolor("#111a34")

                ax_e.plot(
                    nomor_iterasi,
                    error,
                    marker="o",
                    color="#ffcc66",
                    linewidth=2,
                    label="Error"
                )

                ax_e.set_xlabel("Iterasi", color="white")
                ax_e.set_ylabel("Error", color="white")
                ax_e.set_title("Grafik Error Setiap Iterasi", color="white")
                ax_e.tick_params(colors="white")
                ax_e.grid(alpha=0.2)
                ax_e.legend()

                st.pyplot(fig_e)
                plt.close(fig_e)

                # Unduh hasil
                st.markdown("### 📥 Unduh Hasil")
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Tabel Iterasi (CSV)",
                    data=csv,
                    file_name="hasil_metode_secant.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

# About
elif halaman == "About":
    st.markdown("## 🌠 About ASTRA SECANT SURYA")

    st.write("""
    ASTRA SECANT SURYA merupakan aplikasi komputasi numerik
    untuk mencari akar persamaan nonlinier menggunakan
    metode Secant.

    **Rumus Metode Secant:**
    """)

    st.latex(
        r"x_{i+1}=x_i-"
        r"\frac{f(x_i)(x_i-x_{i-1})}"
        r"{f(x_i)-f(x_{i-1})}"
    )

    st.markdown("### Cara Penggunaan")
    st.write("1. Buka menu Secant Calculator.")
    st.write("2. Masukkan persamaan f(x).")
    st.write("3. Masukkan nilai awal x0 dan x1.")
    st.write("4. Tentukan toleransi dan maksimum iterasi.")
    st.write("5. Klik tombol Hitung Akar Persamaan.")
    st.write("6. Amati tabel iterasi dan ketiga grafik.")

    st.markdown("### Contoh Pengujian")
    st.code("""
f(x) = x**2 - 4
x0 = 1
x1 = 3
Toleransi = 0.0001
Maksimum iterasi = 20

Akar yang diharapkan mendekati 2
    """)

    st.info(
        "Aplikasi ini dibuat sebagai media pembelajaran "
        "metode numerik Secant."
    )
