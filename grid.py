
from PIL import Image, ImageDraw

img = Image.open("drdriving.png").convert("RGB")
draw = ImageDraw.Draw(img)

width, height = img.size

# Vertical grid every 100 pixels
for x in range(0, width + 1, 100):
    draw.line((x, 0, x, height), fill="red", width=1)
    draw.text((x + 3, 5), str(x), fill="red")

# Horizontal grid every 100 pixels
for y in range(0, height + 1, 100):
    draw.line((0, y, width, y), fill="red", width=1)
    draw.text((5, y + 3), str(y), fill="red")

img.save("drdriving_grid.png")

print(f"Created grid: {width} x {height}")
