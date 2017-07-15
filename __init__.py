
from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger

__author__ = 'eward'

LOGGER = getLogger(__name__)

class ShoppingListSkill(MycroftSkill):

    items = []

    def __init__(self):
        super(ShoppingListSkill, self).__init__(name="ShoppingListSkill")

    def initialize(self):
        self.load_data_files(dirname(__file__))
        self.load_regex_files(join(dirname(__file__), 'regex', self.lang))

        read_list_intent = IntentBuilder("ReadListIntent").\
            require("ReadKeyword").build()
        self.register_intent(read_list_intent, self.handle_read_list_intent)

        add_item_intent = IntentBuilder("AddItemIntent"). \
            require("AddKeyWord").require("Item").build()
        self.register_intent(add_item_intent, self.handle_add_item_intent)

        remove_item_intent = IntentBuilder("RemoveItemIntent"). \
            require("RemoveKeyword").require("Item").build()
        self.register_intent(remove_item_intent, self.handle_remove_item_intent)

        clear_list_intent = IntentBuilder("ClearListIntent"). \
            require("ClearKeyword").build()
        self.register_intent(clear_list_intent, self.handle_clear_list_intent)

        count_items_intent = IntentBuilder("CountItemsIntent"). \
            require("CountKeyword").build()
        self.register_intent(count_items_intent, self.handle_count_items_intent())

    def _say_item_count(self):
        num = len(self.items)
        self.speak(str(num) + " items in your list")

    def handle_read_list_intent(self, message):
        if(len(self.items) < 1):
            self.speak("Your list is empty")
        else:
            items_text = " . ".join(self.items)
            data = { 'items': items_text }
            self.speak_dialog('read.list', data)

    def handle_add_item_intent(self, message):
        item = message.data.get("Item")
        self.items.append(item)
        self.speak("okay, I added " + item)


    def handle_remove_item_intent(self, message):
        item = message.data.get("Item")
        item_index = self.items.index(item)

        if(item_index > -1):
            del self.items[item_index]
            self.speak("okay, I removed "+item)
        else:
            self.speak("I couldn't find "+item+" in your list")

        self._say_item_count()

    def handle_count_items_intent(self, message):
        self._say_item_count()


    def handle_clear_list_intent(self, message):
        self.items = []
        self.speak("okay, I cleared it")


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
