
# Emotion-Based Music Recommender

A FastAPI app that detects your emotion via webcam and suggests Spotify songs based on that emotion — with music previews playable right in the browser.

---

## Features

* Webcam emotion detection using DeepFace
* Spotify API integration for genre-based music recommendation
* Play song previews directly on the page
* Modular code structure (`spotify.py` handles Spotify API logic)

---

## Requirements

* Python 3.8 or higher
* [Spotify Developer Account](https://developer.spotify.com/dashboard/)
* ffmpeg installed (optional, only if needed by DeepFace or media handling)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create and activate a virtual environment (recommended)

```bash
python3 -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

> Make sure your `requirements.txt` includes:
>
> ```
> fastapi
> uvicorn
> deepface
> opencv-python
> numpy
> spotipy
> python-dotenv
> ```

### 4. Set up environment variables

Create a `.env` file in the root directory with your Spotify API credentials:

```env
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

You can get these by creating an app on the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/).

### 5. Run the FastAPI server

```bash
uvicorn main:app --reload
```

The app will be available at: `http://localhost:8000`

### 6. Open your browser

Visit `http://localhost:8000` to see the app. Allow webcam access when prompted.

---

## Project Structure

```
/public             # Static files like index.html, CSS, JS
main.py             # FastAPI application entrypoint
spotify.py          # Spotify API utility module
.env                # Environment variables (not committed)
requirements.txt    # Python dependencies
```

---

## Notes

* Make sure your webcam is accessible and allowed for the browser.
* Emotion detection works best with clear, frontal face images.
* The app fetches 10 random songs per detected emotion genre to keep recommendations fresh.
* To add more songs or customize genres, edit the `emotion_to_genre` dict and `spotify.py` logic.

