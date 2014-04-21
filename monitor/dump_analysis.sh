#!/bin/bash
tcpdump ip -v -l | python dump_analysis.py 
