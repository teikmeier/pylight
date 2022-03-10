class Fixtures:
    def __init__(self, dmx_adress, dimmer_channel, strobe_channel, color_group_size, number_of_color_groups, color_groups_start_channel, fog_channel = None):
        self.dmx_adress = dmx_adress
        self.dimmer_channel = dimmer_channel
        self.strobe_channel = strobe_channel
        self.color_group_size = color_group_size
        self.number_of_color_groups = number_of_color_groups
        self.color_groups_start_channel = color_groups_start_channel
        self.fog_channel = fog_channel
    
    def get_dimmer_adress(self):
        dimmer_adress = self.dmx_adress + self.dimmer_channel -2
        return dimmer_adress

    def get_strobe_adress(self):
        strobe_adress = self.dmx_adress + self.strobe_channel -2
        return strobe_adress

    def get_fog_adress(self):
        fog_adress = self.dmx_adress + self.fog_channel -2
        return fog_adress

    def get_color_groups_adress(self):
        color_groups_adress = self.dmx_adress + self.color_groups_start_channel -2
        return color_groups_adress



class ColorGroups:
    def __init__(self, color_group_size, color_group_adress):
        self.color_group_size = color_group_size
        self.color_group_adress = color_group_adress
        self.values = [0] * self.color_group_size