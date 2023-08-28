class AppError(Exception):
    ERROR_MESSAGE = ""


class FileTypeError(AppError):
    ERROR_MESSAGE = "Invalid file type given. File must be an .srt file."


class FileReadError(AppError):
    ERROR_MESSAGE = "File could not be read."


class OffsetError(AppError):
    ERROR_MESSAGE = "Invalid offset value given. Initial timecode goes below 00:00:00,000."


class CommandLineArgumentsError(AppError):
    ERROR_MESSAGE = "Invalid arguments given."


class ArgumentAmountError(CommandLineArgumentsError):
    ERROR_MESSAGE = "Too many tag arguments listed. Use -h to see list of valid arguments."


class ArgumentValueError(CommandLineArgumentsError):
    ERROR_MESSAGE = "Non-accepted tag value given. Use -h to see list of valid arguments."
