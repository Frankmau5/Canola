
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import GObject, GLib, Gtk, Gio
import get_media_data

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='mlv.knrf.canola')
        GLib.set_application_name('canola')
        GLib.set_prgname('mlv.knrf.canola')

    def do_activate(self):
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
        if self.backend.db_utils.db_exist() == False:
            self.info_box()
        else:
            store = self.mk_store()
            # add store to tree view 

    def info_box(self):
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

    def mk_title_bar(self):
        header = Gtk.HeaderBar(
            title='Canola',
            show_close_button=True)

        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        db_btn = Gtk.ModelButton(label="Make DB")
        db_btn.connect("clicked", self.on_make_db)

        about_btn = Gtk.ModelButton(label="About")
        #about_btn.connect("clicked", self.on_about)


        vbox.pack_start(db_btn, False, True, 5)
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
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        
        store = Gtk.ListStore()
        self.tree = Gtk.TreeView(model=store)
        
        column_path = Gtk.TreeViewColumn("File path")
        self.tree.append_column(column_path)
        
        column_type = Gtk.TreeViewColumn("File type")
        self.tree.append_column(column_type)
        
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Title", renderer, text=2)
        self.tree.append_column(column)

        column1 = Gtk.TreeViewColumn("Artist")
        self.tree.append_column(column1)
        
        column2 = Gtk.TreeViewColumn("Album")
        self.tree.append_column(column2)
        
        column3 = Gtk.TreeViewColumn("Year")
        self.tree.append_column(column3)
        
        column4 = Gtk.TreeViewColumn("Track Number")
        self.tree.append_column(column4)
        
        column5 = Gtk.TreeViewColumn("genre")
        self.tree.append_column(column5)
        
        column6 = Gtk.TreeViewColumn("Time")
        self.tree.append_column(column6)
        
        column7 = Gtk.TreeViewColumn("Channel")
        self.tree.append_column(column7)
        
        column8 = Gtk.TreeViewColumn("Bitrate")
        self.tree.append_column(column8)
        
        column9 = Gtk.TreeViewColumn("Sample rate")
        self.tree.append_column(column9)
        
        column10 = Gtk.TreeViewColumn("encoder")
        self.tree.append_column(column10)

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
        encoder = Gtk.CellRendererText()

        column_path.pack_start(_path, True)
        column_type.pack_start(_type, True)
        column.pack_start(title, True)
        column1.pack_start(artist, True)
        column2.pack_start(album,True)

        column3.pack_start(year,True)
        column4.pack_start(track_number,True)
        column5.pack_start(genres,True)
        column6.pack_start(time,True)
        column7.pack_start(channel,True)
        column8.pack_start(bitrate,True)
        column9.pack_start(sample_rate,True)
        column10.pack_start(encoder,True)


        column_path.add_attribute(_path, "text", 0)
        column_type.add_attribute(_type, "text", 1)
        column1.add_attribute(artist, "text", 3)
        column2.add_attribute(album, "text", 4)
        column3.add_attribute(year, "text", 5)
        column4.add_attribute(track_number, "text", 6)
        column5.add_attribute(genres, "text", 7)
        column6.add_attribute(time, "text", 8)
        column7.add_attribute(channel, "text", 9)
        column8.add_attribute(bitrate, "text", 10)
        column9.add_attribute(sample_rate, "text", 11)
        column10.add_attribute(encoder, "text", 12)


        scrolledwindow.add(self.tree)
        return scrolledwindow

    def mk_album_page(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        return scrolledwindow

    def mk_artist_page(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        return scrolledwindow

    def mk_store(self):
        data = self.backend.db_utils.load_json()
        store = Gtk.ListStore(str, str, str, str, str, str, str, str, str, str, str, str, str)
        print(type(data))
        for item in data:
            store.append([item["file_path"],
                    item["file_type"],
                    item["title"],
                    item["artist"],
                    item["album"],
                    item["year"],
                    item["track_num"],
                    item["genres"],
                    item["length"],
                    item["channels"],
                    item["bitrate"],
                    item["sample_rate"],
                    item["encoder"],
                    ])
        #add
        self.tree.set_model(store)

    def on_make_db(self, button):
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
            self.backend.find_files(filename)
       
        elif response == Gtk.ResponseType.CANCEL:
           dialog.destroy()

