# Brand/ Business Sentiment Monitor

This is a minimal working final-project scaffold that analyzes social-media comments for sentiment,
detects spikes in negative sentiment and suggests simple actions.

## What's included
- `streamlit_app.py` — Streamlit dashboard that:
  - Loads `sample_comments.csv`
  - Runs VADER sentiment analysis
  - Shows sentiment distribution, daily trend, spike detection, and top negative comments
  - Outputs suggested actions and allows CSV export

- `sample_comments.csv` — synthetic sample dataset (200 comments over the last 30 days).
- `requirements.txt` — Python dependencies.

## How to run (locally)
   ```
1. Install dependencies: pip install -r requirements.txt
   ```
```
2. Run Streamlit: streamlit run streamlit_app.py
```
## Notes
- You can replace `sample_comments.csv` with your own CSV. The app expects columns: `id,timestamp,username,comment,source`
