import os
import argparse
from pydub import AudioSegment
from subprocess import call

def increase_gain(input_folder: str, gain_db: float = None) -> str:
    output_folder = f"{input_folder}_gain"
    os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.wav'):
                input_file_path = os.path.join(root, file)
                audio = AudioSegment.from_wav(input_file_path)

                if gain_db is not None:
                    audio = audio + gain_db

                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                output_file_path = os.path.join(output_subfolder, file)
                audio.export(output_file_path, format='wav')
                if gain_db is not None:
                    print(f"Increased gain for {input_file_path} to {output_file_path}")
                else:
                    print(f"Copied {input_file_path} to {output_file_path} without gain modification")

    return output_folder

def radio_effect(audio):
    audio = audio.low_pass_filter(3000)  # Low-pass filter to simulate limited bandwidth
    audio = audio + 10  # Increase volume to simulate radio compression
    return audio

def apply_radio_effect(input_folder: str) -> str:
    output_folder = f"{input_folder}_radio"
    os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.wav'):
                input_file_path = os.path.join(root, file)
                audio = AudioSegment.from_wav(input_file_path)

                audio_with_effect = radio_effect(audio)

                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                output_file_path = os.path.join(output_subfolder, file)
                audio_with_effect.export(output_file_path, format='wav')
                print(f"Applied radio effect for {input_file_path} to {output_file_path}")

    return output_folder

if __name__ == "__main__":
    # argparse configuration
    parser = argparse.ArgumentParser(description="Process WAV files: optionally increase gain, then apply a radio effect.")
    parser.add_argument('--input_folder', required=True, help="Path to the input folder containing WAV files")
    parser.add_argument('--gain', type=float, help="Gain value in dB (e.g., 5 for +5dB). If not provided, gain will not be modified.")

    args = parser.parse_args()

    # Step 1: Increase Gain if specified
    print("Processing files...")
    gain_output_folder = increase_gain(args.input_folder, args.gain)

    # Step 2: Apply Radio Effect
    print("Applying radio effect...")
    radio_output_folder = apply_radio_effect(gain_output_folder)

    print(f"Processing complete. Final output in: {radio_output_folder}")
