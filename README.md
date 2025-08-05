## Hotel Feedback Summarizer API

API that accepts hotel guest feedback, categorizes it into key themes (like **Cleanliness**, **Service**, etc.), and provides AI-generated summaries per theme.

---

##  Features

*  Submit feedback via `POST /feedback`
*  Group all feedback into 5 hotel themes via `GET /feedback/themes`
*  Summarize each theme using OpenAI GPT (or fallback if offline)
*  Stats route (`GET /feedback/stats`) shows most common theme and negativity ratio
*  Local or OpenAI-based grouping supported

---

## ⚙️ Setup Instructions

### 1. 📦 Clone & Install

```bash
# TODO add real link
git clone https://github.com/yourusername/hotel-feedback-api.git
cd hotel-feedback-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. ⚙️ Setup `.env`

Create a `.env` file from template:

```bash
cp .env.example .env
```

Edit `.env`:

```env
OPENAI_API_KEY=your-key-here
```

> Set `false` to use local models or keyword fallback.

### 3. 🧱 Initialize DB

```bash
python scripts/init_db.py
```

Or use SQLite manually:

```sql
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guest_id TEXT NOT NULL,
    comment TEXT NOT NULL
);
```

---

## 🧪 Sample Requests (Curl)

###  Add Feedback

```bash
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{"guest_id": "GUEST101", "comment": "The food was amazing but the WiFi didn’t work."}'
```

### 📚 Get Grouped Themes + Summaries

```bash
curl http://localhost:8000/feedback/themes
```

### 📊 Get Stats

```bash
curl http://localhost:8000/feedback/stats
```

---

## 🧠 Grouping Logic

* **Primary**: Uses OpenAI (`gpt-3.5-turbo`) to map feedback to a single theme
* **Fallback**: Keyword-based logic assigns themes if OpenAI is unavailable

Themes supported:

* Cleanliness
* Staff & Service
* Food & Dining
* Location
* Amenities

---

## 📝 Summarization Logic

* Feedbacks are grouped by theme

* Each group is summarized using GPT via a prompt like:

  > “Summarize the following guest feedback about **Staff & Service**...”

---

## 🔎 Example Response

```json
{
  "themes": [
    {
      "name": "Cleanliness",
      "summary": "Most guests praised clean rooms, though a few mentioned bad odors."
    },
    {
      "name": "Staff & Service",
      "summary": "Service was hit or miss. Some praised staff, others mentioned rudeness."
    }
  ]
}
```

---

## 🧪 Testing

```bash
pytest
```

Includes unit tests for:

* Grouping fallback logic
* Theme-to-comment mapping
* Summary formatting

---

## 🛠 Dev Tools

* `FastAPI` for web app
* `SQLite` for local storage
* `transformers` or `sentence-transformers` for local grouping (optional)
* `OpenAI GPT-3.5` for summarization (if enabled)

---
