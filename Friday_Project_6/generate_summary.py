# ---------- generate_summary.py ----------
import pandas as pd
from collections import Counter
import re

# Load your CSVs
sentiment_df = pd.read_csv("sentiment_results.csv")
aspects_df = pd.read_csv("sentiment_and_aspects.csv")

# ---------- Sentiment Summary ----------
sentiment_counts = sentiment_df["sentiment_label"].value_counts(dropna=True)
total_reviews = sentiment_counts.sum()

sentiment_summary = []
for sentiment, count in sentiment_counts.items():
    percent = round((count / total_reviews) * 100, 1)
    sentiment_summary.append(f"{sentiment}: {count} reviews ({percent}%)")

# ---------- Aspect Frequency ----------
aspect_counter = Counter()
for aspects_text in aspects_df["aspects"].dropna():
    for line in aspects_text.splitlines():
        match = re.match(r"^\s*-\s*([A-Za-z\s/]+):", line)
        if match:
            aspect = match.group(1).strip().title()
            aspect_counter[aspect] += 1

top_aspects = aspect_counter.most_common(10)

# ---------- Generate Insights ----------
insights = """
INSIGHTS:
- Positive feedback focuses on display quality, immersion, and build materials.
- Negative feedback focuses on comfort/weight, price, and early software limitations.
- Many reviews mention optimism for future software improvements.
"""

recommendations = """
RECOMMENDATIONS:
- Reduce headset weight and improve ergonomics for better comfort.
- Expand visionOS app ecosystem to increase usability.
- Maintain strengths in display clarity and premium build.
- Reassess pricing or provide bundled value (apps, accessories).
"""

# ---------- Write summary to file ----------
with open("summary_report.txt", "w", encoding="utf-8") as f:
    f.write("=== APPLE VISION PRO FEEDBACK SUMMARY ===\n\n")
    f.write("SENTIMENT DISTRIBUTION:\n")
    for line in sentiment_summary:
        f.write("  " + line + "\n")

    f.write("\nTOP MENTIONED ASPECTS:\n")
    for aspect, count in top_aspects:
        f.write(f"  {aspect}: {count} mentions\n")

    f.write(insights)
    f.write(recommendations)

print("✅ Summary report generated: summary_report.txt")
