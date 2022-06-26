
class Colors:
    def __init__(self, color):
        #R G B W A UV
        self.color_name = color

        if color == 'blue_deep':
            self.color = [0, 0, 255, 0, 0, 0]
            self.color_fogger = [0, 0, 255]

        elif color == 'blue_cold':
            self.color = [0, 0, 255, 128, 0, 0]
            self.color_fogger = [55, 55, 255]

        elif color == 'white_cold':
            self.color = [0, 0, 92, 255, 0, 0]
            self.color_fogger = [200, 200, 255]

        elif color == 'white_plain':
            self.color = [0, 0, 0, 255, 0, 0]
            self.color_fogger = [255, 255, 255]

        elif color == 'white_warm':
            self.color = [0, 0, 0, 255, 140, 0]
            self.color_fogger = [255, 255, 200]

        elif color == 'amber':
            self.color = [0, 41, 0, 0, 255, 0]
            self.color_fogger = [0, 0, 0]

        elif color == 'orange':
            self.color = [255, 120, 0, 0, 110, 0]
            self.color_fogger = [255, 120, 0]

        elif color == 'yellow':
            self.color = [255, 220, 0, 0, 244, 0]
            self.color_fogger = [255, 220, 0]

        elif color == 'red':
            self.color = [255, 0, 0, 0, 0, 0]
            self.color_fogger = [255, 0, 0]

        elif color == 'magenta':
            self.color = [142, 0, 0, 0, 0, 255]
            self.color_fogger = [0, 0, 0]

        elif color == 'purple':
            self.color = [211, 25, 255, 0, 0, 255]
            self.color_fogger = [211, 25, 255]

        elif color == 'uv':
            self.color = [0, 0, 0, 0, 0, 255]
            self.color_fogger = [0, 0, 0]

        elif color == 'turquoise':
            self.color = [0, 255, 158, 0, 0, 255]
            self.color_fogger = [0, 255, 158]

        elif color == 'nothing':
            self.color = [0, 0, 0, 0, 0, 0]
            self.color_fogger = [0, 0, 0]

    def get_color(self):
        return self.color
    
    def get_color_fogger(self):
        return self.color_fogger

    def get_color_name(self):
        return self.color_name


class DynamicColors:
    def __init__(self, movement_shape, color = None, duration_ms = None, duration_percentage = None, chase_percentage = None):
        #R G B W A UV
        self.movement = []
        self.shape = movement_shape #string
        self.reverse = False
        self.repititon = 0
        self.chase_percentage = chase_percentage
        
        if duration_ms == None and duration_percentage == None:
            self.duration = 400
            self.timing_unit = 'percentage'
        elif duration_percentage != None and duration_ms == None:
            self.duration = duration_percentage
            self.timing_unit = "percentage"
        elif duration_ms != None and duration_percentage == None:
            self.duration = duration_ms
            self.timing_unit = "ms"

        if color != None:
            for i in color.get_color():
                if self.chase_percentage == 0:
                    self.movement.append({'shape': movement_shape, 'min': 0, 'max': i, 'duration_' + self.timing_unit: self.duration})
                else:
                    self.movement.append({'shape': movement_shape, 'min': 0, 'max': i, 'duration_' + self.timing_unit: self.duration, 'delay_percentage': self.chase_percentage})
        else:
            for i in range(0,6):
                if self.chase_percentage == 0:
                    self.movement.append({'shape': movement_shape, 'duration_' + self.timing_unit: self.duration})
                else:
                    self.movement.append({'shape': movement_shape, 'duration_' + self.timing_unit: self.duration, 'delay_percentage': self.chase_percentage})
    
    def set_min_max(self, min, max, curve_min = None, curve_max = None):
        # min, max and curve_min, curve_max must be lists of size 6 to represent R, G, B, W, A, UV
        for i in range(0,6):
            self.movement[i]['min'] = min[i]
            self.movement[i]['max'] = max[i]
            if curve_min != None:
                self.movement[i]['curve_min'] = curve_min[i]
            if curve_max != None:
                self.movement[i]['curve_max'] = curve_max[i]

    def set_duration(self, duration):
        self.duration = duration
        for i in range(0,6):
            self.movement[i]['duration_' + self.timing_unit] = self.duration
    
    def set_reverse(self, reverse):
        if reverse == True:
            for i in range(0,6):
                self.movement[i]['reverse'] = True
            self.reverse = True
        elif reverse == False:
            for i in range(0,6):
                self.movement[i]['reverse'] = False
            self.reverse = False
    
    def set_repition(self, repitition):
        self.repititon = repitition
        for i in range(0,6):
                self.movement[i]['repitition'] = repitition
    
    def set_chase_percentage(self, delay_percentage):
        self.chase_percentage = delay_percentage
        for i in range(0,6):
            self.movement[i]['delay_percentage'] = delay_percentage
    
    def get_movement(self):
        return self.movement

    def get_timing_unit(self):
        return self.timing_unit

    def get_shape(self):
        return self.shape
    
    def get_repitition(self):
        return self.repititon
    
    def get_duration(self):
        return self.duration

    def is_reverse(self):
        return self.reverse
