from hashlib import md5 
from struct import unpack_from
from bisect import bisect
import sys
import matplotlib.pyplot as plt

def plot(a,b, title, label_y, label_x): #plot for results
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    plt.plot(b,a, linestyle='-')
    plt.legend()

    plt.show()

def hash(value): #given function
    k = md5(str(value).encode('utf-8')).digest()    
    r = unpack_from(">I", k)[0]
    return r

def generate_nodes(machine_dict, n): #generate nodes for each machine
    nodes = []
    for i in range(n):
        for m in machine_dict:
            nodes.append("{0}-{1}".format(i, m))
    return nodes

def get_server_by_value(val, servers): #input value and server dict, returns int of server id.
    h = hash(val)
    s = sys.maxsize
    a = False
    for x in servers:
        if(x > h):
            if(x < s):
                s = x
                a = True
    if(not a): #if no node found then take the smallest.
        for x in servers:
            if(x < s):
                s = x
    return servers[s]

def is_balanced(load, avg): #check if balanced load or not
    p = 0.15 * load
    if( avg + p < load ):
        return False
    if( avg - p > load):
        return False
    return True

k = range(1,200,1)
ratios = []
for i in k:
    MACHINES, KEYS = 10, 100000
    server_list = range(0,MACHINES)
    keys = range(0,KEYS)
    nodes = generate_nodes(server_list, i)
    nodes_map = {hash(node): node.split("-")[1] for node in nodes}
    keys_by_node = [ [],[],[],[],[],[],[],[],[],[] ]
    avg_load = KEYS / MACHINES

    for x in keys: #divide keys to nodes
        idx = get_server_by_value(x, nodes_map)
        keys_by_node[int(idx)].append(x)
    not_balanced = 0
    for y in keys_by_node: # calc load per server and add to result
        load = len(y)
        if(not is_balanced(load, avg_load)):
            not_balanced += 1
    imbalance_ratio = not_balanced / MACHINES
    ratios.append(imbalance_ratio)

plot(ratios,k, 'Imbalance ratio per amount of nodes', 'load imbalance ratio', 'Amount of nodes per machine')