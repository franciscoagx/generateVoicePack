import os
import argparse
from pydub import AudioSegment

def process_wav_files(input_folder):
    # Create the output folder with the prefix "reduced_"
    output_folder = os.path.join(os.path.dirname(input_folder), "reduced_" + os.path.basename(input_folder))
    os.makedirs(output_folder, exist_ok=True)

    # Walk through all directories and subdirectories in the input folder
    for root, dirs, files in os.walk(input_folder):
        # Construct the relative path from the root directory
        relative_path = os.path.relpath(root, input_folder)
        output_subfolder = os.path.join(output_folder, relative_path)

        # Ensure the same folder structure in the output directory
        os.makedirs(output_subfolder, exist_ok=True)

        # Process each WAV file in the current directory
        for filename in files:
            if filename.endswith(".wav"):
                input_file = os.path.join(root, filename)
                output_file = os.path.join(output_subfolder, filename)  # Keep the same filename in the output

                # Load the input WAV file
                audio = AudioSegment.from_wav(input_file)

                # Reduce the sample rate to 32 kHz and keep bit depth at 16 bits
                audio = audio.set_frame_rate(32000).set_sample_width(2)  # 2 bytes = 16 bits

                # Export the modified file
                audio.export(output_file, format="wav")
                print(f"Processed: {input_file} -> {output_file}")

    print(f"All files have been processed and saved to: {output_folder}")

if __name__ == "__main__":
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Reduce the size of WAV files by changing the sample rate and bit depth.")
    parser.add_argument('--input_folder', required=True, help="Path to the input folder containing WAV files.")
    
    args = parser.parse_args()

    # Check if the folder exists
    if not os.path.isdir(args.input_folder):
        print(f"Folder {args.input_folder} not found.")
        sys.exit(1)

    # Process the WAV files in the input folder
    process_wav_files(args.input_folder)
