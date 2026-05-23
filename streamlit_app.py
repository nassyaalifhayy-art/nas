import streamlit as st
from chempy import balance_stoichiometry

# =========================
# JUDUL
# =========================

st.title("🧪 Kalkulator Stoikiometri")
st.write(
    "Aplikasi untuk menyetarakan persamaan reaksi "
    "dan menghitung stoikiometri sederhana"
)

# =========================
# INPUT REAKSI
# =========================

reaksi = st.text_input(
    "Masukkan persamaan reaksi",
    placeholder="Contoh: H2 + O2 -> H2O"
)

# =========================
# PROSES SETARAKAN
# =========================

if st.button("Setarakan Reaksi"):

    # Cek input kosong
    if reaksi.strip() == "":
        st.warning("⚠ Masukkan persamaan reaksi terlebih dahulu")

    else:
        try:

            # Pisahkan kiri dan kanan
            kiri, kanan = reaksi.split("->")

            # Ambil reaktan dan produk
            reaktan = set(
                i.strip() for i in kiri.split("+")
            )

            produk = set(
                i.strip() for i in kanan.split("+")
            )

            # Setarakan reaksi
            reac, prod = balance_stoichiometry(
                reaktan,
                produk
            )

            # Format hasil kiri
            hasil_kiri = " + ".join(
                [
                    f"{v if v != 1 else ''}{k}"
                    for k, v in reac.items()
                ]
            )

            # Format hasil kanan
            hasil_kanan = " + ".join(
                [
                    f"{v if v != 1 else ''}{k}"
                    for k, v in prod.items()
                ]
            )

            # Hasil akhir
            hasil_reaksi = (
                hasil_kiri + " -> " + hasil_kanan
            )

            # Tampilkan hasil
            st.success(
                "✅ Persamaan reaksi berhasil disetarakan!"
            )

            st.code(hasil_reaksi)

            # =========================
            # STOIKIOMETRI
            # =========================

            st.subheader("Perhitungan Stoikiometri")

            # Semua zat
            semua_zat = (
                list(reac.keys()) +
                list(prod.keys())
            )

            # Pilih zat diketahui
            zat_diketahui = st.selectbox(
                "Pilih zat diketahui",
                semua_zat
            )

            # Pilih zat ditanya
            zat_ditanya = st.selectbox(
                "Pilih zat yang ditanya",
                semua_zat
            )

            # Input massa
            massa = st.number_input(
                f"Masukkan massa {zat_diketahui} (gram)",
                min_value=0.0,
                step=1.0
            )

            # Data Mr sederhana
            Mr = {
                "H2": 2,
                "O2": 32,
                "H2O": 18,
                "Fe": 56,
                "Fe2O3": 160,
                "N2": 28,
                "NH3": 17,
                "CO2": 44,
                "CH4": 16
            }

            # Tombol hitung
            if st.button("Hitung Stoikiometri"):

                # Cek Mr tersedia
                if (
                    zat_diketahui not in Mr or
                    zat_ditanya not in Mr
                ):

                    st.warning(
                        "⚠ Mr zat belum tersedia "
                        "di dalam program"
                    )

                else:

                    # Gram → mol
                    mol_diketahui = (
                        massa / Mr[zat_diketahui]
                    )

                    # Ambil koefisien
                    if zat_diketahui in reac:
                        koef_diketahui = (
                            reac[zat_diketahui]
                        )
                    else:
                        koef_diketahui = (
                            prod[zat_diketahui]
                        )

                    if zat_ditanya in reac:
                        koef_ditanya = (
                            reac[zat_ditanya]
                        )
                    else:
                        koef_ditanya = (
                            prod[zat_ditanya]
                        )

                    # Perbandingan mol
                    mol_ditanya = (
                        mol_diketahui *
                        koef_ditanya /
                        koef_diketahui
                    )

                    # Mol → gram
                    massa_ditanya = (
                        mol_ditanya *
                        Mr[zat_ditanya]
                    )

                    # Output
                    st.success(
                        f"✅ Massa {zat_ditanya} = "
                        f"{massa_ditanya:.2f} gram"
                    )

        except Exception as e:

            st.error(
                "❌ Format reaksi salah\n\n"
                "Gunakan format seperti:\n"
                "H2 + O2 -> H2O"
            )

            st.text(f"Detail error: {e}")
