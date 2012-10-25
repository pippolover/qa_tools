#! /bin/bash
#######################################
# this script will remove last time jmeter performance log then run testplan named online_perf.jmx
# under testplan dir
# performance report will be generate after test finished
##########################################
rm -rf ../log/rlt.jtl 
rm -rf ../log/perf.jtl
bash ../../apache-jmeter-2.6/bin/jmeter -n -t ../testplan/online_perf.jmx
python analyse_jmeter.py txt
