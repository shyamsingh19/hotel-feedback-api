## Hotel Feedback Summarizer API

API that accepts hotel guest feedback, categorizes it into key themes (like **Cleanliness**, **Service**, etc.), and provides AI-generated summaries per theme
🔗 **Live Demo & Docs:** [https://hotel-feedback-api.onrender.com/docs](https://hotel-feedback-api.onrender.com/docs)

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
git clone https://github.com/shyamsingh19/hotel-feedback-api
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

---

## 🧪 Sample Requests (Curl)

###  Add Feedback

```bash
curl -X POST https://hotel-feedback-api.onrender.com/feedback \
  -H "Content-Type: application/json" \
  -d '{"guest_id": "GUEST101", "comment": "The food was amazing but the WiFi didn’t work."}'
```

### 📚 Get Grouped Themes + Summaries

```bash
curl https://hotel-feedback-api.onrender.com/feedback/themes
```

### 📊 Get Stats

```bash
curl https://hotel-feedback-api.onrender.com/feedback/stats
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

---

## 🛠 Dev Tools

* `FastAPI` for web app
* `SQLite` for local storage
* `OpenAI GPT-3.5` for summarization (if enabled)

---
