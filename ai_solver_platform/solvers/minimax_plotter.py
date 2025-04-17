import numpy as np
import matplotlib.pyplot as plt
from typing import List, Dict, Any

class MinimaxPlotter:
    def __init__(self, depth: int = 3, branching_factor: int = 2):
        self.depth = depth
        self.branching_factor = branching_factor
        self.nodes = []
        self.edges = []
        
    def generate_plot_data(self) -> Dict[str, Any]:
        """Generate data for plotting the minimax tree"""
        self._generate_tree()
        return {
            'nodes': self.nodes,
            'edges': self.edges,
            'depth': self.depth,
            'branching_factor': self.branching_factor
        }
        
    def _generate_tree(self):
        """Generate the minimax tree structure"""
        # Generate nodes
        for level in range(self.depth + 1):
            for node in range(self.branching_factor ** level):
                node_id = f"{level}_{node}"
                value = np.random.randint(-10, 11) if level == self.depth else None
                self.nodes.append({
                    'id': node_id,
                    'level': level,
                    'value': value,
                    'type': 'max' if level % 2 == 0 else 'min'
                })
                
        # Generate edges
        for level in range(self.depth):
            for parent in range(self.branching_factor ** level):
                parent_id = f"{level}_{parent}"
                for child in range(self.branching_factor):
                    child_id = f"{level + 1}_{parent * self.branching_factor + child}"
                    self.edges.append({
                        'from': parent_id,
                        'to': child_id
                    })
                    
    def plot_tree(self, save_path: str = None):
        """Plot the minimax tree and optionally save it"""
        plt.figure(figsize=(12, 8))
        
        # Plot nodes
        for node in self.nodes:
            x = node['level']
            y = int(node['id'].split('_')[1])
            plt.scatter(x, y, s=500, c='lightblue' if node['type'] == 'max' else 'lightgreen')
            plt.text(x, y, str(node['value']) if node['value'] is not None else node['type'],
                    ha='center', va='center')
                    
        # Plot edges
        for edge in self.edges:
            from_node = next(n for n in self.nodes if n['id'] == edge['from'])
            to_node = next(n for n in self.nodes if n['id'] == edge['to'])
            plt.plot([from_node['level'], to_node['level']],
                    [int(from_node['id'].split('_')[1]), int(to_node['id'].split('_')[1])],
                    'k-', alpha=0.3)
                    
        plt.title('Minimax Tree Visualization')
        plt.xlabel('Depth')
        plt.ylabel('Node Position')
        plt.grid(True, alpha=0.3)
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
            
        plt.close() 