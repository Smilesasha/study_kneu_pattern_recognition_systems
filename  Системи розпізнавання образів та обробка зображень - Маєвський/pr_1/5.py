import time
from PIL import Image


def settle(n):
    """Обмежує значення кольору в межах 0–255."""
    return int(max(0, min(255, n)))


def recolor(r, g, b):
    """Перефарбовує піксель у фіолетову гаму (твій авторський стиль)."""
    # R та B масштабуються, G занулюється
    return (
        settle(r * 255 / 256),
        0,
        settle(b * 255 / 256)
    )


def get_edge_pixel(pixels, x, y, width, height, painted=False):
    """
    Аналізує область 3x3 навколо пікселя (x, y) для пошуку контурів.
    """
    pixels_nearby = []

    # Збір сусідніх пікселів з перевіркою меж (замість повільного try/except)
    for di in range(-1, 2):
        for dj in range(-1, 2):
            nx, ny = x + di, y + dj
            if 0 <= nx < width and 0 <= ny < height:
                pixels_nearby.append(pixels[nx, ny])

    total_delta = 0
    n = len(pixels_nearby)

    # Спрощена, але ефективна логіка дельти (яскравісна різниця)
    for current in pixels_nearby:
        curr_r, curr_g, curr_b = current[:3]
        for other in pixels_nearby:
            oth_r, oth_g, oth_b = other[:3]
            # Обчислюємо різницю яскравості
            delta = (abs(oth_r - curr_r) + abs(oth_g - curr_g) + abs(oth_b - curr_b)) / 3
            total_delta += delta

    # Усереднюємо різницю
    res_val = total_delta / (n * n)

    if painted:
        return recolor(res_val, res_val, res_val)

    res_val = settle(res_val)
    return (res_val, res_val, res_val)


def process_image(input_path, output_path, use_recolor=True):
    """Головна функція обробки."""
    try:
        start_time = time.time()

        with Image.open(input_path) as img:
            img = img.convert("RGB")  # Гарантуємо роботу з 3 каналами
            width, height = img.size
            pixels = img.load()

            # Створюємо нове полотно (Верх: оригінал, Низ: результат)
            combined_img = Image.new('RGB', (width, height * 2))
            new_pixels = combined_img.load()

            print(f"🚀 Processing {width}x{height} image...")

            for x in range(width):
                for y in range(height):
                    # 1. Копіюємо оригінал у верхню частину
                    new_pixels[x, y] = pixels[x, y]

                    # 2. Обробляємо та записуємо в нижню частину
                    new_pixels[x, y + height] = get_edge_pixel(
                        pixels, x, y, width, height, painted=use_recolor
                    )

                # Прогрес-бар для терміналу (кожні 10%)
                if x % (width // 10) == 0:
                    print(f"📊 Progress: {int(x / width * 100)}%")

            combined_img.save(output_path)

            end_time = time.time()
            print(f"✅ Done! Saved as {output_path}")
            print(f"⏱ Time taken: {end_time - start_time:.2f} seconds")
            combined_img.show()

    except FileNotFoundError:
        print("❌ Error: File 'ris1.jpg' not found.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")


# Виклик скрипта
if __name__ == "__main__":
    process_image("1.png", "final_1.png", use_recolor=True)