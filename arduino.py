import serial
import time
import threading


from queue import Queue, Empty, Full


ARDUINO_READ_TIMEOUT = 1


class Arduino:
    def __init__(self, port, baud, serial_args=(), serial_kwargs={}):
        self.queue_in = Queue() #messages coming in to the computer
        self.queue_out = Queue()#messages going out to the arduino

        self.port = port
        self.baud = baud
        self.serial = serial.Serial(port, baud, *serial_args, **serial_kwargs)
        self.serial.flush()

        self.READ_THREAD_REQUIRED = True
        self.SEND_THREAD_REQUIRED = True
        self.READ_THREAD_ACTIVE = False
        self.SEND_THREAD_ACTIVE = False

        time.sleep(1) #give the connection a second to settle
        self.read_thread = threading.Thread(target = self.__read_thread_target)
        self.send_thread = threading.Thread(target = self.__send_thread_target)
        self.read_thread.start()
        self.send_thread.start()

    def shutdown(self):
        #TODO shutdown serial

        self.READ_THREAD_REQUIRED = False
        self.SEND_THREAD_REQUIRED = False

        #TODO use Thread.join 
        #wait until the threads clean up
        while self.SEND_THREAD_ACTIVE or self.READ_THREAD_ACTIVE:
            time.sleep(0.1)



    def __read_thread_target(self):
        #helper function that is only ever used here
        def add_message(msg):
            try:
                self.queue_in.put_nowait(msg)
            except Full:
                print("Something went horribly wrong with read_thread.")

        def readline():
            try:
                msg = self.serial.readline()
                return True, msg
            except:
                return False, b""


        print(f"<<Arduino[{self.port}:{self.baud}] read thread>> Thread starting")
        while self.READ_THREAD_REQUIRED:
            self.READ_THREAD_ACTIVE = True

            success, msg = readline()
            if success and len(msg) != 0:
                decoded = Arduino.decode(msg)
                print(f"<<Arduino[{self.port}:{self.baud}] read thread>> Got: {msg}")
                add_message(decoded)

        self.READ_THREAD_ACTIVE = False
        print(f"<<Arduino[{self.port}:{self.baud}] read thread>> Thread closing")


    def __send_thread_target(self):
        #helper function that is only ever used here
        def get_message():
            if self.count_messages_out() == 0:
                return False
            
            try:
                return self.queue_out.get_nowait()
            except Empty:
                return False
            except:
                print("Something went horribly wrong with send_thread.")
                return False

        print(f"<<Arduino[{self.port}:{self.baud}] send thread>> Thread starting")
        while self.SEND_THREAD_REQUIRED:
            self.SEND_THREAD_ACTIVE = True

            if (msg := get_message()):
                if isinstance(msg, bytes):
                    self.serial.write(msg)
                else:
                    self.serial.write(Arduino.encode(msg))
                print(f"<<Arduino[{self.port}:{self.baud}] send thread>> Sending: {msg}")

        self.SEND_THREAD_ACTIVE = False
        print(f"<<Arduino[{self.port}:{self.baud}] send thread>> Thread closing")



    def count_messages_in(self):
        return self.queue_in._qsize()
    
    def count_messages_out(self):
        return self.queue_out.qsize()
    
    def try_read_message(self):
        try:
            return True, self.queue_in.get_nowait()
        except Empty:
            return False, None
    
    def try_send_message(self, msg):
        try:
            self.queue_out.put_nowait(msg)
            return True
        except Full:
            return False
        
        

    @staticmethod
    def encode(msg: str):
        return msg.encode("utf-8")
    
    @staticmethod
    def decode(msg: bytes):
        return msg.decode("utf-8")



if __name__ == "__main__":
    arduino = Arduino('COM3', 115200, serial_kwargs={"timeout": 0.1})
   
    try:
        while True:
            # Send the string. Make sure you encode it before you send it to the Arduino.
            arduino.try_send_message(input("Send a message!\n"))
    except KeyboardInterrupt:
        pass
    finally:
        arduino.shutdown()