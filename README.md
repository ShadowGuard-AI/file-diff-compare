# File Diff Compare

## Overview

File Diff Compare is a command-line tool for comparing two files for differences, ignoring whitespace and comments. The tool is primarily focused on file operations and analysis.

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
* `-v`, `--verbose`: Enable verbose output
* `-q`, `--quiet`: Disable all output except errors

## Usage Examples

### Example 1: Compare two files

```
file-diff-compare file1.txt file2.txt
```

### Example 2: Compare two files and ignore whitespace

```
file-diff-compare -w file1.txt file2.txt
```

### Example 3: Compare two files and ignore comments

```
file-diff-compare -c file1.txt file2.txt
```

### Example 4: Compare two files and ignore both whitespace and comments

```
file-diff-compare -w -c file1.txt file2.txt
```

## Security Warnings

This tool should only be used to compare files from trusted sources. Comparing files from untrusted sources could lead to security vulnerabilities.

## License

This tool is licensed under the GNU General Public License v3.0.