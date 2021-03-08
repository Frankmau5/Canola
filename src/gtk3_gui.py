
import gi
gi.require_version("Gtk", "3.0")

from gi.repository import GObject, GLib, Gtk, Gio

class App(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='mlv.knrf.canola')
        GLib.set_application_name('canola')
        GLib.set_prgname('mlv.knrf.canola')

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_icon_name('mlv.knrf.canola')
        
        window.set_titlebar(self.mk_title_bar())
        window.add(self.mk_switch(self.mk_song_page(),
            self.mk_album_page(),
            self.mk_artist_page()
            ))
        
        window.set_default_size(1080, 720)
        window.show_all()

    def mk_title_bar(self):
        header = Gtk.HeaderBar(
            title='Canola',
            show_close_button=True)

        self.popover = Gtk.Popover()
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        
        open_btn = Gtk.ModelButton(label="Open")
        #open_btn.connect("clicked", self.on_open)

        about_btn = Gtk.ModelButton(label="About")
        #about_btn.connect("clicked", self.on_about)


        vbox.pack_start(open_btn, False, True, 5)
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
        
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Song", renderer, text=0)
        self.tree.append_column(column)

        column1 = Gtk.TreeViewColumn("Artist")
        self.tree.append_column(column1)
        
        column2 = Gtk.TreeViewColumn("Album")
        self.tree.append_column(column2)

        song = Gtk.CellRendererText()
        artist = Gtk.CellRendererText()
        album = Gtk.CellRendererText()

        column.pack_start(song, True)
        column1.pack_start(artist, True)
        column2.pack_start(album,True)
        column1.add_attribute(artist, "text", 1)
        column2.add_attribute(album, "text", 2)

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

