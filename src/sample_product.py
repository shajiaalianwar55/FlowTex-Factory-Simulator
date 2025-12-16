# src/sample_product.py
import random
from datetime import datetime

SIZES = ["XS","S","M","L","XL"]
COLORS = ["white","black","navy","red","green","yellow"]
PRODUCT_LINES = ["Line A","Line B","Line C"]

def make_sample(i=1):
    size = random.choices(SIZES, weights=[5,20,50,20,5])[0]
    product = {
        "product_id": f"T{str(i).zfill(6)}",
        "product_line": random.choice(PRODUCT_LINES),
        "batch_id": datetime.now().strftime("B%Y%m%d_01"),
        "line_sequence": i,
        "size": size,
        "color": random.choice(COLORS),
        "weight_g": round(random.normalvariate(180 if size=='M' else 160, 8), 1),
        "production_timestamp": datetime.now().isoformat(timespec='seconds'),
        "raw_defect_score": round(random.random(), 3),
        "inspected": True,
        "passed_inspection": None,
        "rejection_reason": ""
    }
    product["passed_inspection"] = product["raw_defect_score"] < 0.35
    if not product["passed_inspection"]:
        product["rejection_reason"] = random.choice(["stain","misprint","wrong_size","hole"])
    return product

if __name__ == "__main__":
    sample = make_sample(1)
    for k,v in sample.items():
        print(f"{k}: {v}")