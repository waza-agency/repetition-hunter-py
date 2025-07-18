# 🔍 Python Repetition Hunter

> *Hunt down code repetitions like a pro detective*

A powerful Python tool that analyzes your codebase to find repeated patterns and duplicated logic. Based on the Clojure repetition-hunter algorithm, this tool helps you identify opportunities for refactoring and code deduplication.

## ✨ Features

- 🎯 **Smart Pattern Detection** - Finds semantic duplications, not just copy-paste
- 🧠 **AST-Based Analysis** - Uses Abstract Syntax Trees for deep code understanding  
- 🔧 **Variable Normalization** - Detects patterns even when variable names differ
- 📊 **Complexity Scoring** - Ranks findings by complexity × repetition count
- 🎛️ **Configurable Thresholds** - Tune sensitivity to your needs
- 📁 **Recursive Directory Scanning** - Analyze entire projects at once

## 🚀 Quick Start

```bash
# Analyze a single file
python repetition_hunter.py my_code.py

# Scan entire project
python repetition_hunter.py src/

# Find only high-complexity duplications
python repetition_hunter.py --min-complexity 5 --min-repetition 3 src/
```

## 📋 Usage

```
python repetition_hunter.py [OPTIONS] PATHS...

Arguments:
  PATHS                    Python files or directories to analyze

Options:
  --min-complexity INT     Minimum complexity threshold (default: 3)
  --min-repetition INT     Minimum repetition count (default: 2)  
  --sort [complexity|repetition]  Sort results by complexity or repetition (default: complexity)
```

## 🎯 Example Output

```
3 repetitions of complexity 12

Line 15 - src/utils.py:
if data is None:
    return None
result = []
for item in data:
    if item > 0:
        result.append(item * 2)
return result

Line 28 - src/processor.py:
if items is None:
    return None
output = []
for element in items:
    if element > 0:
        output.append(element * 2)
return output

======================================================================
```

## 🧪 Test It Out

The project includes `test_sample.py` with intentional duplications to demonstrate the tool:

```bash
python repetition_hunter.py test_sample.py
```

You'll see it catches patterns like:
- Similar data processing loops with different variable names
- Duplicate validation logic
- Repeated calculation patterns

## 🔧 How It Works

1. **Parse** - Converts Python code to Abstract Syntax Trees
2. **Extract** - Identifies all meaningful code nodes (skipping trivial ones)
3. **Normalize** - Replaces variable names with generic placeholders
4. **Group** - Clusters identical normalized patterns
5. **Score** - Ranks by complexity × repetition count
6. **Report** - Shows original code locations for each pattern

## 🎨 Why Use This?

- **Reduce Technical Debt** - Spot duplicated logic before it spreads
- **Improve Code Quality** - Identify refactoring opportunities
- **Save Time** - Automated detection vs manual code review
- **Learn Patterns** - Understand your codebase's repetition hotspots

## 🛠️ Requirements

- Python 3.6+
- No external dependencies (uses only standard library)

## 🤝 Contributing

Found a bug or have an idea? Feel free to open an issue or submit a PR!

## 📄 License

This project, made by WAZA.baby, is open source. Use it, modify it, share it!

---

*Happy hunting! 🎯*