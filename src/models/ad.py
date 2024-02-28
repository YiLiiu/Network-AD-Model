import random
from .software import Software
from .network import Network


# Define the Attacker class
class Attacker:
    def __init__(self, network: Network):
        self.network = network
        # Knowledge about the network, saved as:
        # set of software instances
        self.knowledge = self.init_knowledge()
        self.strategy = self.init_strategy()
        self.t = 0

    def init_knowledge(self) -> set[Software]:
        # Initialize the knowledge about the network, get all the compromised nodes, record as id: 
        knowledge = set()
        for computer in self.network.computers:
            if computer.os.state == 1 and computer.os.attack_phase == -1:
                knowledge.add(computer.os)
                computer.os.attack_phase = 0
            for app in computer.apps:
                if app.state == 1 and app.attack_phase == -1:
                    knowledge.add(app)
                    app.attack_phase = 0
        return knowledge

    def init_strategy(self) -> dict:
        # Simulate attacker's strategy phases based on MITRE's ATT&CK
        return {
            -1: "No Attack",        # No attack
            0: "Discovered",         # Phase 0
            1: "Installation",      # Phase 1
            2: "Discovery",         # Phase 2
            3: "Privilege Escalation",  # Phase 3
            4: "Lateral Movement",  # Phase 4
            5: "Causing Damages"    # Phase 5
        }
    
    def installation_phase(self):
        # Update the knowledge, for the 0 phase, the attacker installs the malware
        for sw in self.knowledge:
            if sw.attack_phase == 0:
                sw.attack_phase = 1
                sw.state = 1

    def discovery_phase(self):
        # Update the knowledge, for the 1 phase, the attacker discovers the network
        discovered_sws = set()
        for sw in self.knowledge:
            if sw.attack_phase == 1:
                sw.attack_phase = 2
                # Get the connected apps
                connected_sws = self.network.get_connected_software(sw)
                for connected_sw in connected_sws:
                    # If the connected software is not compromised, add it to the knowledge
                    if connected_sw.attack_phase == -1 and connected_sw not in self.knowledge and connected_sw.state != 2:
                        # Check if there is a exploit matching the vulnerabilities of the connected software
                        exploits = self.network.exploits[connected_sw.get_software_type()]
                        vulnerabilities = connected_sw.get_vulnerabilities()
                        for exploit in exploits:
                            if vulnerabilities[exploit] == 1:
                                discovered_sws.add(connected_sw)
                                break
        self.knowledge.update(discovered_sws)

    def privilege_escalation_phase(self):
        # Upgrade the attack phase for the discovered OS
        for sw in self.knowledge:
            if sw.get_software_type() != 'OS' and sw.attack_phase == 2:
                sw.attack_phase = 3
                connected_sws = self.network.get_connected_software(sw)
                for connected_sw in connected_sws:
                    if connected_sw.attack_phase == -1 and connected_sw in self.knowledge and connected_sw.get_software_type() == 'OS':
                        connected_sw.attack_phase = 0

    def lateral_movement_phase(self):
        # Upgrade the attack phase for the discovered apps
        for sw in self.knowledge:
            if sw.attack_phase == 2 or sw.attack_phase == 3:
                sw.attack_phase = 4
                connected_sws = self.network.get_connected_software(sw)
                for connected_sw in connected_sws:
                    if connected_sw.attack_phase == -1 and connected_sw in self.knowledge and connected_sw.get_software_type() != 'OS':
                        connected_sw.attack_phase = 0

    def causing_damages_phase(self):
        # Upgrade the attack phase for the phase 4
        for sw in self.knowledge:
            if sw.attack_phase == 4:
                sw.attack_phase = 5

    def update_state(self):
        for computer in self.network.computers:
            computer.update_state()
        self.network.update_cc()
        self.network.update_vc()
        self.network.update_ic()

    def attack(self):
        attack_choice = self.t % 5
        if attack_choice == 0:
            self.installation_phase()
        elif attack_choice == 1:
            self.discovery_phase()
        elif attack_choice == 2:
            self.privilege_escalation_phase()
        elif attack_choice == 3:
            self.lateral_movement_phase()
        elif attack_choice == 4:
            self.causing_damages_phase()
        self.t += 1
        self.update_state()

# Define the Defender class
class Defender:
    def __init__(self, network: Network, strategy: str, algorithm: str):
        self.network = network
        # Strategy: "Static" or "Proactive" or "Reactive"
        self.strategy = strategy
        # Function to update the software implementation
        self.algorithm = self.init_algorithm(algorithm)
        self.t = 0

    def init_algorithm(self, algorithm: str):
        if algorithm.lower() == "random":
            return self.random_algorithm
        elif algorithm.lower == "colorflipping":
            return self.color_flipping_algorithm

    def random_algorithm(self, proportion: float):
        # Randomly select a proportion of the software redefine the implementation
        for computer in self.network.computers:
            if random.random() < proportion:
                computer.os.update_implementation(random.choice(self.network.os_versions))
                for app in computer.apps:
                    app.update_implementation(random.choice(self.network.app1_versions) if app.get_software_type() == 'APP1' else random.choice(self.network.app2_versions))
    
    def color_flipping_algorithm(self, proportion: float):
        pass

    def defend(self):
        if self.strategy.lower() == "static":
            if self.t == 0:
                # Randomly select a proportion of the software and redefine the implementation
                # self.algorithm(1)
                pass
        elif self.strategy.lower() == "proactive":
            # Every 5 time steps, randomly select a proportion of the software and redefine the implementation
            if self.t % 5 == 0:
                self.algorithm(0.5)
        elif self.strategy.lower() == "reactive":
            pass
        self.t += 1

