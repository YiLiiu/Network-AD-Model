from models import *
import matplotlib.pyplot as plt

# Create a Network
net = Network(20, 3, [0, 50], [0,50])

t_range = [0,10]

net.print_diversity_configurations()
net.print_st()
net.print_spt()

print(net.get_connected_apps())

print(f"VC: {net.vc}")
print(f"CC: {net.cc}")
print(f"IC: {net.ic}")

# net.plot()

print("Invulnerable SWs:")
invulnerable_sws = net.get_invulnerable_softwares()
for sw in invulnerable_sws:
    print(sw)

print("Compromised SWs before attack:")
compromised_sws = net.get_compromised_softwares()
for sw in compromised_sws:
    print(sw)

attacker = Attacker(net)
defender = Defender(net, "Static", "Random")
time_steps = 30
# tau from 0.00 to 0.50, 0.05 step
taus = [0.05*i for i in range(11)]
tts_list = []
tau_index = 0
for t in range(time_steps):
    attacker.attack()
    # defender.defend()

    if tau_index == len(taus):
        break
    while tau_index < len(taus) and net.cc >= taus[tau_index]:
        tts_list.append(t)
        tau_index += 1
        print(f"At time {t}, VC: {net.vc}, CC: {net.cc}, IC: {net.ic}")

    # compromised_sws = net.get_compromised_softwares()
    # print(f"Compromised SWs at t={t}:")
    # for sw in compromised_sws:
    #     print(sw)


# Short the tau list to the same length as tts_list
taus = taus[:len(tts_list)]

# plot tau vs tts
plt.plot(taus, tts_list)
plt.xlabel("Tau")
plt.ylabel("Time to compromise")
plt.title("Tau vs Time to compromise")
plt.show()

# Set compromised apps and os
# net.computers[0].os.
# net.plot()