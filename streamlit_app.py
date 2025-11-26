"""
Streamlit Brand Reputation & Crisis Monitor (simple)
Run:
    pip install -r requirements.txt
    streamlit run streamlit_app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
import plotly.express as px
from collections import Counter
import io

st.set_page_config(page_title="Brand Monitor - AcmeShop", layout="wide")

st.title("Brand Reputation & Crisis Monitor — Simple Demo")
st.markdown("Analyze comments and track sentiment trends. Built with Streamlit + VADER.")

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is None:
        df = pd.read_csv("sample_comments.csv", parse_dates=["timestamp"])
    else:
        df = pd.read_csv(uploaded_file, parse_dates=["timestamp"])
    return df

uploaded = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"])
df = load_data(uploaded)

st.sidebar.markdown("**Dataset**")
st.sidebar.write(f"Rows: {len(df)}")
st.sidebar.write("Columns: " + ", ".join(df.columns))

st.header("Raw data sample")
st.dataframe(df.head(50))

# Sentiment analysis with VADER
analyzer = SentimentIntensityAnalyzer()
def score_text(text):
    s = analyzer.polarity_scores(str(text))
    return s["compound"], s["neg"], s["neu"], s["pos"]

df[["sentiment_compound", "neg", "neu", "pos"]] = df["comment"].apply(lambda t: pd.Series(score_text(t)))
df["sentiment_label"] = df["sentiment_compound"].apply(lambda x: "positive" if x>0.05 else ("negative" if x < -0.05 else "neutral"))
df["date"] = df["timestamp"].dt.date

st.header("Overall sentiment distribution")
dist = df["sentiment_label"].value_counts().reset_index()
dist.columns = ["sentiment","count"]
fig = px.pie(dist, names="sentiment", values="count", title="Sentiment Distribution")
st.plotly_chart(fig, use_container_width=True)

st.header("Daily sentiment trend")
daily = df.groupby("date").agg(
    total_comments=("id","count"),
    avg_compound=("sentiment_compound","mean"),
    negative_pct=("sentiment_label", lambda x: (x=="negative").sum()/len(x)*100)
).reset_index()
fig2 = px.line(daily, x="date", y=["avg_compound","negative_pct"], labels={"value":"score","variable":"metric"}, title="Avg compound & Negative % over time")
st.plotly_chart(fig2, use_container_width=True)
st.dataframe(daily)

# Simple spike detection (negative_pct)
st.header("Spike detection (simple)")
daily["neg_diff"] = daily["negative_pct"].diff().fillna(0)
threshold = st.slider("Spike threshold: increase in negative % (absolute points)", 5, 1, 20)
spikes = daily[daily["neg_diff"] >= threshold]
st.write(f"Threshold: +{threshold} percentage points")
if not spikes.empty:
    st.write("Detected spikes:")
    st.dataframe(spikes)
else:
    st.write("No spikes detected with current threshold.")

# Top negative comments
st.header("Top negative comments (by compound score)")
neg_comments = df[df["sentiment_label"]=="negative"].sort_values("sentiment_compound").head(20)
st.dataframe(neg_comments[["timestamp","username","comment","sentiment_compound"]])

# Quick keyword extraction (simple)
st.header("Common complaint keywords (negative comments)")
neg_text = " ".join(neg_comments["comment"].astype(str).tolist()).lower().split()
# remove tiny words
neg_words = [w.strip(".,!?:;()[]\"'") for w in neg_text if len(w)>3]
common = Counter(neg_words).most_common(20)
common_df = pd.DataFrame(common, columns=["word","count"])
st.table(common_df)

# Auto-suggest actions
st.header("Auto-suggested actions")
issues = [w for w,c in common if c>=2]
suggestions = []
if "delivery" in issues or "delayed" in issues or "delay" in issues:
    suggestions.append("- Investigate shipping partners and update ETAs to customers.")
if "support" in issues or "service" in issues or "reply" in issues:
    suggestions.append("- Improve customer support SLAs and add canned helpful responses.")
if "refund" in issues or "returned" in issues or "wrong" in issues:
    suggestions.append("- Audit order fulfillment process and streamline refund policy.")
if "damaged" in issues or "packaging" in issues:
    suggestions.append("- Review packaging processes and quality checks before dispatch.")
if not suggestions:
    suggestions.append("- No frequent issues found. Continue monitoring.")

for s in suggestions:
    st.write(s)

st.markdown("---")
st.write("Export results:")
buf = io.StringIO()
df.to_csv(buf, index=False)
st.download_button("Download analyzed CSV", data=buf.getvalue(), file_name="analyzed_comments.csv", mime="text/csv")