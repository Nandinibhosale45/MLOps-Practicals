
import pandas as pd
from datetime import datetime


class SimpleFeatureStore:
    def __init__(self):
        self.repository = {}
        self.offline_store = {}
        self.online_store = {}

    def register_feature(self, name, entity_key, columns, description):
        if name in self.repository:
            raise ValueError(f"Feature group '{name}' is already registered.")

        self.repository[name] = {
            "entity_key": entity_key,
            "columns": columns,
            "description": description,
            "registered_at": datetime.now().isoformat(timespec="seconds")
        }
        print(f"Registered feature group: {name}")

    def ingest(self, name, dataframe):
        if name not in self.repository:
            raise ValueError(f"Register '{name}' before ingestion.")

        metadata = self.repository[name]
        required = [metadata["entity_key"]] + metadata["columns"]
        missing = [col for col in required if col not in dataframe.columns]

        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        data = dataframe[required].copy()

        if data[metadata["entity_key"]].isna().any():
            raise ValueError("Entity key cannot contain missing values.")

        # Offline store: keep all records
        if name not in self.offline_store:
            self.offline_store[name] = data.copy()
        else:
            self.offline_store[name] = pd.concat(
                [self.offline_store[name], data], ignore_index=True
            )

        # Online store: keep the latest record per entity
        latest = data.drop_duplicates(
            subset=[metadata["entity_key"]], keep="last"
        )

        if name not in self.online_store:
            self.online_store[name] = {}

        for _, row in latest.iterrows():
            key = row[metadata["entity_key"]]
            self.online_store[name][key] = row.to_dict()

        print(f"Ingested {len(data)} rows into '{name}'.")

    def get_offline_features(self, name, entity_ids=None):
        if name not in self.offline_store:
            raise ValueError(f"No offline data found for '{name}'.")

        data = self.offline_store[name].copy()
        key = self.repository[name]["entity_key"]

        if entity_ids is not None:
            data = data[data[key].isin(entity_ids)]

        return data.reset_index(drop=True)

    def get_online_features(self, name, entity_id):
        if name not in self.online_store:
            raise ValueError(f"No online data found for '{name}'.")

        return self.online_store[name].get(entity_id)

    def show_repository(self):
        return pd.DataFrame(self.repository).T


# 1. Create the feature store
store = SimpleFeatureStore()

# 2. Register customer features
store.register_feature(
    name="customer_features",
    entity_key="customer_id",
    columns=[
        "total_orders",
        "avg_order_value",
        "days_since_last_order"
    ],
    description="Purchase activity features for customer models"
)

# 3. Prepare and ingest data
customer_data = pd.DataFrame({
    "customer_id": [101, 102, 103, 101],
    "total_orders": [5, 2, 9, 6],
    "avg_order_value": [450.0, 220.0, 780.0, 470.0],
    "days_since_last_order": [4, 20, 2, 1]
})

store.ingest("customer_features", customer_data)

# 4. Display repository
print("\nFEATURE REPOSITORY")
print(store.show_repository()[
    ["entity_key", "columns", "description"]
])

# 5. Retrieve offline features
print("\nOFFLINE FEATURES FOR TRAINING")
training_data = store.get_offline_features(
    "customer_features", entity_ids=[101, 102, 103]
)
print(training_data)

# 6. Retrieve online features
print("\nONLINE FEATURES FOR CUSTOMER 101")
online_features = store.get_online_features(
    "customer_features", 101
)
print(online_features)

# 7. Reuse features in two models
churn_input = online_features
print("\nMODEL A (CHURN) INPUT:", churn_input)

offer_input = online_features
print("\nMODEL B (OFFER RECOMMENDATION) INPUT:", offer_input)
