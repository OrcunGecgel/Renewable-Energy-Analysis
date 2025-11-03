import pandas as pd

# Verileri okuma
nufus = pd.read_csv(r"C:\Users\Saydof\Desktop\API_SP.POP.TOTL_DS2_en_csv_v2_85220.csv", skiprows=4)  # Nüfus
yenilenebilir = pd.read_csv(r"C:\Users\Saydof\Desktop\modern-renewable-energy-consumption.csv")  # Yenilenebilir enerji üretimi
co2_per_capita = pd.read_csv(r"C:\Users\Saydof\Desktop\co-emissions-per-capita.csv")  # CO2 emisyonları
gdp_per_capita = pd.read_csv(r"C:\Users\Saydof\Desktop\API_NY.GDP.PCAP.PP.CD_DS2_en_csv_v2_85176.csv", skiprows=4)  # GSYİH

# Yılları belirleme
yillar = [str(yil) for yil in range(2000, 2024)]

# Ülke isimlerini standart hale getir
nufus["Country Name"] = nufus["Country Name"].replace({"Turkiye": "Turkey", "Türkiye": "Turkey"})
yenilenebilir["Entity"] = yenilenebilir["Entity"].replace({"Russia": "Russian Federation"})
co2_per_capita["Entity"] = co2_per_capita["Entity"].replace({"Russia": "Russian Federation"})
gdp_per_capita["Country Name"] = gdp_per_capita["Country Name"].replace({"Turkiye": "Turkey", "Türkiye": "Turkey"})

# Nüfus verisini düzenleme
nufus = nufus[["Country Name"] + yillar]
nufus = nufus.melt(id_vars=["Country Name"], var_name="year", value_name="population")
nufus["year"] = nufus["year"].astype(int)

# Yenilenebilir enerji üretimini düzenleme
yenilenebilir["renewables_production"] = (
    yenilenebilir["other_renewables_electricity_generation_twh"].fillna(0) +
    yenilenebilir["solar_electricity_generation_twh"].fillna(0) +
    yenilenebilir["wind_electricity_generation_twh"].fillna(0) +
    yenilenebilir["hydro_electricity_generation_twh"].fillna(0)
)
yenilenebilir = yenilenebilir[yenilenebilir["Year"].isin(range(2000, 2024))][
    ["Entity", "Year", "renewables_production", "solar_electricity_generation_twh",
     "wind_electricity_generation_twh", "hydro_electricity_generation_twh",
     "other_renewables_electricity_generation_twh"]
]
yenilenebilir = yenilenebilir.rename(columns={"Entity": "Country Name", "Year": "year"})
yenilenebilir = yenilenebilir.fillna(0)

# CO2 emisyonlarını düzenleme
co2_per_capita = co2_per_capita[co2_per_capita["Year"].isin(range(2000, 2024))][["Entity", "Year", "emissions_total_per_capita"]]
co2_per_capita = co2_per_capita.rename(columns={"Entity": "Country Name", "Year": "year", "emissions_total_per_capita": "co2_per_capita"})

# GSYİH verisini düzenleme
gdp_per_capita = gdp_per_capita[["Country Name"] + yillar]
gdp_per_capita = gdp_per_capita.melt(id_vars=["Country Name"], var_name="year", value_name="gdp_per_capita")
gdp_per_capita["year"] = gdp_per_capita["year"].astype(int)

# Verileri birleştirme
veri = nufus.merge(yenilenebilir, on=["Country Name", "year"], how="inner")
veri = veri.merge(co2_per_capita, on=["Country Name", "year"], how="inner")
veri = veri.merge(gdp_per_capita, on=["Country Name", "year"], how="inner")

# Eksik verileri doldurma
for col in ["renewables_production", "solar_electricity_generation_twh", "wind_electricity_generation_twh",
            "hydro_electricity_generation_twh", "other_renewables_electricity_generation_twh",
            "co2_per_capita", "gdp_per_capita", "population"]:
    veri[col] = veri.groupby("Country Name")[col].transform(lambda x: x.fillna(x.mean()))
veri = veri.fillna(0)

# Veriyi kaydetme
veri.to_csv("dunya_temiz_veri_tum_ulkeler.csv", index=False)
print("Tüm ülkeler için veri birleştirme tamamlandı: 'dunya_temiz_veri_tum_ulkeler.csv'")