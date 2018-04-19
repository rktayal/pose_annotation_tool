import os
import sys

class FileFeed():
    """The FileFeed class determines appropiate path to use for
    retrieving images"""

    def __init__(self, img_dir, res_dir):
        self.img_dir = img_dir
        self.res_dir = res_dir
        self.index = 0

        # Retrieves the complete list of files to be edited
        self.list_of_files = []
        self.file_names = []
        img_abs_path = os.path.abspath(self.img_dir)
        for file in os.listdir(self.img_dir):
            if file.endswith('.jpg') or file.endswith('.JPG') \
                    and (not file.startswith('.')):
                file_path = os.path.join(img_abs_path, file)
                self.file_names.append(file)
                self.list_of_files.append(file_path)

        #print self.list_of_files

    def next_file(self):
        self.index += 1
        if self.index == len(self.list_of_files) + 1:
            print "traversed through all images... Exiting"
            sys.exit(0)
            #self.index = 1
        print self.file_names[self.index - 1]
        return self.list_of_files[self.index - 1]

    def prev_file(self):
        self.index -= 1
        if self.index <= 0:
            # no file before this, so return same file
            self.index = 1
        return self.list_of_files[self.index - 1]

    def next_json_file(self):
        json_abs_path = os.path.abspath(self.res_dir)
        filename = self.file_names[self.index - 1]
        filename = filename[:-3] + 'csv'
        file =  os.path.join(json_abs_path, filename)
        return file

    def get_filename(self):
        return self.list_of_files[self.index - 1]
