#! /bin/bash

# netfilter Manager
# Template : Start template

# These rules will be added at the beginning of each file pushed on the servers

# Resetting all iptables rules

iptables -F
iptables -Z
iptables -F INPUT
iptables -F OUTPUT
iptables -F FORWARD
iptables -t nat -F
iptables -t nat -Z
iptables -t mangle -Z
iptables -t mangle -F

# Start of host specific rules

