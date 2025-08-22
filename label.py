from win32 import win32print
from pythonwin import win32ui
from PIL import Image, ImageWin, ImageGrab
import tkinter


def save_label(path, student):
    def save_image():
        x = root.winfo_rootx()
        y = root.winfo_rooty()
        width = root.winfo_width()
        height = root.winfo_height()

        image = ImageGrab.grab(bbox=(x, y, x+width, y+height))
        image.save(path, "JPEG")
        root.destroy()

    root = tkinter.Tk()
    root.configure(bg="white")
    root.geometry("350x110")

    if len(student.name) < 25:
        fontSize = 18
    elif len(student.name) < 38:
        fontSize = 12
    else:
        fontSize = 8

    name_label = tkinter.Label(root, text=f"{student.name}", font=('Consolas', fontSize), bg="white")
    name_label.pack()
    info_label = tkinter.Label(root, text=f"{student.grade}\n{student.number}   {student.password}", font=('Consolas', 18), bg="white")
    info_label.pack()

    root.attributes('-topmost', 1) #force window to jump to front
    root.after(1000, save_image)

    root.mainloop()


#none of this is my code. i ripped it from some dudes github page (buptxge/print_with_win32.print.py)

def print_label(path):
#physical dimensions of printers page in tenths of mm
#these are not at all the dimensions of my label sheet, but it wouldnt work with the actual dimensions
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111

    printer_name = win32print.GetDefaultPrinter()
    file_name = path

    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    printer_size = hDC.GetDeviceCaps(PHYSICALWIDTH), hDC.GetDeviceCaps(PHYSICALHEIGHT)

    bmp = Image.open(file_name)
    if bmp.size[0] < bmp.size[1]:
        bmp = bmp.rotate(90)

    hDC.StartDoc(file_name)
    hDC.StartPage()

    dib = ImageWin.Dib(bmp)
    dib.draw(hDC.GetHandleOutput (), (0,0,printer_size[0],printer_size[1]))

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()