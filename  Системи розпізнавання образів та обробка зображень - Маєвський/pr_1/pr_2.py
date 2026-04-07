from PIL import Image

im = Image.open("1.png").convert("RGB")
pixels = im.load()
x, y = im.size

mode = 'bw'

for i in range(x):
    for j in range(y):
        r, g, b = pixels[i, j]

        if mode == 'bw':
            avg = (r + g + b) // 3
            pixels[i, j] = (avg, avg, avg)

        elif mode == 'negative':
            pixels[i, j] = (255 - r, 255 - g, 255 - b)

im.save("result.png")