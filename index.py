from __future__ import print_function
from ola.ClientWrapper import ClientWrapper
from ola.DMXConstants import *
import array
import sys
import time
import logging

# Constants, startup options, and globals
wrapper = None
client = None
last_frame_date = 0
universe = 1
dmx_data = array.array('B', [DMX_MIN_SLOT_VALUE] * DMX_UNIVERSE_SIZE)
FPS = 30

def main():
  print_welcome()
  read_config()
  load_show()
  start_wrapper()

def print_welcome():
  print('=======================')
  print()
  print('        PI LIGHT       ')
  print()
  print('=======================')
  print()
  print()

def read_config():
  logging.debug('cli options')

def load_show():
  logging.debug('loading show')
  logging.debug('show loaded')

def start_wrapper():
  global wrapper
  global client
  wrapper = ClientWrapper()
  client = wrapper.Client()
  wrapper.AddEvent(0, main_loop)
  wrapper.Run()

def main_loop():

  logging.debug('')
  logging.debug('------------------------')

  # Calculate and wait time delta until next frame can be started
  global last_frame_date
  now = time.time()
  sleep_time = 1./FPS - (now - last_frame_date)
  last_frame_date = now
  if sleep_time > 0:
    time.sleep(sleep_time)

  # Main loop content
  global wrapper
  global client
  global universe
  global dmx_data
  process_events() # process input and other stuff
  update_state() # update all objects that need to be updated, e.g. scene changes, scene updates
  render(client, universe, dmx_data) # send things to DMX

  logging.debug('------------------------')
  logging.debug('')

  # Restart loop
  wrapper.AddEvent(0, main_loop)


# ----------------- Loop steps -----------------

def process_events():
  logging.debug('input processing')
  logging.debug('event processing')

def update_state():
  logging.debug('update state')
  dmx_data[0] = DMX_MAX_SLOT_VALUE
  dmx_data[2] = DMX_MAX_SLOT_VALUE
  dmx_data[8] = DMX_MAX_SLOT_VALUE
  dmx_data[14] = DMX_MAX_SLOT_VALUE
  dmx_data[20] = DMX_MAX_SLOT_VALUE
  dmx_data[26] = DMX_MAX_SLOT_VALUE
  dmx_data[32] = DMX_MAX_SLOT_VALUE
  dmx_data[38] = DMX_MAX_SLOT_VALUE
  dmx_data[44] = DMX_MAX_SLOT_VALUE
  dmx_data[50] = DMX_MAX_SLOT_VALUE
  dmx_data[56] = DMX_MAX_SLOT_VALUE
  dmx_data[62] = DMX_MAX_SLOT_VALUE
  dmx_data[68] = DMX_MAX_SLOT_VALUE

def render(client, universe, dmx_data):
  logging.debug('read state and send dmx')
  client.SendDmx(universe, dmx_data, __on_dmx_sent)

def __on_dmx_sent(status):
  if status.Succeeded():
    logging.debug('Success!')
  else:
    logging.error('Error: %s' % status.message, file=sys.stderr)

if __name__ == '__main__':
  main()
