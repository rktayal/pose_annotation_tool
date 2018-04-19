import os
import sys
import argparse
from Tkinter import *
from PIL import Image, ImageTk
from ttk import Frame, Style
from collections import OrderedDict

import imagefeed
import imagefilefeed

class Main(Frame):

    def __init__(self, parent, img_path, res_path):
        Frame.__init__(self, parent)
        self.parent = parent
        self.image_feed = imagefeed.ImageFeed(imagefilefeed.FileFeed(img_path, res_path))
        self.image = None
        self.canvas = None
        self.keypoints = OrderedDict()
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.rect = None
        self.initUI()
        self.resetCanvas()

    def initUI(self):

        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)

        #create canvas
        self.canvas = Canvas(self, width=500, height=500)
        self.canvas.pack()

        vcmd = (self.register(self.check_string))
        #add img height width labels
        self.add_label("IMG_WIDTH", 10, 350)
        self.img_wid = StringVar()
        self.wid = Entry(self, width=6, validate='all', validatecommand=(vcmd, '%P'), textvariable=self.img_wid, state="readonly")
        self.wid.place(x=90, y=350)

        self.add_label("IMG_HEIGHT", 10, 370)
        self.img_hei = StringVar()
        self.hei = Entry(self, width=6, textvariable=self.img_hei, state="readonly")
        self.hei.place(x=90, y=370)

        # add x, y labels
        self.add_label("start x", 160, 350)
        self.input_x = StringVar()
        self.x_entry = Entry(self, width=6, textvariable=self.input_x, state="readonly")
        self.x_entry.place(x=220, y=350)

        self.add_label("start y", 160, 370)
        self.input_y = StringVar()
        self.y_entry = Entry(self, width=6, textvariable=self.input_y, state="readonly")
        self.y_entry.place(x=220, y=370)

        # add keypoint buttons
        self.add_button("nose", 10, 400)
        self.add_button("neck", 70, 400)
        self.add_button("eye_l", 10, 430)
        self.add_button("eye_r", 70, 430)
        self.add_button("ear_l", 160, 430)
        self.add_button("ear_r", 220, 430)
        self.add_button("sho_l", 10, 460)
        self.add_button("sho_r", 70, 460)
        self.add_button("elb_l", 160, 460)
        self.add_button("elb_r", 220, 460)
        self.add_button("wri_l", 10, 490)
        self.add_button("wri_r", 70, 490)
        self.add_button("hip_l", 160, 490)
        self.add_button("hip_r", 220, 490)
        self.add_button("kne_l", 10, 520)
        self.add_button("kne_r", 70, 520)
        self.add_button("ank_l", 160, 520)
        self.add_button("ank_r", 220, 520)


        b4 = Button(self, text="show all", anchor=NW, relief=RAISED)
        b4.configure(command=lambda arg=b4:self.showAll(arg), width=5, activebackground="#33B5E5")
        b4.place(x=160, y=400)

        nextButton = Button(self, text="Save & Next", anchor=NW)
        nextButton.configure(command=lambda arg=nextButton:self.next(arg))
        nextButton.place(x=10, y=550)

        backButton = Button(self, text="prev Img", anchor=NW)
        backButton.configure(command=lambda arg=backButton:self.back(arg))
        backButton.place(x=160, y=550)

        b5 = Button(self, text="Crop & Load", anchor = NW, relief=RAISED)
        b5.configure(command=self.crop_and_load, width=8, activebackground="#33B5E5")
        b5.place(x=10, y=590)

        button = Button(self, text="Quit", command=self.quit, anchor=NW)
        button.configure(width=4, activebackground="#33B5E5", relief=RAISED)
        button.place(x=160, y=590)

        #bindings related to drawing a dot and removing it
        self.canvas.bind("<ButtonPress-1>", self.paint)
        self.canvas.tag_bind("mark", '<ButtonRelease-2>', self.remove)

        #bindings related to draw a rect
        self.canvas.bind("<ButtonPress-3>", self.on_button_press)
        self.canvas.bind("<B3-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-3>", self.on_button_release)

        #bindings related to chages in entries
        self.x_entry.bind('<Return>', self.callback)
        self.y_entry.bind('<Return>', self.callback)
        self.wid.bind('<Return>', self.callback)
        self.hei.bind('<Return>', self.callback)

        self.bind_all('<Control-Key-o>', self.new)


    def new(self, event):
        print " working"
        #print event

    def check_string(self, p):
        if str.isdigit(p) or p == '\r' or p == "":
            return True
        else:
            return False

    def reset_entries(self):
        self.input_x.set(self.start_x)
        self.input_y.set(self.start_y)
        self.img_wid.set(self.end_x - self.start_x)
        self.img_hei.set(self.end_y - self.start_y)

    def callback(self, event):
        if self.img_wid.get() == "" or self.img_hei.get() == "" \
                or self.input_x.get() == "" or self.input_y.get() == "":
            self.reset_entries()
            print "not valid numbers"
            return
        if int(self.img_wid.get()) + int(self.input_x.get()) > self.image.width():
            self.reset_entries()
            print "not valid numbers"
            return
        if int(self.img_hei.get()) + int(self.input_y.get()) > self.image.height():
            self.reset_entries()
            print "not valid numbers"
            return
        self.start_x = int(self.input_x.get())
        self.start_y = int(self.input_y.get())
        self.end_x = int(self.img_wid.get()) + self.start_x
        self.end_y = int(self.img_hei.get()) + self.start_y
        self.canvas.coords(self.rect, self.start_x, self.start_y, self.end_x, self.end_y)
        pass

    def add_label(self, text, x1, y1):
        l = Label(self, text=text)
        l.place(x=x1, y=y1)

    def add_button(self, key, x1, y1):
        b = Button(self, text=key, anchor=NW, relief=RAISED)
        b.configure(command=lambda arg=b:self.map(key,arg), width=4, activebackground="#33B5E5")
        b.place(x=x1, y=y1)

    def next(self, widget):
        """saves current and advances to next image"""
        self.clearButton(widget)
        self.image_feed.resultFile(self.keypoints)
        self.image_feed.nextImage()
        self.reset()
        #self.photo = self.image_feed.returnTkImage()
        #self.canvas.itemconfig(self.image_on_canvas, image=self.photo)

    def back(self, widget):
        """goes back to previous image"""
        #self.image_feed.resultFile(self.keypoints)
        self.clearButton(widget)
        self.image_feed.prevImage()
        self.reset()

    def resetCanvas(self):
        """Reset all canvas element without advancing forward"""
        self.image = self.image_feed.returnTkImage()
        self.canvas.create_image(0, 0, image=self.image, anchor="nw")
        self.canvas.configure(height=self.image.height(), width=self.image.width() * 2 + 20)
        self.canvas.place(x = 0, y=0, height=self.image.height(), width=self.image.width() * 2 + 20)
        self.keypoints = self.image_feed.returnKeypoints()
        self.showAll(None)

        # display another image calling draw limbs
        self.reload_canvas_image()

        self.img_wid.set(str(self.image.width()))
        self.img_hei.set(str(self.image.height()))

        self.wid.configure(state="readonly")
        self.hei.configure(state="readonly")

        self.input_x.set("")
        self.input_y.set("")

        self.x_entry.configure(state="readonly")
        self.y_entry.configure(state="readonly")
        #print self.keypoints

    def reset(self):
        """Removes all drawings on the canvas so user can start over on same image"""
        self.canvas.delete("all")
        self.rect = None
        self.resetCanvas()

    def reload_canvas_image(self):
        keypt_list = self.image_feed.returnKeypointList(self.keypoints)
        # print 'keypt_list', keypt_list
        self.image_feed.draw_limbs(keypt_list)
        out_img = self.image_feed.returnOutputImage()
        self.canvas.create_image(self.image.width()+20, 0, image=out_img, anchor="nw")

    def crop_and_load(self):
        if self.rect:
            self.image_feed.crop_and_save(self.start_x, self.start_y, self.end_x, self.end_y)
            self.reset()

    def on_button_press(self, event):
        # save the mouse drag start position
        #self.start_x = self.canvas.canvasx(event.x)
        #self.start_y = self.canvas.canvasy(event.y)
        self.start_x = event.x
        self.start_y = event.y

        # change the state of wid, height enteries
        self.wid.configure(state="normal")
        self.hei.configure(state="normal")

        # set the start_x and start_y coords
        self.input_x.set(self.start_x)
        self.input_y.set(self.start_y)

        # change the state of x, y entries
        self.x_entry.configure(state="normal")
        self.y_entry.configure(state="normal")

        # create rectange if not yet exist
        if not self.rect:
            self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='red', tag='cropped')

    def on_move_press(self, event):
        curX = self.canvas.canvasx(event.x)
        curY = self.canvas.canvasy(event.y)

        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()

        # expand the rectangle as you drag the mouse
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        self.end_x = event.x
        self.end_y = event.y

        # set the img_wid and img_hei coords
        self.img_wid.set(self.end_x - self.start_x)
        self.img_hei.set(self.end_y - self.start_y)

        # print self.start_x, self.start_y, event.x, event.y
        pass

    def paint(self, event):
        global previously_clicked
        if 'previously_clicked' in globals():
            python_green = "#476042"
            key = previously_clicked['text']
            # allow user to mark keypoint only if
            # any correponding key button is clicked
            if key in self.image_feed.part_labels:
                x1, y1 = (event.x - 1), (event.y - 1)
                x2, y2 = (event.x + 1), (event.y + 1)
                #remove the old keypoint first
                self.canvas.delete(key)
                self.canvas.create_oval(x1, y1, x2, y2, outline='yellow', width=5, tags=("mark", key))
                self.keypoints[key][0], self.keypoints[key][1], self.keypoints[key][2] = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y), 1
                self.reload_canvas_image()

    def remove(self, event):
        self.canvas.delete('current&&mark')

    def map(self, key, widget):
        # print widget
        python_green = "#476042"
        self.modifyAppearance(widget)

        for item in self.canvas.find_withtag("mark"):
            self.canvas.delete(item)
        x1, y1 = (self.keypoints[key][0] - 1), (self.keypoints[key][1] - 1)
        x2, y2 = (self.keypoints[key][0] + 1), (self.keypoints[key][1] + 1)
        self.canvas.create_oval(x1, y1, x2, y2, outline='yellow', width=5, tags=("mark", key))

    def clearButton(self, widget):
        global previously_clicked
        if 'previously_clicked' in globals():
            previously_clicked['bg'] = widget['bg']
            previously_clicked['activebackground'] = widget['activebackground']
            previously_clicked['relief'] = widget['relief']

    def modifyAppearance(self, widget):
        global previously_clicked
        if 'previously_clicked' in globals():
            previously_clicked['bg'] = widget['bg']
            previously_clicked['activebackground'] = widget['activebackground']
            previously_clicked['relief'] = widget['relief']
        widget['bg'] = 'green'
        widget['activebackground'] = '#33B5E5'
        widget['relief'] = 'sunken'
        previously_clicked = widget

    def showAll(self, widget):
        python_green = "#476042"
        if widget is not None:
            self.modifyAppearance(widget)

        # first removing remaining marks
        for item in self.canvas.find_withtag("mark"):
            self.canvas.delete(item)
        # creating the marks
        for key, value in self.keypoints.items():
            x1, y1 = (value[0] - 1), (value[1] - 1)
            x2, y2 = (value[0] + 1), (value[1] + 1)
            #print value[0], value[1]
            self.canvas.create_oval(x1, y1, x2, y2, outline='yellow', width=5, tags=("mark", key))

    def quit(self):
        print "Exiting..."
        sys.exit(-1)

def main():
    root = Tk()
    root.geometry("500x650+300+300")
    #root['bg'] = "white"
    obj = Main(root, args.img_dir, args.res_dir)
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='PROG', \
            usage='%(prog)s <images_dir_to_annotate> <result_dir_for_imgs>')
    parser.add_argument("img_dir", help="dir path for images to annotate/check")
    parser.add_argument("res_dir", help="dir path to result files(.json) for images")
    parser.add_argument("-f", "--file", help="file mode")
    args = parser.parse_args()

    if os.path.exists(args.img_dir) and os.path.exists(args.res_dir):
        #obj = Main(args.img_dir, args.res_dir)
        #print args.file
        main()
    else:
        print "invalid paths passed as argument... exiting"
        sys.exit(-1)
