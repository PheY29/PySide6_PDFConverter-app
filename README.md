First application made almost by myself, some notions come from the courses i watched about PySide6, especially the notion of thread/worker to allow background tasks (in this case : image conversion)

I saw that the PIL (pillow) library allows image conversion, so i used this in my code for 3 type of image (.png / .jpg / .bmp), second things, if your image is too small/large, i also wanted to be able to resize it from 50% to 150% of the basic size and for the whole interface, of course PySide6

_________________________________

### How it works

- Drag and drop your images to be converted (a green or red cross will indicate if your file has not yet been converted)
- Choose the size of your document (default : 100%)  
        --> if the selected size is different from 100%, we also run a filter to upscale the image with antialias (using LANCZOS) to try to keep the image as similar as possible
- And press convert (where you choose the destination folder)

![image](https://github.com/user-attachments/assets/cb5e9f47-6af7-449f-bfc0-635fce6a004b) ![image](https://github.com/user-attachments/assets/f10f5176-67ac-4c60-95ea-1e668ff0a2a3)

### Other Infos
- There is a minor visual bug when only one file is placed, the progress bar stops in the middle, i don't understand why, but it works fine.
- To enable the application to be converted from .exe (in 1 file), this piece of code has been added and is used for each image:  ![image](https://github.com/user-attachments/assets/3f42e798-d8ec-4705-8097-16533fa59aa9)

  **QtGui.QIcon(resource_path("_img/checked.png"))**



