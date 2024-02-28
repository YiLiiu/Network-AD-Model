import random

class Implementation:
    def __init__(self, type: str, implementation_type: int, num_vuls: int, vulnerabilities: list[int] = []):
        # Software type (OS, App1, App2, etc.)
        self.type = type
        # Implementation type, e.g., Windows, Linux, Mac for OS etc. using numbers for simplicity
        self.implementation_type = implementation_type
        self.vuls = self.generate_vuls(vulnerabilities, num_vuls)
        print(f'Implementation {self.implementation_type}: {self.vuls}')

    def generate_vuls(self, vulnerabilities: list[int], num_vuls: int):
        # vuls is a list 0 and 1 where 0 means no vulnerability and 1 means vulnerability
        vuls = [0] * num_vuls
        for vul in vulnerabilities:
            vuls[vul] = 1
        return vuls        

    def set_vulnerabilities(self, vulnerabilities: list[int]):
        self.vuls = vulnerabilities

    def __str__(self):
        return f'{self.type} with implementation {self.implementation_type}'
    
    def get_vulnerabilities(self):
        return self.vuls

class Software:
    def __init__(self, id: int, implementation: Implementation):
        # Unique identifier
        self.id = id
        self.implementation= implementation
        # Vulnerabilities (0: vulnerable, 1: compromised, 2: not vulnerable)
        self.state = self.init_state()
        self.attack_phase = -1 # -1: not attacked, 0: installation, 1: discovery, 2: privilege escalation, 3: lateral movement

    def init_state(self):
        # Calculate the state based on the vulnerabilities
        if 1 in self.implementation.vuls:
            # If there are vulnerabilities, set the state to 0 (vulnerable)
            return 0
        return 2

    def set_state_based_on_vulnerabilities(self):
        # If the state is already compromised, do nothing
        if self.state == 1:
            return
        # If there are vulnerabilities, set the state to 0 (vulnerable)
        self.state = 0 if len(self.implementation.vuls) > 0 else 2

    def set_attack_phase(self, phase: int):
        self.attack_phase = phase

    def get_software_type(self):
        return self.implementation.type

    def get_implementation_type(self):
        return self.implementation.implementation_type
    
    def get_vulnerabilities(self):
        return self.implementation.get_vulnerabilities()

    def __str__(self):
        return f'{self.implementation.type}_{self.id}'
    
    def update_implementation(self, implementation: Implementation):
        self.implementation = implementation
        self.set_state_based_on_vulnerabilities()

class OperatingSystem(Software):
    def __init__(self, id: int, implementation: Implementation):
        super().__init__(id, implementation)


class Application(Software):
    def __init__(self, id: int, implementation: Implementation):
        super().__init__(id, implementation)
