"""Unit tests for repetition_hunter module."""

import ast
import os
import tempfile
import unittest

from python_repetition_hunter.repetition_hunter import (
    ASTNormalizer,
    RepetitionResult,
    calculate_complexity,
    collect_python_files,
    extract_all_nodes,
    find_repetitions,
    get_builtin_names,
    normalize_ast,
    parse_python_file,
    sort_results,
)


class TestGetBuiltinNames(unittest.TestCase):
    def test_returns_set(self):
        result = get_builtin_names()
        self.assertIsInstance(result, set)

    def test_contains_common_builtins(self):
        result = get_builtin_names()
        self.assertIn("print", result)
        self.assertIn("len", result)
        self.assertIn("range", result)
        self.assertIn("True", result)
        self.assertIn("False", result)
        self.assertIn("None", result)


class TestASTNormalizer(unittest.TestCase):
    def test_normalizes_variable_names(self):
        code = "x = 1; y = x + 2"
        tree = ast.parse(code)
        builtin_names = get_builtin_names()
        normalizer = ASTNormalizer(builtin_names)
        normalized = normalizer.visit(tree)
        unparsed = ast.unparse(normalized)
        self.assertIn("x_0", unparsed)
        self.assertIn("x_1", unparsed)
        self.assertNotIn("y", unparsed)

    def test_preserves_builtins(self):
        code = "print(len(x))"
        tree = ast.parse(code)
        builtin_names = get_builtin_names()
        normalizer = ASTNormalizer(builtin_names)
        normalized = normalizer.visit(tree)
        unparsed = ast.unparse(normalized)
        self.assertIn("print", unparsed)
        self.assertIn("len", unparsed)

    def test_consistent_mapping(self):
        code = "a = 1; b = a + a"
        tree = ast.parse(code)
        builtin_names = get_builtin_names()
        normalizer = ASTNormalizer(builtin_names)
        normalized = normalizer.visit(tree)
        unparsed = ast.unparse(normalized)
        self.assertEqual(unparsed.count("x_0"), 3)


class TestParsePythonFile(unittest.TestCase):
    def test_parses_valid_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write("x = 1\n")
            f.flush()
            try:
                result = parse_python_file(f.name)
                self.assertIsInstance(result, ast.AST)
            finally:
                os.unlink(f.name)

    def test_raises_on_invalid_syntax(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write("def broken(\n")
            f.flush()
            try:
                with self.assertRaises(SyntaxError):
                    parse_python_file(f.name)
            finally:
                os.unlink(f.name)


class TestExtractAllNodes(unittest.TestCase):
    def test_extracts_nodes(self):
        code = "x = 1 + 2"
        tree = ast.parse(code)
        nodes = extract_all_nodes(tree)
        self.assertGreater(len(nodes), 0)

    def test_excludes_trivial_nodes(self):
        code = "x = 1"
        tree = ast.parse(code)
        nodes = extract_all_nodes(tree)
        node_types = [type(n).__name__ for n in nodes]
        self.assertNotIn("Name", node_types)
        self.assertNotIn("Constant", node_types)
        self.assertNotIn("Load", node_types)
        self.assertNotIn("Store", node_types)


class TestCalculateComplexity(unittest.TestCase):
    def test_simple_expression(self):
        code = "x = 1"
        tree = ast.parse(code)
        nodes = list(ast.walk(tree))
        assign_node = [n for n in nodes if isinstance(n, ast.Assign)][0]
        complexity = calculate_complexity(assign_node)
        self.assertGreater(complexity, 0)

    def test_complex_expression_higher(self):
        simple_code = "x = 1"
        complex_code = "x = 1 + 2 + 3 + 4 + 5"
        simple_tree = ast.parse(simple_code)
        complex_tree = ast.parse(complex_code)
        simple_assign = [
            n for n in ast.walk(simple_tree) if isinstance(n, ast.Assign)
        ][0]
        complex_assign = [
            n for n in ast.walk(complex_tree) if isinstance(n, ast.Assign)
        ][0]
        self.assertGreater(
            calculate_complexity(complex_assign),
            calculate_complexity(simple_assign),
        )


class TestNormalizeAst(unittest.TestCase):
    def test_normalizes_variables(self):
        code = "foo = bar + baz"
        tree = ast.parse(code)
        assign = [n for n in ast.walk(tree) if isinstance(n, ast.Assign)][0]
        builtin_names = get_builtin_names()
        normalized = normalize_ast(assign, builtin_names)
        self.assertIsInstance(normalized, ast.AST)


class TestFindRepetitions(unittest.TestCase):
    def test_finds_duplicates(self):
        code1 = """
def func1(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""
        code2 = """
def func2(items):
    output = []
    for element in items:
        output.append(element * 2)
    return output
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f1:
            f1.write(code1)
            f1.flush()
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".py", delete=False
            ) as f2:
                f2.write(code2)
                f2.flush()
                try:
                    results = find_repetitions(
                        [f1.name, f2.name], min_complexity=3, min_repetition=2
                    )
                    self.assertGreater(len(results), 0)
                finally:
                    os.unlink(f1.name)
                    os.unlink(f2.name)

    def test_respects_min_complexity(self):
        code = "x = 1\nx = 1"
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write(code)
            f.flush()
            try:
                results = find_repetitions(
                    [f.name], min_complexity=100, min_repetition=2
                )
                self.assertEqual(len(results), 0)
            finally:
                os.unlink(f.name)

    def test_respects_min_repetition(self):
        code = """
def a(): pass
def b(): pass
def c(): pass
"""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write(code)
            f.flush()
            try:
                results = find_repetitions(
                    [f.name], min_complexity=1, min_repetition=10
                )
                self.assertEqual(len(results), 0)
            finally:
                os.unlink(f.name)

    def test_handles_missing_file(self):
        results = find_repetitions(
            ["/nonexistent/file.py"], min_complexity=1, min_repetition=2
        )
        self.assertEqual(len(results), 0)


