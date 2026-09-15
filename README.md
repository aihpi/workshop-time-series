<div style="background-color: #ffffff; color: #000000; padding: 30px;">
    <p style="text-align:right;"><img src="./media/images/kisz_logo.png" alt="kisz logo" width="192" height="69" style="margin-right: 30px; margin-bottom:30px;"></p>
    <p style="text-align:center;"><img src="./media/images/mooc_image.png" alt="mooc image" width="628" height="390"></p>
    <h1 style="text-align:center;"> Time Series Analysis and Forecasting </h1>
</div>

In this repository, you'll find code and resources for the OpenHPI course [Time Series Analysis and Forecasting](https://open.hpi.de/courses/timeseries2025).

---

**IMPORTANT**: As the content is going to be appearing gradually, we recommend you to work in a development branch, for avoiding conflicts when pulling new code.  

---

**Current version of the materials**:

- Code v1.0.0
- Presentation Slides v1.0.0
- Extra resources: v1.0.0

---

## Course Structure

0. [Practical Introduction to the Course](./notebooks/00_Practical_Introduction.ipynb)

### Part A: Foundations & Data Exploration

1. [Loading and manipulating the data](./notebooks/A01_Loading_data.ipynb)
2. [Visualizing time series](./notebooks/A02_Basic_plotting.ipynb)
3. [Handling Missing Data](./notebooks/A03_Handling_missing_data.ipynb)
4. [Handling Outliers](./notebooks/A04_Handling_outliers.ipynb)
5. [Forecasting Baselines](./notebooks/A05_Forecasting_baselines.ipynb)
6. [Evaluating Models](./notebooks/A06_Evaluating_models.ipynb)

### Part B: Statistical Forecasting

1. [Exponential Smoothing Models](./notebooks/B01_Exponential_smoothing_models.ipynb)
2. [ARIMA Family Models](./notebooks/B02_ARIMA_models.ipynb)
3. [Advanced Statistical Methods](./notebooks/B03_Advanced_statistical_models.ipynb)
4. [Probabilistic Forecasting](./notebooks/B04_Probabilistic_forecasting.ipynb)

### Part C: Machine Learning Approaches

1. [Feature Engineering for ML Forecasting](./notebooks/C01_Feature_engineering.ipynb)
    - Generate lag features, rolling statistics, Fourier terms, calendar features.
    - Explore feature importances with tree models.

2. [ML Models for Forecasting](./notebooks/C02_Machine_learning_models.ipynb)
    - Compare linear regression, random forests, gradient boosting on time series regression tasks.
    - Discuss limitations of ML vs statistical baselines.
3. [Ensembles and Model Combinations](./notebooks/C03_Ensembles.ipynb)
    - Weighted averaging, stacking simple ARIMA + RF + XGBoost.
    - Show how ensembling improves robustness.

### Part D: Deep Learning Approaches

1. Intro to Neural Networks for Time Series
    - Train a simple feed-forward NN on lagged features.
    - Compare with linear regression baseline.
2. RNNs (LSTM, GRU)
    - Forecast univariate time series with LSTM/GRU.
    - Show sequence-to-sequence architecture.
3. CNNs for Time Series
    - Use 1D convolutions for forecasting.
    - Compare receptive fields with RNN.
4. Transformers for Time Series
    - Build a simple attention-based model.
    - Forecast using a pretrained framework (e.g., PyTorch Forecasting or Darts).
5. State-of-the-Art Architectures
    - Experiment with N-BEATS, N-HiTS, Autoformer (using an existing library like NeuralForecast or Darts).
    - Benchmark against traditional methods.

### Part E: Wrap-Up & Integration

1. End-to-End Forecasting Pipeline
    - Data prep, feature engineering, baseline models, advanced models, evaluation.
    - Case study on a real dataset (e.g., electricity demand or M4 competition dataset).

### Part F: Appendices

1. [Using the datasets](./notebooks/F01_Using_the_datasets.ipynb)
    - Overview of every dataset used in the course, and where each one comes from.
    - [Preparing the OPS datasets](./notebooks/F01a_Preparing_OPS_datasets.ipynb)
    - [Preparing the CDC dataset](./notebooks/F01b_Preparing_CDC_dataset.ipynb)
    - [Preparing the external datasets](./notebooks/F01c_Preparing_external_datasets.ipynb)

---

## Documentation

In progress

...

## Installation

You can find instructions on how to use these materials [here](./notebooks/00_Practical_Introduction.ipynb).

## FAQ

We are going to collect the most interesting questions from the course and their answers in this [FAQ](FAQ.md).

## Contributing

Contributions are always welcome!

See [`contributing.md`](contributing.md) for ways to get started.

Please adhere to this project's [`code of conduct`](CODE_OF_CONDUCT.md).

## Roadmap

- ...

## Authors

- [Mario Tormo Romero](https://github.com/mt0rm0)

## License

[GNU GENERAL PUBLIC LICENSE, V.3](LICENSE)