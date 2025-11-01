#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 09:31:47 2025

@author: prabhanvishnu
"""

import streamlit as st
import plotly.express as px
from utils import load_platform_comparison_data

st.set_page_config(page_title="H1: Local Language", layout="wide")
st.title("H1: Local-Language Representation and Market Share")
st.markdown("""
**Hypothesis 1:** In a local market with high OTT platform saturation, if Netflix maintains a competitive local-language title ratio compared to its main rivals, it will realize superior gains in market share.
""")

# --- Load Data ---
df = load_platform_comparison_data()

if df.empty:
    st.error("Data could not be loaded for H1. Please ensure you have renamed and uploaded all 6 platform files (e.g., 'apple_tv_titles.csv', 'hbo_titles.csv', etc.).")
else:
    st.header("Storyboard and Visualizations")
    
    # --- Storyboard: Beginning ---
    st.subheader("Beginning: Competitive Context (6 Platforms)")
    st.markdown("We use **'Non-U.S.' content as a proxy for 'local-language' content** to create a standardized comparison metric across all platforms.")

    col1, col2 = st.columns(2)
    
    # Viz 1: Total Catalog Size
    with col1:
        total_titles = df['platform'].value_counts().reset_index()
        fig_total = px.bar(
            total_titles.sort_values('count', ascending=False), 
            x='platform', 
            y='count', 
            title="Total Catalogue Size by Platform",
            labels={'count': 'Total Titles', 'platform': 'Platform'},
            color='platform'
        )
        st.plotly_chart(fig_total, use_container_width=True)

    # Viz 2: Overall Local-Language Ratio
    with col2:
        ratio_df = df.groupby('platform')['is_local'].mean().reset_index()
        ratio_df['local_ratio'] = ratio_df['is_local'] * 100
        fig_ratio = px.bar(
            ratio_df.sort_values('local_ratio', ascending=False), 
            x='platform', 
            y='local_ratio', 
            title="Percentage of Local (Non-U.S.) Titles",
            labels={'local_ratio': 'Local-Language Ratio (%)', 'platform': 'Platform'},
            color='platform'
        )
        st.plotly_chart(fig_ratio, use_container_width=True)
    
    # --- Storyboard: Middle & End ---
    st.subheader("Middle & End: Exploration of Trends")
    st.markdown("A line chart visualizes how each platform’s local-language ratio evolved, showing strategic shifts over time.")
    
    # Filter data for relevance
    trend_df = df[df['release_year'].between(2010, 2023)]
    
    # Viz 3: Localization Trend Over Time
    trend_agg = trend_df.groupby(['platform', 'release_year'])['is_local'].mean().reset_index()
    trend_agg['local_ratio'] = trend_agg['is_local'] * 100
    
    fig_trend = px.line(
        trend_agg,
        x="release_year",
        y="local_ratio",
        color="platform",
        markers=True,
        title="Localization Ratio (Non-U.S. Content) Over Time (Post-2010)",
        labels={"release_year": "Release Year", "local_ratio": "Local-Language Ratio (%)"}
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # --- Observations ---
    st.header("Observations")
    st.markdown("""
    This analysis now incorporates **six major platforms**. 
    
    * **Crunchyroll** is expected to be an outlier with an extremely high Non-U.S. ratio.
    * The line chart is critical for showing which platforms (like Netflix and Amazon Prime) are investing most aggressively in Non-U.S. content to fuel international growth.
    """)