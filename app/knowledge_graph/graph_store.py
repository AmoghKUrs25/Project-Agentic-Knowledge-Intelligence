import networkx as nx


class KnowledgeGraph:

    def __init__(self):
        self.graph = nx.Graph()

        relationships = [
            ("Machine Learning", "Artificial Intelligence"),
            ("Machine Learning", "Data Science"),
            ("Machine Learning", "Python"),
            ("Machine Learning", "PyTorch"),
            ("Machine Learning", "TensorFlow"),

            ("Cloud Computing", "Distributed Systems"),
            ("Cloud Computing", "Machine Learning"),

            ("Cybersecurity", "Authentication"),
            ("Cybersecurity", "Authorization"),
            ("Cybersecurity", "Secure Software Development"),

            ("Training", "Employee Development"),
            ("Training", "Technical Skills"),
            ("Training", "Machine Learning"),
            ("Training", "Cloud Computing"),
            ("Training", "Cybersecurity"),

            ("Leave Policy", "Employees"),
            ("Training Policy", "Employees"),
            ("Security Policy", "Employees")
        ]

        for source, target in relationships:
            self.graph.add_edge(source, target)

    def search(self, entity):
        if entity not in self.graph:
            return []

        return list(self.graph.neighbors(entity))

    def related_nodes(self, entity):
        if entity not in self.graph:
            return []

        return list(
            nx.single_source_shortest_path_length(
                self.graph,
                entity,
                cutoff=2
            ).keys()
        )