import os
from PIL import Image, ImageFilter


class ConvertImage:
    def __init__(self, path, folder_path):
        self.image = Image.open(path)
        self.path = path
        self.folder_path = folder_path

        self.image_width, self.image_height = self.image.size
        self.image_name = os.path.splitext(os.path.basename(self.path))[0]
        self.image_type = os.path.splitext(os.path.basename(self.path))[1]

        self.just_type = self.image_type.split(".")[1].upper()

    def convert_image_to_pdf(self, upscale_factor=1):
        convert_image = self.image.convert("RGB")

        if upscale_factor != 1:
            new_width = int(self.image_width * upscale_factor)
            new_height = int(self.image_height * upscale_factor)
            convert_image = convert_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        convert_image = convert_image.filter(ImageFilter.SHARPEN)
        return convert_image

    def save_image(self, upscale_factor=1, quality=100):
        image_converted = self.convert_image_to_pdf(upscale_factor)
        new_folder = self.folder_path
        new_path = os.path.join(new_folder, self.image_name)

        if self.image_type.lower() not in [".png", ".jpg", ".bmp"]:
            raise TypeError(f"Invalid image '{self.image_name}' :  only PNG / JPG / BMP files are supported")
        else:
            if not os.path.exists(new_folder):
                os.makedirs(new_folder)

        image_converted.save(f"{new_path}.pdf", quality=quality)
        return os.path.exists(f"{new_path}.pdf")
