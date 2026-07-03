# Sparkeefy Wingman

Streamlit app that helps you figure out what to text in dating and relationship situations. Describe what's going on, get a quick read on the vibe, advice in plain language, and 1–3 messages you can copy and send.

Uses DeepSeek (`deepseek-v4-flash`)

## Live demo

Deploy on [Streamlit Community Cloud](https://share.streamlit.io) (free for public repos). After deploy, your app URL will look like:

`https://your-app-name.streamlit.app`

## Local setup

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Add your API key to `.env`:

```
DEEPSEEK_API_KEY=your_key_here
```

Get a key at https://platform.deepseek.com

**Never commit `.env`** — it is listed in `.gitignore`.

## Run locally

```bash
streamlit run app.py
```

Open http://localhost:8501

## Deploy to Streamlit Cloud (free)

1. Push this repo to GitHub (public repo for free tier).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app** and select:
   - **Repository:** your fork or `Rashal10/Sparkeefy-Wingman`
   - **Branch:** `main`
   - **Main file path:** `app.py`
4. Open **Advanced settings → Secrets** and add:

```toml
DEEPSEEK_API_KEY = "your_actual_deepseek_key_here"
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-v4-flash"
WINGMAN_MAX_TOKENS = 500
WINGMAN_TEMPERATURE = 0.7
```

5. Click **Deploy** and wait 2–5 minutes for the build to finish.

Pushes to `main` redeploy automatically. Update secrets anytime under **Manage app → Settings → Secrets**.

## Project layout

```
app.py                  Streamlit UI
wingman/
  client.py             DeepSeek API calls
  config.py             env settings
  prompt.py             system prompt + few-shot examples
  safety.py             basic input/output checks
  schema.py             response models
  service.py            main entry point for the app
requirements.txt
.env.example
.streamlit/config.toml  theme + cloud settings
eval/                   evaluation scenarios (CSV / XLSX)
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

On Streamlit Cloud, set these in **Secrets** (not in the repo).
