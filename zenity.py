"""
Author  :   Avraham Mayer
Date    :   19/06/2020

This is a python wrapper for the linux zenity GUI tool.
It runs zenity as a separate process using the subprocess module

I haven't yet implemented the forms option but I'll probably get to it sometime

Forms dialog options
  --forms                                           Display forms dialog
  --add-entry=Field name                            Add a new Entry in forms dialog
  --add-password=Field name                         Add a new Password Entry in forms dialog
  --add-calendar=Calendar field name                Add a new Calendar in forms dialog
  --add-list=List field and header name             Add a new List in forms dialog
  --list-values=List of values separated by |       List of values for List
  --column-values=List of values separated by |     List of values for columns
  --add-combo=Combo box field name                  Add a new combo box in forms dialog
  --combo-values=List of values separated by |      List of values for combo box
  --show-header                                     Show the columns header
  --text=TEXT                                       Set the dialog text
  --separator=SEPARATOR                             Set output separator character
  --forms-date-format=PATTERN                       Set the format for the returned date
"""

import datetime
import shlex
import subprocess
from typing import Union


def run_local_command(command, wait=True):
    """
    This function runs a command using subprocess
    :param command: The command to run - either a list of arguments or a string
    :param wait: whether to wait for the command to complete or return immediately
    :return: The subprocess object
    """
    if isinstance(command, str):
        command = shlex.split(command)
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    if wait:
        process.wait()
    return process


class ZenityError(Exception):
    pass


class BaseZenityDialogue:
    """
    A class representing a base zenity dialogue with the attributes common to all zenity dialogues - height, width
    Should not be instantiated as it does not have a dialogue type
    """
    def __init__(self, window_icon=None, ok_label=None, cancel_label=None, width=None, height=None):
        self.arguments = ['zenity']
        self.zenity_process: Union[subprocess.Popen, None] = None
        if ok_label is not None:
            self.arguments.append(f'--ok-label={ok_label}')
        if cancel_label is not None:
            self.arguments.append(f'--cancel-label={cancel_label}')
        if window_icon is not None:
            self.arguments.append(f'--window-icon={window_icon}')
        if width is not None:
            self.arguments.append(f'--width={width}')
        if height is not None:
            self.arguments.append(f'--height={height}')
        self.output = ''

    def run(self):
        """
        This function will run the zenity command and wait for it to complete
        """
        self.start()
        self.wait()

    def wait(self):
        """
        This function will wait for the running zenity command to complete
        :return: the exit code of the zenity command
        """
        self.output += self.zenity_process.stdout.read().decode()
        exit_code = self.zenity_process.wait()
        if exit_code not in (0, 1):
            raise ZenityError(
                f'zenity process failed. stdout: {self.output}, stderr: {self.zenity_process.stderr.read().decode()}')
        return exit_code

    def send_input(self, input_to_send):
        """
        This function will write input to the standard input of the zenity process
        :param input_to_send: the input to send to the program
        """
        if isinstance(input_to_send, str):
            input_to_send = input_to_send.encode('utf-8')
        self.zenity_process.stdin.write(input_to_send)
        self.zenity_process.stdin.flush()

    def start(self):
        """
        This function will start the zenity process and immediately return without waiting for it
        in order to allow running zenity command asynchronously - for example progress bars
        """
        self.zenity_process = run_local_command(self.arguments, wait=False)

    def stop(self):
        """
        Stop the zenity process
        :return: the return code of the process
        """
        self.zenity_process.terminate()
        return self.zenity_process.wait()

    def get_output(self):
        """
        Read the standard output of the zenity process
        :return: the resulting string
        """
        if self.zenity_process.poll() is not None:
            self.wait()
        return self.output


class DateSelection(BaseZenityDialogue):
    """
    A class representing the zenity date selection option
    """
    def __init__(self, text=None, title=None, starting_date: datetime.date = None, window_icon=None, ok_label=None,
                 cancel_label=None, width=None, height=None):
        super().__init__(window_icon, ok_label, cancel_label, width, height)
        self.arguments.extend(['--calendar', '--date-format=%d/%m/%Y'])
        if text is not None:
            self.arguments.append(f'--text={text}')
        if title is not None:
            self.arguments.append(f'--title={title}')
        if starting_date is not None:
            self.arguments.append(f'--day={starting_date.day}')
            self.arguments.append(f'--month={starting_date.month}')
            self.arguments.append(f'--year={starting_date.year}')


class FileSelection(BaseZenityDialogue):
    def __init__(self, multiple=False, separator='|', directory=False, new=False, window_icon=None, width=None,
                 height=None):
        super().__init__(window_icon, None, None, width, height)
        self.arguments.append('--file-selection')
        if multiple:
            self.arguments.append('--multiple')
        self.arguments.append(f'--separator={separator}')
        if directory:
            self.arguments.append('--directory')
        if new:
            self.arguments.append('--save')


class Notification(BaseZenityDialogue):
    def __init__(self, text=None, window_icon=None, ok_label=None, cancel_label=None, width=None, height=None):
        super().__init__(window_icon, ok_label, cancel_label, width, height)
        self.arguments.append('--notification')
        if text is not None:
            self.arguments.append(f'--text={text}')


