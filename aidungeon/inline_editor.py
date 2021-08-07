from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import (
    HSplit,
    Window,
)
from .utils import clear_lines, getTermWidth
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.widgets import (
    TextArea,
)


def edit_multiline(default_text=""):
    kb = KeyBindings()

    @kb.add('c-q')
    @kb.add('escape', 'enter')
    def exit_(event):
        """
        Pressing Ctrl-Q, Alt+Enter or Esc + Enter will exit the editor.
        """
        event.app.exit(textf.text)

    @kb.add('c-c')
    def do_copy(event):
        data = textf.buffer.copy_selection()
        get_app().clipboard.set_data(data)

    @kb.add('c-x', eager=True)
    def do_cut(event):
        data = textf.buffer.cut_selection()
        get_app().clipboard.set_data(data)

    @kb.add('c-z')
    def do_undo(event):
        textf.buffer.undo()

    @kb.add('c-y')
    def do_redo(event):
        textf.buffer.redo()

    @kb.add('c-a')
    def do_select_all(event):
        textf.buffer.cursor_position = 0
        textf.buffer.start_selection()
        textf.buffer.cursor_position = len(textf.buffer.text)
        update_stored_pos(None)

    @kb.add('c-v')
    def do_paste(event):
        textf.buffer.paste_clipboard_data(get_app().clipboard.get_data())

    @kb.add('left')
    def kb_left(event):
        textf.buffer.selection_state = None
        if textf.buffer.cursor_position != 0 and textf.text[textf.buffer.cursor_position-1] == '\n':
            textf.buffer.cursor_up()
            textf.buffer.cursor_right(len(textf.text))
        else:
            textf.buffer.cursor_left()
        update_stored_pos(None)

    @kb.add('right')
    def kb_right(event):
        textf.buffer.selection_state = None
        if textf.buffer.cursor_position < len(textf.text) and textf.text[textf.buffer.cursor_position] == '\n':
            textf.buffer.cursor_down()
            textf.buffer.cursor_left(len(textf.text))

        else:
            textf.buffer.cursor_right()
        update_stored_pos(None)

    @kb.add('home')
    def kb_home(event):
        textf.buffer.selection_state = None
        width = getTermWidth()
        doc = textf.document
        if textf.buffer.cursor_position == doc._line_start_indexes[cursor_row()] + int(cursor_col() / width) * width:
            textf.buffer.cursor_position = doc._line_start_indexes[cursor_row()]
        else:
            textf.buffer.cursor_position = doc._line_start_indexes[cursor_row()] + int(cursor_col() / width) * width
        update_stored_pos(None)

    @kb.add('end')
    def kb_end(event):
        textf.buffer.selection_state = None
        width = getTermWidth()
        doc = textf.document
        row = cursor_row()
        if textf.buffer.cursor_position == doc._line_start_indexes[row] + (int(cursor_col() / width) + 1) * width - 1:
            textf.buffer.cursor_position = doc._line_start_indexes[row] + len(doc.current_line)
        else:
            textf.buffer.cursor_position = min(doc._line_start_indexes[row] + (int(cursor_col() / width) + 1) * width - 1, doc._line_start_indexes[row] + len(doc.current_line))
        update_stored_pos(None)

    @kb.add('up')
    def kb_up(event):
        textf.freezestore = True
        width = getTermWidth()
        doc = textf.document
        textf.buffer.selection_state = None
        col = cursor_col()
        row = cursor_row()
        if width > 9000:  # A failsafe in case the terminal size is incorrectly detected
            textf.buffer.cursor_up()
            return

        if col >= width:  # Move one row up staying on the same line
            textf.buffer.cursor_position = doc._line_start_indexes[row] + int(col / width - 1) * width + textf.stored_cursor_pos
        elif row >= 1:   # Moving up to a different line
            prevlinelen = len(doc.lines[row - 1])

            textf.buffer.cursor_position = min(doc._line_start_indexes[row] - 1, doc._line_start_indexes[row-1]+int(prevlinelen / width)*width + textf.stored_cursor_pos)
        else:                                # Cursor is on the first row of first line
            textf.buffer.cursor_position = 0
            textf.freezestore = False
            update_stored_pos(None)

    @kb.add('down')
    def kb_down(event):
        textf.freezestore = True
        width = getTermWidth()
        doc = textf.document
        textf.buffer.selection_state = None
        col = cursor_col()
        row = cursor_row()
        nextlinelen = len(doc.lines[row + 1]) if row < len(doc.lines)-1 else -1
        if width > 9000:  # A failsafe in case the terminal size is incorrectly detected
            textf.buffer.cursor_down()
            return

        if col <= len(doc.current_line)-width:  # Move one row down staying on the same line
            textf.buffer.cursor_position = doc._line_start_indexes[row] + int(col / width + 1) * width + textf.stored_cursor_pos
        elif nextlinelen < 0:  # Move to the very end
            textf.buffer.cursor_position = len(textf.text)
            textf.freezestore = False
            update_stored_pos(None)
        # Move to the end of the same line the cursor is on
        elif col != len(doc.lines[row]) and textf.stored_cursor_pos >= len(doc.lines[row]) - int(len(doc.lines[row]) / width)*width:
            textf.buffer.cursor_position = doc._line_start_indexes[row+1] - 1
        else:  # Move to a different line
            textf.buffer.cursor_position = min(doc._line_start_indexes[row+1]+nextlinelen, doc._line_start_indexes[row+1]+textf.stored_cursor_pos)


    textf = TextArea()
    bottom_bar_text=FormattedTextControl(text='\nCurrently editing. Press Ctrl+Q, Alt+Enter or Esc + Enter to exit.')
    bottom_bar=Window(content=bottom_bar_text)

    root_container = HSplit([
        textf,
        bottom_bar,
    ])

    layout = Layout(root_container)

    app = Application(key_bindings=kb, layout=layout, enable_page_navigation_bindings=True, full_screen=False)
    textf.freezestore = False
    textf.text=default_text
    textf.buffer.cursor_position = len(textf.buffer.text)


    # Find the row the cursor is at
    # My own function, in fear of race conditions
    def cursor_row():
        i = 0
        while i < len(textf.document._line_start_indexes) and textf.buffer.cursor_position >= textf.document._line_start_indexes[i]:
            i+=1
        return i-1


    # Find the column the cursor is at
    # There is a built-in function, but I think there's some kind of a race condition if it's used
    def cursor_col():
        i = textf.buffer.cursor_position - 1
        while i >= 0 and textf.text[i] != '\n':
            i-=1
        return textf.buffer.cursor_position - i - 1


    def update_stored_pos(event):
        if not event:
            textf.freezestore = False
        if textf.freezestore:
            textf.freezestore = False
            return
        width = getTermWidth()
        col = cursor_col()
        textf.stored_cursor_pos = col - int(col / width) * width

    textf.buffer.on_cursor_position_changed += update_stored_pos
    update_stored_pos(None)

    text = app.run()

    clear_lines(1)

    return text


