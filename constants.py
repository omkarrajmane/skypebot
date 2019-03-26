import os

BOT_TAG_STRING = "chitragupt"

# postgres constants
DB_URL = os.environ['HEROKU_POSTGRESQL_TEAL_URL']
user_details_table = "user_details"
task_details_table = "task_details"
task_mapping_table = "TaskMapping"

# parsing constants
# PARSING_LOGIC_FILE = r"/tmp/.parsinglogic"
PARSING_LOGIC_FILE = r".parsinglogic"
TASK_PARSER = "task"
ASSIGN_TASK_PARSER = "assigntask"
UPDATE_TASK_PARSER = "updatetask"
DELETE_TASK_PARSER = "deletetask"
VIEW_TABLE_PARSER = "viewtable"
CREATE_USER_PARSER = "createuser"
GET_EXCEL_PARCER = "getexcel"
SHOW_TASKS_PARSER = "showtasks"

SUB_PARSER_NAME = "subparser_name"

#  These are the arguments which require a -- before them but for readability
# we add it afterward so user won't need to add -- before these arguments
ACCEPTED_ARGS = ["hrs", "desc", "to", "mytask", "taskid", "percent", "name", "email", "table"]
# table related constants

USER_TABLE_COLS = ["user_id", "user_name", "email"]
TASK_TABLE_COLS = ["task_id", "description", "hrs", "percent_complete"]
ID_FIELDS = ["task_id", "user_id"]
SHOW_TASKS_FIELDS = ["task_id", "user_name", "description", "hrs", "percent_complete"]

DATABASE_URI = "postgresql url from heroku"
TABLE_COL_MAPPING = {
    user_details_table: USER_TABLE_COLS,
    task_details_table: TASK_TABLE_COLS,
    task_mapping_table: ID_FIELDS
}
col_size_mapping = {
    "user_id": 6,
    "user_name": 10,
    "email": 10,
    "task_id": 6,
    "description": 20,
    "hrs": 6,
    "percent_complete": 10

}

# Excel file constants
EXCEL_FOLDER_NAME = "excel_files"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FOLDER_PATH = os.path.join(BASE_DIR, EXCEL_FOLDER_NAME)  # r"/tmp/"
EXCEL_EXT = ".xlsx"

# aws related constants
aws_file_link = "amazon s3 bucket url"
aws_folder_name = "files"
aws_access_key_id = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
bucket_name = os.environ['S3_BUCKET_NAME']

# adaptive cards json
adaptive_json = {
    "contentType": "application/vnd.microsoft.card.adaptive",
    "content": {
        "type": "AdaptiveCard",
        "version": "1.0",
        "body": [
            {
                "type": "TextBlock",
                "text": "",
                "size": "medium"
            }
        ]
    }
}
