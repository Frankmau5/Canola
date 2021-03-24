"""Gtk3 UI """

import time as time_lib
import threading
import pathlib
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject, GLib, Gtk, Gio
import humanize
import get_media_data

class QuestionDialog(Gtk.Dialog):
    """A Small dialog to show a msg and getting a response (cancel/ok)"""
    def __init__(self, parent, d_title, msg):

        Gtk.Dialog.__init__(self, title=d_title, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        self.set_default_size(150, 100)

        label = Gtk.Label(label=msg)

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class EditDialog(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, title="Edit data", flags=0)
        self.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK)
        self.set_default_size(800,600)
        
        box =self.get_content_area()
        box.add(self.Mk_Ui())
        self.show_all()

    def Mk_Ui(self):
        return Gtk.Label(label="hello edit dialog")

class App(Gtk.Application):
    """Main object\n
    GTK3 UI Window"""
    def __init__(self):
        super().__init__(application_id='mlv.knrf.canola')
        GLib.set_application_name('canola')
        GLib.set_prgname('mlv.knrf.canola')
        
        self.window = None
        """The main window""" 
        self.backend = None
        """Backend Object """
        self.popover = None
        """Popup Menu"""
        self.switch_stack = None
        """Stack for a stackswitcher """
        self.switch_view = None
        """StackSwitcher """
        self.tree = None
        """GTK Treeview """
        self.worker_thread = None
        """Python Thread used for making database """
        self.database = None
        """The json file data """
        self.need_to_save = False
        """Switch to see if datebase needs to be save before close"""

    def do_activate(self):
        """Method makes a Window, sets size of window, sets up backend and builds UI\n
        After setting up backend this object will display a messagebox if no database is found or will load database\n
        """

        self.window = Gtk.ApplicationWindow(application=self)
        self.window.set_icon_name('mlv.knrf.canola')
        
        self.window.set_titlebar(self.mk_title_bar())
        self.window.add(self.mk_switch(self.mk_song_page(),
            self.mk_album_page(),
            self.mk_artist_page()
            ))
        
        self.window.set_default_size(1080, 720)
        self.window.show_all()
        self.backend = get_media_data.MediaData()
        if  self.backend.db_utils.db_exist() is not True:
            self.info_box()
        else:
            self.mk_store()
    
    def info_box(self):
        """Infobox that display a message\n
        Used for at start of program if no database if found"""
        dialog = Gtk.MessageDialog(
            transient_for=self.window,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Database Not Found",
        )
        dialog.format_secondary_text(
            "Please make database."
        )
        dialog.run()
        dialog.destroy()

    def info_box_no_btn(self, msg):
        """Infobox that displays a message\n
        Used as loading screen\n
        NOTE you need to destory when done"""
        dialog = Gtk.MessageDialog(
                transient_for=self.window,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                text=msg,)
        return dialog

    def mk_title_bar(self):
        """Makes GTK3 headerbar\n
        returns Gtk.HeaderBar"""
        header = Gtk.HeaderBar(
            title='Canola',
            show_close_button=True)

        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        db_btn = Gtk.ModelButton(label="Make Database")
        db_btn.connect("clicked", self.on_make_db_cmd)

        delete_btn = Gtk.ModelButton(label="Delete Database")
        delete_btn.connect("clicked", self.on_delete_db)

        delete_row_btn = Gtk.ModelButton(label="Delete row(s)")
        delete_row_btn.connect("clicked", self.on_row_delete)

        delete_file_btn = Gtk.ModelButton(label="Delete files(s)")
        delete_file_btn.connect("clicked", self.on_file_delete)

        edit_btn = Gtk.ModelButton(label="Edit row(s)")
        edit_btn.connect("clicked", self.on_edit_row)

        about_btn = Gtk.ModelButton(label="About")
        #about_btn.connect("clicked", self.on_about)


        vbox.pack_start(db_btn, False, True, 5)
        vbox.pack_start(delete_btn, False, True, 5)
        vbox.pack_start(delete_row_btn, False, True, 5)
        vbox.pack_start(delete_file_btn, False, True, 5)
        vbox.pack_start(edit_btn, False, True, 5)
        vbox.pack_start(about_btn, False, True, 5)

        vbox.show_all()
        self.popover.add(vbox)
        self.popover.set_position(Gtk.PositionType.BOTTOM)

        btn = Gtk.MenuButton(popover=self.popover)
        icon = Gio.ThemedIcon(name="preferences-system-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        btn.add(image)
        header.add(btn)
        return header

    def mk_switch(self, song_page, album_page, artist_page):
        """Makes GTK3 StackSwitcher and Stack then adds them to Gtk Box \n
        returns Gtk Box"""
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL, spacing = 5) 

        #Start of switch view
        self.switch_view = Gtk.StackSwitcher()
        self.switch_stack = Gtk.Stack()
        self.switch_view.set_halign(Gtk.Align.CENTER)

        self.switch_stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT) 
        self.switch_stack.set_transition_duration(1000) 

        self.switch_stack.add_titled(song_page, "Songs", "Songs")
        self.switch_stack.add_titled(album_page, "Albums", "Albums")
        self.switch_stack.add_titled(artist_page, "Artists", "Artists")

        self.switch_stack.show()
        self.switch_view.show()
        
        self.switch_view.set_stack(self.switch_stack)
        vbox.pack_start(self.switch_view,False,True,10)
        vbox.pack_start(self.switch_stack,False,True,10)
        return vbox

    def mk_song_page(self):
        """Makes UI for songs page on the stackswitcher\n
        returns GTK ScrolledWindow"""
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        
        store = Gtk.ListStore()
        self.tree = Gtk.TreeView(model=store)
        self.selector = self.tree.get_selection()
        self.selector.set_mode(Gtk.SelectionMode.MULTIPLE)

        column_type = Gtk.TreeViewColumn("File type")
        column_type.set_resizable(True)
        self.tree.append_column(column_type)
        
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=1)
        column.set_resizable(True)
        self.tree.append_column(column)
        column.set_sort_column_id(1)  

        column1 = Gtk.TreeViewColumn("Artist")
        column1.set_resizable(True)
        self.tree.append_column(column1)
        
        column2 = Gtk.TreeViewColumn("Album")
        column2.set_resizable(True)
        self.tree.append_column(column2)
        
        column3 = Gtk.TreeViewColumn("Year")
        column3.set_resizable(True)
        self.tree.append_column(column3)
        
        column4 = Gtk.TreeViewColumn("Track Number")
        column4.set_resizable(True)
        self.tree.append_column(column4)
        
        column5 = Gtk.TreeViewColumn("Genre")
        column5.set_resizable(True)
        self.tree.append_column(column5)
        
        column6 = Gtk.TreeViewColumn("Time")
        column6.set_resizable(True)
        self.tree.append_column(column6)
        
        column7 = Gtk.TreeViewColumn("Channel")
        column7.set_resizable(True)
        self.tree.append_column(column7)
        
        column8 = Gtk.TreeViewColumn("Bitrate")
        column8.set_resizable(True) 
        self.tree.append_column(column8)
        
        column9 = Gtk.TreeViewColumn("Sample rate")
        column9.set_resizable(True)
        self.tree.append_column(column9)
        
        column10 = Gtk.TreeViewColumn("Filesize")
        column10.set_resizable(True)
        self.tree.append_column(column10)

        column_path = Gtk.TreeViewColumn("File path")
        column_path.set_resizable(True)
        self.tree.append_column(column_path)

        _path = Gtk.CellRendererText()
        _type = Gtk.CellRendererText()
        title = Gtk.CellRendererText()
        artist = Gtk.CellRendererText()
        album = Gtk.CellRendererText()
        year = Gtk.CellRendererText()
        track_number = Gtk.CellRendererText()
        genres = Gtk.CellRendererText()
        time = Gtk.CellRendererText()
        channel = Gtk.CellRendererText()
        bitrate = Gtk.CellRendererText()
        sample_rate = Gtk.CellRendererText()
        filesize = Gtk.CellRendererText()

        column_type.pack_start(_type, True)
        column.pack_start(title, True)
        column1.pack_start(artist, True)
        column1.set_sort_column_id(2) 
        
        column2.pack_start(album,True)
        column2.set_sort_column_id(3)

        column3.pack_start(year,True)
        column3.set_sort_column_id(4)

        column4.pack_start(track_number,True)
        column4.set_sort_column_id(5)

        column5.pack_start(genres,True)
        column5.set_sort_column_id(6)

        column6.pack_start(time,True)
        column6.set_sort_column_id(7)


        column7.pack_start(channel,True)
        column8.pack_start(bitrate,True)
        column9.pack_start(sample_rate,True)
        column10.pack_start(filesize,True)
        column_path.pack_start(_path, True)  

        column_type.add_attribute(_type, "text", 0)
        column1.add_attribute(artist, "text", 2)
        column2.add_attribute(album, "text", 3)
        column3.add_attribute(year, "text", 4)
        column4.add_attribute(track_number, "text", 5)
        column5.add_attribute(genres, "text", 6)
        column6.add_attribute(time, "text", 7)
        column7.add_attribute(channel, "text", 8)
        column8.add_attribute(bitrate, "text", 9)
        column9.add_attribute(sample_rate, "text", 10)
        column10.add_attribute(filesize, "text", 11)
        column_path.add_attribute(_path, "text", 12)  

        scrolledwindow.add(self.tree)
        return scrolledwindow

    def mk_album_page(self):
        """Makes UI for album page on the stackswitcher\n
        returns GTK ScrolledWindow"""
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        return scrolledwindow

    def mk_artist_page(self):
        """Makes UI for album page on the stackswitcher\n
        returns GTK ScrolledWindow"""

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        return scrolledwindow

    def mk_store(self):
        """Make a store and add it to tree\n
        Gets data from backend and  json_utils"""
        if self.database == None:
            self.database = self.backend.db_utils.load_json()
        store = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str, str, str, str)
        for item in self.database:
            store.append([
                    item["file_type"],
                    item["title"],
                    item["artist"],
                    item["album"],
                    item["year"],
                    item["track_num"],
                    item["genres"],
                    self.human_readable_time(item["length"]),
                    item["channels"],
                    item["bitrate"],
                    item["sample_rate"],
                    self.human_readable_size(item["filesize"]),
                    item["file_path"],
                    ])
        store.set_sort_func(1, self.compare, None)
        self.tree.set_model(Gtk.TreeModelSort(model=store))

    def on_edit_row(self, button):
        """Get data needed to make an Editdialog and displays it """
        tree_selc = self.tree.get_selection()
        (model,pathlist) = tree_selc.get_selected_rows()
        edit_row = dict()
        count = 0
        for path in pathlist:
            count = count + 1
            # get info needed
            if count == 1:
                text_iter = model.get_iter(path)
                edit_row["title"] = model.get_value(text_iter,1) 
                edit_row["artist"] = model.get_value(text_iter,2)
                edit_row["album"] = model.get_value(text_iter,3)
                edit_row["year"] = model.get_value(text_iter,4)
                edit_row["track_num"] = model.get_value(text_iter,5)
                edit_row["genres"] = model.get_value(text_iter,6) 
                
        if count > 1:
            pass # show muitl dialog
        else:
            edit_dialog = EditDialog(self)
            edit_dialog.run()
            edit_dialog.destroy()
    def get_edit_dialog_data(self):
        """get a set of artist, album, year, track, genres for self.database\n
        resturns set as a tuple"""
        artist_set = list()
        album_set = list()
        year_set = list()
        track_set = list()
        genres_set = list()
        
        for row in self.database:
            artist_set.append(row["artist"])
            album_set.append(row["album"])
            year_set.append(row["year"])
            track_set.append(row["track_num"])
            genres_set.append(row["genres"])
        return(set(artist_set), set(album_set), set(year_set), set(track_set), set(genres_set))

    def on_row_delete(self, button):
        """Event handler for delete by row database menu item\n
        this method does not use button as you would think\n
        button does not get used when deleting rows\n
        but when it is used with deleting files\n 
        on_file_delete passes true into button to let the method call delete
        """
        # need to make func after response if 
        # then a thread is need and a timeout for update ui
        # this code can take a long time if deleting a lot of data

        dialog = QuestionDialog(self, "Are you sure?", "Do you want to delete row(s)") 
        response = dialog.run()
        if response == Gtk.ResponseType.OK: 
            tree_selc = self.tree.get_selection()
            (model,pathlist) = tree_selc.get_selected_rows()
            for path in pathlist:
                text_iter = model.get_iter(path)
                title = model.get_value(text_iter,1)
                filepath = model.get_value(text_iter,12)
                if title != " " and filepath != " ":
                    self._delete_row(title, filepath)
                    if button is not None and button == True:
                        try:
                            pathlib.Path(filepath).unlink()
                        except FileNotFoundError as fnfe:
                            print("Error")
        dialog.destroy()

    def _delete_row(self, title, filepath):
        for row in self.database:
            if title == row['title']:
                if filepath == row['file_path']:
                    self.database.remove(row)
        self.need_to_save = True
        self.mk_store()
    def on_make_db_cmd(self, button):
        """Event handler for make database menu item\n
        calls inner method __update_display_and_mkdb() and start a load dialog
        NOTE: might change the dialog with a messagebox"""
        self._update_display_and_mkdb(self._get_filepath_for_open())
        self.load_dialog = self.info_box_no_btn("Making Database. Plaese wait.")
        self.load_dialog.run()
        
    def on_delete_db(self, button):
        """Event handler for delete database menu item\n
        Deletes database file
        """
        dialog = QuestionDialog(self, "Are you sure?", "You want to delete database?")
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            self._delete_database()
        elif response == Gtk.ResponseType.CANCEL:
            print("The Cancel button was clicked")

        dialog.destroy()

    def on_file_delete(self, button):
        self.on_row_delete(True)

    def _delete_database(self):
        try:
           pathlib.Path(self.backend.db_utils.db_filepath).unlink()
           self.mk_store()
        except FileNotFoundError as file_error:
            print("Error")

    def _get_filepath_for_open(self):
        """Dispay Gtk.FileChooserDialog and get filepath\n
        return none (error) or str"""
        dialog = Gtk.FileChooserDialog(
            title="Please choose a folder",
            parent=self.window,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK
        )
        dialog.set_default_size(800, 400)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            dialog.destroy() 
            return filename
        dialog.destroy()
        return None
         
    def _update_display_and_mkdb(self, filename):
            """Starts thread to create database and starts a timeout every second """
            self.worker_thread = threading.Thread(name="db_createing_deamon", daemon=True,
                    target=self.backend.find_files, args=(filename,))
            
            self.worker_thread.start()
            GObject.timeout_add(1000,self.update_callback, self)

    def update_callback(self,s):
        """Callback for timer used to see when thread is done\n
        check is Thread is alive is so then adds a new timeout for a second or \n
        call mk_store to update UI then it destroys load dialog"""
        if self.worker_thread.is_alive():
            GObject.timeout_add(1000,self.update_callback, self) 
        else:
            self.mk_store()
            self.load_dialog.destroy() 

    def compare(model, row1, row2, user_data):
        sort_column, _ = model.get_sort_column_id()
        value1 = model.get_value(row1, sort_column)
        value2 = model.get_value(row2, sort_column)
        print(value1)
        if value1 < value2:
            return -1
        elif value1 == value2:
            return 0
        else:
            return 1

    def human_readable_size(self, size):
       return humanize.naturalsize(int(size), gnu=True)

    def human_readable_time(self, seconds):
        #TODO: need a try incase str -> float then float -> int fails
        """Helper method to change seconds into human readable time\n
        returns time str time.strftime()"""
        ty_res = time_lib.gmtime(int(float(seconds)))
        res = time_lib.strftime("%H:%M:%S", ty_res)
        return res

        self.set_default_size(250, 100)

        label = Gtk.Label(label="Database is being made.")
        box = self.get_content_area()
        box.add(label)
        
        self.show_all()
