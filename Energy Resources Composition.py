import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi oku
veri = pd.read_csv("dunya_temiz_veri_tum_ulkeler.csv")

# Ülkeleri seç
ulkeler = ["Turkey", "Poland", "Mexico", "Indonesia", "Malaysia", "South Africa", "China", "Germany", "United States","Denmark","Finland","Belgium","France","Ireland","Sweden","Greece","Luxembourg","Portugal","World"]
veri_filtre = veri[veri["Country Name"].isin(ulkeler) & (veri["year"].isin([2000, 2023]))].copy()

# Kaynak paylarını hesapla
veri_filtre["hydro_share"] = veri_filtre["hydro_electricity_generation_twh"] / veri_filtre["renewables_production"]
veri_filtre["solar_share"] = veri_filtre["solar_electricity_generation_twh"] / veri_filtre["renewables_production"]
veri_filtre["wind_share"] = veri_filtre["wind_electricity_generation_twh"] / veri_filtre["renewables_production"]
veri_filtre["other_share"] = veri_filtre["other_renewables_electricity_generation_twh"] / veri_filtre["renewables_production"]

# Eksik verileri temizle
veri_filtre = veri_filtre[["Country Name", "year", "hydro_share", "solar_share", "wind_share", "other_share"]].dropna()

# Veriyi kaydet
veri_filtre.to_csv("kaynak_kompozisyon.csv", index=False)

# Görselleştirme: 2023 için stacked bar grafiği
veri_2023 = veri_filtre[veri_filtre["year"] == 2023]
plt.figure(figsize=(12, 6))
veri_2023.set_index("Country Name")[["hydro_share", "solar_share", "wind_share", "other_share"]].plot(kind="bar", stacked=True)
plt.title("Ülkeler Arası Yenilenebilir Enerji Kaynak Payları (2023)")
plt.xlabel("Ülke")
plt.ylabel("Pay (%)")
plt.legend(["Hidro", "Güneş", "Rüzgar", "Diğer"])
plt.savefig("kaynak_kompozisyon_2023.png")
plt.close()