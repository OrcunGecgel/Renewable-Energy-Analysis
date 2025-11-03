import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import seaborn as sns
import matplotlib.pyplot as plt

# Veriyi oku
veri = pd.read_csv("dunya_temiz_veri_tum_ulkeler.csv")

# Ülkeleri seç
ulkeler = ["Turkey", "Poland", "Mexico", "Indonesia", "Malaysia", "South Africa", "China", "Germany", "United States","Denmark","Finland","Belgium","France","Ireland","Sweden","Greece","Luxembourg","Portugal"]
veri_filtre = veri[veri["Country Name"].isin(ulkeler) & (veri["year"] >= 2000) & (veri["year"] <= 2023)].copy()

# Kişi başına yenilenebilir enerji üretimi hesapla
veri_filtre["renewables_production_per_capita"] = veri_filtre["renewables_production"] / veri_filtre["population"]

# Eksik verileri temizle
veri_filtre = veri_filtre.dropna(subset=["renewables_production_per_capita", "co2_per_capita", "gdp_per_capita"])


# CAGR hesaplama fonksiyonu
def hesapla_cagr(ilk_deger, son_deger, yil_sayisi):
    if ilk_deger == 0 or son_deger == 0 or np.isnan(ilk_deger) or np.isnan(son_deger):
        return np.nan
    return (son_deger / ilk_deger) ** (1 / yil_sayisi) - 1


# Ülke bazlı analiz
sonuclar = []
for ulke in ulkeler:
    ulke_veri = veri_filtre[veri_filtre["Country Name"] == ulke]

    # 2000 ve 2023 değerlerini al
    veri_2000 = ulke_veri[ulke_veri["year"] == 2000]
    veri_2023 = ulke_veri[ulke_veri["year"] == 2023]

    if not veri_2000.empty and not veri_2023.empty:
        renewables_2000 = veri_2000["renewables_production_per_capita"].iloc[0]
        renewables_2023 = veri_2023["renewables_production_per_capita"].iloc[0]
        co2_2000 = veri_2000["co2_per_capita"].iloc[0]
        co2_2023 = veri_2023["co2_per_capita"].iloc[0]

        # CAGR hesapla
        cagr_renewables = hesapla_cagr(renewables_2000, renewables_2023, 2023 - 2000)

        # CO2 değişimi
        co2_degisim = (co2_2023 - co2_2000) / co2_2000 * 100

        # Pearson korelasyonu
        corr_renew_gdp, _ = pearsonr(ulke_veri["renewables_production_per_capita"], ulke_veri["gdp_per_capita"])

        sonuclar.append({
            "Ülke": ulke,
            "Yenilenebilir CAGR (%)": cagr_renewables * 100,
            "CO2 Değişimi (%)": co2_degisim,
            "Yenilenebilir-GSYİH Korelasyonu": corr_renew_gdp
        })

# Sonuçları DataFrame'e çevir
sonuclar_df = pd.DataFrame(sonuclar)
print("\nÜlke Karşılaştırmaları:")
print(sonuclar_df)

# Sonuçları kaydet
sonuclar_df.to_csv("ulke_karsilastirmalari.csv", index=False)

# Görselleştirme
plt.figure(figsize=(12, 6))
sns.barplot(x="Ülke", y="Yenilenebilir CAGR (%)", data=sonuclar_df)
plt.title("Ülkeler Arası Yenilenebilir Enerji CAGR (2000-2023)")
plt.xticks(rotation=45)
plt.savefig("cagr_karsilastirma.png")
plt.close()

plt.figure(figsize=(12, 6))
sns.barplot(x="Ülke", y="CO2 Değişimi (%)", data=sonuclar_df)
plt.title("Ülkeler Arası CO2 Değişimi (2000-2023)")
plt.xticks(rotation=45)
plt.savefig("co2_karsilastirma.png")
plt.close()

plt.figure(figsize=(12, 6))
sns.barplot(x="Ülke", y="Yenilenebilir-GSYİH Korelasyonu", data=sonuclar_df)
plt.title("Yenilenebilir Enerji-GSYİH Korelasyonu (2000-2023)")
plt.xticks(rotation=45)
plt.savefig("korelasyon_karsilastirma.png")
plt.close()