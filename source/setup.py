#!/usr/bin/python3

'''
setup.py
'''

import sys
import os
import git
from shutil import *
from tkinter import *
from tkinter import filedialog

class Setup:
    def __init__(self, master):
        self.master = master
        master.title('plasmac2 Setup')
        text = ['Setup utility for plasmac2\n']
        text.append('Migration:\n'
                    ' - will copy an existing QtPlasmaC config and make any\n'
                    '   required modifications for plasmac2\n')
        text.append('Simulation:\n'
                    '- will make a new sim using supplied parameters\n'
                    '- name is mandatory\n'
                    '- other missing parameters will have the following applied\n'
                    '  X = 1200mm or 48"\n'
                    '  Y = 1200mm or 48"\n'
                    '  Z = 100mm or 4"\n')
        label = Label(master, text='\n'.join(text), justify='left')
        buttons = Frame(master)
        migrateB = Button(buttons, text='Migration', width=10, command=lambda: self.migrate(), padx=0)
        simB = Button(buttons, text='Simulation', width=10, command=lambda: self.sim(), padx=0)
        quitB = Button(buttons, text='Quit', width=10, command=lambda: self.shutdown(), padx=0)
        migrateB.grid(row=0, column=0)
        simB.grid(row=0, column=1)
        quitB.grid(row=0, column=2)
        label.grid(row=0, column=0, sticky='ew', padx=8, pady=(8,0))
        buttons.grid(row=1, column=0, sticky='ew', padx=8, pady=(16,8))
        buttons.columnconfigure((0,1,2), weight=1)
        self.lcnc = os.path.expanduser('~/linuxcnc')
        if 'root' in self.lcnc:
            title = 'User Error'
            msg = ['plasmac2 setup can not be run as a root user']
            self.myMsg(title, '\n'.join(msg), 1)
            raise SystemExit
        if not os.path.isdir(self.lcnc):
            title = 'Directory Error'
            msg = ['The directory ~/linuxcnc does not exist']
            msg.append('It needs to be created by LinuxCNC')
            msg.append('to ensure that the structure is correct')
            self.myMsg(title, '\n'.join(msg), 1)
            raise SystemExit
        self.configs = os.path.join(self.lcnc, 'configs')
        self.b2tf = os.path.dirname(os.path.realpath(sys.argv[0]))
        try:
            repo = git.Repo(os.path.join(self.b2tf, '../'))
        except:
            title = 'Repository Error'
            msg = ' is not a git repository'
            self.myMsg(title, os.path.join(self.b2tf, '../') + msg, 1)
            raise SystemExit
        self.reply = [False, None]

    def migrate(self):
        ini = filedialog.askopenfilename(
            title='QtPlasmaC INI File',
            initialdir=self.configs,
            filetypes=(('ini files', '*.ini'),))
        if not ini:
            return
        iniFile = os.path.basename(ini)
        oldDir = os.path.dirname(ini)
        newDir = oldDir + '_plasmac2'
        newIni = os.path.join(newDir, iniFile)
        if os.path.exists(newDir):
            title = 'Directory Exists'
            msg = [newDir]
            msg.append('already exists')
            msg.append('\n\n')
            msg.append('Overwrite?')
            self.reply[0] = False
            self.myMsg(title, ' '.join(msg), 2)
            if not self.reply[0]:
                return
            if os.path.isfile(newDir) or os.path.islink(newDir):
                os.remove(newDir)
            elif os.path.isdir(newDir):
                rmtree(newDir)
        try:
            ignores = ignore_patterns('qtplasmac','backups','machine_log*.txt', \
                                      '*.qss','*.py','*.bak','qtvcp.prefs','M190')
            copytree(oldDir, newDir, ignore=ignores)
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
                    config[lNum] = 'USER_M_PATH = ./plasmac2:{}\n'.format(mPath)
                    done.append('u')
            for option in ['u']:
                if option == 'u' and option not in done:
                    config.insert(insert,'USER_M_PATH = ./plasmac2:./\n')
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
            qtplasmacHal = []
            for lNum in range(config.index('[HAL]\n') + 1, len(config)):
                if config[lNum].startswith('['):
                    break
                section[lNum] = config[lNum]
            for lNum in section:
                if section[lNum].startswith('HALFILE') or section[lNum].startswith('POSTGUI_HALFILE'):
                    halFileRaw = config[lNum].split('=')[1].strip()
                    halFile = os.path.realpath(os.path.join(oldDir, halFileRaw))
                    # if existing config is a sim
                    if 'sim_postgui' in halFile:
                        sim = True
                        config[lNum] = ''
                    elif 'sim_no_stepgen.tcl' in halFile:
                        config[lNum] = 'HALFILE                 = ./plasmac2/sim/sim_no_stepgen.tcl\n'
                        sim = True
                    elif 'sim_stepgen.tcl' in halFile:
                        config[lNum] = 'HALFILE                 = ./plasmac2/sim/sim_stepgen.tcl\n'
                        sim = True
                    elif 'qtplasmac_comp.hal' not in halFile:
                        if not os.path.dirname(halFile):
                            halFile = os.path.join(newDir, halFile)
                        # check for references to qtplasmac
                        with open(halFile, 'r') as halRead:
                            if 'qtplasmac' in halRead.read():
                                qtplasmacHal.append(config[lNum].strip())
                                config[lNum] = '#{}'.format(config[lNum])
            # add sim panel if required
            if sim:
                config.insert(0, '[APPLICATIONS]\n' \
                                'DELAY = 2\n' \
                                'APP = ./plasmac2/sim/sim_panel.py\n\n')
            # write the ini file
            with open(newIni, 'w') as outFile:
                for line in config:
                    outFile.write(line)
            # remove any existing plasmac2
            if os.path.islink(os.path.join(newDir, 'plasmac2')):
                os.remove(os.path.join(newDir, 'plasmac2'))
            elif os.path.exists(os.path.join(newDir, 'plasmac2')):
                os.remove(os.path.join(newDir, 'plasmac2'))
            # create a link to plasmac2
            os.symlink(os.path.join(self.b2tf), os.path.join(newDir, 'plasmac2'))
            # copy user custom files
            self.copy_custom_files(newDir)
            # we made it...
            title = 'Migration Complete'
            msg = ['Ini file for plasmac2 config is:']
            msg.append(os.path.join(newDir, iniFile))
            if qtplasmacHal:
                msg.append('\n\n')
                msg.append('\nThe following hal files contain references to qtplasmac and were commented out in the ini file')
                for file in qtplasmacHal:
                    msg.append('\n\n{}'.format(file.split('=')[1].strip()))
                msg.append('\n\nIf the files are required then you will need to edit them to suit this config then uncomment them')
        except Exception as e:
            title = 'Migration error'
            msg = ['Migration was unsuccessful']
            msg.append('\n\n')
            msg.append('Error in line: {}\n'.format(sys.exc_info()[-1].tb_lineno))
            msg.append(str(e))
        self.myMsg(title, ' '.join(msg), 1)

    def sim(self):
        title = 'Create A Sim'
        msg = ['Name:']
        self.reply[0] = False
        self.myMsg(title, msg, 2, 'left', 'sim')
        # cancel clicked
        if not self.reply[0]:
            return
        simName = self.reply[1][0]
        if not simName:
            title = 'Name Error'
            msg = ['A name is required for the sim']
            self.myMsg(title, '\n'.join(msg), 1)
            return
        simUnits = self.reply[1][1]
        safe = 0.01 if simUnits == 'metric' else 0.001
        try:
            simX = float(self.reply[1][2]) + safe
        except:
            simX = 1200.01 if simUnits == 'metric' else 48.001
        try:
            simY = float(self.reply[1][3]) + safe
        except:
            simY = 1200.01 if simUnits == 'metric' else 48.001
        try:
            simZ = float(self.reply[1][4]) + safe
        except:
            simZ = 100.01 if simUnits == 'metric' else 4.001
        if not simName:
            title = 'Name Error'
            msg = ['Name is required for sim']
            self.myMsg(title, '\n'.join(msg), 1)
            return
        simDir = os.path.join(self.configs, simName)
        if os.path.exists(simDir):
            title = 'Directory Exists'
            msg = [simDir]
            msg.append('already exists')
            msg.append('\n\n')
            msg.append('Overwrite?')
            self.reply[0] = False
            self.myMsg(title, ' '.join(msg), 2)
            if not self.reply[0]:
                return
        else:
            os.mkdir(simDir)
        for file in ['custom.hal', 'sim_no_stepgen.tcl', 'sim_panel.py', 'sim_stepgen.tcl', \
                     'user_commands.py', 'user_hal.py', 'user_periodic.py']:
            copy(os.path.join(self.b2tf, 'sim', file), os.path.join(simDir, file))
        for file in ['{}.ini'.format(simUnits), '{}_material.cfg'.format(simUnits), \
                     '{}.prefs'.format(simUnits), '{}_tool.tbl'.format(simUnits)]:
            copy(os.path.join(self.b2tf, 'sim', file), os.path.join(simDir, file.replace(simUnits, simName)))
        with open(os.path.join(simDir, '{}.ini'.format(simName)), 'r') as inFile:
            ini = inFile.readlines()
        index = 0
        with open(os.path.join(simDir, '{}.ini'.format(simName)), 'w') as outFile:
            for line in ini:
                if line.startswith('PARAMETER_FILE'):
                    line = 'PARAMETER_FILE          = parameters.txt\n'
                elif line.startswith('MDI_HISTORY_FILE'):
                    line = 'MDI_HISTORY_FILE        = mdi_history.txt\n'
                elif line.startswith('MACHINE'):
                    line = 'MACHINE                 = {}\n'.format(simName)
                elif line.startswith('TOOL_TABLE'):
                    line = 'TOOL_TABLE              = {}_tool.tbl\n'.format(simName)
                elif line.startswith('POSITION_FILE'):
                    line = 'POSITION_FILE           = position.txt\n'
                elif line.startswith('[AXIS_'):
                    index += 1
                elif line.startswith('MAX_LIMIT'):
                    if index == 1:
                        line = 'MAX_LIMIT               = {}\n'.format(simX)
                    elif index == 2:
                        line = 'MAX_LIMIT               = {}\n'.format(simY)
                    elif index == 3:
                        line = 'MAX_LIMIT               = {}\n'.format(simZ)
                elif line.startswith('HOME ') and index == 3:
                    if simUnits == 'metric':
                        line = 'HOME                    = {}\n'.format(simZ - 5)
                    else:
                        line = 'HOME                    = {}\n'.format(simZ - 0.2)
                elif line.startswith('HOME_OFFSET') and index == 3:
                    line = 'HOME_OFFSET             = {}\n'.format(simZ)
                outFile.write(line)
        # remove any existing plasmac2
        if os.path.islink(os.path.join(simDir, 'plasmac2')):
            os.remove(os.path.join(simDir, 'plasmac2'))
        elif os.path.exists(os.path.join(simDir, 'plasmac2')):
            os.remove(os.path.join(simDir, 'plasmac2'))
        # copy user custom files
        self.copy_custom_files(simDir)
        # create a link to plasmac2
        os.symlink(os.path.join(self.b2tf), os.path.join(simDir, 'plasmac2'))
        title = 'Sim Creation Complete'
        msg = ['Ini file for {} sim config is: {}'.format(simUnits, os.path.join(simDir, simName))]
        msg.append('X={}   Y={}   Z={}'.format(simX, simY, simZ))
        self.myMsg(title, '\n\n'.join(msg), 1)

    def copy_custom_files(self, dir):
        for f in ['commands', 'hal', 'periodic']:
            src = os.path.join(self.b2tf, 'sim', 'user_{}.py'.format(f))
            copy(src, os.path.join(dir, '.'))

    def myMsg(self, title, text, buttons=1, justify='center', entry=False):
        reply = self.msgBox(title, text, buttons, justify, entry)
        root.wait_window(self.pop)
        return reply

    def msgBox(self, title, text, numButtons=1, justify='center', entry=False):

        def action(reply, entry=None):
            self.reply = [reply, entry]
            self.pop.destroy()

        self.pop = Toplevel(root)
        self.pop.title(title)
        self.pop.resizable(False, False)
        self.pop.transient(self.master)
        self.pop.protocol("WM_DELETE_WINDOW", self.disable_close)
        self.pop.grab_set()
        label = Label(self.pop, text=text, justify=justify)
        enter = Entry(self.pop, width=20, justify='right')
        units = Frame(self.pop)
        self.units = StringVar(root, 'metric')
        self.metric = Radiobutton(units, text='Metric', variable=self.units, value='metric')
        self.inch = Radiobutton(units, text=('Inch'), variable=self.units, value='imperial')
        xL = Label(self.pop, text='X Length:')
        x = Entry(self.pop, width=20, justify='right')
        yL = Label(self.pop, text='Y Length:')
        y = Entry(self.pop, width=20, justify='right')
        zH = Label(self.pop, text='Z Height:')
        z = Entry(self.pop, width=20, justify='right')
        buttons = Frame(self.pop, relief='raised')
        ok = Button(buttons, text='OK', width=6, command=lambda:action(True, [enter.get(), self.units.get(), x.get(), y.get(), z.get()]))
        no = Button(buttons, text='Cancel', width=6, command=lambda:action(False))
        if entry:
            label.grid(row=0, column=0, sticky='e', padx=(8,0), pady=(8,0))
            enter.grid(row=0, column=1, padx=(0,8), pady=(8,0))
            enter.focus_set()
        else:
            label.grid(row=0, column=0, columnspan=2, padx=8, pady=(8,0))
        if entry == 'sim':
            self.metric.grid(row=0, column=1)
            self.inch.grid(row=0, column=2)
            units.grid(row=2, column=1, columnspan=2, padx=(0,8))
            xL.grid(row=3, column=0, padx=(8,0))
            x.grid(row=3, column=1, padx=(0,8))
            yL.grid(row=4, column=0, padx=(8,0))
            y.grid(row=4, column=1, padx=(0,8))
            zH.grid(row=5, column=0, padx=(8,0))
            z.grid(row=5, column=1, padx=(0,8))
        if numButtons > 1:
            ok.grid(row=0, column=0, sticky='w', padx=(8,0))
            no.grid(row=0, column=1, sticky='e', padx=(0,8))
            buttons.columnconfigure((0,1), weight=1)
        else:
            ok.grid(row=0, column=0)
            buttons.columnconfigure(0, weight=1)
        buttons.grid(row=6, column=0, columnspan=2, sticky='we', pady=(16,8))

    # dummy so we can't close msgBox from the window close icon
    def disable_close(self):
        pass

    def shutdown(self):
        raise SystemExit

root = Tk()
my_gui = Setup(root)
root.mainloop()
