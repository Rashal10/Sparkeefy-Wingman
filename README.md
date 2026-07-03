# Sparkeefy Wingman

Local Streamlit app that helps you figure out what to text in dating and relationship situations.

Uses DeepSeek (`deepseek-v4-flash`)

## Setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
```

Add your API key to `.env`:

```
DEEPSEEK_API_KEY=your_key_here
```

Get a key at https://platform.deepseek.com

## Run

```bash
streamlit run app.py
```

Open http://localhost:8501

## Project layout

```
app.py              Streamlit UI
wingman/
  client.py         DeepSeek API calls
  config.py         env settings
  prompt.py         system prompt + few-shot examples
  safety.py         basic input/output checks
  schema.py         response models
  service.py        main entry point for the app
requirements.txt
.env.example
```

## Response format

The model returns JSON with:

- `energy_read` — read on the other person's vibe
- `wingman_response` — advice for you
- `suggested_messages` — copy-paste texts
- `follow_up_question` — optional, only when needed
- `confidence` — 0 to 1
- `safety_flag` — true for harassment/manipulation requests

## Env vars

| Variable | Default |
|----------|---------|
| `DEEPSEEK_API_KEY` | required |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL` | `deepseek-v4-flash` |
| `WINGMAN_MAX_TOKENS` | `500` |
| `WINGMAN_TEMPERATURE` | `0.7` |
