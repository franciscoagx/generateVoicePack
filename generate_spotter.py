import os
import random
import subprocess
import requests
import json
import csv
from pathlib import Path
import argparse

def parse_arguments():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Generate audio samples using ElevenLabs API."
    )
    parser.add_argument(
        "--eleven_labs_api_key", type=str, required=True, help="ElevenLabs API key"
    )
    parser.add_argument(
        "--voice_name", type=str, required=True, help="Your custom name for this voice"
    )
    parser.add_argument(
        "--voice_id",
        type=str,
        required=True,
        help="ID of the voice from the ElevenLabs 'Voices' page",
    )
    parser.add_argument(
        "--subtitles_file",
        type=str,
        default="data/spotter_subtitles.json",  # Default filename
        help="Path to the spotter_subtitles.json file (default: spotter_subtitles.json)",
    )
    parser.add_argument(
        "--single_version",
        action="store_true",
        help="If provided, generates only one version of audio per phrase",
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
    eleven_labs_api_key: str, voice_name: str, voice_id: str, phrases: dict, single_version: bool
) -> None:
    # Create base directory
    base_dir = Path("voice")
    base_dir.mkdir(parents=True, exist_ok=True)

    # Create directories for spotter and radio_check
    spotter_dir = base_dir / f"spotter_{voice_name}"
    radio_check_dir = base_dir / f"radio_check_{voice_name}"
    
    spotter_dir.mkdir(parents=True, exist_ok=True)
    radio_check_dir.mkdir(parents=True, exist_ok=True)

    # Process spotter phrases
    process_phrases(eleven_labs_api_key, voice_name, voice_id, phrases.get("spotter", {}), single_version, spotter_dir)

    # Process radio_check phrases
    process_phrases(eleven_labs_api_key, voice_name, voice_id, phrases.get("radio_check", {}), single_version, radio_check_dir)

    print(f"Audio sample generation complete for {voice_name} in {base_dir}")

def process_phrases(
    eleven_labs_api_key: str, voice_name: str, voice_id: str, phrases: dict, single_version: bool, output_base_dir: Path
) -> None:
    for phrase_key, variants in phrases.items():  # Accedemos a las frases directamente
        phrase_dir = output_base_dir / phrase_key
        phrase_dir.mkdir(parents=True, exist_ok=True)

        csv_rows = []  # List to store rows for the CSV file
        audio_index = 1  # Counter for audio filenames

        # Determine number of versions to generate based on the --single_version flag
        num_versions = 1 if single_version else (2 if len(variants) >= 5 else 3)

        for variant in variants:  # Iteramos sobre las variantes de cada frase
            for idx in range(1, num_versions + 1):  # 1, 2, or 3 versions depending on the flag
                audio_filename = f"{phrase_key}_{audio_index}.wav"  # Audio filename
                csv_rows.append([audio_filename, variant])  # Add row for CSV file
                generate_speech_elevenlabs(
                    eleven_labs_api_key=eleven_labs_api_key,
                    text=variant,
                    voice_name=voice_name,
                    voice_id=voice_id,
                    output_dir=phrase_dir,
                    output_filename=f"{phrase_key}_{audio_index}",
                )
                audio_index += 1  # Increment counter

        # Create CSV file in the same directory as the WAV files
        csv_file_path = phrase_dir / "subtitles.csv"
        with open(csv_file_path, "w", newline='') as csvfile:
            csv_writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
            for row in csv_rows:
                csv_writer.writerow(row)

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
        print(f"Error from ElevenLabs API: {response.status_code} - {response.text}")

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
    print("Generating audio samples using ElevenLabs API...")
    phrases = load_phrases(args.subtitles_file)
    generate_audio_samples(args.eleven_labs_api_key, args.voice_name, args.voice_id, phrases, args.single_version)
