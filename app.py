#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 09:28:16 2025

@author: prabhanvishnu
"""

import streamlit as st
import pandas as pd
from utils import load_netflix_data

st.set_page_config(
    page_title="Strategic Analysis of OTT Platforms",
    page_icon="🎬",
    layout="wide"
)

# Load data once to check availability and prime the cache
df = load_netflix_data()

st.title("Strategic Analysis of OTT Platforms")
st.markdown("""
A data-driven dashboard analyzing Netflix's content strategy based on three core hypotheses:

1.  **Local Language & Market Share (H1):** Comparison of localization efforts across 6 major platforms.
2.  **Recency of Content (H2):** Analysis of content age distribution (Plotly Histogram/Donut).
3.  **International Growth (H3):** Geographic breakdown of non-U.S. content sourcing (Plotly Choropleth Map/Treemap).
""")

st.subheader("How to Navigate")
st.markdown("""
Use the sidebar on the left to select the analysis for each Hypothesis.
""")

if df.empty:
    st.error("Please ensure 'netflix_titles (1).csv' and all other required data files are in the main directory.")