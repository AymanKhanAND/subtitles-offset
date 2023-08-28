import re
from argparse import ArgumentParser
from typing import Any, Tuple, Dict

from exceptions import ArgumentAmountError, ArgumentValueError


def arg_validation(args, tags) -> Dict[str, Any]:
    if len(args.Tags) > len(tags):
        raise ArgumentAmountError
    for tag in args.Tags:
        if tag.lower() == "bold":
            tags["bold"] = True
        elif tag.lower() == "italic":
            tags["italic"] = True
        elif tag.lower() == "underline":
            tags["underline"] = True
        elif re.search(r"#(?:[\da-fA-F]{3}){1,2}", tag):
            tags["colour_code"] = tag
        else:
            raise ArgumentValueError

    return tags


def get_command_line_arguments() -> Tuple[str, int, dict[Any]]:
    """
    Adds values to retrieve from command line.
    filename, offset (in milliseconds), optional list of
    tags: bold, italic, underline, colour code.
    Raises exception if invalid arguments are provided.
    :return: file name, offset, optional tags from command line
    """

    tags = {
        "bold": False,
        "italic": False,
        "underline": False,
        "colour_code": ""
    }

    parser = ArgumentParser(
        prog="subtitle_offset",
        description="Generates new .srt file with updated timecodes.")
    parser.add_argument(
        "File",
        metavar="file",
        type=str,
        help="the name of the .srt file to modify"
    )
    parser.add_argument(
        "Offset",
        metavar="offset",
        type=int,
        help="the amount in milliseconds to offset the subtitle timecodes by"
    )
    parser.add_argument(
        "Tags",
        metavar="tags",
        type=str,
        nargs="*",
        help="optionally add \"bold\", \"italic\", \"underline\" and/or \"#XXXXXX\" colour-code "
             "to subtitle text (must include speech marks)")

    args = parser.parse_args()
    print(type(args))
    print(args)
    tags = arg_validation(args, tags)

    return args.File, args.Offset, tags
