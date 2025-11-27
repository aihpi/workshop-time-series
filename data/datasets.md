# Datasets

This document provides an overview of the datasets prepared for this course, along with additional external datasets that may be useful for extended learning, projects, or research.

---

## Prepared datasets

The following datasets have been prepared for this course and are **hosted on Hugging Face**. They are not included in this repository; you can download them directly as needed.

<!-- start:prepared-datasets -->
| Dataset Name | Domain | Link | Description |
| ------------ | ------ | ---- | ----------- |
| `ops_data_15m.parquet` | Energy | [Link](https://huggingface.co/datasets/mt0rm0/opsdata) | Electricity Consumption Data for some European Countries, Freq 15min - Source: ENTSO-E Transparency Platform |
| `ops_data_30m.parquet` | Energy | [Link](https://huggingface.co/datasets/mt0rm0/opsdata) | Electricity Consumption Data for some European Countries, Freq 30min - Source: ENTSO-E Transparency Platform |
| `cdc_monthly_regional_air_temp_D` | Climate | [Link](https://huggingface.co/datasets/mt0rm0/cdcdata) | Regional monthly air Temperature in Germany - Source: Deutscher Wetterdienst|
<!-- end:prepared-datasets -->


📌 **Usage Notes**
  
- All datasets are stored in **Parquet format**, which allows efficient reading and storage.  
- You can use **`pandas.read_parquet(<filename>)`** to load them directly in your notebooks.  

---

## Additional Relevant Datasets

The following datasets were not prepared for this course, but cover different fields and may be useful for you.  

<!-- start:additional-datasets -->
| Dataset Name | Domain | Link | Notes |
| ------------ | ------ | ---- | ----- |
| **International Airline Passengers**       | Transportation   | [Kaggle](https://www.kaggle.com/datasets/andreazzini/international-airline-passengers)        | Monthly totals of international airline passengers from 1949 to 1960. A classic dataset for demonstrating ARIMA and other time series models.                   |
| **Air Quality**            | Environment   | [UCI](https://archive.ics.uci.edu/dataset/387/air%2Bquality)         | Hourly responses from a chemical multisensor device in an Italian city (2004–2005). Contains sensor outliers, ideal for practicing anomaly detection. |
| **Sunspot Numbers**                        | Astronomy        | [SIDC](https://www.sidc.be/SILSO/datafiles)                                      | Daily and monthly sunspot numbers, useful for modeling long-term cyclic phenomena. Data version 2.0 is the most recent.                                         |
| **Individual Household Electric Power Consumption** | Energy / Utilities | [UCI](https://archive.ics.uci.edu/dataset/27/individual+household+electric+power+consumption) | Minute-level measurements of electric power consumption from a single household located in Sceaux (7km of Paris, France) between 2006 and 2010. Contains missing values and occasional spikes, ideal for practicing cleaning, resampling, and anomaly detection. |
| **Daily Minimum Temperatures (Melbourne)** | Weather          | [Kaggle](https://www.kaggle.com/datasets/paulbrabban/daily-minimum-temperatures-in-melbourne) | Daily minimum temperatures in Melbourne from 1981 to 1990. Ideal for univariate seasonal forecasting tasks.                                                     |
| **Rossmann Store Sales**                   | Retail           | [Kaggle](https://www.kaggle.com/competitions/rossmann-store-sales)                            | Daily sales data for 1,115 Rossmann stores, including features like promotions and holidays. A comprehensive dataset for multivariate forecasting.   |
| **Exchange Rates Dataset**                 | Finance          | [Kaggle](https://www.kaggle.com/datasets/federalreserve/exchange-rates)                       | Daily exchange rates between the US dollar and 23 other currencies, based on the Federal Reserve's H.10 statistical release.                                    |
| **PJM Hourly Energy Consumption**          | Energy           | [Kaggle](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)                | Hourly power consumption data from the PJM Interconnection, spanning over 10 years. Includes data for multiple regions, useful for energy demand forecasting.   |
| **COVID-19 Global Time Series**            | Health           | [Github/Johns Hopkins CSSE](https://github.com/CSSEGISandData/COVID-19)                              | Time series data tracking the number of COVID-19 cases, deaths, and recoveries worldwide. Includes data by country and region.                                  |
| **M4 Forecasting Competition Dataset**     | Multiple Domains | [Kaggle](https://www.kaggle.com/datasets/yogesh94/m4-forecasting-competition-dataset)                                      | A large collection of 100,000 time series across various domains, including finance, demographics, and industry. Designed for benchmarking forecasting methods. |
<!-- end:additional-datasets -->

**Tips for Using External Datasets**

- Always check the **license** and **terms of use** before downloading.  
- Some datasets may require **registration** or **API keys**.  
- Consider preprocessing steps (cleaning, anonymization, feature extraction) to make them compatible with the course code.  

---

## Contributing
If you discover additional datasets that could be relevant for this course, feel free to suggest them via a pull request or by opening an issue in this repository.