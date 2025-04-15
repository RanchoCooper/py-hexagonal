"""
Main entry point for Clean Architecture validator.
"""
import argparse
import logging
import sys
from typing import Dict

from util.clean_arch import Layer, Validator


def main():
    """
    Main function to run the Clean Architecture validator from the command line.
    """
    parser = argparse.ArgumentParser(description="Clean Architecture validator")
    parser.add_argument("--root", default=".", help="Root directory to validate")
    parser.add_argument("--ignore-tests", action="store_true", help="Ignore test files")
    parser.add_argument(
        "--ignored-packages", nargs="+", default=[], help="Packages to ignore"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Set the logging level",
    )
    args = parser.parse_args()

    # Configure logging
    logging.basicConfig(
        level=getattr(logging, args.log_level), format="%(levelname)s: %(message)s"
    )

    # Define alias mapping from directory patterns to layers
    alias: Dict[str, Layer] = {
        "domain": Layer.DOMAIN,
        "application": Layer.APPLICATION,
        "infrastructure": Layer.INFRASTRUCTURE,
        "interfaces": Layer.INTERFACES,
        # Add more aliases as needed
    }

    # Create validator and run validation
    validator = Validator(alias)
    count, passed, errors = validator.validate(
        args.root, args.ignore_tests, args.ignored_packages
    )

    # Report results
    print(f"\nProcessed {count} files.")
    if passed:
        print("Validation passed! No Clean Architecture violations found.")
        return 0
    else:
        print(f"Validation failed! Found {len(errors)} Clean Architecture violations.")
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
