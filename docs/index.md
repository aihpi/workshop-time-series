# Time Series Analysis and Forecasting

Code and resources for the OpenHPI course
[Time Series Analysis and Forecasting](https://open.hpi.de/courses/timeseries2025), taught by the
KI-Servicezentrum Berlin-Brandenburg at the Hasso Plattner Institute.

The course is a sequence of Jupyter notebooks. They are the material, and this site is the map around
them: how to set the environment up, what each part covers, where the datasets come from, and how to
maintain the repository if you are contributing to it.

:::{note}
The notebooks themselves are not rendered here. They are large, several take many minutes to execute, and
they are meant to be run rather than read. Every link on this site goes to the notebook on GitHub, where
it renders and can be downloaded.
:::

## Start here

If you are taking the course, you need two things and then you can begin:

1. **[Set up the environment](setup.md)** — Python, `uv`, and the editor.
2. **[Download the datasets](_generated/datasets.md)** — three of the appendix notebooks do this for you.

Then open `notebooks/00_Practical_Introduction.ipynb` and work forward.

## What the course covers

The eighteen teaching notebooks divide into five parts, each building on the last. Fifty exercises are
spread across them, and every one has a worked solution in
[`solutions/`](https://github.com/aihpi/workshop-time-series/blob/main/solutions/).

:::{list-table}
:header-rows: 1
:widths: 12 30 58

* - Part
  - Subject
  - What you come away with
* - **A**
  - Foundations and data exploration
  - Loading and plotting a series, handling gaps and outliers, building baselines that are hard to beat,
    and evaluating a forecast in a way that will not mislead you.
* - **B**
  - Statistical forecasting
  - Exponential smoothing, the ARIMA family, dynamic harmonic regression and Prophet, and forecasting a
    distribution rather than a point.
* - **C**
  - Machine learning approaches
  - Turning a sequence into a feature matrix without letting the future in, gradient boosting and random
    forests, and combining models.
* - **D**
  - Deep learning approaches
  - Neural network foundations, recurrent and convolutional architectures, transformers, and the
    specialised forecasting models that beat all of them here.
* - **E**
  - Wrap-up and integration
  - The whole sequence on one problem, including what happens when the world changes underneath a
    deployed model.
:::

Part F is an appendix documenting the datasets and downloading them.

## For contributors

```{toctree}
:maxdepth: 2

setup
_generated/datasets
_generated/faq
_generated/contributing
maintenance
api
```
