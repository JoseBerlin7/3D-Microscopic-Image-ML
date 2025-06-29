import pyapr
from skimage import io
import tempfile
import os
import fsspec
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()  # loads variables from .env into environment

storage_acc_name = os.getenv("STORAGE_ACC_NAME")
storage_acc_key = os.getenv("STORAGE_ACC_KEY")
container_name = "cell-training-data"
source_dir = "tif files/"
destination_dir = "apr files"

def get_filesystem():
    fs = fsspec.filesystem(
        'az', 
        account_name = storage_acc_name,
        account_key = storage_acc_key
    )

    return fs

def get_tif_files_path():

    fs = get_filesystem()

    all_files = fs.find(f"{container_name}/{source_dir}")
    tif_files = [file for file in all_files if file.endswith('.tif')]

    print(f"Found {len(tif_files)} .tif files")

    return tif_files


def write_apr_files():
    fs = get_filesystem()
    # os.makedirs(destination_dir, exist_ok=True)

    for file_path in get_tif_files_path():
            filename = os.path.basename(file_path)
            output_path = f"{container_name}/{destination_dir}/{filename[:-4]}.apr"

            try:
                print(f"Processing {filename}")

                with fs.open(file_path, 'rb') as f_in:
                    with tempfile.NamedTemporaryFile(suffix='.tif', delete=True) as tmp_tif:
                        tmp_tif.write(f_in.read())
                        tmp_tif_path = tmp_tif.name
                        img = io.imread(tmp_tif_path)
                    
                apr, parts = pyapr.converter.get_apr(img)

                '''
                
                # Testing against a locally stored file
                img1 = io.imread('5-8F_CUBIC_001.tif')
                apr1, parts1 = pyapr.converter.get_apr(img)
                print(f"{apr}\n{apr1}\n\n{parts}\n{apr}")

                '''

                with tempfile.NamedTemporaryFile(suffix='.apr', delete=False) as tmp_apr:
                    tmp_apr_path = tmp_apr.name
                pyapr.io.write(tmp_apr_path, apr, parts)

                with fs.open(output_path, 'wb') as f_out:
                    with open(tmp_apr_path, 'rb') as local_apr_file:
                        f_out.write(local_apr_file.read())


                print(f"Success {output_path}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")
            finally:
                for path in [tmp_tif_path, tmp_apr_path]:
                    if os.path.exists(path):
                        os.remove(path)
                # break


# print(get_tif_files_path())
write_apr_files()