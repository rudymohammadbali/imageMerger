import argparse
import math

from PIL import Image


def open_images(image_paths):
    images = []
    for img_path in image_paths:
        try:
            img = Image.open(img_path)
            images.append(img)
        except IOError:
            print(f"Invalid image: {img_path}")
            return None
    return images


def resize_images(images, width, height):
    return [img.resize((width, height)) for img in images]


def merge_images(images, grid_size, width, height):
    new_img = Image.new("RGBA", (width * grid_size, height * grid_size))
    for i, img in enumerate(images):
        row = i // grid_size
        col = i % grid_size
        new_img.paste(img, (width * col, height * row))
    return new_img


def save_image(image):
    try:
        image.save("merged.png", format="PNG")
        print("Image merged successfully.")
    except IOError:
        print("Could not save image. Please check if the disk is not full or if the file path is valid.")
        return False
    return True


def main(image_paths):
    if not image_paths:
        print("No image paths provided.")
        return
    images = open_images(image_paths)
    if images is None:
        print("Could not open one or more images.")
        return
    width, height = images[0].size
    resized_images = resize_images(images, width, height)
    grid_size = math.ceil(math.sqrt(len(images)))
    merged_image = merge_images(resized_images, grid_size, width, height)
    if not save_image(merged_image):
        print("Could not save the merged image.")
        return


# Usage:
# main(["image1.png", "image2.png", "image3.png", "image4.png"])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Merge images.')
    parser.add_argument('image_paths', nargs='+', help='Paths to the images to merge')
    args = parser.parse_args()
    main(args.image_paths)
