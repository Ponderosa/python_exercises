"""
The colortoypiano uses multi-threading to interface with
a chosen midi interface. This interface is used to print all
incoming midi messages for that device.
"""

import colortoypianoshell
import mido
import queue
import sys
import threading


class ColorToyPiano(object):

    def __init__(self):
        """Create local queue and thread."""
        self.q = queue.Queue()
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
        self.t = threading.Thread(
            target=midi_monitor, args=(inport, self.q))
        self.t.start()


def midi_monitor(inport, q):
    """A function meant to run as a child thread that polls
    the midi input for the next available midi message. When
    a midi message is available it prints it to the stdout.

    Args:
        inport (mido inport): a reference to the current midi in.
    """
    while True:
        if not q.empty():
            if (q.get() == 'quit'):
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
    ctps = colortoypianoshell.ColorToyPianoShell(ctp)
    ctps.cmdloop()

if __name__ == '__main__':
    main()
