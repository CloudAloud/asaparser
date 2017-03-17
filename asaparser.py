import sys
import re
from ciscoconfparse import CiscoConfParse
from classes import *
from functions import *

filename = sys.argv[1]
parse = CiscoConfParse(filename)

acllist, result = [], []
ObjectGroupNetworkList, ObjectNetworkList, ObjectGroupServiceList = {}, {}, {}
lists = [ObjectGroupNetworkList, ObjectNetworkList, ObjectGroupServiceList]

protocols = ['ah', 'eigrp', 'esp', 'gre', 'icmp', 'icmp6', 'igmp', 'igrp', 'ip', 'ipinip', 'ipsec', 'nos', 'ospf', \
             'pcp', 'pim', 'pptp', 'snp', 'tcp', 'udp', '51', '88', '50', '47', '1', '58', '2', '9', '0', '4', '50', \
             '94', '89', '108', '103', '47', '109', '6', '17']

# Create a list of ACLs
file = open(filename, 'r')
for line in file:
    if re.search('access-list ', line):
        aclname = line.split(" ")[1]
        if acllist.count(aclname) == 0:
            acllist.append(aclname)
file.close()

# Parse for network objects
object_network = parse.find_objects("object network")
for line in object_network:
    object = ObjectNetwork(line.text.split(" ")[2])
    ObjectNetworkList[object.name] = object
    for child in line.re_search_children('host|subnet'):
        if len(child.text.split(" ")[2:]) == 1:
            # print(child.text.split(" ")[2:])
            object.children.append(child.text.split(" ")[2:][0])
        else:
            object.children.append(child.text.split(" ")[2] + "/" + str(convertSubnetMask(child.text.split(" ")[3])))

# Parse for network group objects
object_group_network = parse.find_objects("object-group network")
for line in object_group_network:
    object = ObjectGroupNetwork(line.text.split(" ")[2])
    ObjectGroupNetworkList[object.name] = object
    for child in line.re_search_children('network-object'):
        object.children.append(child.text.split(" ")[3:][0])

# Parse for service objects
object_group_service = parse.find_objects("object-group service")
for line in object_group_service:
    object = ObjectGroupService(line.text.split(" ")[2])
    ObjectGroupServiceList[object.name] = object
    for child in line.re_search_children('port-object eq'):
        object.children.append(child.text.split(" ")[3:][0])

# TODO parse for TCPUDP protocol group

# Parse file for ACL entries
for acl in acllist:
    remark = ''
    pattern = 'access-list ' + acl

    file = open(filename, 'r')
    for line in file:
        if re.search(pattern, line):
            newline = line[:-1].split(" ")
            if newline[2] == 'remark':
                remark = ''
                for word in newline[3:]:
                    remark += word + " "
            else:
                entry = Line()
                entry.remark = remark[:-1]
                entry.acl = newline[1]
                while newline:
                    element = newline.pop(0)
                    if element in ('access-list', acl, 'extended', 'log', 'disable', 'debugging', 'inactive', ''):
                        pass
                    elif element in ('permit', 'deny'):
                        entry.action = element
                    elif element in protocols:
                        entry.protocol = element
                    elif element == 'any':
                        if entry.source is None:
                            entry.source = 'any'
                        elif entry.destination is None:
                            entry.destination = 'any'
                        else:
                            entry.service = 'any'
                    elif element in ('object', 'object-group'):
                        if entry.source is None:
                            # TODO convert source here
                            #entry.source = newline.pop(0)
                            entry.source = findObject(newline.pop(0), lists)
                        elif entry.destination is None:
                            #entry.destination = newline.pop(0)
                            entry.destination = findObject(newline.pop(0), lists)
                        else:
                            #entry.service = newline.pop(0)
                            entry.service = findObject(newline.pop(0), lists)
                    elif element == 'eq':
                        #entry.service = newline.pop(0)
                        entry.service = findObject(newline.pop(0), lists)
                    else:
                        print('ERROR: ' + element)
                        print(line)

                result.append([entry.acl, entry.action, entry.protocol, entry.source, entry.destination, entry.service,
                               entry.remark])
    file.close()

# Call function to create XLSX file
friteXLSX('output.xlsx', result)

print('Written to output.xlsx')
