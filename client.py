#!/usr/bin/env python
 
import pygtk
pygtk.require("2.0")
import gtk, threading, time, dbus    
from dbus.mainloop.glib import DBusGMainLoop


class ClientApp :

    def on_window_destroy(self, widget, data=None) :
        "Called when window destroy signal emitted"

        gtk.main_quit()


    def on_button_clicked(self, button, data=None) :
        "Called when button is clicked or enter is pressed while in entry box"

        try :
            self.chat.send_message(self.colorButton.get_color().to_string(), self.entry.get_text())
            self.entry.set_text("")

        except dbus.exceptions.DBusException :
            self.set_server_unavailable()


    def on_message_received(self, color, text) :
        "When Dbus signal comes in indicating a message was received by the server"

        textbuffer = self.textView.get_buffer()

        texttag = gtk.TextTag()
        texttag.set_property("foreground", color)
        
        tagtable = textbuffer.get_tag_table()
        tagtable.add(texttag)

        textbuffer.insert_with_tags(textbuffer.get_end_iter(), text + "\n", texttag)


    def set_server_unavailable(self) :
        textbuffer = self.textView.get_buffer()

        texttag = gtk.TextTag()
        texttag.set_property("foreground", "gray")
        
        tagtable = textbuffer.get_tag_table()
        tagtable.add(texttag)

        textbuffer.insert_with_tags(textbuffer.get_end_iter(), "-- No Chat Server Available --\n", texttag)

        self.button.set_sensitive(False)


    def __init__(self) :
        "Reads glade file and sets up instance variables"

        builder = gtk.Builder()
        builder.add_from_file("client.glade")
        builder.connect_signals(self)

        self.window = builder.get_object("window")
        self.entry = builder.get_object("entry")
        self.colorButton = builder.get_object("colorbutton")
        self.textView = builder.get_object("textview")
        self.button = builder.get_object("button")

        try :
            dbus_loop = DBusGMainLoop()
            dbus.set_default_main_loop(dbus_loop)

            self.bus = dbus.SessionBus()
            self.chat_obj = self.bus.get_object("com.chat.serverbusname", "/com/chat/serverobject")
            self.chat = dbus.Interface(self.chat_obj, "com.chat.serverinterface")
            self.chat.connect_to_signal("message_received", self.on_message_received)

        except dbus.exceptions.DBusException :
            self.set_server_unavailable()            

    def main(self) :
        "Makes gui visible and enters main loop"
        self.window.show()
        gtk.main()

 
if __name__ == "__main__":
    gtk.gdk.threads_init()
    clientapp = ClientApp()
    clientapp.main()

