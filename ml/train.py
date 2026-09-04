import os
import json
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


DATA_PATH = "data/house_prices.csv"
MODEL_DIR = "models"

MODEL_PATH = os.path.join(
    MODEL_DIR,
    "linear_regression_model.pkl"
)

PREPROCESSOR_PATH = os.path.join(
    MODEL_DIR,
    "preprocessor.pkl"
)

METADATA_PATH = os.path.join(
    MODEL_DIR,
    "model_metadata.json"
)


def train_model():

    print("=" * 60)
    print("SMART HOUSE AI - LINEAR REGRESSION TRAINING")
    print("=" * 60)

    # Create models directory
    os.makedirs(MODEL_DIR, exist_ok=True)

    # Load dataset
    print("\nLoading dataset...")

    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    print(f"Dataset loaded successfully!")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove rows without target
    df = df.dropna(subset=["price"])

    # Features
    features = [
        "area",
        "bedrooms",
        "bathrooms",
        "floors",
        "location",
        "parking",
        "furnishing",
        "property_type",
        "age"
    ]

    target = "price"

    # Check required columns
    missing_columns = [
        column
        for column in features + [target]
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    X = df[features]
    y = df[target]

    # Numerical features
    numerical_features = [
        "area",
        "bedrooms",
        "bathrooms",
        "floors",
        "parking",
        "age"
    ]

    # Categorical features
    categorical_features = [
        "location",
        "furnishing",
        "property_type"
    ]

    # Numerical preprocessing
    numerical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="median")
            )
        ]
    )

    # Categorical preprocessing
    categorical_pipeline = Pipeline(
        steps=[
            (
                "imputer",
                SimpleImputer(strategy="most_frequent")
            ),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )

    # Combined preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numerical",
                numerical_pipeline,
                numerical_features
            ),
            (
                "categorical",
                categorical_pipeline,
                categorical_features
            )
        ]
    )

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    print("\nTraining data:", len(X_train))
    print("Testing data:", len(X_test))

    # Linear Regression
    model = LinearRegression()

    # Complete ML pipeline
    pipeline = Pipeline(
        steps=[
            (
                "preprocessor",
                preprocessor
            ),
            (
                "model",
                model
            )
        ]
    )

    print("\nTraining Linear Regression model...")

    pipeline.fit(X_train, y_train)

    print("Model training completed!")

    # Predictions
    y_pred = pipeline.predict(X_test)

    # Evaluation
    mae = mean_absolute_error(
        y_test,
        y_pred
    )

    mse = mean_squared_error(
        y_test,
        y_pred
    )

    rmse = mse ** 0.5

    r2 = r2_score(
        y_test,
        y_pred
    )

    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE")
    print("=" * 60)

    print(f"MAE  : {mae:,.2f}")
    print(f"MSE  : {mse:,.2f}")
    print(f"RMSE : {rmse:,.2f}")
    print(f"R²   : {r2:.4f}")

    # Save complete pipeline
    joblib.dump(
        pipeline,
        MODEL_PATH
    )

    print(
        f"\nModel saved to: {MODEL_PATH}"
    )

    # Save metadata
    metadata = {
        "model_name": "Linear Regression",
        "dataset": DATA_PATH,
        "features": features,
        "target": target,
        "training_rows": len(X_train),
        "testing_rows": len(X_test),
        "metrics": {
            "MAE": float(mae),
            "MSE": float(mse),
            "RMSE": float(rmse),
            "R2": float(r2)
        }
    }

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4
        )

    print(
        f"Metadata saved to: {METADATA_PATH}"
    )

    print("\nTraining completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    train_model()