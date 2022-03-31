'''
Adapted from:
http://rogueliketutorials.com/tutorials/tcod/v2/
'''
from game.messages.message import Message

class MessageLog():
    def __init__(self):
        self.messages: list[Message] = []

    def add_message(self, text: str, stack: bool = True) -> None:
        '''
        Allows to add a message to this log.
        - 'text' is the message text.
        - if 'stack' is True then the message can stack with previous
        one if the text is the same.
        '''

        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text))
        
    def clear(self):
        '''
        Clears all the previous messages.
        '''
        self.messages = []

    def render(self):
        '''
        Renders all the messages it contains.
        '''

        for msg in self.messages:
            print('  ' + msg.full_text)