from typing import Dict, List, Optional
import itertools

class CryptarithmeticSolver:
    def __init__(self, equation: str):
        self.equation = equation.replace(' ', '')
        self.words = self.equation.replace('+', ' ').replace('=', ' ').split()
        self.result = self.words[-1]
        self.addends = self.words[:-1]
        self.letters = sorted(list(set(''.join(self.words))))
        self.first_letters = set(word[0] for word in self.words)
        
    def solve(self) -> Dict[str, int]:
        """Solve the cryptarithmetic puzzle and return the solution"""
        # Generate all possible digit assignments
        for digits in itertools.permutations(range(10), len(self.letters)):
            # Create mapping of letters to digits
            mapping = dict(zip(self.letters, digits))
            
            # Skip if any first letter is mapped to 0
            if any(mapping[letter] == 0 for letter in self.first_letters):
                continue
                
            # Convert words to numbers
            addend_values = [self._word_to_number(word, mapping) for word in self.addends]
            result_value = self._word_to_number(self.result, mapping)
            
            # Check if the equation holds
            if sum(addend_values) == result_value:
                return mapping
                
        return {}  # No solution found
        
    def _word_to_number(self, word: str, mapping: Dict[str, int]) -> int:
        """Convert a word to a number using the given mapping"""
        return int(''.join(str(mapping[letter]) for letter in word))
        
    def format_solution(self, solution: Dict[str, int]) -> str:
        """Format the solution in a readable way"""
        if not solution:
            return "No solution found"
            
        # Create the equation with numbers
        formatted_addends = [self._word_to_number(word, solution) for word in self.addends]
        formatted_result = self._word_to_number(self.result, solution)
        
        # Create the mapping display
        mapping_display = '\n'.join(f"{letter} = {digit}" for letter, digit in solution.items())
        
        return f"""
Solution:
{' + '.join(str(n) for n in formatted_addends)} = {formatted_result}

Letter assignments:
{mapping_display}
""" 