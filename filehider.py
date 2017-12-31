#!/usr/bin/python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import time

from picture import *
from operations import *

#Fonction à redéfinir
verbosePrint = lambda *a : None

def measureTime(func):

	def wrap(*args, **kwargs):
		start_time = time.time()
		ret = func(*args, **kwargs)
		elapsed = time.time() - start_time

		print "Elapsed time : {} s".format(elapsed)

		return ret	

	return wrap

parser = ArgumentParser()

parser.add_argument("-dt", "--dissimulate-text", metavar="TEXT", action="store", help="To hide some raw text", type=str, default="\0", dest="dt")
parser.add_argument("-df", "--dissimulate-file", metavar="PATH", action="store", help="To hide an entire file", type=str, default="\0", dest="df")

parser.add_argument("-ft", "--find-text", metavar="KEY", action="store", help="To quickly output hidden text", type=int, default=0, dest="ft")
parser.add_argument("-ff", "--find-file", metavar="KEY", action="store", help="To retrieve an entire file", type=int, default=0, dest="ff")

parser.add_argument("-i", "--input", action="store", help="The input image", default="\0")
parser.add_argument("-o", "--output", action="store", help="The output file", default="\0")

parser.add_argument("-q", "--quiet", action="store_true", help="Quiet mode : only the results or errors will be output (doesn't work for now)", default=False)
parser.add_argument("-v", "--verbose", action="store_true", help="Verbosity increased (doesn't work for now)", default=False)

parser.add_argument("-b", "--buffer", metavar="LENGTH", action="store", help="The buffer length to use when using the image", type=int, default=-1)

args = parser.parse_args()

b_dt = True if args.dt!="\0" else False
b_df = True if args.df!="\0" else False
b_ft = True if args.ft!=0 else False
b_ff = True if args.ff!=0 else False

if ( (b_dt or b_df) and (b_ft or b_ff) ) or ( (b_dt or b_ft) and (b_df or b_ff) ) :
	raise ValueError("You can only do one operation at once")

if not True in (b_dt, b_df, b_ft, b_ff):
	raise ValueError("No operation specified")

if args.input == "\0" : raise ValueError("-i option is mandatory") 

if args.quiet:
	pass

if args.verbose:
	def verbosePrint(*args):
		for a in args:
			print a

buf = args.buffer if args.buffer>=0 else DEF_BUF_LEN


@measureTime
def op():

	if b_dt:
		assert args.output != "\0"
		
		hide( args.input, args.output, map(ord, list(args.dt)), buf )

	elif b_df:
		assert args.output != "\0"
		
		data = list()
		with open( args.df, 'rb' ) as f:
			data_ = list(f.read())
			data = map(ord, data_)

		hide( args.input, args.output, data, buf )

	elif b_ft:
		data = find( args.input, args.ft, buf )
		print ''.join(c for c in map( chr, data ))

	elif b_ff:
		assert args.output != "\0"

		data_ = find( args.input, args.ff, buf )

		with open( args.output, 'wb' ) as f:
			data = ''.join(c for c in map( chr, data_ ))
			f.write( data )

op()
