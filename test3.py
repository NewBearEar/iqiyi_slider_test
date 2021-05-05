import execjs
import re
import json
import random
import time
import requests
from img_locate import get_distance
from process_trace import get_risk_data
import iqiyi_crypt

with open('test3.js', encoding='utf-8') as f:
    aiqiyi = f.read()
js = execjs.compile(aiqiyi)
s = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
logid = js.call('getRandom', 64,s)