sudo ovs-vsctl add-port s1 tap2
sudo ovs-vsctl add-port s2 tap3
sudo ovs-vsctl set bridge s1 protocols=OpenFlow13
sudo ovs-vsctl set bridge s2 protocols=OpenFlow13

