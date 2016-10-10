import sys
import colortoypianoshell
import mido
from multiprocessing import Process, Queue
import time


class ColorToyPiano(object):

    def __init__(self):
        self.q = Queue()
        self.p = None

    def quit(self):
        """Used to quit this program as well as the cmdloop and the
        child processes.
        """
        if self.p is not None:
            self.q.put('quit')
            while self.p.is_alive():
                pass

    def open(self, channel):
        inport = mido.open_input(mido.get_input_names()[int(channel)])
        self.p = Process(target=self.midi_monitor_start, args=(inport,))
        self.p.start()

    def show_in_ports(self):
        print(list(enumerate(mido.get_input_names())))

    def midi_monitor_start(self, inport):
        while True:
            if not self.q.empty():
                if (self.q.get() == 'quit'):
                    print('process quit')
                    sys.exit()
            print(inport)
            sys.stdout.flush()
            time.sleep(2)
            msg = inport.poll()
            print(msg)
            sys.stdout.flush()
            if msg is not None:
                print(msg)
                sys.stdout.flush()


if __name__ == '__main__':
    """Main function for colortoypiano"""
    mido.set_backend('mido.backends.rtmidi')
    ctp = ColorToyPiano()
    ctps = colortoypianoshell.ColorToyPianoShell(ctp)
    ctps.cmdloop()
