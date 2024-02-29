from matplotlib import pyplot as plt

from src import Simulation


sim1 = Simulation(200, 3, 5, 'Static', 'Random')
sim2 = Simulation(200, 3, 5, 'Proactive', 'Random')

taus1, tts_list1 = sim1.run(30, [0.05*i for i in range(11)])
taus2, tts_list2 = sim2.run(30, [0.05*i for i in range(11)])

plt.plot(taus1, tts_list1, label="Static")
plt.plot(taus2, tts_list2, label="Proactive")
plt.legend()
plt.xlabel("Tau")
plt.ylabel("Time to compromise")
plt.title("Tau vs Time to compromise")
plt.show()