# Worcflow AI

**Worcflow AI** is an AI-powered commitment tracker that analyzes recent email conversations and automatically identifies commitments made by the connected user.

The application connects to Gmail, analyzes recent email threads using an LLM pipeline, and extracts key actionable details so you never miss a deadline buried in your inbox.

---

## ✨ Features

- **Automated Extraction:** Identifies what you committed to do, for whom, and key requirements mentioned in the thread.
- **Recipient Tracking:** Extracts recipient names and email addresses.
- **Due Date Extraction:** Automatically parses target completion dates when available.
- **Smart Dashboard:** Displays active commitments sorted by due date.
- **Google Calendar Integration:** Syncs upcoming commitments directly to Google Calendar with a single click.

---

## 🛠 Tech Stack

- **Backend:** Python 3.10+, FastAPI, LangGraph
- **Frontend:** React, Vite
- **Database:** MongoDB Atlas
- **Integrations:** Gmail API, Google Calendar API
- **LLM Engine:** OpenAI API

---

## 📋 Prerequisites

Ensure you have the following installed and set up before getting started:

- [Python 3.10+](https://www.python.org/)
- [Node.js 18+](https://nodejs.org/) & `npm`
- A [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) account
- A [Google Cloud Console](https://console.cloud.google.com/) project with **Gmail API** and **Google Calendar API** enabled
- An [OpenAI API](https://platform.openai.com/) key

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Purvakalantri/worcflow_product_eng.git
cd worcflow_product_eng
```

---

### 2. Backend Setup

1. **Navigate to the backend directory and set up a virtual environment:**

   ```bash
   cd backend
   python -m venv venv
   ```

2. **Activate the virtual environment:**
   - **Windows:**
     ```cmd
     venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**

   Create a `.env` file in the `backend/` directory and populate it with your credentials:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   MODEL=gpt-4o-mini

   MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=your_database_name
   COLLECTION_NAME=your_collection_name
   ```

---

### 3. Google OAuth & API Setup (Gmail & Calendar)

To allow Worcflow AI to access your Gmail and Google Calendar:

(link: 
Gmail API : https://developers.google.com/workspace/gmail/api/quickstart/python
Calendar API: https://developers.google.com/workspace/calendar/api/quickstart/python)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a new project (or select an existing one).
3. Enable both the **Gmail API** and **Google Calendar API**:
   - Go to **APIs & Services > Library**.
   - Search for **Gmail API** and click **Enable**.
   - Search for **Google Calendar API** and click **Enable**.
4. Configure the OAuth Consent Screen:
   - Go to **APIs & Services > OAuth consent screen**.
   - Select **External** and click **Create**.
   - Fill in the required fields (App Name, User Support Email, Developer Contact Info).
   - Click **Save and Continue**.
   - Under **Test Users / Audience**, click **+ Add Users** and add the Gmail address you plan to connect with the app.
5. Create OAuth Credentials:
   - Go to **APIs & Services > Credentials**.
   - Click **+ Create Credentials** > **OAuth client ID**.
   - Choose Application Type: **Desktop App**.
   - Give it a name (e.g., `Worcflow AI Client`) and click **Create**.
6. Download the Client Secret JSON:
   - Download the generated JSON file.
   - Rename it to **`credentials.json`**.
   - Place `credentials.json` inside the `backend/` directory (where your backend authentication script resides).

---

### 4. MongoDB Setup

1. Log in to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas).
2. Create a new cluster (Free Shared tier is sufficient).
3. Under **Security > Database Access**, create a database user with read/write privileges.
4. Under **Security > Network Access**, add your current IP address (or `0.0.0.0/0` for testing).
5. Go to **Database > Connect > Drivers**, select **Python**, and copy your connection string.
6. Paste the connection string into your `backend/.env` file under `MONGODB_URI`.

---

### 5. OpenAI API Key

1. Go to the [OpenAI Platform Dashboard](https://platform.openai.com/).
2. Navigate to **API Keys** and generate a new secret key.
3. Add the key to `OPENAI_API_KEY` in your `backend/.env` file.

---

### 6. Frontend Setup

1. Open a new terminal window and navigate to the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the Vite development server:

   ```bash
   npm run dev
   ```

---

## 🏃 Running the Application

1. **Start Backend Server:**

   ```bash
   cd backend
   python main.py
   ```

2. **Start Frontend Client:**

   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:5173` to start using Worcflow AI!