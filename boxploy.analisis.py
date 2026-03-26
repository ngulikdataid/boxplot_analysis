# ==============================================================
# ADVANCED BOXPLOT ANALYSIS (VS CODE VERSION)
# MULTI-FEATURE VISUALIZATION & COMPARISON
# ==============================================================

# ==============================
# 1. IMPORT LIBRARIES
# ==============================
import pandas as pd                     # Manipulasi data
import numpy as np                      # Operasi numerik
import matplotlib.pyplot as plt         # Visualisasi

# ==============================
# 2. LOAD DATASET
# ==============================
FILE_PATH = r"C:\Users\ronny\Documents\knime_models\boxplot_analysis\metering_nec_20kw - cleaned.csv"  # Path dataset

try:
    DF = pd.read_csv(FILE_PATH)         # Load CSV
except Exception as e:
    raise Exception(f"GAGAL MEMBACA FILE: {e}")

# ==============================
# 3. NORMALISASI KOLOM
# ==============================
DF.columns = [col.upper() for col in DF.columns]  # Ubah ke uppercase

# ==============================
# 4. DAFTAR KOLOM NUMERIK UNTUK BOXPLOT
# ==============================
FEATURE_COLUMNS = [
    "TX_ROOM_TEMPERATURE","MULTIPLEXER_I_CN","MULTIPLEXER_I_EB-NO","MULTIPLEXER_I_LINK_MARGIN",
    "MULTIPLEXER_I_BITRATE","TRANSCODER_BITRATE","PA1_DC","PA2_DC","PA3_DC","PA4_DC",
    "PA5_DC","PA6_DC","PA7_DC","PA8_DC","PA9_DC","PA10_DC","PA11_DC","PA12_DC",
    "PA13_DC","PA14_DC","PA15_DC","PA16_DC","PA17_DC","PA18_DC","TX_ROOM_HUMIDITY",
    "EXCITER_A_MER","EXCITER_B_MER","TRANSMITTER_FWD_POWER","TRANSMITTER_REFLECTED_POWER",
    "PA1_FWD_POWER","PA1_TEMP","PA2_FWD_POWER","PA2_TEMP","PA3_FWD_POWER","PA3_TEMP",
    "PA4_FWD_POWER","PA4_TEMP","PA5_FWD_POWER","PA5_TEMP","PA6_FWD_POWER","PA6_TEMP",
    "PA7_FWD_POWER","PA7_TEMP","PA8_FWD_POWER","PA8_TEMP","PA9_FWD_POWER","PA9_TEMP",
    "PA10_FWD_POWER","PA10_TEMP","PA11_FWD_POWER","PA11_TEMP","PA12_FWD_POWER","PA12_TEMP",
    "PA13_FWD_POWER","PA13_TEMP","PA14_FWD_POWER","PA14_TEMP","PA15_FWD_POWER","PA15_TEMP",
    "PA16_FWD_POWER","PA16_TEMP","PA17_FWD_POWER","PA17_TEMP","PA18_FWD_POWER","PA18_TEMP"
]

# Filter hanya kolom yang ada di dataset
AVAILABLE_COLUMNS = [col for col in FEATURE_COLUMNS if col in DF.columns]

if len(AVAILABLE_COLUMNS) == 0:
    raise ValueError("TIDAK ADA KOLOM YANG VALID UNTUK BOXPLOT")

# ==============================
# 5. CLEANING DATA
# ==============================
NUMERIC_DF = DF[AVAILABLE_COLUMNS].apply(pd.to_numeric, errors='coerce')  # Convert ke numeric

# ==============================
# 6. BOXPLOT GLOBAL (ALL FEATURES)
# ==============================
plt.figure(figsize=(20, 8))  # Ukuran besar agar terbaca
plt.boxplot(NUMERIC_DF.dropna(), vert=True)  # Boxplot semua fitur
plt.xticks(range(1, len(AVAILABLE_COLUMNS)+1), AVAILABLE_COLUMNS, rotation=90)  # Label X
plt.title("GLOBAL BOXPLOT - ALL FEATURES COMPARISON")
plt.tight_layout()

