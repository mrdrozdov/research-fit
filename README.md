# Research Fit

Learn about research.

## Setup

```
pip install -r requirements.txt
```

## Pipeline

Download and pre-process data.

```
# Download data.
python pipeline/01_read_ftp.py

# Convert to json. Keep only papers that have abstracts.
python pipeline/02b_parse_pubmed_json.py

# Extract keywords.
#TODO
```
