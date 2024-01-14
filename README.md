# Youtify

![banner2](https://github.com/Karoll-e/youtify/assets/141882497/3e251c8c-cfcf-407b-980e-a1d3280161d8)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white) 	![YouTube Music](https://img.shields.io/badge/YouTube_Music-FF0000?style=for-the-badge&logo=youtube-music&logoColor=white)

#### This Python script allows you to download and convert Spotify tracks and YouTube videos to MP3.

## How to run
1. Clone the Repository: ```git clone https://github.com/Karoll-e/youtify.git```
2. Create a Virtual Environment: ```python -m venv venv```
3. Activate the Virtual Environment:
   * On Windows: ```venv\Scripts\activate```
   * On macOS and Linux: ```source venv/bin/activate```
4. Install Dependencies: ```pip install -r requirements.txt```
5. Get Spotify Developer credentials → [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api)
6. replace ```os.getenv("SPOTIPY_CLIENT_ID")``` and ```os.getenv("SPOTIPY_CLIENT_SECRET")``` with your Spotify Developer credentials:

## Usage
* Run the script from the command line using the following format:
```
python main.py [URI] --output [OUTPUT_PATH]
```
* Replace ```[URI]``` with the Spotify or YouTube URI you want to process and ```[OUTPUT_PATH]``` with the desired output path for downloaded files.

## Example
```
python main.py https://www.youtube.com/watch?v=dQw4w9WgXcQ --output C:\Users\karoll\Downloads
```

## Contributing
Feel free to contribute to this project. If you find any issues or have suggestions, please open an issue or submit a pull request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
