import os
import argparse
from pydub import AudioSegment

def radio_effect(audio):
    # Modify the audio to simulate a radio effect
    audio = audio.low_pass_filter(3000)  # Low-pass filter to simulate limited bandwidth
    audio = audio + 10  # Increase volume to simulate radio compression
    return audio

def process_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.lower().endswith('.wav'):
                file_path = os.path.join(root, file)
                
                # Load the audio file
                audio = AudioSegment.from_wav(file_path)
                
                # Apply the radio effect
                audio_with_effect = radio_effect(audio)
                
                # Create the same directory structure in the output directory
                relative_path = os.path.relpath(root, input_dir)
                output_folder = os.path.join(output_dir, relative_path)
                os.makedirs(output_folder, exist_ok=True)
                
                # Save the audio file with effect
                output_file_path = os.path.join(output_folder, file)
                audio_with_effect.export(output_file_path, format='wav')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apply a radio effect to WAV files in a directory.")
    parser.add_argument('--input_folder', required=True, help='Path to the input directory containing WAV files.')
    parser.add_argument('--output_folder', help='Path to the output directory where modified files will be saved. Defaults to the input folder name with "_radio" suffix.')

    args = parser.parse_args()

    # Set default output_folder if not provided
    if not args.output_folder:
        args.output_folder = f"{os.path.basename(args.input_folder)}_radio"
        args.output_folder = os.path.join(os.path.dirname(args.input_folder), args.output_folder)

    process_directory(args.input_folder, args.output_folder)
