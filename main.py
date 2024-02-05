from models import *

# Create a Network
net = Network(5,3,[0, 10],[0,10])

net.print_diversity_configurations()

print(net.get_connected_apps())

net.plot()