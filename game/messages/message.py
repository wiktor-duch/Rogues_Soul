class Message():
    def __init__(self, text: str):
        self.plain_text = text
        self.count = 1
    
    @property
    def full_text(self):
        '''
        The full text of this message, including count
        if the message was repeated.
        '''

        if self.count > 1:
            return f'{self.plain_text} (x{self.count})'
        
        return self.plain_text