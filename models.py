import random
import itertools
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

class Implementation:
    def __init__(self, type: str, implementation_type: int, num_vuls: int, vulnerabilities: list[int] = []):
        # Software type (OS, App1, App2, etc.)
        self.type = type
        # Implementation type, e.g., Windows, Linux, Mac for OS etc. using numbers for simplicity
        self.implementation_type = implementation_type
        self.vuls = self.generate_vuls(vulnerabilities, num_vuls)
        print(f'The {self.implementation_type} type of {self.type} has vulnerabilities: {self.vuls}.')

    def generate_vuls(self, vulnerabilities: list[int], num_vuls: int):
        # vuls is a list 0 and 1 where 0 means no vulnerability and 1 means vulnerability
        vuls = [0] * num_vuls
        for vul in vulnerabilities:
            vuls[vul] = 1
        return vuls        

    def set_vulnerabilities(self, vulnerabilities: list[int]):
        self.vuls = vulnerabilities

    def get_info(self):
        return f'{self.type} with corresponding implementation type {self.implementation_type}.'
    
    def get_vulnerabilities(self):
        return self.vuls

class Software:
    def __init__(self, id: int, implementation: Implementation):
        # Unique identifier
        self.id = id
        self.implementation= implementation
        # Vulnerabilities (0: vulnerable, 1: compromised, 2: not vulnerable)
        self.state = self.cal_state()
        self.attack_phase = -1 # -1: not attacked, 0: installation, 1: discovery, 2: privilege escalation, 3: lateral movement

    def cal_state(self):
        # Calculate the state based on the vulnerabilities
        if 1 in self.implementation.vuls:
            # If there are vulnerabilities, at least vulnerable, also have 1/4 chance to be compromised
            return 1 if random.random() < 0.25 else 0
        return 2

    def set_state_based_on_vulnerabilities(self):
        # If the state is already compromised, do nothing
        if self.state == 2:
            return
        # If there are vulnerabilities, set the state to 1 (vulnerable)
        self.state = 1 if len(self.implementation.vuls) > 0 else 0

    def set_attack_phase(self, phase: int):
        self.attack_phase = phase

    def get_software_type(self):
        return self.implementation.type

    def get_implementation_type(self):
        return self.implementation.implementation_type

    def get_info(self):
        return f'{self.implementation.get_info()} with state {self.state}.'

class OperatingSystem(Software):
    def __init__(self, id: int, implementation: Implementation):
        super().__init__(id, implementation)


class Application(Software):
    def __init__(self, id: int, implementation: Implementation):
        super().__init__(id, implementation)

class Computer:
    def __init__(self, id: int, os: OperatingSystem, apps: list[Application], x_position, y_position):
        self.id = id
        self.os = os
        self.apps = apps
        self.state = self.cal_state()
        # Position in the network, used for visualization
        self.x_position = x_position
        self.y_position = y_position

    def cal_state(self):
        # Calculate the state based on the os and apps states
        # If any of the os or apps is compromised, the computer is compromised
        # If any of the os or apps is vulnerable and none is compromised, the computer is vulnerable
        state = self.os.state
        for app in self.apps:
            state = max(state, app.state)
        return state

