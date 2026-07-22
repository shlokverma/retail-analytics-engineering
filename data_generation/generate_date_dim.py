import pandas as pd
from datetime import datetime, timedelta

def generate_date_dimension(start_date="2023-01-01", end_date="2024-12-31"):
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    df = pd.DataFrame({
        'date_id': dates.strftime('%Y%m%d').astype(int),
        'full_date': dates,
        'day_of_week': dates.day_name(),
        'day_of_month': dates.day,
        'month': dates.month,
        'month_name': dates.month_name(),
        'quarter': dates.quarter,
        'year': dates.year,
        'is_weekend': dates.dayofweek >= 5,
    })
    
    return df


if __name__ == "__main__":
    df = generate_date_dimension()
    print(df.head())
    print(f"\nGenerated {len(df)} rows")
    df.to_csv("date_dimension.csv", index=False)