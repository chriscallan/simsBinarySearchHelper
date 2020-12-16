import sys
import os
from src.bin_search_logging import SimsLogging

inst_logger = SimsLogging()


def extract_input_args():
    """
    Simple method to pull off the base/output path input arguments and return them to the caller
    :return:mods and mods_backup locations
    """
    if len(sys.argv) != 3:
        for item in sys.argv:
            # print("input argument is: {}".format(item))
            inst_logger.info("input argument is: {}".format(item))
        raise Exception("Script requires the base_path & put input argument")
    mods_path = sys.argv[1]
    mods_tmp_path = sys.argv[2]
    if not os.path.exists(mods_path):
        raise Exception("mods_path provided is non-extant, your install must be somewhere else")
    if not os.path.exists(mods_tmp_path):
        inst_logger.info("mods_tmp_path didn't exist, creating it now")
        os.mkdir(mods_tmp_path)
    return mods_path, mods_tmp_path


if __name__ == '__main__':
    my_mods_path, my_mods_tmp_path = extract_input_args()

