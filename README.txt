Copyright (c) 2012 Pragma Nolint.
See LICENSE.txt for details.
Note: Some code based on pygame "Type Game" by Pawel Krawczak (diavel) 
released under license "You're free do to whatever you want with this 
program.".


Fly: Training program for Plover, Open Source Stenography Software

For information about Plover, visit http://stenoknight.com/plover/


INSTALLATION

Installation is not required for Fly.


REQUIREMENTS

* Keyboard supported by plover 2.2.0: 
    . QWERTY keyboards with n-key rollover (e.g. Microsoft SideWinder X4)
    . Gemini PR (a.k.a. Gemini Enhanced)
    . TX Bolt (a.k.a. Gemini TX)
* Plover must NOT be active when running Fly.
* Python 2.6 or later
* pygame installed (preferably 1.9.1release or later) 
* xlib is required (if plover is installed, this will have also been 
        installed)


RUNNING FLY

Note: Plover should NOT be active when running Fly.
From a terminal, type: "python main.py". This will launch Fly. 

Alternatively, set main.py to be executable (right-click on
main.py -> properties -> permissions -> check "Allow executing 
file as program") and double click it.

Use the mouse to click on options on the right-hand panel, and
press keys to enter chords as prompted.


ACCESSIBILITY

Fly can be run with different colour schemes, see config.py option
COLOR_SCHEME. For people with low vision, the colour scheme
"highcontrast" will provide a high contrast view.


EXTENDING FLY

Custom lessons can be added to fly by adding files to data/lessons. 
See file HOW_TO_ADD_LESSONS in data/lessons for how to do this.


DEVELOPING FLY

Fly is hosted at https://launchpad.net/flyploverfly.

Fly has tests in directory "tests". All tests can be run by typing in
a terminal: "./run_all_tests.csh" providing you are in the main directory, 
and that the run_all_tests file has the appropriate permissions (chmod 
+x run_all_tests.csh to make executable).


SUPPORT

Please email the google discussion group ploversteno@googlegroups.com 
for support, or report a bug on launchpad. 


AUTHORS

Pragma Nolint
Michael Roberts

