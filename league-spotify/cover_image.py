import requests
from PIL import Image
from io import BytesIO

class ImageProcessor:
    @staticmethod
    def download_image(url):
        """
        Downloads an image from a URL and returns it as a PIL.Image object.

        :param url: URL of the image to download.
        :return: PIL.Image object if successful, None otherwise.
        """
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise HTTPError for bad responses
            image = Image.open(BytesIO(response.content))
            return image
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return None

    @staticmethod
    def resize_and_grayscale_image(image, size=(16, 8)):
        """
        Resizes a given PIL.Image object to the specified size.

        :param image: PIL.Image object to resize.
        :param size: Tuple specifying the new size (width, height).
        :return: Resized PIL.Image object.
        """
        try:
            resized_image = image.resize(size, reducing_gap=2, resample=Image.Resampling.BILINEAR)
            grayscale_image = resized_image.convert('L')  # Convert to grayscale
            return grayscale_image
        except Exception as e:
            print(f"Error resizing image: {e}")
            return None
    
    @staticmethod
    def process_grayscale_image(image):
        """
        Processes a grayscale image to map pixel values to numbers from 0 to 5 based on brightness,
        and returns the concatenated string of these values.

        :param image: Grayscale PIL.Image object.
        :return: Concatenated string of numbers representing pixel brightness levels.
        """
        try:
            pixels = list(image.getdata())
            width, height = image.size
            processed_string = ""

            for i in range(height):
                for j in range(width):
                    pixel_value = pixels[i * width + j]
                    mapped_value = round(pixel_value / (255/3))  # Map 0-255 to 0-3 (inclusive)
                    match mapped_value:
                        case 0:
                            processed_string += '░'
                        case 1:
                            processed_string += '▒'
                        case 2:
                            processed_string += '▓'
                        case 3:
                            processed_string += '█'
                processed_string += '　'*(37-16) + '\n'

            return processed_string
        except Exception as e:
            print(f"Error processing grayscale image: {e}")
            return None
