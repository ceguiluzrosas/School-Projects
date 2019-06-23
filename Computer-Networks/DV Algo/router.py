# Distance Vector Routing Algorithm

import socket
import sys
import time
import ast
import math

class Router():

    def __init__(self, host, port, num_routers, num_neighbors, neighbors_and_costs):
        self.host = host
        self.port = port
        self.num_routers = num_routers
        self.num_neighbors = num_neighbors
        self.neighbors_and_costs = neighbors_and_costs
        self.distance_vector = neighbors_and_costs.copy()

    def start(self):
        '''Creates sockets between windows'''
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((self.host, self.port))
        except OSError:
            print("Unable to allocate socket")
            sys.exit(0)

        while len(self.distance_vector)!=self.num_routers:
            self.send(sock)
            self.read(sock)

        # By Now All Routes & Distances Have Been Included
        # into Original Distance Vector
        while True:
            time.sleep(1)
            self.print_distance_vector()
            self.send(sock)
            self.read(sock)

    def read(self, sock):
        '''Read Distance Vector from Neighbor'''
        try:
            bin_vector, _ = sock.recvfrom(4096)
            decoded_vector = bin_vector.decode('utf-8')
            vector = ast.literal_eval(decoded_vector)
            self.update_distance_vector(vector)
        except ValueError:
            print ('unable to decode')
        except OSError:
            print ('request timeout')

    def send(self, sock):
        '''Send Distance Vector to all Neighbors'''
        for neighbor in self.neighbors_and_costs:
            bin_vector = str(self.distance_vector).encode('utf-8')
            sock.sendto(bin_vector, (self.host, neighbor))

    def print_distance_vector(self):
        '''Prints Distance Vector'''
        print ('-------------------------------------------')
        print ("Distance Vector for Node {}:".format(self.port))
        print (self.distance_vector)

    def update_distance_vector(self, recv_vector):
        '''Update my Distance Vector'''
        for router in recv_vector:
            if router not in self.neighbors_and_costs:
                self.distance_vector[router] = math.inf
            mini = min(self.distance_vector[router], recv_vector[router] + recv_vector[self.port])
            self.distance_vector[router] = mini
            self.neighbors_and_costs[router] = mini

def main():
    print (sys.argv, len(sys.argv))
    host = 'localhost'
    port = int(sys.argv[1])
    num_routers = int(sys.argv[2])
    num_neighbors = int(sys.argv[3])
    
    rest = sys.argv[4::]
    assert len(rest)%2==0 # make sure input includes both port and cost
    neighbors_and_costs = {} # {key: value} is {neighbor (port): cost (distance)}

    for i in range(0,len(rest),2):
        neighbors_and_costs[int(rest[i])] = int(rest[i+1]) 
    neighbors_and_costs[port] = 0 # adding my own distance to myself
    
    router = Router(host, port, num_routers, num_neighbors, neighbors_and_costs)
    router.start()

if __name__ == '__main__':
    main()
