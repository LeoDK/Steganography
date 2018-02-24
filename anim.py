# -*- coding:utf-8 -*-

from time import sleep
from threading import Thread
import sys

"""
Juste pour apporter un peu d'esthétisme à notre programme.
"""

class AnimHide (Thread):

    def __init__(self, total_length, final):
        super(AnimHide, self).__init__()

        #Le curseur
        self.cursor_length = 0
        self.total_length = total_length

        #La partie données
        self.now = 0
        self.final = final

        self.terminated = False

    def stop(self):
        self.terminated = True

    def calc(self, now, final):
        part = now/float(final)
        ret = int( part*self.total_length )

        return ret

    def getPercent(self):
        return int( self.now/float(self.final) *100 )

    def run(self):
        while not self.terminated:
            sys.stdout.write( '\b'*(self.total_length+6) )
            self.cursor_length = self.calc(self.now, self.final)

            string = ( "[" + "#"*(self.cursor_length) + " "*(self.total_length - self.cursor_length) + "] " + str(self.getPercent()) + "%")
            sys.stdout.write(string)

            sys.stdout.flush()

            sleep(0.1)

            sys.stdout.write( '\b'*(self.total_length+6) )
            string = ("[" + "#"*self.total_length + "] ")
            sys.stdout.write(string)
            sys.stdout.write("100%")

            sys.stdout.flush()

    def setNow(self, now):
            self.now = now

    def setFinal(self, final):
            self.final = final

class AnimFind (Thread):

    def __init__(self, cursor, length):
        super(AnimFind, self).__init__()
        self.cursor = cursor
        self.length = length
        self.terminated = False

    def calc(self, pos):
        leftover = 0

        if pos+self.cursor >= self.length :
                leftover = (pos + self.cursor - self.length)

        string = ("[" + "#"*leftover + " "*(pos - leftover) + "#"*(self.cursor - leftover) + " "*(self.length - leftover - self.cursor - pos) + "]")

        return string

    def run(self):
        while not self.terminated:
            for i in range(self.length):
                # +2 psk il faut compter les []
                sys.stdout.write( '\b'*(self.length+2) )
                sys.stdout.write( self.calc(i) )
                sys.stdout.flush()

                sleep(0.05)
        print '\n'

    def stop(self):
        self.terminated = True 
