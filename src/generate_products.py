# src/generate_products.py
import csv
import random
import argparse
from datetime import datetime, timedelta

# Configuration: allowed values & simple rules
PRODUCT_LINES = ["Line A", "Line B", "Line C"]
SIZE_DISTR = {"XS": 0.05, "S": 0.20, "M": 0.50, "L": 0.20, "XL": 0.05}
COLORS = ["white", "black", "navy", "red", "green", "yellow"]
WEIGHT_MEANS = {"XS": 140, "S": 160, "M": 180, "L": 200, "XL": 220}
WEIGHT_SD = 8.0

# thresholds for "passed_inspection" (lower threshold = stricter)
PASS_THRESHOLDS = {"Line A": 0.35, "Line B": 0.30, "Line C": 0.25}

def weighted_choice_from_dict(d):
    items = list(d.keys())
    weights = list(d.values())
    return random.choices(items, weights=weights, k=1)[0]

def generate_one(product_index, start_time):
    # pick size/color/line
    size = weighted_choice_from_dict(SIZE_DISTR)
    color = random.choice(COLORS)
    product_line = random.choice(PRODUCT_LINES)

    # weight based on size
    mean = WEIGHT_MEANS.get(size, 180)
    weight_g = round(max(50.0, random.gauss(mean, WEIGHT_SD)), 1)

    # defect score 0..1
    raw_defect_score = round(random.random(), 3)

    # decide pass/fail by line threshold
    threshold = PASS_THRESHOLDS.get(product_line, 0.35)
    passed_inspection = raw_defect_score < threshold

    # rejection reason if failed
    rejection_reason = ""
    if not passed_inspection:
        rejection_reason = random.choice(["stain", "misprint", "wrong_size", "hole", "color mismatch"])

    product = {
        "product_id": f"T{str(product_index).zfill(6)}",
        "product_line": product_line,
        "batch_id": start_time.strftime("B%Y%m%d_01"),
        "line_sequence": product_index,
        "size": size,
        "color": color,
        "weight_g": weight_g,
        "production_timestamp": start_time.isoformat(timespec='seconds'),
        "raw_defect_score": raw_defect_score,
        "inspected": True,
        "passed_inspection": passed_inspection,
        "rejection_reason": rejection_reason
    }
    return product

def generate_products(n, seed=None, start_time=None):
    if seed is not None:
        random.seed(seed)
    start_time = start_time or datetime.now()
    products = []
    current_time = start_time

    # simple interarrival: increment time by a small random delta (1-10 seconds)
    for i in range(1, n + 1):
        p = generate_one(i, current_time)
        products.append(p)

        # increment current_time so timestamps increase (keeps it simple & deterministic with seed)
        delta_seconds = random.randint(1, 10)
        current_time = current_time + timedelta(seconds=delta_seconds)

    return products

def write_csv(products, out_path):
    if not products:
        print("No products to write.")
        return
    keys = list(products[0].keys())
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for p in products:
            writer.writerow(p)
    print(f"Wrote {len(products)} rows to: {out_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate T-shirt factory dataset.")
    parser.add_argument("--n", type=int, default=1000, help="Number of products to generate.")
    parser.add_argument("--out", type=str, default="data/generated_products.csv", help="Output CSV path.")
    parser.add_argument("--seed", type=int, default=42, help="Random seed (for reproducibility).")
    args = parser.parse_args()

    products = generate_products(args.n, seed=args.seed)
    write_csv(products, args.out)

    # simple summary
    accepted = sum(1 for p in products if p["passed_inspection"])
    rejected = len(products) - accepted
    print(f"Accepted: {accepted}, Rejected: {rejected}")

if __name__ == "__main__":
    main()