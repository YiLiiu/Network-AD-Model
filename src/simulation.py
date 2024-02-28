from .models import Network, Attacker, Defender

class Simulation:
    def __init__(self, num_computers: int, num_app_versions: int, compromised_sw: int, x_range, y_range):
        self.network = Network(num_computers, num_app_versions, compromised_sw, x_range, y_range)
        self.attacker = Attacker(self.network)
        self.defender = Defender(self.network, "Static", "Random")
        self.tau_index = 0
        self.tts_list = []

    def run(self, time_steps: int, taus: list[float]) -> tuple[list[float], list[int]]:
        for t in range(time_steps):
            self.attacker.attack()
            print(f"At time {t}, {self.net_info()}")
            if self.tau_index == len(taus):
                break
            while self.tau_index < len(taus) and self.network.cc >= taus[self.tau_index]:
                self.tts_list.append(t)
                self.tau_index += 1
        taus = taus[:len(self.tts_list)]
        return taus, self.tts_list
    
    def net_info(self):
        return f"VC: {self.network.vc}; CC: {self.network.cc}; IC: {self.network.ic}"