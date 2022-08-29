'''
plasmac2 is an add-on to the LinuxCNC Axis GUI for creating
a plasma cutting configuration using the plasmac component

plasmac2 makes use of code from the LinuxCNC project:
http://linuxcnc.org & https://github.com/linuxcnc

Copyright (C) 2022  Phillip A Carter
Copyright (C) 2022  Gregory D Carl

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


##############################################################################
# NEW CLASSES                                                                #
##############################################################################
# class for preferences file
prefP = configparser.ConfigParser
class plasmacPreferences(prefP):
    optionxform = str
    types = {bool: prefP.getboolean,
             float: prefP.getfloat,
             int: prefP.getint,
             str: prefP.get,
             repr: lambda self, section, option: eval(prefP.get(self, section, option)),
            }

    def __init__(self):
        prefP.__init__(self, strict=False, interpolation=None)
        self.fn = os.path.join(configPath, '{}.prefs'.format(vars.machine.get()))
        self.read(self.fn)

# class for materials file
matsP = configparser.ConfigParser
class plasmacMaterials(matsP):
    optionxform = str
    types = {bool: matsP.getboolean,
             float: matsP.getfloat,
             int: matsP.getint,
             str: matsP.get,
             repr: lambda self, section, option: eval(matsP.get(self, section, option)),
            }

    def __init__(self):
        matsP.__init__(self)
        self.fn = os.path.join(configPath, '{}_material.cfg'.format(vars.machine.get()))
        self.read(self.fn)

# class for temp materials file
tempP = configparser.ConfigParser
class plasmacTempMaterial(tempP):
    optionxform = str
    types = {bool: tempP.getboolean,
             float: tempP.getfloat,
             int: tempP.getint,
             str: tempP.get,
             repr: lambda self,section, option: eval(tempP.get(self, section, option)),
            }

    def __init__(self):
        tempP.__init__(self)
        self.fn = os.path.join(tmpPath, '{}_material.gcode'.format(vars.machine.get()))
        self.read(self.fn)


##############################################################################
# PREFERENCE FUNCTIONS                                                       #
##############################################################################
def getPrefs(prefs, section, option, default=False, type=bool):
    m = prefs.types.get(type)
    if prefs.has_section(section):
        if prefs.has_option(section, option):
            return m(prefs, section, option)
        else:
            prefs.set(section, option, str(default))
            prefs.write(open(prefs.fn, 'w'))
            return default
    else:
        prefs.add_section(section)
        prefs.set(section, option, str(default))
        prefs.write(open(prefs.fn, 'w'))
        return default

def putPrefs(prefs, section, option, value, type=bool):
    if prefs.has_section(section):
        prefs.set(section, option, str(type(value)))
        prefs.write(open(prefs.fn, 'w'))
    else:
        prefs.add_section(section)
        prefs.set(section.upper(), option, str(type(value)))
        prefs.write(open(prefs.fn, 'w'))

def removePrefsSect(prefs, section):
    prefs.remove_section(section)
    prefs.write(open(prefs.fn, 'w'))

def sortPrefs(prefs):
    prefs._sections = OrderedDict(sorted(prefs._sections.items(), key=lambda t: int(t[0].rsplit('_',1)[1]) ))
    prefs.write(open(prefs.fn, 'w'))


##############################################################################
# WINDOW FUNCTIONS                                                           #
##############################################################################
def mode_changed():
    if pVars.plasmacMode.get() == 2:
        rC('grid','forget',foverride)
        rC('grid','forget',fplasma + '.arcvl')
        rC('grid','forget',fplasma + '.arc-voltage')
        rC('grid','forget',fleds + '.led-kerf-locked')
        rC('grid','forget',fleds + '.lKLlab')
        rC('grid','forget','.runs.check.av')
        rC('grid','forget','.runs.check.avL')
        rC('grid','forget',fparam + '.c2.thc.thc-delay')
        rC('grid','forget',fparam + '.c2.thc.thc-delayL')
        rC('grid','forget',fparam + '.c2.thc.thc-threshold')
        rC('grid','forget',fparam + '.c2.thc.thc-thresholdL')
        rC('grid','forget',fparam + '.c2.thc.pid-i-gain')
        rC('grid','forget',fparam + '.c2.thc.pid-i-gainL')
        rC('grid','forget',fparam + '.c2.thc.pid-d-gain')
        rC('grid','forget',fparam + '.c2.thc.pid-d-gainL')
        rC('grid','forget',fparam + '.c2.thc.kerfcross-override')
        rC('grid','forget',fparam + '.c2.thc.kerfcross-overrideL')
        rC('grid','forget',fparam + '.c3.arc.arc-voltage-scale')
        rC('grid','forget',fparam + '.c3.arc.arc-voltage-scaleL')
        rC('grid','forget',fparam + '.c3.arc.arc-voltage-offset')
        rC('grid','forget',fparam + '.c3.arc.arc-voltage-offsetL')
        rC('grid','forget',fparam + '.c3.arc.arc-ok-high')
        rC('grid','forget',fparam + '.c3.arc.arc-ok-highL')
        rC('grid','forget',fparam + '.c3.arc.arc-ok-low')
        rC('grid','forget',fparam + '.c3.arc.arc-ok-lowL')
    elif pVars.plasmacMode.get() == 1:
        rC('grid','forget',fparam + '.c3.arc.arc-ok-high')
        rC('grid','forget',fparam + '.c3.arc.arc-ok-highL')
        rC('grid','forget',fparam + '.c3.arc.arc-ok-low')
        rC('grid','forget',fparam + '.c3.arc.arc-ok-lowL')
    else:
        rC('grid',fparam + '.c3.arc.arc-ok-highL','-column',0,'-row',5,'-sticky','e')
        rC('grid',fparam + '.c3.arc.arc-ok-high','-column',1,'-row',5)
        rC('grid',fparam + '.c3.arc.arc-ok-lowL','-column',0,'-row',6,'-sticky','e')
        rC('grid',fparam + '.c3.arc.arc-ok-low','-column',1,'-row',6)
    if pVars.plasmacMode.get() < 2:
        rC('grid',foverride,'-column',0,'-row',3,'-padx',2,'-pady',(0,4),'-sticky','w')
        rC('grid',fplasma + '.arcvl','-column',0,'-row',0,'-sticky','nw')
        rC('grid',fplasma + '.arc-voltage','-column',0,'-row',1,'-sticky','se','-rowspan',2)
        rC('grid',fleds + '.led-kerf-locked','-column',4,'-row',3,'-padx',(4,0),'-pady',(4,0))
        rC('grid',fleds + '.lKLlab',         '-column',5,'-row',3,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
        rC('grid','.runs.check.av','-column',0,'-row',0,'-sticky','w')
        rC('grid','.runs.check.avL','-column',1,'-row',0,'-sticky','w')
        rC('grid',fparam + '.c2.thc.thc-delayL','-column',0,'-row',0,'-sticky','e')
        rC('grid',fparam + '.c2.thc.thc-delay','-column',1,'-row',0)
        rC('grid',fparam + '.c2.thc.thc-thresholdL','-column',0,'-row',1,'-sticky','e')
        rC('grid',fparam + '.c2.thc.thc-threshold','-column',1,'-row',1)
        rC('grid',fparam + '.c2.thc.pid-i-gainL','-column',0,'-row',3,'-sticky','e')
        rC('grid',fparam + '.c2.thc.pid-i-gain','-column',1,'-row',3)
        rC('grid',fparam + '.c2.thc.pid-d-gainL','-column',0,'-row',4,'-sticky','e')
        rC('grid',fparam + '.c2.thc.pid-d-gain','-column',1,'-row',4)
        rC('grid',fparam + '.c2.thc.kerfcross-overrideL','-column',0,'-row',6,'-sticky','e')
        rC('grid',fparam + '.c2.thc.kerfcross-override','-column',1,'-row',6)
        rC('grid',fparam + '.c3.arc.arc-voltage-scaleL','-column',0,'-row',3,'-sticky','e')
        rC('grid',fparam + '.c3.arc.arc-voltage-scale','-column',1,'-row',3)
        rC('grid',fparam + '.c3.arc.arc-voltage-offsetL','-column',0,'-row',4,'-sticky','e')
        rC('grid',fparam + '.c3.arc.arc-voltage-offset','-column',1,'-row',4)
    hal.set_p('plasmac.mode', str(pVars.plasmacMode.get()))

def cone_size_changed():
    o.set_cone_basesize(float(rC(fsetup + '.l.gui.cone','get')))

def font_size_changed():
    global fontName, fontSize, startFontSize
    fontName = 'sans'
    fontSize = pVars.fontSize.get()
    font = '{} {}'.format(fontName, fontSize)
    arcFont = '{} {}'.format(fontName, str(int(fontSize) * 3))
    ngcFont = str(int(fontSize) - 1)
    rC('font','configure','TkDefaultFont','-family', fontName, '-size', fontSize)
    rC(fplasma + '.arc-voltage','configure','-font',arcFont)
    rC('.pane.bottom.t.text','configure','-height',8,'-font',font, '-foreground',ourBlue)
    rC('.info.gcodef.gcodes','configure','-font',font)
    if s.paused:
        rC(ftabs,'itemconfigure','cutrecs','-text','Cut Recovery')
    else:
        rC(ftabs,'delete','manual',0)
        rC(ftabs,'delete','mdi',0)
        rC(ftabs,'insert','end','manual')
        rC(ftabs,'insert','end','mdi')
        rC(ftabs,'raise','manual')
        rC(ftabs,'itemconfigure','manual','-text','Manual')
        rC(ftabs,'itemconfigure','mdi','-text','MDI')
    rC(fright,'delete','preview',0)
    rC(fright,'delete','numbers',0)
    rC(fright,'delete','stats',0)
    rC(fright,'insert','end','preview')
    rC(fright,'insert','end','numbers')
    rC(fright,'insert','end','stats')
    rC(fright,'raise','preview')
    rC(fright,'itemconfigure','preview','-text',_('Preview'))
    rC(fright,'itemconfigure','numbers','-text',_('DRO'))
    rC(fright,'itemconfigure','stats','-text',_('Statistics'))
    rC(fright + '.fpreview','configure','-bd',2)
    rC(fright + '.fnumbers','configure','-bd',2)
    rC(fright + '.fstats','configure','-bd',2)
    for box in spinBoxes:
        rC(box,'configure','-font',fontName + ' ' + fontSize)
    ledFrame = int(fontSize) * 2
    ledSize = ledFrame - 2
    ledScale = int(fontSize) / int(startFontSize)
    startFontSize = fontSize
    for led in wLeds:
        rC(led,'configure','-width',ledFrame,'-height',ledFrame)
        rC(led,'scale',1,1,1,ledScale,ledScale)
    bSize = int(int(fontSize) / 10 * 24) if int(fontSize) > 10 else 24
    for w in toolButtons:
        rC('.toolbar.{}'.format(w),'configure','-width',bSize,'-height',bSize)
    for w in matButtons:
        rC('.toolmat.{}'.format(w),'configure','-width',bSize,'-height',bSize)

def close_window():
    if pVars.closeDialog.get():
        text1 = getPrefs(PREF,'GUI_OPTIONS', 'Exit warning text', '', str)
        text2 = _('Do you really want to close LinuxCNC?')
        text = '{}\n\n{}'.format(text1, text2)
        if rC('nf_dialog', '.error', _('Confirm Close'), text, 'warning', 1, _('Yes'), _('No')):
            return
    putPrefs(PREF,'GUI_OPTIONS', 'Window last', rC('winfo','geometry',root_window), str)
    if pVars.pmx485Enable.get():
        hal.set_p('pmx485.enable', '0')
    root_window.destroy()

def set_window_size():
    size = pVars.winSize.get()
    if size not in ['default', 'last', 'fullscreen', 'maximized']:
        title = _('WINDOW ERROR')
        msg0 = _('Invalid parameters in [GUI_OPTIONS]Window size in preferences file')
        notifications.add('error', '{}:\n{}\n'.format(title, msg0))
        return False
    else:
        if size == 'maximized':
            rC('wm','attributes','.','-fullscreen', 0)
            rC('wm','attributes','.','-zoomed',1)
        elif size == 'fullscreen':
            rC('wm','attributes','.','-zoomed', 0)
            rC('wm','attributes','.','-fullscreen',1)
        elif size == 'last':
            size = getPrefs(PREF,'GUI_OPTIONS', 'Window last', 'none', str)
            if size == 'none':
                size = 'default'
            else:
                rC('wm','attributes','.','-zoomed', 0)
                rC('wm','attributes','.','-fullscreen', 0)
                rC('wm','geometry','.',size)
        if size == 'default':
            rC('wm','attributes','.','-zoomed', 0)
            rC('wm','attributes','.','-fullscreen', 0)
            width = 1024
            height = 570
            rC('wm','geometry','.','{}x{}'.format(width, height))

            rC('tk::PlaceWindow','.')

def wcs_rotation(mode):
    global currentX, currentY, currentRot
    if mode == 'get':
        currentX = s.g5x_offset[0]
        currentY = s.g5x_offset[1]
        currentRot = s.rotation_xy
    elif mode == 'set':
        ensure_mode(linuxcnc.MODE_MDI)
        c.mdi('G10 L2 P0 X{} Y{} R{}'.format(currentX, currentY, currentRot))
        c.wait_complete()
        if currentRot != s.rotation_xy:
            reload_file()
        ensure_mode(linuxcnc.MODE_MANUAL)

def preview_toggle(conv=False):
    if pVars.previewLarge.get() or conv:
        rC('grid','forget','.fbuttons')
        rC('grid','forget','.pane.top.tabs')
        rC('grid','forget',ftop + '.feedoverride')
        rC('grid','forget',ftop + '.rapidoverride')
        rC('grid','forget',ftop + '.jogspeed')
        rC('grid','forget',ftop + '.ajogspeed')
        rC('.pane','forget','.pane.bottom')
        rC('grid','forget','.toolmat')
        rC('grid','forget','.runs')
    else:
        rC('grid','.fbuttons','-column',0,'-row',1,'-rowspan',2,'-sticky','nsew','-padx',0,'-pady',0)
        rC('grid','.pane.top.tabs','-column',0,'-row',1,'-sticky','nesw','-padx',2,'-pady',2)
        rC('grid','.pane.top.feedoverride','-column',0,'-row',2,'-sticky','new')
        rC('grid','.pane.top.rapidoverride','-column',0,'-row',3,'-sticky','new')
        rC('grid','.pane.top.jogspeed','-column',0,'-row',5,'-sticky','new')
        # test if we need the angular jog slider, 56==0x38==000111000==ABC
        if s.axis_mask & 56 == 0 and 'ANGULAR' in joint_type:
            rC('grid','.pane.top.ajogspeed','-column',0,'-row',6,'-sticky','new')
        rC('.pane','add','.pane.bottom','-sticky','nsew')
        rC('grid','.toolmat','-column',3,'-row',0,'-sticky','nesw')
        rC('grid','.runs','-column',3,'-row',1,'-rowspan',2,'-sticky','nsew','-padx',1,'-pady',1)

def setup_toggle(state):
    if int( state):
        hide_default()
        enable_menus(False)
        rC('grid','.toolsetup','-column',0,'-row',0,'-columnspan',3,'-sticky','nesw')
        rC('grid',fsetup,'-column',1,'-row',1,'-rowspan',2,'-sticky','nsew')
    else:
        rC('grid','forget','.toolsetup')
        rC('grid','forget',fsetup)
        show_default()

def param_toggle(state):
    if int(state):
        hide_default()
        enable_menus(False)
        rC('grid','.toolparam','-column',0,'-row',0,'-columnspan',3,'-sticky','nesw')
        rC('grid',fparam,'-column',1,'-row',1,'-rowspan',2,'-sticky','nsew')
    else:
        rC('grid','forget','.toolparam')
        rC('grid','forget',fparam)
        show_default()

def conv_toggle(state, convSent=False):
    global CONV, convFirstRun, preConvFile, loaded_file, lastViewType
    if int(state):
        lastViewType = get_view_type()
        preview_toggle(True)
        enable_menus(False)
        rC('grid','.toolconv','-column',0,'-row',0,'-columnspan',3,'-sticky','nesw')
        rC('grid','.fconv','-column',0,'-row',1,'-rowspan',2,'-sticky','nsew','-padx',(4,0),'-pady',(0,4))
        rC(fright,'itemconfigure','numbers','-state','disabled')
        rC(fright,'raise','preview')
        matIndex = rC('.runs.materials','getvalue')
        if comp['development']:
            reload(conversational)
        if convFirstRun or comp['development']:
            CONV = conversational.Conv(convFirstRun, root_window, widgets.toolFrame, \
                   widgets.convFrame, imagePath, tmpPath, pVars, unitsPerMm, comp, PREF, \
                   getPrefs, putPrefs, open_file_guts, wcs_rotation, conv_toggle)
            convFirstRun = False
        set_conv_preview()
        if loaded_file:
            COPY(loaded_file, preConvFile)
        CONV.start(materialFileDict, matIndex, vars.taskfile.get(), s.g5x_index, commands.set_view_z)
    else:
        preview_toggle()
        rC('grid','forget','.toolconv')
        rC('grid','forget','.fconv')
        show_default()
        rC(fright,'itemconfigure','numbers','-state','normal')
        reset_conv_preview()
        if convSent:
            loaded_file = vars.taskfile.get()
        else:
            if loaded_file:
                if 'shape.ngc' in loaded_file:
                    COPY(preConvFile, loaded_file)
                open_file_guts(loaded_file, True, False)
            else:
                clear_program()
        root_window.update_idletasks()
        if lastViewType == 'p':
            commands.set_view_p()
        elif lastViewType == 't':
            commands.set_view_t()
        else:
            commands.set_view_z()

def clear_program():
    file = os.path.join(tmpPath, 'clear.ngc')
    with open(file, 'w') as outFile:
        outFile.write('m2')
    open_file_guts(file, True, False)
    t.configure(state='normal')
    t.delete(0.0, 'end')
    t.configure(state='disabled')

def set_conv_preview():
    global convViewOptions
    convViewOptions['alpha'] = vars.program_alpha.get()
    convViewOptions['dtg'] = vars.show_distance_to_go.get()
    convViewOptions['extents'] = vars.show_extents.get()
    convViewOptions['limits'] = vars.show_machine_limits.get()
    convViewOptions['offsets'] = vars.show_offsets.get()
    convViewOptions['plot'] = vars.show_live_plot.get()
    convViewOptions['rapids'] = vars.show_rapids.get()
    convViewOptions['speed'] = vars.show_machine_speed.get()
    convViewOptions['tool'] = vars.show_tool.get()
    convViewOptions['cone'] = o.cone_basesize
    convViewOptions['origin'] = o.show_small_origin
    vars.program_alpha.set(False)
    vars.show_distance_to_go.set(False)
    vars.show_extents.set(True)
    vars.show_machine_limits.set(False)
    vars.show_offsets.set(False)
    vars.show_live_plot.set(False)
    vars.show_rapids.set(True)
    vars.show_machine_speed.set(False)
    vars.show_tool.set(False)
    o.cone_basesize = .025
    o.show_small_origin = False
    o.enable_dro = False
    o.set_view_z()

def reset_conv_preview():
    global convViewOptions
    vars.program_alpha.set(convViewOptions['alpha'])
    vars.show_distance_to_go.set(convViewOptions['dtg'])
    vars.show_extents.set(convViewOptions['extents'])
    vars.show_machine_limits.set(convViewOptions['limits'])
    vars.show_offsets.set(convViewOptions['offsets'])
    vars.show_live_plot.set(convViewOptions['plot'])
    vars.show_rapids.set(convViewOptions['rapids'])
    vars.show_machine_speed.set(convViewOptions['speed'])
    vars.show_tool.set(convViewOptions['tool'])
    o.cone_basesize = convViewOptions['cone']
    o.show_small_origin = convViewOptions['origin']
    o.enable_dro = True

def hide_default():
    rC('grid','forget','.pane')
    rC('grid','forget','.fbuttons')
    rC('grid','forget','.fconv')
    rC('grid','forget','.toolbar')
    rC('grid','forget','.toolmat')
    rC('grid','forget','.runs')

def show_default():
    rC('grid','.toolbar','-column',0,'-row',0,'-columnspan',3,'-sticky','nesw')
    rC('grid','.pane','-column',1,'-row',1,'-rowspan',2,'-sticky','nsew')
    if not pVars.previewLarge.get():
        rC('grid','.fbuttons','-column',0,'-row',1,'-rowspan',2,'-sticky','nsew','-padx',0,'-pady',0)
        rC('grid','.toolmat','-column',3,'-row',0,'-sticky','nesw')
        rC('grid','.runs','-column',3,'-row',1,'-rowspan',2,'-sticky','nsew','-padx',1,'-pady',1)
    enable_menus(True)

def enable_menus(state):
    state = 'normal' if state else 'disabled'
    menus = ['File', 'Machine', 'View', 'Conversational', 'Parameters', 'Setup', 'Help']
    for menu in menus:
        rC('.menu','entryconfig',menu,'-state',state)


##############################################################################
# TABLE VIEW FUNCTIONS                                                       #
##############################################################################
def open_file_name(f):
    open_file_guts(f)
    if str(widgets.view_z['relief']) == 'sunken':
        commands.set_view_z()
    elif str(widgets.view_t['relief']) == 'sunken':
        commands.set_view_t()
    else:
        commands.set_view_p()
    if o.canon is not None:
        x = (o.canon.min_extents[0] + o.canon.max_extents[0])/2
        y = (o.canon.min_extents[1] + o.canon.max_extents[1])/2
        z = (o.canon.min_extents[2] + o.canon.max_extents[2])/2
        o.set_centerpoint(x, y, z)

def gcode_properties(event=None, reply=None):
    props = {}
    if not loaded_file:
        props['name'] = _('No file loaded')
    else:
        ext = os.path.splitext(loaded_file)[1]
        program_filter = None
        if ext:
            program_filter = inifile.find('FILTER', ext[1:])
        name = os.path.basename(loaded_file)
        if program_filter:
            props['name'] = _('generated from %s') % name
        else:
            props['name'] = name
        size = os.stat(loaded_file).st_size
        lines = int(widgets.text.index('end').split('.')[0])-2
        props['size'] = _('%(size)s bytes\n%(lines)s gcode lines') % {'size': size, 'lines': lines}
        if vars.metric.get():
            conv = 1
            units = _('mm')
            fmt = '%.3f'
        else:
            conv = 1/25.4
            units = _('in')
            fmt = '%.4f'
        mf = vars.max_speed.get()
        g0 = sum(dist(l[1][:3], l[2][:3]) for l in o.canon.traverse)
        g1 = (sum(dist(l[1][:3], l[2][:3]) for l in o.canon.feed) +
              sum(dist(l[1][:3], l[2][:3]) for l in o.canon.arcfeed))
        gt = (sum(dist(l[1][:3], l[2][:3])/min(mf, l[3]) for l in o.canon.feed) +
              sum(dist(l[1][:3], l[2][:3])/min(mf, l[3])  for l in o.canon.arcfeed) +
              sum(dist(l[1][:3], l[2][:3])/mf  for l in o.canon.traverse) +
              o.canon.dwell_time)
        props['g0'] = '%f %s'.replace('%f', fmt) % (from_internal_linear_unit(g0, conv), units)
        props['g1'] = '%f %s'.replace('%f', fmt) % (from_internal_linear_unit(g1, conv), units)
        if gt > 120:
            props['run'] = _('%.1f minutes') % (gt/60)
        else:
            props['run'] = _('%d seconds') % (int(gt))
        min_extents = from_internal_units(o.canon.min_extents, conv)
        max_extents = from_internal_units(o.canon.max_extents, conv)
        for (i, c) in enumerate('xyz'):
            a = min_extents[i]
            b = max_extents[i]
            if a != b:
                props[c] = _('%(a)f to %(b)f = %(diff)f %(units)s').replace('%f', fmt) % {'a': a, 'b': b, 'diff': b-a, 'units': units}
        gcodeProperties = props
    if reply:
        return props
    properties(root_window, _('G-Code Properties'), property_names, props)

def get_view():
    x,y,z,p = 0,1,2,3
    if str(widgets.view_x['relief']) == "sunken":
        view = x
    elif (str(widgets.view_y['relief']) == "sunken" or
         str(widgets.view_y2['relief']) == "sunken"):
        view = y
    elif (str(widgets.view_z['relief']) == "sunken" or
          str(widgets.view_z2['relief']) == "sunken" or
          str(widgets.view_t['relief']) == "sunken"):
        view = z
    else:
        view = p
    return view

def set_view_z(event=None):
    widgets.view_z.configure(relief='sunken')
    widgets.view_z2.configure(relief="link")
    widgets.view_x.configure(relief="link")
    widgets.view_y.configure(relief="link")
    widgets.view_y2.configure(relief="link")
    widgets.view_t.configure(relief='link')
    widgets.view_p.configure(relief='link')
    vars.view_type.set(1)
    o.set_view_z()

def set_view_p(event=None):
    widgets.view_z.configure(relief="link")
    widgets.view_z2.configure(relief="link")
    widgets.view_x.configure(relief="link")
    widgets.view_y.configure(relief="link")
    widgets.view_y2.configure(relief="link")
    widgets.view_t.configure(relief='link')
    widgets.view_p.configure(relief="sunken")
    vars.view_type.set(5)
    o.set_view_p()

def set_view_t(event=None, scale=None):
    zoomScale = scale if scale else float(rC(fsetup + '.l.gui.zoom','get'))
    widgets.view_z.configure(relief='link')
    widgets.view_z2.configure(relief="link")
    widgets.view_x.configure(relief="link")
    widgets.view_y.configure(relief="link")
    widgets.view_y2.configure(relief="link")
    widgets.view_t.configure(relief='sunken')
    widgets.view_p.configure(relief="link")
    vars.view_type.set(5)
    mult = 1/25.4 if s.linear_units == 1 else 1
    xLen = machineBounds['xLen'] * mult
    yLen = machineBounds['yLen'] * mult
    size = [xLen / zoomScale * 0.5, yLen / zoomScale * 0.5, 0]
    mid = [xLen * 0.5, yLen * 0.5, 0]
    o.reset()
    glTranslatef(-mid[0], -mid[1], -mid[2])
    o.set_eyepoint_from_extents(size[0], size[1])
    o.perspective = False
    o.lat = o.lon = 0
    glRotateScene(o, 1.0, mid[0], mid[1], mid[2], 0, 0, 0, 0)
    o._redraw()

def draw_grid():
    x,y,z,p = 0,1,2,3
    view = get_view()
    rotation = math.radians(s.rotation_xy % 90)
    permutations = [
            lambda x_y_z: (x_y_z[2], x_y_z[1], x_y_z[0]),  # YZ X
            lambda x_y_z1: (x_y_z1[2], x_y_z1[0], x_y_z1[1]),  # ZX Y
            lambda x_y_z2: (x_y_z2[0], x_y_z2[1], x_y_z2[2])]  # XY Z
    inverse_permutations = [
            lambda z_y_x: (z_y_x[2], z_y_x[1], z_y_x[0]),  # YZ X
            lambda z_x_y: (z_x_y[1], z_x_y[2], z_x_y[0]),  # ZX Y
            lambda x_y_z3: (x_y_z3[0], x_y_z3[1], x_y_z3[2])]  # XY Z
    o.draw_grid_permuted(rotation, permutations[2],
            inverse_permutations[2])

def get_view_type():
    if str(widgets.view_x['relief']) == "sunken":
        view = 'x'
    elif (str(widgets.view_y['relief']) == "sunken" or
         str(widgets.view_y2['relief']) == "sunken"):
        view = 'y'
    elif (str(widgets.view_z['relief']) == "sunken" or
          str(widgets.view_z2['relief']) == "sunken"):
        view = 'z'
    elif (str(widgets.view_t['relief']) == "sunken"):
        view = 't'
    else:
        view = 'p'
    return view


##############################################################################
# STATISTICS FUNCTIONS                                                       #
##############################################################################
def secs_to_hms(s):
    m, s = divmod(int(s), 60)
    h, m = divmod(m, 60)
    return '{:02.0f}:{:02.0f}:{:02.0f}'.format(h, m, s)

def hms_to_secs(hms):
    h, m, s = hms.split(':')
    return int(h)*3600 + int(m)*60 + int(s)

def save_total_stats():
    if hal.get_value('plasmac.torch-enable'):
        val = float(pVars.lengthT.get()[:len(pVars.lengthT.get()) - 1]) * statDivisor
        pVars.lengthS.set(val)
        putPrefs(PREF,'STATISTICS', 'Cut length', val, float)
        val = pVars.pierceT.get()
        pVars.pierceS.set(val)
        putPrefs(PREF,'STATISTICS', 'Pierce count', val, int)
        val = hms_to_secs(pVars.rapidT.get())
        pVars.rapidS.set(val)
        putPrefs(PREF,'STATISTICS', 'Rapid time', val, int)
        val = hms_to_secs(pVars.probeT.get())
        pVars.probeS.set(val)
        putPrefs(PREF,'STATISTICS', 'Probe time', val, int)
        val = hms_to_secs(pVars.torchT.get())
        pVars.torchS.set(val)
        putPrefs(PREF,'STATISTICS', 'Torch on time', val, int)
        val = hms_to_secs(pVars.cutT.get())
        pVars.cutS.set(val)
        putPrefs(PREF,'STATISTICS', 'Cut time', val, int)
        val = hms_to_secs(pVars.pausedT.get())
        pVars.pausedS.set(val)
        putPrefs(PREF,'STATISTICS', 'Paused time', val, int)
        val = hms_to_secs(pVars.runT.get())
        pVars.runS.set(val)
        putPrefs(PREF,'STATISTICS', 'Program run time', val, int)

def clear_job_stats():
    pVars.lengthJ.set('{:0.2f}{}'.format(0.00, statSuffix))
    pVars.pierceJ.set(0)
    pVars.rapidJ.set('00:00:00')
    pVars.probeJ.set('00:00:00')
    pVars.torchJ.set('00:00:00')
    pVars.cutJ.set('00:00:00')
    pVars.pausedJ.set('00:00:00')
    pVars.runJ.set('00:00:00')

def reset_all_stats(stat):
    if stat == 'length':
        pVars.lengthS.set(0)
        pVars.lengthJ.set('{:0.2f}{}'.format(0.00, statSuffix))
        pVars.lengthT.set('{:0.2f}{}'.format(0.00, statSuffix))
        putPrefs(PREF,'STATISTICS', 'Cut length', 0, float)
    elif stat == 'pierce':
        pVars.pierceS.set(0)
        pVars.pierceJ.set('0')
        pVars.pierceT.set('0')
        putPrefs(PREF,'STATISTICS', 'Pierce count', 0, int)
    elif stat == 'rapid':
        pVars.rapidS.set(0)
        pVars.rapidJ.set('00:00:00')
        pVars.rapidT.set('00:00:00')
        putPrefs(PREF,'STATISTICS', 'Rapid time', 0, int)
    elif stat == 'probe':
        pVars.probeS.set(0)
        pVars.probeJ.set('00:00:00')
        pVars.probeT.set('00:00:00')
        putPrefs(PREF,'STATISTICS', 'Probe time', 0, int)
    elif stat == 'torch':
        pVars.torchS.set(0)
        pVars.torchJ.set('00:00:00')
        pVars.torchT.set('00:00:00')
        putPrefs(PREF,'STATISTICS', 'Torch on time', 0, int)
    elif stat == 'cut':
        pVars.cutS.set(0)
        pVars.cutJ.set('00:00:00')
        pVars.cutT.set('00:00:00')
        putPrefs(PREF,'STATISTICS', 'Cut time', 0, int)
    elif stat == 'paused':
        pVars.pausedS.set(0)
        pVars.pausedJ.set('00:00:00')
        pVars.pausedT.set('00:00:00')
        putPrefs(PREF,'STATISTICS', 'Paused time', 0, int)
    elif stat == 'run':
        pVars.runS.set(0)
        pVars.runJ.set('00:00:00')
        pVars.runT.set('00:00:00')
        putPrefs(PREF,'STATISTICS', 'Program run time', 0, int)


##############################################################################
# PARAMETER FUNCTIONS                                                        #
##############################################################################
# set appropriate hal pin if parameter changed
def param_changed(widget, value):
    global widgetValues
    item = widget.rsplit('.',1)[1]
    if item in ['x-single-cut','y-single-cut']:
        return
    widgetValues[widget] = value
    if item == 'kerf-width':
        comp['kerf-width'] = value
    elif item == 'cut-amps':
        if pmx485['exists']:
            pmx485_current_changed(int(value))
    elif item == 'cut-mode':
        if pmx485['exists']:
            pmx485_mode_changed(int(value))
    elif item == 'gas-pressure':
        if pmx485['exists']:
            pmx485_pressure_changed(float(value))
    elif item == 'cut-speed':
        hal.set_p('plasmac.cut-feed-rate','{}'.format(value))
    else:
        hal.set_p('plasmac.{}'.format(item),'{}'.format(value))

def validate_spinbox(widget, spinType, resolution, value, original):
    dbPrint = True if (not firstRun and comp['development']) else False
    if value == '':
        if comp['development']: print('blank = still valid')
        return True
    minval = float(rC(widget,'cget','-from')) if spinType == 'flt' else int(rC(widget,'cget','-from'))
    maxval = float(rC(widget,'cget','-to')) if spinType == 'flt' else int(rC(widget,'cget','-to'))
    # a negative value if range min equals zero is invalid
    if value == '-' and minval >= 0:
        if dbPrint: print('cannot be less than zero = invalid')
        return False
    # a decimal point in an int is invalid
    if '.' in str(value) and spinType == 'int':
        if dbPrint: print('a decimal in an int = invalid')
        return False
    # more digits than the resolution of a float is invalid
    if '.' in str(value) and len(str(value).split('.')[1]) > int(resolution):
        # don't error on first run so we can import parameters from qtplasmac
        if dbPrint: print('float resolution too large = invalid')
        if not firstRun:
            return False
    # we cannot do math on "-", ".", or "-." but they are valid for a float
    if value == '.' or value == '-' or value == '-.':
        if dbPrint: print('illegal math = still valid')
        return True
    # if a float cannot be calculated from value then it is invalid
    # we won't change the hal pin yet
    try:
        v = float(value)
    except:
        if dbPrint: print('cannot calculate a float = invalid')
        return False
    # if value is too large it is invalid
    if v > maxval:
        if dbPrint: print('value out of bounds = invalid')
        return False
    # if value is too small it may be valid
    if v < minval or v > maxval:
        if dbPrint: print('value out of bounds = still valid')
        return True
    # must be a good number...
    if widget == fsetup + '.l.gui.zoom':
        commands.set_view_t(None, v)
    elif widget == fsetup + '.l.jog.speed':
        jog_default_changed(value)
    elif widget == fsetup + '.l.cr.speed':
        cut_rec_default_changed(value)
    else:
        param_changed(widget,value)
    if dbPrint: print('valid entry')
    return True

def load_param_clicked():
    for widget in cpList:
        try:
            # we bring in all parameters as floats so we can read QtPlasmaC parameters
            value = getPrefs(PREF,'PLASMA_PARAMETERS', str(widget[8]), widget[3], float)
        except:
            value = 0
            title = _('Parameter Error')
            msg = _('Invalid parameter for')
            messagebox.showerror(title, '{}:\n\n{}'.format(msg, widget[8]))
        # convert to int here if required
        value = value if widget[2] > 0 else int(value)
        rC(fparam + widget[0] + '.' + widget[1],'set',value)
        widgetValues[fparam + widget[0] + '.' + widget[1]] = value

def save_param_clicked():
    for widget in cpList:
        value = rC(fparam + widget[0] + '.' + widget[1],'get')
        if widget[2] > 0:
            putPrefs(PREF,'PLASMA_PARAMETERS', str(widget[8]), value, float)
        else:
            putPrefs(PREF,'PLASMA_PARAMETERS', str(widget[8]), value, int)

def load_setup_clicked():
    rC(fsetup + '.l.jog.speed','set',restoreSetup['jogSpeed'])
    jog_default_changed(restoreSetup['jogSpeed'])
    if pVars.plasmacMode.get() != restoreSetup['plasmacMode']:
        pVars.plasmacMode.set(restoreSetup['plasmacMode'])
        mode_changed()
    if pVars.winSize.get() != restoreSetup['winSize']:
        pVars.winSize.set(restoreSetup['winSize'])
        set_window_size()
    if pVars.fontSize.get() != restoreSetup['fontSize']:
        pVars.fontSize.set(restoreSetup['fontSize'])
        font_size_changed()
    if pVars.coneSize.get() != restoreSetup['coneSize']:
        pVars.coneSize.set(restoreSetup['coneSize'])
        cone_size_changed()
    if pVars.matDefault.get() != restoreSetup['matDefault']:
        pVars.matDefault.set(restoreSetup['matDefault'])
        display_selected_material(restoreSetup['matDefault'])
    if int(rC(fsetup + '.l.cr.speed','get')) == restoreSetup['crPercent']:
        rC(fcutrec + '.display.cut-rec-speed','set',restoreSetup['crPercent'])
    else:
        rC(fsetup + '.l.cr.speed','set',restoreSetup['crPercent'])
    pVars.closeDialog.set(restoreSetup['closeDialog'])
    rC(fsetup + '.l.gui.zoom','set',restoreSetup['tableZoom'])
    user_button_load()

def save_setup_clicked():
    if int(rC(fsetup + '.l.jog.speed','get')) < minJogSpeed:
        rC(fsetup + '.l.jog.speed','set',minJogSpeed)
    restoreSetup['jogSpeed'] = rC(fsetup + '.l.jog.speed','get')
    putPrefs(PREF,'GUI_OPTIONS', 'Jog speed', restoreSetup['jogSpeed'], int)
    restoreSetup['plasmacMode'] = pVars.plasmacMode.get()
    putPrefs(PREF,'GUI_OPTIONS', 'Mode', restoreSetup['plasmacMode'], int)
    restoreSetup['closeDialog'] = pVars.closeDialog.get()
    putPrefs(PREF,'GUI_OPTIONS', 'Exit warning', restoreSetup['closeDialog'], str)
    restoreSetup['winSize'] = pVars.winSize.get()
    putPrefs(PREF,'GUI_OPTIONS', 'Window size', restoreSetup['winSize'], str)
    restoreSetup['fontSize'] = pVars.fontSize.get()
    putPrefs(PREF,'GUI_OPTIONS', 'Font size', restoreSetup['fontSize'], str)
    restoreSetup['coneSize'] = pVars.coneSize.get()
    putPrefs(PREF,'GUI_OPTIONS', 'Preview cone size', restoreSetup['coneSize'], float)
    restoreSetup['tableZoom'] = float(rC(fsetup + '.l.gui.zoom','get'))
    putPrefs(PREF,'GUI_OPTIONS', 'Table zoom', restoreSetup['tableZoom'], float)
    restoreSetup['matDefault'] = pVars.matDefault.get()
    putPrefs(PREF,'GUI_OPTIONS', 'Default material', restoreSetup['matDefault'], int)
    restoreSetup['crPercent'] = rC(fsetup + '.l.cr.speed','get')
    putPrefs(PREF,'GUI_OPTIONS', 'Cut recovery speed %', restoreSetup['crPercent'], int)
    rC(fcutrec + '.display.cut-rec-speed','set',restoreSetup['crPercent'])
    user_button_save()


##############################################################################
# GENERAL FUNCTIONS                                                          #
##############################################################################
def thc_enable_toggled():
    hal.set_p('plasmac.thc-enable', str(pVars.thcEnable.get()))
    putPrefs(PREF,'ENABLE_OPTIONS','THC enable', pVars.thcEnable.get(), bool)

def corner_enable_toggled():
    hal.set_p('plasmac.cornerlock-enable', str(pVars.cornerEnable.get()))
    putPrefs(PREF,'ENABLE_OPTIONS','Corner lock enable', pVars.cornerEnable.get(), bool)

def kerf_enable_toggled():
    hal.set_p('plasmac.kerfcross-enable', str(pVars.kerfEnable.get()))
    putPrefs(PREF,'ENABLE_OPTIONS','Kerf cross enable', pVars.kerfEnable.get(), bool)

def auto_volts_toggled():
    hal.set_p('plasmac.use-auto-volts', str(pVars.autoVolts.get()))
    putPrefs(PREF,'ENABLE_OPTIONS', 'Use auto volts', pVars.autoVolts.get(), bool)

def ohmic_enable_toggled():
    hal.set_p('plasmac.ohmic-probe-enable', str(pVars.ohmicEnable.get()))
    putPrefs(PREF,'ENABLE_OPTIONS', 'Ohmic probe enable', pVars.ohmicEnable.get(), bool)

def ignore_arc_ok_toggled():
    hal.set_p('plasmac.ignore-arc-ok-1', str(pVars.ignorArcOk.get()))

def laser_button_enable():
    if laserOffsets['X'] or laserOffsets['Y']:
        rC('grid',fjogf + '.zerohome.laser','-column',3,'-row',0)
        rC('pack',fcutrecs + '.buttons.laser','-side','left')
    else:
        rC('pack','forget',fjogf + '.zerohome.laser')
        rC('pack','forget',fcutrecs + '.buttons.laser')

def set_probe_offset_pins():
    hal.set_p('plasmac.offset-probe-x', '{}'.format(probeOffsets['X']))
    hal.set_p('plasmac.offset-probe-y', '{}'.format(probeOffsets['Y']))
    hal.set_p('plasmac.offset-probe-delay', '{}'.format(probeOffsets['Delay']))

def set_peripheral_offsets():
    if comp['development']:
        reload(set_offsets)
    toolFile = os.path.realpath(tooltable)
    setup_toggle(False)
    set_offsets.offsets_show(s, c, PREF, putPrefs, laserOffsets, laser_button_enable, comp, toolFile, probeOffsets, set_probe_offset_pins)

def jog_default_changed(value):
    set_jog_slider(int(value) / (vars.max_speed.get() * 60))

def set_jog_slider(value):
    # jog slider value is from 0 to 1
    if not manualCut['state']:
        rC('set','jog_slider_val', value)
        rC('update_jog_slider_vel', value)

def tar_filter(tarinfo):
     if os.path.splitext(tarinfo.name)[1] in ['.pyc']:
          return None
     else:
          return tarinfo

def backup_clicked():
    n = time.gmtime()
    d = '{:02d}{:02d}{:02d}'.format(n.tm_year, n.tm_mon, n.tm_mday)
    t = '{:02d}{:02d}{:02d}'.format(n.tm_hour, n.tm_min, n.tm_sec)
    configDir = os.path.dirname(vars.emcini.get())
    outName = '{}_V{}_{}_{}.tar.gz'.format(vars.machine.get(), VER, d, t)
    outFile = os.path.join(os.path.expanduser('~'), outName)
    with tarfile.open(outFile, mode='w:gz', ) as archive:
        archive.add(configDir, filter=tar_filter)
    title = _('BACKUP')
    msg0 = _('A compressed backup of the machine configuration has been saved in your home directory')
    msg1 = _('The file name is')
    msg2 = _('This file may be attached to a post on the LinuxCNC forum to aid in problem solving')
#FIXME: TRY TO SET A MESSAGEBOX SIZE
#    rC('wm','geometry','[messagebox.showinfo(title, msg)]','600x100')
    messagebox.showinfo(title, '{}\n\n{}: {}\n\n{}\n'.format(msg0, msg1, outName, msg2))

def torch_enable():
    if hal.get_value('plasmac.torch-enable'):
        hal.set_p('plasmac.torch-enable','0')
        rC('.fbuttons.torch-enable','configure','-text',torchEnable['disabled'].replace('\\','\n'),'-bg',ourRed,'-activebackground',ourRed)
    else:
        hal.set_p('plasmac.torch-enable','1')
        rC('.fbuttons.torch-enable','configure','-text',torchEnable['enabled'].replace('\\','\n'),'-bg',ourGreen,'-activebackground',ourGreen)

#FIXME: KEEP THE PREVIEW UPDATING WHILE CODE IS BEING RUN
# this is a kludge, cannot Esc to abort...
# we probably don't need it, because we don't use it...
def update_preview(clear):
    c.wait_complete(.25)
    s.poll()
    while s.interp_state != linuxcnc.INTERP_IDLE:
        s.poll()
        o.tkRedraw()
        o.redraw_dro()
        o.update_idletasks()
        root_window.update_idletasks()
    if clear:
       live_plotter.clear()


##############################################################################
# JOINTS/AXES FUNCTIONS                                                      #
##############################################################################
def ja_button_setup(widget, button, text):
    rC('radiobutton', widget,'-value',button,'-text',text,'-anchor','center', \
       '-variable','ja_rbutton','-command','ja_button_activated','-padx',10,'-pady',6, \
       '-indicatoron',0,'-bd',2,'-highlightthickness',0,'-selectcolor',ourGreen)

def ja_button_activated():
    if vars.ja_rbutton.get() in 'xyzabcuvw':
        widget = getattr(widgets, 'axis_%s' % vars.ja_rbutton.get())
        widget.focus()
        rC(fjogf + '.zerohome.zero','configure','-text',_('Zero') + ' ' + vars.ja_rbutton.get().upper())
        if not homing_order_defined:
            widgets.homebutton.configure(text = _('Home') + ' ' + vars.ja_rbutton.get().upper() )
    else:
        widget = getattr(widgets, 'joint_%s' % vars.ja_rbutton.get())
        widget.focus()
    commands.axis_activated

def joint_mode_switch(a,b,c):
    if vars.motion_mode.get() == linuxcnc.TRAJ_MODE_FREE and s.kinematics_type != linuxcnc.KINEMATICS_IDENTITY:
        rC('grid','forget',fmanual + '.axes')
        rC('grid',fmanual + '.joints','-column','0','-row','0','-padx','2','-sticky','ew')
        widget = getattr(widgets, 'joint_%d' % 0)
        widget.focus()
        vars.ja_rbutton.set(0)
    else:
        rC('grid','forget',fmanual + '.joints')
        rC('grid',fmanual + '.axes','-column','0','-row','0','-padx','2','-sticky','ew')
        widget = getattr(widgets, 'axis_%s' % first_axis)
        widget.focus()
        vars.ja_rbutton.set(first_axis)


##############################################################################
# MANUAL CUT                                                                 #
##############################################################################
def manual_cut(event):
    global manualCut
    if manual_ok():
        if not hal.get_value('spindle.0.on'):
            c.spindle(linuxcnc.SPINDLE_FORWARD, 1)
            manualCut['feed'] = vars.jog_speed.get()
            vars.jog_speed.set(int(rC('.runs.material.cut-feed-rate','get')))
            manualCut['state'] = True
            rC('.pane.top.jogspeed.s','configure','-state','disabled')
            clear_job_stats()
        else:
            manualCut['state'] = False
            c.spindle(linuxcnc.SPINDLE_OFF)
            vars.jog_speed.set(manualCut['feed'])
            rC('.pane.top.jogspeed.s','configure','-state','normal')
            save_total_stats()


##############################################################################
# SINGLE CUT                                                                 #
##############################################################################
def single_cut():
    global result, singleCut
    result = False

    def cut_file(event):
        global result
        result = True
        sc.quit()

    def cancel_file(event):
        sc.quit()

    sc = Tkinter.Toplevel()
    sc.title(_('SINGLE CUT'))
    lbl1 = Tkinter.Label(sc, text=_('x-Length:'))
    lbl2 = Tkinter.Label(sc, text=_('y-Length:'))
    lbl3 = Tkinter.Label('')
    xLength = Tkinter.StringVar()
    xlength = Tkinter.Spinbox(sc, textvariable=xLength)
    yLength = Tkinter.StringVar()
    ylength = Tkinter.Spinbox(sc, textvariable=yLength)
    buttons = Tkinter.Frame(sc)
    buttonCut = Tkinter.Button(buttons, text=_('Load'), width=8)
    buttonCancel = Tkinter.Button(buttons, text=_('Cancel'), width=8)
    lbl1.grid(column=0, row=0, sticky='e')
    lbl2.grid(column=0, row=1, sticky='e')
    lbl3.grid(column=0, row=3, sticky='e')
    xlength.grid(column=1, row=0, sticky='w')
    ylength.grid(column=1, row=1, sticky='w')
    buttonCut.pack(side='left')
    buttonCancel.pack(side='right')
    buttons.grid(column=0, row=4, columnspan=2, sticky='ew')
    buttons.grid_columnconfigure(0, weight=1, uniform='group1')
    buttons.grid_columnconfigure(2, weight=1, uniform='group1')
    sc.grid_rowconfigure(0, weight=1, uniform='group2')
    sc.grid_rowconfigure(1, weight=1, uniform='group2')
    sc.grid_rowconfigure(2, weight=1, uniform='group2')
    sc.grid_rowconfigure(3, weight=1, uniform='group2')
    sc.grid_rowconfigure(4, weight=1, uniform='group2')
    xlength.config(width=10, from_=-9999, to=9999, increment=1, format='%0.0f', wrap=1)
    xLength.set(getPrefs(PREF,'SINGLE_CUT', 'x-length', 0, float))
    ylength.config(width=10, from_=-9999, to=9999, increment=1, format='%0.0f', wrap=1)
    yLength.set(getPrefs(PREF,'SINGLE_CUT', 'y-length', 0, float))
    buttonCut.bind('<Button-1>', cut_file)
    buttonCancel.bind('<Button-1>', cancel_file)
    Tkinter.mainloop()
    sc.destroy()
    if not result:
        return
    singleCut['state'] = True
    singleCut['G91'] = True if 910 in s.gcodes else False
    putPrefs(PREF,'SINGLE_CUT', 'X length', xLength.get(), float)
    putPrefs(PREF,'SINGLE_CUT', 'Y length', yLength.get(), float)
    xEnd = s.position[0] + float(xLength.get())
    yEnd = s.position[1] + float(yLength.get())
    scFile = os.path.join(tmpPath, 'single_cut.ngc')
    with open(scFile, 'w') as f:
        f.write('G90\n')
        f.write('F#<_hal[plasmac.cut-feed-rate]>\n')
        f.write('G53 G0 X{:0.6f} Y{:0.6f}\n'.format(s.position[0], s.position[1]))
        f.write('M3 $0 S1\n')
        f.write('G53 G1 X{:0.6f} Y{:0.6f}\n'.format(xEnd, yEnd))
        f.write('M5 $0\n')
        f.write('M2\n')
    if loaded_file != scFile:
        pVars.preRflFile.set(loaded_file)
    open_file_guts(scFile, False, False)


##############################################################################
# ALIGNMENT FUNCTIONS                                                        #
##############################################################################
def touch_off_xy(state, x, y):
    if state == '0' and isIdleHomed:
        if manual_ok():
            save_task_mode = s.task_mode
            ensure_mode(linuxcnc.MODE_MDI)
            c.mdi('G10 L20 P0 X{} Y{}'.format(x, y))
            c.wait_complete()
            s.poll()
            o.tkRedraw()
            reload_file(False)
            ensure_mode(save_task_mode)
            set_motion_teleop(1)
            o.redraw_dro()

def laser_button_toggled(state, button):
    global laserTimer, laserButtonState, laserText, laserOffsets
    global machineBounds, isIdleHomed
    title = _('LASER ERROR')
    if state == '1': # button pressed
        if s.paused and not hal.get_value('plasmac.laser-recovery-state'):
            xPos = s.position[0] + laserOffsets['X']
            yPos = s.position[1] + laserOffsets['Y']
            if xPos < machineBounds['X-'] or xPos > machineBounds['X+'] or yPos < machineBounds['Y-'] or yPos > machineBounds['Y+']:
                msg0 = _('Torch cannot move outside the machine boundary')
                notifications.add('error', '{}:\n{}'.format(title, msg0))
                return
            hal.set_p('plasmac.laser-x-offset', '{}'.format(str(int(laserOffsets['X'] / hal.get_value('plasmac.offset-scale')))))
            hal.set_p('plasmac.laser-y-offset', '{}'.format(str(int(laserOffsets['Y'] / hal.get_value('plasmac.offset-scale')))))
            hal.set_p('plasmac.laser-recovery-start', '1')
            hal.set_p('plasmac.cut-recovery', '1')
            comp['laser-on'] = 1
            return
        # long press timer
        elif isIdleHomed:
            laserTimer = 0.7
    else: # button released
        laserTimer = 0.0
        if not isIdleHomed:
            return
        xPos = s.position[0] - laserOffsets['X']
        yPos = s.position[1] - laserOffsets['Y']
        if xPos < machineBounds['X-'] or xPos > machineBounds['X+'] or yPos < machineBounds['Y-'] or yPos > machineBounds['Y+']:
            msg0 = _('Laser is outside the machine boundary')
            notifications.add('error', '{}:\n{}'.format(title, msg0))
            return
        if laserButtonState == 'reset':
            laserButtonState = 'laser'
            return
        elif laserButtonState == 'laser':
            pVars.laserText.set(_('Mark'))
            laserButtonState = 'markedge'
            comp['laser-on'] = 1
            return
        elif laserButtonState == 'setorigin':
            comp['laser-on'] = 0
        laserButtonState = sheet_align('laser', laserButtonState, laserOffsets['X'], laserOffsets['Y'])

def sheet_align(mode, buttonState, offsetX, offsetY):
    global relPos, startAlignPos
    msgList = []
    if buttonState == 'markedge':
#FIXME: NO CAMERA YET
#        zAngle = self.w.camview.rotation = 0
        ensure_mode(linuxcnc.MODE_MDI)
        c.mdi('G10 L2 P0 R0')
        c.wait_complete()
        live_plotter.clear()
        ensure_mode(linuxcnc.MODE_MANUAL)
#FIXME: NO CAMERA YET
#        self.w.cam_goto.setEnabled(False)
        pVars.laserText.set(_('Origin'))
        buttonState = 'setorigin'
        startAlignPos['X'] = relPos['X']
        startAlignPos['Y'] = relPos['Y']
    else:
        if mode == 'laser':
            pVars.laserText.set(_('Laser'))
            buttonState = 'laser'
        else:
            pVars.laserText.set(_('Mark'))
            buttonState = 'markedge'
        xDiff = relPos['X'] - startAlignPos['X']
        yDiff = relPos['Y'] - startAlignPos['Y']
        if xDiff and yDiff:
            zAngle = degrees(atan(yDiff / xDiff))
            if xDiff > 0:
                zAngle += 180
            elif yDiff > 0:
                zAngle += 360
            if abs(xDiff) < abs(yDiff):
                zAngle -= 90
        elif xDiff:
            if xDiff > 0:
                zAngle = 180
            else:
                zAngle = 0
        elif yDiff:
            if yDiff > 0:
                zAngle = 180
            else:
                zAngle = 0
        else:
            zAngle = 0
#FIXME: I CANNOT REMEMBER WHY WE DO THIS, I CANNOT SEE A REASON (1)
#        if not o.canon:
#            msgList, units, xMin, yMin, xMax, yMax = bounds_check('align', 0, 0)
#FIXME: NO CAMERA YET
#        self.w.camview.rotation = zAngle
        ensure_mode(linuxcnc.MODE_MDI)
        c.mdi('G10 L20 P0 X{} Y{}'.format(offsetX, offsetY))
        c.wait_complete()
        c.mdi('G10 L2 P0 R{}'.format(zAngle))
        c.wait_complete()
        if loaded_file:
            commands.reload_file(False)
        ensure_mode(linuxcnc.MODE_MANUAL)
#FIXME: SEE (1) ABOVE
#        if not boundsError['align']:
        if 1:
            ensure_mode(linuxcnc.MODE_MDI)
            c.mdi('G0 X0 Y0')
            c.wait_complete()
            ensure_mode(linuxcnc.MODE_MANUAL)
#FIXME: NO CAMERA YET
#        self.w.cam_goto.setEnabled(True)
    return buttonState


##############################################################################
# FRAMING FUNCTIONS                                                          #
##############################################################################
def frame_error(torch, msgList, units, xMin, yMin, xMax, yMax):
    title = _('AXIS LIMIT ERROR')
    msgs = ''
    msg1 = _('due to laser offset')
    for n in range(0, len(msgList)):
        if msgList[n][1] == 'MAX':
            msg0 = _('move would exceed the maximum limit by')
        else:
            msg0 = _('move would exceed the minimum limit by')
        fmt = '{} {} {}{} {}\n\n' if msgs else '{} {} {}{} {}\n\n'
        msgs += fmt.format(msgList[n][0], msg0, msgList[n][2], units, msg1)
    if not torch:
        msgs += _('Do you want to try with the torch?')
        response = messagebox.askyesno('Axis Limit Error', msgs)
    else:
        msgs += _('Framing can not proceed')
        response = messagebox.showerror('Axis Limit Error', msgs)
    return response

def frame_job(feed, height):
    global framingState, activeFunction
    if o.canon:
        msgList, units, xMin, yMin, xMax, yMax = bounds_check('framing', laserOffsets['X'], laserOffsets['Y'])
        if msgList:
            reply = frame_error(False, msgList, units, xMin, yMin, xMax, yMax)
            if not reply:
                return
            msgList, units, xMin, yMin, xMax, yMax = bounds_check('framing', 0, 0)
            if msgList:
                reply = frame_error(True, msgList, units, xMin, yMin, xMax, yMax)
                return
        if s.interp_state == linuxcnc.INTERP_IDLE:
            activeFunction = True
            if not msgList:
                comp['laser-on'] = 1
            if not feed:
                feed = widgetValues['.runs.material.cut-feed-rate']
            ensure_mode(linuxcnc.MODE_MDI)
            c.mdi('G64 P{:0.3f}'.format(hal.get_value('halui.machine.units-per-mm')))
            c.wait_complete()
            if not height:
                height = machineBounds['Z+'] - (hal.get_value('plasmac.max-offset') * unitsPerMm)
                c.mdi('G53 G0 Z{:0.4f}'.format(height))
            c.mdi('G53 G0 X{:0.2f} Y{:0.2f}'.format(xMin, yMin))
            c.mdi('G53 G1 Y{:0.2f} F{:0.0f}'.format(yMax, feed))
            c.mdi('G53 G1 X{:0.2f}'.format(xMax))
            c.mdi('G53 G1 Y{:0.2f}'.format(yMin))
            c.mdi('G53 G1 X{:0.2f}'.format(xMin))
            ensure_mode(linuxcnc.MODE_MANUAL)
            framingState = True


##############################################################################
# BOUNDS CHECK                                                               #
##############################################################################
def bounds_check(boundsType, xOffset , yOffset):
    global machineBounds
    # glcanon reports in imperial (dinosaur) units, we need to:
    #   test the bounds in machine units
    #   report the error in currently displayed units
    boundsMultiplier = 25.4 if s.linear_units == 1 else 1
    if o.canon:
        gcUnits = 'mm' if 210 in o.canon.state.gcodes else 'in'
        xMin = (round(o.canon.min_extents[0] * boundsMultiplier + xOffset, 5))
        xMax = (round(o.canon.max_extents[0] * boundsMultiplier + xOffset, 5))
        yMin = (round(o.canon.min_extents[1] * boundsMultiplier + yOffset, 5))
        yMax = (round(o.canon.max_extents[1] * boundsMultiplier + yOffset, 5))
    else:
        gcUnits = 'mm' if s.linear_units == 1 else 'in'
        xMin = xMax = xOffset
        yMin = yMax = yOffset
#FIXME: CAN WE USE VARS.METRIC.GET() INSTEAD OF GCUNITS ABOVE
    print("vars.metric:{}  gcUnits:{}".format(vars.metric.get(), gcUnits))
    if s.linear_units == 1 and gcUnits == 'in':
        reportMultipler = 0.03937
    elif s.linear_units != 1 and gcUnits == 'mm':
        reportMultipler = 25.4
    else:
        reportMultiplier = 1
    msgList = []
    if xMin < machineBounds['X-']:
        amount = machineBounds['X-'] - xMin # machine units
        msgList.append(['X','MIN','{:0.2f}'.format(amount * reportMultiplier)])
    if xMax > machineBounds['X+']:
        amount = xMax - machineBounds['X+']
        msgList.append(['X','MAX','{:0.2f}'.format(amount * reportMultiplier)])
    if yMin < machineBounds['Y-']:
        amount = machineBounds['T-'] - yMin
        msgList.append(['Y','MIN','{:0.2f}'.format(amount * reportMultiplier)])
    if yMax > machineBounds['Y+']:
        amount = yMax - machineBounds['Y+']
        msgList.append(['Y','MAX','{:0.2f}'.format(amount * reportMultiplier)])
    return msgList, gcUnits, xMin, yMin, xMax, yMax


##############################################################################
# HEIGHT OVERRIDE                                                            #
##############################################################################
def height_lower():
    if rC(foverride + '.lower','cget','-state') == 'disabled':
        return
    global torchHeight
    torchHeight -= 0.1
    rC(foverride + '.height-override','configure','-text','%0.1fV' % (torchHeight))
    hal.set_p('plasmac.height-override','%f' %(torchHeight))

def height_raise():
    if rC(foverride + '.raise','cget','-state') == 'disabled':
        return
    global torchHeight
    torchHeight += 0.1
    rC(foverride + '.height-override','configure','-text','%0.1fV' % (torchHeight))
    hal.set_p('plasmac.height-override','%f' %(torchHeight))

def height_reset():
    if rC(foverride + '.reset','cget','-state') == 'disabled':
        return
    global torchHeight
    torchHeight = 0
    rC(foverride + '.height-override','configure','-text','%0.1fV' % (torchHeight))
    hal.set_p('plasmac.height-override','%f' %(torchHeight))


##############################################################################
# CUT RECOVERY FUNCTIONS                                                     #
##############################################################################
def cut_rec_default_changed(percent):
    rC(fcutrec + '.display.cut-rec-speed','set',percent)

def cut_rec_slider_changed(percent):
    pVars.crSpeed.set('{:0.0f}'.format(int(widgetValues['.runs.material.cut-feed-rate']) * int(percent) * 0.01, 0))

def cut_rec_motion(direction):
    if int(direction):
        speed = float(rC(fcutrec + '.display.cut-rec-speed','get')) * 0.01
        hal.set_p('plasmac.paused-motion-speed','%f' % (speed * int(direction)))
    else:
        hal.set_p('plasmac.paused-motion-speed','0')

def cut_rec_move(x, y):
    if not s.paused:
        return
    maxMove = 10
    if s.linear_units != 1:
        maxMove = 0.4
    laser = hal.get_value('plasmac.laser-recovery-state') > 0
    distX = float(pVars.kerfWidth.get()) * int(x)
    distY = float(pVars.kerfWidth.get()) * int(y)
    xNew = hal.get_value('plasmac.axis-x-position') + hal.get_value('axis.x.eoffset') - (laserOffsets['X'] * laser) + distX
    yNew = hal.get_value('plasmac.axis-y-position') + hal.get_value('axis.y.eoffset') - (laserOffsets['Y'] * laser) + distY
    if xNew < machineBounds['X-'] or xNew > machineBounds['X+'] or yNew < machineBounds['Y-'] or yNew > machineBounds['Y+']:
        return
    xTotal = hal.get_value('axis.x.eoffset') - (laserOffsets['X'] * laser) + distX
    yTotal = hal.get_value('axis.y.eoffset') - (laserOffsets['Y'] * laser) + distY
    if xTotal > maxMove or xTotal < -maxMove or yTotal > maxMove or yTotal < -maxMove:
        return
    moveX = int(distX / hal.get_value('plasmac.offset-scale'))
    moveY = int(distY / hal.get_value('plasmac.offset-scale'))
    hal.set_p('plasmac.x-offset', '{}'.format(str(hal.get_value('plasmac.x-offset') + moveX)))
    hal.set_p('plasmac.y-offset', '{}'.format(str(hal.get_value('plasmac.y-offset') + moveY)))
    hal.set_p('plasmac.cut-recovery', '1')

def cut_rec_cancel():
    hal.set_p('plasmac.cut-recovery', '0')
    hal.set_p('plasmac.laser-recovery-start', '0')
    hal.set_p('plasmac.x-offset', '0')
    hal.set_p('plasmac.y-offset', '0')
    comp['laser-on'] = 0


##############################################################################
# RUN FROM LINE DIALOG                                                       #
##############################################################################
def dialog_run_from_line():
    global result
    result = None

    def leadin_clicked(event):
        global result
        result = event
        rfl.quit()

    rfl = Tkinter.Toplevel()
    rfl.title('Run From Line')
    lbl1 = Tkinter.Label(rfl, text=_('Use Leadin:'))
    lbl2 = Tkinter.Label(rfl, text=_('Leadin Length:'))
    lbl3 = Tkinter.Label(rfl, text=_('Leadin Angle:'))
    lbl4 = Tkinter.Label('')
    leadIn = Tkinter.BooleanVar()
    leadinDo = Tkinter.Checkbutton(rfl, variable=leadIn)
    leadLength = Tkinter.StringVar()
    leadinLength = Tkinter.Spinbox(rfl, textvariable=leadLength)
    leadAngle = Tkinter.StringVar()
    leadinAngle = Tkinter.Spinbox(rfl, textvariable=leadAngle)
    buttons = Tkinter.Frame(rfl)
    buttonLoad = Tkinter.Button(buttons, text=_('Load'), width=8, )
    buttonCancel = Tkinter.Button(buttons, text=_('Cancel'), width=8)
    lbl1.grid(column=0, row=0, sticky='e')
    lbl2.grid(column=0, row=1, sticky='e')
    lbl3.grid(column=0, row=2, sticky='e')
    lbl4.grid(column=0, row=3, sticky='e')
    leadinDo.grid(column=1, row=0, sticky='w')
    leadinLength.grid(column=1, row=1, sticky='w')
    leadinAngle.grid(column=1, row=2, sticky='w')
    buttonLoad.pack(side='left')
    buttonCancel.pack(side='right')
    buttons.grid(column=0, row=4, columnspan=2, sticky='ew')
    buttons.grid_columnconfigure(0, weight=1, uniform='group1')
    buttons.grid_columnconfigure(2, weight=1, uniform='group1')
    rfl.grid_rowconfigure(0, weight=1, uniform='group2')
    rfl.grid_rowconfigure(1, weight=1, uniform='group2')
    rfl.grid_rowconfigure(2, weight=1, uniform='group2')
    rfl.grid_rowconfigure(3, weight=1, uniform='group2')
    rfl.grid_rowconfigure(4, weight=1, uniform='group2')
    leadIn.set(False)
    if s.linear_units == 1:
        leadinLength.config(width=10, from_=1, to=25, increment=1, format='%0.0f', wrap=1)
        leadLength.set(5)
    else:
        leadinLength.config(width=10, from_=0.05, to=1, increment=0.05, format='%0.2f', wrap=1)
        leadLength.set(0.2)
    leadinAngle.config(width=10, from_=-359, to=359, increment=1, format='%0.0f', wrap=1)
    leadAngle.set(0)
    buttonLoad.bind('<Button-1>', lambda event: leadin_clicked('load'))
    buttonCancel.bind('<Button-1>', lambda event: leadin_clicked('cancel'))
    Tkinter.mainloop()
    rfl.destroy()
    # load clicked
    if result == 'load':
        return {'cancel':False, 'do':leadIn.get(), 'length':float(leadLength.get()), 'angle':float(leadAngle.get())}
    # cancel clicked
    else:
        pVars.rflActive = False
        pVars.startLine.set(0)
        return {'cancel':True}


##############################################################################
# TCL FUNCTIONS HIJACKED FROM AXIS.PY                                        #
##############################################################################
# add plasmac to the title
def update_title(*args):
    if vars.taskfile.get() == '':
        file = 'no file'
        name = 'AXIS'
    else:
        file = name = os.path.basename(vars.taskfile.get())
    base = '{} on PLASMAC_V{} + AXIS {}'.format(vars.machine.get(), VER, linuxcnc.version)
    rC('wm','title','.','{} - ({})'.format(base, file))
    rC('wm','iconname','.', name)

# inhibit slider update if manual cut is active and use a linear response for jog slider
def update_jog_slider_vel(value):
    if not manualCut['state']:
        rE('set jog_speed {}'.format(int(float(value) * vars.max_speed.get() * 60)))


##############################################################################
# PYTHON FUNCTIONS HIJACKED FROM AXIS.PY                                     #
##############################################################################
def vupdate(var, val):
    # pretend no file is loaded if program is cleared
    if var == vars.taskfile and 'clear.ngc' in val:
        val = ''
    try:
        if var.get() == val: return
    except ValueError:
        pass
    var.set(val)

def reload_file(refilter=True):
    if running(): return
    s.poll()
    if not loaded_file and not pVars.preRflFile.get():
        root_window.tk.call('set_mode_from_tab')
        return
    line = vars.highlight_line.get()
    o.set_highlight_line(None)
    f = pVars.preRflFile.get() if pVars.preRflFile.get() else loaded_file
    if refilter or not get_filter(f):
        open_file_guts(f, False, False)
    else:
        tempfile = os.path.join(tempdir, os.path.basename(f))
        open_file_guts(tempfile, True, False)
    if line:
        o.set_highlight_line(line)

def task_run_line():
    if vars.highlight_line.get() == 0:
        return
    title = _('RUN FROM LINE ERROR')
    pVars.startLine.set(vars.highlight_line.get() - 1)
    if loaded_file != os.path.join(tmpPath, 'rfl.ngc'):
        rflIn = os.path.join(tmpPath, 'filtered_bkp.ngc')
    else:
        rflIn = loaded_file
    if comp['development']:
        reload(RFL)
    setup = RFL.run_from_line_get(rflIn, pVars.startLine.get())
    # cannot do run from line within a subroutine or if using cutter compensation
    if setup['error']:
        if setup['compError']:
            msg0 = _('Cannot run from line while cutter compensation is active')
            notifications.add('error', '{}:\n{}\n'.format(title, msg0))
        if setup['subError']:
            msg0 = _('Cannot do run from line inside a subroutine')
            msg1 = ''
            for sub in setup['subError']:
                msg1 += ' {}'.format(sub)
                notifications.add('error', '{}:\n{} {}\n'.format(title, msg0, msg1))
            pVars.rflActive = False
            pVars.startLine.set(0)
    else:
        # get user input
        userInput = dialog_run_from_line()
        # rfl cancel clicked
        if userInput['cancel']:
            pVars.rflActive = False
            pVars.startLine.set(0)
        else:
            # rfl load clicked
            rflFile = os.path.join(tmpPath, 'rfl.ngc')
            result = RFL.run_from_line_set(rflFile, setup, userInput, unitsPerMm)
            # leadin cannot be used
            if result['error']:
                msg0 = _('Unable to calculate a leadin for this cut')
                msg1 = _('Program will run from selected line with no leadin applied')
                notifications.add('error', '{}:\n{}\n{}\n'.format(title, msg0, msg1))
            # load rfl file
            if loaded_file != os.path.join(tmpPath, 'rfl.ngc'):
                pVars.preRflFile.set(loaded_file)
            open_file_guts(os.path.join(tmpPath, 'rfl.ngc'), False, False)

def task_stop(*event):
    if s.task_mode == linuxcnc.MODE_AUTO and vars.running_line.get() != 0:
        o.set_highlight_line(vars.running_line.get())
    comp['abort'] = True
    c.abort()
    c.wait_complete()
    time.sleep(0.3)
    comp['abort'] = False


##############################################################################
# USER BUTTON FUNCTIONS                                                      #
##############################################################################
def validate_hal_pin(halpin, button, usage):
    title = _('HAL PIN ERROR')
    valid = pBit = False
    for pin in halPinList:
        if halpin in pin['NAME']:
            pBit = isinstance(pin['VALUE'], bool)
            valid = True
            break
    if not valid:
        msg0 = _('does not exist for user button')
        notifications.add('error', '{}:\n{} {} #{}'.format(title, halpin, msg0, button))
    if not pBit:
        msg0 = _('must be a bit pin for user button')
        notifications.add('error', '{}:\n{} {} #{}'.format(title, usage, msg0, button))
        valid = False
    return valid

def validate_ini_param(code, button):
    title = _('PARAMETER ERROR')
    valid = [False, None]
    try:
        parm = code[code.index('{') + len('') + 1: code.index('}')]
        value = inifile.find(parm.split()[0], parm.split()[1]) or None
        if value:
            valid = [True, code.replace('{{{}}}'.format(parm), value)]
    except:
        pass
    if not valid[0]:
        msg0 = _('invalid parameter')
        msg1 = _('for user button')
        notifications.add('error', '{}:\n{} {} {} #{}'.format(title, msg0, code, msg1, button))
    return valid

def button_action(button, pressed):
    if int(pressed):
        user_button_pressed(button, buttonCodes[int(button)])
    else:
        user_button_released(button, buttonCodes[int(button)])

def user_button_setup():
    global buttonNames, buttonCodes, togglePins, pulsePins, machineBounds, criticalButtons
    global probeButton, probeText, torchButton, torchText, cChangeButton
    singleCodes = ['ohmic-test','cut-type','single-cut','manual-cut','probe-test', \
                   'torch-pulse','change-consumables','framing','latest-file']
    buttonNames = {0:{'name':None}}
    buttonCodes = {0:{'code':None}}
    criticalButtons = []
    row = 1
    for n in range(1,21):
        bLabel = None
        bName = getPrefs(PREF,'BUTTONS', str(n) + ' Name', '', str)
        bCode = getPrefs(PREF,'BUTTONS', str(n) + ' Code', '', str)
        outCode = {'code':None}
        if bCode.strip() == 'ohmic-test' and not 'ohmic-test' in [(v['code']) for k, v in buttonCodes.items()]:
            outCode['code'] = 'ohmic-test'
        elif bCode.strip() == 'cut-type' and not 'cut-type' in buttonCodes:
            bName = bName.split(',')
            if len(bName) == 1:
                text = _('Pierce\Only') if '\\' in bName[0] else _('Pierce Only')
                bName.append(text)
            outCode = {'code':'cut-type', 'text':bName}
        elif bCode.strip() == 'single-cut' and not 'single-cut' in buttonCodes:
            outCode['code'] = 'single-cut'
            criticalButtons.append(n)
        elif bCode.strip() == 'manual-cut' and not 'manual-cut' in buttonCodes:
            outCode['code'] = 'manual-cut'
            criticalButtons.append(n)
        elif bCode.startswith('probe-test') and not 'probe-test' in [(v['code']) for k, v in buttonCodes.items()]:
            if bCode.split()[0].strip() == 'probe-test' and len(bCode.split()) < 3:
                codes = bCode.strip().split()
                outCode = {'code':'probe-test', 'time':10}
                probeButton = str(n)
                probeText = bName.replace('\\', '\n')
                if len(codes) == 2:
                    try:
                        value = int(float(codes[1]))
                        outCode['time'] = value
                    except:
                        outCode['code'] = None
        elif bCode.startswith('torch-pulse') and not 'torch-pulse' in [(v['code']) for k, v in buttonCodes.items()]:
            if bCode.split()[0].strip() == 'torch-pulse' and len(bCode.split()) < 3:
                codes = bCode.strip().split()
                outCode = {'code':'torch-pulse', 'time':1.0}
                torchButton = str(n)
                torchText = bName.replace('\\', '\n')
                if len(codes) == 2:
                    try:
                        value = round(float(codes[1]), 1)
                        outCode['time'] = value
                    except:
                        outCode['code'] = None
        elif bCode.startswith('change-consumables ') and not 'change-consumables' in [(v['code']) for k, v in buttonCodes.items()]:
            codes = re.sub(r'([xyf]|[XYF])\s+', r'\1', bCode) # remove any spaces after x, y, and f
            codes = codes.lower().strip().split()
            if len(codes) > 1 and len(codes) < 5:
                outCode = {'code':'change-consumables', 'X':None, 'Y':None, 'F':None}
                for l in 'xyf':
                    for c in range(1, len(codes)):
                        if codes[c].startswith(l):
                            try:
                                value = round(float(codes[c].replace(l,'')), 3)
                                outCode['XYF'['xyf'.index(l)]] = value
                            except:
                                outCode['code'] = None
                if (not outCode['X'] and not outCode['Y']) or not outCode['F']:
                    outCode['code'] = None
                else:
                    buff = 10 * hal.get_value('halui.machine.units-per-mm') # keep 10mm away from machine limits
                    for axis in 'XY':
                        if outCode[axis]:
                            if outCode['{}'.format(axis)] < machineBounds['{}-'.format(axis)] + buff:
                                outCode['{}'.format(axis)] = machineBounds['{}-'.format(axis)] + buff
                            elif outCode['{}'.format(axis)] > machineBounds['{}+'.format(axis)] - buff:
                                outCode['{}'.format(axis)] = machineBounds['{}+'.format(axis)] - buff
            if outCode['code']:
                cChangeButton = str(n)
        elif bCode.startswith('framing') and not 'framing' in [(v['code']) for k, v in buttonCodes.items()]:
            codes = re.sub(r'([f]|[F])\s+', r'\1', bCode) # remove any spaces after f
            codes = codes.lower().strip().split()
            if codes[0] == 'framing' and len(codes) < 4:
                outCode = {'code':'framing', 'F':False, 'Z':False}
                for c in range(1, len(codes)):
                    if codes[c].startswith('f'):
                        try:
                            value = round(float(codes[c].replace('f','')), 3)
                            outCode['F'] = value
                        except:
                            outCode['code'] = None
                    elif codes[c] == 'usecurrentzheight':
                        outCode['Z'] = True
                    else:
                        outCode['code'] = None
        elif bCode.startswith('load '):
            if len(bCode.split()) > 1 and len(bCode.split()) < 3:
                codes = bCode.strip().split()
                if os.path.isfile(os.path.join(open_directory, codes[1])):
                    outCode = {'code':'load', 'file':os.path.join(open_directory, codes[1])}
        elif bCode.startswith('latest-file') and not 'latest-file' in [(v['code']) for k, v in buttonCodes.items()]:
            if len(bCode.split()) < 3:
                codes = bCode.strip().split()
                outCode = {'code':'latest-file', 'dir':None}
                if len(codes) == 1:
                    outCode['dir'] = open_directory
                elif len(codes) == 2 and os.path.isdir(codes[1]):
                    outCode['dir'] = codes[1]
                else:
                    outCode['code'] = None
        elif bCode.startswith('pulse-halpin '):
            if len(bCode.split()) > 1 and len(bCode.split()) < 4:
                codes = bCode.strip().split()
                if validate_hal_pin(codes[1], n, 'pulse-halpin'):
                    outCode = {'code':'pulse-halpin', 'pin':codes[1], 'time':1.0}
                    outCode['pin'] = codes[1]
                    try:
                        value = round(float(codes[2]), 1)
                        outCode['time'] = value
                        pulsePins[str(n)] = {'button':str(n), 'pin':outCode['pin'], 'text':None, 'timer':0, 'counter':0, 'state':False}
                    except:
                        outCode = {'code':None}
        elif bCode.startswith('toggle-halpin '):
            if len(bCode.split()) > 1 and len(bCode.split()) < 4:
                codes = bCode.strip().split()
                if validate_hal_pin(codes[1], n, 'toggle-halpin'):
                    outCode = {'code':'toggle-halpin', 'pin':codes[1], 'critical':False}
                    outCode['pin'] = codes[1]
                    if len(codes) == 3 and codes[2] == 'runcritical':
                        outCode['critical'] = True
                    togglePins[str(n)] = {'button':str(n), 'pin':outCode['pin'], 'state':hal.get_value(outCode['pin']), 'runcritical':outCode['critical']}
        elif bCode and bCode not in singleCodes:
            codes = bCode.strip().split('/')
            codes = [x.strip() for x in codes]
            outCode['code'] = '%Code'
            nc = 0
            for cd in codes:
                nc += 1
                if cd[0] == '%':
                    outCode[nc] = cd
                elif cd[:2].lower() == 'o<':
                    outCode[nc] = cd
                    outCode['code'] = 'gCode'
                elif cd[0].lower() in 'gm':
                    outCode['code'] = 'gCode'
                    if not '{' in cd:
                        outCode[nc] = cd
                    else:
                        reply = validate_ini_param(cd, n)
                        if reply[0]:
                            outCode[nc] = reply[1]
                        else:
                            outCode = {'code':None}
                            break
                else:
                    outCode = {'code':None}
                    break
        else:
            outCode = {'code':None}
        if not rC('winfo','exists','.fbuttons.button' + str(n)):
            rC('button','.fbuttons.button' + str(n),'-takefocus',0,'-width',10)
        if bName and outCode['code']:
            bHeight = 1
            if type(bName) == list:
                if '\\' in bName[0] or '\\' in bName[1]:
                    bHeight = 2
                if rC('.fbuttons.button' + str(n),'cget','-bg') != buttonBackG:
                    bName = bName[1]
                else:
                    bName = bName[0]
            else:
                if '\\' in bName:
                    bHeight = 2
            bLabel = bName.replace('\\', '\n')
            rC('.fbuttons.button' + str(n),'configure','-text',bLabel,'-height',bHeight)
            rC('grid','.fbuttons.button{}'.format(n),'-column',0,'-row',row,'-sticky','new')
            rC('bind','.fbuttons.button{}'.format(n),'<ButtonPress-1>','button_action {} 1'.format(n))
            rC('bind','.fbuttons.button{}'.format(n),'<ButtonRelease-1>','button_action {} 0'.format(n))
            if bCode.startswith('toggle-halpin ') and togglePins[str(n)]['runcritical']:
                rC('.fbuttons.button' + str(n),'configure','-bg',ourRed)
            row += 1
        elif bName or bCode:
            title = _('USER BUTTON ERROR')
            msg0 = _('is invalid code for user button')
            notifications.add('error', '{}:\n"{}" {} #{}'.format(title, bCode, msg0, n))
            bName = None
            outCode = {'code':None}
        buttonNames[n] = {'name':bName}
        buttonCodes[n] = outCode
    user_button_load()

def user_button_pressed(button, code):
    global buttonBackG, activeFunction
    global probePressed, probeStart, probeTimer, probeButton
    global torchPressed, torchStart, torchTimer, torchButton

    if rC('.fbuttons.button' + button,'cget','-state') == 'disabled' or not code:
        return
    from subprocess import Popen,PIPE
    if code['code'] == 'ohmic-test':
        hal.set_p('plasmac.ohmic-test','1')
#FIXME: TEMPORARY PRINT FOR REPORTING WINDOW SIZES
        print('Width={}   Height={}'.format(rC('winfo','width',root_window), rC('winfo','height',root_window)))
    elif code['code'] == 'cut-type':
        pass # actioned from button_release
    elif code['code'] == 'single-cut':
        pass # actioned from button_release
    elif code['code'] == 'manual-cut':
        manual_cut(None)
    elif code['code'] == 'probe-test' and not hal.get_value('halui.program.is-running'):
        if probeTimer:
            probeTimer = 0
        elif not hal.get_value('plasmac.z-offset-counts'):
            activeFunction = True
            probePressed = True
            probeStart = time.time()
            probeTimer = code['time']
            hal.set_p('plasmac.probe-test','1')
            rC('.fbuttons.button' + probeButton,'configure','-text',str(int(probeTimer)))
            rC('.fbuttons.button' + probeButton,'configure','-bg',ourRed)
    elif code['code'] == 'torch-pulse':
        if torchTimer:
            torchTimer = 0
        elif not hal.get_value('plasmac.z-offset-counts'):
            torchPressed = True
            torchStart = time.time()
            torchTimer = code['time']
            hal.set_p('plasmac.torch-pulse-time','{}'.format(torchTimer))
            hal.set_p('plasmac.torch-pulse-start','1')
            rC('.fbuttons.button' + torchButton,'configure','-text',str(int(torchTimer)))
            rC('.fbuttons.button' + torchButton,'configure','-bg',ourRed)
    elif code['code'] == 'change-consumables' and not hal.get_value('plasmac.breakaway'):
        if hal.get_value('axis.x.eoffset-counts') or hal.get_value('axis.y.eoffset-counts'):
            hal.set_p('plasmac.consumable-change', '0')
            hal.set_p('plasmac.x-offset', '0')
            hal.set_p('plasmac.y-offset', '0')
            rC('.fbuttons.button' + button,'configure','-bg',buttonBackG)
            activeFunction = False
        else:
            activeFunction = True
            xPos = s.position[0] if not code['X'] else code['X']
            yPos = s.position[1] if not code['Y'] else code['Y']
            hal.set_p('plasmac.xy-feed-rate', str(code['F']))
            hal.set_p('plasmac.x-offset', '{:.0f}'.format((xPos - s.position[0]) / hal.get_value('plasmac.offset-scale')))
            hal.set_p('plasmac.y-offset', '{:.0f}'.format((yPos - s.position[1]) / hal.get_value('plasmac.offset-scale')))
            hal.set_p('plasmac.consumable-change', '1')
            rC('.fbuttons.button' + button,'configure','-bg',ourOrange)
    elif code['code'] == 'framing':
        pass # actioned from button_release
    elif code['code'] == 'load':
        pass # actioned from button_release
    elif code['code'] == 'latest-file':
        pass # actioned from button_release
    elif code['code'] == 'pulse-halpin' and hal.get_value('halui.program.is-idle'):
        hal.set_p(code['pin'], str(not hal.get_value(code['pin'])))
        if not pulsePins[button]['timer']:
            pulsePins[button]['text'] = rC('.fbuttons.button' + button,'cget','-text')
            pulsePins[button]['timer'] = code['time']
            pulsePins[button]['counter'] = time.time()
        else:
            pulsePins[button]['timer'] = 0
            rC('.fbuttons.button' + button,'configure','-text',pulsePins[button]['text'])
    elif code['code'] == 'toggle-halpin' and hal.get_value('halui.program.is-idle'):
        hal.set_p(code['pin'], str(not hal.get_value(code['pin'])))
    else:
        for n in range(1, len(code)):
            if code[n][0] == '%':
                Popen(code[n][1:], stdout=PIPE, stderr=PIPE, shell=True)
            else:
                if manual_ok():
                    ensure_mode(linuxcnc.MODE_MDI)
                    commands.send_mdi_command(code[n])
                    ensure_mode(linuxcnc.MODE_MANUAL)

def user_button_released(button, code):
    global cutType, probePressed, torchPressed
    if rC('.fbuttons.button' + button,'cget','-state') == 'disabled' or not code: return
    if code['code'] == 'ohmic-test':
        hal.set_p('plasmac.ohmic-test','0')
    elif code['code'] == 'cut-type':
        if not hal.get_value('halui.program.is-running'):
            cutType ^= 1
            if cutType:
                comp['cut-type'] = 1
                text = code['text'][1].replace('\\', '\n')
                color = ourOrange
            else:
                comp['cut-type'] = 0
                text = code['text'][0].replace('\\', '\n')
                color = buttonBackG
            rC('.fbuttons.button' + button,'configure','-bg',color,'-text',text)
            reload_file()
    elif code['code'] == 'single-cut':
        single_cut()
    elif code['code'] == 'manual-cut':
        pass
    elif code['code'] == 'probe-test':
        probePressed = False
    elif code['code'] == 'torch-pulse':
        torchPressed = False
    elif code['code'] == 'change-consumables':
        pass
    elif code['code'] == 'framing':
        frame_job(code['F'], code['Z'])
    elif code['code'] == 'load':
        commands.open_file_name(code['file'])
    elif code['code'] == 'latest-file':
        files = GLOB('{}/*.ngc'.format(code['dir']))
        latest = max(files, key=os.path.getctime)
        commands.open_file_name(latest)
    elif code['code'] == 'pulse-halpin':
        pass
    elif code['code'] == 'toggle-halpin':
        pass
    else:
        pass

def user_button_add():
    for n in range(1, 21):
        if not rC('winfo','ismapped',fsetup + '.r.ubuttons.num' + str(n)):
            rC('grid',fsetup + '.r.ubuttons.num' + str(n),'-column',0,'-row',n,'-sticky','ne','-padx',(4,0),'-pady',(4,0))
            rC('grid',fsetup + '.r.ubuttons.name' + str(n),'-column',1,'-row',n,'-sticky','nw','-padx',(4,0),'-pady',(4,0))
            rC('grid',fsetup + '.r.ubuttons.code' + str(n),'-column',2,'-row',n,'-sticky','new','-padx',(4,4),'-pady',(4,0))
            break

def user_button_load():
    rC(fsetup + '.r.torch.enabled','delete',0,'end')
    rC(fsetup + '.r.torch.disabled','delete',0,'end')
    rC(fsetup + '.r.torch.enabled','insert','end',getPrefs(PREF,'BUTTONS', 'Torch enabled', 'Torch\Enabled', str))
    rC(fsetup + '.r.torch.disabled','insert','end',getPrefs(PREF,'BUTTONS','Torch disabled', 'Torch\Disabled', str))
    for n in range(1, 21):
        rC('grid','forget',fsetup + '.r.ubuttons.num' + str(n))
        rC('grid','forget',fsetup + '.r.ubuttons.name' + str(n))
        rC('grid','forget',fsetup + '.r.ubuttons.code' + str(n))
        rC(fsetup + '.r.ubuttons.name' + str(n),'delete',0,'end')
        rC(fsetup + '.r.ubuttons.code' + str(n),'delete',0,'end')
        if getPrefs(PREF,'BUTTONS', str(n) + ' Name', '', str) or getPrefs(PREF,'BUTTONS', str(n) + ' Code', '', str):
            rC(fsetup + '.r.ubuttons.name' + str(n),'insert','end',getPrefs(PREF,'BUTTONS', str(n) + ' Name', '', str))
            rC(fsetup + '.r.ubuttons.code' + str(n),'insert','end',getPrefs(PREF,'BUTTONS', str(n) + ' Code', '', str))
            rC('grid',fsetup + '.r.ubuttons.num' + str(n),'-column',0,'-row',n,'-sticky','ne','-padx',(4,0),'-pady',(4,0))
            rC('grid',fsetup + '.r.ubuttons.name' + str(n),'-column',1,'-row',n,'-sticky','nw','-padx',(4,0),'-pady',(4,0))
            rC('grid',fsetup + '.r.ubuttons.code' + str(n),'-column',2,'-row',n,'-sticky','new','-padx',(4,4),'-pady',(4,0))
            fg = ourBlack if buttonNames[n]['name'] else ourRed
            rC(fsetup + '.r.ubuttons.name' + str(n),'configure','-fg',fg)
            rC(fsetup + '.r.ubuttons.code' + str(n),'configure','-fg',fg)

def user_button_save():
    global torchEnable
    putPrefs(PREF,'BUTTONS', 'Torch enabled', rC(fsetup + '.r.torch.enabled','get'), str)
    putPrefs(PREF,'BUTTONS', 'Torch disabled', rC(fsetup + '.r.torch.disabled','get'), str)
    torchEnable['enabled'] = getPrefs(PREF,'BUTTONS', 'Torch enabled', 'Torch\Enabled', str)
    torchEnable['disabled'] = getPrefs(PREF,'BUTTONS','Torch disabled', 'Torch\Disabled', str)
    if '\\' in torchEnable['enabled'] or '\\' in torchEnable['disabled']:
        rC('.fbuttons.torch-enable','configure','-height',2)
    else:
        rC('.fbuttons.torch-enable','configure','-height',1)
    if hal.get_value('plasmac.torch-enable'):
        rC('.fbuttons.torch-enable','configure','-text',torchEnable['enabled'].replace('\\','\n'),'-bg',ourGreen,'-activebackground',ourGreen)
    else:
        rC('.fbuttons.torch-enable','configure','-text',torchEnable['disabled'].replace('\\','\n'),'-bg',ourRed,'-activebackground',ourRed)
    for n in range(1, 21):
        if rC(fsetup + '.r.ubuttons.name' + str(n),'get') and rC(fsetup + '.r.ubuttons.code' + str(n),'get'):
            putPrefs(PREF,'BUTTONS', '{} Name'.format(n), rC(fsetup + '.r.ubuttons.name' + str(n),'get'), str)
            putPrefs(PREF,'BUTTONS', '{} Code'.format(n), rC(fsetup + '.r.ubuttons.code' + str(n),'get'), str)
            rC('grid','forget',fsetup + '.r.ubuttons.num' + str(n))
            rC('grid','forget',fsetup + '.r.ubuttons.name' + str(n))
            rC('grid','forget',fsetup + '.r.ubuttons.code' + str(n))
            rC('grid','forget','.fbuttons.button' + str(n))
            rC(fsetup + '.r.ubuttons.name' + str(n),'delete',0,'end')
            rC(fsetup + '.r.ubuttons.code' + str(n),'delete',0,'end')
        elif (rC(fsetup + '.r.ubuttons.name' + str(n),'get') and not rC(fsetup + '.r.ubuttons.code' + str(n),'get')) or \
             (not rC(fsetup + '.r.ubuttons.name' + str(n),'get') and rC(fsetup + '.r.ubuttons.code' + str(n),'get')):
            title = _('USER BUTTON ERROR')
            msg0 = _('code or name missing from user button')
            notifications.add('error', '{}:\n{} #{}'.format(title, msg0, n))
            rC(fsetup + '.r.ubuttons.name' + str(n),'delete',0,'end')
            rC(fsetup + '.r.ubuttons.code' + str(n),'delete',0,'end')
    user_button_setup()


##############################################################################
# MATERIAL HANDLING FUNCTIONS                                                #
##############################################################################
def save_material_clicked():
    section = 'MATERIAL_NUMBER_{}'.format(int(rC('.runs.materials','get').split(':')[0]))
    save_one_material(section)
    load_materials(section)

def reload_material_clicked():
    load_materials(int(rC('.runs.materials','get').split(':')[0]))

def new_material_clicked():
    global materialNumList
    title = _('ADD MATERIAL')
    msg1 = _('Enter New Material Number')
    msgs = msg1
    while(1):
        num = simpledialog.askstring(title, '{}:'.format(msgs))
        if num == None:
            return
        if not num:
            msg0 = _('A material number is required')
            msgs = '{}.\n\n{}:'.format(msg0, msg1)
            continue
        try:
            num = int(num)
        except:
            msg0 = _('is not a valid number')
            msgs = '{} {}.\n\n{}:'.format(num, msg0, msg1)
            continue
        if num == 0 or num in materialNumList:
            msg0 = _('Material')
            msg2 = _('is in use')
            msgs = '{} #{} {}.\n\n{}:'.format(msg0, num, msg2, msg1)
        elif num >= 1000000:
            msg0 = _('Material numbers need to be less than 1000000')
            msgs = '{}.\n\n{}:'.format(msg0, msg1)
        else:
            break
    msg1 = _('Enter New Material Name')
    msgs = msg1
    while(1):
        nam = simpledialog.askstring(title, '{}:'.format(msgs))
        if nam == None:
            return
        if not nam:
            msg0 = _('Material name is required')
            msgs = '{}.\n\n{}:'.format(msg0, msg1)
        else:
            break
    putPrefs(MATS,'MATERIAL_NUMBER_{}'.format(num),'NAME', nam, str)
    save_one_material('MATERIAL_NUMBER_{}'.format(num))
    sortPrefs(MATS)
    load_materials(num)

def delete_material_clicked():
    title = _('DELETE MATERIAL')
    msg0 = _('Default material cannot be deleted')
    material = int(rC('.runs.materials','get').split(':')[0])
    if material == getPrefs(PREF,'GUI_OPTIONS', 'Default material', 0, int):
        reply = messagebox.showwarning(title,msg0)
        return
    msg0 = _('Do you wish to delete material')
    reply = messagebox.askyesno(title, '{} #{}?'.format(msg0, material))
    if not reply:
        return
    removePrefsSect(MATS,'MATERIAL_NUMBER_{}'.format(int(rC('.runs.materials','get').split(':')[0])))
    load_materials()

def material_changed():
    global getMaterialBusy, materialAutoChange
    if rC('.runs.materials','get'):
        if getMaterialBusy:
            comp['material-change'] = 0
            materialAutoChange = False
            return
        matnum = int(rC('.runs.materials','get').split(': ', 1)[0])
        if matnum >= 1000000:
            rC('.toolmat.save','configure','-state','disabled')
        else:
            rC('.toolmat.save','configure','-state','normal')
        if materialAutoChange:
            hal.set_p('motion.digital-in-03','0')
            display_selected_material(matnum)
            comp['material-change'] = 2
            hal.set_p('motion.digital-in-03','1')
        else:
            display_selected_material(matnum)
    materialAutoChange = False

def material_change_pin_changed(halpin):
    if halpin == 0:
        hal.set_p('motion.digital-in-03','0')
    elif halpin == 3:
        hal.set_p('motion.digital-in-03','1')
        comp['material-change'] = 0

def material_change_number_pin_changed(halpin):
    global getMaterialBusy, materialAutoChange
    if getMaterialBusy:
        return
    if comp['material-change'] == 1:
        materialAutoChange = True
    if not material_exists(halpin):
        materialAutoChange = False
        return
    index = '@{}'.format(materialNumList.index(halpin))
    rC('.runs.materials','setvalue',index)
    display_selected_material(halpin)

def material_change_timeout_pin_changed(halpin):
    if halpin:
        title = _('MATERIALS ERROR')
        material = rC('.runs.materials','get').split(': ', 1)[0]
        msg0 = _('Material change timeout occurred for material')
        notifications.add('error', '{}:\n{} #{}\n'.format(title, msg0, material))
        comp['material-change-number'] = material
        comp['material-change-timeout'] = 0
        hal.set_p('motion.digital-in-03','0')

def material_temp_pin_changed(halpin):
    if halpin:
        title = _('MATERIALS ERROR')
        TEMP.read(TEMP.fn)
        material = get_one_material(TEMP, 'MATERIAL_NUMBER_{}'.format(halpin), halpin)
        if not material['valid']:
            msg0 = _('Temporary material')
            msg1 = _('is invalid')
            notifications.add('error', '{}:\n{} #{} {}\n'.format(title, msg0, halpin, msg1))
            return
        materialFileDict[halpin] = { \
                'name': material['name'], \
                'kerf_width': material['kerf_width'], \
                'pierce_height': material['pierce_height'], \
                'pierce_delay': material['pierce_delay'], \
                'puddle_jump_height': material['puddle_jump_height'], \
                'puddle_jump_delay': material['puddle_jump_delay'], \
                'cut_height': material['cut_height'], \
                'cut_speed': material['cut_speed'], \
                'cut_amps': material['cut_amps'], \
                'cut_volts': material['cut_volts'], \
                'pause_at_end': material['pause_at_end'], \
                'gas_pressure': material['gas_pressure'], \
                'cut_mode': material['cut_mode']}
        insert_materials()
        comp['material-temp'] = 0

def insert_materials():
    global materialNumList, materialFileDict
    mats = []
    materialNumList = []
    for matnum in sorted(materialFileDict):
        mats.append('{:07d}: {}'.format(matnum, materialFileDict[matnum]['name']))
        materialNumList.append(matnum)
    rC('.runs.materials','configure','-values',mats)

def display_selected_material(matnum, reload=False):
    rC('.runs.material.kerf-width','set',materialFileDict[matnum]['kerf_width'])
    rC('.runs.material.pierce-height','set',materialFileDict[matnum]['pierce_height'])
    rC('.runs.material.pierce-delay','set',materialFileDict[matnum]['pierce_delay'])
    rC('.runs.material.puddle-jump-height','set',materialFileDict[matnum]['puddle_jump_height'])
    rC('.runs.material.puddle-jump-delay','set',materialFileDict[matnum]['puddle_jump_delay'])
    rC('.runs.material.cut-height','set',materialFileDict[matnum]['cut_height'])
    rC('.runs.material.cut-feed-rate','set',materialFileDict[matnum]['cut_speed'])
    rC('.runs.material.cut-amps','set',materialFileDict[matnum]['cut_amps'])
    rC('.runs.material.cut-volts','set',materialFileDict[matnum]['cut_volts'])
    rC('.runs.material.pause-at-end','set',materialFileDict[matnum]['pause_at_end'])
    rC('.runs.material.gas-pressure','set',materialFileDict[matnum]['gas_pressure'])
    rC('.runs.material.cut-mode','set',materialFileDict[matnum]['cut_mode'])
    if not reload:
        comp['material-change-number'] = matnum

def save_one_material(section):
    putPrefs(MATS,section, 'KERF_WIDTH', rC('.runs.material.kerf-width','get'), float)
    putPrefs(MATS,section, 'PIERCE_HEIGHT', rC('.runs.material.pierce-height','get'), float)
    putPrefs(MATS,section, 'PIERCE_DELAY', rC('.runs.material.pierce-delay','get'), float)
    putPrefs(MATS,section, 'PUDDLE_JUMP_HEIGHT', rC('.runs.material.puddle-jump-height','get'), int)
    putPrefs(MATS,section, 'PUDDLE_JUMP_DELAY',rC('.runs.material.puddle-jump-delay','get'), float)
    putPrefs(MATS,section, 'CUT_HEIGHT', rC('.runs.material.cut-height','get'), float)
    putPrefs(MATS,section, 'CUT_SPEED', rC('.runs.material.cut-feed-rate','get'), int)
    putPrefs(MATS,section, 'CUT_AMPS', rC('.runs.material.cut-amps','get'), int)
    putPrefs(MATS,section, 'CUT_VOLTS', rC('.runs.material.cut-volts','get'), int)
    putPrefs(MATS,section, 'PAUSE_AT_END', rC('.runs.material.pause-at-end','get'), float)
    putPrefs(MATS,section, 'GAS_PRESSURE', rC('.runs.material.gas-pressure','get'), float)
    putPrefs(MATS,section, 'CUT_MODE', rC('.runs.material.cut-mode','get'), int)

def set_saved_material():
    matnum = int(rC('.runs.materials','get').split(':')[0])
    materialFileDict[matnum] = { \
            'name': rC('.runs.materials','get').split(':')[1], \
            'kerf_width': rC('.runs.material.kerf-width','get'), \
            'pierce_height': rC('.runs.material.pierce-height','get'), \
            'pierce_delay': rC('.runs.material.pierce-delay','get'), \
            'puddle_jump_height': rC('.runs.material.puddle-jump-height','get'), \
            'puddle_jump_delay': rC('.runs.material.puddle-jump-delay','get'), \
            'cut_height': rC('.runs.material.cut-height','get'), \
            'cut_speed': rC('.runs.material.cut-feed-rate','get'), \
            'cut_amps': rC('.runs.material.cut-amps','get'), \
            'cut_volts': rC('.runs.material.cut-volts','get'), \
            'pause_at_end': rC('.runs.material.pause-at-end','get'), \
            'gas_pressure': rC('.runs.material.gas-pressure','get'), \
            'cut_mode': rC('.runs.material.cut-mode','get')}

def get_one_material(prefs, section, matnum):
    global notifications
    title = _('MATERIALS ERROR')
    material = {}
    # we bring in some ints as floats so we can read QtPlasmaC material files
    material['name'] = getPrefs(prefs, section, 'NAME', 'Material', str)
    material['kerf_width'] = getPrefs(prefs, section, 'KERF_WIDTH', round(1 * unitsPerMm,  2), float)
    material['pierce_height'] = getPrefs(prefs, section, 'PIERCE_HEIGHT', round(3.0 * unitsPerMm,  2), float)
    material['pierce_delay'] = getPrefs(prefs, section, 'PIERCE_DELAY', 0, float)
    material['puddle_jump_height'] = int(getPrefs(prefs, section, 'PUDDLE_JUMP_HEIGHT', 0, float))
    material['puddle_jump_delay'] = getPrefs(prefs, section, 'PUDDLE_JUMP_DELAY', 0, float)
    material['cut_height'] = getPrefs(prefs, section, 'CUT_HEIGHT', round(1.0 * unitsPerMm,  2), float)
    material['cut_speed'] = int(getPrefs(prefs, section, 'CUT_SPEED', round(2540 * unitsPerMm,  0), float))
    material['cut_amps'] = int(getPrefs(prefs, section, 'CUT_AMPS', 45, float))
    material['cut_volts'] = int(getPrefs(prefs, section, 'CUT_VOLTS', 100, float))
    material['pause_at_end'] = getPrefs(prefs, section, 'PAUSE_AT_END', 0, float)
    material['gas_pressure'] = getPrefs(prefs, section, 'GAS_PRESSURE', 0, float)
    material['cut_mode'] = int(getPrefs(prefs, section, 'CUT_MODE', 1, float))
    material['valid'] = True
    required = {'pierce_height':material['pierce_height'],'cut_height':material['cut_height'],'cut_speed':material['cut_speed']}
    for item in required:
        if not required[item]:
            material['valid'] = False
            msg0 = _('is missing from Material')
            notifications.add('error','{}:\n{} {} #{}\n'.format(title, item, msg0, matnum))
    return material

def set_material_dict(materialFileDict, matnum, material):
    materialFileDict[matnum] = { \
            'name': material['name'], \
            'kerf_width': material['kerf_width'], \
            'pierce_height': material['pierce_height'], \
            'pierce_delay': material['pierce_delay'], \
            'puddle_jump_height': material['puddle_jump_height'], \
            'puddle_jump_delay': material['puddle_jump_delay'], \
            'cut_height': material['cut_height'], \
            'cut_speed': material['cut_speed'], \
            'cut_amps': material['cut_amps'], \
            'cut_volts': material['cut_volts'], \
            'pause_at_end': material['pause_at_end'], \
            'gas_pressure': material['gas_pressure'], \
            'cut_mode': material['cut_mode']}

def load_materials(mat=None):
    global getMaterialBusy, materialFileDict
    materialFileDict = {}
    getMaterialBusy = True
    if not MATS.sections():
        title = _('MATERIALS WARNING')
        msg0 = _('Creating new materials file')
        notifications.add('error', '{}:\n{}\n'.format(title, msg0))
        material = get_one_material(MATS, 'MATERIAL_NUMBER_0', 0)
        set_material_dict(materialFileDict, 0, material)
    else:
        title = _('MATERIALS ERROR')
        for section in MATS.sections():
            matnum = int(section.rsplit('_', 1)[1].strip().strip(']'))
            if matnum >= 1000000:
                msg0 = _('Material number')
                msg1 = _('is invalid')
                msg2 = _('Material numbers need to be less than 1000000')
                notifications.add('error', '{}:\n{} {} {}\n{}\n'.format(title, msg0, matnum, msg1, msg2))
                continue
            material = get_one_material(MATS, section, matnum)
            if not material['valid']:
                continue
            set_material_dict(materialFileDict, matnum, material)
        if not materialFileDict:
            msg0 = _('Materials file is empty or corrupt')
            notifications.add('error', '{}:\n{}\n'.format(title, msg0))
            return
    insert_materials()
    rC(fsetup + '.l.mats.default','configure','-values',materialNumList)
    value = getPrefs(PREF,'GUI_OPTIONS', 'Default material', materialNumList[0], int)
    pVars.matDefault.set(value)
    restoreSetup['matDefault'] = value
    if pVars.matDefault.get() not in materialNumList:
        mat = sorted(materialNumList)[0]
        title = _('MATERIALS WARNING')
        msg0 = _('Default material')
        msg1 = _('was not found')
        msg2 = _('Changing default material to')
        notifications.add('info', '{}:\n{} #{} {}\n{} #{}\n'.format(title, msg0, pVars.matDefault.get(), msg1, msg2, mat))
        pVars.matDefault.set(mat)
        putPrefs(PREF,'GUI_OPTIONS', 'Default material', pVars.matDefault.get(), int)
    index = '@{}'.format(materialNumList.index(pVars.matDefault.get()))
    rC('.runs.materials','setvalue',index)
    display_selected_material(pVars.matDefault.get())
    getMaterialBusy = False

def change_default_material():
    display_selected_material(pVars.matDefault.get())

def material_exists(material):
    global materialNumList, materialAutoChange
    if int(material) in materialNumList:
        return True
    else:
        if materialAutoChange:
            comp['material-change'] = -1
            comp['material-change-number'] = rC('.runs.materials','get').split(':')[0]
            title = _('MATERIALS ERROR')
            msg0 = _('Material')
            msg1 = _('not in material list')
            notifications.add('error', '{}:\n{} #{} {}\n'.format(title, msg0, int(material),msg1))
        return False


##############################################################################
# POWERMAX COMMUNICATIONS FUNCTIONS                                          #
##############################################################################
def pmx485_startup(port):
    global pmx485
    for parm in ['compStatus','commsError','connected','exists','meshMode']:
        pmx485[parm] = False
    for parm in ['compArcTime','compFault','commsTimer','retryTimer','oldPressure']:
        pmx485[parm] = 0.0
    for parm in ['compMinC','compMaxC','compMinP','compMaxP']:
        pmx485[parm] = 0.0
    for parm in ['oldMode']:
        pmx485[parm] = 0
    rC('grid','.runs.material.cut-mode','-column',0,'-row',20)
    rC('grid','.runs.material.cut-modeL','-column',1,'-row',20,'-sticky','W')
    rC('grid','.runs.material.gas-pressure','-column',0,'-row',21)
    rC('grid','.runs.material.gas-pressureL','-column',1,'-row',21,'-sticky','W')
    rC('grid','.runs.pmx','-column',0,'-row',10,'-sticky','new','-padx',2,'-pady',(0,2))
    if pmx485_load(port):
        return
    pmx485['exists'] = True
    pVars.pmx485Enable.set(True)
    pmx485_enable_toggled()

def pmx485_load(port):
    import subprocess
    title = _('COMMS ERROR')
    msg0 = _('PMX485 component is not able to be loaded,')
    msg1 = _('Powermax communications are not available')
    count = 0
    while not hal.component_exists('pmx485'):
        if count >= 3:
            notifications.add('error', '{}:\n{}\n{}\n'.format(title, msg0, msg1))
            return 1
        subprocess.run(['halcmd', 'loadusr', '-Wn', 'pmx485', 'pmx485', '{}'.format(port)])
        count += 1
    return 0

def pmx485_enable_toggled():
    global pmx485
    if pVars.pmx485Enable.get():
        pmx485['commsError'] = False
        pmx485['retryTimer'] == 0
        if pmx485_load(pmPort):
            return
        # ensure valid parameters before trying to connect
        if pVars.cutMode.get() == 0 or pVars.cutAmps.get() == 0:
            title = _('MATERIALS ERROR')
            msg0 = _('Invalid Cut Mode or Cut Amps')
            msg1 = _('cannot connect to Powermax')
            notifications.add('error', '{}:\n{}\n{}\n'.format(title, msg0, msg1))
            pVars.pmx485Enable.set(False)
            return
        # good to go
        else:
            hal.set_p('pmx485.pressure_set', str(pVars.gasPressure.get()))
            hal.set_p('pmx485.current_set', str(pVars.cutAmps.get()))
            hal.set_p('pmx485.mode_set', str(pVars.cutMode.get()))
            hal.set_p('pmx485.enable', '1')
            rC('.runs.pmx.info','configure','-text','CONNECTING')
            pmx485['commsTimer'] = 3
    else:
        hal.set_p('pmx485.enable', '0')
        pmx485['connected'] = False
        pmx485['commsError'] = False
        pmx485['commsTimer'] == 0
        pmx485['retryTimer'] == 0
        rC('.runs.pmx.info','configure','-text','')

def pmx485_current_changed(value):
    hal.set_p('pmx485.current_set', str(value))

def pmx485_mode_changed(value):
    pVars.gasPressure.set(0)
    hal.set_p('pmx485.pressure_set', '0')
    hal.set_p('pmx485.mode_set', str(value))

def pmx485_pressure_changed(value):
    if value > 0 and value < int(hal.get_value('pmx485.pressure_min') / 2):
        pVars.gasPressure.set(int(hal.get_value('pmx485.pressure_min')))
    elif value > int(hal.get_value('pmx485.pressure_min') / 2)  and value < hal.get_value('pmx485.pressure_min'):
        pVars.gasPressure.set(0)
    else:
        pVars.gasPressure.set(float(value))
    hal.set_p('pmx485.pressure_set', str(pVars.gasPressure.get()))

def pmx485_min_current_changed():
    rC('.runs.material.cut-amps','configure','-from',hal.get_value('pmx485.current_min'))

def pmx485_max_current_changed():
    rC('.runs.material.cut-amps','configure','-to',hal.get_value('pmx485.current_max'))

def pmx485_max_pressure_changed():
    rC('.runs.material.gas-pressure','configure','-to',hal.get_value('pmx485.pressure_max'))
    if float(hal.get_value('pmx485.pressure_max')) > 15:
        rC('.runs.material.gas-pressureL','configure','-text','Gas Pressure psi')
        rC('.runs.material.gas-pressure','configure','-increment',1,'-format','%0.0f')
    else:
        rC('.runs.material.gas-pressureL','configure','-text','Gas Pressure bar')
        rC('.runs.material.gas-pressure','configure','-increment',0.1,'-format','%0.1f')

def pmx485_status_changed(state):
    global pmx485
    if state != pmx485['connected']:
        if state:
            pmx485['commsError'] = False
            rC('.runs.pmx.info','configure','-text','CONNECTED')
            pmx485['connected'] = True
            # probably not required as we change the text directly in periodic
            #if pmx485['compArcTime']:
            #    pmx485_arc_time_changed(pmx485['compArcTime'])
            # probably not required as we check the fault in periodic
            #if hal.get_value('pmx485.fault'):
            #    pmx485_fault_changed(hal.get_value('pmx485.fault'))
            pmx485['commsTimer'] = 0
            pmx485['retryTimer'] = 0
        else:
            rC('.runs.pmx.info','configure','-text','COMMS ERROR')
            pmx485['commsError'] = True
            pmx485['connected'] = False
            pmx485['retryTimer'] = 3

#FIXME: PROBABLY NOT REQUIRED AS WE CHANGE THE TEXT IN PERIODIC
#def pmx485_arc_time_changed(time):
#    print('pmx485_arc_time_changed', time)
#    if pmx485['connected']:
#        pass
#        self.w.pmx_stats_frame.show()
#        self.w.pmx_arc_time_label.setText(_translate('HandlerClass', 'ARC ON TIME'))
#        self.display_time('pmx_arc_time_t', time)

def pmx485_fault_changed(fault):
    global pmx485
    if pmx485['connected']:
        faultRaw = '{:04.0f}'.format(fault)
        pmx485['compFaultCode'] = '{}-{}-{}'.format(faultRaw[0], faultRaw[1:3], faultRaw[3])
        title = _('POWERMAX ERROR')
        code = _('Fault Code')
        text = _('Powermax error')
        if faultRaw == '0000':
            rC('.runs.pmx.info','configure','-text','CONNECTED')
        elif faultRaw in pmx485FaultName.keys():
            if faultRaw == '0210' and hal.get_value('pmx485.current_max') > 110:
                faultMsg = pmx485FaultName[faultRaw][1]
            elif faultRaw == '0210':
                faultMsg = pmx485FaultName[faultRaw][0]
            else:
                faultMsg = pmx485FaultName[faultRaw]
            rC('.runs.pmx.info','configure','-text','{}: {}'.format(code, pmx485['compFaultCode']))
            msg0 = _('Code')
            notifications.add('error', '{}:\n{}: {}\n{}\n'.format(title, msg0, pmx485['compFaultCode'], faultMsg))
        else:
            rC('.runs.pmx.info','configure','-text','{}: {}'.format(code, pmx485['compFaultCode']))
            pmx485['labelState'] = None
            msg0 = _('Unknown Powermax fault code')
            notifications.add('error', '{}:\n{}: {}\n'.format(title, msg0, faultRaw))

def pmx485_mesh_enable_toggled():
    global pmx485
    if pVars.meshEnable.get() and not pmx485['meshMode']:
        pmx485['oldMode'] = pVars.cutMode.get()
        pVars.cutMode.set(2)
        rC('.runs.material.cut-mode','configure','-state','disabled')
        pmx485['meshMode'] = True
        hal.set_p('plasmac.mesh-enable', '1')
    elif not hal.get_value('plasmac.mesh-enable') and pmx485['meshMode']:
        pVars.cutMode.set(pmx485['oldMode'])
        rC('.runs.material.cut-mode','configure','-state','normal')
        pmx485['meshMode'] = False
        hal.set_p('plasmac.mesh-enable', '0')

def pmx485_comms_timeout():
    global pmx485
    rC('.runs.pmx.info','configure','-text',_('COMMS ERROR'))
    pmx485['commsError'] = True
    pmx485['connected'] = False
    pmx485['retryTimer'] = 3

def pmx485_retry_timeout():
    pmx485_enable_toggled()

pmx485FaultName = {
            '0110': _('Remote controller mode invalid'),
            '0111': _('Remote controller current invalid'),
            '0112': _('Remote controller pressure invalid'),
            '0120': _('Low input gas pressure'),
            '0121': _('Output gas pressure low'),
            '0122': _('Output gas pressure high'),
            '0123': _('Output gas pressure unstable'),
            '0130': _('AC input power unstable'),
            '0199': _('Power board hardware protection'),
            '0200': _('Low gas pressure'),
            '0210': (_('Gas flow lost while cutting'), _('Excessive arc voltage')),
            '0220': _('No gas input'),
            '0300': _('Torch stuck open'),
            '0301': _('Torch stuck closed'),
            '0320': _('End of consumable life'),
            '0400': _('PFC/Boost IGBT module under temperature'),
            '0401': _('PFC/Boost IGBT module over temperature'),
            '0402': _('Inverter IGBT module under temperature'),
            '0403': _('Inverter IGBT module over temperature'),
            '0500': _('Retaining cap off'),
            '0510': _('Start/trigger signal on at power up'),
            '0520': _('Torch not connected'),
            '0600': _('AC input voltage phase loss'),
            '0601': _('AC input voltage too low'),
            '0602': _('AC input voltage too high'),
            '0610': _('AC input unstable'),
            '0980': _('Internal communication failure'),
            '0990': _('System hardware fault'),
            '1000': _('Digital signal processor fault'),
            '1100': _('A/D converter fault'),
            '1200': _('I/O fault'),
            '2000': _('A/D converter value out of range'),
            '2010': _('Auxiliary switch disconnected'),
            '2100': _('Inverter module temp sensor open'),
            '2101': _('Inverter module temp sensor shorted'),
            '2110': _('Pressure sensor is open'),
            '2111': _('Pressure sensor is shorted'),
            '2200': _('DSP does not recognize the torch'),
            '3000': _('Bus voltage fault'),
            '3100': _('Fan speed fault'),
            '3101': _('Fan fault'),
            '3110': _('PFC module temperature sensor open'),
            '3111': _('PFC module temperature sensor shorted'),
            '3112': _('PFC module temperature sensor circuit fault'),
            '3200': _('Fill valve'),
            '3201': _('Dump valve'),
            '3201': _('Valve ID'),
            '3203': _('Electronic regulator is disconnected'),
            '3410': _('Drive fault'),
            '3420': _('5 or 24 VDC fault'),
            '3421': _('18 VDC fault'),
            '3430': _('Inverter capacitors unbalanced'),
            '3441': _('PFC over current'),
            '3511': _('Inverter saturation fault'),
            '3520': _('Inverter shoot-through fault'),
            '3600': _('Power board fault'),
            '3700': _('Internal serial communications fault'),
            }


##############################################################################
# SETUP                                                                      #
##############################################################################
firstRun = 'valid'
if os.path.isdir(os.path.expanduser('~/linuxcnc/plasmac2/lib')):
    libPath = os.path.expanduser('~/linuxcnc/plasmac2/lib')
    sys.path.append(libPath)

    import tarfile
    from tkinter import messagebox
    from tkinter import simpledialog
    from math import radians, atan, degrees
    from collections import OrderedDict
    from glob import glob as GLOB
    from shutil import copy as COPY
    from importlib import reload
    from plasmac import run_from_line as RFL
    import conversational
    import set_offsets

    configPath = os.getcwd()
    imagePath = os.path.join(libPath, 'images') # our own images
    imageAxis = os.path.join(BASE, 'share', 'axis', 'images') # images pinched from Axis
    if not os.path.isdir('/tmp/plasmac'):
        os.mkdir('/tmp/plasmac')
    tmpPath = '/tmp/plasmac'

    # not used:
    #installType = 'pkg' if os.path.dirname(os.path.realpath(__file__)) == '/bin' else 'rip'

    # not used:
    # use a non existant file name so Axis doesn't open a default file
    # only usefull if we move the file open code in Axis so it it called after the user command file is called
    #args = ['do_not_open_a_file']

    VER = '2.0'
    PREF = plasmacPreferences()
    MATS = plasmacMaterials()
    TEMP = plasmacTempMaterial()
    rC = root_window.tk.call
    rE = root_window.tk.eval
    # set the default font
    fontName = 'sans'
    fontSize = startFontSize = '10'
    # some color names
    ourRed = '#DD0000'
    ourGreen = '#00CC00'
    ourOrange = '#FFAA00'
    ourYellow = '#FFFF00'
    ourBlue = '#0000FF'
    ourWhite = '#FFFFFF'
    ourGray = '#AAAAAA'
    ourBlack = '#000000'
    # make some widget names to save typing
    ftop = '.pane.top'
    ftabs = ftop + '.tabs'
    fright = ftop + '.right'
    fmanual = ftabs + '.fmanual'
    faxes = fmanual + '.axes'
    fjoints = fmanual + '.joints'
    fjogf = fmanual + '.jogf'
    foverride = fmanual + '.override'
    flimitovr = fmanual + '.jogf.limitovr'
    fjogiovr = fmanual + '.jogf.inhibitovr'
    fplasma = fmanual + '.plasma'
    farcv = fplasma + '.arcv'
    fthc = fplasma + '.thc'
    fmdi = ftabs + '.fmdi'
    ft = '.pane.bottom.t'
    fleds = '.pane.bottom.leds'
    fcutrecs = ftabs + '.fcutrecs'
    fcutrec = fcutrecs + '.pm'
    fleadins = fcutrecs + '.leadins'
    fparam = '.param'
    fsetup = '.setup'
    wLeds = [fleds + '.led-arc-ok',\
             fleds + '.led-torch',\
             fleds + '.led-thc-enabled',\
             fleds + '.led-ohmic',\
             fleds + '.led-float',\
             fleds + '.led-breakaway',\
             fleds + '.led-thc-active',\
             fleds + '.led-up',\
             fleds + '.led-down',\
             fleds + '.led-corner-locked',\
             fleds + '.led-kerf-locked',\
            ]
    wCombos = [fsetup + '.l.gui.wsize',\
               fsetup + '.l.mats.default',\
               '.runs.materials',\
              ]
    # recreate widget list to move active gcodes and add new widgets
    widget_list_new = []
    for l in widget_list:
        if '.gcodes' in l[2]:
            l = ('code_text', Text, '.info.gcodef.gcodes')
        widget_list_new.append(l)
    widget_list_new.append(('buttonFrame', Frame, '.fbuttons'))
    widget_list_new.append(('convFrame', Frame, '.fconv'))
    widget_list_new.append(('toolFrame', Frame, '.toolconv'))
    widget_list_new.append(('materials', bwidget.ComboBox, '.runs.materials'))
    widget_list_new.append(('kerfWidth', Spinbox, '.runs.material.kerf-width'))
    widget_list_new.append(('view_t', Button, '.toolbar.view_t'))
    widgets = nf.Widgets(root_window, *widget_list_new)
    # tk widget variables
    pVars = nf.Variables(root_window,
             ('plasmatool', StringVar),
             ('thcEnable', BooleanVar),
             ('cornerEnable', BooleanVar),
             ('kerfEnable', BooleanVar),
             ('autoVolts', BooleanVar),
             ('ohmicEnable', BooleanVar),
             ('meshEnable', BooleanVar),
             ('ignorArcOk', BooleanVar),
             ('closeDialog', BooleanVar),
             ('winSize', StringVar),
             ('startLine', IntVar),
             ('rflActive', BooleanVar),
             ('preRflFile', StringVar),
             ('laserText', StringVar),
             ('crSpeed', IntVar),
             ('previewLarge', BooleanVar),
             ('jogSpeed', DoubleVar),
             ('plasmacMode', IntVar),
             ('fontSize', StringVar),
             ('coneSize', DoubleVar),
             ('kerfWidth', DoubleVar),
             ('cutAmps', IntVar),
             ('cutMode', IntVar),
             ('gasPressure', DoubleVar),
             ('pmx485Enable', BooleanVar),
             ('max_speed_units', DoubleVar),
             ('convButton', IntVar),
             ('preConvFile', IntVar),
             ('lengthJ', StringVar),
             ('lengthT', StringVar),
             ('lengthS', DoubleVar),
             ('pierceJ', StringVar),
             ('pierceT', StringVar),
             ('pierceS', IntVar),
             ('rapidJ', StringVar),
             ('rapidT', StringVar),
             ('rapidS', IntVar),
             ('probeJ', StringVar),
             ('probeT', StringVar),
             ('probeS', IntVar),
             ('torchJ', StringVar),
             ('torchT', StringVar),
             ('torchS', IntVar),
             ('cutJ', StringVar),
             ('cutT', StringVar),
             ('cutS', IntVar),
             ('pausedJ', StringVar),
             ('pausedT', StringVar),
             ('pausedS', IntVar),
             ('runJ', StringVar),
             ('runT', StringVar),
             ('runS', IntVar),
             ('probeJ', StringVar),
             ('probeT', StringVar),
             ('probeS', IntVar),
             ('arcT', StringVar),
             ('jiOverride', BooleanVar),
             ('matDefault', IntVar),
             ('jogInhibitOvr', IntVar),
             ('limitOvr', IntVar),
             )
    restoreSetup = {}
    pVars.plasmacMode.set(getPrefs(PREF,'GUI_OPTIONS', 'Mode', 0, int))
    restoreSetup['plasmacMode'] = pVars.plasmacMode.get()
    pVars.fontSize.set(getPrefs(PREF,'GUI_OPTIONS','Font size', '10', str))
    restoreSetup['fontSize'] = pVars.fontSize.get()
    thcFeedRate = round((float(inifile.find('AXIS_Z', 'MAX_VELOCITY')) * float(inifile.find('AXIS_Z', 'OFFSET_AV_RATIO'))) * 60, 3)
    maxHeight = round(hal.get_value('ini.z.max_limit') - hal.get_value('ini.z.min_limit'), 3)
    unitsPerMm = hal.get_value('halui.machine.units-per-mm')
    isIdle = False
    isIdleHomed = False
    isPaused = False
    isRunning = False
    getMaterialBusy = False
    materialFileDict = {}
    materialNumList = []
    materialList = [] # this  may be deleted, duplicate of materialNumList
    materialName = '' # this  may be deleted,  not used
    materialAutoChange = False
    materialChangePin = materialChangeNumberPin = materialChangeTimeoutPin = materialReloadPin = materialTempPin = 0
    probePressed = False
    probeTimer = 0
    probeButton = ''
    probeStart = 0
    torchPressed = False
    torchTimer = 0
    torchButton = ''
    torchStart = 0
    torchHeight = 0
    cChangeButton = ''
    cutType = 0
    togglePins = {}
    pulsePins = {}
    currentTool = None
    manualCut = {'state':False, 'feed':vars.jog_speed.get()}
    singleCut = {'state':False, 'G91':False}
    framingState = False
    runState = False
    torchEnable = {}
    torchEnable['enabled'] = getPrefs(PREF,'BUTTONS', 'Torch enabled', 'Torch\Enabled', str)
    torchEnable['disabled'] = getPrefs(PREF,'BUTTONS','Torch disabled', 'Torch\Disabled', str)
    laserTimer = 0.0
    laserButtonState = 'laser'
    laserOffsets = {}
    laserOffsets['X'] = getPrefs(PREF,'LASER_OFFSET', 'X axis', 0, float)
    laserOffsets['Y'] = getPrefs(PREF,'LASER_OFFSET', 'Y axis', 0, float)
    probeOffsets = {}
    probeOffsets['X'] = getPrefs(PREF, 'OFFSET_PROBING', 'X axis', 0, float)
    probeOffsets['Y'] = getPrefs(PREF, 'OFFSET_PROBING', 'Y axis', 0, float)
    probeOffsets['Delay'] = getPrefs(PREF, 'OFFSET_PROBING', 'Delay', 0, float)
    machineBounds = {}
    machineBounds['X-'] = round(float(inifile.find('AXIS_X', 'MIN_LIMIT')), 6)
    machineBounds['X+'] = round(float(inifile.find('AXIS_X', 'MAX_LIMIT')), 6)
    machineBounds['Y-'] = round(float(inifile.find('AXIS_Y', 'MIN_LIMIT')), 6)
    machineBounds['Y+'] = round(float(inifile.find('AXIS_Y', 'MAX_LIMIT')), 6)
    machineBounds['Z-'] = round(float(inifile.find('AXIS_Z', 'MIN_LIMIT')), 6)
    machineBounds['Z+'] = round(float(inifile.find('AXIS_Z', 'MAX_LIMIT')), 6)
    machineBounds['xLen'] = machineBounds['X+'] - machineBounds['X-']
    machineBounds['yLen'] = machineBounds['Y+'] - machineBounds['Y-']
    machineBounds['zLen'] = machineBounds['Z+'] - machineBounds['Z-']
    startAlignPos = {X:0, Y:0}
    relPos = {X:0, Y:0}
    activeFunction = False
    pausedState = False
    convFirstRun = True
    convViewOptions = {}
    lastViewType = None
    preConvFile = os.path.join(tmpPath, 'pre_conv.ngc')
    pmx485 = {'exists':False}
    spinBoxes = []
    widgetValues = {}
    statValues = {'length':0, 'pierce':0, 'rapid':0, 'probe':0, 'torch':0, 'cut':0, 'paused':0, 'run':0}
    gcodeProperties = None
    # get the default button background colors
    buttonBackG = rC(fjogf + '.jog.jogminus','cget','-bg')
    buttonActBackG = rC(fjogf + '.jog.jogminus','cget','-activebackground')
    toolButtons  = ['machine_estop','machine_power','file_open','reload','program_run',
                    'program_step','program_pause','program_stop','program_blockdelete',
                    'program_optpause','view_zoomin','view_zoomout','view_z','view_z2',
                    'view_x','view_y','view_y2','view_p','rotate','clear_plot']
    matButtons   = ['delete','new','reload','save']
    # spinbox validator
    valspin = root_window.register(validate_spinbox)
    # monkeypatched functions
    o.get_view = get_view # axis.py
    o.draw_grid = draw_grid # glcanon.py
    # tcl called functions hijacked from axis.py
    TclCommands.reload_file = reload_file
    TclCommands.task_run_line = task_run_line
    TclCommands.task_stop = task_stop
    TclCommands.open_file_name = open_file_name
    TclCommands.gcode_properties = gcode_properties
    TclCommands.set_view_p = set_view_p
    TclCommands.set_view_z = set_view_z
    # tcl functions hijacked from axis.tcl
    TclCommands.update_title = update_title
    TclCommands.update_jog_slider_vel = update_jog_slider_vel
    # new functions
    TclCommands.set_view_t = set_view_t
    TclCommands.param_changed = param_changed
    TclCommands.material_changed = material_changed
    TclCommands.save_material_clicked = save_material_clicked
    TclCommands.reload_material_clicked = reload_material_clicked
    TclCommands.new_material_clicked = new_material_clicked
    TclCommands.delete_material_clicked = delete_material_clicked
    TclCommands.change_default_material = change_default_material
    TclCommands.save_param_clicked = save_param_clicked
    TclCommands.load_param_clicked = load_param_clicked
    TclCommands.backup_clicked = backup_clicked
    TclCommands.save_setup_clicked = save_setup_clicked
    TclCommands.load_setup_clicked = load_setup_clicked
    TclCommands.user_button_add = user_button_add
    TclCommands.preview_toggle = preview_toggle
    TclCommands.setup_toggle = setup_toggle
    TclCommands.param_toggle = param_toggle
    TclCommands.conv_toggle = conv_toggle
    TclCommands.thc_enable_toggled = thc_enable_toggled
    TclCommands.corner_enable_toggled = corner_enable_toggled
    TclCommands.kerf_enable_toggled = kerf_enable_toggled
    TclCommands.auto_volts_toggled = auto_volts_toggled
    TclCommands.ohmic_enable_toggled = ohmic_enable_toggled
    TclCommands.ignore_arc_ok_toggled = ignore_arc_ok_toggled
    TclCommands.close_window = close_window
    TclCommands.set_window_size = set_window_size
    TclCommands.button_action = button_action
    TclCommands.mode_changed = mode_changed
    TclCommands.font_size_changed = font_size_changed
    TclCommands.cone_size_changed = cone_size_changed
    TclCommands.height_raise = height_raise
    TclCommands.height_lower = height_lower
    TclCommands.height_reset = height_reset
    TclCommands.torch_enable = torch_enable
    TclCommands.joint_mode_switch = joint_mode_switch
    TclCommands.ja_button_activated = ja_button_activated
    TclCommands.manual_cut = manual_cut
    TclCommands.touch_off_xy = touch_off_xy
    TclCommands.laser_button_toggled = laser_button_toggled
    TclCommands.cut_rec_motion = cut_rec_motion
    TclCommands.cut_rec_default_changed = cut_rec_default_changed
    TclCommands.cut_rec_slider_changed = cut_rec_slider_changed
    TclCommands.cut_rec_move = cut_rec_move
    TclCommands.cut_rec_cancel = cut_rec_cancel
    TclCommands.pmx485_mode_changed = pmx485_mode_changed
    TclCommands.pmx485_pressure_changed = pmx485_pressure_changed
    TclCommands.pmx485_enable_toggled = pmx485_enable_toggled
    TclCommands.pmx485_mesh_enable_toggled = pmx485_mesh_enable_toggled
    TclCommands.reset_all_stats = reset_all_stats
    TclCommands.set_peripheral_offsets = set_peripheral_offsets
    commands = TclCommands(root_window)


##############################################################################
# GUI ALTERATIONS AND ADDITIONS                                              #
##############################################################################
    # change dro screen colors
    rC('.pane.top.right.fnumbers.text','configure','-foreground',ourGreen,'-background',ourBlack)

    # keep tab label sizes the same
    rC(ftabs,'configure','-homogeneous',True)
    rC(fright,'configure','-homogeneous',True)

    # hide some existing widgets
    rC('pack','forget','.toolbar.rule9')
    rC('pack','forget','.toolbar.view_zoomin')
    rC('pack','forget','.toolbar.view_zoomout')
    rC('pack','forget','.toolbar.view_z')
    rC('pack','forget','.toolbar.view_z2')
    rC('pack','forget','.toolbar.view_x')
    rC('pack','forget','.toolbar.view_y')
    rC('pack','forget','.toolbar.view_y2')
    rC('pack','forget','.toolbar.view_p')
    rC('pack','forget','.toolbar.rotate')
    rC('pack','forget','.toolbar.rule12')
    rC('pack','forget','.toolbar.clear_plot')
    rC('grid','forget',fmanual + '.axis')
    rC('grid','forget',fmanual + '.jogf')
    rC('grid','forget',fmanual + '.space1')
    rC('grid','forget',fmanual + '.spindlel')
    rC('grid','forget',fmanual + '.spindlef')
    rC('grid','forget',fmanual + '.space2')
    rC('grid','forget',fmanual + '.coolant')
    rC('grid','forget',fmanual + '.mist')
    rC('grid','forget',fmanual + '.flood')
    rC('pack','forget',ftop + '.jogspeed.l1')
    rC('grid','forget',ftop + '.spinoverride')
    rC('grid','forget',ftop + '.maxvel')

    # modify the toolbar
    rC('vrule','.toolbar.rule10')
    rC('vrule','.toolbar.rule11')
    rC('pack','.toolbar.rule9','-side','left','-padx',(66,4),'-pady',4,'-fill','y')
    rC('pack','.toolbar.clear_plot','-side','left')
    rC('pack','.toolbar.rule10','-side','left','-padx',4,'-pady',4,'-fill','y')
    rC('pack','.toolbar.view_z','-side','left')
    rC('pack','.toolbar.view_p','-side','left')
    rC('Button','.toolbar.view_t','-text','T','-command','set_view_t','-relief','link','-takefocus',0)
    rC('pack','.toolbar.view_t','-side','left')
    rC('pack','.toolbar.rule11','-side','left','-padx',4,'-pady',4,'-fill','y')
    rC('pack','.toolbar.view_zoomout','-side','left')
    rC('pack','.toolbar.view_zoomin','-side','left')
    rC('pack','.toolbar.rule12','-side','left','-padx',4,'-pady',4,'-fill','y')
    rC('pack','.toolbar.rotate','-side','left')
    rC('.toolbar.rotate','configure','-takefocus',0)

    # new setup toolbar
    # create widgets
    rC('frame','.toolsetup','-borderwidth',1,'-relief','raised')
    rC('Button','.toolsetup.save','-command','save_setup_clicked','-width',8,'-takefocus',0,'-text',_('Save All'),'-padx',0)
    rC('Button','.toolsetup.reload','-command','load_setup_clicked','-width',8,'-takefocus',0,'-text',_('Reload'),'-padx',0)
    rC('Button','.toolsetup.add','-command','user_button_add','-width',8,'-takefocus',0,'-text',_('Add'),'-padx',0)
    rC('Button','.toolsetup.bkp','-command','backup_clicked','-width',8,'-takefocus',0,'-text',_('Backup'),'-padx',0)
    rC('Button','.toolsetup.close','-command','setup_toggle 0','-width',8,'-takefocus',0,'-text',_('Close'),'-padx',0)
    # populate the tool bar
    rC('pack','.toolsetup.save','-side','left')
    rC('pack','.toolsetup.reload','-side','left','-padx',(8,0))
    rC('pack','.toolsetup.add','-side','left','-padx',(8,0))
    rC('pack','.toolsetup.bkp','-side','left','-padx',(8,0))
    rC('pack','.toolsetup.close','-side','left','-padx',(16,0))
    rC('grid','forget','.toolsetup')

    # new parameters toolbar
    # create widgets
    rC('frame','.toolparam','-borderwidth',1,'-relief','raised')
    rC('Button','.toolparam.save','-command','save_param_clicked','-width',8,'-takefocus',0,'-text',_('Save All'),'-padx',0)
    rC('Button','.toolparam.reload','-command','load_param_clicked','-width',8,'-takefocus',0,'-text',_('Reload'),'-padx',0)
    rC('Button','.toolparam.close','-command','param_toggle 0','-width',8,'-takefocus',0,'-text',_('Close'),'-padx',0)
    # populate the tool bar
    rC('pack','.toolparam.save','-side','left')
    rC('pack','.toolparam.reload','-side','left','-padx',(8,0))
    rC('pack','.toolparam.close','-side','left','-padx',(16,0))
    rC('grid','forget','.toolparam')

    # new material toolbar
    # create widgets
    rC('frame','.toolmat','-borderwidth',1,'-relief','raised')
    rC('Button','.toolmat.delete','-command','delete_material_clicked','-relief','link','-takefocus',0)
    rC('Button','.toolmat.new','-command','new_material_clicked','-relief','link','-takefocus',0)
    rC('Button','.toolmat.reload','-command','reload_material_clicked','-relief','link','-takefocus',0)
    rC('Button','.toolmat.save','-command','save_material_clicked','-relief','link','-takefocus',0)
    # add images
    rC('.toolmat.delete','configure','-image',rC('load_image',imageAxis + '/tool_zoomout'))
    rC('.toolmat.new','configure','-image',rC('load_image',imageAxis + '/tool_zoomin'))
    rC('.toolmat.reload','configure','-image',rC('load_image',imageAxis + '/tool_reload'))
    rC('.toolmat.save','configure','-image',rC('load_image',imagePath + '/save'))
    # populate the tool bar
    rC('pack','.toolmat.save','-side','left','-padx',(0,4))
    rC('pack','.toolmat.reload','-side','left')
    rC('pack','.toolmat.delete','-side','right','-padx',(4,0))
    rC('pack','.toolmat.new','-side','right')
    rC('grid','.toolmat','-column',3,'-row',0,'-sticky','nesw')

    # new statistics page
    rC(fright,'insert','end','stats','-text',_('Statistics'))
    rC(fright + '.fstats','configure','-bd',2)
    stats = fright + '.fstats.statistics'
    rC('labelframe',stats,'-relief','groove')
    rC('label',stats + '.itemL','-text',_('Item'),'-width',16,'-anchor','e')
    rC('label',stats + '.jobL','-text',_('Job'),'-width',10,'-anchor','e')
    rC('label',stats + '.totalL','-text',_('Total'),'-width',10,'-anchor','e')
    rC('label',stats + '.lengthL','-text',_('Cut Length'),'-width',16,'-anchor','e')
    rC('label',stats + '.lengthJ','-textvariable','lengthJ','-width',10,'-anchor','e')
    rC('label',stats + '.lengthT','-textvariable','lengthT','-width',10,'-anchor','e')
    rC('button',stats + '.lengthB','-command','reset_all_stats length','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.pierceL','-text',_('Torch Starts'),'-width',16,'-anchor','e')
    rC('label',stats + '.pierceJ','-textvariable','pierceJ','-width',10,'-anchor','e')
    rC('label',stats + '.pierceT','-textvariable','pierceT','-width',10,'-anchor','e')
    rC('button',stats + '.pierceB','-command','reset_all_stats pierce','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.rapidL','-text',_('Rapid Time'),'-width',16,'-anchor','e')
    rC('label',stats + '.rapidJ','-textvariable','rapidJ','-width',10,'-anchor','e')
    rC('label',stats + '.rapidT','-textvariable','rapidT','-width',10,'-anchor','e')
    rC('button',stats + '.rapidB','-command','reset_all_stats rapid','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.probeL','-text',_('Probe Time'),'-width',16,'-anchor','e')
    rC('label',stats + '.probeJ','-textvariable','probeJ','-width',10,'-anchor','e')
    rC('label',stats + '.probeT','-textvariable','probeT','-width',10,'-anchor','e')
    rC('button',stats + '.probeB','-command','reset_all_stats probe','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.torchL','-text',_('Torch On Time'),'-width',16,'-anchor','e')
    rC('label',stats + '.torchJ','-textvariable','torchJ','-width',10,'-anchor','e')
    rC('label',stats + '.torchT','-textvariable','torchT','-width',10,'-anchor','e')
    rC('button',stats + '.torchB','-command','reset_all_stats torch','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.cutL','-text',_('Cutting Time'),'-width',16,'-anchor','e')
    rC('label',stats + '.cutJ','-textvariable','cutJ','-width',10,'-anchor','e')
    rC('label',stats + '.cutT','-textvariable','cutT','-width',10,'-anchor','e')
    rC('button',stats + '.cutB','-command','reset_all_stats cut','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.pausedL','-text',_('Paused Time'),'-width',16,'-anchor','e')
    rC('label',stats + '.pausedJ','-textvariable','pausedJ','-width',10,'-anchor','e')
    rC('label',stats + '.pausedT','-textvariable','pausedT','-width',10,'-anchor','e')
    rC('button',stats + '.pausedB','-command','reset_all_stats paused','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.runL','-text',_('Total Run Time'),'-width',16,'-anchor','e')
    rC('label',stats + '.runJ','-textvariable','runJ','-width',10,'-anchor','e')
    rC('label',stats + '.runT','-textvariable','runT','-width',10,'-anchor','e')
    rC('button',stats + '.runB','-command','reset_all_stats run','-text',_('Reset'),'-pady',0)
    rC('label',stats + '.arcL','-text',_('Arc On Time'),'-width',16,'-anchor','e')
    rC('label',stats + '.arcT','-textvariable','arcT','-width',10,'-anchor','e')
    rC('grid',stats + '.itemL','-column',0,'-row',0)
    rC('grid',stats + '.jobL','-column',1,'-row',0)
    rC('grid',stats + '.totalL','-column',2,'-row',0)
    rC('grid',stats + '.lengthL','-column',0,'-row',1,'-pady',(8,0))
    rC('grid',stats + '.lengthJ','-column',1,'-row',1,'-pady',(8,0))
    rC('grid',stats + '.lengthT','-column',2,'-row',1,'-pady',(8,0))
    rC('grid',stats + '.lengthB','-column',3,'-row',1,'-padx',(16,0),'-pady',(8,0))
    rC('grid',stats + '.pierceL','-column',0,'-row',2,'-pady',(8,0))
    rC('grid',stats + '.pierceJ','-column',1,'-row',2,'-pady',(8,0))
    rC('grid',stats + '.pierceT','-column',2,'-row',2,'-pady',(8,0))
    rC('grid',stats + '.pierceB','-column',3,'-row',2,'-padx',(16,0),'-pady',(8,0))
    rC('grid',stats + '.rapidL','-column',0,'-row',3,'-pady',(8,0))
    rC('grid',stats + '.rapidJ','-column',1,'-row',3,'-pady',(8,0))
    rC('grid',stats + '.rapidT','-column',2,'-row',3,'-pady',(8,0))
    rC('grid',stats + '.rapidB','-column',3,'-row',3,'-padx',(16,0),'-pady',(8,0))
    rC('grid',stats + '.probeL','-column',0,'-row',4,'-pady',(8,0))
    rC('grid',stats + '.probeJ','-column',1,'-row',4,'-pady',(8,0))
    rC('grid',stats + '.probeT','-column',2,'-row',4,'-pady',(8,0))
    rC('grid',stats + '.probeB','-column',3,'-row',4,'-padx',(16,0),'-pady',(8,0))
    rC('grid',stats + '.torchL','-column',0,'-row',5,'-pady',(8,0))
    rC('grid',stats + '.torchJ','-column',1,'-row',5,'-pady',(8,0))
    rC('grid',stats + '.torchT','-column',2,'-row',5,'-pady',(8,0))
    rC('grid',stats + '.torchB','-column',3,'-row',5,'-padx',(16,0),'-pady',(8,0))
    rC('grid',stats + '.cutL','-column',0,'-row',6,'-pady',(8,0))
    rC('grid',stats + '.cutJ','-column',1,'-row',6,'-pady',(8,0))
    rC('grid',stats + '.cutT','-column',2,'-row',6,'-pady',(8,0))
    rC('grid',stats + '.cutB','-column',3,'-row',6,'-padx',(16,0),'-pady',(8,0))
    rC('grid',stats + '.pausedL','-column',0,'-row',7,'-pady',(8,0))
    rC('grid',stats + '.pausedJ','-column',1,'-row',7,'-pady',(8,0))
    rC('grid',stats + '.pausedT','-column',2,'-row',7,'-pady',(8,0))
    rC('grid',stats + '.pausedB','-column',3,'-row',7,'-padx',(16,0),'-pady',(8,0))
    rC('grid',stats + '.runL','-column',0,'-row',8,'-pady',(8,0))
    rC('grid',stats + '.runJ','-column',1,'-row',8,'-pady',(8,0))
    rC('grid',stats + '.runT','-column',2,'-row',8,'-pady',(8,0))
    rC('grid',stats + '.runB','-column',3,'-row',8,'-padx',(16,0),'-pady',(8,0))
    rC('pack',stats,'-fill','both','-expand',True,'-padx',2,'-pady',2)

    # destroy existing axes and joints
    rC('destroy',faxes)
    rC('destroy',fjoints)
    # create widgets
    rC('labelframe',faxes,'-text',_('Axis:'),'-relief','flat','-bd',0)
    rC('labelframe',fjoints,'-text',_('Joint:'),'-relief','flat','-bd',0)
    # make joints radiobuttons
    for number in range(0,linuxcnc.MAX_JOINTS):
        ja_button_setup(fjoints + '.joint' + str(number), number, number)
    # populate joints frame
    count = 0
    for row in range(0,2):
        for column in range(0,5):
            if count == jointcount: break
            pad = (0,0) if column == 0 else (8,0)
            rC('grid',fjoints + '.joint' + str(count),'-row',row,'-column',column,'-padx',pad)
            count += 1
    # make axis radiobuttons
    for letter in 'xyzabcuvw':
        ja_button_setup(faxes + '.axis' + letter, letter, letter.upper())
    # populate the axes frame
    count = 0
    letters = 'xyzabcuvw'
    first_axis = ''
    for row in range(0,2):
        for column in range(0,5):
            if letters[count] in trajcoordinates:
                if first_axis == '':
                    first_axis = letters[count]
                pad = (0,0) if column == 0 else (8,0)
                rC('grid',faxes + '.axis' + letters[count],'-row',row,'-column',column,'-padx',pad)
            count += 1
            if count == 9: break

    # rework the jogf frame
    rC('destroy',fjogf)
    # create the widgets
    rC('frame',fjogf)
    rC('labelframe',fjogf + '.jog','-text',_('Jog:'),'-relief','flat','-bd',0)
    rC('button',fjogf + '.jog.jogminus','-command','if ![is_continuous] {jog_minus 1}','-height',1,'-width',1,'-text','-')
    rC('button',fjogf + '.jog.jogplus','-command','if ![is_continuous] {jog_plus 1}','-height',1,'-width',1,'-text','+')
    rC('combobox',fjogf + '.jog.jogincr','-editable',0,'-textvariable','jogincrement','-value',_('Continuous'),'-width',10)
    rC(fjogf + '.jog.jogincr','list','insert','end',_('Continuous'))
    if increments:
        rC(fjogf + '.jog.jogincr','list','insert','end',*increments)
    rC('labelframe',fjogf + '.zerohome','-text',_('Zero:'),'-relief','flat','-bd',0)
    rC('button',fjogf + '.zerohome.home','-command','home_joint','-height',1,'-width',6)
    rC('setup_widget_accel',fjogf + '.zerohome.home',_('Home Axis'))
    rC('button',fjogf + '.zerohome.zero','-command','touch_off_system','-height',1,'-width',3)
    rC('setup_widget_accel',fjogf + '.zerohome.zero',_('Zero') + ' X')
    rC('button',fjogf + '.zerohome.zeroxy','-height',1,'-width',3,'-text',_('X0Y0'))
    rC('button',fjogf + '.zerohome.laser','-height',1,'-width',3,'-textvariable','laserText')
    rC('button',fjogf + '.zerohome.tooltouch') # unused... kept for tk hierarchy
    # widget bindings
    rC('bind',fjogf + '.jog.jogminus','<Button-1>','if [is_continuous] {jog_minus}')
    rC('bind',fjogf + '.jog.jogminus','<ButtonRelease-1>','if [is_continuous] {jog_stop}')
    rC('bind',fjogf + '.jog.jogplus','<Button-1>','if [is_continuous] {jog_plus}')
    rC('bind',fjogf + '.jog.jogplus','<ButtonRelease-1>','if [is_continuous] {jog_stop}')
    rC('bind',fjogf + '.zerohome.zeroxy','<Button-1>','touch_off_xy 1 0 0')
    rC('bind',fjogf + '.zerohome.zeroxy','<ButtonRelease-1>','touch_off_xy 0 0 0')
    rC('bind',fjogf + '.zerohome.laser','<Button-1>','laser_button_toggled 1 1')
    rC('bind',fjogf + '.zerohome.laser','<ButtonRelease-1>','laser_button_toggled 0 1')
    # populate the frame
    rC('grid',fjogf + '.jog.jogminus','-row',0,'-column',0,'-sticky','nsew')
    rC('grid',fjogf + '.jog.jogincr','-row',0,'-column',1,'-sticky','nsew','-padx',8)
    rC('grid',fjogf + '.jog.jogplus','-row',0,'-column',2,'-sticky','nsew')
    rC('grid',fjogf + '.jog','-row',0,'-column',0,'-sticky','ew')
    rC('grid',fjogf + '.zerohome.home','-row',0,'-column',0,'-padx',(0,6))
    rC('grid',fjogf + '.zerohome.zero','-row',0,'-column',1,'-padx',(0,6))
    rC('grid',fjogf + '.zerohome.zeroxy','-row',0,'-column',2,'-padx',(0,6))
    rC('grid',fjogf + '.zerohome','-row',1,'-column',0,'-pady',(2,0),'-sticky','w')
    rC('grid',fjogf,'-column','0','-row',1,'-padx',2,'-pady',(0,0),'-sticky','w')

    # make home button a home all button if required
    if homing_order_defined:
        if ja_name.startswith('A'):
            hbName = 'axes'
        else:
            hbName ='joints'
        widgets.homebutton.configure(text = _('Home All'), command = 'home_all_joints')
    else:
        widgets.homebutton.configure(text = _('Home') + ' X' )

    # add a spacer to keep the plasma widgets at the bottom
    rC('vspace',fmanual + '.vspace','-height',1)
    rC('grid',fmanual + '.vspace','-column',0,'-row',2,'-pady',0,'-sticky','nsew')
    rC('grid','rowconfigure',fmanual,2,'-weight',99)

    # new limit switch override frame
    rC('frame',flimitovr,'-bd',0)
    rC('button',fjogf + '.override') # dummy button to placate original axis code
    rC('checkbutton',flimitovr + '.button','-command','toggle_override_limits','-variable','override_limits','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label',flimitovr + '.label','-text',_('Override Limits'),'-anchor','center')
    # populate the frame
    rC('grid',flimitovr + '.button','-column',0,'-row',1,'-sticky','nsw')
    rC('grid',flimitovr + '.label','-column',1,'-row',1,'-sticky','w','-padx',(4,0))
    rC('grid','rowconfigure',flimitovr,0,'-weight',1)
    rC('grid','rowconfigure',flimitovr,1,'-weight',0)
    rC('grid','rowconfigure',flimitovr,2,'-weight',1)

    # new jog inhibit override frame
    rC('frame',fjogiovr,'-bd',0)
    rC('checkbutton',fjogiovr + '.button','-variable','jogInhibitOvr','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label',fjogiovr + '.label','-text',_('Jog Inhibit Override'),'-anchor','center')
    # populate the frame
    rC('grid',fjogiovr + '.button','-column',0,'-row',1,'-sticky','nsw')
    rC('grid',fjogiovr + '.label','-column',1,'-row',1,'-sticky','w','-padx',(4,0))
    rC('grid','rowconfigure',fjogiovr,0,'-weight',1)
    rC('grid','rowconfigure',fjogiovr,1,'-weight',0)
    rC('grid','rowconfigure',fjogiovr,2,'-weight',1)

    # new height override frame
    # create the widgets
    rC('labelframe',foverride,'-text',_('THC Height Override:'),'-relief','flat','-bd',0)
    rC('Button',foverride + '.lower','-text','-','-width',1,'-takefocus',0)
    rC('Button',foverride + '.raise','-text','+','-width',1,'-takefocus',0)
    rC('label',foverride + '.height-override','-width',6,'-justify','center','-text','%0.1fV' % (torchHeight))
    rC('Button',foverride + '.reset','-text',_('Reset'),'-width',1,'-takefocus','0','-width',3)
    # populate the frame
    rC('pack',foverride + '.lower','-side','left')
    rC('pack',foverride + '.raise','-side','left','-padx',(8,0))
    rC('pack',foverride + '.height-override','-side','left')
    rC('pack',foverride + '.reset','-side','right')
    rC('grid',foverride,'-column',0,'-row',3,'-padx',2,'-pady',(0,4),'-sticky','w')
    # widget bindings
    rC('bind',foverride + '.lower','<ButtonPress-1>','height_lower')
    rC('bind',foverride + '.raise','<ButtonPress-1>','height_raise')
    rC('bind',foverride + '.reset','<ButtonPress-1>','height_reset')

    # new plasma frame
    # create the widgets
    rC('frame',fplasma,'-bd',0)
    rC('label',fplasma + '.arcvl','-anchor','nw','-text','Arc Voltage:')
    rC('label',fplasma + '.arc-voltage','-anchor','se','-width',4,'-fg',ourBlue)
    rC('checkbutton',fplasma + '.thc','-variable','thcEnable','-command','thc_enable_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label',fplasma + '.thcL','-anchor','nw','-text','THC Enable')
    rC('checkbutton',fplasma + '.vel','-variable','cornerEnable','-command','corner_enable_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label',fplasma + '.velL','-anchor','nw','-text','Velocity Lock')
    rC('checkbutton',fplasma + '.void','-variable','kerfEnable','-command','kerf_enable_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label',fplasma + '.voidL','-anchor','nw','-text','Void Lock')
    # populate the frame
    rC('grid',fplasma + '.thc','-column',2,'-row',0,'-sticky','w')
    rC('grid',fplasma + '.thcL','-column',3,'-row',0,'-sticky','w')
    rC('grid',fplasma + '.vel','-column',2,'-row',1,'-sticky','w')
    rC('grid',fplasma + '.velL','-column',3,'-row',1,'-sticky','w')
    rC('grid',fplasma + '.void','-column',2,'-row',2,'-sticky','w')
    rC('grid',fplasma + '.voidL','-column',3,'-row',2,'-sticky','w')
    rC('grid',fplasma,'-column',0,'-row',4,'-padx',2,'-pady',(0,0),'-sticky','sew')
    rC('grid','columnconfigure',fplasma,1,'-weight',1)

    # hide bottom pane until modified
    rC('pack','forget','.pane.bottom.t.text')
    rC('pack','forget','.pane.bottom.t.sb')

    # new led frame
    # create the widgets
    rC('frame',fleds,'-relief','flat','-bd',1)
    rC('canvas',fleds + '.led-arc-ok','-width',20,'-height',20)
    rC('label',fleds + '.lAOlab','-text',_('Arc OK'),'-anchor','w','-width',9)
    rC('canvas',fleds + '.led-torch','-width',20,'-height',20)
    rC('label',fleds + '.lTlab','-text',_('Torch On'),'-anchor','w','-width',9)
    rC('canvas',fleds + '.led-breakaway','-width',20,'-height',20)
    rC('label',fleds + '.lBlab','-text',_('Breakaway'),'-anchor','w','-width',9)
    rC('canvas',fleds + '.led-thc-enabled','-width',20,'-height',20)
    rC('label',fleds + '.lTElab','-text',_('THC Enabled'),'-anchor','w','-width',10)
    rC('canvas',fleds + '.led-thc-active','-width',20,'-height',20)
    rC('label',fleds + '.lTAlab','-text',_('THC Active'),'-anchor','w','-width',10)
    rC('canvas',fleds + '.led-ohmic','-width',20,'-height',20)
    rC('label',fleds + '.lOlab','-text',_('Ohmic Probe'),'-anchor','w','-width',10)
    rC('canvas',fleds + '.led-float','-width',20,'-height',20)
    rC('label',fleds + '.lFlab','-text',_('Float Switch'),'-anchor','w','-width',10)
    rC('canvas',fleds + '.led-up','-width',20,'-height',20)
    rC('label',fleds + '.labup','-text',_('Up'),'-anchor','w','-width',8)
    rC('canvas',fleds + '.led-down','-width',20,'-height',20)
    rC('label',fleds + '.labdn','-text',_('Dn'),'-anchor','w','-width',8)
    rC('canvas',fleds + '.led-corner-locked','-width',20,'-height',20)
    rC('label',fleds + '.lCLlab','-text',_('Vel Lock'),'-anchor','w','-width',8)
    rC('canvas',fleds + '.led-kerf-locked','-width',20,'-height',20)
    rC('label',fleds + '.lKLlab','-text',_('Void Lock'),'-anchor','w','-width',8)
    # create the led shapes
    led1 = rC(fleds + '.led-arc-ok','create','oval',1,1,18,18,'-fill',ourGreen,'-disabledfill',ourGray)
    rC(fleds + '.led-torch','create','oval',1,1,18,18,'-fill',ourOrange,'-disabledfill',ourGray)
    rC(fleds + '.led-breakaway','create','oval',1,1,18,18,'-fill',ourRed,'-disabledfill',ourGray)
    rC(fleds + '.led-thc-enabled','create','oval',1,1,18,18,'-fill',ourGreen,'-disabledfill',ourGray)
    rC(fleds + '.led-thc-active','create','oval',1,1,18,18,'-fill',ourGreen,'-disabledfill',ourGray)
    rC(fleds + '.led-ohmic','create','oval',1,1,18,18,'-fill',ourYellow,'-disabledfill',ourGray)
    rC(fleds + '.led-float','create','oval',1,1,18,18,'-fill',ourYellow,'-disabledfill',ourGray)
    rC(fleds + '.led-up','create','oval',1,1,18,18,'-fill',ourYellow,'-disabledfill',ourGray)
    rC(fleds + '.led-down','create','oval',1,1,18,18,'-fill',ourYellow,'-disabledfill',ourGray)
    rC(fleds + '.led-corner-locked','create','oval',1,1,18,18,'-fill',ourRed,'-disabledfill',ourGray)
    rC(fleds + '.led-kerf-locked','create','oval',1,1,18,18,'-fill',ourRed,'-disabledfill',ourGray)
    # populate the frame
    rC('grid',fleds + '.led-arc-ok',         '-column',0,'-row',0,'-padx',(4,0),'-pady',(4,0),'-sticky','EW')
    rC('grid',fleds + '.lAOlab',             '-column',1,'-row',0,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-torch',          '-column',0,'-row',1,'-padx',(4,0),'-pady',(4,0))
    rC('grid',fleds + '.lTlab',              '-column',1,'-row',1,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-breakaway',      '-column',0,'-row',3,'-padx',(4,0),'-pady',(4,0))
    rC('grid',fleds + '.lBlab',              '-column',1,'-row',3,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-thc-enabled',    '-column',2,'-row',0,'-padx',(0,0),'-pady',(4,0))
    rC('grid',fleds + '.lTElab',             '-column',3,'-row',0,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-thc-active',     '-column',2,'-row',1,'-padx',(0,0),'-pady',(4,0))
    rC('grid',fleds + '.lTAlab',             '-column',3,'-row',1,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-ohmic',          '-column',2,'-row',2,'-padx',(0,0),'-pady',(4,0))
    rC('grid',fleds + '.lOlab',              '-column',3,'-row',2,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-float',          '-column',2,'-row',3,'-padx',(0,0),'-pady',(4,0))
    rC('grid',fleds + '.lFlab',              '-column',3,'-row',3,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-up',             '-column',4,'-row',0,'-padx',(4,0),'-pady',(4,0))
    rC('grid',fleds + '.labup',              '-column',5,'-row',0,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-down',           '-column',4,'-row',1,'-padx',(4,0),'-pady',(4,0))
    rC('grid',fleds + '.labdn',              '-column',5,'-row',1,'-padx',(0,0),'-pady',(4,0),'-sticky','W')
    rC('grid',fleds + '.led-corner-locked',  '-column',4,'-row',2,'-padx',(4,0),'-pady',(4,0))
    rC('grid',fleds + '.lCLlab',             '-column',5,'-row',2,'-padx',(0,0),'-pady',(4,0),'-sticky','W')

    # menu alterations
    # delete existing
    rC('.menu.file','delete','last')
    rC('.menu','delete','last')
    # add new menu items
    rC('.menu.file','add','command','-command','close_window')
    rC('setup_menu_accel','.menu.file','end',_('_Quit'))
    rC('.menu.view','insert',0,'checkbutton','-variable','previewLarge','-command','preview_toggle')
    rC('setup_menu_accel','.menu.view',0,_('Large Pre_view'))
    rC('.menu.view','insert',1,'separator')
    rC('.menu','add','command','-command','conv_toggle 1')
    rC('setup_menu_accel','.menu','end',_('_Conversational'))
    rC('.menu','add','command','-command','param_toggle 1')
    rC('setup_menu_accel','.menu','end',_('_Parameters'))
    rC('.menu','add','command','-command','setup_toggle 1')
    rC('setup_menu_accel','.menu','end',_('_Setup'))
    rC('.menu','add','cascade','-menu','.menu.help')
    rC('setup_menu_accel','.menu','end',_('_Help'))

    # rework the status bar
    rC('grid','forget',ftop + '.gcodel')
    rC('grid','forget',ftop + '.gcodes')
    rC('pack','forget','.info.tool')
    rC('.info.task_state','configure','-width',6)
    rC('.info.tool','configure','-width',10,'-textvariable','::plasmatool')
    rC('.info.position','configure','-width',25)
    rC('grid','.info','-columnspan',4)
    rC('labelframe','.info.gcodef','-relief','sunken','-bd',2)
    rC('label','.info.gcodef.gcodel','-bd',0)
    rC('setup_widget_accel','.info.gcodef.gcodel','Active Codes:')
    rC('text','.info.gcodef.gcodes','-height',1,'-width',10,'-relief','flat','-bd',0,'-pady',0,)
    rC('.info.gcodef.gcodes','configure','-bg',buttonBackG,'-undo',0,'-wrap','word',)
    rC('pack','.info.tool','-side','left')
    rC('pack','.info.gcodef.gcodel','-side','left')
    rC('pack','.info.gcodef.gcodes','-side','left','-fill','x','-expand',1)
    rC('pack','.info.gcodef','-side','left','-fill','x','-expand',1)

    # move existing pane to column 1
    rC('grid','.pane','-column',1,'-row',1,'-rowspan',2,'-sticky','nsew')
    rC('grid','columnconfigure','.',0,'-weight',0)
    rC('grid','columnconfigure','.',1,'-weight',1)
    rC('grid','columnconfigure','.',2,'-weight',0)

    # new button panel
    # create widgets
    rC('frame','.fbuttons','-relief','flat')
    rC('button','.fbuttons.torch-enable','-width',6,'-bg',ourRed,'-activebackground',ourRed,'-text',torchEnable['disabled'].replace('\\','\n'))
    if '\\' in torchEnable['enabled'] or '\\' in torchEnable['disabled']:
        rC('.fbuttons.torch-enable','configure','-height',2)
    else:
        rC('.fbuttons.torch-enable','configure','-height',1)
    # populate frame
    rC('grid','.fbuttons.torch-enable','-column',0,'-row',0,'-sticky','new')
    rC('grid','.fbuttons','-column',0,'-row',1,'-rowspan',2,'-sticky','nsew','-padx',0,'-pady',0)
    # widget bindings
    rC('bind','.fbuttons.torch-enable','<ButtonPress-1>','torch_enable')

    # new cut recovery tab
    # create the widgets
    rC(ftabs,'insert','end','cutrecs','-text','Cut Recovery')
    rC(fcutrecs,'configure','-borderwidth',2)
    rC(ftabs,'delete','cutrecs',0)
    rC('labelframe',fcutrec,'-text','Speed:','-relief','flat')
    rC('Button',fcutrec + '.reverse','-text','Rev','-takefocus',0,'-width',3)
    rC('bind',fcutrec + '.reverse','<Button-1>','cut_rec_motion -1')
    rC('bind',fcutrec + '.reverse','<ButtonRelease-1>','cut_rec_motion 0')
    rC('frame',fcutrec + '.display','-relief','flat')
    rC('frame',fcutrec + '.display.top','-relief','flat')
    rC('label',fcutrec + '.display.top.value','-textvariable','crSpeed','-width',6,'-anchor','center')
    rC('scale',fcutrec + '.display.cut-rec-speed','-takefocus',0,'-orient','horizontal','-showvalue',0,'-command','cut_rec_slider_changed')
    rC(fcutrec + '.display.cut-rec-speed','configure','-from',1,'-to',100,'-resolution',1)
    rC('Button',fcutrec + '.forward','-text','Fwd','-takefocus',0,'-width',3)
    rC('frame',fcutrecs + '.buttons')
    rC('button',fcutrecs + '.buttons.laser','-text',_('Laser'),'-takefocus',0)
    rC('button',fcutrecs + '.buttons.cancel','-text',_('Cancel'),'-command','cut_rec_cancel','-takefocus',0)
    rC('labelframe',fleadins,'-text','Leadins:','-relief','flat')
    rC('Button',fleadins + '.nw','-takefocus',0,'-image',rC('load_image',imagePath + '/nw'))
    rC('Button',fleadins + '.n','-takefocus',0,'-image',rC('load_image',imagePath + '/n'))
    rC('Button',fleadins + '.ne','-takefocus',0,'-image',rC('load_image',imagePath + '/ne'))
    rC('Button',fleadins + '.w','-takefocus',0,'-image',rC('load_image',imagePath + '/w'))
    rC('Label',fleadins + '.offset','-textvariable','kerfWidth','-takefocus',0)
    rC('Button',fleadins + '.e','-takefocus',0,'-image',rC('load_image',imagePath + '/e'))
    rC('Button',fleadins + '.sw','-takefocus',0,'-image',rC('load_image',imagePath + '/sw'))
    rC('Button',fleadins + '.s','-takefocus',0,'-image',rC('load_image',imagePath + '/s'))
    rC('Button',fleadins + '.se','-takefocus',0,'-image',rC('load_image',imagePath + '/se'))
    # populate the frame
    rC('pack',fcutrec + '.reverse','-side','left','-fill','y')
    rC('pack',fcutrec + '.display.top.value','-side','left','-fill','y')
    rC('pack',fcutrec + '.display.top','-fill','y')
    rC('pack',fcutrec + '.display.cut-rec-speed','-fill','y')
    rC('pack',fcutrec + '.display','-side','left','-fill','x','-expand',1)
    rC('pack',fcutrec + '.forward','-side','right','-fill','y')
    rC('pack',fcutrecs + '.buttons.cancel','-side','right')
    rC('grid',fcutrecs + '.buttons','-column',0,'-row',1,'-sticky','n','-pady',12)
    rC('grid',fleadins + '.nw','-column',0,'-row',0)
    rC('grid',fleadins + '.n','-column',1,'-row',0)
    rC('grid',fleadins + '.ne','-column',2,'-row',0)
    rC('grid',fleadins + '.w','-column',0,'-row',1)
    rC('grid',fleadins + '.offset','-column',1,'-row',1)
    rC('grid',fleadins + '.e','-column',2,'-row',1)
    rC('grid',fleadins + '.sw','-column',0,'-row',2)
    rC('grid',fleadins + '.s','-column',1,'-row',2)
    rC('grid',fleadins + '.se','-column',2,'-row',2)
    rC('grid',fcutrec,'-column',0,'-row',0,'-sticky','wne')
    rC('grid',fleadins,'-column',0,'-row',2,'-sticky','nsew')
    # set direction buttons stretch
    rC('grid','columnconfigure',fleadins,0,'-weight',1)
    rC('grid','columnconfigure',fleadins,1,'-weight',1,)
    rC('grid','columnconfigure',fleadins,2,'-weight',1)
    rC('grid','rowconfigure',fleadins,0,'-weight',1)
    rC('grid','rowconfigure',fleadins,1,'-weight',1,'-pad',20)
    rC('grid','rowconfigure',fleadins,2,'-weight',1)
    # widget bindings
    rC('bind',fcutrec + '.forward','<Button-1>','cut_rec_motion 1')
    rC('bind',fcutrec + '.forward','<ButtonRelease-1>','cut_rec_motion 0')
    rC('bind',fleadins + '.nw','<Button-1>','cut_rec_move -1 1')
    rC('bind',fleadins + '.n','<Button-1>','cut_rec_move 0 1')
    rC('bind',fleadins + '.ne','<Button-1>','cut_rec_move 1 1')
    rC('bind',fleadins + '.w','<Button-1>','cut_rec_move -1 0')
    rC('bind',fleadins + '.e','<Button-1>','cut_rec_move 1 0')
    rC('bind',fleadins + '.sw','<Button-1>','cut_rec_move -1 -1')
    rC('bind',fleadins + '.s','<Button-1>','cut_rec_move 0 -1')
    rC('bind',fleadins + '.se','<Button-1>','cut_rec_move 1 -1')
    rC('bind',fcutrecs + '.buttons.laser','<Button-1>','laser_button_toggled 1 0')
    rC('bind',fcutrecs + '.buttons.laser','<ButtonRelease-1>','laser_button_toggled 0 0')

    # new parameters frame
    rC('frame',fparam)
    # create the widgets
    rC('frame',fparam + '.c1')
    rC('frame',fparam + '.c2')
    rC('frame',fparam + '.c3')
    rC('frame',fparam + '.c4')
    rC('labelframe',fparam + '.c1.probe','-text','Probing','-relief','groove')
    rC('labelframe',fparam + '.c1.motion','-text','Motion','-relief','groove')
    rC('labelframe',fparam + '.c2.thc','-text','THC','-relief','groove')
    rC('labelframe',fparam + '.c2.safety','-text','Safety','-relief','groove')
    rC('labelframe',fparam + '.c3.arc','-text','Arc','-relief','groove')
    rC('labelframe',fparam + '.c4.scribe','-text','Scribe','-relief','groove')
    rC('labelframe',fparam + '.c4.spotting','-text','Spotting','-relief','groove')
    #  (parent, name, label text, prefs option)
    cp1=['.c1.probe','float-switch-travel','Float Travel','Float Switch Travel']
    # decimals, value, min, max, increment,
    cp1[2:1] = [2,1.5,-25,25,0.01] if s.linear_units == 1 else [3,0.06,-1,1,0.001]
    cp2=['.c1.probe','probe-feed-rate','Probe Speed','Probe Feed Rate']
    cp2[2:1] = [0,300,1,thcFeedRate,1] if s.linear_units == 1 else [1,12,0.1,thcFeedRate,.1]
    cp3=['.c1.probe','probe-start-height','Probe Height','Probe Start Height']
    cp3[2:1] = [0,38,1,maxHeight,1] if s.linear_units == 1 else [2,1.5,.1,maxHeight,0.01]
    cp4=['.c1.probe','ohmic-probe-offset','Ohmic Z Offset','Ohmic Probe Offset']
    cp4[2:1] = [2,0,-25,+25,0.01] if s.linear_units == 1 else [3,0,-1,1,0.001]
    cp5=['.c1.probe','skip-ihs-distance','Skip IHS','Skip IHS Distance']
    cp5[2:1] = [0,0,0,999,1] if s.linear_units == 1 else [1,0,0,99,.1]
    cp6=['.c1.motion','setup-feed-rate','Setup Speed','Setup Feed Rate']
    cp6[2:1] = [0,int(thcFeedRate * 0.8),1,thcFeedRate,1] if s.linear_units == 1 else [1,int(thcFeedRate * 0.8),0.1,thcFeedRate,0.1]
    cp7=['.c2.safety','safe-height','Safe Height','Safe Height']
    cp7[2:1] = [0,20,0,maxHeight,1] if s.linear_units == 1 else [2,0.75,0,maxHeight,0.01]
    cp8=['.c3.arc','height-per-volt','Height Per Volt','Height Per Volt']
    cp8[2:1] = [3,0.1,0.025,0.5,0.01] if s.linear_units == 1 else [4,0.004,0.001,0.020,0.001]
    cpList = [cp1, cp2, cp3, cp4, \
              ['.c1.probe','ohmic-max-attempts',0,0,0,10,1,'Ohmic Retries','Ohmic Maximum Attempts'], \
              cp5, cp6, \
              ['.c2.thc','thc-delay',1,0.5,0,9,0.1,'Delay','THC Delay'], \
              ['.c2.thc','thc-threshold',2,1,0.05,9,0.01,'Threshold (V)','THC Threshold'], \
              ['.c2.thc','pid-p-gain',0,10,0,1000,1,'PID P Gain (Speed)','Pid P Gain'], \
              ['.c2.thc','pid-i-gain',0,0,0,1000,1,'PID I Gain','Pid I Gain'], \
              ['.c2.thc','pid-d-gain',0,0,0,1000,1,'PID D Gin','Pid D Gain'], \
              ['.c2.thc','cornerlock-threshold',0,90,1,99,1,'VAD Threshold (%)','Velocity Anti Dive Threshold'], \
              ['.c2.thc','kerfcross-override',0,100,10,500,1,'Void Override (%)','Void Sense Override'], \
              cp7, \
              ['.c3.arc','arc-fail-delay',1,3,0.1,60,0.1,'Fail Timeout','Arc Fail Timeout'], \
              ['.c3.arc','arc-max-starts',0,3,1,9,1,'Max. Attempts','Arc Maximum Starts'], \
              ['.c3.arc','restart-delay',0,3,1,60,1,'Retry Delay','Arc Restart Delay'], \
              ['.c3.arc','arc-voltage-scale',6,1,-9999,9999,0.000001,'Voltage Scale','Arc Voltage Scale'], \
              ['.c3.arc','arc-voltage-offset',3,0,-999999,999999,0.001,'Voltage Offset','Arc Voltage Offset'], \
              ['.c3.arc','arc-ok-high',0,99999,0,99999,1,'OK High Volts','Ark OK High'], \
              ['.c3.arc','arc-ok-low',0,60,0,100,1,'OK Low Volts','Arc OK Low'], \
              cp8, \
              ['.c4.scribe','scribe-arm-delay',1,0,0,9,0.1,'Arm Delay','Scribe Arming Delay'], \
              ['.c4.scribe','scribe-on-delay',1,0,0,9,0.1,'On delay','Scribe On Delay'], \
              ['.c4.spotting','spotting-threshold',0,0,0,199,1,'Threshold (V)','Spotting Threshold'], \
              ['.c4.spotting','spotting-time',0,0,0,9999,1,'On Time (mS)','Spotting Time'], \
             ]
    cpRow = 0
    cpFrame = cp1[0]
    for cpItem in cpList:
        if cpItem[0] != cpFrame:
            cpFrame = cpItem[0]
            cpRow = 0
        cpName = fparam + cpItem[0] + '.' + cpItem[1]
        cpType = 'flt' if cpItem[2] > 0 else 'int'
        rC('label',cpName + 'L','-text',cpItem[7],'-width',15,'-anchor','e')
        rC('spinbox',cpName,'-width', 10,'-justify','right','-wrap','true','-bg',ourWhite)
        spinBoxes.append(cpName)
        rC(cpName,'configure','-from',cpItem[4],'-to',cpItem[5])
        rC(cpName,'configure','-increment',cpItem[6],'-format','%0.{}f'.format(cpItem[2]))
        rC(cpName,'configure','-validate','key','-vcmd','{} %W {} {} %P %s'.format(valspin,cpType,cpItem[2]))
        if cpItem[7] == 'Setup Speed':
            rC('label',fparam + cpItem[0] + '.maxzL','-text','Max Z Speed','-width',15,'-anchor','e')
            rC('label',fparam + cpItem[0] + '.maxz','-text',int(thcFeedRate),'-width',10,'-anchor','e')
            rC('grid', fparam + cpItem[0] + '.maxzL','-column',0,'-row',cpRow,'-sticky','e','-padx',(4,0),'-pady',(4,0))
            rC('grid', fparam + cpItem[0] + '.maxz','-column',1,'-row',cpRow,'-sticky','e','-padx',(0,8),'-pady',(4,0))
            cpRow += 1
        rC('grid', cpName + 'L','-column',0,'-row',cpRow,'-sticky','e','-padx',(4,0),'-pady',(4,0))
        rC('grid', cpName,'-column',1,'-row',cpRow,'-sticky','e','-padx',(0,4),'-pady',(4,0))
        cpRow += 1
    # populate parameters frame
    rC('grid',fparam + '.c1.probe','-column',0,'-row',0,'-sticky','new','-padx',(4,2),'-pady',(4,0),'-ipady',4)
    rC('grid',fparam + '.c1.motion','-column',0,'-row',1,'-sticky','new','-padx',(4,2),'-pady',(4,0),'-ipady',4)
    rC('grid',fparam + '.c2.thc','-column',0,'-row',0,'-sticky','new','-padx',(2,2),'-pady',(4,0),'-ipady',4)
    rC('grid',fparam + '.c2.safety','-column',0,'-row',1,'-sticky','new','-padx',(2,2),'-pady',(4,0),'-ipady',4)
    rC('grid',fparam + '.c3.arc','-column',0,'-row',0,'-sticky','new','-padx',(2,2),'-pady',(4,0),'-ipady',4)
    rC('grid',fparam + '.c4.scribe','-column',0,'-row',0,'-sticky','new','-padx',(2,2),'-pady',(4,0),'-ipady',4)
    rC('grid',fparam + '.c4.spotting','-column',0,'-row',1,'-sticky','new','-padx',(2,2),'-pady',(4,0),'-ipady',4)
    rC('grid',fparam + '.c1','-column',0,'-row',0,'-sticky','n')
    rC('grid',fparam + '.c2','-column',1,'-row',0,'-sticky','n')
    rC('grid',fparam + '.c3','-column',2,'-row',0,'-sticky','n')
    rC('grid',fparam + '.c4','-column',3,'-row',0,'-sticky','n')

    # new settings frame
    rC('frame',fsetup)
    # left panel
    rC('frame',fsetup + '.l')
    # gui frame
    rC('labelframe',fsetup + '.l.gui','-text','GUI','-relief','groove')
    rC('label',fsetup + '.l.gui.closedialogL','-text','Close Dialog','-anchor','e')
    rC('checkbutton',fsetup + '.l.gui.closedialog','-variable','closeDialog','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label',fsetup + '.l.gui.wsizeL','-text','Window Size','-width', 13,'-anchor','e')
    rC('ComboBox',fsetup + '.l.gui.wsize','-modifycmd','set_window_size','-textvariable','winSize','-bd',1,'-width',10,'-justify','right','-editable',0)
    rC(fsetup + '.l.gui.wsize','configure','-values',['default','last','fullscreen','maximized'])
    rC('label',fsetup + '.l.gui.fsizeL','-text','Font Size','-anchor','e')
    rC('ComboBox',fsetup + '.l.gui.fsize','-modifycmd','font_size_changed','-textvariable','fontSize','-bd',1,'-width',10,'-justify','right','-editable',0)
    rC(fsetup + '.l.gui.fsize','configure','-values',[9,10,11,12,13,14,15,16])
    rC('label',fsetup + '.l.gui.coneL','-text','Cone Size','-anchor','e')
    rC('ComboBox',fsetup + '.l.gui.cone','-modifycmd','cone_size_changed','-textvariable','coneSize','-bd',1,'-width',10,'-justify','right','-editable',0)
    rC(fsetup + '.l.gui.cone','configure','-values',[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0])
    rC('label',fsetup + '.l.gui.zoomL','-text','Table Zoom','-anchor','e')
    rC('spinbox',fsetup + '.l.gui.zoom','-width', 10,'-justify','right','-wrap','true','-bg',ourWhite,'-from',0.1,'-to',10.0,'-increment',0.1,'-format','%0.1f')
    rC(fsetup + '.l.gui.zoom','configure','-validate','key','-vcmd','{} %W {} {} %P %s'.format(valspin,'flt',1))
    spinBoxes.append(fsetup + '.l.gui.zoom')
    # populate gui frame
    rC('grid',fsetup + '.l.gui.closedialogL','-column',0,'-row',0,'-sticky','e','-padx',(4,0),'-pady',(4,0))
    rC('grid',fsetup + '.l.gui.closedialog','-column',1,'-row',0,'-sticky','e','-padx',(0,4),'-pady',(4,0))
    rC('grid',fsetup + '.l.gui.wsizeL','-column',0,'-row',1,'-sticky','e','-padx',(4,0),'-pady',(4,0))
    rC('grid',fsetup + '.l.gui.wsize','-column',1,'-row',1,'-sticky','w','-padx',(0,4),'-pady',(4,0))
    rC('grid',fsetup + '.l.gui.fsizeL','-column',0,'-row',2,'-sticky','e','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.l.gui.fsize','-column',1,'-row',2,'-sticky','w','-padx',(0,4),'-pady',(4,4))
    rC('grid',fsetup + '.l.gui.coneL','-column',0,'-row',3,'-sticky','e','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.l.gui.cone','-column',1,'-row',3,'-sticky','w','-padx',(0,4),'-pady',(4,4))
    rC('grid',fsetup + '.l.gui.zoomL','-column',0,'-row',4,'-sticky','e','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.l.gui.zoom','-column',1,'-row',4,'-sticky','w','-padx',(0,4),'-pady',(4,4))
    rC('grid','columnconfigure',fsetup + '.l.gui',0,'-weight',1)
    rC('grid','columnconfigure',fsetup + '.l.gui',1,'-weight',1)

    # jog frame
    rC('labelframe',fsetup + '.l.jog','-text','Default Jog Speed','-relief','groove')
    rC('label',fsetup + '.l.jog.speedL','-width', 13,'-text','Units Per Minute','-anchor','e')
    rC('spinbox',fsetup + '.l.jog.speed','-width', 10,'-justify','right','-wrap','true','-bg',ourWhite)
    minJogSpeed = int(float(rC(ftop + '.jogspeed.s','cget','-from')) * vars.max_speed.get() * 60)
    rC(fsetup + '.l.jog.speed','configure','-from',minJogSpeed,'-to','{}'.format(vars.max_speed.get() * 60),'-increment',1)
    rC(fsetup + '.l.jog.speed','configure','-format','%0.0f')
    rC(fsetup + '.l.jog.speed','configure','-validate','key','-vcmd','{} %W {} {} %P %s'.format(valspin,'int',0))
    spinBoxes.append(fsetup + '.l.jog.speed')
    # populate plasmac frame
    rC('grid',fsetup + '.l.jog.speedL','-column',0,'-row',0,'-sticky','e','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.l.jog.speed','-column',1,'-row',0,'-sticky','w','-padx',(0,4),'-pady',(4,4))
    rC('grid','columnconfigure',fsetup + '.l.jog',0,'-weight',1)
    rC('grid','columnconfigure',fsetup + '.l.jog',1,'-weight',1)

    # plasmac frame
    rC('labelframe',fsetup + '.l.plasmac','-text','Plasmac','-relief','groove')
    rC('label',fsetup + '.l.plasmac.modeL','-width', 13,'-text','Mode','-anchor','e')
    rC('ComboBox',fsetup + '.l.plasmac.mode','-modifycmd','mode_changed','-textvariable','plasmacMode','-bd',1,'-width',10,'-justify','right','-editable',0)
    rC(fsetup + '.l.plasmac.mode','configure','-values',[0,1,2])
    # populate plasmac frame
    rC('grid',fsetup + '.l.plasmac.modeL','-column',0,'-row',0,'-sticky','e','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.l.plasmac.mode','-column',1,'-row',0,'-sticky','w','-padx',(0,4),'-pady',(4,4))
    rC('grid','columnconfigure',fsetup + '.l.plasmac',0,'-weight',1)
    rC('grid','columnconfigure',fsetup + '.l.plasmac',1,'-weight',1)

    # material frame
    rC('labelframe',fsetup + '.l.mats','-text','Material','-relief','groove')
    rC('label',fsetup + '.l.mats.defaultL','-width', 13,'-text','Default','-anchor','e')
    rC('ComboBox',fsetup + '.l.mats.default','-modifycmd','change_default_material','-textvariable','matDefault','-bd',1,'-width',10,'-justify','right','-editable',0)
    # populate material frame
    rC('grid',fsetup + '.l.mats.defaultL','-column',0,'-row',0,'-sticky','e','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.l.mats.default','-column',1,'-row',0,'-sticky','w','-padx',(0,4),'-pady',(4,4))
    rC('grid','columnconfigure',fsetup + '.l.mats',0,'-weight',1)
    rC('grid','columnconfigure',fsetup + '.l.mats',1,'-weight',1)

    # cut recovery frame
    rC('labelframe',fsetup + '.l.cr','-text','Cut Recovery','-relief','groove')
    rC('label',fsetup + '.l.cr.speedL','-width', 13,'-text','Speed %','-anchor','e')
    rC('spinbox',fsetup + '.l.cr.speed','-width', 10,'-justify','right','-wrap','true','-bg',ourWhite)
    minJogSpeed = int(float(rC(ftop + '.jogspeed.s','cget','-from')) * vars.max_speed.get() * 60)
    rC(fsetup + '.l.cr.speed','configure','-from',1,'-to',100,'-increment',1)
    rC(fsetup + '.l.cr.speed','configure','-format','%0.0f')
    rC(fsetup + '.l.cr.speed','configure','-validate','key','-vcmd','{} %W {} {} %P %s'.format(valspin,'int',0))
    spinBoxes.append(fsetup + '.l.cr.speed')
    # populate cut recovery frame
    rC('grid',fsetup + '.l.cr.speedL','-column',0,'-row',0,'-sticky','e','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.l.cr.speed','-column',1,'-row',0,'-sticky','w','-padx',(0,4),'-pady',(4,4))
    rC('grid','columnconfigure',fsetup + '.l.cr',0,'-weight',1)
    rC('grid','columnconfigure',fsetup + '.l.cr',1,'-weight',1)
    #populate left panel
    rC('grid',fsetup + '.l.gui','-column',0,'-row',0,'-sticky','new')
    rC('grid',fsetup + '.l.jog','-column',0,'-row',1,'-sticky','new')
    rC('grid',fsetup + '.l.plasmac','-column',0,'-row',2,'-sticky','new')
    rC('grid',fsetup + '.l.mats','-column',0,'-row',3,'-sticky','new')
    rC('grid',fsetup + '.l.cr','-column',0,'-row',4,'-sticky','new')

    # middle panel for utilities
    rC('labelframe',fsetup + '.utilities','-text','Utilities','-relief','groove')
    rC('button',fsetup + '.utilities.offsets','-command','set_peripheral_offsets','-text','Set Offsets')
    #populate left panel
    rC('grid',fsetup + '.utilities.offsets','-column',0,'-row',0,'-sticky','new')

    # right panel (for buttons)
    rC('frame',fsetup + '.r')
    # top for torch enable
    rC('labelframe',fsetup + '.r.torch','-text','Torch Enable','-relief','groove')
    rC('label',fsetup + '.r.torch.enabledL','-text','Enabled','-width',14,'-anchor','w')
    rC('label',fsetup + '.r.torch.disabledL','-text','Disabled','-width',14,'-anchor','w')
    rC('entry',fsetup + '.r.torch.enabled','-width',14)
    rC('entry',fsetup + '.r.torch.disabled','-width',14)
    rC('grid',fsetup + '.r.torch.enabledL','-column',0,'-row',0,'-sticky','nw','-padx',(4,0),'-pady',(4,0))
    rC('grid',fsetup + '.r.torch.disabledL','-column',1,'-row',0,'-sticky','nw','-padx',(4,0),'-pady',(4,0))
    rC('grid',fsetup + '.r.torch.enabled','-column',0,'-row',1,'-sticky','nw','-padx',(4,0))
    rC('grid',fsetup + '.r.torch.disabled','-column',1,'-row',1,'-sticky','nw','-padx',(4,0))
    # ubuttons for user buttons
    rC('labelframe',fsetup + '.r.ubuttons','-text','User Buttons','-relief','groove')
    rC('label',fsetup + '.r.ubuttons.numL','-text',' #','-width',2,'-anchor','e')
    rC('label',fsetup + '.r.ubuttons.nameL','-text','Name','-width',14,'-anchor','w')
    rC('label',fsetup + '.r.ubuttons.codeL','-text','Code','-width',48,'-anchor','w')
    for n in range(1, 21):
        rC('label',fsetup + '.r.ubuttons.num' + str(n),'-text',str(n),'-anchor','e')
        rC('entry',fsetup + '.r.ubuttons.name' + str(n),'-width',14)
        rC('entry',fsetup + '.r.ubuttons.code' + str(n))
    rC('grid',fsetup + '.r.ubuttons.numL','-column',0,'-row',0,'-sticky','ne','-padx',(4,0),'-pady',(4,0))
    rC('grid',fsetup + '.r.ubuttons.nameL','-column',1,'-row',0,'-sticky','nw','-padx',(4,0),'-pady',(4,0))
    rC('grid',fsetup + '.r.ubuttons.codeL','-column',2,'-row',0,'-sticky','nw','-padx',(4,4),'-pady',(4,0))
    # populate right panel
    rC('grid',fsetup + '.r.torch','-column',0,'-row',0,'-sticky','ew')
    rC('grid',fsetup + '.r.ubuttons','-column',0,'-row',1,'-sticky','ew')

    # populate settings frame
    rC('grid',fsetup + '.l','-column',0,'-row',0,'-sticky','nw','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.utilities','-column',2,'-row',0,'-sticky','nw','-padx',(4,0),'-pady',(4,4))
    rC('grid',fsetup + '.r','-column',4,'-row',0,'-sticky','ne','-padx',(0,4),'-pady',(4,4))
    rC('grid','columnconfigure',fsetup,0,'-weight',0)
    rC('grid','columnconfigure',fsetup,1,'-weight',1)
    rC('grid','columnconfigure',fsetup,2,'-weight',0)
    rC('grid','columnconfigure',fsetup,3,'-weight',1)
    rC('grid','columnconfigure',fsetup,4,'-weight',0)

    # run panel
    # create the widgets
    rC('frame','.runs','-relief','flat')
    # materials frame
    rC('ComboBox','.runs.materials','-modifycmd','material_changed','-textvariable','matCurrent','-width',10,'-editable',0)
    rC('labelframe','.runs.material','-text','Material','-relief','groove')
    #  (parent, name, label text)
    rp1=['.runs.material','kerf-width','Kerf Width']
    #  (decimals, value, min, max, increment
    rp1[2:1] = [2,0.5,0,5,0.01] if s.linear_units == 1 else [4,0.02,0,1,0.0001]
    rp2=['.runs.material','pierce-height','Pierce Height']
    rp2[2:1] = [2,4,0,25,0.01] if s.linear_units == 1 else [3,0.16,0,1,0.001]
    rp3=['.runs.material','cut-height','Cut Height']
    rp3[2:1] = [2,1,0,25,0.01] if s.linear_units == 1 else [3,0.04,0,1,0.001]
    rp4=['.runs.material','cut-feed-rate','Feed Rate']
    rp4[2:1] = [0,4000,0,19999,1] if s.linear_units == 1 else [0,160,0,999,0.1]
    rpList = [rp1, rp2, \
              ['.runs.material','pierce-delay',1,0.0,0,10,0.1,'Pierce Delay'], \
              rp3, rp4, \
              ['.runs.material','cut-amps',0,45,0,999,1,'Cut Amps'], \
              ['.runs.material','cut-volts',0,122,50,300,1,'Cut Volts'], \
              ['.runs.material','puddle-jump-height',0,0,0,200,1,'P-Jump Height'], \
              ['.runs.material','puddle-jump-delay',2,0,0,9,0.01,'P-Jump Delay'], \
              ['.runs.material','pause-at-end',1,0,0,9,0.1,'Pause At End'], \
              ['.runs.material','cut-mode',0,1,1,3,1,'Cut Mode'], \
              ['.runs.material','gas-pressure',1,0,0,150,0.1,'Gas Pressure'], \
             ]
    rpRow = 0
    for rpItem in rpList:
        rpName = rpItem[0] + '.' + rpItem[1]
        rpType = 'flt' if rpItem[2] > 0 else 'int'
        rC('spinbox',rpName,'-width', '9','-justify','right','-wrap','true','-bg',ourWhite)
        spinBoxes.append(rpName)
        rC(rpName,'configure','-from',rpItem[4],'-to',rpItem[5])
        if rpItem[1] == 'kerf-width':
            rC(rpName,'configure','-textvariable','kerfWidth')
        elif rpItem[1] == 'cut-amps':
            rC(rpName,'configure','-textvariable','cutAmps')
        elif rpItem[1] == 'cut-mode':
            rC(rpName,'configure','-textvariable','cutMode')
        elif rpItem[1] == 'gas-pressure':
            rC(rpName,'configure','-textvariable','gasPressure')
        rC(rpName,'configure','-increment',rpItem[6],'-format','%0.{}f'.format(rpItem[2]))
        rC(rpName,'configure','-validate','key','-vcmd','{} %W {} {} %P %s'.format(valspin,rpType,rpItem[2]))
        rC('label',rpName + 'L','-text',rpItem[7])
        if rpItem[1] not in ['cut-mode', 'gas-pressure']:
            rC('grid', rpName,'-column',0,'-row',rpRow)
            rC('grid', rpName + 'L','-column',1,'-row',rpRow,'-sticky','W')
        rpRow += 1
    # checkbox frame
    rC('labelframe','.runs.check','-text','Cut','-relief','groove')
    rC('checkbutton','.runs.check.av','-variable','autoVolts','-command','auto_volts_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label','.runs.check.avL','-text','Use Auto Volts')
    rC('checkbutton','.runs.check.ohmic','-variable','ohmicEnable','-command','ohmic_enable_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label','.runs.check.ohmicL','-text','Ohmic Probe Enable')
    rC('checkbutton','.runs.check.mesh','-variable','meshEnable','-command','pmx485_mesh_enable_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label','.runs.check.meshL','-text','Mesh Mode')
    rC('checkbutton','.runs.check.ignoreok','-variable','ignorArcOk','-command','ignore_arc_ok_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label','.runs.check.ignoreokL','-text','Ignore Arc OK')
    # populate the frame
    rC('grid','.runs.check.av','-column',0,'-row',0,'-sticky','w')
    rC('grid','.runs.check.avL','-column',1,'-row',0,'-sticky','w')
    rC('grid','.runs.check.ohmic','-column',0,'-row',1,'-sticky','w')
    rC('grid','.runs.check.ohmicL','-column',1,'-row',1,'-sticky','w')
    rC('grid','.runs.check.mesh','-column',0,'-row',2,'-sticky','w')
    rC('grid','.runs.check.meshL','-column',1,'-row',2,'-sticky','w')
    rC('grid','.runs.check.ignoreok','-column',0,'-row',3,'-sticky','w')
    rC('grid','.runs.check.ignoreokL','-column',1,'-row',3,'-sticky','w')

    # pmx frame
    rC('labelframe','.runs.pmx','-text','Powermax','-relief','groove')
    rC('checkbutton','.runs.pmx.enable','-text','Powermax Comms','-variable','pmx485Enable','-command','pmx485_enable_toggled','-width',2,'-anchor','w','-indicatoron',0,'-selectcolor',ourGreen)
    rC('label','.runs.pmx.info','-text','PMX Info goes here','-anchor','w')
    rC('pack','.runs.pmx.enable','-expand',1,'-fill','x')
    rC('pack','.runs.pmx.info','-expand',1,'-fill','x')
    # populate the run panel
    rC('grid','.runs.materials','-column',0,'-row',0,'-sticky','new','-padx',2,'-pady',(0,2))
    rC('grid','.runs.material','-column',0,'-row',1,'-sticky','new','-padx',2,'-pady',(0,2))
    rC('grid','.runs.check','-column',0,'-row',2,'-sticky','new','-padx',2,'-pady',(0,2))
    # rC('grid','.runs.pmx','-column',0,'-row',3,'-sticky','new','-padx',2,'-pady',(0,2))
    rC('grid','.runs','-column',3,'-row',1,'-rowspan',2,'-sticky','nsew','-padx',1,'-pady',1)

    # bottom pane widgets
    # configure
    rC(ft,'configure','-relief','flat','-pady',0)
    rC(ft + '.sb','configure','-bd',1)
    rC(ft + '.sb','configure','-width', 16)
    rC(ft + '.text','configure','-width',10,'-height',6,'-borderwidth',1,'-relief','sunken')
    # populate
    rC('grid',fleds,'-column',0,'-row',1,'-padx',(2,0),'-pady',2,'-sticky','nsew')
    rC('pack',ft + '.sb','-fill','y','-side','left','-padx',1)
    rC('pack',ft + '.text','-fill','both','-expand',1,'-side','left','-pady',0)

    # new conversational frames
    rC('frame','.toolconv','-borderwidth',1,'-relief','raised')
    rC('frame','.fconv','-relief','flat')

    # change jog slider resolution
    rC('.pane.top.jogspeed.s', 'configure','-resolution',0.00001)

    # change some existing help text
    dels = [24,23,22,20,19,18,17]
    for d in dels:
        del help1[d]
    del help1[4]
    help1.insert(10,('Control+ `,1..9,0', _('Set Rapid Override from 0% to 100%')),)
    help1.insert(11,('Alt+ `,1..9,0', _('Set Jog Speed from 0% to 100%')),)

    # remove redundant bindings
    root_window.unbind('R') # reverse
    root_window.unbind('F') # forward
    root_window.unbind('<Key-F7>') # mist toggle
    root_window.unbind('<Key-F8>') # flood toggle
    root_window.unbind('<Key-F9>') # spindle forward toggle
    root_window.unbind('<Key-F10>') # spindle backward toggle
    root_window.unbind('<Key-F11>') # spindle decrease
    root_window.unbind('<Key-F12>') # spindle increase
    root_window.unbind('B') # brake on
    root_window.unbind('b') # brake off

    # new key bindings
    root_window.bind('<Escape>', commands.task_stop)
    root_window.bind('<Key-F9>', commands.manual_cut)
    root_window.bind('<Control-Key-quoteleft>',lambda event: set_rapidrate(0))
    root_window.bind('<Control-Key-1>',lambda event: set_rapidrate(10))
    root_window.bind('<Control-Key-2>',lambda event: set_rapidrate(20))
    root_window.bind('<Control-Key-3>',lambda event: set_rapidrate(30))
    root_window.bind('<Control-Key-4>',lambda event: set_rapidrate(40))
    root_window.bind('<Control-Key-5>',lambda event: set_rapidrate(50))
    root_window.bind('<Control-Key-6>',lambda event: set_rapidrate(60))
    root_window.bind('<Control-Key-7>',lambda event: set_rapidrate(70))
    root_window.bind('<Control-Key-8>',lambda event: set_rapidrate(80))
    root_window.bind('<Control-Key-9>',lambda event: set_rapidrate(90))
    root_window.bind('<Control-Key-0>',lambda event: set_rapidrate(100))
    root_window.bind('<Alt-Key-quoteleft>',lambda event: set_jog_slider(0.0))
    root_window.bind('<Alt-Key-1>',lambda event: set_jog_slider(0.1))
    root_window.bind('<Alt-Key-2>',lambda event: set_jog_slider(0.2))
    root_window.bind('<Alt-Key-3>',lambda event: set_jog_slider(0.3))
    root_window.bind('<Alt-Key-4>',lambda event: set_jog_slider(0.4))
    root_window.bind('<Alt-Key-5>',lambda event: set_jog_slider(0.5))
    root_window.bind('<Alt-Key-6>',lambda event: set_jog_slider(0.6))
    root_window.bind('<Alt-Key-7>',lambda event: set_jog_slider(0.7))
    root_window.bind('<Alt-Key-8>',lambda event: set_jog_slider(0.8))
    root_window.bind('<Alt-Key-9>',lambda event: set_jog_slider(0.9))
    root_window.bind('<Alt-Key-0>',lambda event: set_jog_slider(1.0))

    # remove all tooltips
    rC('DynamicHelp::delete','ftabs_manual.axes.axisx')
    for w in toolButtons:
        rC('DynamicHelp::delete','.toolbar.{}'.format(w))


##############################################################################
# INITIALIZATION                                                             #
##############################################################################
    # reinitialize notifications to keep them on top of new widgets
    notifications.__init__(root_window)
    font_size_changed()
    update_title()
    o.show_overlay = False
    hal.set_p('plasmac.mode', '{}'.format(pVars.plasmacMode.get()))
    hal.set_p('plasmac.torch-enable', '0')
    hal.set_p('plasmac.height-override', '{:0.3f}'.format(torchHeight))
    hal.set_p('plasmac.thc-feed-rate', '{}'.format(thcFeedRate))
    pVars.previewLarge.set(False)
    pVars.laserText.set(_('Laser'))
    value = getPrefs(PREF,'ENABLE_OPTIONS', 'THC enable', False, bool)
    pVars.thcEnable.set(value)
    hal.set_p('plasmac.thc-enable', str(value))
    value = getPrefs(PREF,'ENABLE_OPTIONS', 'Corner lock enable', False, bool)
    pVars.cornerEnable.set(value)
    hal.set_p('plasmac.cornerlock-enable', str(value))
    value = getPrefs(PREF,'ENABLE_OPTIONS', 'Kerf cross enable', False, bool)
    pVars.kerfEnable.set(value)
    hal.set_p('plasmac.kerfcross-enable', str(value))
    value = getPrefs(PREF,'ENABLE_OPTIONS', 'Use auto volts', False, bool)
    pVars.autoVolts.set(value)
    hal.set_p('plasmac.use-auto-volts', str(value))
    value = getPrefs(PREF,'ENABLE_OPTIONS', 'Ohmic probe enable', False, bool)
    pVars.ohmicEnable.set(value)
    hal.set_p('plasmac.ohmic-probe-enable', str(value))
    value = getPrefs(PREF,'GUI_OPTIONS', 'Jog speed', int(vars.max_speed.get() * 60 * 0.5), int)
    rC(fsetup + '.l.jog.speed','set',value)
    restoreSetup['jogSpeed'] = value
    set_jog_slider(value / vars.max_speed.get() / 60)
    value = getPrefs(PREF,'GUI_OPTIONS', 'Exit warning', True, bool)
    pVars.closeDialog.set(value)
    restoreSetup['closeDialog'] = value
    root_window.protocol('WM_DELETE_WINDOW', close_window)
    value = getPrefs(PREF,'GUI_OPTIONS', 'Window size', 'default', str).lower().replace(' ','')
    putPrefs(PREF,'GUI_OPTIONS', 'Window size', value, str)
    pVars.winSize.set(value)
    restoreSetup['winSize'] = value
    value = getPrefs(PREF,'GUI_OPTIONS', 'Preview cone size', 0.5, float)
    pVars.coneSize.set(value)
    restoreSetup['coneSize'] = value
    cone_size_changed()
    value = getPrefs(PREF,'GUI_OPTIONS', 'Table zoom', 1, float)
    rC(fsetup + '.l.gui.zoom','set',value)
    restoreSetup['tableZoom'] = value
    value = getPrefs(PREF,'GUI_OPTIONS','Cut recovery speed %', 20, int)
    restoreSetup['crPercent'] = value
    rC(fsetup + '.l.cr.speed','set',value)
    statDivisor = 1000 if unitsPerMm == 1 else 1
    statSuffix = 'M' if unitsPerMm == 1 else '"'
    # we bring in some ints as floats so we can read QtPlasmaC statistics
    pVars.lengthS.set(getPrefs(PREF,'STATISTICS', 'Cut length', 0, float))
    pVars.lengthJ.set('0.00{}'.format(statSuffix))
    pVars.lengthT.set('{:0.2f}{}'.format(pVars.lengthS.get() / statDivisor, statSuffix))
    pVars.pierceS.set(getPrefs(PREF,'STATISTICS', 'Pierce count', 0, int))
    pVars.pierceJ.set('0')
    pVars.pierceT.set(pVars.pierceS.get())
    pVars.rapidS.set(int(getPrefs(PREF,'STATISTICS', 'Rapid time', 0, float)))
    pVars.rapidJ.set('00:00:00')
    pVars.rapidT.set(secs_to_hms(pVars.rapidS.get()))
    pVars.probeS.set(int(getPrefs(PREF,'STATISTICS', 'Probe time', 0, float)))
    pVars.probeJ.set('00:00:00')
    pVars.probeT.set(secs_to_hms(pVars.probeS.get()))
    pVars.torchS.set(int(getPrefs(PREF,'STATISTICS', 'Torch on time', 0, float)))
    pVars.torchJ.set('00:00:00')
    pVars.torchT.set(secs_to_hms(pVars.torchS.get()))
    pVars.pausedS.set(int(getPrefs(PREF,'STATISTICS', 'Paused time', 0, float)))
    pVars.pausedJ.set('00:00:00')
    pVars.pausedT.set(secs_to_hms(pVars.pausedS.get()))
    pVars.cutS.set(int(getPrefs(PREF,'STATISTICS', 'Cut time', 0, float)))
    pVars.cutJ.set('00:00:00')
    pVars.cutT.set(secs_to_hms(pVars.cutS.get()))
    pVars.runS.set(int(getPrefs(PREF,'STATISTICS', 'Program run time', 0, float)))
    pVars.runJ.set('00:00:00')
    pVars.runT.set(secs_to_hms(pVars.runS.get()))
    laser_button_enable()
    set_probe_offset_pins()
    for widget in wLeds:
        rC(widget,'configure','-state','disabled')
        widgetValues[widget] = 0

    comboFg = rC(fsetup + '.r.ubuttons.name1','cget','-fg')
    comboBg = rC(fsetup + '.r.ubuttons.name1','cget','-bg')
    for widget in wCombos:
        rC(widget,'configure','-selectforeground',comboFg)
        rC(widget,'configure','-selectbackground',comboBg)

    halPinList = hal.get_info_pins()
    load_param_clicked()
    mode_changed()
    pmPort = getPrefs(PREF,'POWERMAX', 'Port', '', str)
    if pmPort:
        try:
            import serial.tools.list_ports as PORTS
            pmPort = getPrefs(PREF,'POWERMAX', 'Port', '', str)
            ports = []
            for p in PORTS.comports():
                ports.append(p[0])
            if pmPort not in ports:
                title = 'PORT ERROR'
                msg0 = 'cannot be found'
                msg1 = 'Powermax communications is disabled'
                notifications.add('error', '{}:\n{} {}\n{}\n'.format(title, pmPort, msg0, msg1))
                pmPort = None
            rC('grid','.runs.pmx','-column',0,'-row',3,'-sticky','new','-padx',2,'-pady',(0,2))
            rC('grid',stats + '.arcL','-column',0,'-row',9,'-pady',(8,0))
            rC('grid',stats + '.arcT','-column',2,'-row',9,'-pady',(8,0))
        except:
            title = 'MODULE ERROR'
            msg0 = 'python3-serial cannot be found'
            msg1 = 'Install python3-serial or linuxcnc-dev'
            notifications.add('error', '{}:\n{}\n{}\n'.format(title, msg0, msg1))
            pmPort = None
    set_window_size()

else:
    firstRun = 'invalid'
    title = _('LOAD ERROR')
    msg0 = _('Cannot find valid library directory')
    msg1 = _('PlasmaC2 extensions are not loaded')
    notifications.add('error', '{}:\n{}\n{}\n{}\n'.format(title, msg0, os.path.expanduser('~/linuxcnc/plasmac2/lib'), msg1))


##############################################################################
# HAL SETUP - CALLED DIRECTLY FROM AXIS ONCE AT STARTUP                      #
##############################################################################
def user_hal_pins():
    global firstRun, previewSize
    if firstRun == 'invalid':
        return
    # create new hal pins
    comp.newpin('arc-voltage', hal.HAL_FLOAT, hal.HAL_IN)
    comp.newpin('led-arc-ok', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-torch', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-thc-enabled', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-ohmic', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-float', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-breakaway', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-thc-active', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-up', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-down', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-corner-locked', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('led-kerf-locked', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('refresh', hal.HAL_S32, hal.HAL_IN)
    comp.newpin('material-change-number', hal.HAL_S32, hal.HAL_IN)
    comp.newpin('material-change', hal.HAL_S32, hal.HAL_IN)
    comp.newpin('material-change-timeout', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('material-reload', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('material-temp', hal.HAL_S32, hal.HAL_IN)
    comp.newpin('kerf-width', hal.HAL_FLOAT, hal.HAL_OUT)
    comp.newpin('cut-type', hal.HAL_S32, hal.HAL_IN)
    comp.newpin('thc-enable-out', hal.HAL_BIT, hal.HAL_OUT)
    comp.newpin('program-is-idle', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('laser-on', hal.HAL_BIT, hal.HAL_OUT)
    comp.newpin('preview-tab', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('development', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('conv-block-loaded', hal.HAL_BIT, hal.HAL_IN)
    comp.newpin('offset-set-probe', hal.HAL_BIT, hal.HAL_OUT)
    comp.newpin('offset-set-scribe', hal.HAL_BIT, hal.HAL_OUT)
    # create some new signals and connect pins
    hal_data = [[0,'plasmac:arc-voltage-out','plasmac.arc-voltage-out','axisui.arc-voltage'],\
                [1,'plasmac:axis-x-min-limit','ini.x.min_limit','plasmac.axis-x-min-limit'],\
                [2,'plasmac:axis-x-max-limit','ini.x.max_limit','plasmac.axis-x-max-limit'],\
                [3,'plasmac:axis-y-min-limit','ini.y.min_limit','plasmac.axis-y-min-limit'],\
                [4,'plasmac:axis-y-max-limit','ini.y.max_limit','plasmac.axis-y-max-limit'],\
                [5,'plasmac:axis-z-min-limit','ini.z.min_limit','plasmac.axis-z-min-limit'],\
                [6,'plasmac:axis-z-max-limit','ini.z.max_limit','plasmac.axis-z-max-limit'],\
                [7,'plasmac:arc-ok-out','plasmac.arc-ok-out','axisui.led-arc-ok'],\
                [8,'plasmac:thc-enabled','plasmac.thc-enabled','axisui.led-thc-enabled'],\
                [9,'plasmac:thc-active','plasmac.thc-active','axisui.led-thc-active'],\
                [10,'plasmac:led-up','plasmac.led-up','axisui.led-up'],\
                [11,'plasmac:led-down','plasmac.led-down','axisui.led-down'],\
                [11,'plasmac:cornerlock-is-locked','plasmac.cornerlock-is-locked','axisui.led-corner-locked'],\
                [13,'plasmac:kerfcross-is-locked','plasmac.kerfcross-is-locked','axisui.led-kerf-locked'],\
                [14,'plasmac:offset-set-probe','plasmac.offset-set-probe','axisui.offset-set-probe'],\
                [15,'plasmac:offset-set-scribe','plasmac.offset-set-scribe','axisui.offset-set-scribe'],\
                ]
    for line in hal_data:
        if line[0] < 7:
            hal.new_sig(line[1],hal.HAL_FLOAT)
        else:
            hal.new_sig(line[1],hal.HAL_BIT)
        hal.connect(line[2],line[1])
        hal.connect(line[3],line[1])
    # connect pins to some existing signals
    hal.connect('axisui.led-ohmic','plasmac:ohmic-probe-out')
    hal.connect('axisui.led-float','plasmac:float-switch-out')
    hal.connect('axisui.led-breakaway','plasmac:breakaway-switch-out')
    hal.connect('axisui.led-torch','plasmac:torch-on')
    # connect laser-on if it exists
    laser = False
    for signal in hal.get_info_signals():
        if signal['NAME'] == 'plasmac:laser-on':
            laser = True
            break
    if laser:
        hal.connect('axisui.laser-on','plasmac:laser-on')
    # initialize halpin variables
    materialChangePin = comp['material-change']
    materialChangeNumberPin = comp['material-change-number']
    materialChangeTimeoutPin = comp['material-change-timeout']
    materialReloadPin = comp['material-reload']
    materialTempPin = comp['material-temp']
    # do user button setup after hal pin creation
    user_button_setup()
    # load materials when setup is complete
    load_materials()
    # start powermax comms if valid port
    if pmPort:
        pmx485_startup(pmPort)
    # check preferences for a file to load
    addRecent = True
    openFile = getPrefs(PREF,'GUI_OPTIONS','Open file', '', str)
    loadLast = True if openFile == 'last' else False
    if loadLast:
        openFile = ap.getpref('recentfiles', [], repr).pop(0) if len(ap.getpref('recentfiles', [], repr)) else None
        addRecent = False
    elif openFile:
        openFile = os.path.join(open_directory,openFile)
    # load the file
    if openFile:
        if os.path.exists(openFile):
            open_file_guts(openFile, False, addRecent)
            commands.set_view_z()
        else:
            title = 'FILE ERROR'
            msg0 = 'does not exist'
            notifications.add('error', '{}:\n"{}" {}\n'.format(title, os.path.realpath(openFile), msg0))
    # run users custom hal commands if it exists
    if os.path.isfile(os.path.join(configPath, 'user_hal.py')):
        exec(open(os.path.join(configPath, 'user_hal.py')).read())
    # the first run has successfully completed
    firstRun = None
    # run users custom python commands if it exists
    if os.path.isfile(os.path.join(configPath, 'user_commands.py')):
        exec(open(os.path.join(configPath, 'user_commands.py')).read())
    previewSize = {'w':rC('winfo','width',tabs_preview), 'h':rC('winfo','height',tabs_preview)}


##############################################################################
# UPDATE FUNCTION - CALLED FROM AXIS EVERY CYCLE                             #
##############################################################################
def user_live_update():
    # don't do any updates until first run is complete.
    if firstRun:
        return
    global isIdle, isIdleHomed, isPaused, isRunning
    global runState, pausedState, relPos
    global probeTimer, probeStart, probeButton
    global probeText, probePressed, previewSize
    global torchTimer, torchStart, torchButton
    global torchText, torchPressed, torchColor
    global laserTimer, laserButtonState
    global framingState, activeFunction
    global currentTool, pmx485
    global materialChangePin, materialChangeNumberPin
    global materialReloadPin, materialTempPin
    global materialChangeTimeoutPin
    #set machine state variables
    isIdle = s.task_state == linuxcnc.STATE_ON and s.interp_state == linuxcnc.INTERP_IDLE
    isIdleHomed = isIdle and all_homed()
    isPaused = s.task_state == linuxcnc.STATE_ON and s.paused
    isRunning = not s.interp_state == linuxcnc.INTERP_IDLE and not s.paused
    # set current x and y relative positions
    relPos['X'] = round(s.position[0] - s.g5x_offset[0] - s.g92_offset[0], 6)
    relPos['Y'] = round(s.position[1] - s.g5x_offset[1] - s.g92_offset[1], 6)
#FIXME: WE MAY WANT TO MAKE THIS OPTIONAL WITH A CHECKBOX
    # set display units
    if o.canon:
        if 200 in o.canon.state.gcodes:
            vars.metric.set(0)
        else:
            vars.metric.set(1)
    else:
        vars.metric.set(s.linear_units == 1)
    # program has started
    if running() and not runState:
        runState = True
        clear_job_stats()
    # program has ended
    elif not running() and runState:
        runState = False
        save_total_stats()
        # reset single-cut
        if singleCut['G91']:
            ensure_mode(linuxcnc.MODE_MDI)
            c.mdi('G91')
            ensure_mode(linuxcnc.MODE_MANUAL)
    # override standard tool info
    if current_tool.id != currentTool:
        currentTool = current_tool.id
        if currentTool < 1:
            tool = 'Torch'
        elif currentTool == 1:
            tool = 'Scribe'
        vupdate(pVars.plasmatool, 'Tool: {}'.format(tool))
    # update status leds
    for widget in wLeds:
        tmp, item = widget.rsplit('.',1)
        if comp[item] != widgetValues[widget]:
            widgetValues[widget] = comp[item]
            if comp[item] == 1:
                rC(widget,'configure','-state','normal')
            else:
                rC(widget,'configure','-state','disabled')
    # update arc voltage
    rC(fplasma + '.arc-voltage','configure','-text','{:3.0f}v'.format(comp['arc-voltage']))
    # probe-test
    if probeTimer > 0:
        if hal.get_value('plasmac.probe-test-error') and not probePressed:
            probeTimer = 0
        elif time.time() >= probeStart + 0.1:
            probeStart += 0.1
            probeTimer -= 0.1
            rC('.fbuttons.button' + probeButton,'configure','-text',str(round(probeTimer, 1)))
    elif probeStart and probeTimer <= 0 and not probePressed:
        hal.set_p('plasmac.probe-test','0')
        rC('.fbuttons.button' + probeButton,'configure','-text',probeText)
        rC('.fbuttons.button' + probeButton,'configure','-bg',buttonBackG)
        probeStart = 0
        probeTimer = 0
        activeFunction = False
    # torch pulse
    if torchTimer > 0:
        if time.time() >= torchStart + 0.1:
            torchStart += 0.1
            torchTimer -= 0.1
            rC('.fbuttons.button' + torchButton,'configure','-text',str(abs(round(torchTimer, 1))))
    elif torchStart and torchTimer <= 0 and not torchPressed:
        hal.set_p('plasmac.torch-pulse-start','0')
        hal.set_p('plasmac.torch-pulse-time', '0')
        rC('.fbuttons.button' + torchButton,'configure','-text',torchText)
        rC('.fbuttons.button' + torchButton,'configure','-bg',buttonBackG)
        torchStart = 0
        torchTimer = 0
    # halpin toggle
    for key in togglePins:
        if hal.get_value(togglePins[key]['pin']) != togglePins[key]['state']:
            togglePins[key]['state'] = hal.get_value(togglePins[key]['pin'])
            if togglePins[key]['state']:
                rC('.fbuttons.button' + togglePins[key]['button'],'configure','-bg',ourGreen)
            else:
                if togglePins[key]['runcritical']:
                    rC('.fbuttons.button' + togglePins[key]['button'],'configure','-bg',ourRed)
                else:
                    rC('.fbuttons.button' + togglePins[key]['button'],'configure','-bg',buttonBackG)
        if togglePins[key]['runcritical']:
            if togglePins[key]['state'] and rC('.toolbar.program_run','cget','-state') != 'normal' and isIdleHomed:
                rC('.toolbar.program_run','configure','-state','normal')
            elif not togglePins[key]['state'] and rC('.toolbar.program_run','cget','-state') != 'disabled':
                rC('.toolbar.program_run','configure','-state','disabled')
    # halpin pulse
    for key in pulsePins:
        # service the timers
        if pulsePins[key]['timer']:
            if time.time() >= pulsePins[key]['counter'] + 0.1:
                pulsePins[key]['counter'] += 0.1
                pulsePins[key]['timer'] -= 0.1
                rC('.fbuttons.button' + pulsePins[key]['button'],'configure','-text',str(abs(round(pulsePins[key]['timer'], 1))))
                if pulsePins[key]['timer'] <= 0:
                    pulsePins[key]['timer'] = 0
                    rC('.fbuttons.button' + pulsePins[key]['button'],'configure','-text',pulsePins[key]['text'])
                    hal.set_p(pulsePins[key]['pin'], str(not hal.get_value(pulsePins[key]['pin'])))
        # set button color for pulse-halpin buttons
        if hal.get_value(pulsePins[key]['pin']) != pulsePins[key]['state']:
            pulsePins[key]['state'] = hal.get_value(pulsePins[key]['pin'])
            if pulsePins[key]['state']:
                rC('.fbuttons.button' + pulsePins[key]['button'],'configure','-bg',ourGreen)
            else:
                rC('.fbuttons.button' + pulsePins[key]['button'],'configure','-bg',buttonBackG)
    # reset a consumable change
    if (hal.get_value('plasmac.consumable-change') or hal.get_value('plasmac.consumable-change')) and \
       (hal.get_value('axisui.abort') or not s.paused):
        hal.set_p('plasmac.consumable-change', '0')
        hal.set_p('plasmac.x-offset', '0')
        hal.set_p('plasmac.y-offset', '0')
        hal.set_p('plasmac.xy-feed-rate', '0')
        rC('.fbuttons.button{}'.format(cChangeButton),'configure','-bg',buttonBackG)
        activeFunction = False
    # abort a manual cut
    if manualCut['state'] and not hal.get_value('spindle.0.on'):
        manualCut['state'] = False
        vars.jog_speed.set(manualCut['feed'])
        rC('.pane.top.jogspeed.s','configure','-state','normal')
        save_total_stats()
    # laser timer
    if laserTimer > 0:
        laserTimer -= 0.1
        if laserTimer <= 0:
            comp['laser-on'] = 0
            laserButtonState = 'reset'
            pVars.laserText.set(_('Laser'))
    # show cut recovery tab
    if s.paused and 'manual' in rC(ftabs,'pages'):
        rC(ftabs,'delete','manual',0)
        rC(ftabs,'delete','mdi',0)
        rC(ftabs,'insert','end','cutrecs')
        rC(ftabs,'raise','cutrecs')
        rC(ftabs,'itemconfigure','cutrecs','-text','Cut Recovery')
    # hide cut recovery tab
    if not s.paused and 'cutrecs' in rC(ftabs,'pages') and \
       (not hal.get_value('plasmac.paused-motion') or \
       hal.get_value('axisui.abort') or \
       s.task_state == linuxcnc.STATE_ESTOP):
        rC(ftabs,'delete','cutrecs',0)
        rC(ftabs,'insert','end','manual')
        rC(ftabs,'insert','end','mdi')
        rC(ftabs,'raise','manual')
        rC(ftabs,'itemconfigure','manual','-text','Manual')
        rC(ftabs,'itemconfigure','mdi','-text','MDI')
    # if resumed and component has completed a cut recovery then cancel cut recovey
    if not s.paused and not hal.get_value('plasmac.cut-recovering') and hal.get_value('plasmac.cut-recovery'):
        cut_rec_cancel()
    # if consumable change finished then clear offsets
    if hal.get_value('plasmac.state-out') == 26:
        hal.set_p('plasmac.x-offset', '0')
        hal.set_p('plasmac.y-offset', '0')
    # if resumed and laser recovery is active then undo laser offset
    if not s.paused and  hal.get_value('plasmac.laser-recovery-state') and hal.get_value('plasmac.laser-recovery-start'):
        hal.set_p('plasmac.laser-recovery-start', '0')
    # reset framing when complete
    if framingState and isIdle:
        comp['laser-on'] = 0
        framingState = False
        activeFunction = False
        live_plotter.clear()
    # set X0Y0, laser, and offset_setup buttons state
    if isIdleHomed:
        rC(fjogf + '.zerohome.zeroxy','configure','-state','normal')
        rC(fjogf + '.zerohome.laser','configure','-state','normal')
        rC(fsetup + '.utilities.offsets','configure','-state','normal')
    else:
        rC(fjogf + '.zerohome.zeroxy','configure','-state','disabled')
        rC(fjogf + '.zerohome.laser','configure','-state','disabled')
        rC(fsetup + '.utilities.offsets','configure','-state','disabled')
    # set height override buttons state
    if isIdle or isPaused or isRunning:
        rC(foverride + '.raise','configure','-state','normal')
        rC(foverride + '.lower','configure','-state','normal')
        rC(foverride + '.reset','configure','-state','normal')
    else:
        rC(foverride + '.raise','configure','-state','disabled')
        rC(foverride + '.lower','configure','-state','disabled')
        rC(foverride + '.reset','configure','-state','disabled')
    # set user buttons state
    for n in range(1,21):
        if buttonCodes[n]['code']:
            if buttonCodes[n]['code'] == 'ohmic-test':
                if isIdle:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'cut-type':
                if not isRunning and not isPaused:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'single-cut':
#                if isIdleHomed and not activeFunction and rC('.toolbar.program_run','cget','-state').string == 'normal':
                if isIdleHomed and not activeFunction and rC('.toolbar.program_run','cget','-state') == 'normal':
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'manual-cut':
#                if isIdleHomed and not activeFunction and rC('.toolbar.program_run','cget','-state').string == 'normal':
                if isIdleHomed and not activeFunction and rC('.toolbar.program_run','cget','-state') == 'normal':
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'probe-test':
                if isIdleHomed and (not activeFunction or probeTimer):
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'torch-pulse':
                if isIdleHomed and not activeFunction and hal.get_value('plasmac.torch-enable'):
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'change-consumables':
                if isPaused and (not activeFunction or hal.get_value('plasmac.consumable-change')):
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'framing':
                if isIdleHomed and not activeFunction:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'load':
                if isIdleHomed and not activeFunction:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'latest-file':
                if isIdleHomed and not activeFunction:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'pulse-halpin':
                if isIdle:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'] == 'toggle-halpin':
                if isIdle:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            elif buttonCodes[n]['code'][0] == '%':
                if isIdle or isPaused or isRunning:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
            else:
                if isIdleHomed and not activeFunction:
                    rC('.fbuttons.button' + str(n),'configure','-state','normal')
                else:
                    rC('.fbuttons.button' + str(n),'configure','-state','disabled')
    # material handling
    if materialChangePin != comp['material-change']:
        materialChangePin = comp['material-change']
        material_change_pin_changed(materialChangePin)
    if materialChangeNumberPin != comp['material-change-number']:
        materialChangeNumberPin = comp['material-change-number']
        material_change_number_pin_changed(materialChangeNumberPin)
    if materialChangeTimeoutPin != comp['material-change-timeout']:
        materialChangeTimeoutPin = comp['material-change-timeout']
        material_change_timeout_pin_changed(materialChangeTimeoutPin)
    if materialReloadPin != comp['material-reload']:
        materialReloadPin = comp['material-reload']
        material_reload_pin_changed(materialReloadPin)
    if materialTempPin != comp['material-temp']:
        materialTempPin = comp['material-temp']
        material_temp_pin_changed(materialTempPin)
    # try to show the preview tab if hal pin is set
    if comp['preview-tab']:
        try:
            rC('.pane.top.right','raise','preview')
            comp['preview-tab'] = 0
        except:
            pass
    # allows user to set a HAL pin to initiate the sequence of:
    # reloading the program
    if comp['refresh'] == 1:
        comp['refresh'] = 2
        commands.reload_file()
    # clearing the live plot
    elif comp['refresh'] == 2:
        comp['refresh'] = 3
        commands.clear_live_plot()
    # rezooming the axis
    elif comp['refresh'] == 3:
        comp['refresh'] = 0
        commands.set_view_z()
    # powermax signals
    if pmx485['exists']:
        if pmx485['compStatus'] != hal.get_value('pmx485.status'):
            pmx485['compStatus'] = hal.get_value('pmx485.status')
            pmx485_status_changed(pmx485['compStatus'])
        if pmx485['compFault'] != hal.get_value('pmx485.fault'):
            pmx485['compFault'] = hal.get_value('pmx485.fault')
            pmx485_fault_changed(pmx485['compFault'])
        if pmx485['compArcTime'] != hal.get_value('pmx485.arcTime'):
            pmx485['compArcTime'] = hal.get_value('pmx485.arcTime')
#FIXME: PROBABLY NOT REQUIRED AS WE CHANGE THE TEXT DIRECTLY, HERE IN PERIODIC
            #pmx485_arc_time_changed(pmx485['compArcTime'])
            pVars.arcT.set(secs_to_hms(pmx485['compArcTime']))
        if pmx485['compMinC'] != hal.get_value('pmx485.current_min'):
            pmx485['compMinC'] = hal.get_value('pmx485.current_min')
            pmx485_min_current_changed()
        if pmx485['compMaxC'] != hal.get_value('pmx485.current_max'):
            pmx485['compMaxC'] = hal.get_value('pmx485.current_max')
            pmx485_max_current_changed()
        if pmx485['compMaxP'] != hal.get_value('pmx485.pressure_max'):
            pmx485['compMaxP'] = hal.get_value('pmx485.pressure_max')
            pmx485_max_pressure_changed()
        if pmx485['commsTimer']:
            pmx485['commsTimer'] -= 0.1
            if pmx485['commsTimer'] <= 0:
                pmx485['commsTimer'] = 0
                pmx485_comms_timeout()
        if pmx485['retryTimer']:
            pmx485['retryTimer'] -= 0.1
            if pmx485['retryTimer'] <= 0:
                pmx485['retryTimer'] = 0
                pmx485_retry_timeout()
    # hide/show override limits checkbox
    if vars.on_any_limit.get() and not rC('winfo','ismapped',flimitovr):
        rC('grid',flimitovr,'-row',1,'-column',0,'-columnspan',3,'-sticky','nsew')
    elif not vars.on_any_limit.get() and rC('winfo','ismapped',flimitovr):
        rC(flimitovr + '.button','invoke')
        rC('grid','forget',flimitovr)
    # hide/show jog inhibit override checkbox
    if rC('winfo','ismapped',fjogiovr):
        if pVars.jogInhibitOvr.get():
            hal.set_p('plasmac.override-jog', '1')
        if not hal.get_value('plasmac.breakaway') and \
           not hal.get_value('plasmac.float-switch') and \
           not hal.get_value('plasmac.ohmic-probe'):
            pVars.jogInhibitOvr.set(False)
            rC('grid','forget',fjogiovr)
    else:
        if hal.get_value('plasmac.jog-inhibit'):
            if isIdleHomed:
                rC('grid',fjogiovr,'-column',0,'-row',1,'-columnspan',3,'-sticky','nsew')
        else:
            if not hal.get_value('plasmac.breakaway') and \
               not hal.get_value('plasmac.float-switch') and \
               not hal.get_value('plasmac.ohmic-probe'):
                hal.set_p('plasmac.override-jog', '0')
    # statistics
    if runState or manualCut['state']:
        # cut length
        sNow = int(hal.get_value('plasmac.cut-length') + 0.5)
        if statValues['length'] != sNow:
            if sNow:
                pVars.lengthJ.set('{:0.2f}{}'.format(sNow / statDivisor, statSuffix))
                if hal.get_value('plasmac.torch-enable'):
                    pVars.lengthT.set('{:0.2f}{}'.format((sNow + pVars.lengthS.get()) / statDivisor, statSuffix))
            statValues['length'] = sNow
        # pierce count
        sNow = hal.get_value('plasmac.pierce-count')
        if statValues['pierce'] != sNow:
            if sNow:
                pVars.pierceJ.set(sNow)
                if hal.get_value('plasmac.torch-enable'):
                    pVars.pierceT.set(sNow + pVars.pierceS.get())
            statValues['pierce'] = sNow
        # rapid time
        sNow = int(hal.get_value('plasmac.rapid-time') + 0.5)
        if statValues['rapid'] != sNow:
            if sNow:
                pVars.rapidJ.set(secs_to_hms(sNow))
                if hal.get_value('plasmac.torch-enable'):
                    pVars.rapidT.set(secs_to_hms(sNow + pVars.rapidS.get()))
            statValues['rapid'] = sNow
        # probe time
        sNow = int(hal.get_value('plasmac.probe-time') + 0.5)
        if statValues['probe'] != sNow:
            if sNow:
                pVars.probeJ.set(secs_to_hms(sNow))
                if hal.get_value('plasmac.torch-enable'):
                    pVars.probeT.set(secs_to_hms(sNow + pVars.probeS.get()))
            statValues['probe'] = sNow
        # torch time
        sNow = int(hal.get_value('plasmac.torch-time') + 0.5)
        if statValues['torch'] != sNow:
            if sNow:
                pVars.torchJ.set(secs_to_hms(sNow))
                if hal.get_value('plasmac.torch-enable'):
                    pVars.torchT.set(secs_to_hms(sNow + pVars.torchS.get()))
            statValues['torch'] = sNow
        # cut time
        sNow = int(hal.get_value('plasmac.cut-time') + 0.5)
        if statValues['cut'] != sNow:
            if sNow:
                pVars.cutJ.set(secs_to_hms(sNow))
                if hal.get_value('plasmac.torch-enable'):
                    pVars.cutT.set(secs_to_hms(sNow + pVars.cutS.get()))
            statValues['cut'] = sNow
        # paused time
        sNow = int(hal.get_value('plasmac.paused-time') + 0.5)
        if statValues['paused'] != sNow:
            if sNow:
                pVars.pausedJ.set(secs_to_hms(sNow))
                if hal.get_value('plasmac.torch-enable'):
                    pVars.pausedT.set(secs_to_hms(sNow + pVars.pausedS.get()))
            statValues['paused'] = sNow
        # run time
        sNow = int(hal.get_value('plasmac.run-time') + 0.5)
        if statValues['run'] != sNow:
            if sNow:
                pVars.runJ.set(secs_to_hms(sNow))
                if hal.get_value('plasmac.torch-enable'):
                    pVars.runT.set(secs_to_hms(sNow + pVars.runS.get()))
            statValues['run'] = sNow
    # set table view zoom if window resized
    if get_view_type() == 't' and (previewSize['w'] != rC('winfo','width',tabs_preview) or previewSize['h'] != rC('winfo','height',tabs_preview)):
        previewSize = {'w':rC('winfo','width',tabs_preview), 'h':rC('winfo','height',tabs_preview)}
        root_window.update_idletasks()
        commands.set_view_t()

    # run users custom periodic commands if it exists
    if os.path.isfile(os.path.join(configPath, 'user_periodic.py')):
        exec(open(os.path.join(configPath, 'user_periodic.py')).read())
