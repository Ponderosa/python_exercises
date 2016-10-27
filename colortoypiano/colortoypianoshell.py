"""
The colortoypianoshell uses the python cmd shell and the
colortyopiano to interface with the user and a chosen midi interface.
This interface is used to print all incoming midi signals for that device.
"""

import cmd


class ColorToyPianoShell(cmd.Cmd):
    intro = 'This is the color toy piano. Type help or ? to list commands.\n'
    prompt = '(color toy piano) '

    # ------- init method -------
    def __init__(self, pi):
        super().__init__()
        self.piano_instance = pi

    # ------- basic colortoypiano commands -------
    def do_quit(self, arg):
        'Gracefully shutdown the color toy piano.'
        self.piano_instance.quit()
        return True

    # ------- open new midi port -------
    def do_open(self, arg):
        'Open a midi in port.'
        self.piano_instance.open(arg)

    # ------- show all in ports -------
    def do_show(self, arg):
        'Prints available in ports.'
        self.piano_instance.show_in_ports()
