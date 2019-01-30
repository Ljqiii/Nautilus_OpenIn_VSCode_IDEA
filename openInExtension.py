
from gi import require_version

require_version('Gtk', '3.0')
require_version('Nautilus', '3.0')
from gi.repository import Nautilus, GObject
from subprocess import call
import os

# path to or command
# if you can't use this command to open application, cahnge this to the application path

VSCODE = 'code'
IDEA = 'idea'

# what name do you want to see in the context menu?
VSCODENAME = 'VS Code'
IDEANAME = 'IDEA'

# always create new window?
VSCODE_NEWWINDOW = False


class VSCodeExtension(GObject.GObject, Nautilus.MenuProvider):

    def new_vscode_menu_item(self):
        return Nautilus.MenuItem(
            name='VSCodeOpen',
            label=VSCODENAME,
            tip='Opens the selected files with VSCode'
        )

    def new_idea_menu_item(self):
        return Nautilus.MenuItem(
            name='VSCodeOpenBackground',
            label=IDEANAME,
            tip='Opens VSCode in the current directory'
        )

    def new_menu(self):
        return Nautilus.MenuItem(
            name='Open in',
            label=('Open in'),
        )

    def launch_vscode(self, menu, files):
        safepaths = ''
        args = ''

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '

            # If one of the files we are trying to open is a folder
            # create a new instance of vscode
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = '--new-window '

        if VSCODE_NEWWINDOW:
            args = '--new-window '

        call(VSCODE + ' ' + args + safepaths + '&', shell=True)

    def launch_idea(self, menu, files):
        safepaths = ''

        for file in files:
            filepath = file.get_location().get_path()
            safepaths += '"' + filepath + '" '
            if os.path.isdir(filepath) and os.path.exists(filepath):
                args = '--new-window '

        call(IDEA + ' ' + safepaths + '&', shell=True)

    def get_file_items(self, window, files):

        menu = self.new_menu()

        submenu = Nautilus.Menu()
        menu.set_submenu(submenu)

        vscodemenu = self.new_vscode_menu_item()
        vscodemenu.connect('activate', self.launch_vscode, files)

        ideamenu = self.new_idea_menu_item()
        ideamenu.connect('activate', self.launch_idea, files)

        submenu.append_item(vscodemenu)
        submenu.append_item(ideamenu)

        return [menu]

    def get_background_items(self, window, current_folder):

        menu = self.new_menu()

        submenu = Nautilus.Menu()
        menu.set_submenu(submenu)

        vscodemenu = self.new_vscode_menu_item()
        vscodemenu.connect('activate', self.launch_vscode, [current_folder])

        ideamenu = self.new_idea_menu_item()
        ideamenu.connect('activate', self.launch_idea, [current_folder])

        submenu.append_item(vscodemenu)
        submenu.append_item(ideamenu)

        return [menu]
