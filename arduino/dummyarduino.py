#fake class to be used when an arduino isn't connected
class DummyArduino:
    def try_send_message(self, msg):
        print(f"<<DummyArduino try_send_message>> Sending \"{msg}\"")
        return True
    
    def try_read_message(self):
        return False, None
    
    def count_messages_in(self):
        return 0
    
    def count_messages_out(self):
        return 0