#!/usr/bin/env python3
"""URL Decoder Utility.

This script provides URL decoding functionality for both standard encoding
(spaces as %20) and plus encoding (spaces as +). It can be used both as a
command line tool and imported as a module.
"""

from urllib.parse import unquote, unquote_plus
import argparse
import sys


def url_decode(text: str, use_plus: bool = False) -> str:
    """URL decode the given text.

    Args:
        text: The string to decode.
        use_plus: If True, converts + to spaces instead of %20.

    Returns:
        str: The URL decoded string.
    """
    try:
        if use_plus:
            return unquote_plus(text)
        return unquote(text)
    except (TypeError, UnicodeDecodeError) as e:
        print(f"Error decoding text: {e}", file=sys.stderr)
        return ""


def main() -> None:
    """Run the URL decoder command line interface."""
    parser = argparse.ArgumentParser(
        description="URL decode text strings"
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to decode (if not provided, reads from stdin)"
    )
    parser.add_argument(
        "-p",
        "--plus",
        action="store_true",
        help="Convert + to spaces instead of %%20"
    )

    args = parser.parse_args()

    # Read from stdin if no text argument provided
    if args.text is None:
        text = sys.stdin.read().strip()
    else:
        text = args.text

    if not text:
        print("Error: No text provided", file=sys.stderr)
        sys.exit(1)

    result = url_decode(text, args.plus)
    print(result)


if __name__ == "__main__":
    main()
