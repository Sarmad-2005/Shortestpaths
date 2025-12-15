"""
Phase 1: Data Preparation
Filter the worldcities dataset to keep only Pakistani cities
and extract necessary columns: City Name, Latitude, and Longitude
"""

import pandas as pd

def prepare_pakistan_cities():
    """
    Load the world cities CSV, filter for Pakistan only,
    and save the cleaned data with only necessary columns.
    """
    # Load the world cities dataset and display initial info
    df = pd.read_csv('worldcities.csv')
    
    print(f"Total cities in dataset: {len(df)}")
    
    # Filter for Pakistan only
    pakistan_df = df[df['country'] == 'Pakistan'].copy()
    
    print(f"Cities in Pakistan: {len(pakistan_df)}")
    
    # Keep only necessary columns: city name, latitude, longitude
    pakistan_df = pakistan_df[['city', 'lat', 'lng']].copy()
    
    # Rename columns for clarity
    pakistan_df.columns = ['City', 'Latitude', 'Longitude']
    
    # Remove any rows with missing data
    pakistan_df = pakistan_df.dropna()
    
    # Sort by city name for easier viewing
    pakistan_df = pakistan_df.sort_values('City').reset_index(drop=True)
    
    # Save to CSV
    pakistan_df.to_csv('pak_cities.csv', index=False)
    
    print(f"\nData saved to pak_cities.csv")
    print(f"\nFirst 10 cities:")
    print(pakistan_df.head(10))
    
    return pakistan_df

if __name__ == "__main__":
    df = prepare_pakistan_cities()
