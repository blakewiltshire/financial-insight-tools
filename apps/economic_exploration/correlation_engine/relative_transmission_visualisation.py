# -------------------------------------------------------------------------------------------------
# Relative Transmission Visualisation
# -------------------------------------------------------------------------------------------------

import streamlit as st
import plotly.graph_objects as go


def render_overlay(df):
    fig = go.Figure()

    standardised = (df - df.mean()) / df.std()

    for col in standardised.columns:
        fig.add_trace(go.Scatter(
            x=standardised.index,
            y=standardised[col],
            mode="lines",
            name=col
        ))

    fig.update_layout(
        title="Standardised Overlay",
        height=500
    )

    st.plotly_chart(fig)


def render_derived_metric(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["derived_metric"],
        mode="lines",
        name="Derived Metric"
    ))

    fig.update_layout(
        title="Derived Metric",
        height=500
    )

    st.plotly_chart(fig)


def render_rolling_panel(df):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["rolling_correlation"],
        mode="lines",
        name="Rolling Correlation"
    ))

    fig.update_layout(
        title="Rolling Transmission",
        height=500
    )

    st.plotly_chart(fig)
