# -*- coding: utf-8 -*-
import os
import glob
import unittest
from CreateTagFiles import TagFiles

# The Path is input via the Tk.Entry widget.
# So don't worry the input string might look like "c:\tmp",
# the input string will always be r"c:\tmp" (i.e. "c:\\tmp")
DIR_NORMAL = r"C:\tmp01"
DIR_CHINESE = r"F:\迅雷下载"
DIR_NOT_EXIST = r"C:\not_exist"
DIR_TAILING_SLASH = "C:\\tmp02\\"
DIR_LIST = [DIR_NORMAL, DIR_CHINESE, DIR_TAILING_SLASH]

TAG_LIST_NORMAL = ["classic", "wagner", "karajan"]
TAG_LIST_CHINESE = ["classic", r"古典", "wagner",
                    r"瓦格纳"]
TAG_LIST_ONE_STRING = "classic"
TAG_LIST_BAD_FILENAME = [r"R/B", r"R\B", r"R:B", r"R*B", r"R?B",
                         "R\"B", r"R>B", r"R<B", r"R|B"]


class TagFilesTest(unittest.TestCase):
    def setUp(self):
        for directory in DIR_LIST:
            os.chdir(directory.decode("utf-8"))
            for existing_tag_file in glob.glob("*.tag"):
                os.rename(existing_tag_file, existing_tag_file+".bak4ut")

    def tearDown(self):
        for directory in DIR_LIST:
            os.chdir(directory.decode("utf-8"))
            for tag_file in glob.glob("*.tag"):
                os.remove(tag_file)
            for old_tag_file in glob.glob("*.bak4ut"):
                os.rename(old_tag_file, old_tag_file[:-7])

    def exec_test_case(self, directory, tag_list):
        tf = TagFiles(directory, tag_list)
        tf.create_tag_files()
        os.chdir(directory.decode("utf-8"))
        for tag in tag_list:
            self.assertTrue(os.path.isfile(tag.decode("utf-8") + ".tag"))

    def test_normal_dir_normal_tags(self):
        self.exec_test_case(DIR_NORMAL, TAG_LIST_NORMAL)

    def test_tailing_dir_chinese_tags(self):
        self.exec_test_case(DIR_TAILING_SLASH, TAG_LIST_CHINESE)

    def test_chiness_dir_chinese_tags(self):
        self.exec_test_case(DIR_CHINESE, TAG_LIST_CHINESE)

    def test_normal_dir_bad_tags(self):
        tf = TagFiles(DIR_NORMAL, TAG_LIST_BAD_FILENAME)
        tf.create_tag_files()
        os.chdir(DIR_NORMAL.decode("utf-8"))
        self.assertEqual(glob.glob("*.tag"), [])

if __name__ == '__main__':
    unittest.main()
