# What is this?

A script to gather and host a filterable view of India ⋅ Ministry of Education ⋅ National Institutional Ranking Framework (NIRF) data. This repository hosts a [live, filterable](https://yig.github.io/auto-NIRF/) view of all the data.

# Install

```
pip install requests beautifulsoup4
```

# Run

```
python3 autonirf.py
```

# Deploy

```
cp All.csv docs/All.csv
```

# Update from year-to-year

Try running the script with a change to the year number? More formally:

1. Go to <https://www.nirfindia.org>
2. Click the link for the latest results, e.g., <https://www.nirfindia.org/Rankings/2024/Ranking.html>
3. Check for any changes to the categories or category URLs.
