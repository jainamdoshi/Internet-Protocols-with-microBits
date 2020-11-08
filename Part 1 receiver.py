# Add your Python code here. E.g.
from microbit import *
import radio

# The function clears the next two LEDs on the microbit 
def clear_next(col, row, x):
    if col == 4:
        row += 1
    col += 1
    display.set_pixel(col % 5, row % 5, 0)
    if x != 0:
        clear_next(col % 5, row % 5, x - 1)

# This function set's LEDs brightness depending on frame received
def set_LED(count):
    col = 0
    row = 0
    for i in range(count):
        display.set_pixel(col, row, 9)
        clear_next(col, row, 1)
        
        if col == 4:
          row = (row + 1) % 5
          
        col = (col + 1) % 5
        
#This functions sends acknowledgment to the sender
def send_ACK(header, seq_no):
    radio.send(header + " ACK " + str(seq_no))

# This is the main fuction of the program
def start(start_time):
    SENDER_ADDRESS = "SD"
    RECEIVER_ADDRESS = "RC"
    ADDRESS = SENDER_ADDRESS + ":" + RECEIVER_ADDRESS
    
    frame_received = 0
    
    prev_seq_no = None
    incoming_seq_no = None
    next_seq_no = None
    
    TIMEOUT = 15000
    
    while True:
        
        frame = radio.receive()
        
        #Checks if the frame received is from the correct sender
        if frame and frame.startswith(ADDRESS):
            
            incoming_seq_no = int(frame[6:7])
            
            #Checks if the frame is not duplicate
            if prev_seq_no == None or prev_seq_no != incoming_seq_no:
                frame_received += 1
                set_LED(frame_received)    
            
            #Calculating the next sequence number,
            next_seq_no = (incoming_seq_no + 1) % 2
            prev_seq_no = incoming_seq_no
            
            send_ACK(ADDRESS, next_seq_no)
            start_time = running_time()
            
        # The receiver will stop receiving more frames if it does not receive any frames within the timeout period
        if running_time() - start_time >= TIMEOUT:
            display.clear()
            return

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
            start_time = running_time()
            start(start_time)

