
class Colors:
    def __init__(self, color):
        #R G B W A UV
        self.color_name = color

        if color == 'blue_deep':
            self.color = [0, 0, 255, 0, 0, 0]

        elif color == 'blue_cold':
            self.color = [0, 0, 255, 128, 0, 0]

        elif color == 'white_cold':
            self.color = [0, 0, 92, 255, 0, 0]

        elif color == 'white_plain':
            self.color = [0, 0, 0, 255, 0, 0]

        elif color == 'white_warm':
            self.color = [0, 0, 255, 140, 0, 0]

        elif color == 'amber':
            self.color = [0, 41, 0, 0, 255, 0]

        elif color == 'orange':
            self.color = [255, 120, 0, 0, 110, 0]

        elif color == 'yellow':
            self.color = [255, 220, 0, 0, 244, 0]

        elif color == 'red':
            self.color = [255, 0, 0, 0, 0, 0]

        elif color == 'magenta':
            self.color = [142, 0, 0, 0, 0, 255]

        elif color == 'purple':
            self.color = [211, 25, 255, 0, 0, 255]

        elif color == 'uv':
            self.color = [0, 0, 0, 0, 0, 255]

        elif color == 'turquoise':
            self.color = [0, 255, 158, 0, 0, 255]

        elif color == 'nothing':
            self.color = [0, 0, 0, 0, 0, 0]

    def get_color(self):
        return self.color

    def get_color_name(self):
        return self.color_name

