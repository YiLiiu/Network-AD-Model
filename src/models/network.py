import random
import itertools
import networkx as nx

from .software import OperatingSystem, Application, Implementation, Software

random.seed(12)

class Computer:
    def __init__(self, id: int, os: OperatingSystem, apps: list[Application], x_position, y_position):
        self.id = id
        self.os = os
        self.apps = apps
        self.update_state()
        # Position in the network, used for visualization
        self.x_position = x_position
        self.y_position = y_position

    def update_state(self):
        # Calculate the state based on the os and apps states
        # If any of the os or apps is compromised, the computer is compromised
        # If any of the os or apps is vulnerable and none is compromised, the computer is vulnerable
        state = self.os.state
        if state == 1:
            self.state = 1
            return
        for app in self.apps:
            if app.state == 1:
                state = 1
                break
            state = min(state, app.state)
        self.state = state
        return

class Network:
    def __init__(self, num_computers: int, num_app_versions: int, compromised_sw: int, num_exploits: int = 2):
        self.num_computers = num_computers
        self.num_app_versions = num_app_versions
        self.num_exploits = num_exploits
        self.x_range = [0, 100]
        self.y_range = [0, 100]
        self.os_versions = self.init_sw_versions("OS")
        self.vulnerabilities = self.init_vulnerabilities(["OS", "APP1", "APP2"])
        self.exploits = self.init_exploits(["OS", "APP1", "APP2"])
        self.app1_versions = self.init_sw_versions("APP1", 1+num_app_versions)
        self.app2_versions = self.init_sw_versions("APP2", 1+2*num_app_versions)
        self.computers = self.init_computers()
        self.graph = self.generate_graph()
        self.init_compromised_sw(compromised_sw)
        self.update_cc()
        self.update_vc()
        self.update_ic()

    def init_sw_versions(self, sw_type: str, start_version: int = 1):
        sw_versions = []
        for i in range(start_version, start_version + self.num_app_versions):
            # choose a random number of vulnerabilities for each implementation
            if sw_type == "OS":
                vulnerabilities_range = range(0, 5)
            elif sw_type == "APP1":
                vulnerabilities_range = range(5, 10)
            elif sw_type == "APP2":
                vulnerabilities_range = range(10, 15)
            sw_versions.append(Implementation(sw_type, i, 15, random.sample(vulnerabilities_range, random.randint(1, len(vulnerabilities_range)))))
        return sw_versions
    
    def init_vulnerabilities(self, app_types: list[str]):
        vulnerabilities = []
        for app_type in app_types:
            vulnerabilities.extend(f'{app_type}-VUL-{i}' for i in range(1, 6))
        return vulnerabilities
    
    def init_exploits(self, sws_types: list[str]) -> dict[str, list[int]]:
        exploits = {}
        for sw_type in sws_types:
            if sw_type == "OS":
                vulnerabilities_range = range(0, 5)
            elif sw_type == "APP1":
                vulnerabilities_range = range(5, 10)
            elif sw_type == "APP2":
                vulnerabilities_range = range(10, 15)
            # Randomly select 2 vulnerabilities for each app type
            exploits[sw_type] = random.sample(vulnerabilities_range, self.num_exploits)
        return exploits

    def init_computers(self) -> list[Computer]:
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

    def init_compromised_sw(self, compromised_sw: int):
        # Randomly set the compromised software
        compromised_sw = random.sample(self.computers, compromised_sw)
        for computer in compromised_sw:
            sws = [computer.os] + computer.apps
            sw = random.choice(sws)
            sw.state = 1
            print(f'Computer{computer.id}: {sw.get_software_type()}_{sw.id} is compromised')
        return

    def generate_graph(self) -> dict:
        graphs = {}
        graph1, graph2 = nx.Graph(), nx.Graph()
        for computer in self.computers:
            for app in computer.apps:
                if app.get_software_type() == 'APP1':
                    graph1.add_node(app)
                elif app.get_software_type() == 'APP2':
                    graph2.add_node(app)
        # Connect nodes with a probability of 0.4 in the same app graph
        for application1, application2 in itertools.combinations(graph1.nodes(), 2):
            if random.random() < 0.4:
                graph1.add_edge(application1, application2)
        for application1, application2 in itertools.combinations(graph2.nodes(), 2):
            if random.random() < 0.4:
                graph2.add_edge(application1, application2)
        graphs['APP1'] = graph1
        graphs['APP2'] = graph2
        return graphs

    def print_diversity_configurations(self):
        # Print the diversity configurations for each computer
        for computer in self.computers:
            print(f'OS{computer.id}: implementation{computer.os.implementation.implementation_type}')
            for app in computer.apps:
                print(f'{app.get_software_type()}{app.id}: implementation{app.implementation.implementation_type}')

    def print_st(self):
        # Print the state of the network
        for computer in self.computers:
            print(f'OS{computer.id}: St={computer.os.state}')
            for app in computer.apps:
                print(f'{app.get_software_type()}{app.id}: St={app.state}')

    def print_spt(self):
        # Print the state of the network
        for computer in self.computers:
            print(f'Computer{computer.id}: S\'t={computer.state}')

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
        connected_software = []
        # Get the apps on the same computer
        computer = self.get_computer(id)
        for app in computer.apps:
            if app.get_software_type() != sw_type:
                connected_software.append(app)
        if sw_type == 'OS':
            return connected_software
        connected_software.append(computer.os)
        app_graph = self.graph[sw_type]
        for edge in app_graph.edges():
            if edge[0] == software:
                connected_software.append(edge[1])
            elif edge[1] == software:
                connected_software.append(edge[0])
        return connected_software
    
    def update_vc(self):
        # Calculate the vulnerability coverage
        vc = 0
        for computer in self.computers:
            if computer.state == 0:
                vc += 1
        self.vc = vc / self.num_computers
        return
    
    def update_cc(self):
        # Calculate the connectivity coverage
        cc = 0
        for computer in self.computers:
            if computer.state == 1:
                cc += 1
        self.cc = cc / self.num_computers
        return
    
    def update_ic(self):
        # Calculate the integrity coverage
        ic = 0
        for computer in self.computers:
            if computer.state == 2:
                ic += 1
        self.ic = ic / self.num_computers
        return
    
    def cal_cswc(self):
        # Calculate the compromised software coverage
        csw = 0
        sw_num = 0
        for computer in self.computers:
            sw_num += 1
            if computer.os == 1:
                csw += 1
            for app in computer.apps:
                sw_num += 1
                if app.state == 1:
                    csw += 1    
        return csw / sw_num
    
    def get_compromised_softwares(self) -> list[Software]:
        # Get the compromised software
        compromised_software = []
        for computer in self.computers:
            if computer.os.state == 1:
                compromised_software.append(computer.os)
            for app in computer.apps:
                if app.state == 1:
                    compromised_software.append(app)
        return compromised_software
        
    def get_invulnerable_softwares(self) -> list[Software]:
        # Get the invulnerable software
        invulnerable_software = []
        for computer in self.computers:
            if computer.os.state == 2:
                invulnerable_software.append(computer.os)
            for app in computer.apps:
                if app.state == 2:
                    invulnerable_software.append(app)
        return invulnerable_software