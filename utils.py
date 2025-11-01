#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  1 09:29:16 2025

@author: prabhanvishnu
"""

import pandas as pd
import streamlit as st
import re
import numpy as np
import json

# --- Data Loading Functions ---

@st.cache_data
def load_netflix_data():
    """Loads the main Netflix dataset and cleans it for H2 and H3."""
    try:
        df = pd.read_csv('netflix_titles (1).csv')
        
        # Clean data for H3 (International Growth)
        df['country'] = df['country'].fillna('Unknown')
        df['is_us'] = df['country'].apply(lambda x: 'United States' in x)
        
        # Function to split and select the primary country for H3 visualization
        def get_primary_country(country_str):
            if pd.isna(country_str):
                return 'Unknown'
            # Split countries and take the first one
            countries = str(country_str).split(',')
            return countries[0].strip()

        df['origin_country'] = df['country'].apply(get_primary_country)
        
        # Clean data for H2 (Recency)
        df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')
        df = df.dropna(subset=['release_year'])
        df['release_year'] = df['release_year'].astype(int)
        df['period'] = df['release_year'].apply(lambda x: 'After 2015' if x > 2015 else 'Before/On 2015')
        
        return df
    except FileNotFoundError:
        st.error("Error: 'netflix_titles (1).csv' not found. Please upload the file.")
        return pd.DataFrame()

@st.cache_data
def load_platform_comparison_data():
    """
    Loads and combines data from Netflix, Amazon Prime, Disney+, Apple TV, Crunchyroll, and HBO
    to create the comparison dataset required for Hypothesis 1.
    """
    platform_dfs = []
    
    # --- Platform Loading Helpers ---
    def load_standard_platform(filename, platform_name, country_col='country'):
        try:
            df = pd.read_csv(filename)
            df['platform'] = platform_name
            
            # Standardize column name if necessary
            if country_col != 'country':
                df = df.rename(columns={country_col: 'country'})
            
            # Ensure it has 'type' column
            if 'type' not in df.columns:
                 df['type'] = 'Unknown' 
                 
            # Clean the list-like string for country if it's from the shared 'titles.csv' schema
            if country_col == 'production_countries':
                 df['country'] = df['country'].apply(lambda x: re.sub(r"[\[\]']", "", str(x)).split(',')[0])
            
            # Standardize 'year' column to 'release_year' for Disney+
            if platform_name == 'Disney+' and 'year' in df.columns:
                df = df.rename(columns={'year': 'release_year'})

            # Filter to only required columns
            required_cols = ['title', 'release_year', 'country', 'platform', 'type']
            for col in required_cols:
                if col not in df.columns:
                    st.warning(f"Missing column '{col}' in {filename}. Skipping load.")
                    return pd.DataFrame()

            return df[required_cols]
        except FileNotFoundError:
            st.warning(f"Could not find '{filename}' for H1 comparison. Please check the filename.")
            return pd.DataFrame()

    # --- Load all 6 Platforms ---
    # Standard CSVs
    platform_dfs.append(load_standard_platform('netflix_titles (1).csv', 'Netflix'))
    platform_dfs.append(load_standard_platform('amazon_prime_titles.csv', 'Amazon Prime'))
    platform_dfs.append(load_standard_platform('disney_plus_shows.csv', 'Disney+', country_col='country'))
    
    # Assumed Renamed CSVs
    platform_dfs.append(load_standard_platform('apple_tv_titles.csv', 'Apple TV', country_col='production_countries'))
    platform_dfs.append(load_standard_platform('crunchyroll_titles.csv', 'Crunchyroll', country_col='production_countries'))
    platform_dfs.append(load_standard_platform('hbo_titles.csv', 'HBO', country_col='production_countries'))

    # Filter out empty dataframes resulting from missing files
    platform_dfs = [df for df in platform_dfs if not df.empty]
    
    if not platform_dfs:
        st.error("No platform data could be loaded for Hypothesis 1. Please ensure you have uploaded and renamed the files.")
        return pd.DataFrame(columns=['title', 'release_year', 'country', 'platform', 'type', 'is_local'])

    # Combine all platforms
    all_platforms = pd.concat(platform_dfs, ignore_index=True)
    
    # --- Final Cleaning and 'is_local' Flag ---
    all_platforms['country'] = all_platforms['country'].fillna('Unknown')
    # 'is_local' is defined as any country NOT 'US' or 'United States'
    us_aliases = ['US', 'United States']
    all_platforms['is_local'] = ~all_platforms['country'].apply(lambda x: any(alias in str(x) for alias in us_aliases))
    
    # Clean release_year
    all_platforms['release_year'] = pd.to_numeric(all_platforms['release_year'], errors='coerce')
    all_platforms = all_platforms.dropna(subset=['release_year'])
    all_platforms['release_year'] = all_platforms['release_year'].astype(int)
    
    return all_platforms