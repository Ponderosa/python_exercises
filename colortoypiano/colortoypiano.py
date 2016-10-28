"""
The colortoypiano uses multi-threading to interface with
a chosen midi interface. This interface is used to print all
incoming midi messages for that device.
"""

from cmd import Cmd
import mido
from queue import Queue, Empty
import sys
from threading import Thread


class ColorToyPiano(object):

    def __init__(self):
        """Create local queue and thread."""
        self.q = Queue()
        self.t = None

    def quit(self):
        """Quit child threads"""
        if self.t is not None:
            # Pass 'quit' command to child thread.
            self.q.put('quit')
            self.t.join()

    def open(self, channel):
        """Open a mido input device on another thread.

        Args:
            channel (int): midi input channel
        """
        inport = mido.open_input(mido.get_input_names()[int(channel)])
        self.t = Thread(
            target=midi_monitor, args=(inport, self.q))
        self.t.start()


class ColorToyPianoShell(Cmd):
    """
    The colortoypianoshell uses the python cmd shell and the
    colortyopiano to interface with the user and a chosen midi interface.
    This interface is used to print all incoming midi signals for that device.
    """
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
        show_in_ports()


def midi_monitor(inport, q):
    """A function meant to run as a child thread that polls
    the midi input for the next available midi message. When
    a midi message is available it prints it to the stdout.

    Args:
        inport (mido inport): a reference to the current midi in.
    """
    while True:
        try:
            msg = q.get_nowait()
        except Empty:
            pass
        else:
            if msg == 'quit':
                print(inport.name + ' quit')
                break
        # Polls (doesn't block) so if we get a quit command the response
        # will not need to wait for another midi message to be sent.
        msg = inport.poll()
        if msg is not None:
            print(msg)
            sys.stdout.flush()


def show_in_ports():
    """Print a list of all available midi input ports."""
    print(list(enumerate(mido.get_input_names())))


def main():
    """Main function for colortoypiano"""
    mido.set_backend('mido.backends.rtmidi')
    ctp = ColorToyPiano()
    ctps = ColorToyPianoShell(ctp)
    ctps.cmdloop()

if __name__ == '__main__':
    main()
