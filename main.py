from matplotlib import pyplot as plt

from src import Simulation, Network

net_base = Network(250, 1, 5, 5)
net1 = Network(250, 3, 5)
net2 = Network(250, 3, 5)

sim_base = Simulation(net_base, 'Static', 'Random')
sim1 = Simulation(net1, 'Static', 'Random')
sim2 = Simulation(net2, 'Proactive', 'Random')

taus_base, tts_list_base = sim_base.run(30, [0.05*i for i in range(11)])
taus1, tts_list1 = sim1.run(30, [0.05*i for i in range(11)])
taus2, tts_list2 = sim2.run(30, [0.05*i for i in range(11)])

asd1 = [tts_list1[i] - tts_list_base[i] for i in range(len(tts_list1))]
asd2 = [tts_list2[i] - tts_list_base[i] for i in range(len(tts_list2))]

# plt.plot(taus1, tts_list1, label="Static")
# plt.plot(taus2, tts_list2, label="Proactive")
# plt.legend()
# plt.xlabel("Tau")
# plt.ylabel("Time to compromise")
# plt.title("Tau vs Time to compromise")
# plt.show()

plt.plot(taus1, asd1, label="Static")
plt.plot(taus2, asd2, label="Proactive")
plt.legend()
plt.xlabel("Tau")
plt.ylabel("ASD")
plt.title("Tau vs ASD")
plt.show()