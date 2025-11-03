import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# Dosyayı oku
df = pd.read_csv("dunya_temiz_veri_tum_ulkeler.csv")

# Yıllık küresel toplamlar
global_trend = df.groupby('year', as_index=False).agg({
    'renewables_production': 'sum',
    'solar_electricity_generation_twh': 'sum',
    'wind_electricity_generation_twh': 'sum',
    'hydro_electricity_generation_twh': 'sum',
    'other_renewables_electricity_generation_twh': 'sum'
})

# Hareketli ortalama (3 yıllık)
global_trend['moving_avg'] = global_trend['renewables_production'].rolling(window=3).mean()

# Lineer regresyon
X = global_trend['year'].values.reshape(-1, 1)
y = global_trend['renewables_production'].values
model = LinearRegression().fit(X, y)
global_trend['linear_trend'] = model.predict(X)

# Üstel büyüme tahmini
log_y = np.log(y + 1e-6)
exp_model = LinearRegression().fit(X, log_y)
log_pred = exp_model.predict(X)
global_trend['exponential_trend'] = np.exp(log_pred)

# CSV olarak kaydet
global_trend.to_csv("kuresel_yenilenebilir_trend_analizi.csv", index=False)
