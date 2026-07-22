from faker import Faker
import random
import pandas as pd

fake = Faker()

# Category definitions with realistic price ranges (CAD) for an apparel/outdoor lifestyle brand
# Price ranges are deliberately different per category — a t-shirt and a jacket
# shouldn't be drawn from the same distribution.
CATEGORIES = {
    "Outerwear": {
        "price_range": (150, 400),
        "product_names": [
            "Alpine Shell Jacket", "Trailhead Rain Jacket", "Summit Down Parka",
            "Windward Softshell", "Glacier Insulated Coat", "Ridge Vest",
            "Coastal Anorak", "Highline Bomber", "Tundra Parka", "Cascade Windbreaker"
        ],
    },
    "Activewear": {
        "price_range": (60, 130),
        "product_names": [
            "Momentum Leggings", "Flow Sports Bra", "Pulse Training Tee",
            "Drift Joggers", "Core Compression Shorts", "Velocity Tank",
            "Align Leggings", "Endure Half-Zip", "Surge Shorts", "Tempo Tights"
        ],
    },
    "Footwear": {
        "price_range": (90, 220),
        "product_names": [
            "Trailrunner Mid Boot", "Pathfinder Sneaker", "Switchback Hiker",
            "Urban Trail Shoe", "Granite Approach Shoe", "Stride Runner",
            "Basecamp Boot", "Coastal Slip-On", "Ridgeline Trainer", "Traverse Sandal"
        ],
    },
    "Bottoms": {
        "price_range": (70, 150),
        "product_names": [
            "Voyager Hiking Pant", "Commuter Chino", "Trailblazer Cargo",
            "Everyday Jogger", "Crestline Shorts", "Switchback Pant",
            "Basecamp Trouser", "Ridge Utility Pant", "Drift Cargo Short", "Alpine Snow Pant"
        ],
    },
    "Tops": {
        "price_range": (35, 90),
        "product_names": [
            "Heritage Crewneck Tee", "Longline Henley", "Basecamp Flannel",
            "Trailhead Hoodie", "Everyday Crew Sweatshirt", "Ridge Quarter-Zip",
            "Summit Fleece", "Coastal Linen Shirt", "Alpine Thermal Tee", "Drift Pullover"
        ],
    },
    "Accessories": {
        "price_range": (20, 80),
        "product_names": [
            "Trailhead Beanie", "Summit Wool Socks", "Ridge Daypack",
            "Voyager Tote", "Basecamp Cap", "Coastal Sunglasses",
            "Alpine Gloves", "Drift Water Bottle", "Switchback Belt", "Tundra Scarf"
        ],
    },
}

VENDOR_COUNTRIES = ["Canada", "Vietnam", "China", "Portugal", "Bangladesh"]
VENDOR_COUNTRY_WEIGHTS = [25, 25, 25, 15, 10]  # rough manufacturing distribution


def generate_products():
    products = []
    product_id = 1

    for category, details in CATEGORIES.items():
        min_price, max_price = details["price_range"]

        for name in details["product_names"]:
            price = round(random.uniform(min_price, max_price), 2)
            vendor_country = random.choices(
                VENDOR_COUNTRIES, weights=VENDOR_COUNTRY_WEIGHTS
            )[0]

            products.append({
                "product_id": product_id,
                "title": name,
                "product_type": category,
                "vendor_country": vendor_country,
                "price": price,
            })
            product_id += 1

    return pd.DataFrame(products)


if __name__ == "__main__":
    df = generate_products()
    print(df.head(10))
    print(f"\nGenerated {len(df)} products")
    print(f"\nProducts per category:\n{df['product_type'].value_counts()}")
    print(f"\nPrice range by category:\n{df.groupby('product_type')['price'].agg(['min', 'max']).round(2)}")
    df.to_csv("products.csv", index=False)
    print("\nSaved to products.csv")