from dataclasses import dataclass
from PIL import Image, ImageDraw

@dataclass
class Coordinate:
    x: int
    y: int

class UsbMouseData(object):
    def __init__(self, raw_string_data):
        mapped =map(lambda x: int(x, 16), raw_string_data.split(":"))
        arr = list(mapped) #exhaustion
        if len(arr) != 4:
            raise ValueError("Error: Incorrect format")
        self.is_clicked = arr[1] & 1
        self.x          = self.twos_complement(arr[2])
        self.y          = self.twos_complement(arr[3])

    #11 11 11 11
    #00 00 00 00  ~
    #          1

    @staticmethod
    def twos_complement(val, bits = 8):
        if (val & (1 << (bits - 1))) != 0:
            val = val - (1 << bits)

        return val

###########################################
def draw_dot(draw_obj, x, y, radius = 1):
    draw_obj.ellipse((x - radius, y - radius, x + radius, y + radius), fill = 0)


def create_mouse_outline(input_path, output_path):
    with open(input_path) as f:
        img_size = 2000
        img = Image.new("L", (img_size, img_size),255 )
        draw_obj = ImageDraw.Draw(img)
        position = Coordinate(int(img_size * 0.05), int(img_size * 0.2))

        for line in f:
            try:
                line = line.rstrip()
                data = UsbMouseData(line)

                position.x += data.x
                position.y += data.y

                if data.is_clicked:
                    draw_dot(draw_obj, position.x, position.y, radius = 2)
            except:
                print ("Error with line: {}".format(line))
                pass

        img.save(output_path)

if __name__ == "__main__":
    create_mouse_outline("capture_data.txt", "res.png")