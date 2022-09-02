
# axis.py - search environment path for user command file
if user_command_file:
    if os.path.exists(user_command_file):
        rcfile = user_command_file
    else:
        for dir in os.environ['PATH'].split(':'):
            if os.path.exists(os.path.join(dir, user_command_file)):
                rcfile = os.path.join(dir, user_command_file)
                break
        if rcfile != os.path.join(dir, user_command_file):
            root_window.tk.call("nf_dialog", ".error", _("USER_COMMAND_FILE Error"),
                '{} could not be found'.format(user_command_file), "error", 0, _("OK"))
