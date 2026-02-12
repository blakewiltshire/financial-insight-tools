# -------------------------------------------------------------------------------------------------
# 🔗 Correlation Visualisation — Heatmap & Overlay Display Scaffold (Platinum Canonical Build)
# -------------------------------------------------------------------------------------------------
# pylint: disable=import-error, wrong-import-position, wrong-import-order

"""
This module provides clean, simple visualisation for correlation matrices:
- Heatmap (correlation strength)
- Standardised overlay (multi-indicator visual comparison)
Fully compatible with the correlation_engine.py output.
"""

# -------------------------------------------------------------------------------------------------
# Third-party Libraries
# -------------------------------------------------------------------------------------------------
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# -------------------------------------------------------------------------------------------------
# Heatmap Visualisation Function
# -------------------------------------------------------------------------------------------------

def render_correlation_heatmap(corr_matrix, key_suffix="default"):
    """
    Render correlation matrix as interactive heatmap (Plotly based).

    Args:
        corr_matrix (pd.DataFrame): Correlation matrix from correlation_engine.py
        key_suffix (str): Unique Streamlit key for duplication safety
    """

    if corr_matrix is None or corr_matrix.empty:
        st.warning("No correlation matrix available for visualisation.")
        return

    labels = corr_matrix.columns.tolist()
    z_values = corr_matrix.values

    fig = go.Figure(data=go.Heatmap(
        z=z_values,
        x=labels,
        y=labels,
        colorscale='RdBu',
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation")
    ))

    fig.update_layout(
        title="Correlation Heatmap",
        xaxis_title="Indicators",
        yaxis_title="Indicators",
        width=600,
        height=600
    )

    st.plotly_chart(fig, use_container_width=False, key=f"heatmap_{key_suffix}")

# -------------------------------------------------------------------------------------------------
# Overlay Visualisation Function
# -------------------------------------------------------------------------------------------------

def render_standardised_overlay(df, key_suffix="default"):
    """
    Render standardised multi-indicator overlay plot.
    Expects harmonised monthly dataframe. Applies internal z-score standardisation.
    """

    if df is None or df.empty:
        st.warning("No data available for overlay visualisation.")
        return

    # Standardise via z-score
    standardised_df = (df - df.mean()) / df.std()

    fig = go.Figure()

    for column in standardised_df.columns:
        fig.add_trace(
            go.Scatter(
                x=standardised_df.index,
                y=standardised_df[column],
                mode='lines',
                name=column
            )
        )

    fig.update_layout(
        title="Standardised Overlay (Z-Score Normalised)",
        xaxis_title="Date",
        yaxis_title="Standardised Value (Z-Score)",
        legend_title="Indicators",
        width=900,
        height=500
    )

    st.plotly_chart(fig, use_container_width=False, key=f"overlay_{key_suffix}")

# -------------------------------------------------------------------------------------------------
# End of Correlation Visualisation Module
# -------------------------------------------------------------------------------------------------
