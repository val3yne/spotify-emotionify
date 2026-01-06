import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

HISTORY_FILE = "emotion_history.json"

emotion_playlists = {
    "Happy": "5iR7JBR9Ot6ZPgs4GaPOm2",
    "Sad": "3Kd8XtyN0CmFVZ0SxJTi37",
    "Angry": "5ymqBA8vZSnPEZfDJeuhH1",
    "Overwhelmed": "1LWyQBS7lXGMvHg17m8udS",
    "Worse": "3vleBofUVfr7nfyYLgyPUZ"
}

messages = {
    "Happy": "Here is a happy playlist just for you <3",
    "Sad": "Here is a sad playlist just for you, hope you are doing better soon <3",
    "Angry": "Here is your angry playlist, please calm down a little !!",
    "Overwhelmed": "Here is a playlist to help you relax and feel better",
    "Worse": "You just need to listen to some rock and rock your body. Here you go!!"
}

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-read-private user-read-currently-playing user-read-recently-played user-top-read"
))

# JSON

def load_emotion_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_emotion_history(emotion):
    history = load_emotion_history()
    now = datetime.now()

    history.append({
        "emotion": emotion,
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M")
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print(" Emotion saved successfully.")

# Stats

def show_emotion_stats():
    history = load_emotion_history()
    if not history:
        print("\n No emotion history yet.")
        return

    print("\n Your Emotion Statistics")
    print(f"Total entries: {len(history)}")

    emotion_counts = {}
    for entry in history:
        emotion_counts[entry["emotion"]] = emotion_counts.get(entry["emotion"], 0) + 1

    print("\n Emotion breakdown:")
    for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(history)) * 100
        print(f"  {emotion}: {count} times ({percentage:.1f}%)")

    print("\n Last 5 emotions:")
    for entry in history[-5:][::-1]:
        print(f"  {entry['date']} {entry['time']} - {entry['emotion']}")

# Current Track

def get_current_track():
    try:
        current = sp.current_playback()
        if not current:
            print("\n🎵 Spotify is open but nothing is playing.")
            return

        if current["is_playing"]:
            track = current["item"]
            print(f"\n Currently playing:")
            print(f"  {track['name']} - {track['artists'][0]['name']}")

            features = sp.audio_features(track["id"])[0]
            if features:
                print("\n Track mood analysis:")
                print(f"  Happiness: {features['valence']*100:.0f}%")
                print(f"  Energy: {features['energy']*100:.0f}%")
                print(f"  Danceability: {features['danceability']*100:.0f}%")
                print(f"  Tempo: {features['tempo']:.0f} BPM")
        else:
            print("\n No track currently playing.")
    except Exception as e:
        print("Could not fetch current track:", e)

# Main menu
def main_menu():
    while True:
        print("\n" + "="*50)
        print("🎭 SPOTIFY EMOTION TRACKER")
        print("="*50)
        print("\n1. Log my emotion & get playlist")
        print("2. Show my emotion statistics")
        print("3. What am I listening to now?")
        print("4. Exit")

        choice = input("\nChoose (1-4): ").strip()

        if choice == "1":
            emotion = input("How are you feeling? (Happy/Sad/Angry/Overwhelmed/Worse): ").strip().capitalize()
            if emotion not in emotion_playlists:
                print("Please choose a valid emotion.")
                continue

            save_emotion_history(emotion)

            playlist_id = emotion_playlists[emotion]
            try:
                playlist = sp.playlist(playlist_id, market="from_token")
                print(f"\n{messages[emotion]}")
                print(f"🎵 Playlist: {playlist['name']}")
                print(f"📝 Description: {playlist.get('description', 'No description')}")
                print(f"🎶 Total tracks: {playlist['tracks']['total']}")
                print("\n🎶 Top 10 songs:")

                for i, item in enumerate(playlist["tracks"]["items"][:10], 1):
                    track = item.get("track")
                    if not track:
                        continue
                    print(f"  {i}. {track['name']} - {track['artists'][0]['name']}")

            except Exception as e:
                print("Error accessing playlist:", e)

        elif choice == "2":
            show_emotion_stats()

        elif choice == "3":
            get_current_track()

        elif choice == "4":
            print("\nTake care, see you soon.")
            break
        else:
            print("Please choose a number between 1-4.")

if __name__ == "__main__":
    main_menu()


