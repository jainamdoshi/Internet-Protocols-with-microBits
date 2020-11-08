# Add your Python code here. E.g.
from microbit import *
import radio

# This fucntion displays the ending portion of the task
def end(LED, frame_lost, outcome):
    set_LED(LED)
    sleep(2000)
    if outcome:
        display.show(Image.YES)
    else:
        display.show(Image.NO)
    sleep(1000)
    display.scroll(frame_lost)

# This function clears the next two LEDs of the microbit
def clear_next(col, row, x):
    if col == 4:
        row += 1
    col += 1
    display.set_pixel(col % 5, row % 5, 0)
    if x != 0:
        clear_next(col % 5, row % 5, x - 1)

# this fuction sets LEDs depending on frames received and frames lost
def set_LED(LED):
    col = 0
    row = 0
    for i in range(len(LED)):
        display.set_pixel(col, row, LED[i])
        clear_next(col, row, 1)
        
        if col == 4:
          row = (row + 1) % 5
          
        col = (col + 1) % 5

# This function gets the acknowledgment from the receiver
def get_ACK(address, prev_seq_no, start_time):
    TIMEOUT = 1500
    
    while True:
        ACK = radio.receive()
        
        if ACK and ACK.startswith(address):
            index = ACK.find("ACK") + 4
            new_seq_no = int(ACK[index:])
            
            if new_seq_no != prev_seq_no:
                return new_seq_no
                
        if running_time() - start_time >= TIMEOUT:
            return None
            
# This function sends frame
def send_frame(address, seq_no, data):
    frame = address + " " + str(seq_no) + " " + data
    radio.send(frame)

#This is the main function of the program
def start():
    SENDER_ADDRESS = "SD"
    RECEIVER_ADDRESS = "RC"
    ADDRESS = SENDER_ADDRESS + ":" + RECEIVER_ADDRESS
    
    THRESHOLD = 0.9
    frame_loss_rate = 0
    
    frame_sent = 0
    frame_lost = 0
    frame_received = 0
    
    current_seq_no = 0
    prev_seq_no = None
    
    
    DATA = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    length = len(DATA)
    LED = []
    
    #Base Case
    frame_sent += 1
    prev_seq_no = current_seq_no
    start_time = running_time()
    send_frame(ADDRESS, current_seq_no, DATA[frame_received])
    

    while True:

        current_seq_no = get_ACK(ADDRESS, current_seq_no, start_time)

        if (frame_received == length):
            end(LED, frame_lost, True)
            return

        frame_loss_rate = frame_lost / frame_sent
        if frame_loss_rate >= THRESHOLD:
            end(LED, frame_lost, False)
            return

        if current_seq_no is not None:
            frame_received += 1
            LED.append(9)
            prev_seq_no = current_seq_no
            if frame_received < length:
                frame_sent += 1
                start_time = running_time()
                send_frame(ADDRESS, current_seq_no, DATA[frame_received])
        else:
            LED.append(4)
            frame_lost += 1
            frame_sent += 1
            start_time = running_time()
            send_frame(ADDRESS, prev_seq_no, DATA[frame_received])
            
        set_LED(LED)

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