import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("generated_products.csv")

#passed vs rejected
status_counts = df['passed_inspection'].value_counts()
plt.figure(figsize=(6, 5))
bars = plt.bar(status_counts.index.astype(str), status_counts.values)
plt.xlabel("Inspection Result")
plt.ylabel("Number of Fabric Pieces")
plt.title("Fabric Inspection Outcome")
plt.grid(axis='y', linestyle='--', alpha=0.6)

for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height,
             f'{int(height)}', ha='center', va='bottom')
plt.tight_layout()
plt.show()

#pie chart
status_counts = df['passed_inspection'].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(
    status_counts.values,
    labels=status_counts.index.astype(str),
    autopct='%1.1f%%',
    startangle=90,
    colors=['skyblue', 'yellow']
)
plt.title("Fabric Inspection Result (Pass vs Reject)")
plt.tight_layout()
plt.show()

#defect score distribution histogram
plt.figure(figsize=(7, 5))
plt.hist(df['raw_defect_score'], bins=15)
plt.xlabel("Defect Score")
plt.ylabel("Frequency")
plt.title("Histogram of Fabric Defect Scores")
plt.tight_layout()
plt.show()

#defect vs production order
sorted_df = df.sort_values("line_sequence")
reduced_df = sorted_df.iloc[::10]

plt.figure(figsize=(8, 5))
plt.bar(
    range(len(reduced_df)),
    reduced_df['raw_defect_score'],
    color='orange'
)
plt.xlabel("Sampled Production Items")
plt.ylabel("Defect Score")
plt.title("Defect Scores Across Sampled Production Items")
plt.tight_layout()
plt.show()

#Weight vs Defect Score
plt.figure(figsize=(7, 5))
plt.scatter(df['weight_g'], df['raw_defect_score'])
plt.xlabel("Fabric Weight (grams)")
plt.ylabel("Defect Score")
plt.title("Weight vs Defect Score Relationship")
plt.tight_layout()
plt.show()

#Rejection reasons
reasons = df['rejection_reason'].dropna().value_counts()

plt.figure(figsize=(7, 5))
plt.bar(reasons.index, reasons.values)
plt.xlabel("Defect Type")
plt.ylabel("Count")
plt.title("Reasons for Fabric Rejection")
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()

#stacked bar-Pass vs Reject per Product Line
line_status = df.groupby(['product_line', 'passed_inspection']).size().unstack(fill_value=0)

plt.figure(figsize=(8, 5))
plt.bar(line_status.index, line_status[True], label="Passed")
plt.bar(line_status.index, line_status[False],
        bottom=line_status[True], label="Rejected")

plt.xlabel("Product Line")
plt.ylabel("Count")
plt.title("Pass vs Reject per Production Line")
plt.legend()
plt.tight_layout()
plt.show()

#BOX PLOT — Defect Score by Size
sizes = df['size'].unique()
data = [df[df['size'] == s]['raw_defect_score'] for s in sizes]

plt.figure(figsize=(7, 5))
plt.boxplot(data, labels=sizes)
plt.xlabel("Fabric Size")
plt.ylabel("Defect Score")
plt.title("Defect Score Distribution by Size")
plt.tight_layout()
plt.show()
