from models import *

# Create a Network
net = Network(5,3,[0, 10],[0,10])

t_range = [0,10]

net.print_diversity_configurations()
net.print_st()
net.print_spt()

print(net.get_connected_apps())

print(f"VC: {net.vc}")
print(f"CC: {net.cc}")
print(f"IC: {net.ic}")

# net.plot()

print("Compromised SWs before attack:")
compromised_sws = net.get_compromised_softwares()
for sw in compromised_sws:
    print(sw.get_info())

attacker = Attacker(net)
defender = Defender(net, "Static", "Random")
t = 10
for i in range(t):
    attacker.attack()
    defender.defend()

    compromised_sws = net.get_compromised_softwares()
    print(f"Compromised SWs at t={i+1}:")
    for sw in compromised_sws:
        print(sw.get_info())

    print(f"VC: {net.vc}")
    print(f"CC: {net.cc}")
    print(f"IC: {net.ic}")

# Set compromised apps and os
# net.computers[0].os.