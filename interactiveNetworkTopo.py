from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel
from mininet.node import RemoteController
from mininet.cli import CLI

class RedesTopo(Topo):
    def build(self, switch_qty, host_qty):
        switches = self.crear_switches(switch_qty)
        self.conectar_switches(switch_qty, switches)
        self.conectar_hosts(host_qty, switches)

    def crear_switches(self, switch_qty):
        switches = []
        for i in range(switch_qty):
            switch = self.addSwitch(f's{i}')
            switches.append(switch)
        return switches

    def conectar_switches(self, switch_qty, switches):
        for idx, switch in enumerate(switches):
            while True:
                input_conexiones = input(f"Indique las conexiones para {switch} (números de switches separados por comas, o 'q' para finalizar): ")
                if input_conexiones.lower() == 'q':
                    break
                
                try:
                    conexiones = [int(num) for num in input_conexiones.split(',')]
                    if all(0 <= conn < switch_qty and conn != idx for conn in conexiones):
                        for conn in conexiones:
                            self.addLink(switch, switches[conn])
                        break
                    else:
                        print(f"Entrada inválida. Asegúrese de que los números estén entre 0 y {switch_qty - 1}, y no sean el mismo switch.")
                except ValueError:
                    print("Entrada no válida. Por favor, ingrese números separados por comas.")

    def conectar_hosts(self, host_qty, switches):
        for i in range(host_qty):
            host = self.addHost(f'h{i}')
            while True:
                try:
                    switch_num = int(input(f"Indique el número de switch para conectar {host} (0 a {len(switches) - 1}): "))
                    if 0 <= switch_num < len(switches):
                        self.addLink(host, switches[switch_num])
                        break
                    else:
                        print(f"Conexión no válida. Debe ser un número entre 0 y {len(switches) - 1}.")
                except ValueError:
                    print("Entrada no válida. Por favor, ingrese un número válido.")

if __name__ == '__main__':
    setLogLevel('info')

    switch_qty = int(input("Número de switches: "))
    host_qty = int(input("Número de hosts: "))

    topo = RedesTopo(switch_qty=switch_qty, host_qty=host_qty)

    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    CLI(net)
    net.stop()
