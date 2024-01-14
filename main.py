import argparse
import os

import spotipy
from dotenv import load_dotenv
from moviepy.editor import VideoFileClip
from pytube import Playlist, Search, YouTube
from pytube.exceptions import VideoUnavailable
from spotipy.oauth2 import SpotifyClientCredentials

from logger_config import log


class Youtify:
    FILE_EXTENSION = ".mp3"

    def __init__(self, output_path):
        load_dotenv()
        self.spotipy_client_id = os.getenv("SPOTIPY_CLIENT_ID")
        self.spotipy_client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
        self.output_path = output_path

        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=self.spotipy_client_id,
                client_secret=self.spotipy_client_secret,
            )
        )


    def get_spotify_playlist_tracks(self, spotify_uri):
        results = self.sp.playlist_tracks(spotify_uri)
        return [
            f"{track['track']['name']} - {track['track']['album']['artists'][0]['name']}"
            for track in results["items"]
        ]

    def download_and_convert(self, video):
        try:
            mp4_file = video.streams.first().download(output_path=self.output_path)
            mp3_file = mp4_file[:-4] + self.FILE_EXTENSION

            if not os.path.exists(mp3_file):
                clip = VideoFileClip(mp4_file)
                clip.audio.write_audiofile(mp3_file)
                clip.close()
                log.info(f"{video.title} downloaded and converted to MP3")

            try:
                os.remove(mp4_file)
                log.info(f"{mp4_file} removed")
            except FileNotFoundError:
                log.warning(f"{mp4_file} not found for removal")
        except Exception as e:
            log.error(
                f"Failed to download and convert {video.title}. Error: {str(e)}"
            )

    def search_spotify_track_and_convert_to_mp3(self, song_name):
        try:
            search_result = Search(song_name).results[0]
            video = YouTube(f"http://www.youtube.com/watch?v={search_result.video_id}")
            self.download_and_convert(video)
        except (VideoUnavailable, IndexError):
            log.error(f"{song_name} not found on YouTube or Spotify")

    def download_video_youtube_and_convert_to_mp3(self, playlist_uri):
        try:
            if "list" in playlist_uri:
                p = Playlist(playlist_uri)
                for video_url in p.video_urls:
                    try:
                        self.download_and_convert(YouTube(video_url))
                    except VideoUnavailable:
                        log.error(
                            f"Video at {video_url} not available, skipping to next video."
                        )
            else:
                if "watch" in playlist_uri:
                    self.download_and_convert(YouTube(playlist_uri))
        except VideoUnavailable:
            log.error(f"Video at {playlist_uri} not available")

    def process_playlist_uri(self, playlist_uri):
        if "spotify" in playlist_uri:
            if "playlist" in playlist_uri:
                playlist_tracks = self.get_spotify_playlist_tracks(playlist_uri)
                for song_name in playlist_tracks:
                    self.search_spotify_track_and_convert_to_mp3(song_name)
            else:
                self.search_spotify_track_and_convert_to_mp3(playlist_uri)
        elif "youtube" in playlist_uri:
            self.download_video_youtube_and_convert_to_mp3(playlist_uri)


def run_application():
    parser = argparse.ArgumentParser(
        description="Download and convert videos from Spotify and YouTube to MP3."
    )
    parser.add_argument("uri", type=str, help="The Spotify or YouTube URI to process.")
    parser.add_argument(
        "--output",
        type=str,
        default=os.getcwd(),
        help="The output path for the downloaded files.",
    )
    args = parser.parse_args()

    downloader = Youtify(args.output)
    downloader.process_playlist_uri(args.uri)


if __name__ == "__main__":
    run_application()
