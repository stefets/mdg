## [0.2.1] - 2026-09-20

### 🚜 Refactor

- Remove VLC in favor of MPV  #139
- Remove unused scenes
- Update MPV configuration and control mappings for audio and video devices

### 📚 Documentation

- Update full script example
## [0.2.0] - 2026-09-19

### 🚀 Features

- *(rich)* Add  base code prototype #140
- Connect MPV adapters with rich terminal
- Inject the terminal in the PlaylistManager
- Print the Playlist song from the Terminal

### 🚜 Refactor

- Remove Terminal class
- *(launch)* Kill mpv on start and add comments
- Update controller names for MPV
- Update terminal on every __call__
- Remove the print of the songs from the PlaylistManager
- Playlist changes
- Adjust scenes for playlist generation at level 1

### ⚙️ Miscellaneous Tasks

- Update CHANGELOG for version 0.1.0 with new features, bug fixes, and refactoring details
## [0.1.0] - 2026-09-13

### 🚀 Features

- Add Akai MPK261
- Add supported audio extensions #136
- Open the config file in the helper.py #136
- Add callback from MpvClient #136

### 🐛 Bug Fixes

- Correct log file names in run.sh for mpv instances

### 🚜 Refactor

- Add mpv_controller_3 to transport filter
- Remove playlist loading in scene navigation
- Initialize MPV client and set volume in constructor
- Enhance command handling and response reading in MpvClient
- Remove Transpose in control_patch
- Update Transpose for MKP261 trigger (WIP)
- *(gt1k)* Change target port
- *(pk5)* Add Port
- Update control_patch to use mpv_controller_2 for MPK249 and MPK261
- Update channel mapping for MPK249 and MPK261 controllers
- Unpause MPV before loading the next file to ensure immediate playback
- Enhance socket communication handling in MpvClient

### 📚 Documentation

- Update README for mpv #136

### ⚙️ Miscellaneous Tasks

- Ensure newline at end of file in run.sh
- Remove mp3 config #136
- Add socket path in configuration #136
- Rename mpv start script
- Remove requirements.txt file
## [0.0.3] - 2026-09-05

### 🚀 Features

- Generic test file with VirMIDI
- Add a first minimal MpvClient as a plugin #136
- Add an adapter #136
- Add PlaylistManager and Playlist #136

### 🐛 Bug Fixes

- Init volume at startup

### 🚜 Refactor

- Add Party Mix V3 and restaure Party Mix V2 config
- Remove mpg123 files and import #136
- Add missing import + add def seek
- Enable playlist listing
- Remove the call to clear_screen()
- *(mpv)* Set  --keep-open to no
- Update Numark MIDI port names for PMV3 and PMV2

### ⚙️ Miscellaneous Tasks

- Remove test #136
- Update controller name #136
- Remove mpg123 term #136
- Add run script #136
- Mock Playlist #136
- Rename numark ports
- Add switches to mpv start command (logging, terminal)
## [0.0.2] - 2026-08-04

### 🚀 Features

- Add MIDI support for Numark Party Mix MKII and Mixxx
- Add new scenes for Fields Of Fire
- *(sd90)* Add audio level controls for DigiLevel, MasterLevel, and RecLevel
- Add new scenes for "PeaceInOurTime" with bass and guitar patches
- Add new scenes and MIDI patch for "Peace in Our Time"
- Update scene names and improve clarity in scene groups
- Update hook functionality and move scenes in the include directory
- Add UM-2 MIDI ports and update Cakewalk output port
- Add Edirol UM-2ex in control patch

### 🚜 Refactor

- Rename GT1000Patch to GT1KPreset and update references
- *(mp3)* Rename wrapper to mp3_player for clarity and update references
- Add more modularity
- *(soundcraft)* Switch  treble/bass knobs routing configuration
- Finally, make the main template entirely modular
- Remove argh dependency
- Rename rendering functions and update template handling
- Ignore channel 15 in pre patch

### 📚 Documentation

- Add initial CHANGELOG.md
- Update CHANGELOG
- Update CHANGELOG and README
- Update CHANGELOG with new scenes and MIDI patch for "Peace in Our Time"
- Update rendered script example
- Update changelog

