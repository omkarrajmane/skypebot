import os
import datetime
import logging
from prettytable import PrettyTable
import skype_bot_utils
import db_ops as dbops
import database_setup as db_setup
import constants
import excel_utils
import aws_utils


class TaskExecution(object):
    """
    This is where all the tasks that are extracted from parsing logic are executed in backend
    task
    """

    def __init__(self):
        self.dbo = dbops.DatabaseOperations()
        self.excel_utils = excel_utils.ExcelUtils()

    def process_parsed_logic(self, parsed_dict, message_obj):
        """
        This function processes the parsed logic
        :param parsed_dict:
        :return:
        """
        mapping = {
            constants.ASSIGN_TASK_PARSER: self.assign_task,
            constants.UPDATE_TASK_PARSER: self.update_task,
            constants.DELETE_TASK_PARSER: self.delete_task,
            constants.VIEW_TABLE_PARSER: self.display_table,
            constants.CREATE_USER_PARSER: self.create_user,
            constants.GET_EXCEL_PARCER: self.get_excel,
            constants.SHOW_TASKS_PARSER: self.show_tasks
        }

        # reply msg is None if you dont want to send any reply
        reply_message = mapping[parsed_dict[constants.SUB_PARSER_NAME]](parsed_dict, message_obj)
        return reply_message

    def show_tasks(self, show_tasks_dict=None, message_obj=None):
        """
        Displays the tasks and the user associated with it
        :param show_tasks_dict: Will be in use in future
        :param message_obj:
        :return:
        """
        # currently only all showing all tasks is available
        task_mapping_table = constants.task_mapping_table
        tasks_table = constants.task_details_table
        user_details_table = constants.user_details_table

        task_mapping_table_obj = self.dbo.read_table(task_mapping_table)
        user_details_table_obj = self.dbo.read_table(user_details_table)
        tasks_table_obj = self.dbo.read_table(tasks_table)

        tmapping_dict = {}
        for row in task_mapping_table_obj:
            # if not tmapping_dict.get(row.task_id, None):
            #     tmapping_dict[row.task_id] = []
            tmapping_dict[row.task_id] = row.user_id
        user_dict = {}
        for row in user_details_table_obj:
            user_dict[row.user_id] = row.user_name
        row_lists = []
        for row in tasks_table_obj:
            task_id = row.task_id
            user_id = tmapping_dict[task_id]
            user_name = user_dict[user_id]
            # I know this looks bad, but will generalize this later. Sorry!!
            single_row = [task_id, user_name, row.description, row.hrs, row.percent_complete]
            row_lists.append(single_row)
        currentTime = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
        excel_filename = "report_showtasks_{}{}".format(currentTime, constants.EXCEL_EXT)
        # excel_filename = "report{}".format(constants.EXCEL_EXT)
        excel_path = os.path.join(constants.EXCEL_FOLDER_PATH, excel_filename)
        print("file  PATH:-------> ", excel_path)
        logging.info("Excel file name : {}".format(excel_filename))
        filepath = self.excel_utils.generate_excel_from_row_list(excel_path, row_lists, constants.SHOW_TASKS_FIELDS)
        if not filepath:
            return "File generation failed"
        aws_file_link = aws_utils.upload_file_to_aws(filepath=filepath)
        print(aws_file_link)
        response = "Download file from link below: \n {} ".format(aws_file_link)
        return response

    def display_table(self, table_name_dict, message_obj=None):
        """
        Displays a table in pretty format
        :param table_name_dict: name of table (String)
        :param message_obj:
        :return:
        """
        table_name = table_name_dict["name"]
        table_obj = self.dbo.read_table(table_name)
        pretty_table = self.pretty_print_table(column_list=constants.TABLE_COL_MAPPING[table_name],
                                               table_object=table_obj)
        adaptive_json = constants.adaptive_json
        adaptive_json['content']['body'][0]['text'] = pretty_table
        skype_bot_utils.add_attachment_and_reply(message_obj, adaptive_json)
        return None

    def get_excel(self, info_dict, message_obj=None):
        """
        This function generates an excel file for given table name.
        :param info_dict: Dict containing table info. (DICT)
                info_dict[table]- Name of table which we need to generate excel file for.
        :param message_obj: msg object (DICT)
        :return:
        """
        table_name = info_dict["table"]
        logging.info("Generating excel for table name : {}".format(table_name))
        table_obj = self.dbo.read_table(table_name)
        column_list = constants.TABLE_COL_MAPPING[table_name]
        currentTime = datetime.datetime.now().strftime('%m-%d-%Y-%H-%M-%S')
        excel_filename = "report_{}_{}{}".format(table_name, currentTime, constants.EXCEL_EXT)
        # excel_filename = "report{}".format(constants.EXCEL_EXT)
        excel_path = os.path.join(constants.EXCEL_FOLDER_PATH, excel_filename)
        print("file  PATH:-------> ", excel_path)
        logging.info("Excel file name : {}".format(excel_filename))
        filepath = self.excel_utils.generate_excel_from_table(excel_path, table_obj, column_list)
        if not filepath:
            return "File generation failed"
        aws_file_link = aws_utils.upload_file_to_aws(filepath=filepath)
        print(aws_file_link)
        file_slash = r"blob:file://"
        atc_dict = {'Name': excel_filename,
                    'ContentType': "application/octet-stream",
                    # 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',  # 'file/xlsx'
                    'ContentUrl': "{}{}".format(file_slash, os.path.join(constants.BASE_DIR, filepath))
                    }
        try:
            skype_bot_utils.add_attachment_and_reply(message_obj, atc_dict)
        except Exception as err:
            print(err)
        response = "Download file from link below: \n {} ".format(aws_file_link)
        return response

    def create_user(self, user_dict, message_obj=None):
        """
        Create user
        :param user_dict:
        :param message_obj:
        :return:
        """
        create_user = {
            "user_name": user_dict["name"],
            "email": user_dict["email"]
        }
        user = self.dbo.add_row(table_name=constants.user_details_table, row_details=create_user)
        reply = "user created with details: {}. Type : viewtable name {} for more details of all users".format(
            create_user,
            constants.user_details_table)
        return reply

    def create_task(self, assign_dict):
        """
        Create a new task
        :param assign_dict: dict required for assigning task
                            assign_task["hrs"]: Hours required to complete task
                            assign_task["task_desc"]: Description of the task
        :return: task table object (Object)
        """
        create_task = {
            "description": assign_dict["desc"],
            "hrs": assign_dict["hrs"]
        }
        task = self.dbo.add_row(table_name=constants.task_details_table, row_details=create_task)
        return task

    def pretty_print_table(self, column_list, table_object):
        """

        :return:
        """
        # cols = ["user_id", "user_name", "email"]
        pretty_print_obj = PrettyTable(column_list)
        for row in table_object:
            row_dict = vars(row)
            rowlist = []
            for col in column_list:
                rowlist.append(row_dict.get(col, None))
            pretty_print_obj.add_row(rowlist)
        return pretty_print_obj.get_string()

    def assign_task(self, assign_dict, message_object=None):
        """
        This is the workflow for assign task.
        :param assign_dict: This dict will contain parameters (including optional params if any) required
                            for assigning a task to one or many users
                            assign_task["to"]: Person to which task is to be assigned. (String)
                            assign_task["hrs"]: Hours required to complete task (Float)
                            assign_task["desc"]: Description of the task (String)
        :return:
        """
        # create row in task table
        # check if name or user_id is given for assigning task
        reply_string = ""
        user_id = None
        user_name = self.dbo.get_row_with_query(constants.user_details_table, {"user_name": assign_dict["to"]})
        if assign_dict["to"].isdigit():
            user_id = self.dbo.get_row_with_query(constants.user_details_table, {"user_id": assign_dict["to"]})
        if user_id:
            task_obj = self.create_task(assign_dict)
            if not isinstance(task_obj, db_setup.Tasks):
                # If the returned obj is not of type Tasks then it'll be an error message, pass it to reply
                return task_obj
            self.dbo.add_user_task_mapping(task_obj=task_obj, user_obj=user_id)
            reply_string = "task added using user id"
        elif user_name:
            task_obj = self.create_task(assign_dict)
            if not isinstance(task_obj, db_setup.Tasks):
                # If the returned obj is not of type Tasks then it'll be an error message, pass it to reply
                return task_obj
            self.dbo.add_user_task_mapping(task_obj=task_obj, user_obj=user_name)
            reply_string = "task added using user name"
        else:
            reply_string = "no user found, no records edited!"

        task_table = self.dbo.read_table(constants.task_details_table)
        pretty_table = self.pretty_print_table(column_list=constants.TASK_TABLE_COLS, table_object=task_table)
        return reply_string + "\n" + pretty_table

    def update_task(self, task_details, msg_object=None):
        """
        This is the workflow for update task. We can update only percent complete and desc value.
        From that percent_complete value is compulsory and the desc value is optional.
        :param task_details: dict which contains all the task details
                            task_details["task_id"]: Task ID of task to update(String)
                            task_details["desc"]: Desc if needed to update, else None (String)
                            task_details["percent_complete"]: Percent complete value that needs to be updated
        :return:
        """
        # check if desc is given for changing
        # if yes then call update table method on the tasks table
        # and update desc and percent_complete value.
        # if desc is not given then update only the percent complete value.
        update_dict = {"task_id": task_details.get("taskid", None),
                       "description": task_details.get("desc", None),
                       "percent_complete": task_details.get("percent", None)}
        self.dbo.update_table(table_name=constants.task_details_table,
                              query_dict={"task_id": task_details.get("taskid", None)},
                              update_dict=update_dict)
        return "Successfully updated task"

    def delete_task(self, task_dict, message_obj=None):
        """
        This is the workflow for deleting task from task table
        :return:
        """
        task_query_dict = {
            "task_id": task_dict["taskid"]
        }
        row = self.dbo.get_row_with_query(constants.task_details_table, task_query_dict)
        if row is not None:
            self.dbo.delete_row(row)
            return "Successfully deleted row : {}".format(task_query_dict)
        else:
            return "No task found for given ID"

    def list_tasks(self, user_id):
        """
        This is the workflow for listing tasks
        :return:
        """
        # read the task mapping table
        table = self.dbo.read_table(table_name=constants.task_mapping_table)

        # get tasks for the given user id
        task_id_list = [i.task_id for i in table if i.user_id == user_id]

        # get task table
        task_table = self.dbo.read_table(table_name=constants.task_details_table)
        task_obj_list = [i for i in task_table if i.task_id in task_id_list]
        for i in task_obj_list:
            print("task_id: {} desc : {}, percent_complete : {}, hrs : {}".format(i.task_id, i.description,
                                                                                  i.percent_complete, i.hrs))
