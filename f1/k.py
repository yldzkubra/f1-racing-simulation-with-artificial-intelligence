from PIL import Image

# Load the images from the provided file paths
image_path1 = 'i.png'
image_path2 = 'l.png'

# Open the images
image1 = Image.open(image_path1)
image2 = Image.open(image_path2)

# Define the size for the final image
final_size = (1500, 1000)

# Create a new blank image with the desired size
final_image = Image.new('RGB', final_size, color = 'grey')

# Calculate the y-coordinate for the second image placement
y_coordinate = image1.height

# Paste the first and second image onto the final image
final_image.paste(image1, (0,0))
final_image.paste(image2, (0, image1.height))

# Save the final image
final_image_path = 'combined_image.png'
final_image.save(final_image_path)

final_image_path

