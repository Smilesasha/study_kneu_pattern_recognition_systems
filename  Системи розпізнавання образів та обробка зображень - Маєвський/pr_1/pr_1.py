from PIL import Image

def shift_colors(input_path, output_path):
    with Image.open(input_path) as im:
        im = im.convert("RGB")
        pixels = im.load()
        x, y = im.size

        for i in range(x):
            for j in range(y):
                # Безпечне розпакування (тільки 3 канали)
                r, g, b = pixels[i, j]
                # Змінюємо порядок на G, B, R
                pixels[i, j] = (g, b, r)

        im.save(output_path)

shift_colors("1.png", "2.png")