# generateVoicePack

## Description

Generate voice packs for CrewChief using ElevenLabs API

## Requirements

1. Clone the repository:
    ```bash
    git clone https://github.com/franciscoagx/generateVoicePack.git
    cd generateVoicePack
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # For macOS/Linux
    myenv\Scripts\activate     # For Windows
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


# Generate spotter audios (generate_spotter.py)
This script generates audio samples using the Eleven Labs API. It takes command-line arguments for the API key, voice ID, custom voice name, and a JSON file containing phrases. The script loads the phrases from the JSON file, organizes them into categories and phrases, and generates multiple audio variants for each phrase using the Eleven Labs text-to-speech API. It saves the audio files in a structured directory and generates corresponding CSV files for each set of audio samples. The script also converts the audio from MP3 to WAV format and removes the original MP3 files after conversion.

Usage:
  ```bash
  python3 generate_spotter.py --eleven_labs_api_key XXXXX --voice_name 'name' --voice_id XXXXX

  ```
Optional args:

**--subtitles_file** *file.json*

default: *data/spotter_subtitles.json*

# Radio filter (radio_filter.py)
This script applies a "radio" effect to WAV audio files within a specified directory. The "radio" effect simulates the sound quality of audio transmitted over a radio by applying a low-pass filter to limit bandwidth and increasing the volume to mimic radio compression. This script increase gain 5 dB

Usage:
  ```bash
  python3 radio_filter.py --input_folder voice
  ```

replace folder name if need

# Reduce wav size (reduce_wav_size.py)
This Python script processes all .wav files within a given directory and its subdirectories, reducing their sample rate and bit depth to create smaller audio files. The script preserves the directory structure by creating a new output folder with the prefix reduced_, where all processed audio files are saved with the same filenames and folder hierarchy.

Usage:
  ```bash
  python3 reduce_wav_size.py --input_folder voice
  ```

replace folder name if need

# Increase gain (increase_gain.py)
This script increases the gain (volume) of all .wav audio files in a specified folder. It takes two command-line arguments: --input_folder, which is the path to the folder containing the audio files, and --gain, the amount of gain in decibels to apply to each file. The modified audio files are saved in a new folder with the suffix _gain, maintaining the original folder structure.

Usage:
  ```bash
  python3 increase_gain.py --input_folder voice --gain 5
  ```

replace folder name if need