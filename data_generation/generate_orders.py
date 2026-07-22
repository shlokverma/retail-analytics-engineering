from faker import Faker
import random
import pandas as pd
from datetime import timedelta

fake = Faker()

# Seasonality weights by month — retail isn't flat across the year.
# November/December (holiday season) get a noticeable bump.
MONTH_SEASONALITY = {
    1: 0.8, 2: 0.7, 3: 0.85, 4: 0.9, 5: 0.95, 6: 1.0,
    7: 1.0, 8: 0.95, 9: 1.0, 10: 1.1, 11: 1.6, 12: 1.8,
}

ORDER_STATUS_WEIGHTS = {
    "fulfilled": 85,
    "cancelled": 10,
    "refunded": 5,
}

DISCOUNT_CODES = ["WELCOME10", "SUMMER15", "VIP20", None, None, None, None]  # ~43% of orders have a code


def assign_order_count(n_customers):
    """
    Assigns how many orders each customer gets, following a realistic
    power-law-like distribution rather than uniform random:
      60% -> 1 order
      25% -> 2-3 orders
      10% -> 4-6 orders
       5% -> 7+ orders (loyal/power customers)
    """
    order_counts = []
    for _ in range(n_customers):
        roll = random.random()
        if roll < 0.60:
            order_counts.append(1)
        elif roll < 0.85:
            order_counts.append(random.randint(2, 3))
        elif roll < 0.95:
            order_counts.append(random.randint(4, 6))
        else:
            order_counts.append(random.randint(7, 12))
    return order_counts


def generate_order_date(signup_date, order_index, end_date):
    """
    First order tends to land close to signup (intentional signup-to-purchase).
    Later orders are spread further out over time, but never before signup
    and never after the dataset's end_date.
    """
    if order_index == 0:
        days_after_signup = int(random.expovariate(1 / 5))  # avg ~5 days, some longer tails
        days_after_signup = min(days_after_signup, 14)
    else:
        days_after_signup = order_index * random.randint(20, 90)

    order_date = signup_date + timedelta(days=days_after_signup)
    return min(order_date, end_date)


def weighted_month_choice():
    months = list(MONTH_SEASONALITY.keys())
    weights = list(MONTH_SEASONALITY.values())
    return random.choices(months, weights=weights)[0]


def generate_orders_and_line_items(customers_df, products_df, end_date="2024-12-31"):
    end = pd.Timestamp(end_date)
    order_counts = assign_order_count(len(customers_df))

    orders = []
    line_items = []
    order_id = 1
    line_item_id = 1

    for idx, customer in customers_df.iterrows():
        n_orders = order_counts[idx]
        signup_date = pd.Timestamp(customer["created_at"])

        for order_index in range(n_orders):
            order_date = generate_order_date(signup_date, order_index, end)

            if order_date < signup_date:
                continue

            status = random.choices(
                list(ORDER_STATUS_WEIGHTS.keys()),
                weights=list(ORDER_STATUS_WEIGHTS.values())
            )[0]

            discount_code = random.choice(DISCOUNT_CODES)

            n_line_items = random.randint(1, 4)
            selected_products = products_df.sample(n=n_line_items)

            order_subtotal = 0
            for _, product in selected_products.iterrows():
                quantity = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
                unit_price = product["price"]
                line_subtotal = round(unit_price * quantity, 2)
                order_subtotal += line_subtotal

                line_items.append({
                    "line_item_id": line_item_id,
                    "order_id": order_id,
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "line_subtotal": line_subtotal,
                })
                line_item_id += 1

            discount_amount = round(order_subtotal * 0.1, 2) if discount_code else 0.0
            total_price = round(order_subtotal - discount_amount, 2)

            cancelled_at = order_date + timedelta(days=random.randint(0, 2)) if status == "cancelled" else None

            orders.append({
                "order_id": order_id,
                "customer_id": customer["customer_id"],
                "created_at": order_date,
                "status": status,
                "discount_code": discount_code,
                "discount_amount": discount_amount,
                "subtotal": round(order_subtotal, 2),
                "total_price": total_price,
                "cancelled_at": cancelled_at,
            })
            order_id += 1

    return pd.DataFrame(orders), pd.DataFrame(line_items)


if __name__ == "__main__":
    customers_df = pd.read_csv("customers.csv", parse_dates=["created_at"])
    products_df = pd.read_csv("products.csv")

    orders_df, line_items_df = generate_orders_and_line_items(customers_df, products_df)

    print(orders_df.head())
    print(f"\nGenerated {len(orders_df)} orders and {len(line_items_df)} line items")
    print(f"\nOrders per customer (distribution):\n{orders_df['customer_id'].value_counts().describe()}")
    print(f"\nStatus breakdown:\n{orders_df['status'].value_counts()}")
    print(f"\nOrders by month:\n{orders_df['created_at'].dt.month.value_counts().sort_index()}")

    orders_df.to_csv("orders.csv", index=False)
    line_items_df.to_csv("order_line_items.csv", index=False)
    print("\nSaved to orders.csv and order_line_items.csv")