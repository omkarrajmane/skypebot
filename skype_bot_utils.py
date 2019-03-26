from microsoftbotframework import ReplyToActivity, Activity


def say_hello_function(message_obj):
    """
    This function says hello
    :param message_obj:
    :return:
    """
    reply_text = "Hello!"
    reply_to_message(reply_msg=reply_text, message_obj=message_obj)


def say_bye_function(message_obj):
    """
    This function says bye
    :param message_obj:
    :return:
    """
    reply_text = "Bye..!"
    reply_to_message(reply_msg=reply_text, message_obj=message_obj)


def generic_reply_function(message_obj):
    """
    This is the generic reply function
    :param message_obj:
    :return:
    """
    reply_txt = "I'm not trained to reply to this, human"
    reply_to_message(message_obj=message_obj, reply_msg=reply_txt)


def reply_to_message(reply_msg, message_obj):
    """
    This method sends reply through message object
    :param reply_msg: text msg reply
    :param message_obj: message obj
    :return:
    """
    print("replying to msg with : {}, \n msg object : {}".format(reply_msg, message_obj))
    ReplyToActivity(fill=message_obj, text=reply_msg).send()


def take_func(message_obj, resource_string):
    """
    This is the take function. It is used to claim a resource for utilization
    It will take the user from the message obj as the owner on the resource.
    Resource will be claimed for that day only.
    Thinking of adding more functionality using |
    take
    :param message_obj:
    :param resource_string:
    :return:
    """


def add_attachment_and_reply(message_dict, attachment_dict, text=None):
    """
    This function adds attachment to a message dict/obj
    :param message_dict: message dict/obj of skype
    :param attachment_dict:
    :param text: text you want to add to your attachment reply
    :return:
    """
    attach_dict = {"attachments": [attachment_dict]}
    Activity(attachments=[attachment_dict])
    message_dict.update(attach_dict)
    print("Reply activity msg obj : ", message_dict)
    try:
        ReplyToActivity(fill=message_dict, text=text,
                        attachments=[attachment_dict]).send()
    except Exception as err:
        raise Exception("Error occured while attaching. Error : {}".format(err))
