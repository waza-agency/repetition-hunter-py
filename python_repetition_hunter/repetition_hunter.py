#!/usr/bin/env python3
"""
Python Repetition Hunter

Finds repetitions in Python code, ordered by complexity * repetition count.
Based on the Clojure repetition-hunter algorithm.
"""

import ast
import argparse
import copy
import os
import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Set, Tuple


@dataclass
class RepetitionResult:
    """Result of a repetition analysis"""
    complexity: int
    repetition: int
    original_nodes: List[Tuple[str, int, ast.AST]]  # (filename, line, node)
    generic_form: str


class ASTNormalizer(ast.NodeTransformer):
    """Normalizes AST nodes by replacing variables with generic placeholders"""
    
    def __init__(self, builtin_names: Set[str]):
        self.builtin_names = builtin_names
        self.var_counter = 0
        self.var_map = {}
        
    def visit_Name(self, node: ast.Name) -> ast.Name:
        if node.id in self.builtin_names:
            return node
            
        if node.id not in self.var_map:
            self.var_map[node.id] = f"x_{self.var_counter}"
            self.var_counter += 1
            
        return ast.Name(id=self.var_map[node.id], ctx=node.ctx)


def get_builtin_names() -> Set[str]:
    """Get set of Python builtin names"""
    import builtins
    return set(dir(builtins))


def parse_python_file(filepath: str) -> ast.AST:
    """Parse a Python file and return its AST"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    return ast.parse(content, filename=filepath)


def extract_all_nodes(node: ast.AST) -> List[ast.AST]:
    """Extract all AST nodes from a tree, excluding trivial ones"""
    nodes = []
    
    def collect_nodes(n):
        if isinstance(n, ast.AST):
            # Skip trivial nodes (single names, constants)
            if not isinstance(n, (ast.Name, ast.Constant, ast.Load, ast.Store, ast.Del)):
                nodes.append(n)
            
            for child in ast.iter_child_nodes(n):
                collect_nodes(child)
    
    collect_nodes(node)
    return nodes


def calculate_complexity(node: ast.AST) -> int:
    """Calculate complexity of an AST node (number of child nodes)"""
    count = 0
    for _ in ast.walk(node):
        count += 1
    return count


def normalize_ast(node: ast.AST, builtin_names: Set[str]) -> ast.AST:
    """Create a generic version of an AST node by replacing variables"""
    normalizer = ASTNormalizer(builtin_names)
    return normalizer.visit(node)


def ast_to_string(node: ast.AST) -> str:
    """Convert AST node to a string representation"""
    return ast.dump(node, indent=None)


def find_repetitions(files: List[str], min_complexity: int = 3, min_repetition: int = 2) -> List[RepetitionResult]:
    """Find repetitions across multiple Python files"""
    builtin_names = get_builtin_names()
    
    # Collect all nodes from all files
    all_nodes = []
    
    for filepath in files:
        if not os.path.exists(filepath):
            print(f"Warning: File {filepath} not found", file=sys.stderr)
            continue
            
        try:
            tree = parse_python_file(filepath)
            nodes = extract_all_nodes(tree)
            
            for node in nodes:
                complexity = calculate_complexity(node)
                if complexity >= min_complexity:
                    all_nodes.append((filepath, node.lineno if hasattr(node, 'lineno') else 0, node))
                    
        except (SyntaxError, OSError, UnicodeDecodeError) as e:
            print(f"Error parsing {filepath}: {e}", file=sys.stderr)
            continue
    
    # Group by normalized form
    generic_groups = defaultdict(list)
    
    for filepath, lineno, node in all_nodes:
        try:
            # Deep copy to preserve original variable names for display
            node_copy = copy.deepcopy(node)
            generic_node = normalize_ast(node_copy, builtin_names)
            generic_form = ast_to_string(generic_node)
            complexity = calculate_complexity(node)
            
            generic_groups[generic_form].append((filepath, lineno, node, complexity))
        except (ValueError, RecursionError) as e:
            print(f"Error normalizing node at {filepath}:{lineno}: {e}", file=sys.stderr)
            continue
    
    # Create results for repeated forms
    results = []
    for generic_form, instances in generic_groups.items():
        if len(instances) >= min_repetition:
            complexity = instances[0][3]  # All instances should have same complexity
            original_nodes = [(fp, ln, node) for fp, ln, node, _ in instances]
            
            results.append(RepetitionResult(
                complexity=complexity,
                repetition=len(instances),
                original_nodes=original_nodes,
                generic_form=generic_form
            ))
    
    return results


def sort_results(results: List[RepetitionResult], sort_by: str = "complexity") -> List[RepetitionResult]:
    """Sort results by complexity * repetition or repetition * complexity"""
    if sort_by == "repetition":
        return sorted(results, key=lambda r: (r.repetition, r.complexity), reverse=True)
    else:
        return sorted(results, key=lambda r: (r.complexity, r.repetition), reverse=True)


def shorten_path(filepath: str) -> str:
    """Shorten file path for display by removing ./ prefix and common directories"""
    if filepath.startswith('./'):
        filepath = filepath[2:]
    if filepath.startswith('src/'):
        filepath = filepath[4:]
    return filepath


def print_results(results: List[RepetitionResult]) -> None:
    """Print formatted results in compact format"""
    for result in results:
        # Build compact location list
        locations = [
            f"{shorten_path(fp)}:{ln}"
            for fp, ln, _ in result.original_nodes
        ]

        # Compact header: [complexity] Nx: file:line, file:line, ...
        print(f"[{result.complexity}] {result.repetition}x: {', '.join(locations)}")

        # Show code only once (from first instance)
        _, _, first_node = result.original_nodes[0]
        try:
            print(ast.unparse(first_node))
        except AttributeError:
            # Fallback for Python < 3.9
            print(ast.dump(first_node, indent=2))

        print()
        print("=" * 70)
        print()


def collect_python_files(paths: List[str]) -> List[str]:
    """Collect all Python files from given paths"""
    files = []
    
    for path in paths:
        if os.path.isfile(path) and path.endswith('.py'):
            files.append(path)
        elif os.path.isdir(path):
            for root, dirs, filenames in os.walk(path):
                for filename in filenames:
                    if filename.endswith('.py'):
                        files.append(os.path.join(root, filename))
    
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description='Find repetitions in Python code')
    parser.add_argument('paths', nargs='+', help='Python files or directories to analyze')
    parser.add_argument('--min-complexity', type=int, default=4, 
                       help='Minimum complexity threshold (default: 4)')
    parser.add_argument('--min-repetition', type=int, default=2, 
                       help='Minimum repetition threshold (default: 2)')
    parser.add_argument('--sort', choices=['complexity', 'repetition'], default='complexity',
                       help='Sort by complexity or repetition (default: complexity)')
    
    args = parser.parse_args()
    
    # Collect all Python files
    files = collect_python_files(args.paths)
    
    if not files:
        print("No Python files found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Analyzing {len(files)} Python files...")
    
    # Find repetitions
    results = find_repetitions(files, args.min_complexity, args.min_repetition)
    
    if not results:
        print("No repetitions found")
        return
    
    # Sort and print results
    sorted_results = sort_results(results, args.sort)
    print_results(sorted_results)
    
    print(f"Found {len(results)} repeated patterns")


if __name__ == "__main__":
    main()