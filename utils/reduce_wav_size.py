import sys
import os
from pydub import AudioSegment

# Check if the input folder is provided as an argument
if len(sys.argv) < 2:
    print("Usage: python reduce_wav_size.py <input_folder>")
    sys.exit(1)

# Get the input folder from the arguments
input_folder = sys.argv[1]

# Check if the folder exists
if not os.path.isdir(input_folder):
    print(f"Folder {input_folder} not found.")
    sys.exit(1)

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
