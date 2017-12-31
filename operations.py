# -*- coding: utf-8 -*- 

from picture import *
from anim import *

import sys

DEF_BUF_LEN = 4096

def hide(input_img, output_img, data, buf_len = DEF_BUF_LEN):

	assert type(input_img) == Picture and type(output_img) == Picture or type(input_img) == str and type(output_img) == str
	assert type(data) == list and type(data[0]) == int
	assert type(buf_len) == int and buf_len%8 == 0

	def withPictures(input_img, output_img, data, buf_len):

		print eventMessages("find", input_img, buf_len, output_img)

		#Car il faut pour 1 bit de données 1 octet d'image : ça représente le nb d'octets d'image dont on a besoin
		length = len(data)*8

		a = AnimHide(20, length)

		output_img.copy(input_img)

		a.start()

		#Combien de fois il va falloir remplir notre buffer
		for i in range( length / buf_len + 1 ):

			if i == length / buf_len:
				buf = input_img.read(length % buf_len)

			else:
				buf = input_img.read(buf_len)

			buf = map(ord, buf)

			for j in range( len(buf) ):

				index = i*buf_len/8 + j/8

				#On calcule le bit à coder
				bit = ( data[index] & (1 << j%8) ) >> (j%8)

				#On change le LSB de l'image au bit de data
				buf[j] = (buf[j] & ~1)
				buf[j] |= bit

			output_img.write(buf)

			a.setNow((i+1)*buf_len)

		a.stop()
		a.join()

		print '\n'

		output_img.update()

		print "Done, key : {}".format(length)

	if type(input_img) == str:
		withPictures( Picture(input_img), Picture(output_img), data, buf_len )

	else:
		withPictures( input_img, output_img, data, buf_len )


def find(input_img, key, buf_len = DEF_BUF_LEN):

	assert type(input_img) == str or type(input_img) == Picture
	assert type(key) == int
	assert type(buf_len) == int

	@exceptErrors
	def withPictures(input_img, key, buf_len):

		print eventMessages("find", input_img, buf_len)

		a = AnimFind(5, 10)

		#key est la longueur de notre info, vu que chaque octet d'info est réparti dans 8 autres octets d'image, on a une info de longueur key/8
		data = [0] * (key/8)
		colors = list()

		a.start()

		for i in range(key):
			if i%buf_len == 0:
				colors = list( input_img.read(buf_len) )
				colors = map(ord, colors)

			#On récupère le LSB
			lsb = colors[i - (i/buf_len)*buf_len] & 1

			#On l'ajoute à notre liste
			data[i/8] = data[i/8] | (lsb << i - (i/8) * 8 )

		a.stop()
		a.join()

		input_img.cleanMemo()

		print "Done\n"

		return data

	if type(input_img) == str:
		return withPictures( Picture(input_img), key, buf_len )

	else:
		return withPictures( input_img, key, buf_len )

def eventMessages(op, input_img, buf_len, output_img=None):
	assert type(op) == str
	assert type(input_img) == Picture

	string = ""

	string += "\n********************************\n"
	string += ( "Starting to {0} content in {1}...\n".format(op, input_img.getName()) )

	if output_img != None:
		assert type(output_img) == Picture
		string += ( "Output image : {}\n".format(output_img.getName()) )

	string += ( "Buffer length : {}\n".format(buf_len) )

	return string
