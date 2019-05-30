# Michael Long, Gennadii Sytov -- CS494 -- Server GUI Controller -- May 2019

from tkinter import *

class gui_controller():

    # Paramaters to control the window
    current_frame = 0 
    width = 640
    height = 480

    def __init__(self):
        self.draw_frame()
        pass
        
    def draw_frame(self):

        print("Drawing Frame")
        frame = Tk()
        frame.title = 'CS494 -- Server Application'
        frame.geometry('640x480')
        mainloop()

        # Draw Login / Connect to Host
        if self.current_frame == 0:
            pass

        # Draw Main Screen
        if self.current_frame == 1:
            pass

        