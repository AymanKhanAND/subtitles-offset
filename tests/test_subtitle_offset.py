import os
import pytest
from pathlib import Path

from exceptions import OffsetError, FileTypeError
from subtitle_offset import read_srt, write_updated_srt, update_timestamp, update_text


class TestSubtitleOffset:
    def test_file_read(self):
        # Arrange
        expected_lines = [
            "1\n",
            "00:00:00,498 --> 00:00:02,827\n",
            "- Here's what I love most\n",
            "about food and diet.\n",
            "\n",
            "2\n",
            "00:00:02,827 --> 00:00:06,383\n",
            "We all eat several times a day,\n",
            "and we're totally in charge\n",
            "\n",
            "3\n",
            "00:00:06,383 --> 00:00:09,427\n",
            "of what goes on our plate\n",
            "and what stays off.\n"
        ]

        # Act
        lines = read_srt("data/test.srt")

        # Assert
        assert lines == expected_lines

    def test_new_file_created(self):

        # Arrange
        test_lines = ["test\n"]
        test_file_name = "test_file_name"

        # Act
        write_updated_srt(test_lines, test_file_name)
        created_file = Path(test_file_name)

        # Assert
        assert created_file.is_file()
        os.remove(test_file_name)

    def test_invalid_file_type_raises_exception(self):

        # Arrange
        txt_file = "test_file.txt"

        # Act, Assert
        with pytest.raises(FileTypeError):
            read_srt(txt_file)

    @pytest.mark.parametrize(
        "offset, expected_line",
        [
            (
                500,
                "00:00:00,998 --> 00:00:03,327\n"
             ),
            (
                -200,
                "00:00:00,298 --> 00:00:02,627\n"
            ),
            (
                0,
                "00:00:00,498 --> 00:00:02,827\n"
            )
        ],
    )
    def test_offset_modifies_timestamp(self, offset, expected_line):
        # Arrange
        input_timestamp_line = "00:00:00,498 --> 00:00:02,827\n"

        # Act
        timestamp_line = update_timestamp(input_timestamp_line, offset, False)

        # Assert
        assert timestamp_line == expected_line

    def test_invalid_offset_exception_raised_when_timecode_less_than_0(self):
        # Arrange
        input_timestamp_line = "00:00:00,498 --> 00:00:02,827\n"
        offset = -500

        # Act, Assert
        with pytest.raises(OffsetError):
            update_timestamp(input_timestamp_line, offset, True)

    @pytest.mark.parametrize(
        "tags, expected_line",
        [
            (
                    {
                        "bold": True,
                        "italic": False,
                        "underline": False,
                        "colour_code": ""
                     },
                    "<b>00:00:00,498 --> 00:00:02,827</b>\n"
            ),
            (
                    {
                        "bold": False,
                        "italic": True,
                        "underline": False,
                        "colour_code": ""
                    },
                    "<i>00:00:00,498 --> 00:00:02,827</i>\n"
            ),
            (
                    {
                        "bold": False,
                        "italic": False,
                        "underline": True,
                        "colour_code": ""
                    },
                    "<u>00:00:00,498 --> 00:00:02,827</u>\n"
            ),
            (
                    {
                        "bold": False,
                        "italic": False,
                        "underline": False,
                        "colour_code": "#FFFFFF"
                    },
                    '<font color="#FFFFFF">00:00:00,498 --> 00:00:02,827</font>\n'
            ),
        ],
    )
    def test_text_updated_with_markdown(self, tags, expected_line):
        # Arrange
        input_timestamp_line = "00:00:00,498 --> 00:00:02,827\n"

        # Act
        timestamp_line = update_text(input_timestamp_line, tags)

        # Assert
        assert timestamp_line == expected_line
