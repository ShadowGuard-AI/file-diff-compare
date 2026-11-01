import argparse
import logging
import re
import sys
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
        description="Compares two files for differences, with options to ignore whitespace and comments. Exit codes: 0 when the files are identical, 1 when they differ, 2 when a file cannot be read."
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
        help="Ignore comments during comparison: full line and trailing comments in the # and // styles.",
    )
    parser.add_argument(
        "--ignore-whitespace",
        action="store_true",
        help="Ignore leading and trailing whitespace on each line during comparison.",
    )
    return parser


def read_file(file_path, ignore_comments=False, ignore_whitespace=False):
    try:
        # Files are read as strict utf-8. A binary file or one in another
        # encoding raises here and lands in main's error exit, code 2, which
        # means cannot compare, not different. The three exit codes are the
        # contract scripts around this tool rely on.
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        processed_lines = []
        for line in lines:
            # Only the line ending characters come off here. A CRLF file and an LF
            # file therefore compare equal line by line, while trailing spaces stay
            # significant unless --ignore-whitespace was given.
            line = line.rstrip("\r\n")
            if ignore_comments:
                stripped = line.lstrip()
                if stripped.startswith("#") or stripped.startswith("//"):
                    continue
                # A trailing comment has to be preceded by whitespace. That requirement
                # is what keeps a URL or a string containing // or # intact in the
                # common cases, but it is still blind to strings: quoted text with a
                # space before // is cut there anyway. Full line comments were handled
                # just above, so this branch only ever shortens a code line.
                match = re.search(r"\s+(#|//)", line)
                if match:
                    line = line[:match.start()].rstrip()
            # Comment handling runs before the whitespace strip, in that order, so
            # the comment search sees the original spacing it depends on. The
            # whitespace option then strips only the ends of what remains; spacing
            # inside a line always counts.
            if ignore_whitespace:
                line = line.strip()
            processed_lines.append(line)

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
        # Equality is decided on the whole processed lists at once. This diff
        # is only a report built afterwards: positional pairs first, then the
        # tail of whichever file ran longer, labelled as extra lines.
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
            sys.exit(0)
        else:
            logging.info("Files are different.")
            sys.exit(1)
    except Exception as e:
        logging.error(f"An error occurred during file comparison: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()