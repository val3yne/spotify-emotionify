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

# Emotion playlists
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

# Spotify connection - extended scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope="playlist-read-private user-read-currently-playing user-read-recently-played user-top-read"
))

# Save emotion history
def save_emotion_history(emotion):
    """Save user's emotion with timestamp"""
    history_file = "emotion_history.json"
    
    try:
        with open(history_file, 'r') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []
    
    entry = {
        "emotion": emotion,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M")
    }
    
    history.append(entry)
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=2)
    
    print(f"✓ Emotion saved to history!")

# Emotion statistics
def show_emotion_stats():
    """Show emotion history statistics"""
    try:
        with open("emotion_history.json", 'r') as f:
            history = json.load(f)
        
        if not history:
            print("\n📊 No emotion history yet!")
            return
        
        print("\n Your Emotion Statistics:")
        print(f"Total entries: {len(history)}")
        
        # Emotion counts
        emotion_counts = {}
        for entry in history:
            emotion = entry['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        print("\n Emotion breakdown:")
        for emotion, count in sorted(emotion_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(history)) * 100
            print(f"  {emotion}: {count} times ({percentage:.1f}%)")
        
        # Last 5 entries
        print("\n Last 5 emotions:")
        for entry in history[-5:][::-1]:
            print(f"  {entry['timestamp']} - {entry['emotion']}")
            
    except FileNotFoundError:
        print("\n No emotion history yet!")

# Currently playing track
def get_current_track():
    """Show currently playing track"""
    try:
        current = sp.current_playback()
        if current and current['is_playing']:
            track = current['item']
            print(f"\n Currently playing:")
            print(f"  {track['name']} - {track['artists'][0]['name']}")
            
            # Track's audio features
            features = sp.audio_features(track['id'])[0]
            if features:
                print(f"\n Track mood analysis:")
                print(f"  Happiness level: {features['valence']*100:.0f}%")
                print(f"  Energy level: {features['energy']*100:.0f}%")
                print(f"  Danceability: {features['danceability']*100:.0f}%")
                print(f"  Tempo: {features['tempo']:.0f} BPM")
        else:
            print("\n🎵 No track currently playing")
    except Exception as e:
        print(f"Could not fetch current track: {e}")

# Main menu
def main_menu():
    while True:
        print("\n" + "="*50)
        print(" SPOTIFY EMOTION TRACKER ")
        print("="*50)
        print("\n1. Log my emotion & get playlist")
        print("2. Show my emotion statistics")
        print("3. What am I listening to now?")
        print("4. Exit")
        
        choice = input("\nChoose an option (1-4): ").strip()
        
        if choice == "1":
            emotion = input("\nHow are you feeling right now? (Happy/Sad/Angry/Overwhelmed/Worse): ").title()
            
            if emotion in emotion_playlists:
                # Save emotion
                save_emotion_history(emotion)
                
                # Show playlist
                playlist_id = emotion_playlists[emotion]
                try:
                    playlist = sp.playlist(playlist_id, market="from_token")
                    print(f"\n{messages[emotion]}")
                    print(f"🎵 Playlist: {playlist['name']}")
                    print(f"📝 Description: {playlist.get('description', 'No description')}")
                    print(f"🎶 Total tracks: {playlist['tracks']['total']}")
                    print("\n🎶 Top 10 songs:")
                 for i, item in enumerate(playlist['tracks']['items'][:10], 1):
                        track = item.get("track")
                      if not track:
                      continue
                    name = track["name"]
                    artist = track["artists"][0]["name"]
                    print(f"  {i}. {name} - {artist}")

                except Exception as e:
                    print("Error accessing playlist:", e)
            else:
                print("\n Invalid emotion. Please choose: Happy, Sad, Angry, Overwhelmed, or Worse")
        
        elif choice == "2":
            show_emotion_stats()
        
        elif choice == "3":
            get_current_track()
        
        elif choice == "4":
            print("\n Take care! See you soon <3")
            break
        
        else:
            print("\n Invalid option. Please choose 1-4")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n Goodbye! Take care <3")
    except Exception as e:
        print(f"\n An error occurred: {e}")

