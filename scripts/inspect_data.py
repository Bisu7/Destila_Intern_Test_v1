import pandas as pd

def inspect_data():
    print("=== Data Inspection Report ===\n")
    
    try:
        plan_df = pd.read_csv("../candidate_pack/data/production_plan.csv")
        actual_df = pd.read_csv("../candidate_pack/data/actual_production.csv")
    except Exception as e:
        print(f"Error loading CSVs: {e}")
        return

    def print_stats(name, df, date_col, sku_col, qty_col):
        print(f"--- {name} ---")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(f"Data Types:\n{df.dtypes}\n")
        print(f"First 5 Rows:\n{df.head()}\n")
        print(f"Null Counts:\n{df.isnull().sum()}\n")
        
        try:
            parsed_dates = pd.to_datetime(df[date_col], format='mixed')
            print(f"Date Range: {parsed_dates.min().date()} to {parsed_dates.max().date()}")
            date_parse_error = False
        except Exception as e:
            print(f"Date Range: Error parsing dates - {e}")
            date_parse_error = True

        print(f"Unique {sku_col} Count: {df[sku_col].nunique()}")
        
        print(f"\nQuirks for {name}:")
        dupes = df.duplicated().sum()
        if dupes > 0:
            print(f"- Found {dupes} duplicate rows!")
        else:
            print("- No duplicate rows.")
            
        if date_parse_error:
            print("- Inconsistent date formats found.")
            
        if not pd.api.types.is_numeric_dtype(df[qty_col]):
            print(f"- {qty_col} is not numeric!")
        else:
            neg_zero = (df[qty_col] <= 0).sum()
            if neg_zero > 0:
                print(f"- Found {neg_zero} rows with {qty_col} <= 0!")
            else:
                print(f"- All {qty_col} > 0.")
        print("\n")

    print_stats("Production Plan", plan_df, "plan_date", "sku", "planned_units")
    print_stats("Actual Production", actual_df, "date", "product_code", "units_produced")

    print("--- Overlap Analysis ---")
    try:
        plan_dates = set(pd.to_datetime(plan_df["plan_date"], format='mixed').dt.date)
        actual_dates = set(pd.to_datetime(actual_df["date"], format='mixed').dt.date)
        date_overlap = plan_dates.intersection(actual_dates)
        print(f"Date Overlap: {len(date_overlap)} overlapping days.")
        if len(date_overlap) == 0:
            print("- WARNING: No overlapping dates!")
    except Exception as e:
        print(f"Could not compute date overlap: {e}")

    plan_skus = set(plan_df["sku"].unique())
    actual_skus = set(actual_df["product_code"].unique())
    sku_overlap = plan_skus.intersection(actual_skus)
    print(f"Product Overlap: {len(sku_overlap)} overlapping products.")
    if len(sku_overlap) == 0:
        print("- WARNING: No overlapping products!")
        
    print("\n--- Column Matching Quirks ---")
    if list(plan_df.columns) != list(actual_df.columns):
        print("- Mismatched column names between plan and actual.")
        print(f"  Plan: {list(plan_df.columns)}")
        print(f"  Actual: {list(actual_df.columns)}")

if __name__ == "__main__":
    inspect_data()
