# Institutional Macro Yield Curve & Regime Dashboard

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B.svg)](https://streamlit.io/)

A professional-grade macro quantitative dashboard that models the sovereign yield curve structure, monitors recession signals via term spread inversions, and decomposes yield dynamics using Nelson-Siegel parametric fitting and Principal Component Analysis (PCA).

## Key Features

1. **Yield Curve Fitting (Nelson-Siegel Model)**: Non-linear optimization calibrating the term structure parameters ($\beta_0, \beta_1, \beta_2, \tau$) to fit discrete US Treasury yield points.
2. **Principal Component Analysis (PCA Decomposition)**: Factorization of yield movements into Level ($90\%+$ variance explained), Slope, and Curvature.
3. **Macro Recession Indicator**: Real-time tracking of the 10Y-13W Treasury spread for regime classification.
4. **Interactive Visualization**: Built with Streamlit and Plotly for quantitative exploration.

## Mathematical Architecture

### Nelson-Siegel Term Structure Model
$$y(\tau) = \beta_0 + \beta_1 \left( \frac{1 - e^{-\tau/\lambda}}{\tau/\lambda} \right) + \beta_2 \left( \frac{1 - e^{-\tau/\lambda}}{\tau/\lambda} - e^{-\tau/\lambda} \right)$$

Where:
* $\beta_0$: Long-term level factor
* $\beta_1$: Short-term slope factor
* $\beta_2$: Medium-term curvature factor
* $\lambda$: Decay parameter governing peak curvature position

---

## Quick Start

```bash
# Clone Repository
git clone [https://github.com/hanihiba/macro-yield-curve-dashboard.git](https://github.com/hanihiba/macro-yield-curve-dashboard.git)
cd macro-yield-curve-dashboard

# Install Dependencies
pip install -r requirements.txt

# Launch Dashboard
streamlit run app.py