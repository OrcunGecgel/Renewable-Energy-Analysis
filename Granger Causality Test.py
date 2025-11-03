import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, grangercausalitytests
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi oku
veri = pd.read_csv("dunya_temiz_veri_tum_ulkeler.csv")

# Tüm dünya için filtrele ve 2000-2023 seç
veri_dunya = veri[(veri["Country Name"] == "World") & (veri["year"] >= 2000) & (veri["year"] <= 2023)].copy()

# Kişi başına yenilenebilir enerji üretimi hesapla
veri_dunya["renewables_production_per_capita"] = veri_dunya["renewables_production"] / veri_dunya["population"]

# İlgili sütunları seç ve eksik verileri temizle
veri_dunya = veri_dunya[["year", "renewables_production_per_capita", "co2_per_capita", "gdp_per_capita"]].dropna()

# Durağanlık testi (ADF)
def adf_test(series, name):
    result = adfuller(series, autolag="AIC")
    print(f"\nADF Test for {name}:")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Stationary" if result[1] < 0.05 else "Non-stationary")
    return result[1] < 0.05

# Durağanlık kontrolü
stationary_vars = {
    "renewables_production_per_capita": adf_test(veri_dunya["renewables_production_per_capita"], "Renewables Production per Capita"),
    "co2_per_capita": adf_test(veri_dunya["co2_per_capita"], "CO2 per Capita"),
    "gdp_per_capita": adf_test(veri_dunya["gdp_per_capita"], "GDP per Capita")
}

# Eğer durağan değilse, 1. fark al
veri_dunya["renewables_diff"] = veri_dunya["renewables_production_per_capita"].diff() if not stationary_vars["renewables_production_per_capita"] else veri_dunya["renewables_production_per_capita"]
veri_dunya["co2_diff"] = veri_dunya["co2_per_capita"].diff() if not stationary_vars["co2_per_capita"] else veri_dunya["co2_per_capita"]
veri_dunya["gdp_diff"] = veri_dunya["gdp_per_capita"].diff() if not stationary_vars["gdp_per_capita"] else veri_dunya["gdp_per_capita"]

# Eksik verileri temizle (fark alma sonrası NA oluşur)
veri_dunya = veri_dunya.dropna()

# Granger nedensellik testi
max_lag = 2
print("\nGranger Causality Tests for World:")
tests = [
    ("Renewables -> CO2", "co2_diff", "renewables_diff"),
    ("CO2 -> Renewables", "renewables_diff", "co2_diff"),
    ("GDP -> CO2", "co2_diff", "gdp_diff"),
    ("CO2 -> GDP", "gdp_diff", "co2_diff"),
    ("Renewables -> GDP", "gdp_diff", "renewables_diff"),
    ("GDP -> Renewables", "renewables_diff", "gdp_diff")
]

granger_results = []
for test_name, y, x in tests:
    print(f"\n{test_name}:")
    result = grangercausalitytests(veri_dunya[[y, x]], maxlag=max_lag, verbose=True)
    for lag in range(1, max_lag + 1):
        p_value = result[lag][0]["ssr_chi2test"][1]
        granger_results.append({
            "Test": test_name,
            "Lag": lag,
            "p-value": p_value,
            "Significant": p_value < 0.05
        })

# Granger sonuçlarını DataFrame'e çevir
granger_results_df = pd.DataFrame(granger_results)
print("\nGranger Test Results Summary:")
print(granger_results_df)

# Tüm ülkeler için veri hazırlığı (esnek görselleştirme için)
veri_tum = veri[veri["year"] >= 2000].copy()
veri_tum["renewables_production_per_capita"] = veri_tum["renewables_production"] / veri_tum["population"]
veri_tum["renewables_diff"] = veri_tum.groupby("Country Name")["renewables_production_per_capita"].diff()
veri_tum["co2_diff"] = veri_tum.groupby("Country Name")["co2_per_capita"].diff()
veri_tum["gdp_diff"] = veri_tum.groupby("Country Name")["gdp_per_capita"].diff()
veri_tum = veri_tum[["Country Name", "year", "renewables_diff", "co2_diff", "gdp_diff"]].dropna()

# Verileri kaydet
veri_dunya.to_csv("dunya_granger_veri.csv", index=False)
granger_results_df.to_csv("dunya_granger_results.csv", index=False)
veri_tum.to_csv("tum_ulkeler_granger_veri.csv", index=False)

# Görselleştirme: Dünya için zaman serileri
plt.figure(figsize=(12, 6))
plt.plot(veri_dunya["year"], veri_dunya["renewables_diff"], label="Renewables Diff")
plt.plot(veri_dunya["year"], veri_dunya["co2_diff"], label="CO2 Diff")
plt.plot(veri_dunya["year"], veri_dunya["gdp_diff"], label="GDP Diff")
plt.title("Dünya: Fark Alınmış Zaman Serileri (2000-2023)")
plt.xlabel("Yıl")
plt.ylabel("Değer")
plt.legend()
plt.savefig("dunya_granger_timeseries.png")
plt.close()

# Granger sonuçları için heatmap
plt.figure(figsize=(10, 6))
pivot_table = granger_results_df.pivot(index="Test", columns="Lag", values="p-value")
sns.heatmap(pivot_table, annot=True, cmap="RdYlGn_r", vmin=0, vmax=0.1)
plt.title("Dünya Granger Nedensellik Testi p-değerleri")
plt.savefig("dunya_granger_heatmap.png")
plt.close()