#!/usr/bin/env python3
"""
간단한 테스트 스크립트 - Synthetic Data 생성 확인
사용자가 직접 실행해서 문제를 진단할 수 있습니다.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import pycountry

print("=" * 80)
print("🧪 Synthetic Data Generation 테스트")
print("=" * 80)

# Set seed
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

# Countries
major_countries = [
    'United States', 'France', 'United Kingdom', 'Switzerland', 'Germany',
    'Japan', 'China', 'Singapore', 'United Arab Emirates', 'Hong Kong',
    'Netherlands', 'Spain', 'Italy', 'Belgium', 'Sweden', 'Ireland'
]

offshore_hubs = [
    'Cayman Islands', 'Luxembourg', 'Bermuda', 'British Virgin Islands',
    'Jersey', 'Panama', 'Monaco', 'Liechtenstein', 'Guernsey'
]

other_countries = [
    'India', 'Brazil', 'Mexico', 'South Africa', 'Australia', 'Canada',
    'Portugal', 'Greece', 'Norway', 'Denmark', 'Finland', 'Poland',
    'Czechia', 'Austria', 'Turkey', 'Israel', 'Egypt', 'Morocco'
]

all_countries = major_countries + offshore_hubs + other_countries
segments = ['R1OE', 'R2OE', 'R3OE', 'H1OE', 'H2OE', 'H3OE', 'BH1C', 'BH2C', 'BH3C', 'WM1', 'WM2', 'CORP1', 'SME1']

# Generate small dataset for testing
n_transactions = 100
print(f"\n📊 Generating {n_transactions} test transactions...\n")

# TX IDs
tx_ids = [f"TX_{20000000 + i}" for i in range(n_transactions)]

# Dates
start = pd.to_datetime('2023-01-01')
dates = [start + timedelta(days=random.randint(0, 364)) for _ in range(n_transactions)]
dates = [d.strftime('%Y%m%d') for d in dates]

# Amounts
amounts = np.random.lognormal(mean=9.5, sigma=1.2, size=n_transactions)
amounts = np.round(amounts, 2)

print(f"✅ Generated {len(tx_ids)} TX_IDs")
print(f"✅ Generated {len(dates)} dates")
print(f"✅ Generated {len(amounts)} amounts")

# Sender countries
print(f"\n🌍 Generating sender countries from {len(major_countries)} options...")
sender_probs = np.random.zipf(a=1.5, size=len(major_countries))
sender_probs = sender_probs / sender_probs.sum()
sender_countries = np.random.choice(major_countries, size=n_transactions, p=sender_probs)

print(f"✅ Generated {len(sender_countries)} sender countries")
print(f"   Type: {type(sender_countries)}")
print(f"   Sample: {sender_countries[:5]}")
print(f"   Unique: {len(set(sender_countries))}")

# Beneficiary countries
print(f"\n🌍 Generating beneficiary countries from {len(all_countries)} options...")
benef_probs = np.random.zipf(a=2.0, size=len(all_countries))
benef_probs = benef_probs / benef_probs.sum()
benef_countries = np.random.choice(all_countries, size=n_transactions, p=benef_probs)

print(f"✅ Generated {len(benef_countries)} beneficiary countries")
print(f"   Type: {type(benef_countries)}")
print(f"   Sample: {benef_countries[:5]}")
print(f"   Unique: {len(set(benef_countries))}")

# Segments
sender_segments = np.random.choice(segments, size=n_transactions)
benef_segments = np.random.choice(segments, size=n_transactions)

print(f"\n✅ Generated segments")

# Create DataFrame
print(f"\n📋 Creating DataFrame...")
df = pd.DataFrame({
    'TX_ID': tx_ids,
    'TX_Date': dates,
    'TX_Amount': amounts,
    'S_Country': sender_countries,
    'B_Country': benef_countries,
    'S_Segment': sender_segments,
    'B_Segment': benef_segments,
    'TX_TypeCode': np.random.choice(['C', 'D', 'T'], size=n_transactions),
    'TX_Mechanism': np.random.choice(['SWIFT', 'CHIPS', 'Wire', 'ACH'], size=n_transactions)
})

print(f"\n✅ DataFrame created!")
print(f"   Shape: {df.shape}")
print(f"   Columns: {list(df.columns)}")

# Add intermediaries
print(f"\n🔗 Adding intermediary countries...")
has_intermediary = np.random.random(n_transactions) < 0.25

for i in range(1, 5):
    df[f'I{i}_Country'] = pd.Series([None] * n_transactions, dtype='object')

intermediary_indices = np.where(has_intermediary)[0]
print(f"   Intermediary transactions: {len(intermediary_indices)}")

for idx in intermediary_indices:
    n_inter = np.random.choice([1, 2, 3, 4], p=[0.65, 0.25, 0.08, 0.02])
    
    if np.random.random() < 0.3:
        inter_pool = offshore_hubs + major_countries[:3]
    else:
        inter_pool = major_countries + other_countries[:10]
    
    inter_countries = np.random.choice(inter_pool, size=min(n_inter, len(inter_pool)), replace=False)
    
    for i, country in enumerate(inter_countries, 1):
        df.at[idx, f'I{i}_Country'] = country

print(f"✅ Intermediaries added")

# Country code columns (ISO alpha-2)
df['S_CountryCode'] = df['S_Country'].apply(get_country_code).astype('string')
df['B_CountryCode'] = df['B_Country'].apply(get_country_code).astype('string')
for i in range(1, 5):
    df[f'I{i}_CountryCode'] = df[f'I{i}_Country'].apply(get_country_code).astype('string')

print(f"✅ Country codes added")

# Final check
print(f"\n" + "=" * 80)
print(f"🎉 FINAL RESULTS")
print(f"=" * 80)

print(f"\nDataFrame shape: {df.shape}")
print(f"\nColumn types:")
for col in df.columns:
    print(f"  {col:20s}: {df[col].dtype}")

print(f"\n\nNaN check:")
print(f"  S_Country NaN count: {df['S_Country'].isna().sum()}")
print(f"  B_Country NaN count: {df['B_Country'].isna().sum()}")

print(f"\n\nFirst 5 rows (Country + Code columns):")
print(df[['TX_ID', 'S_Country', 'S_CountryCode', 'B_Country', 'B_CountryCode', 'I1_Country', 'I1_CountryCode']].head())

print(f"\n" + "=" * 80)

# Check if any NaN in main country columns
if df['S_Country'].isna().any() or df['B_Country'].isna().any():
    print("❌ ERROR: Found NaN in S_Country or B_Country!")
    print("   This should not happen. There may be an issue with the code.")
else:
    print("✅ SUCCESS: All S_Country and B_Country values are present!")
    print("   The synthetic data generation is working correctly.")

print("=" * 80)
