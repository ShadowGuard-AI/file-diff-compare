import argparse
import logging
from pathlib import Path


def setup_logging():
    """Configure logging settings."""
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )


def setup_argparse():
    """
    Set up argparse for command-line argument parsing.

    Returns:
        argparse.ArgumentParser: Configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Compares two files for differences, ignoring whitespace and comments."
    )
    parser.add_argument(
        "file1",
        type=str,
        help="Path to the first file to compare.",
    )
    parser.add_argument(
        "file2",
        type=str,
        help="Path to the second file to compare.",
    )
    parser.add_argument(
        "--ignore-comments",
        action="store_true",
        help="Ignore comments during comparison.",
    )
    parser.add_argument(
        "--ignore-whitespace",
        action="store_true",
        help="Ignore differences in whitespace.",
    )
    return parser


def read_file(file_path, ignore_comments=False, ignore_whitespace=False):
    """
    Reads a file with options to ignore comments and/or whitespace.

    Args:
        file_path (str): Path to the file to read.
        ignore_comments (bool): If True, ignore lines starting with '#'.
        ignore_whitespace (bool): If True, strip all whitespace from lines.

    Returns:
        list: List of processed lines from the file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        processed_lines = []
        for line in lines:
            if ignore_comments and line.strip().startswith("#"):
                continue
            if ignore_whitespace:
                line = "".join(line.split())
            processed_lines.append(line.strip())

        return processed_lines
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
        raise


def compare_files(file1, file2, ignore_comments=False, ignore_whitespace=False):
    """
    Compares two files line by line.

    Args:
        file1 (str): Path to the first file.
        file2 (str): Path to the second file.
        ignore_comments (bool): If True, ignore comments during comparison.
        ignore_whitespace (bool): If True, ignore differences in whitespace.

    Returns:
        bool: True if files are identical based on the comparison criteria, False otherwise.
    """
    lines1 = read_file(file1, ignore_comments, ignore_whitespace)
    lines2 = read_file(file2, ignore_comments, ignore_whitespace)

    if lines1 == lines2:
        return True
    else:
        diff = [f"Line {i + 1}: {line1} != {line2}" for i, (line1, line2) in enumerate(zip(lines1, lines2)) if line1 != line2]
        diff.extend([f"Extra line in file1: {line}" for line in lines1[len(lines2):]])
        diff.extend([f"Extra line in file2: {line}" for line in lines2[len(lines1):]])

        logging.info("Differences found between files:")
        for d in diff:
            logging.info(d)

        return False


def main():
    """
    Main entry point for the file comparison tool.

    Parses command-line arguments, performs the comparison, and logs the result.
    """
    setup_logging()
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        are_files_identical = compare_files(
            args.file1,
            args.file2,
            ignore_comments=args.ignore_comments,
            ignore_whitespace=args.ignore_whitespace,
        )

        if are_files_identical:
            logging.info("Files are identical.")
        else:
            logging.info("Files are different.")
    except Exception as e:
        logging.error(f"An error occurred during file comparison: {e}")


if __name__ == "__main__":
    main()