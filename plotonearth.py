from PIL import Image, ImageDraw
import random

IMAGE_PATH = "earth5400x2700.png"
image = Image.open(IMAGE_PATH)
earthangularvelocity = -0.225/2

def plot_coordinates_on_image(file_name, radius=8):
    earthrotate = 0

    width, height = image.size

    print(f"Image width: {width}")
    print(f"Image height: {height}")

    draw = ImageDraw.Draw(image)

    orz = True
    with open(file_name, "r") as file:
        pixel_coords = []
        for line in file:
            if orz:
                orz = False
                continue
            line = line.strip()
            if "	" in line:
                x, y = line.split("	")
            else:
                x, y = line.split()
            x = float(x)+earthrotate
            while(x >= 360):
                x-=360
            while(x < 0):
                x+=360
            pixel_coords.append((float(x), float(y)))
            earthrotate+=earthangularvelocity

    # r = random.randint(100, 255)
    # g = random.randint(100, 255)
    # b = random.randint(100, 255)
    r = 255
    g = 200
    b = 30
    for x, y in pixel_coords:
        x_pixel = int(round(float(x)/360*width))
        y_pixel = -int(round((float(y)-90)/180*height))
        print(x_pixel,y_pixel)
        draw.ellipse((x_pixel - radius, y_pixel - radius, x_pixel + radius, y_pixel + radius), fill=(r, g, b))


# plot_coordinates_on_image("polar_data.txt")
# plot_coordinates_on_image("polar_data2.txt")
# plot_coordinates_on_image("polar_data3.txt")
# plot_coordinates_on_image("polar_data4.txt")
# plot_coordinates_on_image("polar_data5.txt")
# plot_coordinates_on_image("polar_data6.txt")
# plot_coordinates_on_image("polar_data7.txt")
# plot_coordinates_on_image("polar_data8.txt")
plot_coordinates_on_image("polar_data9.txt")
image.show()
image.close()