#!/bin/bash
interface='eth3'
tcpdump ip -v -l -i $interface | python dump_analysis.py 
