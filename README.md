# Internet-Protocols-with-microBits

This project consists of four tasks and all tasks showcase internet protocols using two BBC MicroBits. MicroBits are small computers with LEDs, radio functions, accelerometer, and buttons. The PDF file named "Report" has a more thorough explanation of the implements of the tasks

## Task 1

This part of the project implements the data link layer (OSI level 2) type protocols. The two MicroBits represents two nodes in the network. The protocol simulated in this task is Stop and Wait ARQ with a timeout acknowledge system. The LEDs in each MicroBits represents one packet transferred between the networks

## Task 2

This task still focuses on OSI layer 2 (data link type layer). However, this implementation much more robust and complex prototype than the Stop and Wait for ARQ. The protocol used in this task is called Go Back-N Sliding Window ARQ. The LEDs in each MicroBits represents one packet transferred between the networks

## Task 3

Besides flow control, OSI layer 2’s objective is to perform error checking on the frames being transferred over the network. For the task, the Even-parity SECDED error checking method has been implemented. SECDED code is a step advance version of the Hamming error checking method. The LEDs of MicroBits indicated the status of the messages: Sending, Error-free message, 1-bit error message, 2 or more bits errors.

## Task 4

This task involves implementing Address Resolution Protocol (ARP), where it is used resolve for the Internet Protocol (IP) addresses to Media Access Control (MAC) addresses of the MicroBits. 
