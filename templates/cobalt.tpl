# Host template for cobalt box

# Declare template variables
arguments = internalsubnet, externalsubnet, host

TEMPLATE-START

iptables -A INPUT -s {internalsubnet} -d {externalsubnet} -j ACCEPT
iptables -A OUTPUT -s {externalsubnet} -d {internalsubnet} -j ACCEPT

iptables -A INPUT -s {internalsubnet} -d {host} -j ACCEPT
iptables -A OUTPUT -s {externalsubnet} -d {host} -j ACCEPT

iptables -A INPUT -s {internalsubnet} -d {externalsubnet} -j DROP
iptables -A OUTPUT -s {externalsubnet} -d {internalsubnet} -j DROP

iptables -A INPUT -s {internalsubnet} -d {externalsubnet} -j LOG
iptables -A OUTPUT -s {externalsubnet} -d {internalsubnet} -j SNAT

iptables -A INPUT -s {internalsubnet} -d {externalsubnet} -j REJECT
iptables -A OUTPUT -s {externalsubnet} -d {internalsubnet} -j DNAT
