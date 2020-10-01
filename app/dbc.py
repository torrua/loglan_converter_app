#  -*- coding: utf-8 -*-

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

from app import dbc_support, is_db_connected
from tkinter import PhotoImage, messagebox
import base64
from converters.ac_to_txt import convert_ac_to_txt
from converters.txt_to_ac import convert_txt_to_ac
from converters.txt_to_pg import convert_txt_to_pg
from converters.pg_to_txt import convert_pg_to_txt
from converters.ac_to_pg import convert_ac_to_pg
from converters.pg_to_ac import convert_pg_to_ac

from config.text import IMPORT_DIRECTORY_PATH_REMOTE, IMPORT_DIRECTORY_PATH_LOCAL, EXPORT_DIRECTORY_PATH_LOCAL
from config.text.functions import download_file
from config.postgres.models import all_models_pg
from config.postgres import app_lod

popup_message_title = 'Loglan Converter'
msg_success_export = f'Export completed successfully!'
msg_success = (popup_message_title, msg_success_export)


def app_context():
    """
    Configuration object for remote database
    """
    postgres_uri = dbc_support.postgres_uri.get()

    if not postgres_uri:
        raise ValueError("DB URI is empty. Please specify the Postgres URI")

    class AppConfig:
        SQLALCHEMY_DATABASE_URI = postgres_uri
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    return app_lod(AppConfig).app_context()


def convert_with_context(function):
    def wrapper(*args, **kwargs):
        try:
            context = app_context()
        except ValueError as err:
            messagebox.showwarning(popup_message_title, err)
            return

        context.push()
        function(*args, **kwargs)
        context.pop()

    return wrapper


def get_import_path():
    import_local_path = dbc_support.import_path.get() if dbc_support.import_path.get() else IMPORT_DIRECTORY_PATH_LOCAL
    return IMPORT_DIRECTORY_PATH_REMOTE if dbc_support.from_git.get() else import_local_path


def get_export_path():
    return dbc_support.export_path.get() if dbc_support.export_path.get() else EXPORT_DIRECTORY_PATH_LOCAL


def button_convert_ac_to_txt():
    destination = get_export_path()
    convert_ac_to_txt(output_directory=destination)
    messagebox.showinfo(*msg_success)


def button_convert_txt_to_ac():
    source = get_import_path()
    convert_txt_to_ac(source_directory=source)
    messagebox.showinfo(popup_message_title, f'Export completed successfully from {source}!')


@convert_with_context
def button_convert_txt_to_pg():
    source = get_import_path()
    convert_txt_to_pg(source_directory=source)
    messagebox.showinfo(popup_message_title, f'Export completed successfully from {source}!')


@convert_with_context
def button_convert_ac_to_pg():
    convert_ac_to_pg()
    messagebox.showinfo(*msg_success)


@convert_with_context
def button_convert_pg_to_ac():
    convert_pg_to_ac()
    messagebox.showinfo(*msg_success)


@convert_with_context
def button_convert_pg_to_txt():
    destination = get_export_path()
    convert_pg_to_txt(output_directory=destination)
    messagebox.showinfo(*msg_success)


def download_txt_to_import():
    from pathlib import Path
    import_path = dbc_support.import_path.get()
    if import_path:
        Path(import_path).mkdir(parents=True, exist_ok=True)

    files = [
        f"{IMPORT_DIRECTORY_PATH_REMOTE}{model.import_file_name}" for
        model in all_models_pg if model.import_file_name]

    for file in files:
        download_file(file, import_path)


def download_mdb_filled():
    download_file("https://github.com/torrua/LOD/raw/master/source/LoglanDictionary.mdb")


def download_mdb_empty():
    download_file("https://github.com/torrua/LOD/raw/master/source/LoglanDictionaryTemplate.mdb")


