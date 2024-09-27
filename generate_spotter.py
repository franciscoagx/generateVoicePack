import os
import random
import subprocess
import requests
import json
from pathlib import Path
import argparse

def parse_arguments():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate audio samples using elevenlabs.io API."
    )
    parser.add_argument(
        "--eleven_labs_api_key", type=str, required=True, help="Eleven Labs API key"
    )
    parser.add_argument(
        "--voice_name", type=str, required=True, help="Your custom name for this voice"
    )
    parser.add_argument(
        "--voice_id",
        type=str,
        required=True,
        help="ID of the voice from the elevenlabs 'Voices' page",
    )
    parser.add_argument(
        "--subtitles_file",
        type=str,
        default="spotter_subtitles.json",  # Default filename
        help="Path to the spotter_subtitles.json file (default: spotter_subtitles.json)",
    )
    return parser.parse_args()

def load_phrases(subtitles_file: str) -> dict:
    # Load phrases from the JSON file
    if not os.path.exists(subtitles_file):
        raise FileNotFoundError(f"The file '{subtitles_file}' does not exist.")
    with open(subtitles_file, "r") as f:
        data = json.load(f)
    return data

def generate_audio_samples(
    eleven_labs_api_key: str, voice_name: str, voice_id: str, phrases: dict
) -> None:
    output_base_dir = Path(f"spotter_{voice_name}")  # Base directory
    output_base_dir.mkdir(parents=True, exist_ok=True)  # Create the directory

    for category, phrases_list in phrases.items():
        for phrase_key, variants in phrases_list.items():
            phrase_dir = output_base_dir / category / phrase_key
            phrase_dir.mkdir(parents=True, exist_ok=True)
            
            subtitles = []  # List to store subtitle lines
            audio_index = 1  # Counter for audio filenames

            for variant in variants:
                for idx in range(1, 4):  # 3 variations
                    variant_with_quotes = f'"{variant}"'  # Add quotes
                    audio_filename = f"{phrase_key}_{audio_index}.wav"  # Audio filename
                    subtitles.append(f"{audio_filename},{variant_with_quotes}")  # Add subtitle line
                    generate_speech_elevenlabs(
                        eleven_labs_api_key=eleven_labs_api_key,
                        text=variant_with_quotes,
                        voice_name=voice_name,
                        voice_id=voice_id,
                        output_dir=phrase_dir,
                        output_filename=f"{phrase_key}_{audio_index}",
                    )
                    audio_index += 1  # Increment counter

            # Create subtitle file
            subtitles_file_path = phrase_dir / "subtitles.txt"
            with open(subtitles_file_path, "w") as f:
                f.write("\n".join(subtitles))

    print(f"Audio sample generation complete for {voice_name} in {output_base_dir}")

def generate_speech_elevenlabs(
    eleven_labs_api_key: str,
    text: str,
    voice_name: str,
    voice_id: str,
    output_dir: Path,
    output_filename: str,
) -> None:
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    payload = {
        "text": text.strip() + ".",
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            "style": 0.6,
            "use_speaker_boost": True,
        },
        "seed": random.randrange(1, 9999999),
    }
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": eleven_labs_api_key,
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        full_output_filename = f"{output_dir}/{output_filename}.mp3"
        with open(full_output_filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"Generated {full_output_filename}")
        
        # Convert to WAV and trim silence
        convert_mp3_to_wav(full_output_filename, f"{output_dir}/{output_filename}.wav")
        remove_file(full_output_filename)  # Cleanup MP3 file
    else:
        print(f"Error from Eleven Labs API: {response.status_code} - {response.text}")

def convert_mp3_to_wav(input_file: str, output_file: str) -> None:
    ffmpeg_command = ["ffmpeg", "-y", "-i", input_file, output_file]

    try:
        subprocess.run(ffmpeg_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")

def remove_file(file_path: str) -> None:
    path = Path(file_path)
    path.unlink()

if __name__ == "__main__":
    args = parse_arguments()
    print("Generating audio samples using Eleven Labs API...")
    phrases = load_phrases(args.subtitles_file)
    generate_audio_samples(args.eleven_labs_api_key, args.voice_name, args.voice_id, phrases)
