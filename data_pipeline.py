
import pandas as pd

# 1. DATA COLLECTION
def collect_data():
    data = {
        "Name": ["Amit", "Riya", "Rahul", "Sneha", "Vikas"],
        "Marks": [85, 72, None, 90, 65],
        "Attendance": [90, 80, 75, None, 60],
        "Study_Hours": [5, 4, 3, 6, 2]
    }

    df = pd.DataFrame(data)
    print("\n--- Raw Data ---")
    print(df)
    return df


# 2. DATA PREPROCESSING
def preprocess_data(df):
    df = df.copy()

    # Fill missing values with the column mean
    df["Marks"] = df["Marks"].fillna(df["Marks"].mean())
    df["Attendance"] = df["Attendance"].fillna(
        df["Attendance"].mean()
    )

    # Remove duplicate records
    df = df.drop_duplicates()
    return df


# 3. FEATURE ENGINEERING
def feature_engineering(df):
    df = df.copy()

    df["Performance_Score"] = (
        df["Marks"] * 0.7 +
        df["Attendance"] * 0.3
    )

    df["Performance"] = df["Performance_Score"].apply(
        lambda x: "Good" if x >= 75 else "Needs Improvement"
    )

    return df


# 4. DATA VALIDATION
def validate_data(df):
    print("\n--- Data Validation ---")

    print("Missing values:")
    print(df.isnull().sum())

    if df["Attendance"].between(0, 100).all():
        print("Attendance values are valid.")
    else:
        print("Invalid attendance values.")

    if df["Marks"].between(0, 100).all():
        print("Marks values are valid.")
    else:
        print("Invalid marks values.")

    return True


# 5. END-TO-END PIPELINE
def data_pipeline():
    print("\nStarting Data Pipeline...")

    # Data Collection
    df = collect_data()

    # Data Preprocessing
    df = preprocess_data(df)
    print("\n--- After Preprocessing ---")
    print(df)

    # Feature Engineering
    df = feature_engineering(df)
    print("\n--- After Feature Engineering ---")
    print(df)

    # Data Validation
    validate_data(df)

    # Save final dataset
    df.to_csv("processed_student_data.csv", index=False)

    print("\nPipeline completed successfully.")
    print("Final data saved as processed_student_data.csv")

    return df


# 6. EXECUTE PIPELINE
if __name__ == "__main__":
    final_data = data_pipeline()

    print("\n--- Final Dataset ---")
    print(final_data)
