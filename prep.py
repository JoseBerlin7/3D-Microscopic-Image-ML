import pyapr
from skimage import io

filename = '5-8F_ClearT_001.tif'
img = io.imread(f"3D cells/{filename}")

apr, parts = pyapr.converter.get_apr(img)

pyapr.io.write(f'APR files/{filename[:-4]}.apr', apr, parts)