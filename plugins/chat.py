from plugins import Plugin


class ChatPlugin(Plugin):
    def setup(self):
        self.messages = []
        self.scrollback_limit = 100

    def attach(self):
        if self.messages:
            self.messages.append(u"\u00a7a--- end scrollback ---")
        for message in self.messages:
            self.downstream.send_packet(
                'chat_message',
                self.bt.pack_chat(message),
                self.bt.pack('b', 0))
        del self.messages[:]

    def packet_downstream_chat_message(self, buff):
        message = buff.unpack_chat()
        position = buff.unpack('b')
        if position in (0, 1):
            self.messages.append(message)
            if len(self.messages) > self.scrollback_limit:
                self.messages.pop(0)
