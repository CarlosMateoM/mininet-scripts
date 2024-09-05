from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI

class Topology(Topo):

    def __init__(self, num_switches, num_hosts):
        
        # Initialize topology
        Topo.__init__(self)

        self.switch_list = []
        self.host_list = []

        for s in range(num_switches):
            switch = self.addSwitch('s%s' % s)  # Switch names starting from 0
            self.switch_list.append(switch)
        
        self.connect_switches()
        self.connect_hosts(num_hosts)

    def connect_switches(self):
        for i, switch in enumerate(self.switch_list):
            while True:
                user_input = input(f"Ingrese los números de switch para conectar con {switch} (separados por comas, o 'q' para terminar): ")
                if user_input.lower() == 'q':
                    break
                
                try:
                    connections = list(map(int, user_input.split(',')))
                    valid_connections = True
                    
                    for conn in connections:
                        if conn < 0 or conn >= len(self.switch_list) or conn == i:
                            valid_connections = False
                            print(f"Conexión no válida: {conn}. Debe ser un número entre 0 y {len(self.switch_list) - 1} y no puede ser el mismo switch.")
                            break
                    
                    if valid_connections:
                        for conn in connections:
                            self.addLink(switch, self.switch_list[conn])
                        break
                
                except ValueError:
                    print("Entrada no válida. Por favor ingrese números separados por comas.")

    def connect_hosts(self, num_hosts):
        for h in range(num_hosts):
            host = self.addHost(f'h{h}')
            self.host_list.append(host)
            while True:
                try:
                    switch_num = int(input(f"Ingrese el número de switch al que se debe conectar {host} (entre 0 y {len(self.switch_list) - 1}): "))
                    if switch_num < 0 or switch_num >= len(self.switch_list):
                        print(f"Conexión no válida. Debe ser un número entre 0 y {len(self.switch_list) - 1}.")
                    else:
                        switch = self.switch_list[switch_num]
                        self.addLink(host, switch)
                        break
                except ValueError:
                    print("Entrada no válida. Por favor ingrese un número válido.")

if __name__ == '__main__':
    
    num_switches = int(input("Ingrese el número de switches: "))
    num_hosts = int(input("Ingrese el número de hosts: "))

    setLogLevel('info')

    topo = Topology(num_switches, num_hosts)

    # Iniciar Mininet con la topología personalizada
    net = Mininet(topo=topo)
    net.start()

    # Iniciar la CLI de Mininet
    CLI(net)

    # Detener Mininet
    net.stop()