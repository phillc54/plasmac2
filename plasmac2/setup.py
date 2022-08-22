
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
                #return
            title = 'Path Exists'
            msg = 'plasmac2 already exists... Overwrite?'
            reply = messagebox.askyesno(title, msg)
            if not reply:
                return
        copytree(os.path.dirname(sys.argv[0]), b2tf, dirs_exist_ok=True)
        title = 'Success'
        msg = 'Files copied to '
        messagebox.showinfo(title, msg + b2tf)

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
        newIni = os.path.join(newDir, iniFile)
        if os.path.exists(newDir):
            title = 'Path Exists'
            msg = ' already exists... Overwrite?'
            reply = messagebox.askyesno(title, newDir + msg)
            if not reply:
                return
        copytree(oldDir, newDir, dirs_exist_ok=True)
        with open(newIni, 'r') as inFile:
            config = inFile.readlines()
        # [DISPLAY] section
        section = {}
        for lNum in range(config.index('[DISPLAY]\n') + 1, len(config)):
            if config[lNum].startswith('['):
                break
            section[lNum] = config[lNum]
        insert = lNum - 1 if config[lNum - 1] == '\n' else lNum
        done = []
        for lNum in section:
            if section[lNum].startswith('DISPLAY') and 'd' not in done:
                config[lNum] = 'DISPLAY = axis\n'
                done.append('d')
            elif section[lNum].startswith('OPEN_FILE') and 'o' not in done:
                config[lNum] = 'OPEN_FILE = ""\n'
                done.append('o')
            elif section[lNum].startswith('TOOL_EDITOR') and 't' not in done:
                config[lNum] = 'TOOL_EDITOR = tooledit x y\n'
                done.append('t')
            elif section[lNum].startswith('CYCLE_TIME') and 'c' not in done:
                config[lNum] = 'CYCLE_TIME = 100\n'
                done.append('c')
            elif section[lNum].startswith('USER_COMMAND_FILE') and 'u' not in done:
                config[lNum] = 'USER_COMMAND_FILE = ./plasmac2/plasmac2.py\n'
                done.append('u')
        for option in ['d','o','t','c','u']:
            if option == 'd' and option not in done:
                config.insert(insert,'DISPLAY = axis\n')
            elif option == 'o' and option not in done:
                config.insert(insert,'OPEN_FILE = ""\n')
            elif option == 't' and option not in done:
                config.insert(insert,'TOOL_EDITOR = tooledit x y\n')
            elif option == 'c' and option not in done:
                config.insert(insert,'CYCLE_TIME = 100\n')
            elif option == 'u' and option not in done:
                config.insert(insert,'USER_COMMAND_FILE = ./plasmac2/plasmac2.py\n')
        # [RS274NGC] section
        section = {}
        for lNum in range(config.index('[RS274NGC]\n') + 1, len(config)):
            if config[lNum].startswith('['):
                break
            section[lNum] = config[lNum]
        insert = lNum - 1 if config[lNum - 1] == '\n' else lNum
        done = []
        for lNum in section:
            if section[lNum].startswith('USER_M_PATH') and 'u' not in done:
                mPath = config[lNum].split('=')[1].strip()
                config[lNum] = 'USER_M_PATH = ./qtplasmac:{}\n'.format(mPath)
                done.append('u')
        for option in ['u']:
            if option == 'u' and option not in done:
                config.insert(insert,'USER_M_PATH = ./qtplasmac:./\n')
        # [FILTER] section
        section = {}
        for lNum in range(config.index('[FILTER]\n') + 1, len(config)):
            if config[lNum].startswith('['):
                break
            section[lNum] = config[lNum]
        insert = lNum - 1 if config[lNum - 1] == '\n' else lNum
        done = []
        for lNum in section:
            if section[lNum].startswith('PROGRAM_EXTENSION') and 'p' not in done:
                config[lNum] = 'PROGRAM_EXTENSION = .ngc,.nc,.tap (filter gcode files)\n'
                done.append('p')
            if section[lNum].startswith('ngc') and 'g' not in done:
                config[lNum] = 'ngc = qtplasmac_gcode\n'
                done.append('g')
            if section[lNum].startswith('nc') and 'c' not in done:
                config[lNum] = 'nc = qtplasmac_gcode\n'
                done.append('c')
            if section[lNum].startswith('tap') and 'a' not in done:
                config[lNum] = 'tap = qtplasmac_gcode\n'
                done.append('a')
        for option in ['a','c','g','p']:
            if option == 'a' and option not in done:
                config.insert(insert,'tap = qtplasmac_gcode\n')
            elif option == 'c' and option not in done:
                config.insert(insert,'nc = qtplasmac_gcode\n')
            elif option == 'g' and option not in done:
                config.insert(insert,'ngc = qtplasmac_gcode\n')
            elif option == 'p' and option not in done:
                config.insert(insert,'PROGRAM_EXTENSION = .ngc,.nc,.tap (filter gcode files)\n')
        # [HAL] section
        section = {}
        sim = False
        for lNum in range(config.index('[HAL]\n') + 1, len(config)):
            if config[lNum].startswith('['):
                break
            section[lNum] = config[lNum]
        for lNum in section:
            if section[lNum].startswith('HALFILE') or section[lNum].startswith('POSTGUI_HALFILE'):
                halFile = config[lNum].split('=')[1].strip()
                if 'sim_postgui' in halFile:
                    sim = True
                if 'qtplasmac_comp.hal' not in halFile and 'sim_no_stepgen' not in halFile:
                    if not os.path.dirname(halFile):
                        halFile = os.path.join(newDir, halFile)
                    with open(halFile, 'r') as halRead:
                        if 'qtplasmac' in halRead.read():
                            config[lNum] = '# {}'.format(config[lNum])
                            title = 'HAL Error'
                            msg0 = 'There are references to qtplasmac in '
                            msg1 = 'The HAL file has been commented out in the ini file'
                            messagebox.showerror(title, msg0 + halFile + '\n' + msg1)
        if sim:
            config.insert(0, '[APPLICATIONS]\n' \
                             'DELAY = 1\n' \
                             'APP = plasmac_sim.py\n')
        # write the ini file
        with open(newIni, 'w') as outFile:
            for line in config:
                outFile.write(line)
        # create a link to plasmac2
        if os.path.exists(os.path.join(newDir, 'plasmac2')):
            os.remove(os.path.join(newDir, 'plasmac2'))
        os.symlink(os.path.expanduser('~/linuxcnc/plasmac2'), os.path.join(newDir, 'plasmac2'))
        # we made it...
        title = 'Success'
        msg = 'Ini file for PlasmaC2 config is '
        messagebox.showinfo(title, msg + os.path.join(newDir, iniFile))

    def sim(self):
        print('CREATE A SIM')

    def shutdown(self):
        raise SystemExit

root = Tk()
my_gui = Setup(root)
root.mainloop()
