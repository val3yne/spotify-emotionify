# Emotionify

**Spotify Emotionify** is a Python application that tracks your emotions and recommends personalized Spotify playlists based on your current mood.

Built with Spotipy and the Spotify Web API, it turns your feelings into music — and keeps your emotional story over time. 


## Features

-  **Mood-Based Playlists** — Instant Spotify playlist recommendations based on your emotions  
-  **Emotion Tracking** — Log and track your moods over time  
-  **Statistics Dashboard** — Visual breakdown of your emotional patterns  
-  **Real-Time Analysis** — Mood analysis of your currently playing tracks  
-  **Local Storage** — Emotion history stored locally in JSON format  


### Prerequisites

- Python 3.7+
- A Spotify account
- Spotify Developer credentials


### Installation

#### 1. Clone the repository
git clone https://github.com/yourusername/spotify-emotionify.git cd spotify-emotionify

## Install dependencies:

pip install -r requirements.txt


## Create a Spotify app at https://developer.spotify.com/dashboard

Add the following Redirect URI:

http://localhost:8888/callback

## Create a .env file in the project root:

SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback


## Run the application:
python main.py
