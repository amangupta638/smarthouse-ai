import pandas as pd
import numpy as np
import os

np.random.seed(42)

# Number of houses
n = 1000

# Available locations
locations = [
    "Delhi",
    "Lucknow",
    "Noida",
    "Gurgaon",
    "Kanpur",
    "Prayagraj",
    "Jaipur",
    "Mumbai",
    "Bangalore",
    "Pune"
]

# Create dataset
data = {
    "area": np.random.randint(500, 4000, n),
    "bedrooms": np.random.randint(1, 6, n),
    "bathrooms": np.random.randint(1, 5, n),
    "floors": np.random.randint(1, 4, n),

    "location": np.random.choice(
        locations,
        n
    ),

    "parking": np.random.randint(
        0,
        3,
        n
    ),

    "furnishing": np.random.choice(
        [
            "Furnished",
            "Semi-Furnished",
            "Unfurnished"
        ],
        n
    ),

    "property_type": np.random.choice(
        [
            "Apartment",
            "House",
            "Villa"
        ],
        n
    ),

    "age": np.random.randint(
        0,
        30,
        n
    )
}

df = pd.DataFrame(data)

# Location price multiplier
location_factor = df["location"].map({
    "Delhi": 1.8,
    "Mumbai": 2.2,
    "Bangalore": 1.9,
    "Gurgaon": 2.0,
    "Noida": 1.5,
    "Pune": 1.6,
    "Jaipur": 1.2,
    "Lucknow": 1.0,
    "Kanpur": 0.8,
    "Prayagraj": 0.7
})

# Generate realistic-ish price
df["price"] = (
    df["area"] * 7000 * location_factor
    + df["bedrooms"] * 500000
    + df["bathrooms"] * 250000
    + df["parking"] * 150000
    - df["age"] * 50000
    + np.random.normal(
        0,
        500000,
        n
    )
)

# Prevent unrealistic negative prices
df["price"] = df["price"].clip(
    lower=1_000_000
)

# Make sure data directory exists
os.makedirs(
    "data",
    exist_ok=True
)

# Save CSV
output_path = "data/house_prices.csv"

df.to_csv(
    output_path,
    index=False
)

print("=" * 50)
print("SMART HOUSE AI DATASET GENERATOR")
print("=" * 50)
print()
print("Dataset created successfully!")
print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")
print(f"Saved to: {output_path}")
print()
print("Columns:")
print(list(df.columns))
print()
print("First 5 records:")
print(df.head())
print()
print("=" * 50)