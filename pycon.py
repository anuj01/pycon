#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# Copyright (C) 2010 Anuj Aggarwal<anuj01@gmail.com>
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with program; see the file COPYING. If not, write to the
# Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
# MA 02111-1307, USA."""
#
# Net4India Broadband Connector Ver 0.1
#

import pygtk
pygtk.require('2.0')
import  gtk
import sys, time, os, signal, socket
from threading import *

####################### README ################################## 
# Make this script executable using command -                   #
# $ chmod a+x pycon.py                                          #
# and run this in terminal -                                    #
# $ ./pycon.py                                                  #
# or You can edit Main Menu in panel to add this script as new  #
# item in Internet Menu. Refer your distribution's documentaion #
# for details to do this.                                       #
# See Configuraion options Section below.                       #
##################### Good Luck !!! #############################

################# Configuraion options Section ################## 
# Set here your DNS server hostname or IP and port number
dns_server = "10.24.0.2"      
port = 6699
# Set here Login Id, Password and MAC Address
# or you can specify these in GUI every time you run pycon.py
login_id = "anuj"
passwd   = "net4india"
mac_addr = "00-24-E8-81-C9-XX"
# Set this for debug messages on terminal
debug = False    # True / False
#################################################################

# Global Variables
server_response = "Init ##@@## NA ##@@## NA ##@@## NA ##@@## NA ##@@## NA"
session_info = "Init ##@@## NA ##@@## NA ##@@## NA ##@@## NA ##@@## NA"
session_id = ""
threadquit = 0
is_connected = 0

# Initilize gtk thread
gtk.gdk.threads_init()

