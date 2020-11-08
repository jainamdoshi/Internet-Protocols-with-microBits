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

#This function sends one frame
def send_frame(address, index, data):
    frame = address + " " + str(index) + " " + data[index]
    radio.send(frame)

#This function sends multiple frames
def send_frames(address, window_start, window_end, data):
    for seq_no in range(window_start, window_end + 1):
        frame = address + " " + str(seq_no) + " " + data[seq_no]
        radio.send(frame)
    
# This function gets the acknowledgment from the receiver
def get_ACK(address, start_time, frame_received):
    TIMEOUT = 1500

    while True:
        ACK = radio.receive()

        #Checks if the ack is from the correct receiver
        if ACK and ACK.startswith(address):
            index = ACK.find("ACK") + 4
            new_seq_no = int(ACK[index:])
            if frame_received == new_seq_no:
                return True
    
        if running_time() - start_time >= TIMEOUT:
            return False

#This is the main function of the program
def start():
    
    window_start = 0
    window_end = 3

    SENDER_ADDRESS = "SD"
    RECEIVER_ADDRESS = "RC"
    ADDRESS = SENDER_ADDRESS + ":" + RECEIVER_ADDRESS

    DATA = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    length = len(DATA)
    LED = []

    frame_received = 0
    frame_sent = 0
    frame_lost = 0

    frame_loss_rate = 0
    THRESHOLD = 0.2

    # Base Case
    frame_sent += (window_end - window_start) + 1
    start_time = running_time()
    send_frames(ADDRESS, window_start, window_end, DATA)

    while True:
           
        ACK = get_ACK(ADDRESS, start_time, frame_received)

        if frame_received == length:
            end(LED, frame_lost, True)
            return
        
        frame_loss_rate = frame_lost / frame_sent
        if frame_loss_rate > THRESHOLD:
            end(LED, frame_lost, False)
            return

        if ACK:
            LED.append(9)
            window_start += 1
            window_end += 1
            frame_received += 1
            if window_end < length:
                frame_sent += 1
                start_time = running_time()
                send_frame(ADDRESS, window_end, DATA)
                
        else:
            LED.append(4)
            if window_end >= length:
                window_end = length - 1
            frame_lost += 1
            frame_sent += (window_end - window_start) + 1
            start_time = running_time()
            send_frames(ADDRESS, window_start, window_end, DATA)

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