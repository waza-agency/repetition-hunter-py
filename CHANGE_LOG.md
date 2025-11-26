# Change Log

## [2025-11-25] Technical debt cleanup and bug fixes | Status: ✅ Exitoso

### Changes Made:

1. **Added missing return type hints**
   - `print_results()` now has `-> None` return type
   - `main()` now has `-> None` return type

2. **Fixed bare exception handling**
   - Changed generic `except Exception` to specific exceptions
   - File parsing: `(SyntaxError, OSError, UnicodeDecodeError)`
   - AST normalization: `(ValueError, RecursionError)`

3. **Created missing LICENSE file**
   - Added MIT License file referenced in MANIFEST.in

4. **Fixed pyproject.toml version declaration**
   - Changed from `dynamic = ["version"]` to explicit `version = "1.0.3"`
   - Was declaring dynamic version but not implementing it

5. **Updated placeholder GitHub URLs**
   - Changed `yourusername` to `waza-agency` in pyproject.toml and setup.py
   - Now matches actual git remote

6. **Added edge case tests**
   - Empty file handling
   - Files with only comments
   - Unicode content handling
   - Deeply nested structures
   - Multiple files in same directory
   - Total: 27 tests (up from 22), all passing

### Files affected:
- `python_repetition_hunter/repetition_hunter.py` (modified)
- `pyproject.toml` (modified)
- `setup.py` (modified)
- `LICENSE` (created)
- `tests/test_repetition_hunter.py` (modified)

---

## [2025-11-25 19:25:00] Bug fixes and technical debt cleanup | Status: Exitoso

### Changes Made:

1. **Removed unused imports from `python_repetition_hunter/repetition_hunter.py`**
   - Removed: `hashlib`, `Counter`, `Path`, `Dict`, `Any`, `Optional`
   - Kept only: `ast`, `argparse`, `os`, `sys`, `defaultdict`, `dataclass`, `List`, `Set`, `Tuple`

2. **Deleted unnecessary root `__init__.py`**
   - This file was redundant (package is in `python_repetition_hunter/`)
   - Had outdated version (1.0.0) and placeholder author info

3. **Fixed author info in `pyproject.toml`**
   - Changed from placeholder "Your Name" to "Andres GU"
   - Changed email from "your.email@example.com" to "andres@waza.baby"

4. **Updated `README.md` default complexity**
   - Changed documented default from 3 to 4 (matching actual code)

5. **Added comprehensive unit tests**
   - Created `tests/` directory with 22 unit tests
   - Tests cover: ASTNormalizer, parsing, complexity calculation, normalization, repetition finding, sorting, file collection
   - All tests passing

6. **Created sample test file**
   - Added `test_sample.py` with intentional duplications for demonstration

### Files affected:
- `python_repetition_hunter/repetition_hunter.py` (modified)
- `__init__.py` (deleted - root level)
- `pyproject.toml` (modified)
- `README.md` (modified)
- `tests/__init__.py` (created)
- `tests/test_repetition_hunter.py` (created)
- `test_sample.py` (created)
