import os
import cv2
import json
import scipy.misc
import numpy as np
import Image, ImageTk
from collections import OrderedDict

class ImageFeed:
    """The ImageFeed class manages all operations related to loading,
    formatting images for presentation. The ImageFeed has a member file
    manager that determines what files it loads. The ImageFeed supplies
    a TkinterImage to requester objects"""

    def __init__(self, file_feed):
        self.part_labels = ['nose', 'neck', 'sho_r', 'elb_r', 'wri_r',
                'sho_l', 'elb_l', 'wri_l', 'hip_r', 'kne_r', 'ank_r',
                'hip_l', 'kne_l', 'ank_l', 'eye_r', 'eye_l', 'ear_r',
                'ear_l']
        self.part_idx = {b:a for a, b in enumerate(self.part_labels)}
        self.file_feed = file_feed
        self.image = None
        self.width = self.height = None
        self.photo = None
        self.nextImage()
        open("files_modified.txt", 'w').close()

    def PIL2array(self, img):
        return np.array(img.getdata(),
        np.uint8).reshape(img.size[1], img.size[0], 3)

    def array2PIL(self, arr, size):
        mode = 'RGBA'
        arr = arr.reshape(arr.shape[0]*arr.shape[1], arr.shape[2])
        if len(arr[0]) == 3:
            arr = np.c_[arr, 255*np.ones((len(arr),1), np.uint8)]
            return Image.frombuffer(mode, size, arr.tostring(), 'raw', mode, 0, 1)

    def returnTkImage(self):
        return self.photo

    def returnKeypoints(self):
        return self.keypoints

    def returnOutputImage(self):
        pil_img = self.array2PIL(self.output, self.image.size)
        self.out_photo = ImageTk.PhotoImage(pil_img)
        return self.out_photo

    def setParams(self):
        self.image = Image.open(self.img_name)
        self.image = self.image.resize((128, 256), Image.ANTIALIAS)
        self.width, self.height = self.image.size
        self.photo = ImageTk.PhotoImage(self.image)
        self.getKeypoints()

    def prevImage(self):
        """Call's teh file feed's method to advance in the
        file list and then loads and formats the next image
        file"""
        self.img_name = self.file_feed.prev_file()
        self.setParams()

    def nextImage(self):
        """ Call's the file feed's method to advance in the
        file list and then loads and formates the next image
        file"""
        self.img_name = self.file_feed.next_file()
        self.setParams()

        ## draw limbs
        #self.output = scipy.misc.imread(self.img_name, mode='RGB')
        #self.output = cv2.resize(self.output, (128,256), interpolation=cv2.INTER_CUBIC)

    def getKeypoints(self):
        """Call's the file feed's method to get json file
        to be read"""
        self.keypoints = OrderedDict()
        self.file = self.file_feed.next_json_file()
        if not os.path.exists(self.file):
            # create an empty dictionary for keypoints
            self.initKeypoints()
            return
        with open(self.file) as f:
            data = f.readlines()
        #print "data[0].split(',') =>", data[0].split(',')
        keypt_list = map(float, data[0].split(','))
        for i, key in enumerate(self.part_labels):
            self.keypoints[key] = [keypt_list[i*3] * self.width , keypt_list[i*3+1] * self.height, keypt_list[i*3 + 2]]

    def resultFile(self, keypt_dict):
        f = open(self.file, 'w')
        keypt_list = []
        #print "keypt_dict", keypt_dict
        for key, values in keypt_dict.items():
            values[0] = values[0]/self.width
            values[1] = values[1]/self.height
            val = map(str, values)
            keypt_list += val

        #print keypt_list
        f.write(' ,'.join(keypt_list))
        f.close()

    def returnKeypointList(self, keypt_dict):
        keypt_list = []
        for key, values in keypt_dict.items():
            keypt_list += values
        return keypt_list

    def crop_and_save(self, x1, y1, x2, y2):
        img = self.image.crop((x1, y1, x2, y2))
        filename = self.file_feed.get_filename()
        print 'filename', filename
        img.save(filename)
        self.image = Image.open(filename)
        self.image = self.image.resize((128,256), Image.ANTIALIAS)
        self.width, self.height = self.image.size
        self.img_name = filename
        #self.output = self.image
        self.photo=ImageTk.PhotoImage(self.image)
        self.initKeypoints()
        with open("files_modified.txt", "a") as f:
            f.write(filename+'\n')

    def initKeypoints(self):
        for i, key in enumerate(self.part_labels):
            self.keypoints[key] = [0, 0, 0]

    def draw_limbs(self, pred):
        def link(a, b, color):
            if part_idx[a] < pred.shape[0] and part_idx[b] < pred.shape[0]:
                a = pred[part_idx[a]]
                b = pred[part_idx[b]]
                if a[2]>0.07 and b[2]>0.07:
                    cv2.line(self.output, (int(a[0]), int(a[1])), (int(b[0]), int(b[1])), color, 6)

        #self.paint_img = self.output
        self.output = scipy.misc.imread(self.img_name, mode='RGB')
        self.output = cv2.resize(self.output, (128,256), interpolation=cv2.INTER_CUBIC)
        # check if pred is list of zeros
        if not any(pred):
            return
        part_idx = {b:a for a, b in enumerate(self.part_labels)}
        pred = np.array(pred).reshape(-1, 3)
        bbox = pred[pred[:,2]>0]
        #print 'bbox',bbox
        #print 'bbox[:,0]', bbox[:,0]
        a, b, c, d = bbox[:,0].min(), bbox[:,1].min(), bbox[:,0].max(), bbox[:,1].max()

        #cv2.rectangle(inp, (int(a), int(b)), (int(c), int(d)), (255, 255, 255), 2)

        link('nose', 'eye_l', (255, 0, 0))
        link('eye_l', 'eye_r', (255, 0, 0))
        link('eye_r', 'nose', (255, 0, 0))

        link('eye_l', 'ear_l', (255, 0, 0))
        link('eye_r', 'ear_r', (255, 0, 0))

        link('ear_l', 'sho_l', (255, 0, 0))
        link('ear_r', 'sho_r', (255, 0, 0))
        link('sho_l', 'sho_r', (255, 0, 0))
        link('sho_l', 'hip_l', (0, 255, 0))
        link('sho_r', 'hip_r', (0, 255, 0))
        link('hip_l', 'hip_r', (0, 255, 0))

        link('sho_l', 'elb_l', (0, 0, 255))
        link('elb_l', 'wri_l', (0, 0, 255))

        link('sho_r', 'elb_r', (0, 0, 255))
        link('elb_r', 'wri_r', (0, 0, 255))

        link('hip_l', 'kne_l', (255, 255, 0))
        link('kne_l', 'ank_l', (255, 255, 0))

        link('hip_r', 'kne_r', (255, 255, 0))
        link('kne_r', 'ank_r', (255, 255, 0))

