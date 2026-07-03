# Sparkeefy Wingman

Sparkeefy Wingman helps you figure out what to text in dating and relationship situations.

I have used **DeepSeek**(`deepseek-v4-flash`)

## **Local setup**

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

pip install -r requirements.txt
cp .env.example .env            # add your DeepSeek API key
streamlit run app.py
```

App runs at [http://localhost:8501](http://localhost:8501)

Hosted application at [https://sparkeefy-wingman.streamlit.app/](https://sparkeefy-wingman.streamlit.app/)

Add your API key to `.env`:

```
DEEPSEEK_API_KEY=your_key_here
```



## Configuration


| Variable              | Description          | Default                    |
| --------------------- | -------------------- | -------------------------- |
| `DEEPSEEK_API_KEY`    | DeepSeek API key     | —                          |
| `DEEPSEEK_BASE_URL`   | API base URL         | `https://api.deepseek.com` |
| `DEEPSEEK_MODEL`      | Model ID             | `deepseek-v4-flash`        |
| `WINGMAN_MAX_TOKENS`  | Max response tokens  | `500`                      |
| `WINGMAN_TEMPERATURE` | Sampling temperature | `0.7`                      |


## Output

Each response is structured JSON:


| Field                | Description                                 |
| -------------------- | ------------------------------------------- |
| `energy_read`        | Read on the other person's vibe             |
| `wingman_response`   | Advice in plain language                    |
| `suggested_messages` | 1–3 copy-paste message options              |
| `follow_up_question` | Optional clarifying question                |
| `confidence`         | Model confidence (0–1)                      |
| `safety_flag`        | Set when input/output violates safety rules |




## Project structure

```
app.py                  Streamlit UI
wingman/
  client.py             DeepSeek API client
  config.py             Settings from environment
  prompt.py             System prompt and examples
  safety.py             Input/output safety checks
  schema.py             Response models and validation
  service.py            Application service layer
eval/                   Evaluation dataset (CSV / XLSX)
```



