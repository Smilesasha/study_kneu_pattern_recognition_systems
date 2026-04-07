from PIL import Image

im = Image.open("1.png").convert("RGB")
pixels = im.load()
x, y = im.size

factor = 50

for i in range(x):
    for j in range(y):
        r, g, b = pixels[i, j]

        new_r = min(255, r + factor)
        new_g = min(255, g + factor)
        new_b = min(255, b + factor)


        pixels[i, j] = (new_r, new_g, new_b)

im.save("bright.png")