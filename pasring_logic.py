# st = 'assigntask desc "vrli playbook" hrs "6" to omee'
import os
import dill as pickle
import shlex
import argparse
import logging
import constants


def load_parsing_logic():
    """
    Description: Loads saved parsing logic from pickle file.
    """
    parsing = None
    # logging.debug("Loading saved parsing logic.")
    if os.path.exists(constants.PARSING_LOGIC_FILE):
        with open(constants.PARSING_LOGIC_FILE, "rb") as pickleFP:
            parsing = pickle.load(pickleFP)
    else:
        msg = "Could not load parsing logic. Pickle file missing. Creating new parsing logic"
        logging.warning(msg)
    return parsing


def create_parser():
    parser = argparse.ArgumentParser(description="blabla", formatter_class=argparse.RawTextHelpFormatter)
    sub_parser = parser.add_subparsers(dest="subparser_name")

    task_parser = sub_parser.add_parser(constants.TASK_PARSER)
    assign_task_parser = sub_parser.add_parser(constants.ASSIGN_TASK_PARSER)
    update_task_parser = sub_parser.add_parser(constants.UPDATE_TASK_PARSER)
    delete_task_parser = sub_parser.add_parser(constants.DELETE_TASK_PARSER)
    viewtables_parser = sub_parser.add_parser(constants.VIEW_TABLE_PARSER)
    create_user_parser = sub_parser.add_parser(constants.CREATE_USER_PARSER)
    get_excel_parser = sub_parser.add_parser(constants.GET_EXCEL_PARCER)
    show_tasks_parser = sub_parser.add_parser(constants.SHOW_TASKS_PARSER)

    task_parser.add_argument("--hrs")
    task_parser.add_argument("--desc")

    assign_task_parser.add_argument("--hrs")
    assign_task_parser.add_argument("--to")
    assign_task_parser.add_argument("--desc")

    update_task_parser.add_argument("--taskid")
    update_task_parser.add_argument("--percent")

    delete_task_parser.add_argument("--taskid")

    viewtables_parser.add_argument("--name")

    create_user_parser.add_argument("--name")
    create_user_parser.add_argument("--email")

    get_excel_parser.add_argument("--table")

    save_parsing_logic(parser)
    return parser


def pasrse_it(parse_string):
    """
    This is where all the parsing is done.
    :param parse_string: The command string that has tagged the bot.
                        Starting with @bot_name(name of bot may differ, take from constants
    :return: Figuring out
    """
    parser = load_parsing_logic()
    if not parser:
        parser = create_parser()

    parse_string_list = shlex.split(parse_string)
    accepted_arguements = constants.ACCEPTED_ARGS
    arguments = ['--' + arg if arg in accepted_arguements else arg for arg in parse_string_list]
    try:
        parsed_args = parser.parse_args(arguments)
        # convert to dict and return
        return vars(parsed_args)
    except SystemExit:
        msg = """
        
        I don't understand you! Please refer below commands for correct ones:
        
        
        "use quotes where you have multiple words"
        "use @chitragupt when in group chat"
        
        assigntask to "omkar" hrs 6 desc "Add a description here"  --> Will create a task with given details and assign it to omkar
        
        createuser name omkar email omkar@gmail.com --> Will create a user with given details
        
        viewtable name task_details ---> Will show task details
        
        deletetask taskid 1002 --> Means task with id 1002 will be deleted
        
        updatetask taskid 1001 percent 50 --> Means task with id 1001 is 50% complete
        
        showtasks  --> gives you all the tasks and the usernames to whom they were assigned
        """
        return msg


def save_parsing_logic(parser):
    """
    Description: Saves parsing logic to pickle file.
    """
    with open(constants.PARSING_LOGIC_FILE, "wb") as pickleFP:
        pickle.dump(parser, pickleFP)
