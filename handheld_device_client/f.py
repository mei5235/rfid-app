import tkinter as tk
import threading
from queue import Queue
from turtle import st

import requests
import hid

vendorID = 0x1a86
productID = 0xe010

device = hid.device()
device.open(0x1a86,0xe010)
device.set_nonblocking(1)

thread = None

scanned_book = [""]
scanned_bookshelf = [""]

current_bookshelf_sn = ''

scanType = "BOOKSHELF"

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('LIMS')

        self.geometry('320x200')
        self.grid_rowconfigure(0, weight=1) 
        self.grid_columnconfigure(0, weight=1) 

        container = tk.Frame(self)
        container.grid(column=0, row=0, sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # TODO add page in frames[]
        self.frames = {}
        self.frames['IndexPage'] = IndexPage(parent=container, controller=self)
        self.frames['ScanBookshelf'] = ScanBookshelf(parent=container, controller=self)
        self.frames['ScanBook'] = ScanBook(parent=container, controller=self)
        self.frames['FinalPage'] = FinalPage(parent=container, controller=self)

        self.frames['IndexPage'].grid(row=0, column=0, sticky="nsew")
        self.frames['ScanBookshelf'].grid(row=0, column=0, sticky="nsew")
        self.frames['ScanBook'].grid(row=0, column=0, sticky="nsew")
        self.frames['FinalPage'].grid(row=0, column=0, sticky="nsew")

        self.show_frame('IndexPage')

        # self.appData = {"count":1}

    def show_frame(self, page_num):
        frame = self.frames[page_num]
        frame.tkraise()


class IndexPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self,parent,*args,**kwargs)
        self.controller = controller
        self.grid_rowconfigure(0, weight=6)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0,weight=1)

        title = tk.Label(self, text='Library Inventory Management System', font=("Comic Sans MS",12), justify='center')
        title.grid(columnspan=2,sticky="nsew")

        button1 = tk.Button(self, text='start new stocktaking session',padx=3, pady=3, command=lambda:controller.show_frame('ScanBookshelf'))
        button1.grid(row=2, sticky='sw')

        button2 = tk.Button(self, text='exit', padx=3, pady=3, command=lambda:[controller.destroy(),thread.stop()])
        button2.grid(row=2, column=1, sticky='se')

class ScanBookshelf(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=7)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        navBar = tk.Label(self, text='scan bookshlves',padx=5, pady=5)
        navBar.grid(row=0,sticky="nsew",columnspan=2)

        self.containterAlert = tk.Frame(self)
        self.containterAlert.grid(row=1, sticky="nsew",columnspan=2)

        navBar2 = tk.Label(self.containterAlert, text='Please scan tags',padx=5, pady=5)
        navBar2.place(relx=0.5, rely=0.5, anchor="center") # center align

        def openScanBook():
            global scanType
            scanType = "BOOK"
            print(scanType)
            controller.show_frame('ScanBook')
        button1 = tk.Button(self, text='scan book', command=openScanBook)

        def f():
            global scanned_book 
            scanned_book = [""]
            global scanned_bookshelf
            scanned_bookshelf = [""]
            controller.show_frame('IndexPage')
        button2 = tk.Button(self, text='Cancel session', command=f)

        button1.grid(row=2,column=0,sticky='w')
        button2.grid(row=2,column=1,sticky='e')

