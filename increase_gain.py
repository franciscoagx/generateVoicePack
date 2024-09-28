import os
import argparse
from pydub import AudioSegment

def increase_gain(input_folder: str, gain_db: float) -> None:
    output_folder = f"{input_folder}_gain"
    os.makedirs(output_folder, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.wav'):
                input_file_path = os.path.join(root, file)
                audio = AudioSegment.from_wav(input_file_path)
                # Increase the gain
                louder_audio = audio + gain_db

                # Create the folder structure in the output folder
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                output_file_path = os.path.join(output_subfolder, file)
                louder_audio.export(output_file_path, format='wav')
                print(f"Increased gain for {input_file_path} to {output_file_path}")

if __name__ == "__main__":
    # argparse configuration
    parser = argparse.ArgumentParser(description="Increase gain of WAV files in a folder.")
    parser.add_argument('--input_folder', required=True, help="Path to the input folder containing WAV files")
    parser.add_argument('--gain', type=float, required=True, help="Gain value in dB (e.g., 5 for +5dB)")

    args = parser.parse_args()

    # Call the function with provided arguments
    increase_gain(args.input_folder, args.gain)