# Save image
GLOBAL_PLOT_PATH = r"C:\Users\ronny\Documents\knime_models\boxplot_analysis\boxplot_all_features.png"
plt.savefig(GLOBAL_PLOT_PATH)
plt.close()

# ==============================
# 7. BOXPLOT PER FEATURE (INDIVIDUAL)
# ==============================
OUTPUT_FOLDER = r"C:\\Users\\ronny\\Documents\\knime_models\\boxplot_analysis\\boxplot_per_feature\\"[:-1]  # Fix trailing backslash issue

import os
os.makedirs(OUTPUT_FOLDER, exist_ok=True)  # Buat folder jika belum ada

for col in AVAILABLE_COLUMNS:
    plt.figure()
    plt.boxplot(NUMERIC_DF[col].dropna())  # Boxplot per kolom
    plt.title(f"BOXPLOT - {col}")

    file_name = OUTPUT_FOLDER + f"boxplot_{col}.png"  # Nama file output
    plt.savefig(file_name)
    plt.close()

# ==============================
# 8. BOXPLOT BERDASARKAN STATUS (COMPARISON GROUP)
# ==============================
if "TRANSMITTER_POWER_STATUS" in DF.columns:
    for col in AVAILABLE_COLUMNS:
        plt.figure(figsize=(8,5))

        grouped_data = []
        labels = []

        for status, group in DF.groupby("TRANSMITTER_POWER_STATUS"):
            values = pd.to_numeric(group[col], errors='coerce').dropna()
            if len(values) > 0:
                grouped_data.append(values)
                labels.append(status)

        if len(grouped_data) > 0:
            plt.boxplot(grouped_data)
            plt.xticks(range(1, len(labels)+1), labels)
            plt.title(f"BOXPLOT {col} BY STATUS")

            file_name = OUTPUT_FOLDER + f"boxplot_{col}_by_status.png"
            plt.savefig(file_name)
            plt.close()

# ==============================
# 9. SUMMARY STATISTICS (OPTIONAL)
# ==============================
SUMMARY = NUMERIC_DF.describe().T  # Statistik ringkasan

SUMMARY_PATH = r"C:\Users\ronny\Documents\knime_models\boxplot_analysis\summary_statistics.csv"
SUMMARY.to_csv(SUMMARY_PATH)

# ==============================
# 10. TAMBAHAN: STATUS CLASSIFICATION (OUTPUT CSV)
# ==============================

TARGET_COLUMN = "TRANSMITTER_FWD_POWER"  # Kolom utama untuk klasifikasi

if TARGET_COLUMN not in DF.columns:
    raise ValueError(f"COLUMN {TARGET_COLUMN} NOT FOUND IN DATASET")

# Fungsi klasifikasi status (engineering rule)
def CLASSIFY_STATUS(VALUE):

    if pd.isna(VALUE):
        return "UNKNOWN"

    # LOW POWER
    if VALUE < 17400:
        return "LOW_POWER"

    # NORMAL LOW
    elif 17400 <= VALUE < 18000:
        return "NORMAL_LOW"

    # NORMAL
    elif 18000 <= VALUE < 20700:
        return "NORMAL"

    # HIGH POWER
    elif 20700 <= VALUE <= 21300:
        return "HIGH_POWER"

    # EXTREME HIGH
    elif VALUE > 21300:
        return "EXTREME_HIGH"

    else:
        return "UNKNOWN"

# Apply klasifikasi
DF["TRANSMITTER_POWER_STATUS"] = pd.to_numeric(
    DF[TARGET_COLUMN], errors='coerce'
).apply(CLASSIFY_STATUS)

# Simpan ke CSV baru
STATUS_OUTPUT_PATH = r"C:\Users\ronny\Documents\knime_models\boxplot_analysis\transmitter_status_output.csv"
DF.to_csv(STATUS_OUTPUT_PATH, index=False)

# ==============================
# 10. LOG OUTPUT
# ==============================
print("=== ANALISIS BOXPLOT SELESAI ===")
print(f"Global Plot: {GLOBAL_PLOT_PATH}")
print(f"Per Feature Folder: {OUTPUT_FOLDER}")
print(f"Summary Stats: {SUMMARY_PATH}")
