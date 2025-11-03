import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# Hata mesajlarını özelleştirmek için fonksiyon
def log_error(message):
    print(f"HATA: {message}")
    exit()

# Veriyi oku
try:
    veri = pd.read_csv("dunya_temiz_veri_tum_ulkeler.csv")
except FileNotFoundError:
    log_error("'dunya_temiz_veri_tum_ulkeler.csv' dosyası bulunamadı.")

# Veri özeti
print("Veri Seti Özeti:")
print(veri.info())
print("\nEksik Veri Oranı (Orijinal):")
print(veri[["renewables_production", "solar_electricity_generation_twh", "wind_electricity_generation_twh",
            "hydro_electricity_generation_twh", "other_renewables_electricity_generation_twh",
            "co2_per_capita", "gdp_per_capita", "population"]].isna().mean())

# Sıfır değer oranını kontrol et
print("\nSıfır Değer Oranı (Ham Veri):")
for col in ["solar_electricity_generation_twh", "wind_electricity_generation_twh",
            "hydro_electricity_generation_twh", "other_renewables_electricity_generation_twh"]:
    print(f"{col}: {(veri[col] == 0).mean():.4f}")

# Nüfus sıfır veya eksik olan satırları temizle
veri = veri[veri["population"] > 0].copy()

# Kişi başı metrikleri hesapla
try:
    veri["renewables_production_per_capita"] = veri["renewables_production"] / veri["population"]
    veri["solar_per_capita"] = veri["solar_electricity_generation_twh"] / veri["population"]
    veri["wind_per_capita"] = veri["wind_electricity_generation_twh"] / veri["population"]
    veri["hydro_per_capita"] = veri["hydro_electricity_generation_twh"] / veri["population"]
    veri["other_renewables_per_capita"] = veri["other_renewables_electricity_generation_twh"] / veri["population"]
except ZeroDivisionError:
    log_error("Nüfus sütununda sıfır değerler tespit edildi.")

# Eksik veri yönetimi
for col in ["renewables_production_per_capita", "solar_per_capita", "wind_per_capita",
            "hydro_per_capita", "other_renewables_per_capita"]:
    veri[col] = veri[col].fillna(0)
for col in ["co2_per_capita", "gdp_per_capita"]:
    veri[col] = veri.groupby("Country Name")[col].transform(lambda x: x.fillna(x.mean()))
    veri[col] = veri[col].fillna(veri[col].median())

# Eksik veri kontrolü
print("\nEksik Veri Oranı (Temizlendikten Sonra):")
print(veri[["renewables_production_per_capita", "solar_per_capita", "wind_per_capita",
            "hydro_per_capita", "other_renewables_per_capita", "co2_per_capita",
            "gdp_per_capita"]].isna().mean())

# Sıfır değer oranını kişi başı metriklerde kontrol et
print("\nSıfır Değer Oranı (Kişi Başı Metrikler):")
for col in ["renewables_production_per_capita", "solar_per_capita", "wind_per_capita",
            "hydro_per_capita", "other_renewables_per_capita"]:
    print(f"{col}: {(veri[col] == 0).mean():.4f}")

# Aykırı değer ve dağılım kontrolü
plt.figure(figsize=(12, 10))
veri[["renewables_production_per_capita", "solar_per_capita", "wind_per_capita",
      "hydro_per_capita", "other_renewables_per_capita", "co2_per_capita",
      "gdp_per_capita"]].hist(bins=30)
plt.tight_layout()
plt.close()

plt.figure(figsize=(12, 6))
sns.boxplot(data=veri[["renewables_production_per_capita", "solar_per_capita", "wind_per_capita",
                       "hydro_per_capita", "other_renewables_per_capita", "co2_per_capita",
                       "gdp_per_capita"]])
plt.xticks(rotation=45)
plt.close()

# Log dönüşümü
for col in ["gdp_per_capita", "renewables_production_per_capita", "hydro_per_capita"]:
    veri[f"log_{col}"] = np.log1p(veri[col])

