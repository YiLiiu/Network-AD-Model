from matplotlib import pyplot as plt

from src import Simulation



sim = Simulation(100, 3, 5, [0, 50], [0, 50])

taus, tts_list = sim.run(30, [0.05*i for i in range(11)])

plt.plot(taus, tts_list)
plt.xlabel("Tau")
plt.ylabel("Time to compromise")
plt.title("Tau vs Time to compromise")
plt.show()