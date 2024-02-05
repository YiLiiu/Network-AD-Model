import random
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class Implementation:
    def __init__(self, type: str, implementation_type: int, vulnerabilities: list[str] = []):
        # Software type (OS, App1, App2, etc.)
        self.type = type
        # Implementation type, e.g., Windows, Linux, Mac for OS etc. using numbers for simplicity
        self.implementation_type = implementation_type
        self.vulnerabilities = vulnerabilities

    def set_vulnerabilities(self, vulnerabilities: list[str]):
        self.vulnerabilities = vulnerabilities

    def get_info(self):
        return f'{self.type} with corresponding implementation type {self.implementation_type}.'

class Software:
    def __init__(self, id: int, implementation: Implementation, state: int = 1):
        # Unique identifier
        self.id = id
        self.implementation= implementation
        # Vulnerabilities (0: invulnerable, 1: vulnerable, 2: compromised)
        self.state = state

    def set_state_based_on_vulnerabilities(self):
        # If the state is already compromised, do nothing
        if self.state == 2:
            return
        # If there are vulnerabilities, set the state to 1 (vulnerable)
        self.state = 1 if len(self.implementation.vulnerabilities) > 0 else 0

    def get_app_type(self):
        return self.implementation.type

    def get_info(self):
        return f'{self.implementation.get_info()} with state {self.state}.'

class OperatingSystem(Software):
    def __init__(self, id: int, implementation: Implementation, state: int):
        super().__init__(id, implementation, state)


class Application(Software):
    def __init__(self, id: int, implementation: Implementation, state: int):
        super().__init__(id, implementation, state)

class Computer:
    def __init__(self, id: int, os: OperatingSystem, apps: list[Application], x_position, y_position):
        self.id = id
        self.os = os
        self.apps = apps
        # Position in the network, used for visualization
        self.x_position = x_position
        self.y_position = y_position

class Network:
    def __init__(self, num_computers: int, num_app_versions: int, x_range, y_range):
        self.num_computers = num_computers
        self.num_app_versions = num_app_versions
        self.x_range = x_range
        self.y_range = y_range
        self.os_versions = self.initialize_app_versions("OS")
        self.app1_versions = self.initialize_app_versions("APP1")
        self.app2_versions = self.initialize_app_versions("APP2")
        self.computers = self.initialize_computers()
        self.netwrok = self.generate_network()

    def initialize_app_versions(self, app_type: str):
        app_versions = []
        vulnerabilities = self.initialize_vulnerabilities(app_type)
        for i in range(1, self.num_app_versions + 1):
            # choose a random number of vulnerabilities for each implementation
            app_versions.append(Implementation(app_type, i, random.sample(vulnerabilities, random.randint(0, len(vulnerabilities)))))
        return app_versions
    
    def initialize_vulnerabilities(self, app_type: str):
        return [f'{app_type}-VUL-{i}' for i in range(1, 6)]

    def initialize_computers(self) -> list[Computer]:
        computers = []
        for i in range(self.num_computers):
            os = OperatingSystem(i, random.choice(self.os_versions), 1)
            # Randomly create applications for each computer
            apps = []
            if random.random() < 0.8:
                apps.append(Application(i, random.choice(self.app1_versions), 1))
            if random.random() < 0.6 or len(apps) == 0:
                apps.append(Application(i, random.choice(self.app2_versions), 1))
            computer = Computer(i, os, apps, random.uniform(self.x_range[0], self.x_range[1]), random.uniform(self.y_range[0], self.y_range[1]))
            computers.append(computer)
        return computers

    def generate_network(self):
        graphs = {}
        graph1, graph2 = nx.Graph(), nx.Graph()
        for computer in self.computers:
            for app in computer.apps:
                if app.get_app_type() == 'APP1':
                    graph1.add_node(computer.id)
                elif app.get_app_type() == 'APP2':
                    graph2.add_node(computer.id)
        # Connect nodes with a probability of 0.8 in the same app graph
        for user1, user2 in itertools.combinations(graph1.nodes(), 2):
            if random.random() < 0.8:
                graph1.add_edge(user1, user2)
        for user1, user2 in itertools.combinations(graph2.nodes(), 2):
            if random.random() < 0.8:
                graph2.add_edge(user1, user2)
        graphs['APP1'] = graph1
        graphs['APP2'] = graph2
        return graphs

    def print_diversity_configurations(self):
        # Print the diversity configurations for each computer
        for computer in self.computers:
            print(f'Computer {computer.id} has OS: {computer.os.get_info()} and Apps: {[app.get_info() for app in computer.apps]}')

    def get_connected_apps(self):
        app1_graph = self.netwrok['APP1']
        app2_graph = self.netwrok['APP2']
        connected_apps = []
        for edge in app1_graph.edges():
            connected_apps.append(f"APP1_{edge[0]}-APP1_{edge[1]}")
        for edge in app2_graph.edges():
            connected_apps.append(f"APP2_{edge[0]}-APP2_{edge[1]}")
        return connected_apps


    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        layers = {'OS': 0, 'APP1': 1, 'APP2': 2}

        cmap_os = cm.get_cmap('Blues')
        cmap_app1 = cm.get_cmap('Reds')
        cmap_app2 = cm.get_cmap('Greens')
        num_types = self.num_app_versions  # 假设implementation_type的数量

    
        for computer in self.computers:
            # determine the color based on the implementation type
            os_color = cmap_os(computer.os.implementation.implementation_type / num_types)
            os_position = (computer.x_position, computer.y_position, layers['OS'])
            ax.scatter(*os_position[:-1], os_position[2], c=os_color, marker='o')
            ax.text(*os_position, f'{computer.id}-OS', color='black')
            
            # store the positions of the apps
            app_positions = []
            
            # APPs
            for app in computer.apps:
                z_layer = layers[app.get_app_type()]
                app_position = (computer.x_position, computer.y_position, z_layer)
                if app.get_app_type() == 'APP1':
                    app_color = cmap_app1(app.implementation.implementation_type / num_types)
                elif app.get_app_type() == 'APP2':
                    app_color = cmap_app2(app.implementation.implementation_type / num_types)
                ax.scatter(*app_position[:-1], app_position[2], c=app_color, marker='^')
                ax.text(*app_position, f'{computer.id}-{app.get_app_type()}', color='black')
                
                app_positions.append(app_position)
            
            # Draw the edges between OS and APPs
            for app_pos in app_positions:
                ax.plot([os_position[0], app_pos[0]], [os_position[1], app_pos[1]], [os_position[2], app_pos[2]], c='black')

        # Draw the edges
        for app_name, graph in self.netwrok.items():
            z_layer = layers[app_name]
            for edge in graph.edges():
                x_positions = [self.computers[edge[0]].x_position, self.computers[edge[1]].x_position]
                y_positions = [self.computers[edge[0]].y_position, self.computers[edge[1]].y_position]
                z_positions = [z_layer, z_layer]
                ax.plot(x_positions, y_positions, z_positions, c='black')
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Layer')
        plt.show()






