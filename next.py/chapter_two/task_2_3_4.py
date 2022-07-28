
class Pixel:
    """
    A class used to represent a Pixel.
    """
    COLORS_INDEX = {
        0: "Red",
        1: "Green",
        2: "Blue"
    }

    def __init__(self, x=0, y=0, r=0, g=0, b=0) -> None:
        self._coords = (x, y)
        self._colors = (r, g, b)

    def set_coords(self, x, y):
        self._coords = (x, y)

    def set_grayscale(self):
        avg = int(sum(self._colors) / len(self._colors))
        self._colors = (avg, avg, avg)

    def print_pixel_info(self):
        """
        Prints a pixel's info, showing the coordinates and (R,G,B) color.
        Also prints the dominant color if such exists.
        A color is dominant if its value is above 50 and the rest are zero.
        """
        color = ""
        if len(list(filter(lambda x: x == 0, self._colors))) == 2:
            color = self.COLORS_INDEX[self._colors.index(
                sum(self._colors))] if sum(self._colors) > 50 else ""

        print(
            f"X: {self._coords[0]}, Y: {self._coords[1]}, Color: {self._colors}{f' {color}' if bool(color) else ''}")


def main():
    p = Pixel(5, 6, 250)
    p.print_pixel_info()
    p.set_grayscale()
    p.print_pixel_info()


if __name__ == "__main__":
    main()
