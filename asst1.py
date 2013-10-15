#!/usr/bin/env python

import sys
import csv
import re
from pprint import pprint

fnames = ('los.csv', 'nlos.csv')

# {'<name>': Test}
tests = {}


class Entry():
  ''' 
  entry_name(string):     'LOSX' or 'NLOSX' where X is run number
  rssi(float)
  cinr(float)
  uplink():
  '''
  def __init__(self, entry_as_list_item):
    e = entry_as_list_item
    if len(e[0]):
      self.name = e[0]
    if len(e[1]):
      self.rssi = float(e[1])
    if len(e[2]):
      self.cinr = float(e[2])
    if len(e[3]):
      self.gps = self.get_gps(line)
    if len(e[4]):
      self.time = e[4]
    if len(e[5]):
      self.uplink = float(e[5].split('/')[1])
    if len(e[6]):
      self.downlink = float(e[6].split('/')[0])

  def get_gps(self, line):
    if len(line[3]): # gps coords here
      gps = tuple(re.findall('[\d\.]+', line[3]))
      return (float(gps[0]), float(gps[1]))

  def __str__(self):
    return '%f,%f,%s,%f,%f,%f,%f' % (self.gps[0], self.gps[1], self.time, self.rssi,
    self.cinr, self.uplink, self.downlink)
    

def get_vals(fname):
  '''Helper to get CSV values. Returns list of comma-separated values'''
  with open(fname, 'r') as f:
    r = csv.reader(f)
    lines = []
    try:
      while True:
        lines.append(r.next())
    except Exception as e:
      print e
  return lines



#################################################
###############  SCRIPT START  ##################
#################################################

# Fill out <tests> dict of tests, grouped by test name
for f in fnames:
  lines = get_vals(f)
  output = lines[0] # header
  for line in lines[1:]:
    if len(line[0]): # skip empty lines
      name = line[0]
      if name not in tests:
        tests[name] = []
      tests[name].append(Entry(line))

# Print them
for testname, entries in tests.iteritems():
  for entry in entries:
    print entry


# From here, you have access to all the entries. It looks like:
# tests = {<testname>: [entry 1, entry 2, entry 3, entry 4, entry 5],
#          <testname2>: [entry 1, entry 2, entry 3, entry 4, entry 5],
#          ... }

