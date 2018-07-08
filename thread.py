from Tkinter import *
import ttk
import sys
import threading
import Queue
from time import sleep
#import u3

running = False  # Global flag

class GUI:
    # ...
    def __init__(self, master):
        content = Canvas(master)
        canvas = Canvas(content, borderwidth=5, height=150, width=150, background="light gray")
        self.master = master
        self.content = content
        self.canvas = canvas
        self.canvas.pack(expand = YES, fill = BOTH)

        content.grid(column=0, row=0)
        canvas.grid(column=0, row=0, columnspan=4, rowspan=4)
        self.start_button = Button(content, text="Start", highlightbackground='light gray', command=self.start_click)
        self.stop_button = Button(content, text="Stop", highlightbackground='light gray', command=self.stop_click)
        self.start_button.grid(column=0, row=0)
        self.stop_button.grid(column=1, row=0)

    def start_click(self):
        self.start_button['state'] = 'disabled'
        global running
        running = True
        self.queue = Queue.Queue()
        ThreadedTask(self.queue).start()
        self.master.after(20, self.process_queue) # run task for 20 sec

    def stop_click(self):
        global running
        running = False
        self.start_button['state'] = 'normal'

    def process_queue(self):
        try:
            msg = self.queue.get(0)
            self.start_button['state'] = 'normal'
        except Queue.Empty:
            self.master.after(100, self.process_queue)

class ThreadedTask(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    def run(self):
        myCallback()
        self.queue.put("Task finished")

def myCallback():
    try:
        for i in range(256):
            if (running):
                print("running %s" % i)
                sleep(0.3)
            else:
                break
    except KeyboardInterrupt:
        sys.exit(0)
    print("Done")

root = Tk()
root.title("Python Threads v0.0.1")
main_ui = GUI(root)
root.mainloop()
