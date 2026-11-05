import sys

from PIL import Image

src, dst, maxw = sys.argv[1], sys.argv[2], int(sys.argv[3])
im = Image.open(src)
im.thumbnail((maxw, maxw))
if im.mode in ("RGBA", "LA", "P"):
    im = im.convert("RGBA")
    bg = Image.new("RGB", im.size, (255, 255, 255))
    bg.paste(im, mask=im.split()[-1])
    im = bg
else:
    im = im.convert("RGB")
im.save(dst, "JPEG", quality=88, optimize=True)
