#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pyttsx3
import sys

def init(lang):
    engine = pyttsx3.init()
    engine.setProperty("voice", lang)
    return engine

def say(message):
    engine.say(message)
    engine.runAndWait()

engine = init(str(sys.argv[2]))
say(str(sys.argv[1]))
