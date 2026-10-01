import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from src.data_loader import fetch_yield_curve_data
from src.models import fit_nelson_siegel, nelson_siegel, compute_yield_curve_pca

st.set_page_config(page_title="Macro Yield Curve & Regime Analytics", layout="wide")

st.title("Institutional Macro Yield Curve Dashboard")
st.markdown("---")

# Charger les données
@st.cache_data
def load_data():
    return fetch_yield_curve_data()

data = load_data()

# Sidebar Settings
st.sidebar.header("Parameters & Filters")
selected_date = st.sidebar.date_input("Select Date for Curve Fitting", value=data.index[-1])

# Layout Principal : 2 Colonnes
col1, col2 = st.columns(2)

with col1:
    st.subheader("10Y - 13W Yield Spread & Inversion Signals")
    fig_spread = go.Figure()
    fig_spread.add_trace(go.Scatter(x=data.index, y=data['Spread_10Y_13W'], name="Spread 10Y-13W", line=dict(color='royalblue')))
    fig_spread.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Recession Risk Threshold (Inversion)")
    fig_spread.update_layout(template="plotly_dark", height=400, xaxis_title="Date", yaxis_title="Spread (%)")
    st.plotly_chart(fig_spread, use_container_width=True)

with col2:
    st.subheader("Nelson-Siegel Parametric Yield Curve Fitting")
    
    try:
        closest_date = data.index.get_indexer([pd.to_datetime(selected_date)], method='nearest')[0]
        row_data = data.iloc[closest_date]
        
        obs_maturities = np.array([0.25, 5.0, 10.0, 30.0])
        obs_yields = np.array([row_data['13W'], row_data['5Y'], row_data['10Y'], row_data['30Y']])
        
        params = fit_nelson_siegel(obs_maturities, obs_yields)
        dense_maturities = np.linspace(0.1, 30.0, 100)
        fitted_curve = nelson_siegel(dense_maturities, *params)

        fig_ns = go.Figure()
        fig_ns.add_trace(go.Scatter(x=obs_maturities, y=obs_yields, mode='markers', name='Observed Yields', marker=dict(size=10, color='gold')))
        fig_ns.add_trace(go.Scatter(x=dense_maturities, y=fitted_curve, mode='lines', name='Nelson-Siegel Fit', line=dict(color='crimson', width=2)))
        fig_ns.update_layout(template="plotly_dark", height=400, xaxis_title="Maturity (Years)", yaxis_title="Yield (%)")
        st.plotly_chart(fig_ns, use_container_width=True)
    except Exception as e:
        st.error(f"Error fitting Nelson-Siegel curve: {e}")

# Section PCA
st.markdown("---")
st.subheader("Yield Curve PCA Dynamics (Level, Slope, Curvature)")

factors_df, exp_var = compute_yield_curve_pca(data)

st.write(f"**Explained Variance Ratio:** PC1 (Level): `{exp_var[0]*100:.1f}%` | PC2 (Slope): `{exp_var[1]*100:.1f}%` | PC3 (Curvature): `{exp_var[2]*100:.1f}%`")

fig_pca = go.Figure()
fig_pca.add_trace(go.Scatter(x=factors_df.index, y=factors_df['Level (PC1)'], name="Level (PC1)", line=dict(color='cyan')))
fig_pca.add_trace(go.Scatter(x=factors_df.index, y=factors_df['Slope (PC2)'], name="Slope (PC2)", line=dict(color='orange')))
fig_pca.add_trace(go.Scatter(x=factors_df.index, y=factors_df['Curvature (PC3)'], name="Curvature (PC3)", line=dict(color='magenta')))
fig_pca.update_layout(template="plotly_dark", height=400, xaxis_title="Date", yaxis_title="Factor Score")
st.plotly_chart(fig_pca, use_container_width=True)