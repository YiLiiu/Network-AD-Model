from models import *

# Create a Network
net = Network(5,3,[0, 10],[0,10])

t_range = [0,10]

net.print_diversity_configurations()

print(net.get_connected_apps())

print(f"VC: {net.vc}")
print(f"CC: {net.cc}")
print(f"IC: {net.ic}")

net.plot()


# Set compromised apps and os
# net.computers[0].os.