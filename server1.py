# -*- coding: utf-8 -*-
# file coding to utf-8, for hebrew strings
import socket, pyautogui, threading, pyperclip, time

IP = '0.0.0.0'  # accept any request
PORT = 79
BUFFER = 2048


def recv_data(callback, client_socket, sever_socket, data):
    while data != "exit" and data != "":  # calls stop and checks if  is data is exit and not empty
        callback(data.rstrip("\r\n"))  # calls handle to execute right action and strip newline
        data = client_socket.recv(BUFFER)  # receives info from client
    client_socket.close()
    sever_socket.close()


def handle(data):
    if "key" in data:  # every msg intended for typing will start with the words key
        msg = data[3:]  # separate the word "key" from the msg
        try:
            pyperclip.copy(unicode(msg, 'utf-8'))  # converting the string to unicode and copying it
            pyautogui.hotkey("ctrl", "v")  # paste the text copied
            pyperclip.copy("")  # clear the clipboard
        except Exception, e:  # if cant type
            pass

    elif "del" in data:  # if the user pressed the delete key
        pyautogui.keyDown('backspace')

    elif "enter" in data:  # if the user pressed the enter key
        pyautogui.keyDown('enter')

    elif "left" in data:  # left click
        pyautogui.click(button='left')  # click left

    elif "right" in data:  # right click
        pyautogui.click(button='right')  # click right

    elif "hold" in data:  # if a user holds down left click
        pyautogui.mouseDown(button='left')  # hold left click

    elif "release" in data:  # if the user releases left click
        pyautogui.mouseUp(button='left')  # release left click

    # the idea is to hold left control while pressing +/-
    elif "zoom_in" in data:
        pyautogui.keyDown('ctrlleft')  # hold left control
        pyautogui.press('+')  # press +
        pyautogui.keyUp('ctrlleft')  # let go of left control

    elif "zoom_out" in data:
        pyautogui.keyDown('ctrlleft')
        pyautogui.press('-')  # press -
        pyautogui.keyUp('ctrlleft')

    elif "scroll_up" in data:
        pyautogui.scroll(100)  # scroll up

    elif "scroll_down" in data:  # scroll down
        pyautogui.scroll(-100)

    elif "," in data:  # move mouse
        data = data.splitlines()[0]  # the server gets a lot of data in a packet so it only moves according to first
        cordx, cordy = data.split(",")
        pyautogui.moveRel(float(cordx), float(cordy))  # move the mouse relative to its current position


def main():
    # ASCII ART
    print "----------------------------"
    print "\tH A N D I M O U S E"
    print "----------------------------"

    print "\t   ____((______"
    print "\t  |    _\\\     |"
    print "\t  |   |_|_|    |"
    print "\t  |   |   |    |"
    print "\t  |   |___|    |"
    print "\t  |____________|\n"

    print "THIS IS THE HANDIMOUSE SEVER"
    print "PLEASE ENTER THIS IP IN YOUR PHONE: " + socket.gethostbyname(socket.gethostname())  # print ip of pc
    print "Made by Itay Tovim"

    # create the server socket
    server_socket = socket.socket()
    server_socket.bind((IP, PORT))
    server_socket.listen(1)
    client_socket, address = server_socket.accept()

    data = client_socket.recv(BUFFER)  # initial data
    # this is for getting the initial data because the while depends on it
    t = threading.Thread(target=recv_data, args=[handle, client_socket, server_socket,
                                                 data])  # create a thread that calls recv_data with arguments
    t.start()  # start the thread
    pyautogui.FAILSAFE = False  # this prevents the server from crushing when the mouse goes top left
    input()


if __name__ == '__main__':
    main()