class ScanBook(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=7)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        navBar = tk.Label(self, text='scan books',padx=5, pady=5)
        navBar.grid(row=0,sticky="nsew",columnspan=3)

        self.containterAlert = tk.Frame(self)
        self.containterAlert.grid(row=1, sticky="nsew",columnspan=3)

        navBar2 = tk.Label(self.containterAlert, text='Please scan tags',padx=5, pady=5)
        navBar2.place(relx=0.5, rely=0.5, anchor="center")

        def openScanBookshelf():
            global scanType
            scanType = "BOOKSHELF"
            print(scanType)
            controller.show_frame('ScanBookshelf')
        button1 = tk.Button(self, text='scan bookshelf', command=openScanBookshelf)

        #TODO add function call for sending statistic to server
        def end_session():
            global scanned_book
            r = requests.post('http://localhost:3000/api/submitStat',json={'data':{'totalBook':len(scanned_book)-1,'scannedBook':10}})
            res = r.json()
            # print(res['msg'])
            tk.messagebox.showinfo(title="Alert",message=res['msg'])
            controller.show_frame('FinalPage')
        button2 = tk.Button(self, text='End Session', command=end_session) 

        def cancel_session():
            global scanned_book 
            scanned_book = [""]
            global scanned_bookshelf
            scanned_bookshelf = [""]
            controller.show_frame('IndexPage')
        button3 = tk.Button(self, text='Cancel session', command=cancel_session)

        button1.grid(row=2,column=0,sticky='w')
        button2.grid(row=2,column=1)
        button3.grid(row=2,column=2,sticky='e')

class FinalPage(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.controller = controller

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=7)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        navBar = tk.Label(self, text='scan books',padx=5, pady=5)
        navBar.grid(row=0,sticky="nsew",columnspan=2)

        containterAlert = tk.Frame(self)
        containterAlert.grid(row=1, sticky="nsew",columnspan=2)

        # msgaaaa = tk.Label(containterAlert, text='Thank you for using.',padx=5, pady=5)
        # msgaaaa.place(relx=0.5, rely=0.5, anchor="center")

        navBar2 = tk.Label(containterAlert, text='Thank you for using.',padx=5, pady=5)
        navBar2.place(relx=0.5, rely=0.5, anchor="center")

        button = tk.Button(self, text='End program', command=lambda: [controller.destroy(),thread.stop()])

        button.grid(row=2,column=0)
        
# todo thread class
# while loop => scan
# var for targeting scan book/bookshel
class TagThread(threading.Thread):
    
    def __init__(self, *args, **kwargs):
        super(TagThread,self).__init__(*args, **kwargs)
        self._stop_flag = threading.Event()

    def stop(self):
        self._stop_flag.set()
        print('thread stopped')
    
    def is_stop(self):
        return self._stop_flag.is_set()
    
    def run(self):
        print('TagThread running')
        while not self.is_stop():
            da = device.read(64)
            astr = ""
            if da:
                arr = []
                for d in da:
                    arr.append(hex(d).split('x')[-1])

                if arr[1] == "43" and arr[2] == "54" and arr[6] == "45":
                    for i in range(19,31):
                        if len(arr[i]) <= 1:
                            arr[i] = "0"+arr[i]
                        astr += arr[i]
                
                
            if scanType == "BOOKSHELF":
                if astr not in scanned_bookshelf:
                    scanned_bookshelf.append(astr)
                    print(scanned_bookshelf)
                    # print(astr)
                    r = requests.get('http://localhost:3000/api/bookshelf/tagsn/'+astr)
                    # print(r.json())
                    if r.json()['data'] == "":
                        app.frames['ScanBookshelf'].containterAlert.configure(bg='red')
                    else:
                        app.frames['ScanBookshelf'].containterAlert.configure(bg='green')
                        current_bookshelf_sn = astr
                        
            elif scanType == "BOOK":
                # print(astr)
                if astr not in scanned_book:
                    print(astr)
                    r = requests.post('http://localhost:3000/api/checkBook',json={'data':{'booksn':astr,'shelfsn':current_bookshelf_sn}})
                    scanned_book.append(astr)
                    print(scanned_book)
                    # print(r.json())
                    res = r.json()
                    if res['code'] == 101:
                        app.frames['ScanBook'].containterAlert.configure(bg='green')
                    elif res['code'] == 100:
                        app.frames['ScanBook'].containterAlert.configure(bg='red')

            else:
                print("invalid scan type")


if __name__ == "__main__":
    app = MyApp()
    thread = TagThread()
    thread.start()

    def onClose():
        thread.stop()
        app.destroy()


    app.protocol("WM_DELETE_WINDOW",onClose)

    app.mainloop()
