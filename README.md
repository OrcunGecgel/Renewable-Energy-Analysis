# Global Renewable Energy, Economic Growth, and CO2 Emissions Analysis (2000-2023)

This repository contains the end-to-end data analysis project for my undergraduate thesis, "The Effects of Renewable Energy on Global Economic Growth and Carbon Emissions".

The project analyzes global panel data from 2000 to 2023 to quantify the impact of the renewable energy transition on two critical factors: economic growth (per capita GDP) and environmental sustainability (per capita CO2 emissions).

## 🛠️ Technical Stack

* **Data Analysis & Manipulation:** Python (Pandas, NumPy)
* **Statistical Modeling:** Statsmodels (Trend Analysis, Pearson/Spearman Correlation, Granger Causality Test)
* **Machine Learning:** Scikit-learn (K-Means Clustering)
* **Data Visualization:** Tableau, Matplotlib, Seaborn
* **Development Environment:** PyCharm IDE
* **Data Sources:** World Bank, Our World in Data (OWID)

---

## 🎯 Project Objectives & Research Questions

This analysis sought to answer the following questions:

1.  What are the global production trends for renewable energy (Solar, Wind, Hydro) from 2000-2023?
2.  Is there a statistically significant relationship between the rise in renewable energy consumption and per capita GDP?
3.  What is the statistical relationship between renewable energy adoption and per capita co2 emissions?
4.  Is there a causal relationship (in the Granger sense) between energy consumption, economic growth, and carbon emissions?
5.  Can countries be segmented into distinct groups based on their energy profiles and economic/environmental performance?

---

## 📈 Methodology / Workflow

This project followed a structured, end-to-end data analysis workflow:

1.  **Data Collection & Cleaning (Python):** Sourced panel data from the World Bank and OWID. Using `pandas`, I merged multiple datasets (population, GDP, $CO_2$, and 4+ energy types) by country and year. Handled missing values, standardized country names, and performed data type conversions.
2.  **Feature Engineering (Python):** Created new variables essential for the analysis, such as `Total_Renewable_Energy` (TWh) and `Per_Capita_Renewable_Energy` (kWh).
3.  **Trend Analysis (Python & Tableau):** Applied Linear Regression, Exponential Growth models, and Moving Averages to model and visualize the long-term trends for key variables.
4.  **Statistical Analysis (Python - Statsmodels):**
    * **Correlation:** Calculated **Pearson** (for linear) and **Spearman** (for monotonic) correlation matrices to measure the strength and direction of relationships between variables.
    * **Causality:** Implemented the **Granger Causality Test** on stationary data (checked via unit root tests like ADF) to determine if one time series is useful in forecasting another.
5.  **Machine Learning (Python - Scikit-learn):**
    * **Clustering:** Applied the **K-Means algorithm** to segment countries into four distinct clusters based on their energy, economic, and emissions profiles.
6.  **Strategic Analysis:** Conducted a **SWOT analysis** (Strengths, Weaknesses, Opportunities, Threats) for the global renewable energy sector.

---

## 💡 Key Findings & Insights

My analysis uncovered several critical insights into the global energy transition:

* **Exponential Growth:** Solar and Wind energy production have grown exponentially, with **Solar increasing by 11,536%** and **Wind by 7,391%** between 2000 and 2023.
* **Macro Trends:** During the same period, global per capita GDP *increased* by 140%, while per capita $CO_2$ emissions *decreased* by 17.24%.
* **The GDP-Energy Link:** A positive but **weak correlation** was found between total per capita renewable energy production and per capita GDP (Pearson $r=0.207$, Spearman $\rho=0.387$).
* **The $CO_2$-Energy Nuance:** Contrary to common assumptions, the correlation between total renewable production and $CO_2$ emissions was **not statistically significant** (Pearson $r=0.025$, Spearman $\rho=0.045$). This complex finding suggests that at a global scale, the current share of renewables is not yet the *primary* driver of emissions reduction.
* **The Critical Finding (Granger Causality):** The test revealed that **$CO_2$ emissions are a significant Granger cause of GDP** ($p=0.0201 < 0.05$). This indicates that environmental pressures and emissions levels have a statistically predictive impact on economic growth.
* **Country Clusters:** K-Means clustering successfully identified 4 distinct country profiles, such as "Cluster 1: High GDP, High YE, Low $CO_2$" (e.g., Denmark, Sweden, Germany).

## 📁 Repository Contents

* `/.py_scripts/`: Python scripts for data cleaning, trend analysis, country comparisons, and statistical testing.
* `/tableau_workbooks/`: The `.twbx` Tableau workbook files used to create the dashboards.
* `/data/`: The raw and cleaned `.csv` files used in the analysis.
* `Makale Son Hali.pdf`: The original undergraduate thesis (in Turkish) submitted for this project.