class TestSortResults(unittest.TestCase):
    def setUp(self):
        self.results = [
            RepetitionResult(
                complexity=5, repetition=2, original_nodes=[], generic_form="a"
            ),
            RepetitionResult(
                complexity=3, repetition=10, original_nodes=[], generic_form="b"
            ),
            RepetitionResult(
                complexity=10, repetition=3, original_nodes=[], generic_form="c"
            ),
        ]

    def test_sort_by_complexity(self):
        sorted_results = sort_results(self.results, "complexity")
        self.assertEqual(sorted_results[0].complexity, 10)

    def test_sort_by_repetition(self):
        sorted_results = sort_results(self.results, "repetition")
        self.assertEqual(sorted_results[0].repetition, 10)


class TestCollectPythonFiles(unittest.TestCase):
    def test_collects_single_file(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".py", delete=False
        ) as f:
            f.write("x = 1\n")
            f.flush()
            try:
                files = collect_python_files([f.name])
                self.assertEqual(len(files), 1)
                self.assertEqual(files[0], f.name)
            finally:
                os.unlink(f.name)

    def test_collects_from_directory(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            py_file = os.path.join(tmpdir, "test.py")
            txt_file = os.path.join(tmpdir, "test.txt")
            with open(py_file, "w") as f:
                f.write("x = 1\n")
            with open(txt_file, "w") as f:
                f.write("not python\n")
            files = collect_python_files([tmpdir])
            self.assertEqual(len(files), 1)
            self.assertTrue(files[0].endswith(".py"))

    def test_ignores_non_python_files(self):
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False
        ) as f:
            f.write("x = 1\n")
            f.flush()
            try:
                files = collect_python_files([f.name])
                self.assertEqual(len(files), 0)
            finally:
                os.unlink(f.name)


class TestRepetitionResult(unittest.TestCase):
    def test_dataclass_fields(self):
        result = RepetitionResult(
            complexity=5,
            repetition=3,
            original_nodes=[("file.py", 10, None)],
            generic_form="test",
        )
        self.assertEqual(result.complexity, 5)
        self.assertEqual(result.repetition, 3)
        self.assertEqual(len(result.original_nodes), 1)
        self.assertEqual(result.generic_form, "test")


if __name__ == "__main__":
    unittest.main()
