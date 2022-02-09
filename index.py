from __future__ import print_function
from ola.ClientWrapper import ClientWrapper
import array
import sys
import time

wrapper = None


def DmxSent(status):
  if status.Succeeded():
    print('Success!')
  else:
    print('Error: %s' % status.message, file=sys.stderr)

  global wrapper
  if wrapper:
    wrapper.Stop()


def main():
  print_welcome()

  running = True
  FPS = 30
  last_frame_time = 0

  while running:
    current_time = time.time()
    sleep_time = 1./FPS - (current_time - last_frame_time)
    last_frame_time = current_time
    if sleep_time > 0:
      time.sleep(sleep_time)

    process_events() # process input and other stuff
    update_state() # update all objects that need to be updated, e.g. position changes, physics, all that other stuff
    render() #render things on screen

    print('------------------------')
    print('')

def print_welcome():
  print('=======================')
  print()
  print('        PI LIGHT       ')
  print()
  print('=======================')

def process_events():
  print('input processing')
  print('event processing')

def update_state():
  print('update state')

def render():
  print('read state and send dmx')

  universe = 1
  data = array.array('B')
  # append first dmx-value
  data.append(255)
  # append second dmx-value
  data.append(0)
  # append third dmx-value
  data.append(255)

  global wrapper
  wrapper = ClientWrapper()
  client = wrapper.Client()
  # send 1 dmx frame with values for channels 1-3
  client.SendDmx(universe, data, DmxSent)
  wrapper.Run()


if __name__ == '__main__':
  main()