# Function to create a connection to DNS Server
def make_connection():
	global dns_server
	global port
	if debug : print "I am in make_connection"

	for res in socket.getaddrinfo(dns_server, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
		af, socktype, proto, canonname, sa = res
		try:
			s = socket.socket(af, socktype, proto)
			s.settimeout(10)
		except socket.error, err:
			s = None
			continue
		try:
			s.connect(sa)
		except socket.error, err:
			s.close()
			s = None
			continue
		break

	return s

# Function to send the command to server
def send_command(command, from_thread):
        global server_response
	global session_info
	global is_connected
	global threadquit
	server_response = "Init ##@@## NA ##@@## NA ##@@## NA ##@@## NA ##@@## NA"
	session_info = "Init ##@@## NA ##@@## NA ##@@## NA ##@@## NA ##@@## NA"

	if debug : print "I am in send_command"
        cli_sock = make_connection()
	if not cli_sock:
		if debug : print "send_command : cound not open socket"
		if from_thread :
			threadquit = 1
			return False, "Server Unreachable"
		message(title="Network Error", type=gtk.MESSAGE_ERROR, 
				data="Could not connect to Server : " 
				+ dns_server + ":" + str(port))
		return False

	try:
        	cli_sock.send(command)
	except socket.error, err:
		cli_sock.close()
		cli_sock = None
		if debug : print "send_command : Server Error : %s" % err
		if from_thread :
			threadquit = 1
			return False, "Server Unreachable"
		message(title="Network Error", type=gtk.MESSAGE_ERROR, 
				data="Could not connect to Server : " 
				+ dns_server + ":" + str(port)
				+ "\n Error : %s" % err)
		return False

	try:
		server_response = cli_sock.recv(400)
	except socket.error, err:
		cli_sock.close()
		cli_sock = None
		if debug : print "send_command : Server Error : %s" % err
		if from_thread :
			threadquit = 1
			return False, "Server Unreachable"
		message(title="Network Error", type=gtk.MESSAGE_ERROR, 
				data="Could not connect to Server : " 
				+ dns_server + ":" + str(port)
				+ "\n Error : %s" % err)
		return False

        cli_sock.close()

	if server_response.startswith("YES") :
		if debug : print "send_command : Server response :\n" + server_response
		server_response +=  "##@@## NA ##@@## NA ##@@## NA ##@@## NA ##@@## NA"
		if is_connected :
			session_info = server_response
		if from_thread :
			return True, server_response.split("##@@##")[1]
		return True
	elif server_response.startswith("ERR") :
		if debug : print "send_command : Server response :\n" + server_response
		if from_thread :
			threadquit = 1
			return False, server_response.split("##@@##")[1]
		message(title="Server Error", type=gtk.MESSAGE_ERROR, data=server_response.split("##@@##")[1])
		return False
	else :
		if debug : print "send_command : Server response :\n" + server_response
		server_response = "##@@## \tInvalid Service at Port Number : "	+ str(port) \
					+ " \n Server Response : " + server_response
		if from_thread :
			threadquit = 1
			return False, "Invalid Port Number : " + str(port) 
		message(title="Network Error", type=gtk.MESSAGE_ERROR, data=server_response.split("##@@##")[1])
		return False

        return  server_response.startswith("YES")

def sig_quit(signum, frame):
	if debug : print "I am in sig_quit", signum
	global threadquit
	threadquit = 1
	if debug : print "Bye Quiting..."
	gtk.main_quit()

# Function to connect the internet
def netconnect(user_name,password,mac_address):
	if debug : print "I am in netconnect"
        global session_id
	global server_response
	global is_connected
	
	if is_connected:
		message(title="Connect Failed", type=gtk.MESSAGE_WARNING, data="Already Connected")
		if debug : print "netconnect : Already Connected"
		return True

        mac_auth_req = "reqType=init##@@##mac=" + mac_address + "##@@##dummy=dummy" + chr(10)

        if not send_command(mac_auth_req, False):
		if debug : print "netconnect : MAC Address request not Completed " 
                return False
        
	login_req =   "reqType=login##@@##user=" + user_name + "##@@##password=" + password +         \
                        "##@@##macAddress=" + mac_address + "##@@##version=1, 0, 0, 6##@@##dummy=dummy" + chr(10)

        if not send_command(login_req, False):
		if debug : print "netconnect : Login request not completed  " 
                return False

        session_id =  server_response.split("##@@##")[1]     
	if debug : print "netconnect : session id : " + session_id
	if debug : print "netconnect : Connection Successful!"
        return True

# Function to Disconnect from internet
def netdisconnect():
	if debug : print "I am in netdisconnect"
        global session_id
	global server_response
	global is_connected
	global session_info
	if not is_connected:
		message(title="Connect Failed", type=gtk.MESSAGE_WARNING, data="Already Disconnected")
		if debug : print "netconnect : Already Disconnected"
		return True
        logout_req = "reqType=logout##@@##sessionID=" + session_id + "##@@##dummy=dummyone" + chr(10)
	if not send_command(logout_req, False):
		if debug : print "netdisconnect : logout request not completed " 
		return False

	if debug : print "netdisconnect : " + server_response.split("##@@##")[1]
	server_response = "Init ##@@## NA ##@@## NA ##@@## NA ##@@## NA ##@@## NA"
	session_info = "Init ##@@## NA ##@@## NA ##@@## NA ##@@## NA ##@@## NA"
        return True

# Refersh Thread
class refresh(Thread):

	def __init__(self, class_NetConnect_obj, widget, ctx_id, count):
		Thread.__init__(self)
		self.count = count
		self.nc = class_NetConnect_obj
		self.widget = widget
		self.ctx_id = ctx_id
	
	def run(self):
		global threadquit
		global is_connected
		global session_id
		refresh_str = "reqType=refresh##@@##sessionID=" + session_id + "##@@##dummy=dummyone" + chr(10)
		while not threadquit:
			if debug : 
				print "I am in refresh thread", self.count
				self.count = self.count+1

			self.nc.icon.set_blinking(False)
			time.sleep(15)

			res_list =  send_command(refresh_str, True)
			if not res_list[0]:
				if debug : print "thread : Couldn't refresh. Server Message is " + res_list[1]
				is_connected = 0
				gtk.gdk.threads_enter()
				self.nc.push_status(self.widget, self.ctx_id, "Status : Offline - " + res_list[1])
				gtk.gdk.threads_leave()

			conn_status = ("Offline", "Online")[is_connected]

			self.nc.icon.set_tooltip("Net4India - " + conn_status 
					+ "\n Inbound : " + session_info.split("##@@##")[4]
					+ "\n Outbound: " + session_info.split("##@@##")[5] )
			self.nc.icon.set_blinking(True)
			time.sleep(3)

		self.nc.icon.set_blinking(False)
		threadquit = 0
		is_connected = 0
		session_id = ""
		if debug : print "refresh thread : Thread Quit !!! " 
		return 

# Function to show a Dialog Message
def message(title=None, type=gtk.MESSAGE_INFO, buttons=gtk.BUTTONS_OK, data=None):
	msg = gtk.MessageDialog(None, gtk.DIALOG_MODAL, type, buttons, data)
	msg.set_title(title)
	response = msg.run()
	msg.destroy()
	return response

# Function to show the status of connection
def show_status(data=None):
	global session_info
	global is_connected
	if debug : print "I am in show_status" 
	if debug : print "show_status :\n" + session_info 
	conn_status = ("Offline", "Online")[is_connected]
	message(title="Session Info", data="\nStatus\t\t:\t" + conn_status 		
			+ "\nLogin Time\t:\t" + session_info.split("##@@##")[2] 
			+ "\nInbound Data\t:\t" + session_info.split("##@@##")[4]  
			+ "\nOutbound Data\t:\t" + session_info.split("##@@##")[5])
	return

# Function invoked for options in popup menu  
def menu_callback(data=None):
	global threadquit
	if data == "about":
		authors = [ "Anuj  Aggarwal <anuj01@gmail.com>" ]
		documenters = [ "Anuj  Aggarwal <anuj01@gmail.com>" ]
		license = """Copyright (C) 2010 Anuj Aggarwal<anuj01@gmail.com>

This is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2, or (at your option)
any later version.

This software is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with program; see the file COPYING. If not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston,
MA 02111-1307, USA."""
		dialog = gtk.AboutDialog()
		dialog.set_name("Connector")
		dialog.set_version("0.1")
		dialog.set_comments("Net4India Connector")
		dialog.set_copyright(u"Copyright © 2010 Anuj Aggarwal")
		dialog.set_website("http://anuj01.limewebs.com")
		dialog.set_authors(authors)
		dialog.set_documenters(documenters)
		dialog.set_license(license)
		dialog.run()
		dialog.destroy()

	if data == "status":
		show_status(None)

	if data == "close":
		response = message("Quit Connector", gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, "Are you Sure?")
		if response == gtk.RESPONSE_YES:
			if is_connected:
				netdisconnect()
			threadquit = 1
			if debug : print "Bye Quiting..."
			gtk.main_quit()
		
	return 	

# Function to create right click popup menu on staus icon
def make_right_menu(self, event_button, event_time):

	agr = gtk.AccelGroup()
	self.window.add_accel_group(agr)
	menu = gtk.Menu()

	status_item = gtk.ImageMenuItem(gtk.STOCK_INFO, agr)
	about_item = gtk.ImageMenuItem(gtk.STOCK_ABOUT, agr)
	close_item = gtk.ImageMenuItem(gtk.STOCK_QUIT, agr)


	menu.append(status_item)
	menu.append(about_item)
	menu.append(close_item)

	status_item.connect_object("activate", menu_callback , "status")
	about_item.connect_object("activate", menu_callback , "about")
	close_item.connect_object("activate", menu_callback, "close")

	status_item.show()
	about_item.show()
	close_item.show()

	menu.popup(None, None, None, event_button, event_time)
	return

# Class defined to create all widgets and events handling
class NetConnect:

# Function to push staus message on status bar
   def push_status(self, widget, ctx_id, msg):
	   self.status_bar.push(ctx_id, msg)
	   return

# Function to pop status message from status bar ( not used )
   def pop_item(self, widget, ctx_id):
	   self.status_bar.pop(ctx_id)
	   return

# Callback for Right click event on statusicon
   def on_right_click(self, data, event_button, event_time):
	   if debug : print "I am in right click"
	   make_right_menu(self, event_button, event_time)
	   return

# Callback for Left click event on statusicon
   def on_left_click(self, event):
	   if debug : print "I am in left click"
	   self.window.show()
	   return

# Callback for Connect button
   def connect(self, widget, ctx_id, data):
	   if debug : print "Connect Clicked!"
           global is_connected
	   global threadquit
           user_name = self.uentry.get_text()
           password = self.pentry.get_text()
           mac_address = self.mentry.get_text()
	   if netconnect(user_name,password,mac_address):
		   self.push_status(widget, ctx_id, "Status : Online")
		   is_connected = 1
		   threadquit = 0
		   ref_thread = refresh(self, widget, ctx_id, 1)
		   ref_thread.start() 
           else:
		   self.push_status(widget, ctx_id, "Status : Error in Connection")
           
	   conn_status = ("Offline", "Online")[is_connected]
	   self.icon.set_tooltip("Net4India - " + conn_status 
			   + "\n Inbound : " + session_info.split("##@@##")[4]
			   + "\n Outbound: " + session_info.split("##@@##")[5] )
	   return

# Callback for Disconnect button
   def disconnect(self, widget, ctx_id, data):
	   if debug : print "Disconnect Clicked"
	   global threadquit
	   global session_id 
	   global is_connected
	   if netdisconnect():
		   is_connected = 0
		   session_id = ""
		   self.push_status(widget, ctx_id, "Status : Offline")
	   else:
		   self.push_status(widget, ctx_id, "Status : Error in Disconnection")
	   
           conn_status = ("Offline", "Online")[is_connected]
	   self.icon.set_tooltip("Net4India - " + conn_status 
			   + "\n Inbound : " + session_info.split("##@@##")[4]
			   + "\n Outbound: " + session_info.split("##@@##")[5] )
	   threadquit = 1
	   return

# Callback for window destroy event
   def on_delete_event(self, widget, event):
	   if debug : print "Delete Clicked"
	   self.window.hide()
	   return True

# Constructor for NetConnect class
   def __init__(self):
      global login_id
      global passwd
      global mac_addr
      self.count = 1
# Create a new window
      self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
      self.window.set_size_request(250, 150)
      self.window.set_title("Net4India  Connector")
      self.window.set_border_width(5)
      self.window.connect("delete_event", self.on_delete_event) 

# Create Stausbar
      self.status_bar = gtk.Statusbar()
      context_id = self.status_bar.get_context_id("Connector")

# Create Vertical Box
      vbox = gtk.VBox(False, 0)
      self.window.add(vbox)
      vbox.show()

# User name text entry
      uhbox = gtk.HBox(False,1)
      vbox.pack_start(uhbox, True, True, 0)
      uhbox.show()

      ulabel = gtk.Label("Login ID :")
      uhbox.pack_start(ulabel, True, True, 0)
      ulabel.show()

      self.uentry = gtk.Entry(0)
      self.uentry.set_text(login_id)
      self.uentry.set_tooltip_text("Enter user name")
      uhbox.pack_start(self.uentry, False, True, 0)
      self.uentry.show()

# Password text entry
      phbox = gtk.HBox(False,1)
      vbox.pack_start(phbox, True, True, 0)
      phbox.show()

      plabel = gtk.Label("Password :")
      phbox.pack_start(plabel, True, True, 0)
      plabel.show()

      self.pentry = gtk.Entry(0)
      self.pentry.set_visibility(False)
      self.pentry.set_text(passwd)
      self.pentry.set_tooltip_text("Enter password")
      phbox.pack_start(self.pentry, False, True, 0)
      self.pentry.show()

# MAC Address text entry
      mhbox = gtk.HBox(False,1)
      vbox.pack_start(mhbox, True, True, 0)
      mhbox.show()

      mlabel = gtk.Label("MAC :")
      mhbox.pack_start(mlabel, True, True, 0)
      mlabel.show()


      self.mentry = gtk.Entry(0)
      self.mentry.set_text(mac_addr)
      self.mentry.set_tooltip_text("Enter MAC address")
      mhbox.pack_start(self.mentry, False, True, 0)
      self.mentry.show()

      bhbox = gtk.HBox(False,1)
      vbox.pack_start(bhbox, True, True, 0)
      bhbox.show()

# Connect button
      button = gtk.Button(None)
      cbhbox = gtk.HBox(False,0)
      button.add(cbhbox)
      cbhbox.show()
      s = gtk.Style()
      icon = s.lookup_icon_set(gtk.STOCK_CONNECT).render_icon(
		      s, gtk.TEXT_DIR_LTR, gtk.STATE_NORMAL, gtk.ICON_SIZE_BUTTON,
		      cbhbox, None)
      img = gtk.Image()
      img.set_from_pixbuf(icon)
      cbhbox.add(img)
      img.show()
      label = gtk.Label("_Connect")
      label.set_use_underline(True)
      cbhbox.add(label)
      label.show()
      button.connect("clicked", self.connect, context_id, None)
      bhbox.pack_start(button, True, True, 2)
      button.show()

# Disconnect Button
      button = gtk.Button(label=None)
      dbhbox = gtk.HBox(False,0)
      button.add(dbhbox)
      dbhbox.show()
      s = gtk.Style()
      icon = s.lookup_icon_set(gtk.STOCK_DISCONNECT).render_icon(
		      s, gtk.TEXT_DIR_LTR, gtk.STATE_NORMAL, gtk.ICON_SIZE_BUTTON,
		      dbhbox, None)
      img = gtk.Image()
      img.set_from_pixbuf(icon)
      dbhbox.add(img)
      img.show()
      label = gtk.Label("_Disconnect")
      label.set_use_underline(True)
      dbhbox.add(label)
      label.show()
      button.connect("clicked", self.disconnect, context_id, None)
      bhbox.pack_start(button, True, True, 2)
      button.show()

#  Show Statusbar
      vbox.pack_start(self.status_bar, True, True, 0)
      self.status_bar.show()

# Statusicon in notification area
      self.icon = gtk.status_icon_new_from_stock(gtk.STOCK_NETWORK)
      self.icon.set_tooltip("Net4India Connector")
      self.icon.connect("popup-menu",self.on_right_click)
      self.icon.connect("activate",self.on_left_click)

# Always display the window as the last step so it all splashes on
# the screen at once.
      self.window.show()

# Main Function (event loop)
def main():
    gtk.gdk.threads_enter()
    gtk.main()
    gtk.gdk.threads_leave()
    return 0

# Program starts from here
if __name__ == "__main__":
    nc = NetConnect()
    signal.signal(signal.SIGINT,sig_quit)
    main()

