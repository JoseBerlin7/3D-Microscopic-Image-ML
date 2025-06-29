import pyapr
from skimage import io
import os

input_dir = "3D cells"
output_dir = "APR files"

os.makedirs(output_dir, exist_ok=True)

for filename in os.listdir(input_dir):
    if filename.endswith('.tif'):
        try: 
            file_path = os.path.join(input_dir,filename)
            output_path = os.path.join(output_dir,filename[:-4]+'.apr')

            print(f"Processing {filename}")

            img = io.imread(file_path)

            apr, parts = pyapr.converter.get_apr(img)

            pyapr.io.write(output_path,apr, parts)

            print(f"Success {output_path}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")




