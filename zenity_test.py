import time

from zenity import DateSelection, List, ErrorMessage, FileSelection, SingleLineEntry, Notification, ProgressBar, \
    QuestionMessage, TextEntry, WarningMessage, ColorSelection, PasswordEntry, ScaleSelection

import datetime
from functools import wraps


def section_separator(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        print('-------------------------------------')
        print(f'Running: {func.__name__}')
        result = func(*args, **kwargs)
        print('-------------------------------------')
        print('\n')
        return result

    return decorator


@section_separator
def test_scale():
    options = {'title': "Scale Test",
               'text': 'this is text',
               'initial_value': 50,
               'max_value': 150,
               'min_value': 50,
               'hide_value': True,
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'cancel_label': 'Cancel :-(',
               'width': 500,
               'height': 400}

    s = ScaleSelection(**options)
    s.run()
    print('output:', s.get_output())

    options['hide_value'] = True
    s = ScaleSelection(**options)
    s.run()
    print('output:', s.get_output())


@section_separator
def test_password():
    options = {'title': "Password Test",
               'username': False,
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'cancel_label': 'Cancel :-(',
               'width': 500,
               'height': 400}
    print('Testing password no username')
    p = PasswordEntry(**options)
    p.run()
    print('output:', p.get_output())

    print('Testing password and username')
    options['username'] = True
    p = PasswordEntry(**options)
    p.run()
    print('output:', p.get_output())


@section_separator
def test_color_selection():
    options = {'title': "Color Test",
               'show_palette': False,
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'cancel_label': 'Cancel :-(',
               'width': 500,
               'height': 400}

    print('Testing color no show palette')
    c = ColorSelection(**options)
    c.run()
    print('output:', c.get_output())

    print('Testing color show palette')
    options['show_palette'] = True
    c = ColorSelection(**options)
    c.run()
    print('output:', c.get_output())


@section_separator
def test_date():
    d = DateSelection(text='please choose a date',
                      title="Date Selection",
                      starting_date=datetime.date(2020, 6, 19),
                      window_icon='/home/user/Desktop/update.png',
                      ok_label='Ok :-)',
                      cancel_label='Cancel :-(',
                      width=400,
                      height=100)
    d.run()
    print('output:', d.get_output())


@section_separator
def test_list():
    options = {'column_names': ('first', 'second', 'third', 'fourth', 'fifth'),
               'editable': False,
               'select_col': 'ALL',
               'list_dialogue_type': 'checklist',
               'rows': [(1, 2, 3, 4, 5), ('a', 'b', 'c', 'd', 'e'), ('A', 'B', 'C', 'D', 'E')],
               'text': 'please choose a row',
               'title': "List Test",
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'cancel_label': 'Cancel :-(',
               'width': 500,
               'height': 400}

    lst = List(**options)
    lst.run()
    print('output:', lst.get_output())
    print()

    print('List test: testing radiolist print ALL columns')
    options['list_dialogue_type'] = 'radiolist'
    lst = List(**options)
    lst.run()
    print('output:', lst.get_output())
    print()

    print('List test: testing radiolist print column 2')
    options['select_col'] = 2
    lst = List(**options)
    lst.run()
    print('output:', lst.get_output())
    print()

    print('List test: testing editable')
    options['list_dialogue_type'] = None
    options['select_col'] = 'ALL'
    lst = List(**options)
    lst.run()
    print('output:', lst.get_output())
    print()


@section_separator
def test_file_selection():
    options = {'multiple': False,
               'separator': '|',
               'directory': False,
               'new': False,
               'window_icon': '/home/user/Desktop/update.png',
               'width': 500,
               'height': 400}

    print('File Selection test: testing single regular existing file')
    f = FileSelection(**options)
    f.run()
    print('output:', f.get_output())

    print('File Selection test: testing multiple files')
    options['multiple'] = True
    f = FileSelection(**options)
    f.run()
    print('output:', f.get_output())

    print('File Selection test: testing single directory')
    options['multiple'] = False
    options['directory'] = True
    f = FileSelection(**options)
    f.run()
    print('output:', f.get_output())

    print('File Selection test: testing single regular new file')
    options['directory'] = False
    options['new'] = True
    f = FileSelection(**options)
    f.run()
    print('output:', f.get_output())


@section_separator
def test_line_entry():
    options = {'text': 'this is text',
               'title': 'Title',
               'entry_text': 'Original text in box',
               'hide_text': False,
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'cancel_label': 'Cancel :-(',
               'width': 500,
               'height': 400}

    print('File Selection test: testing single line input')
    line = SingleLineEntry(**options)
    line.run()
    print('output:', line.get_output())

    print('File Selection test: testing single line hidden input')
    options['hide_text'] = True
    line = SingleLineEntry(**options)
    line.run()
    print('output:', line.get_output())


@section_separator
def test_progress():
    options = {'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'cancel_label': 'Cancel :-(',
               'width': 500,
               'height': 400}
    p = ProgressBar(text='this is text', title='Progress', percentage=0, auto_close=True, **options)
    p.start()
    for i in range(100):
        p.update_message(f'this is update {i}')
        p.update_progress(i)
        time.sleep(0.1)
    p.update_progress(100)
    p.stop()


@section_separator
def test_text_entry():
    options = {'title': 'Title',
               'filename': '/home/user/Documents/railway/1.in',
               'editable': False,
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'cancel_label': 'Cancel :-(',
               'width': 500,
               'height': 400}

    print('text entry: testing non editable file')
    t = TextEntry(**options)
    t.run()
    print('output:', t.get_output())

    print('text entry: testing editable file')
    options['editable'] = True
    t = TextEntry(**options)
    t.run()
    print('output:', t.get_output())


@section_separator
def test_warning():
    options = {'text': 'this is text',
               'title': 'Title',
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'width': 500,
               'height': 400}

    print('Warning test: testing warning')
    w = WarningMessage(**options)
    w.run()


@section_separator
def test_error():
    options = {'text': 'this is text',
               'title': 'Title',
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'width': 500,
               'height': 400}

    print('Error test: testing error')
    e = ErrorMessage(**options)
    e.run()


@section_separator
def test_notification():
    options = {'text': 'this is text',
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'width': 500,
               'height': 400}

    print('Notification test: testing notification')
    n = Notification(**options)
    n.run()


@section_separator
def test_question():
    options = {'text': 'this is text',
               'title': 'Title',
               'window_icon': '/home/user/Desktop/update.png',
               'ok_label': 'Ok :-)',
               'width': 500,
               'height': 400}

    print('Question test: testing question')
    q = QuestionMessage(**options)
    q.run()


if __name__ == '__main__':
    # test_date()
    # test_list()
    # test_file_selection()
    # test_line_entry()
    # test_progress()
    # test_text_entry()
    test_warning()
    test_error()
    test_notification()
    test_password()
    test_color_selection()
    test_scale()
    test_question()
