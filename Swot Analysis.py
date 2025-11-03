import pandas as pd

# SWOT verisi
swot_data = [
    {"Kategori": "Güçlü Yönler", "Detay": "Yüksek hidroelektrik kapasitesi (2023: 63.85 TWh)"},
    {"Kategori": "Güçlü Yönler", "Detay": "Güneş ve rüzgar potansiyeli (güneş: 20.52 TWh, rüzgar: 34.07 TWh)"},
    {"Kategori": "Güçlü Yönler", "Detay": "YEKDEM teşvikleri"},
    {"Kategori": "Güçlü Yönler", "Detay": "Avrupa-Asya enerji merkezi potansiyeli"},
    {"Kategori": "Zayıf Yönler", "Detay": "Fosil yakıt bağımlılığı (CO2: 4.95 ton/kişi)"},
    {"Kategori": "Zayıf Yönler", "Detay": "Yüksek finansman maliyetleri"},
    {"Kategori": "Zayıf Yönler", "Detay": "Teknolojik ithalat bağımlılığı"},
    {"Kategori": "Zayıf Yönler", "Detay": "Bürokratik gecikmeler"},
    {"Kategori": "Fırsatlar", "Detay": "AB Yeşil Mutabakatı ile ihracat avantajı"},
    {"Kategori": "Fırsatlar", "Detay": "Yeşil hidrojen pilot projeleri"},
    {"Kategori": "Fırsatlar", "Detay": "Uluslararası fonlar (EBRD, Dünya Bankası)"},
    {"Kategori": "Fırsatlar", "Detay": "Yerli teknoloji üretimi için AR-GE"},
    {"Kategori": "Tehditler", "Detay": "İklim değişikliği ve su kaynaklarında azalma"},
    {"Kategori": "Tehditler", "Detay": "Geopolitik riskler"},
    {"Kategori": "Tehditler", "Detay": "Çin ve Avrupa’dan rekabet"},
    {"Kategori": "Tehditler", "Detay": "Politika belirsizliği"}
]

# Politika önerileri
politika_data = [
    {"Kategori": "Politika", "Detay": "Düşük faizli krediler ve uluslararası fonlar"},
    {"Kategori": "Politika", "Detay": "Güneş/rüzgar teknolojisi için AR-GE teşvikleri"},
    {"Kategori": "Politika", "Detay": "İzin süreçleri için dijital platformlar"},
    {"Kategori": "Politika", "Detay": "Karbon vergisi uygulaması"},
    {"Kategori": "Politika", "Detay": "Mesleki eğitim programları"},
    {"Kategori": "Politika", "Detay": "Yeşil hidrojen pilot projeleri"}
]

# Birleştir ve kaydet
swot_politika_df = pd.DataFrame(swot_data + politika_data)
swot_politika_df.to_csv("swot_politika.csv", index=False)

# Basit bir metin tablosu görselleştirme
print("\nSWOT ve Politika Analizi:")
print(swot_politika_df)