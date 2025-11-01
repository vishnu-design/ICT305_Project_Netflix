#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 09:33:46 2025

@author: prabhanvishnu
"""

import streamlit as st
import plotly.express as px
from utils import load_netflix_data

st.set_page_config(page_title="H3: International Growth", layout="wide")
st.title("H3: International Content Growth")
st.markdown("""
**Hypothesis 3:** Netflix's sustained international market share growth is driven by its high ratio of non-U.S. content (local-language originals and international licensing).
""")

# --- Load Data ---
df = load_netflix_data()

if df.empty:
    st.error("Netflix data could not be loaded for Hypothesis 3.")
else:
    st.header("Storyboard and Visualizations (Plotly Advanced)")
    
    # Filter for non-US content
    df_non_us = df[df['is_us'] == False]
    
    # --- Viz 1: Choropleth Map of Non-US Content Distribution ---
    st.subheader("Geographic Distribution of Non-U.S. Content")
    st.markdown("The **Choropleth Map** is the definitive visualization for showing the global reach of Netflix's content catalog. Darker colors indicate a higher volume of content originating from that country (primary production country).")

    # Aggregate by country
    country_counts = df_non_us['origin_country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Count']
    
    # Filter out Unknown and countries with very low counts for map clarity
    country_counts = country_counts[country_counts['Country'] != 'Unknown']
    country_counts = country_counts[country_counts['Count'] > 5] 
    
    # Plotly Map
    fig_map = px.choropleth(
        country_counts, 
        locations='Country',
        locationmode='country names',
        color='Count',
        hover_name='Country',
        color_continuous_scale=px.colors.sequential.Reds,
        title='Volume of Netflix Content by Primary Non-U.S. Origin Country',
        template='plotly_dark' # Use dark theme for a premium look
    )
    fig_map.update_geos(
        showcoastlines=True, 
        coastlinecolor="Black", 
        showland=True, 
        landcolor="lightgray",
        showocean=True, 
        oceancolor="azure"
    )
    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")
    
    # --- Viz 2: Treemap of Top International Countries/Genres ---
    st.subheader("Hierarchy of Top Non-U.S. Content (Countries & Genres)")
    st.markdown("The **Treemap** visualizes the hierarchy: the size of the box is proportional to the content count, and the color represents the primary genre in that country. This quickly identifies key international content hubs.")

    # Prepare data for Treemap
    # 1. Split 'listed_in' into individual genres
    df_non_us_genres = df_non_us.copy()
    df_non_us_genres['genre'] = df_non_us_genres['listed_in'].str.split(', ')
    df_exploded = df_non_us_genres.explode('genre')

    # 2. Aggregate counts by Country and Genre
    treemap_df = df_exploded.groupby(['origin_country', 'genre']).size().reset_index(name='Count')
    
    # Filter to top N countries for visual clarity (e.g., top 10)
    top_countries = treemap_df.groupby('origin_country')['Count'].sum().nlargest(10).index
    treemap_df_filtered = treemap_df[treemap_df['origin_country'].isin(top_countries)]
    
    fig_tree = px.treemap(
        treemap_df_filtered, 
        path=[px.Constant("Netflix Non-US Content"), 'origin_country', 'genre'], 
        values='Count',
        color='genre',
        title='Treemap of Top 10 Non-U.S. Countries and Their Primary Genres',
        color_discrete_sequence=px.colors.qualitative.Dark24
    )
    fig_tree.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    st.plotly_chart(fig_tree, use_container_width=True)


    # --- Observations ---
    st.header("Observations")
    st.markdown("""
    The **Choropleth Map** visually proves Netflix's global content sourcing strategy.
    
    The **Treemap** provides a granular view, identifying the dominant content types within the most critical international markets.
    """)