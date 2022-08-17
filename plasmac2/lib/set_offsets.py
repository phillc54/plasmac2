'''
set_offsets.py

Copyright (C) 2020, 2021  Phillip A Carter
Copyright (C) 2020, 2021  Gregory D Carl

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

import os, sys
import gettext
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from importlib import reload
from shutil import copy as COPY

for f in sys.path:
    if '/lib/python' in f:
        if '/usr' in f:
            localeDir = 'usr/share/locale'
        else:
            localeDir = os.path.join('{}'.format(f.split('/lib')[0]),'share','locale')
        break
gettext.install("linuxcnc", localedir=localeDir)

def offsets_show(s, c, PREF, putPrefs, laserOffsets, laser_button_enable, comp, toolFile, probeOffsets, set_probe_offset_pins):
    window = Tk()
    window.title('Set Peripheral Offsets')
    window.resizable(False,False)
    window.attributes('-topmost', True)
    text = [_('Usage is as follows') + ':\n']
    text.append(_('1. Touchoff the torch to X0 Y0'))
    text.append(_('2. Mark the material with a torch pulse'))
    text.append(_('3. Jog until the peripheral is close to the mark'))
    text.append(_('4. Click the appropriate button to activate the peripheral'))
    text.append(_('5. Jog until the peripheral is centered on the mark'))
    text.append(_('6. Click the Get Offsets button to get the offsets'))
    text.append(_('7. Confirm whether or not to change the offsets'))
    info = Label(window, text="\n".join(text), justify='left')
    buttons = Frame(window, relief='groove')
    laser = Button(buttons, text=_('Laser'), width=12, padx=0, \
            command=lambda:laser_clicked(widgets, s, PREF, putPrefs, laserOffsets, laser_button_enable, comp))
    scribe = Button(buttons, text=_('Scribe'), width=12, padx=0, \
             command=lambda:scribe_clicked(widgets, s, c, toolFile, comp))
    probe = Button(buttons, text=_('Offset Probe'), width=12, padx=0, \
            command=lambda:probe_clicked(widgets, s, PREF, putPrefs, probeOffsets, set_probe_offset_pins, comp))
    cancel = Button(buttons, text=_('Exit'), width=12, padx=0, \
            command=lambda:cancel_clicked(widgets, comp))
    laser.grid(column=0, row=0, padx=(4,0))
    scribe.grid(column=1, row=0, padx=(4,0))
    probe.grid(column=2, row=0, padx=(4,0))
    cancel.grid(column=3, row=0, padx=(4,4))
    info.pack(pady=8)
    buttons.pack(pady=4)
    widgets = {'window':window, 'laser':laser, 'scribe':scribe, 'probe':probe}
    window.mainloop()

def cancel_clicked(widgets, comp):
    comp['laser-on'] = False
    comp['offset-set-probe'] = False
    comp['offset-set-scribe'] = False
    widgets['window'].destroy()

def laser_clicked(widgets, s, PREF, putPrefs, laserOffsets, laser_button_enable, comp):
    if widgets['laser']['text'] == 'Laser':
        widgets['window'].title('Set Laser Offsets')
        widgets['laser']['text'] = 'Get Offsets'
        widgets['scribe'].grid_forget()
        widgets['probe'].grid_forget()
        comp['laser-on'] = True
        return
    newOffsets = {'X':round(s.position[0] - s.g5x_offset[0] - s.g92_offset[0], 4) + 0, \
                  'Y':round(s.position[1] - s.g5x_offset[1] - s.g92_offset[1], 4) + 0}
    if offset_prompt(widgets, laserOffsets, newOffsets):
        laserOffsets['X'] = newOffsets['X']
        laserOffsets['Y'] = newOffsets['Y']
        putPrefs(PREF,'LASER_OFFSET', 'X axis', laserOffsets['X'], float)
        putPrefs(PREF,'LASER_OFFSET', 'Y axis', laserOffsets['Y'], float)
        laser_button_enable()
        comp['laser-on'] = False
        title = _('Laser Offsets')
        msg = _('Laser offsets have been saved')
        messagebox.showinfo(title, msg, parent=widgets['window'])
        widgets['window'].destroy()
    else:
        widgets['window'].title('Set Peripheral Offsets')
        widgets['laser']['text'] = 'Laser'
        widgets['scribe'].grid(column=1, row=0, padx=(4,0))
        widgets['probe'].grid(column=2, row=0, padx=(4,0))
        comp['laser-on'] = False

def scribe_clicked(widgets, s, c, toolFile, comp):
    try:
        scribeOffsets = {'X': 0, 'Y': 0}
        tool = []
        with open(toolFile, 'r') as inFile:
            for line in inFile:
                if line.startswith('T1'):
                    tool = line.split()
                    inFile.close()
                    break
        if tool:
            for item in tool:
                if item.startswith('X'):
                    scribeOffsets['X'] = float(item.replace('X','').replace('+',''))
                elif item.startswith('Y'):
                    scribeOffsets['Y'] = float(item.replace('Y','').replace('+',''))
    except:
        title = _('Tool File Error')
        msg = _('Could not get current scribe offsets from tooltable')
        messagebox.showerror(title, msg, parent=widgets['window'])
        return
    if widgets['scribe']['text'] == 'Scribe':
        widgets['window'].title('Set Scribe Offsets')
        widgets['scribe']['text'] = 'Get Offsets'
        widgets['laser'].grid_forget()
        widgets['probe'].grid_forget()
        comp['offset-set-scribe'] = True
        return
    newOffsets = {'X':round(s.position[0] - s.g5x_offset[0] - s.g92_offset[0], 4) + 0, \
                  'Y':round(s.position[1] - s.g5x_offset[1] - s.g92_offset[1], 4) + 0}
    if offset_prompt(widgets, scribeOffsets, newOffsets):
        scribeOffsets['X'] = newOffsets['X']
        scribeOffsets['Y'] = newOffsets['Y']
        write_scribe_offsets(toolFile, scribeOffsets)
        c.load_tool_table()
        comp['offset-set-scribe'] = False
        title = _('Scribe Offsets')
        msg = _('Scribe offsets have been saved')
        messagebox.showinfo(title, msg, parent=widgets['window'])
        widgets['window'].destroy()
    else:
        widgets['window'].title('Set Peripheral Offsets')
        widgets['scribe']['text'] = 'Scribe'
        widgets['laser'].grid(column=0, row=0, padx=(4,0))
        widgets['probe'].grid(column=2, row=0, padx=(4,0))
        comp['offset-set-scribe'] = False

def probe_clicked(widgets, s, PREF, putPrefs, probeOffsets, set_probe_offset_pins, comp):
    if widgets['probe']['text'] == 'Offset Probe':
        widgets['window'].title('Set Probe Offsets')
        widgets['probe']['text'] = 'Get Offsets'
        widgets['laser'].grid_forget()
        widgets['scribe'].grid_forget()
        comp['offset-set-probe'] = True
        return
    title = _('Offset Probe Delay')
    prompt = _('Delay (Seconds)')
    delay = simpledialog.askfloat(title, prompt, initialvalue=0.0, parent=widgets['window'])
    newOffsets = {'X':round(s.position[0] - s.g5x_offset[0] - s.g92_offset[0], 4) + 0, \
                  'Y':round(s.position[1] - s.g5x_offset[1] - s.g92_offset[1], 4) + 0, \
                  'Delay':delay}
    if delay != None and offset_prompt(widgets, probeOffsets, newOffsets, True):
        probeOffsets['X'] = newOffsets['X']
        probeOffsets['Y'] = newOffsets['Y']
        probeOffsets['Delay'] = newOffsets['Delay']
        putPrefs(PREF,'OFFSET_PROBING', 'X axis', probeOffsets['X'], float)
        putPrefs(PREF,'OFFSET_PROBING', 'Y axis', probeOffsets['Y'], float)
        putPrefs(PREF,'OFFSET_PROBING', 'Delay', probeOffsets['Delay'], float)
        set_probe_offset_pins()
        comp['offset-set-probe'] = False
        title = _('Probe Offsets')
        msg = _('Probe offsets have been saved')
        messagebox.showinfo(title, msg, parent=widgets['window'])
        widgets['window'].destroy()
    else:
        widgets['window'].title('Set Peripheral Offsets')
        widgets['probe']['text'] = 'Offset Probe'
        widgets['laser'].grid(column=0, row=0, padx=(4,0))
        widgets['scribe'].grid(column=1, row=0, padx=(4,0))
        comp['offset-set-probe'] = False

def offset_prompt(widgets, oldOffsets, newOffsets, probe=False):
    title = _('Offset Change')
    prompt  = _('Change offsets from')
    if probe:
        prompt += ':\nX:{:0.3f}  Y:{:0.3f}  Delay:{:0.2f}\n\n'.format(oldOffsets['X'], oldOffsets['Y'], oldOffsets['Delay'])
    else:
        prompt += ':\nX:{:0.3f}  Y:{:0.3f}\n\n'.format(oldOffsets['X'], oldOffsets['Y'])
    prompt += _('To')
    if probe:
        prompt += ':\nX:{:0.3f}  Y:{:0.3f}  Delay:{:0.2f}\n'.format(newOffsets['X'], newOffsets['Y'], newOffsets['Delay'])
    else:
        prompt += ':\nX:{:0.3f}  Y:{:0.3f}\n'.format(newOffsets['X'], newOffsets['Y'])
    return messagebox.askyesno(title, prompt, parent=widgets['window'])

def write_scribe_offsets(toolFile, offsets):
    written = False
    COPY(toolFile, '{}~'.format(toolFile))
    with open('{}~'.format(toolFile), 'r') as inFile:
        with open(toolFile, 'w') as outFile:
            for line in inFile:
                if line.startswith('T1'):
                    outFile.write('T1 P1 X{:0.3f} Y{:0.3f} ;scribe\n'.format(offsets['X'], offsets['Y']))
                    written = True
                else:
                    outFile.write(line)
            if not written:
                outFile.write('T1 P1 X{:0.3f} Y{:0.3f} ;scribe\n'.format(offsets['X'], offsets['Y']))
    os.remove('{}~'.format(toolFile))
