import sys
import os
from src.sims_binary_search import SimsBinarySearcher
from src.bin_search_logging import SimsLogging

inst_logger = SimsLogging("BinSearchHelper")


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
    # just to give a chance to opt-out, in case you started this accidentally
    start_question = input("Would you like to start binary searching the: {} directory?".format(my_mods_path))
    my_searcher = SimsBinarySearcher(my_mods_path, my_mods_tmp_path)
    my_searcher.move_search_forward()
    while start_question:
        print("Just moved {} files".format(len(my_searcher.get_current_set())))
        # wait for input from user on whether issue was resolved or not
        start_question = input("Did that resolve the issue?")
        if start_question.lower() == "n":
            #   if No: display top 10 potential files (can sometimes see the bad apple right off)
            print("Issue NOT resolved.  top 10 'likely' items: {}".format(my_searcher.get_top_x_from_bisected_set()))
            my_searcher.move_search_forward()
        else:
            if len(my_searcher.get_current_set()) == 1:
                #   if Yes: look at size of last set, if size == 1 you've found your culprit
                print("Found the most likely culprit: {}".format(my_searcher.get_current_set()))
            else:
                #       else: GOTO MOVE operating on current_set
                inst_logger.info("Issue RESOLVED, but set: {}, was larger than 1".format(my_searcher.get_current_set()))
                my_searcher.move_search_backward()
        my_searcher.save_current_object_state()     # keep the config files up-to-date