### 🧪 Testing

- Add Party Mix MKII
- Add routing test

### ⚙️ Miscellaneous Tasks

- Remove duplicate files
- Update full script example
- Reorder channel check
- Remove HttpClient and related test files
- Update scene
- Update scene name
- Add mandoline patch and scene
- Add file in hook
- Add new imports
- Remove dead wood
## [0.0.1] - 2025-11-10

### 🚀 Features

- Add Luminite Graviton MIDI controller
- *(daw)* Wip Rewin/Forward patch
- Add patch to send OSC rectoggle message to Soundcraft UI + Add to a scene group
- Use fcb1010 in control patch for DAW
- Add a callable object for easy bank select for POD HD
- Add GT-1000 MIDI ports to configuration
- Use Boss GT1000 (WIP)
- GT1000 integration (WIP)
- Add GT-1000 patch change by name
- *(control)* Add MASTER volume soundcraft control mapping for Nektar Expression Pedal
- *(soundcraft)* Add MIX auxiliary outputs and control mappings for Soundcraft UI
- *(sd90)* Add variations for Contemporary instrument part in SD-90 patch
- *(scene)* Add new scene 'Restless Natives' and update 'Wonderland' initialization
- *(scene)* Add 'Restless Natives' scene with initialization and patch configuration
- *(sd90)* Add Goblin
- Finish implement  SD90 AFX selectors

### 🐛 Bug Fixes

- Incorrect load_list usage
- *(config)* Incorrect port name
- *(gt1000)* Update target port comment for clarity and correct scene initialization
- *(control)* Update mpk_port_a mapping to use CakewalkController

### 💼 Other

- Set the port for Sysex
- Get NEWS from github, SVN is LOCKED
- Allow switch to scene 1
- Intelligent control patch
- Missing import
- Patch improvement
- *(test)* Add the simplest in/out test possible

### 🚜 Refactor

- *(vlc)* Use composition instead of inherit
- Add mp3 controller patch /  enable audio card
- *(mp3)* Use MPgy123 as property instead of inherit it
- Scene change
- *(mp3)* Add events (wip)
- Stop inherit mpyg123
- *(mp3)* Add managed events
- Use the events callback (WIP)
- Add toggle mute
- *(event)* Use event handler instead of callback
- Add scene
- Use toggle
- Adjust SD90 Sysex SET
- *(cakewalk)* Update routing; add to a scene
- Add control patch for Cakewalk DAW
- Force Channel 1 for DAW
- Abstract GT10B patch
- Abstract HD500 patches
- Patch name
- Remove GT10B patches from runtime patches.
- Decommission the Graviton midi controller
- Drop HD500 usage
- *(gt1000)* Adjusted bank selection patch interval.
- *(soundcraft)* Simplify soundcraft control and enhance key filtering
- *(filters)* Rename filter variables for consistency and clarity
- *(control)* Remove unused FCB1010 control mapping from MPK249 configuration
- Remove Q49 MIDI references from configuration
- *(scene)* Update 'Subdivisions' and 'The Trees' scenes with new initialization patches
- *(control)* Rename control variables for clarity and update references in control patch
- *(scene)* Update 'Grand Designs' scene initialization patch
- Add SD90 control patch for WAVE and INST + better naming for control patches
- *(sd90)* Simplify audio level control definitions and update SD90 controller configuration

### 📚 Documentation

- Update requirements file
- Update ReadMe
- Update example script
- Update readme
- Update readme
- Update readme

### 🧪 Testing

- Add virtual MIDI port

### ⚙️ Miscellaneous Tasks

- Remove useless comments
- Add patch
- Config change
- Patch change
- Scenes update
- Scene update
- Patch change
- Suspend virtual ports
- Patch update
- Control patch update
- *(daw)* Patch update
- Add scenes
- Move helpers outside src to labs
- Simplify file structure by the /include logic
- Patch/Scene update
- Add GT1000 in .asoundrc
- Remove annoying patch
- Update scene
- *(rush)* Patch update
- Update example script