class List(BaseZenityDialogue):
    def __init__(self, column_names, editable=False, select_col=None, list_dialogue_type=None, separator='|', rows=None,
                 title=None, text=None, window_icon=None, ok_label=None, cancel_label=None, width=None, height=None):
        super().__init__(window_icon, ok_label, cancel_label, width, height)
        self.arguments.append('--list')
        for column_name in column_names:
            self.arguments.append(f'--column={column_name}')
        if title is not None:
            self.arguments.append(f'--title={title}')
        if text is not None:
            self.arguments.append(f'--text={text}')
        self.arguments.append(f'--separator={separator}')
        if editable:
            self.arguments.append('--editable')
        if select_col is not None:
            self.arguments.append(f'--print-column={select_col}')
        if list_dialogue_type is not None:
            if list_dialogue_type not in ('checklist', 'radiolist'):
                raise ZenityError(f'{list_dialogue_type} is not a valid list dialogue type')
            self.arguments.append(f'--{list_dialogue_type}')

        if rows is not None:
            for row in rows:
                if len(row) != len(column_names):
                    raise ZenityError(f"row: {row}, has the wrong number of items")
                for item in row:
                    self.arguments.append(str(item))


class ZenityMessage(BaseZenityDialogue):
    def __init__(self, text=None, title=None, window_icon=None, ok_label=None, width=None,
                 height=None):
        super().__init__(window_icon, ok_label, None, width, height)
        if title is not None:
            self.arguments.append(f'--title={title}')
        if text is not None:
            self.arguments.append(f'--text={text}')


class ErrorMessage(ZenityMessage):
    def __init__(self, text=None, title=None, window_icon=None, ok_label=None, width=None,
                 height=None):
        super().__init__(text, title, window_icon, ok_label, width, height)
        self.arguments.append('--error')


class WarningMessage(ZenityMessage):
    def __init__(self, text=None, title=None, window_icon=None, ok_label=None, width=None,
                 height=None):
        super().__init__(text, title, window_icon, ok_label, width, height)
        self.arguments.append('--warning')


class QuestionMessage(ZenityMessage):
    def __init__(self, text=None, title=None, window_icon=None, ok_label=None, width=None,
                 height=None):
        super().__init__(text, title, window_icon, ok_label, width, height)
        self.arguments.append('--question')


class SingleLineEntry(ZenityMessage):
    def __init__(self, text=None, title=None, entry_text=None, hide_text=False, window_icon=None, ok_label=None,
                 width=None, height=None):
        super().__init__(text, title, window_icon, ok_label, width, height)
        self.arguments.append('--entry')
        if entry_text is not None:
            self.arguments.append(entry_text)
        if hide_text:
            self.arguments.append('--hide-text')


class TextEntry(BaseZenityDialogue):
    def __init__(self, title=None, filename=None, editable=False, window_icon=None, ok_label=None, cancel_label=None,
                 width=None, height=None):
        super().__init__(window_icon, ok_label, cancel_label, width, height)
        self.arguments.append('--text-info')
        if title is not None:
            self.arguments.append(f'--title={title}')
        if filename is not None:
            self.arguments.append(f'--filename={filename}')
        if editable:
            self.arguments.append(f'--editable')


class ColorSelection(BaseZenityDialogue):
    def __init__(self, title=None, show_palette=False, window_icon=None, ok_label=None, cancel_label=None,
                 width=None, height=None):
        super().__init__(window_icon, ok_label, cancel_label, width, height)
        self.arguments.append('--color-selection')
        if title is not None:
            self.arguments.append(f'--title={title}')
        if show_palette:
            self.arguments.append('--show-palette')


class ScaleSelection(BaseZenityDialogue):
    def __init__(self, title=None, text=None, initial_value=None, max_value=None, min_value=None, hide_value=False,
                 window_icon=None, ok_label=None, cancel_label=None, width=None, height=None):
        super().__init__(window_icon, ok_label, cancel_label, width, height)
        self.arguments.append('--scale')
        if title is not None:
            self.arguments.append(f'--title={title}')
        if text is not None:
            self.arguments.append(f'--text={text}')
        if initial_value is not None:
            self.arguments.append(f'--value={initial_value}')
        if max_value is not None:
            self.arguments.append(f'--max-value={max_value}')
        if min_value is not None:
            self.arguments.append(f'--min-value={min_value}')
        if hide_value:
            self.arguments.append(f'--hide-value')


class PasswordEntry(BaseZenityDialogue):
    def __init__(self, title=None, username=False, ok_label=None, cancel_label=None,
                 width=None, height=None):
        super().__init__(None, ok_label, cancel_label, width, height)
        self.arguments.append('--password')
        if title is not None:
            self.arguments.append(f'--title={title}')
        if username:
            self.arguments.append('--username')


class ProgressBar(BaseZenityDialogue):
    def __init__(self, text=None, title=None, percentage=0, auto_close=False, pulsate=False, window_icon=None,
                 ok_label=None, cancel_label=None, width=None, height=None):
        super().__init__(window_icon, ok_label, cancel_label, width, height)
        self.arguments.append('--progress')
        self.arguments.append(f'--percentage={percentage}')
        if text is not None:
            self.arguments.append(f'--text={text}')
        if title is not None:
            self.arguments.append(f'--title={title}')
        if auto_close:
            self.arguments.append('--auto-close')
        if pulsate:
            self.arguments.append('--pulsate')

    def update_progress(self, percentage):
        """
        This function will update the position of the progress bar
        :param percentage: the new percentage to move the progress bar to
        """
        self.send_input(f'{str(percentage)}\n')

    def update_message(self, message):
        """
        THis will update the message displayed above the progress bar
        :param message: the new message to display
        """
        self.send_input(f'# {message}\n')
