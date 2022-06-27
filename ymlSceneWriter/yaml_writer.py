import yaml
from fixtures import Fixtures, ColorGroups
from colorLib import Colors, DynamicColors
import copy
import math


scene = {'00_version': '0.1'}
name = ''
strobe = None

led_bar_01 = Fixtures(dmx_adress =  1, dimmer_channel= 1, strobe_channel = 2, color_group_size = 6, number_of_color_groups = 12, color_groups_start_channel = 3)
led_bar_02 = Fixtures(dmx_adress = 75, dimmer_channel= 1, strobe_channel = 2, color_group_size = 6, number_of_color_groups = 12, color_groups_start_channel = 3)
fogger_01 = Fixtures(dmx_adress = 149, dimmer_channel= 2, strobe_channel = 4, color_group_size = 3, number_of_color_groups = 1, color_groups_start_channel = 5, fog_channel = 1)
fogger_02 = Fixtures(dmx_adress = 156, dimmer_channel= 2, strobe_channel = 4, color_group_size = 3, number_of_color_groups = 1, color_groups_start_channel = 5, fog_channel = 1)

#set overall faders
faders = {led_bar_01.get_dimmer_adress(): {'value': 255, 'type': 'default'},  led_bar_02.get_dimmer_adress(): {'value': 255, 'type': 'default'}, fogger_01.get_dimmer_adress(): {'value': 255, 'type': 'default'}, fogger_02.get_dimmer_adress(): {'value': 255, 'type': 'default'}}

for fogger in [fogger_01, fogger_02]:
    faders[fogger.get_fog_adress()] = {'value': 255, 'type': 'midi', 'params': {'note': 60}}

def main():

    '''static functions'''
    #strobe = 150
    #color1 = Colors('red')
    #color2 = Colors('nothing')
    #name = set_full_color(color1, strobe, left = True, right = True)       #left and right can be specified optionally
    #name = set_cross_colors(color1, color2, strobe)
    #name = set_top_color(color1, strobe, left = True, right = False)
    #name = set_bottom_color(color1, strobe, left = True, right = False)
    #name = set_rise_color(color1, strobe, rise_number = 2, left = True, right = False)
    #name = set_seconds_colors(color1, color2, strobe)
    #name = set_combo_colors(color1, color2, strobe, combo = 4, invert = False) #combo can be set to 2,3,4 / invert = True inverts the second LED bar
    #name = set_outer2_colors(color1, color2, strobe, invert = False)
    #name = set_outer3_colors(color1, color2, strobe, invert = False)
    #name = set_lights_off()

    '''dynamic functions'''
    color1 = Colors('amber')
    color2 = Colors('red')
    strobe = 0

    chase_percentage1 = 61
    chase_shift_left1 = 0
    chase_shift_right1 = 50

    chase_percentage2 = 4.15
    chase_shift_left2 = 25
    chase_shift_right2 = 75

    dynamics1 = DynamicColors('sine', color1, duration_percentage = 400, chase_percentage = chase_percentage1)
    dynamics2 = DynamicColors('sine', color2, duration_percentage = 200, chase_percentage = chase_percentage2)
    dynamics1.set_min_max(min = [0,0,0,0,0,0], max = [255,0,0,0,0,0], curve_min = [10,0,0,0,0,0], curve_max = [255,0,0,0,0,0])
    #dynamics2.set_min_max(min = [0,0,0,0,0,0], max = [0,41,0,0,255,0], curve_min = [0,-5,0,0,-31,0], curve_max = [0,41,0,0,255,0])
    #dynamics.set_duration(200)
    #dynamics.set_repition(1)
    #dynamics.set_reverse(True)
    #name = set_full_color_movement(color1, dynamics, strobe)
    name = set_full_color_chase(color1, dynamics1, strobe, chase_percentage1, chase_shift_left1, chase_shift_right1)
    #name = set_two_color_chase(color1, color2, dynamics1, dynamics2, strobe, chase_percentage1, chase_shift_left1, chase_shift_right1, chase_percentage2, chase_shift_left2, chase_shift_right2)
    #name = set_two_color_static_plus_chase(color1, color2, dynamics1, strobe, chase_percentage1, chase_shift_left1, chase_shift_right1)

    scene['faders'] = faders

    #write yml file
    with open(r'Scenes/' + name + r'.yml', 'w') as file:
        outputs = yaml.dump(scene, file)


