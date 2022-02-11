from __future__ import print_function
from ola.ClientWrapper import ClientWrapper
import array
import sys
import time
import logging

wrapper = None
client = None
last_frame_time = 0
universe = 1
dmx_data = array.array('B', [0] * 512)
FPS = 30

def DmxSent(status):
  if status.Succeeded():
    logging.debug('Success!')
  else:
    logging.error('Error: %s' % status.message, file=sys.stderr)

  # global wrapper
  # if wrapper:
  #   wrapper.Stop()


def main_loop():

  logging.debug('')
  logging.debug('------------------------')

  # Calculate and wait time delta until next frame can be started
  global last_frame_time
  now = time.time()
  sleep_time = 1./FPS - (now - last_frame_time)
  last_frame_time = now
  if sleep_time > 0:
    time.sleep(sleep_time)

  # Main loop content
  global wrapper
  global client
  global universe
  global dmx_data
  process_events() # process input and other stuff
  update_state() # update all objects that need to be updated, e.g. position changes, physics, all that other stuff
  render(client, universe, dmx_data) #render things on screen

  logging.debug('------------------------')
  logging.debug('')

  # Restart loop
  wrapper.AddEvent(0, main_loop)

def print_welcome():
  print('=======================')
  print()
  print('        PI LIGHT       ')
  print()
  print('=======================')

def process_events():
  logging.debug('input processing')
  logging.debug('event processing')

def update_state():
  logging.debug('update state')
  dmx_data[0] = 255
  dmx_data[2] = 255
  dmx_data[8] = 255
  dmx_data[14] = 255
  dmx_data[20] = 255
  dmx_data[26] = 255
  dmx_data[32] = 255
  dmx_data[38] = 255
  dmx_data[44] = 255
  dmx_data[50] = 255
  dmx_data[56] = 255
  dmx_data[62] = 255
  dmx_data[68] = 255



def render(client, universe, dmx_data):
  logging.debug('read state and send dmx')
  client.SendDmx(universe, dmx_data, DmxSent)

if __name__ == '__main__':
  print_welcome()

  wrapper = ClientWrapper()
  client = wrapper.Client()
  wrapper.AddEvent(0, main_loop)
  wrapper.Run()

