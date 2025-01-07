#!/usr/bin/env python3
"""URL Encoder Utility.

This script provides URL encoding functionality using both standard encoding
(spaces as %20) and plus encoding (spaces as +). It can be used both as a
command line tool and imported as a module.
"""

from urllib.parse import quote, quote_plus
import argparse
import sys


def url_encode(text: str, use_plus: bool = False, safe: str = "") -> str:
    """URL encode the given text.

    Args:
        text: The string to encode.
        use_plus: If True, converts spaces to + instead of %20.
        safe: Characters to leave unchanged.

    Returns:
        str: The URL encoded string.
    """
    try:
        if use_plus:
            return quote_plus(text, safe=safe)
        return quote(text, safe=safe)
    except (TypeError, UnicodeEncodeError) as e:
        print(f"Error encoding text: {e}", file=sys.stderr)
        return ""


def main() -> None:
    """Run the URL encoder command line interface."""
    parser = argparse.ArgumentParser(
        description="URL encode text strings"
    )
    parser.add_argument(
        "text",
        nargs="?",
        help="Text to encode (if not provided, reads from stdin)"
    )
    parser.add_argument(
        "-p",
        "--plus",
        action="store_true",
        help="Use + for spaces instead of %%20"
    )
    parser.add_argument(
        "-s",
        "--safe",
        default="",
        help="Characters to leave unchanged"
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

    result = url_encode(text, args.plus, args.safe)
    print(result)


if __name__ == "__main__":
    main()
