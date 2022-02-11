# pylight
Send DMX based on scenes controlled through MIDI

## Architecture

The whole application is build around the game loop. It consists of four steps:
1. setup loop speed based on FPS, by default 30
2. check for MIDI input or additional input/events
3. update the current state of the played scene
4. render the scene to DMX

## Dependencies

- Python 2 since OLA still runs on Python 2
- OLA as the deamon to put out DMX
- Something for MIDI input monitoring
- Something for storing DMX scenes

## Ideas
- Use yaml for dmx scene representation
- Base every calculation on some global timing value to change speed of scenes based on BPM
- Use MIDI programm changes for song/bank selection
- Use MIDI control changes for scene selection
- Use MIDI ... for bpm selection
