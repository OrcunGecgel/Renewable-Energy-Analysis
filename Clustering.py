import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# Veriyi oku
veri = pd.read_csv("dunya_temiz_veri_tum_ulkeler.csv")

# 2023 verisini seç
veri_2023 = veri[veri["year"] == 2023].copy()

# Kişi başına yenilenebilir enerji üretimi hesapla
veri_2023["renewables_production_per_capita"] = veri_2023["renewables_production"] / veri_2023["population"]

# Değişkenleri seç
X = veri_2023[["renewables_production_per_capita", "co2_per_capita", "gdp_per_capita"]].dropna()

# Veriyi standardize et
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-means kümeleme
kmeans = KMeans(n_clusters=4, random_state=42)
veri_2023.loc[X.index, "cluster"] = kmeans.fit_predict(X_scaled)

# Sonuçları kaydet
veri_2023[["Country Name", "renewables_production_per_capita", "co2_per_capita", "gdp_per_capita", "cluster"]].to_csv("kumeleme_sonuclari.csv", index=False)

# Görselleştirme: Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=veri_2023, x="renewables_production_per_capita", y="co2_per_capita", hue="cluster", size="gdp_per_capita", sizes=(50, 500))
plt.title("Ülkelerin Kümeleme Analizi (2023)")
plt.xlabel("Yenilenebilir Enerji (Kişi Başına)")
plt.ylabel("CO2 Emisyonları (Kişi Başına)")
plt.savefig("kumeleme_scatter.png")
plt.close()