if __name__ == "__main__":
    print()
    print()
    print()
    editthis = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam eu fringilla sapien. Maecenas sodales consequat lorem, in consectetur mi interdum eu. Nullam ut odio mattis, congue odio non, vulputate metus. Integer vel eros eu risus ultricies venenatis a id diam. Nullam viverra congue quam, in aliquam tellus posuere et. Fusce pharetra interdum velit eget hendrerit. Nulla nec velit nibh. Integer at quam sem. Suspendisse tincidunt est non porttitor lobortis. Nulla orci justo, euismod a venenatis eget, feugiat et orci." +\
    "\nDonec faucibus volutpat diam, nec varius arcu condimentum eget." +\
    "\nUt sollicitudin blandit leo in faucibus. Etiam dictum pretium placerat. Nulla blandit diam vel justo fermentum, sit amet tempor ante gravida." +\
    "\n\nDonec maximus cursus eros, sit amet dapibus tellus. Nullam sed ultrices lacus. Sed nibh nisi, ornare a libero et, mattis facilisis tellus. Cras mauris metus, vulputate ut dolor at, viverra ullamcorper nisi. Nulla ornare augue eget orci semper, ac congue nibh placerat. Duis rhoncus ipsum ut eros eleifend, sed mollis odio ullamcorper. Sed at justo magna."
    edit_multiline(editthis)
