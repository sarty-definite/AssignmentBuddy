import tkinter as tk
from PIL import Image, ImageTk

Height = 330
Left_Gap = 330
Line_Spacing = 105
Font_Size = 80
Font_Colour = (0, 0, 0)

Default_colour = True


def image_func(Height_from_top=Height, gap_from_left=Left_Gap, line_spacing=Line_Spacing, font_size=Font_Size,
               font_colour=Font_Colour, change_colour=Default_colour, a=1):
    filePath = "text.txt"
    bgPath = "background/liner.png"

    txt = open(filePath, "r")
    BG = Image.open(bgPath)
    gap = gap_from_left
    for i in txt.read():
        cases = Image.open(f"font/{ord(i.upper())}.png")
        if not change_colour:
            d = cases.getdata()
            new_image = []
            for item in d:
                if item[2] in list(range(180, 246)):
                    new_image.append(font_colour)
                else:
                    new_image.append(item)

            cases.putdata(new_image)

        newsize = (int(font_size * 0.64 + 40), font_size)
        cases = cases.resize(newsize)
        BG.paste(cases, (gap, Height_from_top), cases.convert('RGBA'))
        gap += cases.width
        if BG.width < gap + 110:
            gap, Height_from_top = gap_from_left, Height_from_top + line_spacing

    if a == 0:
        return BG
    ratio = 700
    size = (int(BG.width / BG.height * ratio), ratio)
    BG.thumbnail(size, Image.ANTIALIAS)
    # print(BG.width, " ", full_size.height)
    return BG


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.minsize(900, 500)
        self.geometry('1300x600')
        self.state("zoomed")
        self.title('Assignment Helper')

        frame1 = tk.Frame(self, width=1024, height=100, bd=4, relief="ridge")
        frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame2 = tk.Frame(self, width=341, height=100, bd=4, relief="ridge")
        frame2.pack(side=tk.RIGHT, fill=tk.Y)

        preview = image_func(a=1)

        img = ImageTk.PhotoImage(preview)

        # scroll = tk.Scrollbar(self, orient="vertical")
        label1 = tk.Label(frame1, image=img)
        label1.image = img
        label1.pack(side="bottom", fill="both", expand=1)
        # scroll.config(command=label1.yview)
        # scroll.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(frame2, text="Distance From Top", font=('Calibri', 12)).place(relx=0.3, rely=0.1, anchor=tk.N)
        height_from_top = tk.Entry(frame2, width=10, font=('Arial', 16))
        height_from_top.insert(0, Height)
        height_from_top.place(relx=0.7, rely=0.12, anchor=tk.CENTER)

        tk.Label(frame2, text="Gap From Left", font=('Calibri', 12)).place(relx=0.3, rely=0.2, anchor=tk.N)
        left_gap = tk.Entry(frame2, width=10, font=('Arial', 16))
        left_gap.insert(0, Left_Gap)
        left_gap.place(relx=0.7, rely=0.2, anchor=tk.N)

        tk.Label(frame2, text="Space between lines", font=('Calibri', 12)).place(relx=0.3, rely=0.3, anchor=tk.N)
        line_spacing = tk.Entry(frame2, width=10, font=('Arial', 16))
        line_spacing.insert(0, Line_Spacing)
        line_spacing.place(relx=0.7, rely=0.32, anchor=tk.CENTER)

        tk.Label(frame2, text="Font Size", font=('Calibri', 12)).place(relx=0.3, rely=0.4, anchor=tk.N)
        f_size_entry = tk.Entry(frame2, width=10, font=('Arial', 16))
        f_size_entry.insert(0, Font_Size)
        f_size_entry.place(relx=0.7, rely=0.42, anchor=tk.CENTER)

        f_colour_entry = tk.Entry(frame2, width=10, font=('Arial', 16))

        def disable_label():
            global Default_colour
            if not var1.get():
                f_colour_entry.config(state='disabled')
            else:
                f_colour_entry.config(state='normal')

        var1 = tk.IntVar()
        c1 = tk.Checkbutton(frame2, text='Use default Colour', variable=var1, onvalue=0, offvalue=1,
                            command=disable_label)
        c1.place(relx=0.3, rely=0.5, anchor=tk.CENTER)

        tk.Label(frame2, text="Font Colour (RGB)", font=('Calibri', 12)).place(relx=0.3, rely=0.53, anchor=tk.N)
        f_colour_entry = tk.Entry(frame2, width=10, font=('Arial', 16))
        f_colour_entry.insert(0, str(Font_Colour))
        f_colour_entry.config(state='disabled')
        f_colour_entry.place(relx=0.7, rely=0.55, anchor=tk.CENTER)

        def Preview_change(x=1):
            global Default_colour
            if not var1.get():
                colour = True
            else:
                colour = False

            preview2 = image_func(int(height_from_top.get()), int(left_gap.get()), int(line_spacing.get()),
                                  int(f_size_entry.get()),
                                  tuple(map(int, f_colour_entry.get()[1:-1].split(','))),
                                  colour, a=x)
            preview3 = ImageTk.PhotoImage(preview2)
            label1.config(image=preview3)
            label1.image = preview3
            return preview2

        # final = image_func(int(height_from_top.get()), int(left_gap.get()), int(line_spacing.get()),
        #                    int(f_size_entry.get()),
        #                    tuple(map(int, f_colour_entry.get()[1:-1].split(','))),
        #                    default_colour(), a=0)

        def Save():
            Preview_change(0).save('final.png')
            preview2 = image_func(int(height_from_top.get()), int(left_gap.get()), int(line_spacing.get()),
                                  int(f_size_entry.get()),
                                  tuple(map(int, f_colour_entry.get()[1:-1].split(','))), a=1)
            preview3 = ImageTk.PhotoImage(preview2)
            label1.config(image=preview3)
            label1.image = preview3

        preview_button = tk.Button(frame2, width=12, font=('Arial', 12), text='Show Preview', command=Preview_change)
        preview_button.place(relx=0.5, rely=0.66, anchor=tk.CENTER)
        save_button = tk.Button(frame2, width=12, font=('Arial', 12), text='Save', command=Save)
        save_button.place(relx=0.5, rely=0.74, anchor=tk.CENTER)


if __name__ == '__main__':
    App().mainloop()
