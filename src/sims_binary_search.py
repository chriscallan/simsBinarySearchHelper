import os
from src.bin_search_logging import SimsLogging




inst_logger = SimsLogging()

class SimsBinarySearcher():
    def __init__(self, in_mods_dir, in_tmp_dir):
        self.mods_dir = in_mods_dir
        self.mods_tmp_dir = in_tmp_dir
        self.file_tracker = dict()
        self.file_tracker["original_files"] = []
        self.file_tracker["current_set"] = []
        self.file_tracker["previous_sets"] = dict()

    def process_directory(self, mods_dir, mods_tmp):
        pass
        # get list of all files
        all_files = self.get_all_files_in_dir(mods_dir)
        # MOVE: move half of mods_dir to mods_tmp
        #   note move direction in previous_sets.<direction> element
        #   note moved files in previous_sets.<runNumber> element (list of file paths)
        # wait for input from user on whether issue was resolved or not
        #   if No: display top 10 potential files (can sometimes see the bad apple right off)
        # GOTO MOVE
        #   if Yes: look at size of last set, if size == 1 you've found your culprit
        #       else: GOTO MOVE operating on present_sert

    def get_all_files_in_dir(self, in_path):
        for tmp_path, tmp_dirs, tmp_files in os.walk(in_path):
            return [os.path.join(tmp_path, x) for x in tmp_files]

    def move_half_to(self, in_path, destination="mods"):
        """

        :param in_path:
        :param destination:
        :return:
        """

