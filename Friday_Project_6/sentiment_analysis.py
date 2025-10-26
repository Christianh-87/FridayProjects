import sqlite3
import pandas as pd
from openai import OpenAI
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import CsAPIkey

# Initialize OpenAI client using your imported key
client = OpenAI(api_key=CsAPIkey.apikey)

# Step 1: Load the reviews data
conn = sqlite3.connect("feedback.db")
df = pd.read_sql_query("SELECT * FROM reviews;", conn)
conn.close()

print(f"✅ Loaded {len(df)} reviews from database.\n")

# Step 2: Define a function to analyze sentiment
def analyze_sentiment(text):
    try:
        response = client.responses.create(
            model="gpt-5",
            input=f"""
            Analyze the sentiment of this Apple Vision Pro customer review.
            Respond with one of the following labels: Positive, Negative, or Neutral.
            Also include a short 1-sentence reason for your classification.

            Review:
            {text}
            """
        )
        return response.output_text.strip()
    except Exception as e:
        return f"Error: {e}"

# Step 3: Run sentiment analysis on a few reviews (test phase)
results = []
for i, review in enumerate(df["review_text"].head(5)):  # test only first 5 reviews for now
    print(f"Analyzing review #{i+1}...")
    result = analyze_sentiment(review)
    results.append(result)

# Step 4: Store results in the dataframe
df["sentiment_analysis"] = results + [None] * (len(df) - len(results))

# Step 5: Extract sentiment label (Positive/Negative/Neutral)
def extract_label(text):
    if text is None:
        return None
    text_lower = text.lower()
    if "positive" in text_lower:
        return "Positive"
    elif "negative" in text_lower:
        return "Negative"
    elif "neutral" in text_lower:
        return "Neutral"
    else:
        return "Unknown"

df["sentiment_label"] = df["sentiment_analysis"].apply(extract_label)

# Step 6: Save results to CSV
df.to_csv("sentiment_results.csv", index=False)
print("✅ Sentiment analysis complete. Results saved to sentiment_results.csv.\n")

# Step 7: Visualize sentiment distribution
plt.figure(figsize=(6, 4))
df["sentiment_label"].value_counts().plot(kind="bar", color=["green", "red", "gray"])
plt.title("Apple Vision Pro Review Sentiment Distribution")
plt.xlabel("Sentiment")
plt.ylabel("Number of Reviews")
plt.tight_layout()
plt.savefig("sentiment_distribution.png")
plt.show()

# Step 8: Generate a word cloud of all reviews
text_blob = " ".join(df["review_text"].dropna().tolist())
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text_blob)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Common Words in Reviews")
plt.show()
# ---------- STEP 2: Aspect Extraction ----------
print("\n🔍 Starting aspect extraction...")

def extract_aspects(text):
    """
    Uses GPT to extract key product aspects and tag them as Positive, Negative, or Neutral.
    Example output:
      - Comfort: Negative (heavy headset)
      - Display: Positive (incredible clarity)
      - Battery: Neutral (acceptable life)
    """
    try:
        response = client.responses.create(
            model="gpt-5",
            input=f"""
            From this Apple Vision Pro review, list the main product aspects or features mentioned.
            For each aspect, classify it as Positive, Negative, or Neutral and include a very short reason.
            Keep the format simple:
              - Aspect: Sentiment (brief reason)
            Example:
              - Comfort: Negative (heavy on the face)
              - Display: Positive (crisp and immersive)
              - Price: Negative (too expensive)
            Only include aspects that are clearly discussed.
            
            Review:
            {text}
            """
        )
        return response.output_text.strip()
    except Exception as e:
        return f"Error: {e}"

# Apply aspect extraction to all reviews
aspects = []
for i, review in enumerate(df["review_text"]):
    if (i + 1) % 10 == 0:
        print(f"Processing aspects for review #{i + 1}...")
    aspects.append(extract_aspects(review))

df["aspects"] = aspects

# Save new results
df.to_csv("sentiment_and_aspects.csv", index=False)
print("✅ Aspect extraction complete. Results saved to sentiment_and_aspects.csv.\n")

# ---------- STEP 3: Visualization ----------
import re
from collections import Counter

print("📊 Generating aspect frequency visualization...")

# Count aspects
aspect_counter = Counter()
for aspects_text in df["aspects"].dropna():
    for line in aspects_text.splitlines():
        match = re.match(r"^\s*-\s*([A-Za-z\s/]+):", line)
        if match:
            aspect = match.group(1).strip().title()
            aspect_counter[aspect] += 1

# Create bar chart for most frequent aspects
top_aspects = aspect_counter.most_common(10)
if top_aspects:
    labels, counts = zip(*top_aspects)
    plt.figure(figsize=(8,4))
    plt.bar(labels, counts, color="skyblue")
    plt.title("Most Frequently Mentioned Aspects")
    plt.xlabel("Aspect")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("aspect_frequency.png")
    plt.show()

print("✅ Visualization complete. aspect_frequency.png created.\n")

