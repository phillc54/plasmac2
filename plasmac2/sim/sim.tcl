# GENERIC HAL TCL FILE FOR PLASMAC SIM CONFIGS WITH STEPGENS

loadrt plasmac
addf plasmac servo-thread

# ---INPUT DEBOUNCE---
loadrt dbounce names=db_breakaway,db_float,db_ohmic,db_arc-ok
addf db_float     servo-thread
addf db_ohmic     servo-thread
addf db_breakaway servo-thread
addf db_arc-ok    servo-thread

# ---Z JOINT CONNECTION---
#net plasmac:axis-position joint.${z-axis}.pos-fb => plasmac.axis-z-position
#net plasmac:axis-position joint.${z-axis}.pos-fb => plasmac.axis-z-position
net plasmac:axis-position joint.3.pos-fb => plasmac.axis-z-position

# ---TOOL CHANGE PASSTHROUGH
#net sim:tool-number                                    <= iocontrol.0.tool-prep-number
#net sim:tool-change-loopback  iocontrol.0.tool-change  => iocontrol.0.tool-changed
#net sim:tool-prepare-loopback iocontrol.0.tool-prepare => iocontrol.0.tool-prepared

# ---ESTOP COMPONENTS FOR QTPLASMAC---
loadrt or2 names=estop_or
loadrt not names=estop_not,estop_not_1
addf estop_or    servo-thread
addf estop_not   servo-thread
addf estop_not_1 servo-thread
