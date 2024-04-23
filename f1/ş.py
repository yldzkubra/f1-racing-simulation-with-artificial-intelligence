from PIL import Image

# Open an image file
with Image.open("zx.png") as img:
    # Resize the image
    resized_img = img.resize((1300, 800))
    # Save the resized image
    resized_img.save("back.png")

# Provide the path to the resized image
"back.png"
