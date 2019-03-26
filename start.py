import html
import json
import pasring_logic
import task_executions, constants
import skype_bot_utils


class Start(object):
    def __init__(self):
        self.task_exec = task_executions.TaskExecution()

    def get_message(self, message):
        """
        This method gets the messages and returns text
        :param message: message object
        :return: message text
        """
        message_text = ""
        if message["type"] == "message":
            message_text = message.get("text", None)
        return message_text

    def process_message(self, message_obj):
        """
        This is the main function of the bot
        :param message_obj: message object
        """

        print("initial msg obj: {}".format(json.dumps(message_obj)))
        msg_text = self.get_message(message_obj)

        # when a file is sent to the bot and there is not text with the attachment, hence this condition
        if not msg_text:
            return

        # get the first word of msg_text
        relevant_msg = msg_text.split(" ", 1)
        print("releant msg : ", relevant_msg)
        # if the first word is bot string, than separate it.
        # also check if its not the only string, or we'll get list index out of range error
        if relevant_msg[0].lower() == constants.BOT_TAG_STRING and len(relevant_msg) > 1:
            msg_text = relevant_msg[1].lstrip()
        html_escaped_string = html.unescape(msg_text)
        print("passing to parse msg txt :", msg_text)
        # send the text for parsing
        parsed_dict = pasring_logic.pasrse_it(html_escaped_string)
        print("Parsing message.. ", msg_text)

        # if there is an error in the passe arguments then parse_it sends a reply string
        if isinstance(parsed_dict, str):
            skype_bot_utils.reply_to_message(reply_msg=parsed_dict, message_obj=message_obj)
            return

        reply_msg = self.task_exec.process_parsed_logic(parsed_dict=parsed_dict,
                                                        message_obj=message_obj)
        if not reply_msg:
            return
        skype_bot_utils.reply_to_message(reply_msg=reply_msg, message_obj=message_obj)
