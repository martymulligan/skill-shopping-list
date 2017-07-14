
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'eward'

LOGGER = getLogger(__name__)

class ShoppingListSkill(MycroftSkill):

    def __init__(self):
        super(ShoppingListSkill, self).__init__(name="ShoppingListSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))

        read_list_intent = IntentBuilder("ReadListIntent").\
            require("ReadListKeyword").build()
        self.register_intent(read_list_intent, self.handle_read_list_intent)


    def handle_read_list_intent(self, message):
        self.speak_dialog("read.list")


    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, the method just contains the keyword "pass", which
    # does nothing.
    def stop(self):
        pass

# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return ShoppingListSkill()
