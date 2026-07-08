# Data_science

A personal collection of independent data science exploration scripts and notebooks — not a single cohesive project.

## What's in here

This repo is a grab-bag of three unrelated pieces of work, each self-contained:

- **`finbot.py`** — A Streamlit-based "stock analysis chatbot" prototype. It defines helper functions for pulling stock data via `yfinance` (price, SMA, EMA, RSI, MACD, institutional holders, news) intended to be wired up to an OpenAI chat model as callable "functions", plus a small Streamlit UI. The OpenAI function-calling wiring is commented out and incomplete, so it does not run as-is.
- **`incomepredict.ipynb`** — A notebook that loads the UCI "Adult" census income dataset (expects `/content/sample_data/adult.csv`, i.e. a Google Colab path), does one-hot encoding of categorical columns, explores correlations, and trains a `RandomForestClassifier` (with a `GridSearchCV` hyperparameter search) to predict whether income is above/below $50K. Reaches ~86% test accuracy.
- **`spamsmspredict.ipynb`** — A notebook that loads an SMS spam dataset (expects `content/spam.csv`), does text cleanup/EDA (message length, word/sentence counts, word clouds, most-common-word plots), tokenizes and stems messages with NLTK, vectorizes with TF-IDF, and compares Gaussian/Multinomial/Bernoulli Naive Bayes classifiers (Bernoulli NB reaches ~98.8% accuracy). Note: one cell references a `num_characters` column that hasn't been created yet, and another cell has a typo (`df[df['']==0]` instead of `df[df['label_enc']==0]`), so the notebook does not run top-to-bottom without fixes.

## Tech stack

- Python
- pandas, numpy, matplotlib, seaborn
- scikit-learn (RandomForestClassifier, GridSearchCV, Naive Bayes variants, TF-IDF)
- NLTK (tokenization, stopwords, stemming), WordCloud
- yfinance, Streamlit, OpenAI Python SDK (`finbot.py` only)
- Jupyter notebooks (`incomepredict.ipynb`, `spamsmspredict.ipynb`)

## Setup

There is no `requirements.txt`, `pyproject.toml`, or environment file in this repo, so dependencies must be installed manually based on the imports used in each file:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn nltk wordcloud yfinance streamlit openai
```

For the notebooks, you'll also need the datasets, which are not included in this repo:
- `incomepredict.ipynb` expects the UCI Adult census dataset as `adult.csv` (path is hardcoded to a Google Colab location, `/content/sample_data/adult.csv` — update the path if running elsewhere).
- `spamsmspredict.ipynb` expects an SMS spam dataset as `content/spam.csv`.

`finbot.py` expects an `API_KEY` file in the working directory containing an OpenAI API key.

## Usage

Notebooks can be opened and run cell-by-cell in Jupyter or Google Colab (after fixing the dataset paths noted above).

`finbot.py` is a Streamlit app, intended to be run as:

```bash
streamlit run finbot.py
```

but it currently errors out before producing useful output (see Status below).

## Status

**Work in progress / exploratory scripts, not a polished product.** Specifically:

- `finbot.py` does not run as-is: the OpenAI function-calling logic is commented out/incomplete.
- `spamsmspredict.ipynb` does not run top-to-bottom: it drops a `num_characters` column before it exists, and has a typo referencing `df['']` instead of `df['label_enc']` when building a word cloud.
- `incomepredict.ipynb` is the most complete of the three — it runs end-to-end and produces a trained classifier — but assumes a Google Colab file path and has no exported model or app around it.
- None of the three pieces are related to each other; this repo is a loose collection of individual learning/practice exercises rather than a single application.
