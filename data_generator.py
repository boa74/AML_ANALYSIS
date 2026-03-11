"""
Synthetic AML Transaction Data Generator

This module generates synthetic financial transaction data for demonstration purposes.
The structure mimics real-world AML datasets but contains no actual financial information.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import pycountry

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

COUNTRY_CODE_OVERRIDES = {
    'Hong Kong': 'HK',
    'Czechia': 'CZ',
    'British Virgin Islands': 'VG'
}


def get_country_code(country_name):
    if pd.isna(country_name):
        return np.nan

    if country_name in COUNTRY_CODE_OVERRIDES:
        return COUNTRY_CODE_OVERRIDES[country_name]

    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_2
    except LookupError:
        try:
            match = pycountry.countries.search_fuzzy(country_name)[0]
            return match.alpha_2
        except LookupError:
            return np.nan


def generate_aml_transactions(
    n_transactions=50000,
    n_countries=50,
    intermediary_rate=0.25,
    offshore_hub_rate=0.15,
    start_date='2023-01-01',
    end_date='2023-12-31'
):
    """
    Generate synthetic AML transaction dataset.
    
    Parameters:
    -----------
    n_transactions : int
        Number of transactions to generate
    n_countries : int
        Number of unique countries in the network
    intermediary_rate : float
        Proportion of transactions involving intermediaries (0.0-1.0)
    offshore_hub_rate : float
        Proportion of intermediary transactions via offshore hubs
    start_date : str
        Start date for transactions (YYYY-MM-DD)
    end_date : str
        End date for transactions (YYYY-MM-DD)
    
    Returns:
    --------
    pd.DataFrame
        Synthetic transaction dataset with structure similar to real AML data
    """
    
    print(f"🔨 Generating {n_transactions:,} synthetic transactions...")
    
    # Country pools
    major_countries = [
        'United States', 'France', 'United Kingdom', 'Switzerland', 'Germany',
        'Japan', 'China', 'Singapore', 'United Arab Emirates', 'Hong Kong',
        'Netherlands', 'Spain', 'Italy', 'Belgium', 'Sweden'
    ]
    
    offshore_hubs = [
        'Cayman Islands', 'Luxembourg', 'Bermuda', 'British Virgin Islands',
        'Jersey', 'Guernsey', 'Panama', 'Monaco', 'Liechtenstein'
    ]
    
    other_countries = [
        'India', 'Brazil', 'Mexico', 'South Africa', 'Australia', 'Canada',
        'Ireland', 'Portugal', 'Greece', 'Norway', 'Denmark', 'Finland',
        'Poland', 'Czechia', 'Austria', 'Turkey', 'Israel', 'Egypt',
        'Morocco', 'Kenya', 'Nigeria', 'Chile', 'Argentina', 'Colombia'
    ]
    
    all_countries = major_countries + offshore_hubs + other_countries
    all_countries = all_countries[:n_countries]
    
    # Customer segments
    segments = [
        'R1OE', 'R2OE', 'R3OE', 'H1OE', 'H2OE', 'H3OE',
        'BH1C', 'BH2C', 'BH3C', 'WM1', 'WM2', 'WM3',
        'CORP1', 'CORP2', 'SME1', 'SME2', 'RETAIL'
    ]
    
    # Generate transaction IDs
    tx_ids = [f"TX_{26000000 + i}" for i in range(n_transactions)]
    
    # Generate dates
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    dates = [start + timedelta(days=random.randint(0, (end-start).days)) 
             for _ in range(n_transactions)]
    dates = [d.strftime('%Y%m%d') for d in dates]
    
    # Generate amounts (log-normal distribution, common in finance)
    # Mean around $20K, with heavy tail
    amounts = np.random.lognormal(mean=9.5, sigma=1.2, size=n_transactions)
    amounts = np.round(amounts, 2)
    
    # Add threshold clustering (structuring behavior)
    threshold_indices = np.random.choice(n_transactions, size=int(n_transactions * 0.15), replace=False)
    thresholds = [9500, 9800, 9900, 9950, 4900, 4950]
    for idx in threshold_indices:
        amounts[idx] = np.random.choice(thresholds) + np.random.uniform(-100, 100)
    
    # Generate sender countries (some concentration)
    sender_probs = np.random.zipf(a=1.5, size=len(major_countries))
    sender_probs = sender_probs / sender_probs.sum()
    sender_countries = np.random.choice(major_countries, size=n_transactions, p=sender_probs)
    
    # Generate beneficiary countries (more concentrated - hub effect)
    benef_probs = np.random.zipf(a=2.0, size=len(all_countries))
    benef_probs = benef_probs / benef_probs.sum()
    benef_countries = np.random.choice(all_countries, size=n_transactions, p=benef_probs)
    
    # Generate segments
    sender_segments = np.random.choice(segments, size=n_transactions)
    benef_segments = np.random.choice(segments, size=n_transactions)
    
    # Initialize DataFrame
    df = pd.DataFrame({
        'TX_ID': tx_ids,
        'TX_Date': dates,
        'TX_Amount': amounts,
        'S_Country': sender_countries,
        'B_Country': benef_countries,
        'S_Segment': sender_segments,
        'B_Segment': benef_segments,
    })
    
    # Generate intermediary columns
    has_intermediary = np.random.random(n_transactions) < intermediary_rate
    
    # Initialize intermediary columns
    for i in range(1, 5):
        df[f'I{i}_Country'] = pd.Series([None] * n_transactions, dtype='object')
    
    # Add intermediaries for selected transactions
    intermediary_indices = np.where(has_intermediary)[0]
    
    for idx in intermediary_indices:
        # Number of intermediaries (1-4)
        n_inter = np.random.choice([1, 2, 3, 4], p=[0.6, 0.25, 0.10, 0.05])
        
        # Select intermediary countries
        # Higher chance for offshore hubs
        use_offshore = np.random.random() < offshore_hub_rate
        if use_offshore:
            inter_pool = offshore_hubs + major_countries[:5]
        else:
            inter_pool = major_countries + other_countries[:10]
        
        inter_countries = np.random.choice(inter_pool, size=n_inter, replace=False)
        
        for i, country in enumerate(inter_countries, 1):
            df.loc[idx, f'I{i}_Country'] = country
    
    # Add round-tripping (5-8%)
    roundtrip_indices = np.random.choice(
        intermediary_indices, 
        size=int(len(intermediary_indices) * 0.2),
        replace=False
    )
    for idx in roundtrip_indices:
        df.loc[idx, 'B_Country'] = df.loc[idx, 'S_Country']
    
    # Additional columns (optional)
    df['TX_TypeCode'] = np.random.choice(['C', 'D', 'T', 'W'], size=n_transactions)
    df['TX_Mechanism'] = np.random.choice(
        ['SWIFT', 'CHIPS RECEIVE', 'FED SEND', 'Wire Transfer', 'ACH'], 
        size=n_transactions
    )

    # Country code columns (ISO alpha-2)
    df['S_CountryCode'] = df['S_Country'].apply(get_country_code).astype('string')
    df['B_CountryCode'] = df['B_Country'].apply(get_country_code).astype('string')
    for i in range(1, 5):
        df[f'I{i}_CountryCode'] = df[f'I{i}_Country'].apply(get_country_code).astype('string')
    
    print(f"✅ Generated {n_transactions:,} transactions")
    print(f"   Countries: {df['S_Country'].nunique()} senders, {df['B_Country'].nunique()} beneficiaries")
    print(f"   Intermediary rate: {has_intermediary.mean()*100:.1f}%")
    print(f"   Amount range: ${df['TX_Amount'].min():.2f} - ${df['TX_Amount'].max():,.2f}")
    print(f"   Median amount: ${df['TX_Amount'].median():,.2f}")
    
    return df


def save_example_data(filename='example_transactions.csv', n_transactions=10000):
    """
    Generate and save a small example dataset.
    """
    df = generate_aml_transactions(n_transactions=n_transactions)
    df.to_csv(filename, index=False)
    print(f"\n💾 Saved to {filename}")
    return df


if __name__ == "__main__":
    # Generate example dataset
    df = save_example_data('example_transactions.csv', n_transactions=10000)
    print("\n📊 Sample data:")
    print(df.head())
    print("\n✅ Done! Use this data for demonstration purposes.")
