import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import engine, Base
from backend.models import RawProductionPlan, RawActualProduction, ProductionPlan, ActualProduction

def ingest():
    print("Recreating database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Loading CSVs...")
    workspace_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    plan_csv_path = os.path.join(workspace_root, "candidate_pack/data/production_plan.csv")
    actual_csv_path = os.path.join(workspace_root, "candidate_pack/data/actual_production.csv")

    raw_plan_df = pd.read_csv(plan_csv_path)
    raw_actual_df = pd.read_csv(actual_csv_path)

    print("Inserting raw data...")
    raw_plan_df.to_sql("raw_production_plan", con=engine, if_exists="append", index=False)
    raw_actual_df.to_sql("raw_actual_production", con=engine, if_exists="append", index=False)

    print("Cleaning production plan data...")
    initial_plan_count = len(raw_plan_df)
    
    clean_plan_df = raw_plan_df.drop_duplicates()
    clean_plan_df = clean_plan_df.dropna(subset=['planned_units'])
    clean_plan_df = clean_plan_df[clean_plan_df['planned_units'] > 0]
    
    clean_plan_df = clean_plan_df.rename(columns={
        "plan_date": "date",
        "plant": "plant_id",
        "sku": "product_code"
    })
    clean_plan_df['date'] = pd.to_datetime(clean_plan_df['date'], format='mixed').dt.date
    
    rows_dropped = initial_plan_count - len(clean_plan_df)

    print("Cleaning actual production data...")
    clean_actual_df = raw_actual_df.copy()
    clean_actual_df['date'] = pd.to_datetime(clean_actual_df['date'], format='mixed').dt.date

    actual_products = set(clean_actual_df['product_code'].unique())
    plan_no_match = clean_plan_df[~clean_plan_df['product_code'].isin(actual_products)]
    plan_no_match_count = len(plan_no_match)

    print("Inserting clean data...")
    clean_plan_df.to_sql("production_plan", con=engine, if_exists="append", index=False)
    clean_actual_df.to_sql("actual_production", con=engine, if_exists="append", index=False)

    print("\n=== Ingestion Summary ===")
    print(f"Rows dropped from production plan (duplicates, nulls, <= 0): {rows_dropped}")
    print(f"Clean plan rows with no matching product_code in actuals: {plan_no_match_count}")
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest()