'''
scene creator functions static
'''
def set_full_color(color, strobe = 0, right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    foggers = [fogger_01, fogger_02]
    name = 'Full_' + color.get_color_name() + side_name
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name

    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            set_color_group(color_group, color)
    for fogger in foggers:
        faders[fogger.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[fogger.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, fogger.number_of_color_groups):
            color_group = ColorGroups(fogger.color_group_size, fogger.get_color_groups_adress() + i*fogger.color_group_size)
            set_color_group(color_group, color, fogger_flag = True)
    return name

def set_cross_colors(color1, color2, strobe):
    led_bars = [led_bar_01, led_bar_02]
    name = 'Cross_' + color1.get_color_name() + '_and_' + color2.get_color_name()
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
        
            if (i%12 < 6 and led_bar == led_bar_01) or (i%12 >=6 and led_bar == led_bar_02):
                set_color_group(color_group, color1)
            else:
                set_color_group(color_group, color2)

    return name

def set_seconds_colors(color1, color2, strobe):
    led_bars = [led_bar_01, led_bar_02]
    name = 'Seconds_' + color1.get_color_name() + '_and_' + color2.get_color_name()
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
        
            if (i%2 == 1):
                set_color_group(color_group, color1)
            else:
                set_color_group(color_group, color2)

    return name

def set_top_color(color, strobe,  right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    foggers = [fogger_01, fogger_02]
    name = 'Top_' + color.get_color_name() + side_name
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
        
            if (i%12 < 6):
                set_color_group(color_group, color)
    if right == True and left == True:
        for fogger in foggers:
            faders[fogger.get_dimmer_adress()] = define_fader(255)
            if strobe > 0:
                faders[fogger.get_strobe_adress()] = define_fader(strobe)
            for i in range(0, fogger.number_of_color_groups):
                color_group = ColorGroups(fogger.color_group_size, fogger.get_color_groups_adress() + i*fogger.color_group_size)
                set_color_group(color_group, color, fogger_flag = True)

    return name

def set_bottom_color(color, strobe,  right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    foggers = [fogger_01, fogger_02]
    name = 'Bottom_' + color.get_color_name() + side_name
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
        
            if (i%12 >= 6):
                set_color_group(color_group, color)

    if right == True and left == True:
        for fogger in foggers:
            faders[fogger.get_dimmer_adress()] = define_fader(255)
            if strobe > 0:
                faders[fogger.get_strobe_adress()] = define_fader(strobe)
            for i in range(0, fogger.number_of_color_groups):
                color_group = ColorGroups(fogger.color_group_size, fogger.get_color_groups_adress() + i*fogger.color_group_size)
                set_color_group(color_group, color, fogger_flag = True)

    return name

def set_rise_color(color, strobe,  rise_number, right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    name = 'Rise' + str(rise_number) + '_' + color.get_color_name() + side_name
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
        
            if (i%12 >= (12-rise_number)):
                set_color_group(color_group, color)

    return name

def set_combo_colors(color1, color2, strobe, combo, invert):   #combo (int) is the number of neighbor LEDs with the same color, can be set to 2,3,4
    led_bars = [led_bar_01, led_bar_02]
    name = 'Combo' + str(combo) + '_' + color1.get_color_name() + '_and_' + color2.get_color_name()
    if invert == True:
        name = name + '_invert'
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)

            if invert == True:
                if (i%(combo*2) < combo and led_bar == led_bar_01) or (i%(combo*2) >= combo and led_bar == led_bar_02):
                    set_color_group(color_group, color1)
                else:
                    set_color_group(color_group, color2)
            elif invert == False:
                if (i%(combo*2) < combo):
                    set_color_group(color_group, color1)
                else:
                    set_color_group(color_group, color2)

    return name

def set_outer2_colors(color1, color2, strobe, invert):   #combo (int) is the number of neighbor LEDs with the same color, can be set to 2,3,4
    led_bars = [led_bar_01, led_bar_02]
    name = 'Outer2_' + color1.get_color_name() + '_and_' + color2.get_color_name()
    if invert == True:
        name = name + '_invert'
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            
            if invert == True:
                if (i%10 < 2 and led_bar == led_bar_01) or (i%10 >= 2 and led_bar == led_bar_02):
                    set_color_group(color_group, color1)
                else:
                    set_color_group(color_group, color2)
            elif invert == False:
                if (i%10 < 2):
                    set_color_group(color_group, color1)
                else:
                    set_color_group(color_group, color2)

    return name

def set_outer3_colors(color1, color2, strobe, invert):   #combo (int) is the number of neighbor LEDs with the same color, can be set to 2,3,4
    led_bars = [led_bar_01, led_bar_02]
    name = 'Outer3_' + color1.get_color_name() + '_and_' + color2.get_color_name()
    if invert == True:
        name = name + '_invert'
    if strobe > 0:
        name = name + '_strobe'
    scene['01_name'] = name
    
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            
            if invert == True:
                if (i%9 < 3 and led_bar == led_bar_01) or (i%9 >= 3 and led_bar == led_bar_02):
                    set_color_group(color_group, color1)
                else:
                    set_color_group(color_group, color2)
            elif invert == False:
                if (i%9 < 3):
                    set_color_group(color_group, color1)
                else:
                    set_color_group(color_group, color2)

    return name

def set_lights_off():
    led_bars = [led_bar_01, led_bar_02]
    foggers = [fogger_01, fogger_02]
    name = 'lights_off'
    scene['01_name'] = name

    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(0)
    for fogger in foggers:
        faders[fogger.get_dimmer_adress()] = define_fader(0)
        faders[fogger.get_fog_adress()] = define_fader(0)

    return name


'''
tbd: scene creator functions dynamic
tbd: include foggers as LEDs
'''


'''
dynamic functions
'''

def set_full_color_movement(color, movement, strobe = 0, right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    name = 'Full_' + color.get_color_name() + '_' + movement.get_shape() + side_name
    if strobe > 0:
        name = name + '_strobe'
    if movement.is_reverse() == True:
        name = name + '_rev'
    if movement.get_repitition() > 0:
        name = name + '_rep'+ str(movement.get_repitition())
    name = name + '_dur' + str(movement.get_duration()) + str(movement.get_timing_unit())
    scene['01_name'] = name

    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            set_color_group(color_group, color, movement)

    return name


def set_full_color_chase(color, movement, strobe = 0, chase_percentage = 0, chase_shift_left = 0, chase_shift_right = 0, right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    name = 'Full_' + color.get_color_name() + '_' + movement.get_shape() + side_name
    if chase_percentage > 0:
        name = name + '_chase_pct' + str(chase_percentage)
    if strobe > 0:
        name = name + '_strobe'
    if movement.is_reverse() == True:
        name = name + '_rev'
    if movement.get_repitition() > 0:
        name = name + '_rep'+ str(movement.get_repitition())
    name = name + '_dur' + str(movement.get_duration()) + str(movement.get_timing_unit())
    scene['01_name'] = name
    chase_shift = chase_shift_left

    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            movement.set_chase_percentage(int(round(chase_shift + i*chase_percentage)))
        
            set_color_group(color_group, color, movement)

        chase_shift = chase_shift_right
    return name


def set_two_color_chase(color1, color2, movement1, movement2, strobe = 0, chase_percentage1 = 0, chase_shift_left1 = 0, chase_shift_right1 = 0, chase_percentage2 = 0, chase_shift_left2 = 0, chase_shift_right2 = 0, right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    name = 'TwoColor_' + color1.get_color_name() + '_' + movement1.get_shape() + ' ' + color2.get_color_name() + '_' + movement2.get_shape()+ ' ' + side_name
    #if chase_percentage > 0:
    #    name = name + '_chase_pct' + str(chase_percentage)
    if strobe > 0:
        name = name + '_strobe'
    #if movement.is_reverse() == True:
    #    name = name + '_rev'
    #if movement.get_repitition() > 0:
    #    name = name + '_rep'+ str(movement.get_repitition())
    name = name + '_dur' + str(movement1.get_duration()) + str(movement1.get_timing_unit())
    scene['01_name'] = name
    chase_shift = chase_shift_left1

    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            movement1.set_chase_percentage(int(round(chase_shift + i*chase_percentage1)))
        
            set_color_group(color_group, color1, movement1)

        chase_shift = chase_shift_right1

    chase_shift = chase_shift_left2

    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            movement2.set_chase_percentage(int(round(chase_shift + i*chase_percentage2)))
        
            set_color_group(color_group, color2, movement2)

        chase_shift = chase_shift_right2
    
    return name


def set_two_color_static_plus_chase(color1, color2, movement1, strobe = 0, chase_percentage1 = 0, chase_shift_left1 = 0, chase_shift_right1 = 0, right = True, left = True):
    led_bars, side_name = choose_led_bars(right, left)
    name = 'Full_' + color2.get_color_name() + '_and_' + color1.get_color_name() + '_' + movement1.get_shape() + '_chase'
    if strobe > 0:
        name = name + '_strobe'
    if movement1.is_reverse() == True:
        name = name + '_rev'
    if movement1.get_repitition() > 0:
        name = name + '_rep'+ str(movement1.get_repitition())
    name = name + '_dur' + str(movement1.get_duration()) + str(movement1.get_timing_unit())
    scene['01_name'] = name

    #static subscene
    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            set_color_group(color_group, color2)
    
    #dynamic subscene
    chase_shift = chase_shift_left1

    for led_bar in led_bars:
        faders[led_bar.get_dimmer_adress()] = define_fader(255)
        if strobe > 0:
            faders[led_bar.get_strobe_adress()] = define_fader(strobe)
        for i in range(0, led_bar.number_of_color_groups):
            color_group = ColorGroups(led_bar.color_group_size, led_bar.get_color_groups_adress() + i*led_bar.color_group_size)
            movement1.set_chase_percentage(int(round(chase_shift + i*chase_percentage1)))
        
            set_color_group(color_group, color1, movement1)

        chase_shift = chase_shift_right1

    return name




'''
helper functions
'''
def set_color_group(color_group, color, movement = None, fogger_flag = False):
    if fogger_flag == True:
        for i in range(0,color_group.color_group_size):
            if movement == None and not color.get_color_fogger()[i] == 0:
                faders[color_group.color_group_adress+i] = define_fader(color.get_color_fogger()[i])
    else:
        for i in range(0,color_group.color_group_size):
            if movement != None and not color.get_color()[i] == 0:
                faders[color_group.color_group_adress+i] = define_fader(color.get_color()[i], movement.get_movement()[i])
            if movement == None and not color.get_color()[i] == 0:
                faders[color_group.color_group_adress+i] = define_fader(color.get_color()[i])
    return

def choose_led_bars(right, left):
    if right == True and left == True:
        led_bars = [led_bar_01, led_bar_02]
        side_name = ''
    elif right == True:
        led_bars = [led_bar_01]
        side_name = '_right'
        faders[led_bar_02.get_dimmer_adress()] = define_fader(0)
    elif left == True:
        led_bars = [led_bar_02]
        side_name = '_left'
        faders[led_bar_01.get_dimmer_adress()] = define_fader(0)
    return led_bars, side_name
    
def define_fader(value, movement = None, type = 'default'):
    if movement == None:
        fader = {'value': value, 'type': type}
    else:
        fader = {'value': value, 'type': type, 'movement': copy.deepcopy(movement)}

    return fader

#main
if __name__ == '__main__':
    main()