# Korelasyon değişkenleri
korelasyon_degiskenleri = ["renewables_production_per_capita", "solar_per_capita",
                          "wind_per_capita", "hydro_per_capita",
                          "other_renewables_per_capita", "co2_per_capita",
                          "gdp_per_capita", "log_renewables_production_per_capita",
                          "log_hydro_per_capita", "log_gdp_per_capita"]

# Korelasyon matrislerini hesapla
pearson_korelasyon = veri[korelasyon_degiskenleri].corr(method="pearson")
spearman_korelasyon = veri[korelasyon_degiskenleri].corr(method="spearman")

# Standartlaştırılmış veri için korelasyon
scaler = StandardScaler()
scaled_data = scaler.fit_transform(veri[korelasyon_degiskenleri])
scaled_df = pd.DataFrame(scaled_data, columns=korelasyon_degiskenleri)
pearson_korelasyon_scaled = scaled_df.corr(method="pearson")

# Son yıl için korelasyon
son_yil = veri["year"].max()
son_yil_veri = veri[veri["year"] == son_yil]
pearson_korelasyon_son_yil = son_yil_veri[korelasyon_degiskenleri].corr(method="pearson")

# Güneş enerjisi üreten ülkeler için korelasyon
solar_veri = veri[veri["solar_electricity_generation_twh"] > 0]
pearson_korelasyon_solar = pd.DataFrame()  # Boş DataFrame, eğer veri yoksa
if not solar_veri.empty:
    pearson_korelasyon_solar = solar_veri[korelasyon_degiskenleri].corr(method="pearson")

# Tüm korelasyon matrislerini tek bir CSV'ye birleştir
korelasyon_sonuclari = []

# Matrisleri uzun formata dönüştür
def matris_to_long(matris, korelasyon_tipi):
    matris = matris.reset_index().melt(id_vars="index", var_name="Variable2", value_name="Correlation")
    matris.columns = ["Variable1", "Variable2", "Correlation"]
    matris["Correlation Type"] = korelasyon_tipi
    return matris

# Her matris için uzun format
korelasyon_sonuclari.append(matris_to_long(pearson_korelasyon, "Pearson"))
korelasyon_sonuclari.append(matris_to_long(spearman_korelasyon, "Spearman"))
korelasyon_sonuclari.append(matris_to_long(pearson_korelasyon_scaled, "Pearson Scaled"))
korelasyon_sonuclari.append(matris_to_long(pearson_korelasyon_son_yil, f"Pearson {son_yil}"))
if not pearson_korelasyon_solar.empty:
    korelasyon_sonuclari.append(matris_to_long(pearson_korelasyon_solar, "Pearson Solar"))

# Birleştir ve kaydet
korelasyon_sonuclari_df = pd.concat(korelasyon_sonuclari, ignore_index=True)
korelasyon_sonuclari_df.to_csv("korelasyon_sonuclari.csv", index=False)
print("Tüm korelasyon sonuçları 'korelasyon_sonuclari.csv' dosyasına kaydedildi.")

# Temizlenmiş veriyi kaydet
veri.to_csv("temizlenmis_veri.csv", index=False)
print("Temizlenmiş veri 'temizlenmis_veri.csv' dosyasına kaydedildi.")

# Tableau için öneriler
print("\nTableau Görselleştirme Önerileri:")
print("1. Heatmap: 'korelasyon_sonuclari.csv' yükleyin.")
print("   - Satır: Variable1, Sütun: Variable2, Renk/Metin: Correlation, Filtre: Correlation Type.")
print("2. Scatter Plot: 'temizlenmis_veri.csv' kullanın.")
print("   - X: log_gdp_per_capita, Y: log_renewables_production_per_capita, Boyut: population, Renk: co2_per_capita.")
print("3. Histogramlar: 'temizlenmis_veri.csv' ile solar_per_capita, wind_per_capita için dağılım analizi.")
print("4. Dashboard: Heatmap, scatter plot ve histogramları birleştirin, Correlation Type, yıl ve ülke filtreleri ekleyin.")