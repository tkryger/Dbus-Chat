#!/usr/bin/env python
 
import pygtk
pygtk.require("2.0")
import gtk, threading, time, dbus    

import dbus.service
from dbus.mainloop.glib import DBusGMainLoop



class ServerApp(dbus.service.Object) :

    def on_window_destroy(self, widget, data=None) :
        "Called when window destroy signal emitted"

        gtk.main_quit()

    @dbus.service.method(dbus_interface='com.chat.serverinterface', in_signature='ss', out_signature='')
    def send_message(self, color, text) :
        "Called when button is clicked or enter is pressed while in entry box"

        #Push message out to all listening clients
        self.message_received(color, text)
        
        #Update local record of messages
        textbuffer = self.textView.get_buffer()

        texttag = gtk.TextTag()
        texttag.set_property("foreground", color)
        
        tagtable = textbuffer.get_tag_table()
        tagtable.add(texttag)

        textbuffer.insert_with_tags(textbuffer.get_end_iter(), text + "\n", texttag)
        


    @dbus.service.signal(dbus_interface='com.chat.serverinterface',signature='ss')
    def message_received(self, color, text):
        pass



    def __init__(self) :
        "Reads glade file and sets up instance variables"

        dbus_loop = DBusGMainLoop()
        dbus.set_default_main_loop(dbus_loop)

        bus_name = dbus.service.BusName('com.chat.serverbusname',bus=dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, "/com/chat/serverobject")

        builder = gtk.Builder()
        builder.add_from_file("server.glade")
        builder.connect_signals(self)

        self.window = builder.get_object("window")
        self.textView = builder.get_object("textview")


    def main(self) :
        "Makes gui visible and enters main loop"
        self.window.show()
        gtk.main()
 
if __name__ == "__main__":
    gtk.gdk.threads_init()
    serverapp = ServerApp()
    serverapp.main()