def vp_start_gui():
    global val, w, root
    root = tk.Tk()
    icon = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAAACBjSFJN' \
           'AAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAABNVBMVEUAAABkokZ0r1N3slV2' \
           'sVV3slR5s1M9cR13slQ+cRx3slV0sVM9cRxQhi53sVV3sVV2sVhAgAA+cR0+chw+cRx3slV3slVV' \
           'qlWAn0B3sVJ1sVR5sVU3bxZtqk93slV3sVR2slV3s1V3s1V3sFV3slV3slR3sFN1sVR3slVmzGZ0' \
           'okZ2sFV3sVRgn0A+ch05cRx3slZ2slc7chs+chw+cR12s1V3sVV3slV2sVV4slYAAAB4s1R2rVI+' \
           'cx0+ch08chtelj08cBx2slR2sVRbkzpooUZ1slQ+chx4slR3s1aAr1B3slV0rlV3sVVttkl3slZj' \
           'nEE9ch13sVR3tFVmoEk8bhk9cBl2s1V3sVN5s1V2slKAv0B5slV5tlVRhy93slU+ch1spkpQhi9o' \
           'oUZ1sFNHfCX///+WtFy5AAAAXnRSTlMAIbbDxMMou6la/S6r/cG0GgRz84fK6QMIPnxOFyrHmrf3' \
           'uy2s9UdV9AULVJQIVwmYODjOgzb95bFZAXkc4/gmm0CReaOamPSRaxDnOeMHVv7xdmkjMzJ1ZTk4' \
           'BF0Vpi9+UAAAAAFiS0dEZizU2SUAAAAHdElNRQfkBhsBCw3V3hlLAAAAyElEQVQY02NgAAFGJmYW' \
           'VjYGBGCPi4+P50DwORMSEuPjubjhAjwJCbxAJXz8AlABQSFhEVGgiJg4mCshKSUtIysHFJAH8xUU' \
           '4+OVGJRVVOPj1cAC6kApDU0GBi1tHV09faCAAVAg3hAkZWScYMLAYGoWH29uYclgZW1jm5BgZ88A' \
           'MszBkcHKKd7ZJSkpzpXBLT4+OcHdyiMeAjwZvLxTUhPcfaB8Xz8GBv+AhIRAhiCIQDDI8JDQMHsG' \
           'hvD4iMjIqGgkH8fEgikAm7UtvPE/wy8AAAAldEVYdGRhdGU6Y3JlYXRlADIwMjAtMDYtMjdUMDE6' \
           'MTE6MTMrMDA6MDC2HXIrAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIwLTA2LTI3VDAxOjExOjEzKzAw' \
           'OjAwx0DKlwAAAABJRU5ErkJggg=='
    img = PhotoImage(data=base64.b64decode(icon))
    root.wm_iconphoto(True, img)

    dbc_support.set_tk_variables()
    top = MainWindow(root)

    dbc_support.init(root, top)

    def trigger_git_local_import(event):
        top.import_path.configure(state="normal") if \
            dbc_support.from_git.get() else top.import_path.configure(state="disable")

    """
    def trigger_pg_buttons_state(event):
        uri = dbc_support.postgres_uri.get()
        state = "disable" if not uri else "normal"

        top.BAP.configure(state=state)
        top.BPA.configure(state=state)
        top.BPT.configure(state=state)
        top.BTP.configure(state=state)
    """

    def trigger_pg_buttons_state(event):
        uri = dbc_support.postgres_uri.get()

        if not uri:
            messagebox.showwarning("No DB URI", "The DB URI field is empty. Please provide the path to the database.")
            return

        db_connection = is_db_connected(uri)
        state = "normal" if db_connection else "disable"
        top.BAP.configure(state=state)
        top.BPA.configure(state=state)
        top.BPT.configure(state=state)
        top.BTP.configure(state=state)
        if not db_connection:
            messagebox.showwarning("No Connection", "Failed to connect the database at the provided address.")

    top.is_from_github.bind('<Button-1>', trigger_git_local_import)
    top.BTC.bind('<ButtonRelease-1>', trigger_pg_buttons_state)

    root.mainloop()


w = None


def create_main_window(rt, *args, **kwargs):
    """Starting point when module is imported by another module.
       Correct form of call: 'create_MainWindow(root, *args, **kwargs)' ."""
    global w, w_win, root
    # rt = root
    root = rt
    w = tk.Toplevel(root)
    dbc_support.set_tk_variables()
    top = MainWindow(w)
    dbc_support.init(w, top, *args, **kwargs)
    return w, top


def destroy_main_window():
    global w
    w.destroy()
    w = None


