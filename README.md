![Banner](banner.png)

# File Diff Compare

## Overview

File Diff Compare is a command-line tool for comparing two files for differences, with options to ignore whitespace and comments. The tool is primarily focused on file operations and analysis.

## Installation

1. Clone the repository:
```
git clone https://github.com/ShadowStrikeHQ/file-diff-compare.git
```
2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

```
file-diff-compare [options] file1 file2
```

## Options

* `-h`, `--help`: Show this help message and exit
* `--ignore-comments`: Ignore comments when comparing: full line comments and trailing comments, in both the `#` and `//` styles
* `--ignore-whitespace`: Ignore leading and trailing whitespace on each line when comparing. Without this flag, lines are compared as they are, apart from the line ending itself.

## Exit codes

* `0`: the files are identical
* `1`: the files differ
* `2`: a file could not be read; the reason is logged

## Usage Examples

### Example 1: Compare two files

```
file-diff-compare file1.txt file2.txt
```

### Example 2: Compare two files and ignore whitespace

```
file-diff-compare --ignore-whitespace file1.txt file2.txt
```

### Example 3: Compare two files and ignore comments

```
file-diff-compare --ignore-comments file1.txt file2.txt
```

### Example 4: Compare two files and ignore both whitespace and comments

```
file-diff-compare --ignore-whitespace --ignore-comments file1.txt file2.txt
```

## Security Warnings

This tool should only be used to compare files from trusted sources. Comparing files from untrusted sources could lead to security vulnerabilities.

## License

This tool is licensed under the GNU General Public License v3.0.