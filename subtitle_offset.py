import re
from datetime import datetime, timedelta
from typing import List

from command_line_arguments import get_command_line_arguments
from exceptions import AppError, OffsetError, FileReadError, FileTypeError

START_TIMESTAMP = slice(0, 12)
END_TIMESTAMP = slice(17, 29)


def read_srt(file_name) -> List[str]:
    """
    Opens and reads input .srt files into a list of lines
    :param file_name: stores the name of the .srt file to be processed
    :return: list of string lines in input file
    """

    if not file_name.lower().endswith(".srt"):
        raise FileTypeError

    try:
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()
        return lines
    except Exception:
        raise FileReadError


def update_timestamp(line, offset, first) -> str:
    """
    Converts timestamps in srt file to datetime objects to perform
    +- offset operation. Formats the timestamps correctly as strings.
    Raises exception if the timestamp value goes below 0.
    :param line: string containing two timestamps
    :param offset: int containing value to modify timestamps by
    :param first: bool, true if first timestamp line in file
    :return: string containing updated timestamps
    """
    start_stripped = datetime.strptime(line[START_TIMESTAMP], "%H:%M:%S,%f")
    end_stripped = datetime.strptime(line[END_TIMESTAMP], "%H:%M:%S,%f")

    time_change = timedelta(milliseconds=offset)
    start_offset = start_stripped + time_change
    end_offset = end_stripped + time_change

    # checks if timestamp has gone below 0 (23:59:59,999 is previous day)
    if first and start_offset.date() != start_stripped.date():
        raise OffsetError

    # stringifies, removes date, 3-fig milliseconds
    formatted_start_offset = format(start_offset, "%H:%M:%S,%f")[:-3]
    formatted_end_offset = format(end_offset, "%H:%M:%S,%f")[:-3]

    updated_timestamp_line = f"{formatted_start_offset} --> {formatted_end_offset}\n"

    return updated_timestamp_line


def update_text(line, tags) -> str:
    """
    Checks if any optional keyword was listed in arguments
    and adds the relevant markdown tags to the subtitle text
    :param line: string containing current subtitle text
    :param tags: dict of optional keywords
    :return: string containing added tags (if applicable)
    """
    new_line = line
    if tags["bold"]:
        new_line = f"<b>{new_line[:-1]}</b>\n"
    if tags["italic"]:
        new_line = f"<i>{new_line[:-1]}</i>\n"
    if tags["underline"]:
        new_line = f"<u>{new_line[:-1]}</u>\n"
    if tags["colour_code"]:
        new_line = f"<font color=\"{tags['colour_code']}\">{new_line[:-1]}</font>\n"
    return new_line


def process_lines(lines, offset, tags) -> List[str]:
    """
    Performs the update to the timecodes and optionally the text
    in the .srt file content
    :param lines: list of lines in input file
    :param offset: time in milliseconds to offset the timestamps by (can be negative)
    :param tags: dict of optional keywords
    :return: list of lines with updated timestamps and optionally text
    """
    processed_lines = []
    first = True
    prev_line = ""
    for line in lines:
        # line is timecodes
        if re.search(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", line):
            processed_lines.append(update_timestamp(line, offset, first))
            first = False
        # line is subtitle text (not a newline, previous line isn't new line or empty and isn't numeric)
        elif not (((prev_line == "\n" or prev_line == "") and line[:-1].isnumeric()) or line == "\n"):
            processed_lines.append(update_text(line, tags))
        # line is block id or newline
        else:
            processed_lines.append(line)
        prev_line = line
    return processed_lines


def write_updated_srt(processed_lines, new_file_name) -> None:
    """
    Writes new lines list to new file with updated filename
    :param processed_lines: list of lines with updated timestamps
    :param new_file_name: file name of input file with "updated_subs" suffix
    """
    with open(new_file_name, "w") as new_file:
        for line in processed_lines:
            new_file.write(line)


if __name__ == '__main__':

    try:
        file_name, offset, tags = get_command_line_arguments()
        lines = read_srt(file_name)
        processed_lines = process_lines(lines, offset, tags)
        new_file_name = f"{file_name[:-4]}_updated_subs.srt"
        write_updated_srt(processed_lines, new_file_name)
        print(f"Successfully generated new subtitle file: {new_file_name}")
    except Exception as e:
        if isinstance(e, AppError):
            print(f"ERROR: {e.ERROR_MESSAGE}")
        else:
            print("ERROR: Unknown error occurred.")
