from datetime import datetime
import re


def validate_form(lines):
    captions = []
    caption = {}

    for line in lines:
        if not caption:
            if line.isnumeric:
                caption["id"] = line
            else:
                print("should be id here")
        elif caption.get("id"):
            if caption.get("timecodes"):
                if caption.get("caption_text"):
                    if line == "\n":
                        caption["newline"] = line
                        captions.append(caption)
                        caption = {}
                    else:
                        caption["caption_text"].append(line)
                elif line != "\n":
                    caption["caption_text"] = [line]
                else:
                    print("should be caption text here")
            elif re.search(r"(\d+:\d+:\d+,\d+) --> (\d+:\d+:\d+,\d+)", line):
                caption["timecodes"] = line
            else:
                print("should be timecode here")

    if caption:
        print("missing elements")

    return captions


def validate_ids(ids):
    if ids[0] != "1":
        print("invalid starting ID")
        return

    for i, val in enumerate(ids):
        if i+1 != int(val):
            print("invalid ID")
            return


def validate_timecodes(timecodes):
    previous_code = datetime.strptime("00:00:00,000", "%H:%M:%S,%f")

    for codes in timecodes:
        start_code = datetime.strptime(codes[:12], "%H:%M:%S,%f")
        end_code = datetime.strptime(codes[-12:], "%H:%M:%S,%f")

        if start_code < previous_code:
            print("invalid timecodes - time codes must increase")

        if start_code > end_code:
            print("invalid timecodes - start time code must be smaller than end")

        previous_code = end_code


def validate_caption_text(caption_text):
    for caption_group in caption_text:
        for caption in caption_group:
            for word in caption.split("<b>"):
                print(word)


def validate_grammar(captions):
    ids = [x["id"] for x in captions]
    timecodes = [x["timecodes"] for x in captions]
    caption_text = [x["caption_text"] for x in captions]

    validate_ids(ids)
    validate_timecodes(timecodes)
    validate_caption_text(caption_text)


if __name__ == '__main__':
    lines = [
        "1", "00:00:00,498 --> 00:00:02,827", "- <b>Here's</b> what I love most", "\n",
        "2", "00:00:02,827 --> 00:00:06,383", "We all eat several times a day,", "and we're totally in charge", "\n",
        "3", "00:00:06,383 --> 00:00:09,427", "of what goes on our plate", "\n"
    ]
    validate_grammar(validate_form(lines))
