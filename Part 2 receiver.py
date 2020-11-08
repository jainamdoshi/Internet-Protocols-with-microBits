from microbit import *
import radio


def clear_next(col, row, x):
    if col == 4:
        row += 1
    col += 1
    display.set_pixel(col % 5, row % 5, 0)
    if x != 0:
        clear_next(col % 5, row % 5, x - 1)

def set_LED(frame_received):
    col = 0
    row = 0
    for i in range(frame_received):
        display.set_pixel(col, row, 9)
        clear_next(col, row, 1)
        
        if col == 4:
          row = (row + 1) % 5
          
        col = (col + 1) % 5

def send_ACK(address, seq_no):
    ACK = address + " ACK " + str(seq_no)
    radio.send(ACK)

def start():
    TIMEOUT = 10000

    SENDER_ADDRESS = "SD"
    RECEIVER_ADDRESS = "RC"
    ADDRESS = SENDER_ADDRESS + ":" + RECEIVER_ADDRESS

    frame_received = 0

    start_time = running_time()

    while True:

        if running_time() - start_time >= TIMEOUT:
            display.clear()
            return

        frame = radio.receive()
        if frame and frame.startswith(ADDRESS):
            start_index = frame.find(" ") + 1
            end_index = frame.find(" ", frame.find(" ") + 1)
            new_seq_no = int(frame[start_index:end_index])
            if (frame_received == new_seq_no):
                frame_received += 1
                set_LED(frame_received)

            start_time = running_time()
            send_ACK(ADDRESS, new_seq_no)
            
'''
*    Title: Python Main Function implementation
*    Author: Bryan Weber
*    Date: n.d
*    Code version: 
*    Availability: https://realpython.com/python-main-function/
*
'''

if __name__ == "__main__":
    while True:
        if button_a.was_pressed():
            radio.on()
            radio.config(group=5)
            start()