# Define the Attacker class
class Attacker:
    def __init__(self):
        self.knowledge = {}  # Attacker's knowledge at each time step t
        self.goal = {}       # Attacker's goal at each time step t
        self.strategy = []   # Attacker's strategy phases
        self.capability = {}  # Attacker's capabilities for each phase and exploit
        self.decision_making = {}  # Attacker's decision-making algorithm

    def simulate_initial_knowledge(self, IniComp):
        # Simulate attacker's initial knowledge
        self.knowledge[0] = {
            "G": None,       # Attacker's perception of the communication graph
            "C": None,       # Attacker's perception of the network diversity configuration
            "Phi": None,     # Attacker's perception of vulnerabilities
            "S": None        # Attacker's perception of the network-wide cybersecurity state
        }
        # Assume attacker knows IniComp
        self.knowledge[0]["S"] = {"Compromised Programs": IniComp}

    def simulate_goal(self, T):
        # Simulate attacker's goal to compromise as many programs as possible till time T
        for t in range(T + 1):
            self.goal[t] = {"Compromise All Programs": 1}

    def simulate_strategy(self):
        # Simulate attacker's strategy phases based on MITRE's ATT&CK
        self.strategy = [
            "Installation",      # Phase 1
            "Discovery",         # Phase 2
            "Privilege Escalation",  # Phase 3
            "Lateral Movement",  # Phase 4
            "Causing Damages"    # Phase 5
        ]

    def simulate_capability(self):
        # Simulate attacker's capabilities as described
        for phase in self.strategy:
            self.capability[phase] = []
            if phase == "Installation":
                self.capability[phase].append("Remote Access Exploit")
            elif phase == "Discovery":
                self.capability[phase].append("Remote System Discovery Exploit")
                self.capability[phase].append("Local System Discovery Exploit")
            elif phase == "Privilege Escalation":
                # Simulate multiple privilege escalation exploits
                self.capability[phase].append("Privilege Escalation Exploit 1")
                self.capability[phase].append("Privilege Escalation Exploit 2")
            elif phase == "Lateral Movement":
                # Simulate multiple lateral movement exploits
                self.capability[phase].append("Lateral Movement Exploit 1")
                self.capability[phase].append("Lateral Movement Exploit 2")
            elif phase == "Causing Damages":
                self.capability[phase].append("Damaging Exploit")

    def simulate_decision_making(self):
        # Simulate attacker's decision-making algorithm
        # Define the decision-making algorithm as described
        self.decision_making = {
            "Installation": "Remote Access Exploit",
            "Discovery": ["Remote System Discovery Exploit", "Local System Discovery Exploit"],
            "Privilege Escalation": "Select Exploit based on Vulnerabilities",
            "Lateral Movement": "Select Exploit based on Vulnerabilities",
            "Causing Damages": "Damaging Exploit"
        }

    def make_attack_plan(self, time):
        # Simulate attacker's decision-making based on the current time and knowledge
        phase = self.strategy[time % len(self.strategy)]  # Cycle through phases
        decision = self.decision_making[phase]
        if isinstance(decision, list):
            # If multiple options, choose one randomly
            import random
            exploit_choice = random.choice(decision)
        else:
            exploit_choice = decision
        return exploit_choice

# Define the Defender class
class Defender:
    def __init__(self):
        self.knowledge = {}

    def observe(self, network):
        # Collect data about the network
        pass

    def orient(self):
        # Analyze the collected data
        pass

    def decide(self):
        # Make a decision based on analysis
        pass

    def act(self, network):
        # Execute the decision
        pass
