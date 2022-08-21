
'''
setup.py
'''

from posixpath import expanduser
import sys
import os
from shutil import *
from tkinter import *
from tkinter import font
from tkinter import messagebox
from tkinter import filedialog
import configparser

iniP = configparser.ConfigParser
class iniParse(iniP):
    optionxform = str
    types = {bool: iniP.getboolean,
             float: iniP.getfloat,
             int: iniP.getint,
             str: iniP.get,
             repr: lambda self, section, option: eval(iniP.get(self, section, option)),
            }

    def __init__(self):
        iniP.__init__(self, strict=False, interpolation=None)

class Setup:
    def __init__(self, master):
        self.master = master
        master.title('PlasmaC2 Setup')
        font1 = font.Font(name='TkCaptionFont', exists=True)
        font1.config(family='arial', size=11)
        text = ['Setup utility for PlasmaC2']
        text.append('blah blah blah')
        text.append('blah blah blah')
        text.append('blah blah blah')
        label = Label(master, text='\n'.join(text))
        buttons = Frame(master)
        installB = Button(buttons, text='Install or\nUpdate', width=10, command=lambda: self.install(), padx=0)
        migrateB = Button(buttons, text='Migrate\nQtPlasmaC', width=10, command=lambda: self.migrate(), padx=0)
        simB = Button(buttons, text='Creat\nSimulation', width=10, command=lambda: self.sim(), padx=0)
        quitB = Button(buttons, text='Quit', width=10, height=2, command=lambda: self.shutdown(), padx=0)
        installB.grid(row=0, column=0)
        migrateB.grid(row=0, column=1, padx=(4,2))
        simB.grid(row=0, column=2, padx=(2,4))
        quitB.grid(row=0, column=3)
        label.grid(row=0, column=0, sticky='ew', padx=4, pady=(4,0))
        buttons.grid(row=1, column=0, sticky='ew', padx=4, pady=4)
        self.INI = iniParse()

    def install(self):
        lcnc = os.path.expanduser('~/linuxcnc')
        b2tf = os.path.join(lcnc, 'plasmac2')
        if not os.path.isdir(lcnc):
            title = 'Path Error'
            msg = '~/linuxcnc directory does not exist... ' \
                  'It needs to be created by LinuxCNC ' \
                  'to ensure that the structure is correct'
            messagebox.showerror(title, msg)
            return
        if os.path.exists(b2tf):
            if os.path.islink(b2tf):
                path = os.path.realpath(b2tf)
                title = 'Path Is Link'
                msg = 'plasmac2 directory is a link... ' \
                      'it should be updated at the source:'
                messagebox.showinfo(title, msg + '\n' + path)
                return
            title = 'Path Exists'
            msg = 'plasmac2 already exists... Overwrite?'
            reply = messagebox.askyesno(title, msg)
            if not reply:
                return
        copytree(os.path.dirname(sys.argv[0]), b2tf, dirs_exist_ok=True)
        title = 'Success'
        msg = 'Files copied to '
        reply = messagebox.askyesno(title, msg + b2tf)

    def migrate(self):
        ini = filedialog.askopenfilename(
            title='QtPlasmaC INI File',
            initialdir=os.path.expanduser('~/linuxcnc/configs'),
            filetypes=(('ini files', '*.ini'),))
        if not ini:
            return
        iniFile = os.path.basename(ini)
        oldDir = os.path.dirname(ini)
        newDir = oldDir + '_plasmac2'
        print(iniFile)
        print(oldDir)
        print(newDir)
        if os.path.exists(newDir):
            title = 'Path Exists'
            msg = ' already exists... Overwrite?'
            reply = messagebox.askyesno(title, newDir + msg)
            if not reply:
                return
        copytree(oldDir, newDir, dirs_exist_ok=True)
        self.INI.fn = os.path.join(newDir, iniFile)
        self.INI.read(self.INI.fn)
        mPath = self.getIni('RS274NGC', 'USER_M_PATH', './', str)
        print(mPath)
        self.putIni('DISPLAY', 'DISPLAY', 'axis', str)
        self.putIni('DISPLAY', 'OPEN_FILE', '""', str)
        self.putIni('DISPLAY', 'TOOL_EDITOR', 'tooledit x y', str)
        self.putIni('DISPLAY', 'CYCLE_TIME', '100', str)
        self.putIni('DISPLAY', 'USER_COMMAND_FILE', './plasmac2/plasmac2.py', str)
        self.putIni('RS274NGC', 'USER_M_PATH', './plasmac2:' + mPath, str)

    def sim(self):
        print('CREATE A SIM')

    def shutdown(self):
        raise SystemExit

    def getIni(self, section, option, default=False, type=bool):
        m = self.INI.types.get(type)
        if self.INI.has_section(section):
            if self.INI.has_option(section, option):
                return m(self.INI, section, option)
            else:
                self.INI.set(section, option, str(default))
                self.INI.write(open(self.INI.fn, 'w'))
                return default
        else:
            self.INI.add_section(section)
            self.INI.set(section, option, str(default))
            self.INI.write(open(self.INI.fn, 'w'))
            return default

    def putIni(self, section, option, value, type=bool):
        if self.INI.has_section(section):
            self.INI.set(section, option, str(type(value)))
            self.INI.write(open(self.INI.fn, 'w'))
        else:
            self.INI.add_section(section)
            self.INI.set(section.upper(), option, str(type(value)))
            self.INI.write(open(self.INI.fn, 'w'))

root = Tk()
my_gui = Setup(root)
root.mainloop()
