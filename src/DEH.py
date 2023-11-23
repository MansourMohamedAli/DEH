import queue
from tkinter import *
from client_async import read_from_server, setup_async_client, read_holding_register, write_regs
import asyncio
import threading

############################################################
#
#                       Modbus Setup
#
############################################################
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
client = setup_async_client('127.0.0.1', 502)
read_register = read_holding_register

############################################################
#
#                 Base Window Properties
#
############################################################
window = Tk()
"""Window Title (Not Visible)"""
window.title("Mirion")
"""Setting Size"""
window.geometry("1000x500")
"""Setting Color"""
window.configure(bg="#000000")
"""Prevent resizing of X and Y"""
# window.resizable(False, False)
"""Remove Border"""
window.overrideredirect(True)


def exit_application(c):
    """Exit Button"""
    c.close()
    window.destroy()


"""Variables to store the mouse's initial position"""
start_x = 0
start_y = 0


def on_mouse_press(event):
    """Function to handle the mouse button press event"""
    global start_x, start_y
    start_x = event.x
    start_y = event.y


def on_mouse_motion(event):
    """Function to handle the mouse motion event"""
    x = window.winfo_x() + (event.x - start_x)
    y = window.winfo_y() + (event.y - start_y)
    window.geometry(f"+{x}+{y}")


def show_page1(page2_frame=None):
    """Function to switch to Page 1"""
    page2_frame.pack_forget()
    page1_frame.pack(fill="both"
                     , expand=True)


def show_page2(page2_frame=None):
    """Function to switch to Page 2"""
    page1_frame.pack_forget()
    page2_frame.pack(fill="both"
                     , expand=True)


gui_queue = queue.Queue()


async def update_from_mb():
    while True:
        value = await read_from_server(client, read_register)
        print(f"Value read: {value}")
        gui_queue.put(lambda: updateValue(value))
        await asyncio.sleep(1)


label_value = StringVar()


def updateValue(value):
    global label_value
    label_value.set(value)


def periodicGuiUpdate():
    while True:
        try:
            fn = gui_queue.get_nowait()
        except queue.Empty:
            break
        fn()
    window.after(1000, periodicGuiUpdate)


def start_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(update_from_mb())
    loop.run_forever()


def onKeyPress(event):
    test = event.char
    keyLabel = Label(page1_frame, text=event.char, bg="#FFFFFF", width=5, height=2)
    keyLabel.pack()
    print(test)


def tab_order(*args, **kwargs):
    args[0].focus_set()
    for w in args:
        w.lift()


def focus(event):
    widget = window.focus_get()
    print(widget, "has focus")

"""Bind mouse button press and motion events to the window"""
window.bind("<ButtonPress-1>", on_mouse_press)
window.bind("<B1-Motion>", on_mouse_motion)
window.bind('<Key>', focus)

############################################################
#
#                     PAGE 1
#
############################################################
"""Initializing Frame Use same color as window."""
page1_frame = Frame(window, bg=window["bg"])
"""Show Page 1 and fill size of window"""
page1_frame.pack(fill="both", expand=True)


############################################################
#                    WIDGETS
############################################################


def write_register():
    asyncio.run(write_regs(client))


"""Label that reads Modbus Server"""
# testLabel1 = Label(page1_frame, textvariable = label_value, bg="#FFFFFF", width=5, height=2)
# testLabel1.place(x=100,y=100)

entry_1 = Entry(window, bg="white", font=("Helvetica", 20), width=3)
entry_1.pack()

entry_2 = Entry(window, bg="white", font=("Helvetica", 20), width=3)
entry_2.pack()

entry_3 = Entry(window, bg="white", font=("Helvetica", 20), width=3)
entry_3.pack()

exitButton = Button(text="Exit", command=lambda: exit_application(client))
exitButton.pack()

tab_order(entry_1, entry_2, entry_3, exitButton)
print(window.focus_get())

# writeButton = Button(text="Write register", command=lambda: write_register)
# writeButton.place(x=0, y=100)



if __name__ == "__main__":
    '''Uncomment next two lines to enable modbus client'''
    # threading.Thread(target=start_loop).start()
    # periodicGuiUpdate()
    window.mainloop()
