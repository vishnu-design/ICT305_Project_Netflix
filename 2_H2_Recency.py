#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 09:33:13 2025

@author: prabhanvishnu
"""

import streamlit as st
import plotly.express as px
from utils import load_netflix_data

st.set_page_config(page_title="H2: Recency", layout="wide")
st.title("H2: Recency of Content")
st.markdown("""
**Hypothesis 2:** Netflix's recent success (market share gains) is tied to a greater proportion of newly released, timely content in its catalog compared to older licensed material.
""")

# --- Load Data ---
df = load_netflix_data()

if df.empty:
    st.error("Netflix data could not be loaded for Hypothesis 2.")
else:
    st.header("Storyboard and Visualizations (Plotly Advanced)")
    
    # --- Viz 1: Interactive Histogram of Release Year ---
    st.subheader("Interactive Distribution of Content by Release Year")
    st.markdown("Use the slider or brush tool to zoom in on specific years. The plot shows the raw volume of titles added across decades.")
    
    # Filter out years that are clearly incorrect (e.g., pre-1900)
    df_filtered = df[df['release_year'] > 1920]

    # Plotly Histogram
    fig_hist = px.histogram(
        df_filtered, 
        x='release_year', 
        nbins=max(df_filtered['release_year']) - min(df_filtered['release_year']) + 1,
        title="Netflix Content Volume by Release Year",
        labels={'release_year': 'Release Year', 'count': 'Number of Titles Released'},
        height=400
    )
    # Update layout for better interactivity and label clarity
    fig_hist.update_layout(xaxis_title="Release Year", yaxis_title="Number of Titles", bargap=0.05)
    fig_hist.update_xaxes(rangeselector=dict(
        buttons=list([
            dict(count=10, label="10y", step="year", stepmode="backward"),
            dict(count=5, label="5y", step="year", stepmode="backward"),
            dict(step="all")
        ])
    ))

    st.plotly_chart(fig_hist, use_container_width=True)
    
    st.markdown("---")
    
    # --- Viz 2: Donut Chart for Recency Split (Before/After 2015) ---
    st.subheader("Market Split: Content Released Before vs. After 2015")
    st.markdown("This visualization quantifies the hypothesis that recent content ('After 2015') constitutes the majority of Netflix's catalog.")
    
    period_counts = df['period'].value_counts().reset_index()
    period_counts.columns = ['Period', 'Count']

    # Plotly Donut Chart (Pie with hole)
    fig_donut = px.pie(
        period_counts, 
        values='Count', 
        names='Period', 
        title='Proportion of Netflix Content by Release Period (Cutoff: 2015)',
        hole=0.4,
        color='Period',
        color_discrete_map={'After 2015':'#E50914', 'Before/On 2015':'#A3A3A3'} # Netflix Red and Grey
    )
    fig_donut.update_traces(textinfo='percent+label', marker=dict(line=dict(color='#000000', width=1)))
    st.plotly_chart(fig_donut, use_container_width=True)

    # --- Observations ---
    st.header("Observations")
    st.markdown("""
    The **Interactive Histogram** clearly shows a dramatic surge in content volume starting around **2014-2015**, which aligns with Netflix's aggressive expansion into original content.
    
    The **Donut Chart** confirms the split: the majority of the current Netflix catalog was released in the period **After 2015**, validating the hypothesis that recent, timely content is a core strategic focus.
    """)