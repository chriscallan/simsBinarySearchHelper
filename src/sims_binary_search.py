import json
import os
from shutil import move
from src.bin_search_logging import SimsLogging

config_location = "config/sims_bin_search.cfg"

inst_logger = SimsLogging("SimBinSearcher")


class SimsBinarySearcher:
    def __init__(self, in_mods_dir, in_tmp_dir):
        self.file_tracker = dict()
        if os.path.exists(config_location):
            my_response = input("Previous config found.  Would you like to load it?")
            if my_response.lower() == "y":
                with open(config_location, "r") as pre_config_file:
                    existing_config = json.load(pre_config_file)
                    self.file_tracker["mods_dir"] = existing_config["mods_dir"]
                    self.file_tracker["mods_tmp"] = existing_config["mods_tmp"]
                    self.file_tracker["original_files"] = existing_config["original_files"]
                    self.file_tracker["current_set"] = existing_config["current_set"]
                    self.file_tracker["bisected_set"] = existing_config["bisected_set"]
                    self.file_tracker["previous_sets"] = existing_config["previous_sets"]
                    inst_logger.info("Loaded the configuration: \n".format(self.file_tracker))
                    return      # after loading this up, there's nothing else to do
            else:
                bak_idx = len([x for x in os.listdir("config") if "bak" in os.path.splitext(x)[-1]])
                move(config_location, config_location + ".bak" + str(bak_idx))
                inst_logger.debug("Moved: {}, to: {}".format(config_location, config_location + ".bak" + str(bak_idx)))
        self.initialize_default_structures(in_mods_dir, in_tmp_dir)

    def __del__(self):
        inst_logger.info("Saving configuration before destroying the object: {}".format(json.dumps(self.file_tracker)))
        self.save_current_object_state()

    def initialize_default_structures(self, in_mods_dir, in_tmp_dir):
        self.file_tracker["mods_dir"] = in_mods_dir
        self.file_tracker["mods_tmp"] = in_tmp_dir
        self.file_tracker["original_files"] = []  # starting list of files
        self.file_tracker["current_set"] = []  # set that we're currently operating on
        self.file_tracker["bisected_set"] = []  # other half of the 'current_set'
        self.file_tracker["previous_sets"] = dict()  # listing of previous sets
        inst_logger.debug("Created a new data storage structure pointing to: {} & {}"
                          .format(self.file_tracker["mods_dir"], self.file_tracker["mods_tmp"]))

    def save_current_object_state(self):
        try:
            with open(config_location, "w+") as config_file:
                json.dump(self.file_tracker, config_file)
        except Exception as exc:
            raise Exception("Exception occurred saving config file: {}".format(exc))

    def _process_directory(self, from_dir, to_dir):
        inst_logger.debug("called _process_directory() with: {}".format("\n".join(from_dir)))
        self._move_half_to(from_dir, to_dir)
        #   note moved files in previous_sets.<runNumber> element (list of file paths)
        prev_set_idx = self._get_next_previous_set_id()
        self.file_tracker["previous_sets"][prev_set_idx] = self.file_tracker["current_set"]
        return self.file_tracker["current_set"], self.file_tracker["bisected_set"]

    def move_search_forward(self):
        """
        Helper method to move files from the mods dir to the tmp dir
        Calling this method infers that the issue still exists and we need to eliminate more 'mods' files
            This will operate on the 'current_set'
        :return: two lists: current_set & bisected_set
        """
        inst_logger.info("move_search_forward, from: {}, to: {}".format(self.file_tracker["bisected_set"],
                                                                        self.file_tracker["mods_tmp"]))
        if len(self.file_tracker["current_set"]) == 0:
            self.file_tracker["current_set"] = self.get_all_files_in_dir(self.file_tracker["mods_dir"])
        self._process_directory(self.file_tracker["current_set"], self.file_tracker["mods_tmp"])
        return self.file_tracker["current_set"], self.file_tracker["bisected_set"]

    def move_search_backward(self):
        """
        Helper method to move files from the mods_tmp to the mods dir
        Calling this method infers that the issue no longer exists and we're trying to narrow down the culprit
            This will operate on the 'bisected_set'
        :return: two lists: current_set & bisected_set
        """
        if len(self.file_tracker["bisected_set"]) == 0:
            self._set_current_and_bisected_lists()
        self._process_directory(self.file_tracker["bisected_set"], self.file_tracker["mods_dir"])
        return self.file_tracker["current_set"], self.file_tracker["bisected_set"]

    def _set_current_and_bisected_lists(self):
        tmp_list = self.get_all_files_in_dir(self.file_tracker["mods_dir"])
        midway_idx = len(tmp_list) // 2
        self.file_tracker["current_set"] = tmp_list[0:midway_idx]
        self.file_tracker["bisected_set"] = tmp_list[midway_idx:]

    def _move_half_to(self, in_file_list, move_dest):
        """
        Helper method to move half of the in_file_list to move_dest
        :param in_file_list: list of absolute file paths
        :param move_dest: directory to move things to
        :return: n/a
        """
        midway_idx = len(in_file_list) // 2
        self.file_tracker["current_set"] = in_file_list[midway_idx:]
        self.file_tracker["bisected_set"] = in_file_list[0:midway_idx]
        # MOVE: move half of mods_dir to mods_tmp
        for current_file in self.file_tracker["current_set"]:
            move(current_file, move_dest)
            inst_logger.info("Moved: {}".format(current_file))

    def get_all_files_in_dir(self, in_path):
        for tmp_path, tmp_dirs, tmp_files in os.walk(in_path):
            return [os.path.join(tmp_path, x) for x in tmp_files]

    def get_current_set(self):
        return self.file_tracker["current_set"]

    def get_top_x_from_current_set(self, num=10):
        return self.file_tracker["current_set"][:num]

    def get_bisected_set(self):
        return self.file_tracker["bisected_set"]

    def get_top_x_from_bisected_set(self, num=10):
        return self.file_tracker["bisected_set"][:num]

    def get_most_recent_previous_set(self):
        self._get_next_previous_set_idx()
        return self.file_tracker["previous_set"][self._get_last_previous_set_idx()]

    def _get_next_previous_set_id(self):
        return max(self.file_tracker["previous_sets"].keys(), default=0) + 1

    def _get_last_previous_set_id(self):
        return max(self.file_tracker["previous_sets"].keys(), default=0)
