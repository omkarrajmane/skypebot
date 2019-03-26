import logging
from xlsxwriter import Workbook
import constants


class ExcelUtils(object):
    """
    This class is for the excel functions
    """

    def __init__(self):
        # initialize values here
        a = 10

    def create_excel_file(self, excel_filename):
        """
        This function creates a workbook(excel file) and returns its object.
        :param excel_filename: Name of the file to be created. (include .xlsx in name)
        :return: object of Workbook class (excel file)
        """
        try:
            # Create an new Excel file and add a worksheet.
            workbook = Workbook(excel_filename)
            return workbook
        except Exception as err:
            logging.error("Error occured while creating excel file: {}. Error : {}".format(excel_filename, err))

    def generate_excel_from_table(self, excel_filename, table_object, column_list):
        """
        This function generates an excel file containing the data in the given table object.
        :param excel_filename: Name of the excel file to be generated (Should include .xlsx in name). (String)
        :param table_object: Object of the table of which you need to generate excel file.
        :param column_list: List of the columns in the table that you need to display in excel sheet (LIST)
        :return: filename/path of the excel file.
        """
        try:
            workbook = self.create_excel_file(excel_filename)
            worksheet = workbook.add_worksheet()
            # Widen the first column to make the text clearer.
            row_no = 0
            col_no = 0
            # Write the titles to the first row
            for column_name in column_list:
                worksheet.write(row_no, col_no, column_name)
                col_size = constants.col_size_mapping.get(column_name, 10)
                worksheet.set_column(col_no, col_no, col_size)
                col_no += 1
            col_no = 0
            row_no = 1
            logging.info("Created the columns..")
            for taskRowObj in table_object:
                # convert row object to dict
                taskRowObj = vars(taskRowObj)
                col_no = 0
                for column_name in column_list:
                    worksheet.write(row_no, col_no, taskRowObj.get(column_name))
                    col_no += 1
                row_no += 1
            logging.info("Entered remaining data..")
            workbook.close()
            return excel_filename
        except Exception as err:
            print("Error occured while generating excel: {}".format(err))
            return None

    def generate_excel_from_row_list(self, excel_filename, row_lists, column_list):
        """
        This function generates an excel file containing the data in the given row lists.
        :param excel_filename: Name of the excel file to be generated (Should include .xlsx in name). (String)
        :param row_lists: List of lists containing rows
        :param column_list: List of the columns in the table that you need to display in excel sheet (LIST)
        :return: filename/path of the excel file.
        """
        try:
            workbook = self.create_excel_file(excel_filename)
            worksheet = workbook.add_worksheet()
            # Widen the first column to make the text clearer.
            row_no = 0
            col_no = 0
            # Write the titles to the first row
            for column_name in column_list:
                worksheet.write(row_no, col_no, column_name)
                col_size = constants.col_size_mapping.get(column_name, 10)
                worksheet.set_column(col_no, col_no, col_size)
                col_no += 1
            col_no = 0
            row_no = 1
            logging.info("Created the columns..")

            for single_row in row_lists:
                col_no = 0
                for row_value in single_row:
                    worksheet.write(row_no, col_no, row_value)
                    col_no += 1
                row_no += 1
            logging.info("Entered remaining data..")
            workbook.close()
            return excel_filename
        except Exception as err:
            print("Error occured while generating excel: {}".format(err))
            return None
