from PIL import Image
import numpy as np

# Load the distorted image
img = Image.open("location.png")
pixels = np.array(img)
height, width, _ = pixels.shape

# Undo the row-wise shifting to restore the original image
restored = []
shift = 0
for row in pixels:
    restored.append(np.roll(row, -shift, axis=0))  # Shift row back left
    shift = (shift + 5) % width

# Save the restored image
restored_image = Image.fromarray(np.array(restored, dtype=np.uint8))
restored_image.save("restored.png")
