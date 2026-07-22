import random
import pandas as pd
from datetime import timedelta

# Core design idea: review scores aren't independent random noise.
# They correlate with two things that matter for your "delivery experience" mart:
#   1. Delivery delay (longer delay -> lower rating, on average)
#   2. Order status (cancelled/refunded orders skew negative if reviewed at all)
# Only fulfilled orders get a realistic chance of a review; cancelled/refunded
# orders rarely get reviewed, and when they are, they skew low.

REVIEW_PROBABILITY_BY_STATUS = {
    "fulfilled": 0.45,
    "cancelled": 0.05,
    "refunded": 0.10,
}

POSITIVE_COMMENTS = [
    "Great quality, fits perfectly.", "Exactly what I expected, very happy.",
    "Fast shipping and love the product.", "Will definitely buy again.",
    "Exceeded my expectations.", "Comfortable and well made.",
]
NEUTRAL_COMMENTS = [
    "It's okay, nothing special.", "Decent for the price.",
    "Average quality, runs a bit small.", "Fine, but took a while to arrive.",
]
NEGATIVE_COMMENTS = [
    "Disappointed with the quality.", "Took way too long to arrive.",
    "Not as described, wouldn't buy again.", "Arrived damaged.",
    "Sizing was way off.",
]


def simulate_delivery_delay():
    roll = random.random()
    if roll < 0.70:
        return random.randint(2, 5)
    elif roll < 0.90:
        return random.randint(6, 10)
    else:
        return random.randint(11, 21)


def rating_from_delay(delay_days, status):
    if status in ("cancelled", "refunded"):
        return random.choices([1, 2, 3], weights=[50, 35, 15])[0]

    if delay_days <= 5:
        return random.choices([5, 4, 3], weights=[60, 30, 10])[0]
    elif delay_days <= 10:
        return random.choices([4, 3, 2], weights=[40, 40, 20])[0]
    else:
        return random.choices([3, 2, 1], weights=[20, 40, 40])[0]


def comment_from_rating(rating):
    if rating >= 4:
        return random.choice(POSITIVE_COMMENTS)
    elif rating == 3:
        return random.choice(NEUTRAL_COMMENTS)
    else:
        return random.choice(NEGATIVE_COMMENTS)


def generate_reviews(orders_df, line_items_df):
    reviews = []
    review_id = 1

    for _, order in orders_df.iterrows():
        review_chance = REVIEW_PROBABILITY_BY_STATUS.get(order["status"], 0)
        if random.random() > review_chance:
            continue

        delay_days = simulate_delivery_delay()
        delivered_at = pd.Timestamp(order["created_at"]) + timedelta(days=delay_days)
        rating = rating_from_delay(delay_days, order["status"])
        comment = comment_from_rating(rating)
        review_date = delivered_at + timedelta(days=random.randint(1, 7))

        order_line_items = line_items_df[line_items_df["order_id"] == order["order_id"]]
        if order_line_items.empty:
            continue
        product_id = order_line_items.sample(n=1)["product_id"].values[0]

        reviews.append({
            "review_id": review_id,
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "product_id": product_id,
            "rating": rating,
            "review_text": comment,
            "delivery_delay_days": delay_days,
            "created_at": review_date,
        })
        review_id += 1

    return pd.DataFrame(reviews)


if __name__ == "__main__":
    orders_df = pd.read_csv("orders.csv", parse_dates=["created_at"])
    line_items_df = pd.read_csv("order_line_items.csv")

    reviews_df = generate_reviews(orders_df, line_items_df)

    print(reviews_df.head())
    print(f"\nGenerated {len(reviews_df)} reviews out of {len(orders_df)} orders")
    print(f"\nRating distribution:\n{reviews_df['rating'].value_counts().sort_index()}")
    print(f"\nAvg rating by delay bucket:")
    reviews_df["delay_bucket"] = pd.cut(
        reviews_df["delivery_delay_days"], bins=[0, 5, 10, 21], labels=["fast", "mild_delay", "long_delay"]
    )
    print(reviews_df.groupby("delay_bucket", observed=True)["rating"].mean().round(2))

    reviews_df.to_csv("reviews.csv", index=False)
    print("\nSaved to reviews.csv")