class MainWindow:
    def __init__(self, top=None):
        """This class configures and populates the top level window.
           top is the top level containing window."""
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9'  # X11 color: 'gray85'
        _ana1color = '#d9d9d9'  # X11 color: 'gray85'
        _ana2color = '#ececec'  # Closest X11 color: 'gray92'
        font9 = "-family {Segoe UI} -size 9"
        pg_buttons_default_state = "disable"

        top.geometry("584x348+1259+518")
        top.minsize(120, 1)
        top.maxsize(3460, 1181)
        top.resizable(1, 1)
        top.title("Loglan DB Converter")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        self.configuration = tk.LabelFrame(top)
        self.configuration.place(relx=0.017, rely=0.03, relheight=0.775
                                 , relwidth=0.964)
        self.configuration.configure(relief='groove')
        self.configuration.configure(foreground="black")
        self.configuration.configure(text='''Configuration''')
        self.configuration.configure(background="#d9d9d9")
        self.configuration.configure(highlightbackground="#d9d9d9")
        self.configuration.configure(highlightcolor="black")

        default_entry_configuration = dict(
            background="white",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            insertbackground="black",
            selectbackground="#c4c4c4",
            selectforeground="black",
            # state="readonly",
            font=font9, )

        default_button_configuration = dict(
            activebackground="#ececec",
            activeforeground="#000000",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black",
            pady="0", )

        default_label_configuration = dict(
            activebackground="#f9f9f9",
            activeforeground="black",
            background="#d9d9d9",
            disabledforeground="#a3a3a3",
            foreground="#000000",
            highlightbackground="#d9d9d9",
            highlightcolor="black", )

        self.postgres_uri = tk.Entry(self.configuration)
        self.postgres_uri.place(relx=0.178, rely=0.118, height=24, relwidth=0.643
                                , bordermode='ignore')
        # self.postgres_uri.configure(show="test")
        self.postgres_uri.configure(**default_entry_configuration)
        self.postgres_uri.configure(textvariable=dbc_support.postgres_uri)
        self.tooltip_font = "TkDefaultFont"
        self.postgres_uri_tooltip = \
        ToolTip(self.postgres_uri, self.tooltip_font, '''Enter URI here...''')

        self.p_label = tk.Label(self.configuration)
        self.p_label.place(relx=0.078, rely=0.125, height=20, width=50
                           , bordermode='ignore')
        self.p_label.configure(**default_label_configuration)
        self.p_label.configure(text='''DB URI''')

        self.access_path = tk.Entry(self.configuration)
        self.access_path.place(relx=0.178, rely=0.275, height=24, relwidth=0.789
                               , bordermode='ignore')
        self.access_path.configure(**default_entry_configuration)
        self.access_path.configure(textvariable=dbc_support.access_path)
        self.access_path_tooltip = \
            ToolTip(self.access_path, self.tooltip_font, '''Enter path to *.mdb file''')

        self.a_label = tk.Label(self.configuration)
        self.a_label.place(relx=0.036, rely=0.282, height=20, width=75
                           , bordermode='ignore')
        self.a_label.configure(**default_label_configuration)
        self.a_label.configure(text='''Access Path''')

        self.export_path = tk.Entry(self.configuration)
        self.export_path.place(relx=0.178, rely=0.549, height=24, relwidth=0.789
                               , bordermode='ignore')
        self.export_path.configure(**default_entry_configuration)
        self.export_path.configure(textvariable=dbc_support.export_path)
        self.export_path_tooltip = \
            ToolTip(self.export_path, self.tooltip_font, '''Enter directory for export...''')

        self.e_label = tk.Label(self.configuration)
        self.e_label.place(relx=0.053, rely=0.549, height=20, width=69
                           , bordermode='ignore')
        self.e_label.configure(**default_label_configuration)
        self.e_label.configure(text='''Export to''')

        self.import_path = tk.Entry(self.configuration)
        self.import_path.place(relx=0.178, rely=0.706, height=24, relwidth=0.789
                               , bordermode='ignore')
        self.import_path.configure(**default_entry_configuration)
        self.import_path.configure(textvariable=dbc_support.import_path)
        self.import_path.configure(state="disable")

        self.i_label = tk.Label(self.configuration)
        self.i_label.place(relx=0.036, rely=0.706, height=21, width=71
                           , bordermode='ignore')
        self.i_label.configure(**default_label_configuration)
        self.i_label.configure(text='''Import from''')

        self.is_from_github = tk.Checkbutton(self.configuration)
        self.is_from_github.place(relx=0.568, rely=0.839, relheight=0.09
                                  , relwidth=0.316, bordermode='ignore')
        self.is_from_github.configure(activebackground="#ececec")
        self.is_from_github.configure(activeforeground="#000000")
        self.is_from_github.configure(background="#d9d9d9")
        self.is_from_github.configure(disabledforeground="#a3a3a3")
        self.is_from_github.configure(foreground="#000000")
        self.is_from_github.configure(highlightbackground="#d9d9d9")
        self.is_from_github.configure(highlightcolor="black")
        self.is_from_github.configure(justify='left')
        self.is_from_github.configure(text='''Use text files from Github''')
        self.is_from_github.configure(variable=dbc_support.from_git)

        self.BFF = tk.Button(self.configuration, command=download_mdb_filled)
        self.BFF.place(relx=0.178, rely=0.408, height=24, width=217
                       , bordermode='ignore')
        self.BFF.configure(activebackground="#ececec")
        self.BFF.configure(activeforeground="#000000")
        self.BFF.configure(background="#d9d9d9")
        self.BFF.configure(disabledforeground="#a3a3a3")
        self.BFF.configure(foreground="#000000")
        self.BFF.configure(highlightbackground="#d9d9d9")
        self.BFF.configure(highlightcolor="black")
        self.BFF.configure(pady="0")
        self.BFF.configure(text='''Download filled MDB file''')

        self.BEF = tk.Button(self.configuration, command=download_mdb_empty)
        self.BEF.place(relx=0.584, rely=0.408, height=24, width=217
                       , bordermode='ignore')
        self.BEF.configure(activebackground="#ececec")
        self.BEF.configure(activeforeground="#000000")
        self.BEF.configure(background="#d9d9d9")
        self.BEF.configure(disabledforeground="#a3a3a3")
        self.BEF.configure(foreground="#000000")
        self.BEF.configure(highlightbackground="#d9d9d9")
        self.BEF.configure(highlightcolor="black")
        self.BEF.configure(pady="0")
        self.BEF.configure(text='''Download empty MDB file''')

        self.BTF = tk.Button(self.configuration, command=download_txt_to_import)
        self.BTF.place(relx=0.178, rely=0.839, height=24, width=217
                       , bordermode='ignore')
        self.BTF.configure(activebackground="#ececec")
        self.BTF.configure(activeforeground="#000000")
        self.BTF.configure(background="#d9d9d9")
        self.BTF.configure(disabledforeground="#a3a3a3")
        self.BTF.configure(foreground="#000000")
        self.BTF.configure(highlightbackground="#d9d9d9")
        self.BTF.configure(highlightcolor="black")
        self.BTF.configure(pady="0")
        self.BTF.configure(text='''Download text files''')

        self.BTC = tk.Button(self.configuration)
        self.BTC.place(relx=0.845, rely=0.118, height=24, width=67
                       , bordermode='ignore')
        self.BTC.configure(activebackground="#ececec")
        self.BTC.configure(activeforeground="#000000")
        self.BTC.configure(background="#d9d9d9")
        self.BTC.configure(disabledforeground="#a3a3a3")
        self.BTC.configure(foreground="#000000")
        self.BTC.configure(highlightbackground="#d9d9d9")
        self.BTC.configure(highlightcolor="black")
        self.BTC.configure(pady="0")
        self.BTC.configure(text='''Connect''')

        self.BTP = tk.Button(top, command=button_convert_txt_to_pg)
        self.BTP.place(relx=0.839, rely=0.851, height=35, width=80)
        self.BTP.configure(**default_button_configuration)
        self.BTP.configure(text='''text to db''')
        self.BTP.configure(state=pg_buttons_default_state)

        self.BTA = tk.Button(top, command=button_convert_txt_to_ac)
        self.BTA.place(relx=0.017, rely=0.851, height=35, width=90)
        self.BTA.configure(**default_button_configuration)
        self.BTA.configure(text='''text to access''')

        self.BAP = tk.Button(top, command=button_convert_ac_to_pg)
        self.BAP.place(relx=0.36, rely=0.851, height=35, width=90)
        self.BAP.configure(**default_button_configuration)
        self.BAP.configure(text='''access to db''')
        self.BAP.configure(state=pg_buttons_default_state)

        self.BAT = tk.Button(top, command=button_convert_ac_to_txt)
        self.BAT.place(relx=0.188, rely=0.851, height=35, width=90)
        self.BAT.configure(**default_button_configuration)
        self.BAT.configure(text='''access to text''')

        self.BPA = tk.Button(top, command=button_convert_pg_to_ac)
        self.BPA.place(relx=0.531, rely=0.851, height=35, width=80)
        self.BPA.configure(**default_button_configuration)
        self.BPA.configure(text='''db to access''')
        self.BPA.configure(state=pg_buttons_default_state)

        self.BPT = tk.Button(top, command=button_convert_pg_to_txt)
        self.BPT.place(relx=0.685, rely=0.851, height=35, width=80)
        self.BPT.configure(**default_button_configuration)
        self.BPT.configure(text='''db to text''')
        self.BPT.configure(state=pg_buttons_default_state)


# ======================================================
# Support code for Balloon Help (also called tooltips).
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# ======================================================

from time import time, localtime, strftime


class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=0.5, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                font=tooltip_font,
                aspect=1000).grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in milliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()

    def update(self, msg):
        """
        Updates the Tooltip with a new message. Added by Rozen
        """
        self.msgVar.set(msg)

# ===========================================================
#                   End of Class ToolTip
# ===========================================================


if __name__ == "__main__":
    vp_start_gui()
