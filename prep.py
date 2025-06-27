import tifffile as tiff
import matplotlib.pyplot as plt
import napari

# Load the .tif file
img = tiff.imread("D:/12620078/T-47D_Uncleared_001.tif")  # shape: (Z, Y, X) or (C, Z, Y, X)

print("Image shape:", img.shape)

def plot_view(img):
    plt.imshow(img[img.shape[0]//2], cmap='gray')  # mid z-slice
    plt.title("Middle Z-slice")
    plt.axis('off')
    plt.show()

def interactive_3D_view(img):
    viewer = napari.Viewer()
    viewer.add_image(img, name='3D Cell Image', colormap='gray')
    napari.run()

# plot_view(img)
# interactive_3D_view(img)
print(img)