class Network:
    def __init__(self, num_computers: int, num_app_versions: int, x_range, y_range):
        self.num_computers = num_computers
        self.num_app_versions = num_app_versions
        self.x_range = x_range
        self.y_range = y_range
        self.os_versions = self.initialize_sw_versions("OS")
        self.vulnerabilities = self.initialize_vulnerabilities(["OS", "APP1", "APP2"])
        self.app1_versions = self.initialize_sw_versions("APP1", 1+num_app_versions)
        self.app2_versions = self.initialize_sw_versions("APP2", 1+2*num_app_versions)
        self.computers = self.initialize_computers()
        self.graph = self.generate_graph()
        self.vc = self.calculate_vc()
        self.cc = self.calculate_cc()
        self.ic = self.calculate_ic()

    def initialize_sw_versions(self, sw_type: str, start_version: int = 1):
        sw_versions = []
        for i in range(start_version, start_version + self.num_app_versions):
            # choose a random number of vulnerabilities for each implementation
            if sw_type == "OS":
                vulnerabilities_range = range(0, 5)
            elif sw_type == "APP1":
                vulnerabilities_range = range(5, 10)
            elif sw_type == "APP2":
                vulnerabilities_range = range(10, 15)
            sw_versions.append(Implementation(sw_type, i, 15, random.sample(vulnerabilities_range, random.randint(0, len(vulnerabilities_range)))))
        return sw_versions
    
    def initialize_vulnerabilities(self, app_types: list[str]):
        vulnerabilities = []
        for app_type in app_types:
            vulnerabilities.extend(f'{app_type}-VUL-{i}' for i in range(1, 6))
        return vulnerabilities

    def initialize_computers(self) -> list[Computer]:
        computers = []
        for i in range(self.num_computers):
            os = OperatingSystem(i, random.choice(self.os_versions))
            # Randomly create applications for each computer
            apps = []
            if random.random() < 0.8:
                apps.append(Application(i, random.choice(self.app1_versions)))
            if random.random() < 0.6 or len(apps) == 0:
                apps.append(Application(i, random.choice(self.app2_versions)))
            computer = Computer(i, os, apps, random.uniform(self.x_range[0], self.x_range[1]), random.uniform(self.y_range[0], self.y_range[1]))
            computers.append(computer)
        return computers

    def generate_graph(self) -> dict:
        graphs = {}
        graph1, graph2 = nx.Graph(), nx.Graph()
        for computer in self.computers:
            for app in computer.apps:
                if app.get_software_type() == 'APP1':
                    graph1.add_node(app)
                elif app.get_software_type() == 'APP2':
                    graph2.add_node(app)
        # Connect nodes with a probability of 0.8 in the same app graph
        for application1, application2 in itertools.combinations(graph1.nodes(), 2):
            if random.random() < 0.8:
                graph1.add_edge(application1, application2)
        for application1, application2 in itertools.combinations(graph2.nodes(), 2):
            if random.random() < 0.8:
                graph2.add_edge(application1, application2)
        graphs['APP1'] = graph1
        graphs['APP2'] = graph2
        return graphs

    def print_diversity_configurations(self):
        # Print the diversity configurations for each computer
        for computer in self.computers:
            print(f'Computer {computer.id} has OS: {computer.os.get_info()} and Apps: {[app.get_info() for app in computer.apps]}')

    def get_computer(self, id: int) -> Computer:
        for computer in self.computers:
            if computer.id == id:
                return computer
        return None

    def get_connected_apps(self):
        app1_graph = self.graph['APP1']
        app2_graph = self.graph['APP2']
        connected_apps = []
        for edge in app1_graph.edges():
            connected_apps.append(f"APP1_{edge[0].id}-APP1_{edge[1].id}")
        for edge in app2_graph.edges():
            connected_apps.append(f"APP2_{edge[0].id}-APP2_{edge[1].id}")
        return connected_apps
    
    def get_connected_software(self, software: Software) -> list[Software]:
        # Get the connected apps for the given app type.
        sw_type = software.get_software_type()
        id = software.id
        app_graph = self.graph[sw_type]
        connected_software = []
        for edge in app_graph.edges():
            if edge[0] == id:
                connected_software.append(edge[1])
            elif edge[1] == id:
                connected_software.append(edge[0])
        # Get the apps on the same computer
        computer = self.get_computer(id)
        for app in computer.apps:
            if app.get_software_type() != sw_type:
                connected_software.append(app.id)
        return connected_software
    
    def calculate_vc(self):
        # Calculate the vulnerability coverage
        vc = 0
        for computer in self.computers:
            if computer.state == 0:
                vc += 1
        return vc / self.num_computers
    
    def calculate_cc(self):
        # Calculate the connectivity coverage
        cc = 0
        for computer in self.computers:
            if computer.state == 1:
                cc += 1
        return cc / self.num_computers
    
    def calculate_ic(self):
        # Calculate the integrity coverage
        ic = 0
        for computer in self.computers:
            if computer.state == 2:
                ic += 1
        return ic / self.num_computers
        
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
                z_layer = layers[app.get_software_type()]
                app_position = (computer.x_position, computer.y_position, z_layer)
                if app.get_software_type() == 'APP1':
                    app_color = cmap_app1(app.implementation.implementation_type / num_types)
                elif app.get_software_type() == 'APP2':
                    app_color = cmap_app2(app.implementation.implementation_type / num_types)
                ax.scatter(*app_position[:-1], app_position[2], c=app_color, marker='^')
                ax.text(*app_position, f'{computer.id}-{app.get_software_type()}', color='black')
                
                app_positions.append(app_position)
            
            # Draw the edges between OS and APPs
            for app_pos in app_positions:
                ax.plot([os_position[0], app_pos[0]], [os_position[1], app_pos[1]], [os_position[2], app_pos[2]], c='black')

        # Draw the edges
        for app_name, graph in self.graph.items():
            z_layer = layers[app_name]
            for edge in graph.edges():
                x_positions = [self.computers[edge[0].id].x_position, self.computers[edge[1].id].x_position]
                y_positions = [self.computers[edge[0].id].y_position, self.computers[edge[1].id].y_position]
                z_positions = [z_layer, z_layer]
                ax.plot(x_positions, y_positions, z_positions, c='black')
        
        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Layer')
        plt.show()

# Define the Attacker class
class Attacker:
    def __init__(self, network: Network):
        self.network = network
        # Knowledge about the network, saved as:
        # set of software instances
        self.knowledge = self.init_knowledge()
        self.strategy = self.init_strategy()

    def init_knowledge(self) -> set[Software]:
        # Initialize the knowledge about the network, get all the compromised nodes, record as id: 
        knowledge = set()
        for computer in self.network.computers:
            if computer.os.state == 2 and computer.os.attack_phase == -1:
                knowledge.add(computer.os)
                computer.os.attack_phase = 0
            for app in computer.apps:
                if app.state == 2 and app.attack_phase == -1:
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
                sw.state = 2

    def discovery_phase(self):
        # Update the knowledge, for the 1 phase, the attacker discovers the network
        for sw in self.knowledge:
            if sw.attack_phase == 1:
                sw.attack_phase = 2
                # Get the connected apps
                connected_sws = self.network.get_connected_software(sw)
                for connected_sw in connected_sws:
                    # If the connected software is not compromised, add it to the knowledge
                    if connected_sw.attack_phase == -1 and connected_sw not in self.knowledge:
                        self.knowledge.add(connected_sw)

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
