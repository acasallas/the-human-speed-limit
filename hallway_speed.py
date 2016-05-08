#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode Tkinter tutorial

In this script, we use the pack manager
to create a more complex layout.

Author: Jan Bodnar
Last modified: December 2015
Website: www.zetcode.com
"""

from Tkinter import *
from ttk import Frame, Label, Entry
import Tkinter
import time
import threading
import random
import Queue


class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        self.initUI()

        
    def initUI(self):
      
        self.parent.title("Review")
        self.pack(fill=BOTH, expand=True)
        
        frame1 = Frame(self)
        frame1.pack(fill=X)
        
        lbl1 = Label(frame1, text="Your Speed Is:", width=18, font=("Helvetica", 16))
        lbl1.pack(padx=5, pady=5)           
        
        frame2 = Frame(self)
        frame2.pack(fill=X)
        
        mph = Label(frame2, text="MPH", width=6, font=("Helvetica", 20))
        mph.pack(side=RIGHT, padx=5, pady=5)        

        self.speed_text = StringVar()
        speed_label = Label(frame2, textvariable = self.speed_text, width = 18, font=("Helvetica", 60))
        speed_label.pack(fill=X, padx=5, expand=True)
        
        frame3 = Frame(self)
        frame3.pack(fill=BOTH, expand=True)

        self.v = StringVar()
        self.v.set("Late For Class?")
        self.speed = Label(frame3, textvariable=self.v, width=16, font=("Helvetica", 40))
        self.speed.pack(padx=5, pady=5)

    def updateMetrics(self,speed,message):
        formatted_speed = "{0:.2f}".format(speed)
        self.speed_text.set(formatted_speed)
        print str("{0:.2f}".format(speed))

class GuiPart:
    def __init__(self, master, queue, endCommand):
        self.queue = queue
        # Set up the GUI
        self.gui = Example(master)
        
        #console = Tkinter.Button(master, text='Done', command=endCommand)
        #console.pack()
        # Add more GUI stuff here

    def processIncoming(self):
        """
        Handle all the messages currently in the queue (if any).
        """
        while self.queue.qsize():
            try:
                msg = self.queue.get(0)
                # Check contents of message and do what it says
                # As a test, we simply print it
                self.gui.updateMetrics(msg,"Late For Class?")
            except Queue.Empty:
                pass

class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """
    def __init__(self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI. We spawn a new thread for the worker.
        """
        self.master = master

        # Create the queue
        self.queue = Queue.Queue()

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More can be made if necessary
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        """
        Check every 100 ms if there is something new in the queue.
        """
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(100, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select()'.
        One important thing to remember is that the thread has to yield
        control.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following 2 lines with the real
            # thing.
            time.sleep(rand.random() * 0.3)
            msg = rand.random()
            self.queue.put(msg)

    def endApplication(self):
        self.running = 0

rand = random.Random()
root = Tkinter.Tk()

client = ThreadedClient(root)
root.mainloop()
