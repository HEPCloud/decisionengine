#!/bin/bash

msglogger -d server -a app1 hello
msglogger -d server -a app2 hello
msglogger -d server -a app3 hello
msglogger -d server -a app4 hello
msglogger -d server -a app5 hello
msglogger -d server -a app6 hello
msglogger -d server -a app7 -s error error
msglogger -d server -a app8 hello
msglogger -d server -a app9 hello
msglogger -d server -a app10 hello
msglogger -d server -a app11 -s error error 
msglogger -d server -a app12 hello

