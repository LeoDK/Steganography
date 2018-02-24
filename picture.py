# -*- coding: utf-8 -*-

import os
from shutil import copyfile

def exceptErrors(func):
    """
    Décorateur pour try/except
    """
    def decorate(*args):
        try:
            return func(*args)

        except Exception as e:
            return e

    return decorate

class Memo(object):
    """
    Là où on stocke les données temporaires.
    """

    data = dict()

    def __init__(self):
        data = {}

    def setData(self, caller, name, value):
        self.data[caller] = {name : value}

    def getData(self, caller, name):
        return self.data[caller][name]

    def rst(self, *caller):
        self.data[caller] = dict()

class Picture (object) :
    """
    Classe représentant une image
    """

    format_error = Exception("Incompatible format")
    corrupted_error = Exception("Corrupted file, please try with another one")

    DEFAULT_IMG = "default.bmp"

    _name = "default.bmp"
    _header = list()
    _header_len = 0

    memo = Memo()

    def __init__(self, name):
        assert type(name) == str
        if not self.getName().endswith(".bmp") : raise Picture.format_error

        self._name = name

        self.cleanMemo()
        
        self._header_len = self.calcImgBegin()
        self._header = self.calcHeader()

        if type(self._header_len) == IOError: 
            print "Image {} not found, using default".format(name)
            self.makeDefault()

        elif type(self._header_len) == TypeError:
            raise Picture.corrupted_error

        elif type(self._header_len) != int:
            raise self._header_len

        else:
            print "{} loaded".format(name)

    @exceptErrors
    def read(self, length, offset = -1):
        assert type(length) == int
        assert type(offset) == int

        def function(offset):
            to_return = list()

            f = open(self.getName(), 'rb')

            f.seek(self.getHeaderLen() + offset)

            f_bytes = f.read(length)
            to_return = list(f_bytes)

            f.close()

            return to_return

        if offset < 0:
            offset = self.memo.getData( self.read, 'offset' )
            result = function(offset)
            self.memo.setData( self.read, 'offset', offset+length )

            return result

        else:
            return function(offset)

    @exceptErrors
    def write(self, tab, offset = -1):
        assert type(tab) == list or type(tab) == tuple
        assert type(offset) == int

        def function(offset, tab):
            f = open(self.getName(), 'r+')

            f.seek(offset + self.getHeaderLen())

            if type(tab[0]) == str:
                for c in tab : f.write(c)
        
            else:
                for b in tab : f.write( chr(b) )

            f.close()

        if offset < 0:
            offset = self.memo.getData( self.write, 'offset' )
            function(offset, tab)
            self.memo.setData( self.write, 'offset', offset+len(tab) )

        else:
            function(offset, tab)

    @exceptErrors
    def calcImgBegin(self):
        """
        Récupérer l'adresse de l'octet à partir duquel l'image commence vraiment
        """
        offset = 0

        f = open(self.getName(), 'rb')
        f.seek(10)

        for i in range(4):
            offset |= ( ord( f.read(1) ) << i*8 )
        
        f.close()

        return offset

    @exceptErrors
    def calcHeader(self):
        """
        Obtenir le header d'une image
        """

        if self.getHeaderLen() > 1000 : raise Picture.corrupted_error

        header = list()
        f = open(self.getName(), 'rb')

        for i in range( self.getHeaderLen() ):
            header.append( f.read(1) )

        f.close()

        return header

    @exceptErrors
    def makeDefault(self):
        self.copy( Picture(Picture.DEFAULT_IMG) )
        self.update()

    @exceptErrors
    def delete(self):
        os.remove(self.getName())
        print "{} file deleted".format(self.getName())

    def makeEmpty(self):
        with open(self.getName(), 'w') as f:
            f.write("")
        print "{} content deleted".format(self.getName())

    @exceptErrors
    def copy(self, src_image):
        assert type(src_image) == Picture
        self.makeEmpty()
        copyfile(src_image.getName(), self.getName())
        self.update()
        print "{0} copied to {1}".format(src_image.getName(), self.getName())

    def update(self):
        self.__init__(self.getName())

    def cleanMemo(self):
        self.memo.rst(self.read)
        self.memo.rst(self.write)

        self.memo.setData(self.read, 'offset', 0)
        self.memo.setData(self.write, 'offset', 0)

    def getName(self):
        return self._name

    def getHeader(self):
        return self._header

    def getHeaderLen(self):
        return self._header_len
