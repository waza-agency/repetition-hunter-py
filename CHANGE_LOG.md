# Change Log

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
