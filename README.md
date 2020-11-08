# Internet-Protocols-with-microBits

This project consists of four taks and all taks showcases internet protocols using two BBC MicroBits. MicroBits are small computers with LEDs, radio functions, accelerometer and buttons. The PDF file named "Report" has more thorough explaing about the implements of the tasks

# Task 1

This part of the project implements data link layer (OSI level 2) type protocols. The two MicroBits represents two nodes in the network. The protocol simulated in this task is Stop and Wait ARQ with timeout acknowledge system. The LEDs in each MicroBits represents one packet transfered betweened the networks

# Task 2

This task still focuses on the OSI layer 2 (data link type layer). However, this implementation much more robust and complex prototype than the Stop and Wait ARQ. The protocol used in this task is called Go Back-N Sliding Window ARQ. The LEDs in each MicroBits represents one packet transferred betweened the networks

# Task 3

Beside flow control, OSI layer 2’s objective is to perform error checking on the frames being transferred over the network. For the task, Even-parity SECDED error checking method has been implemented. SECDED code is one step advance version of Hamming error checking method. THe LEDs of MicroBits indicated the status of the messages: Sending, Error-free message, 1 bit error message, 2 or more bits errors.

# Task 4

This task involves implementing Address Resolution Protocol (ARP), where it is used resolve for the Internet Protocol (IP) addresses to Media Access Control (MAC) addresses of the MicroBits. 