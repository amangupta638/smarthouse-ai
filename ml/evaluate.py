import os
import json

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)


DATA_PATH = "data/house_prices.csv"
OUTPUT_DIR = "data/processed"


def run_eda():

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    print("=" * 60)
    print("SMART HOUSE AI - EDA")
    print("=" * 60)

    print("\nDataset Shape:")
    print(df.shape)

    print("\nDataset Info:")
    print(df.info())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nStatistical Summary:")
    print(df.describe(include="all"))

    # -----------------------------
    # Price distribution
    # -----------------------------

    plt.figure(figsize=(10, 6))
    plt.hist(df["price"], bins=30)
    plt.title("House Price Distribution")
    plt.xlabel("Price")
    plt.ylabel("Number of Houses")
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "price_distribution.png"
        )
    )
    plt.close()

    # -----------------------------
    # Area vs Price
    # -----------------------------

    plt.figure(figsize=(10, 6))
    plt.scatter(
        df["area"],
        df["price"],
        alpha=0.5
    )
    plt.title("Area vs House Price")
    plt.xlabel("Area (sq ft)")
    plt.ylabel("Price")
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "area_vs_price.png"
        )
    )
    plt.close()

    # -----------------------------
    # Bedrooms vs Price
    # -----------------------------

    plt.figure(figsize=(10, 6))
    df.groupby("bedrooms")["price"].mean().plot(
        kind="bar"
    )
    plt.title("Average Price by Bedrooms")
    plt.xlabel("Bedrooms")
    plt.ylabel("Average Price")
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "bedrooms_vs_price.png"
        )
    )
    plt.close()

    # -----------------------------
    # Location vs Price
    # -----------------------------

    plt.figure(figsize=(12, 6))
    df.groupby("location")["price"].mean().sort_values().plot(
        kind="bar"
    )
    plt.title("Average House Price by Location")
    plt.xlabel("Location")
    plt.ylabel("Average Price")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "location_vs_price.png"
        )
    )
    plt.close()

    # -----------------------------
    # Correlation
    # -----------------------------

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    plt.figure(figsize=(10, 8))
    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        fmt=".2f"
    )
    plt.title("Feature Correlation Matrix")
    plt.tight_layout()
    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "correlation_matrix.png"
        )
    )
    plt.close()

    print("\nEDA charts saved successfully.")

    # -----------------------------
    # Model Evaluation
    # -----------------------------

    features = [
        "area",
        "bedrooms",
        "bathrooms",
        "floors",
        "location",
        "parking",
        "furnishing",
        "property_type",
        "age",
    ]

    target = "price"

    X = df[features]
    y = df[target]

    numerical_features = [
        "area",
        "bedrooms",
        "bathrooms",
        "floors",
        "parking",
        "age",
    ]

    categorical_features = [
        "location",
        "furnishing",
        "property_type",
    ]

    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                ),
            )
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                ),
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
            ),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                numerical_pipeline,
                numerical_features,
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_features,
            ),
        ]
    )

    model = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor,
            ),
            (
                "model",
                LinearRegression(),
            ),
        ]
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    model.fit(
        X_train,
        y_train
    )

    predictions = model.predict(X_test)

    mae = mean_absolute_error(
        y_test,
        predictions
    )

    mse = mean_squared_error(
        y_test,
        predictions
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        predictions
    )

    metrics = {
        "model": "Linear Regression",
        "MAE": float(mae),
        "MSE": float(mse),
        "RMSE": float(rmse),
        "R2": float(r2),
    }

    with open(
        os.path.join(
            OUTPUT_DIR,
            "evaluation_metrics.json"
        ),
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            metrics,
            file,
            indent=4
        )

    print("\n" + "=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    print(f"MAE  : {mae:,.2f}")
    print(f"MSE  : {mse:,.2f}")
    print(f"RMSE : {rmse:,.2f}")
    print(f"R2   : {r2:.4f}")

    print("\nMetrics saved successfully.")


if __name__ == "__main__":
    run_eda()