import random
from typing import List, Tuple, Dict, Optional

class WumpusWorld:
    def __init__(self, size: int = 4, wumpus_pos: Optional[List[int]] = None, 
                 gold_pos: Optional[List[int]] = None, pit_positions: Optional[List[List[int]]] = None):
        self.size = size
        self.agent_pos = [0, 0]  # Start at bottom-left corner
        self.agent_direction = 'right'  # Initial direction
        self.has_gold = False
        self.has_arrow = True
        self.score = 0
        self.game_over = False
        self.won = False
        
        # Initialize world elements
        self.wumpus_pos = wumpus_pos or [random.randint(0, size-1), random.randint(0, size-1)]
        self.gold_pos = gold_pos or [random.randint(0, size-1), random.randint(0, size-1)]
        self.pit_positions = pit_positions or []
        
        # Ensure wumpus and gold are not at the start position
        while self.wumpus_pos == [0, 0]:
            self.wumpus_pos = [random.randint(0, size-1), random.randint(0, size-1)]
        while self.gold_pos == [0, 0]:
            self.gold_pos = [random.randint(0, size-1), random.randint(0, size-1)]
            
        # Initialize knowledge base
        self.knowledge = {
            'visited': [[False for _ in range(size)] for _ in range(size)],
            'safe': [[False for _ in range(size)] for _ in range(size)],
            'possible_wumpus': [[True for _ in range(size)] for _ in range(size)],
            'possible_pit': [[True for _ in range(size)] for _ in range(size)],
        }
        
        # Start cell is known safe
        self.knowledge['visited'][0][0] = True
        self.knowledge['safe'][0][0] = True
        self.knowledge['possible_wumpus'][0][0] = False
        self.knowledge['possible_pit'][0][0] = False

    def get_percepts(self) -> List[str]:
        """Return list of percepts at current position"""
        percepts = []
        x, y = self.agent_pos
        
        # Check for gold
        if self.agent_pos == self.gold_pos:
            percepts.append('Glitter')
            
        # Check for stench (adjacent to wumpus)
        if self._is_adjacent(self.agent_pos, self.wumpus_pos):
            percepts.append('Stench')
            
        # Check for breeze (adjacent to pit)
        for pit in self.pit_positions:
            if self._is_adjacent(self.agent_pos, pit):
                percepts.append('Breeze')
                break
                
        return percepts

    def move_agent(self, direction: str) -> Dict:
        """Move agent in specified direction and return result"""
        if self.game_over:
            return {'status': 'error', 'message': 'Game is already over'}
            
        # Update direction
        self.agent_direction = direction
        
        # Calculate new position
        new_pos = self.agent_pos.copy()
        if direction == 'up':
            new_pos[0] += 1
        elif direction == 'down':
            new_pos[0] -= 1
        elif direction == 'left':
            new_pos[1] -= 1
        elif direction == 'right':
            new_pos[1] += 1
            
        # Check if move is valid
        if not (0 <= new_pos[0] < self.size and 0 <= new_pos[1] < self.size):
            return {'status': 'error', 'message': 'Cannot move outside the grid'}
            
        # Update position and score
        self.agent_pos = new_pos
        self.score -= 1
        
        # Update knowledge
        self.knowledge['visited'][new_pos[0]][new_pos[1]] = True
        
        # Check for game events
        result = {
            'status': 'success',
            'new_position': self.agent_pos,
            'percepts': self.get_percepts(),
            'score': self.score,
            'game_over': False,
            'won': False
        }
        
        # Check for death
        if self.agent_pos == self.wumpus_pos:
            result['message'] = 'You were eaten by the Wumpus!'
            result['game_over'] = True
            self.game_over = True
        elif self.agent_pos in self.pit_positions:
            result['message'] = 'You fell into a pit!'
            result['game_over'] = True
            self.game_over = True
            
        # Check for win
        elif self.has_gold and self.agent_pos == [0, 0]:
            result['message'] = 'You won! You found the gold and returned safely!'
            result['game_over'] = True
            result['won'] = True
            self.game_over = True
            self.won = True
            
        else:
            result['message'] = f'Moved {direction}. Percepts: {", ".join(result["percepts"])}'
            
        return result

    def grab_gold(self) -> Dict:
        """Attempt to grab gold at current position"""
        if self.agent_pos == self.gold_pos and not self.has_gold:
            self.has_gold = True
            self.score += 1000
            return {
                'status': 'success',
                'message': 'You grabbed the gold! Now return to the start!',
                'score': self.score
            }
        return {
            'status': 'error',
            'message': 'No gold to grab here!'
        }

    def shoot_arrow(self) -> Dict:
        """Shoot arrow in current direction"""
        if not self.has_arrow:
            return {
                'status': 'error',
                'message': 'You have no arrows left!'
            }
            
        self.has_arrow = False
        self.score -= 10
        
        # Check if arrow hits wumpus
        if self._is_in_line(self.agent_pos, self.agent_direction, self.wumpus_pos):
            return {
                'status': 'success',
                'message': 'You killed the Wumpus!',
                'score': self.score
            }
            
        return {
            'status': 'success',
            'message': 'You missed the Wumpus!',
            'score': self.score
        }

    def _is_adjacent(self, pos1: List[int], pos2: List[int]) -> bool:
        """Check if two positions are adjacent"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) == 1

    def _is_in_line(self, start: List[int], direction: str, target: List[int]) -> bool:
        """Check if target is in line with start position in given direction"""
        if direction == 'up':
            return start[1] == target[1] and start[0] < target[0]
        elif direction == 'down':
            return start[1] == target[1] and start[0] > target[0]
        elif direction == 'left':
            return start[0] == target[0] and start[1] > target[1]
        elif direction == 'right':
            return start[0] == target[0] and start[1] < target[1]
        return False

class WumpusSolverAgent:
    def __init__(self, world: WumpusWorld):
        self.world = world
        self.path = []
        self.current_step = 0
        
    def solve(self) -> List[str]:
        """Return list of actions to solve the world"""
        actions = []
        while not self.world.game_over:
            # Get current percepts
            percepts = self.world.get_percepts()
            
            # If we see gold, grab it
            if 'Glitter' in percepts and not self.world.has_gold:
                actions.append('Grab')
                self.world.grab_gold()
                continue
                
            # If we have gold and are at start, climb out
            if self.world.has_gold and self.world.agent_pos == [0, 0]:
                actions.append('Climb')
                break
                
            # Find next safe move
            next_move = self._find_safe_move()
            if next_move:
                actions.append(f'Move {next_move}')
                self.world.move_agent(next_move)
            else:
                # If no safe moves, take a calculated risk
                risky_move = self._find_risky_move()
                if risky_move:
                    actions.append(f'Move {risky_move} (risky)')
                    self.world.move_agent(risky_move)
                else:
                    break
                    
        return actions

    def _find_safe_move(self) -> Optional[str]:
        """Find a safe move based on current knowledge"""
        x, y = self.world.agent_pos
        possible_moves = []
        
        # Check adjacent cells
        if x > 0 and self.world.knowledge['safe'][x-1][y]:
            possible_moves.append('up')
        if x < self.world.size-1 and self.world.knowledge['safe'][x+1][y]:
            possible_moves.append('down')
        if y > 0 and self.world.knowledge['safe'][x][y-1]:
            possible_moves.append('left')
        if y < self.world.size-1 and self.world.knowledge['safe'][x][y+1]:
            possible_moves.append('right')
            
        return random.choice(possible_moves) if possible_moves else None

    def _find_risky_move(self) -> Optional[str]:
        """Find a move with acceptable risk"""
        x, y = self.world.agent_pos
        possible_moves = []
        
        # Check adjacent cells that haven't been visited
        if x > 0 and not self.world.knowledge['visited'][x-1][y]:
            possible_moves.append('up')
        if x < self.world.size-1 and not self.world.knowledge['visited'][x+1][y]:
            possible_moves.append('down')
        if y > 0 and not self.world.knowledge['visited'][x][y-1]:
            possible_moves.append('left')
        if y < self.world.size-1 and not self.world.knowledge['visited'][x][y+1]:
            possible_moves.append('right')
            
        return random.choice(possible_moves) if possible_moves else None 