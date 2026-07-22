from faker import Faker
import random
import pandas as pd
from datetime import timedelta

fake = Faker()

# Canadian provinces, weighted roughly by population
# so generated customers feel realistic (more from ON/BC/QC, fewer from smaller provinces)
CANADIAN_PROVINCES = [
    "Ontario", "Quebec", "British Columbia", "Alberta",
    "Manitoba", "Saskatchewan", "Nova Scotia", "New Brunswick",
    "Newfoundland and Labrador", "Prince Edward Island"
]
PROVINCE_WEIGHTS = [38, 22, 13, 11, 4, 3, 3, 2, 2, 2]  # rough population skew

CANADIAN_CITIES_BY_PROVINCE = {
    "Ontario": ["Toronto", "Ottawa", "Mississauga", "Hamilton", "London"],
    "Quebec": ["Montreal", "Quebec City", "Laval", "Gatineau"],
    "British Columbia": ["Vancouver", "Victoria", "Surrey", "Burnaby"],
    "Alberta": ["Calgary", "Edmonton", "Red Deer"],
    "Manitoba": ["Winnipeg", "Brandon"],
    "Saskatchewan": ["Saskatoon", "Regina"],
    "Nova Scotia": ["Halifax", "Sydney"],
    "New Brunswick": ["Moncton", "Saint John"],
    "Newfoundland and Labrador": ["St. John's"],
    "Prince Edward Island": ["Charlottetown"],
}


def generate_customers(n=1000, start_date="2023-01-01", end_date="2024-12-31"):
    customers = []

    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    date_range_days = (end - start).days

    for i in range(1, n + 1):
        # Skew signups toward more recent dates (simulates a growing business)
        skew_factor = random.random() ** 1.5
        days_offset = int(skew_factor * date_range_days)
        signup_date = start + timedelta(days=days_offset)

        # Pick a province (population-weighted), then a city within that province
        province = random.choices(CANADIAN_PROVINCES, weights=PROVINCE_WEIGHTS)[0]
        city = random.choice(CANADIAN_CITIES_BY_PROVINCE[province])

        customers.append({
            "customer_id": i,
            "email": fake.email(),
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "city": city,
            "province": province,
            "country": "Canada",
            "created_at": signup_date,
            "accepts_marketing": random.choices([True, False], weights=[70, 30])[0],
        })

    return pd.DataFrame(customers)


if __name__ == "__main__":
    df = generate_customers(n=1000)
    print(df.head())
    print(f"\nGenerated {len(df)} customers")
    print(f"\nProvince distribution:\n{df['province'].value_counts()}")
    df.to_csv("customers.csv", index=False)
    print("\nSaved to customers.csv")