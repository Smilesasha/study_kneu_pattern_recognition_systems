from PIL import Image

im = Image.open("1.png")


w, h = im.size
small_im = im.resize((w // 2, h // 2))

flipped_im = im.transpose(Image.FLIP_LEFT_RIGHT)

rotated_im = im.rotate(45, expand=True, fillcolor="white")

small_im.save("small.png")
flipped_im.save("flipped.png")
rotated_im.save("rotated.png")