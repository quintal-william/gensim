from ..models.leaf import Leaf
from ...output import OmnestOutput

class InetTopologyOutput(OmnestOutput):
    def _print_ned_imports(self, leaves: list[Leaf]) -> None:
        # TODO only print necessary eth
        self._print("import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;")
        self._print("import inet.node.ethernet.Eth400G;")
        self._print("import inet.node.ethernet.Eth200G;")
        self._print("import inet.node.ethernet.Eth100G;")
        self._print("import inet.node.ethernet.Eth40G;")
        self._print("import inet.node.ethernet.Eth10G;")
        self._print("import inet.node.ethernet.Eth1G;")
        self._print("import inet.node.ethernet.Eth100M;")
        self._print("import inet.node.ethernet.Eth10M;")
        self._print("import nsim.nodes.InetNode;")

    def _print_ned_leaves(self, leaves: list[Leaf]) -> None:
        self._print("configurator: Ipv4NetworkConfigurator {", 2)
        self._print('@display("p=389,47");', 3)
        self._print("}", 2)
        for leaf in leaves:
            self._print(f"{leaf.get_id()}: InetNode;", 2)

    def _print_ned_connections(self, leaves: list[Leaf]) -> None:
        self._print()
        for leaf in leaves:
            self._print(f"entry.out++ --> {leaf.get_id()}.in;", 2)

        self._print()
        for leaf in leaves:
            self._print(f"{leaf.get_id()}.out --> exit.in++;", 2)

        self._print()
        seen: set[tuple[str, str]] = set()
        for leaf in leaves:
            for edge in leaf.get_edges():
                source = edge.get_source().get_id()
                destination = edge.get_destination().get_id()

                if (source, destination) not in seen:
                    seen.add((destination, source))
                    bandwidths = {
                        400000000000: "Eth400G",
                        200000000000: "Eth200G",
                        100000000000: "Eth100G",
                        40000000000: "Eth40G",
                        10000000000: "Eth10G",
                        1000000000: "Eth1G",
                        100000000: "Eth100M",
                        10000000: "Eth10M",
                    }
                    bandwidth = edge.get_bandwidth()
                    sorted_bandwidths = sorted(bandwidths.items(), key=lambda x: abs(x[0] - bandwidth))
                    self._print(f"{source}.ethg++ <--> {sorted_bandwidths[0][1]} <--> {destination}.ethg++;", 2)

    def _print_ini_leaves(self, leaves: list[Leaf]) -> None:
        for leaf in leaves:
            leaf_id = leaf.get_id()
            leaf_edges = leaf.get_edges()

            self._print()
            self._print(f'**.{leaf_id}.numApps = {len(leaf_edges) + 1}')
            self._print(f'**.{leaf_id}.app[0].typename = "TcpSinkApp"')

            for index, edge in enumerate(leaf_edges):
                prefix = f'**.{leaf_id}.app[{index + 1}]'
                destination = edge.get_destination().get_id()
                self._print(f'{prefix}.typename = "InetSendApp"')
                self._print(f'{prefix}.localAddress = "{leaf_id}"')
                self._print(f'{prefix}.connectAddress = "{destination}"')
