__author__ = "Nicholas Pugliese"
__copyright__ = "Copyright 2018, NickP"
__credits__ = ["Nicholas Pugliese"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Nicholas Pugliese"
__email__ = "nicholas.d.pugliese@gmail.com"
__status__ = "Prototype"

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
import os
import re


class InputScreen(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("Hugh Jazz Credit Security")
        self.resizable(False, False)

        # center the window
        # assuming you have a symmetrical setup of monitors...
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqwidth()

        position_right = int(self.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(self.winfo_screenheight() / 3 - window_height / 2)

        self.geometry("+{}+{}".format(position_right, position_down))

        # as it turns out, there is no way to make the background of a widget transparent in tkinter.
        # this background image code works, but the label and entry widgets have opaque backgrounds above it.
        # shame.

        # self.base_folder = os.path.dirname(__file__)
        # self.background_path = os.path.join(self.base_folder, 'background.png')
        # self.background_image = tk.PhotoImage(file=self.background_path)
        #
        # self.background_label = tk.Label(self, image=self.background_image)
        # self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # setup the different font sizes to be used in each label
        self.title_font = ('times', 24)
        self.label_font = ('times', 16)
        self.input_font = ('courier', 12)

        # create the three basic frames
        self.text_frame = tk.Frame(self)  # uses pack
        self.input_frame = tk.Frame(self)  # uses grid
        self.progress_frame = tk.Frame(self, pady=20)  # uses pack

        # create the labels and entry fields
        # long_text variable used for readability
        self.long_text = "Hackers keep databases with millions of stolen credit card numbers;\n" \
                         "is yours among them?\n\n" \
                         "Enter your information below and we will scan thousands of illegal hacker databases to see " \
                         "if your credit card data has been compromised."

        # create labels for the header title and the body text
        self.header_text = tk.Label(self.text_frame, text="Did a hacker steal your credit card?", justify="left",
                                    anchor="w", font=self.title_font, wraplength=800, pady=10)
        self.body_text = tk.Label(self.text_frame, text=self.long_text, justify="left", anchor="w",
                                  font=self.label_font, wraplength=600, pady=10)

        # create the label and entry widget for the credit card number input field
        self.cc_text = tk.Label(self.input_frame, text="Credit Card Number: ", font=self.label_font, pady=2)
        self.cc_box = tk.Entry(self.input_frame, width=16, font=self.input_font)

        # create the label and entry widget for the expiration date input field
        self.exp_text = tk.Label(self.input_frame, text="Expiration Date (MM/YY): ", font=self.label_font, pady=2)
        self.exp_box = tk.Entry(self.input_frame, width=5, font=self.input_font)

        # create the label and entry widget for the zip code input field
        self.zip_text = tk.Label(self.input_frame, text="Zip Code: ", font=self.label_font, pady=2)
        self.zip_box = tk.Entry(self.input_frame, width=5, font=self.input_font)

        # create the image of a credit card in the empty space next to the last two input fields
        # photo taken from pexels.com
        # NOTE: when bundling an .exe comment out these 5 lines until i figure out how to get pyinstaller
        # to properly read resource paths
        # link to a reddit post on it:
        # https://www.reddit.com/r/learnpython/comments/4kjie3/how_to_include_gui_images_with_pyinstaller/
        self.base_folder = os.path.dirname(__file__)
        self.card_image_path = os.path.join(self.base_folder, 'credit_card_public.png')
        self.photo = tk.PhotoImage(file=self.card_image_path)
        self.pic_label = tk.Label(self.input_frame, image=self.photo, width=108, height=101)
        self.pic_label.image = self.photo  # keep this reference around for garbage collection

        # big red button
        self.submit_button = tk.Button(self.progress_frame, text="SCAN NOW", command=self.steal_info, bg="red",
                                       width=40, height=3)

        # header and body labels use pack for simplicity
        self.header_text.pack()
        self.body_text.pack()

        # the input fields use a grid
        self.cc_text.grid(sticky="E", row=0, column=0)
        self.cc_box.grid(sticky="W", row=0, column=1, columnspan=5)

        self.exp_text.grid(sticky="E", row=1, column=0)
        self.exp_box.grid(sticky="W", row=1, column=1)

        self.zip_text.grid(sticky="E", row=2, column=0)
        self.zip_box.grid(sticky="W", row=2, column=1)

        # this line needs to be commented out when bundling the .exe
        self.pic_label.grid(row=1, column=4, rowspan=3)

        # the big red button uses its own frame under the input fields
        self.submit_button.pack()

        # pack the frames
        self.text_frame.pack()
        self.input_frame.pack()
        self.progress_frame.pack()

        # make the cursor focus the credit card box
        self.cc_box.focus_set()

    def steal_info(self):
        """
        steal_info generates the window with the progress bar
        """

        # regex to match dates in MM/YY or MMYY format.
        exp_pattern = re.compile('(0[1-9]|1[0-2])/?([0-9]{4}|[0-9]{2})')

        # get the contents of each of the input fields
        cc = self.cc_box.get()
        exp = self.exp_box.get()
        zip_in = self.zip_box.get()  # 'zip' is a keyword in python

        m = exp_pattern.match(exp)
        err = ""

        # start building the error message, if any
        if not cc.isdigit() or len(cc) != 16:
            err += "Credit Card numbers must only be numbers of length 16.\n\n"
        if not m:
            err += "Date must be formatted as MM/YY\n\n"
        if not zip_in.isdigit() or len(zip_in) != 5:
            err += "Zip codes must only be numbers of length 5."
        if len(err) != 0:
            msg.showerror("Input Error", err)
            return
        else:
            # create a child window on top of root
            scan_window = tk.Toplevel(self)
            scanning_frame = tk.Frame(scan_window, pady=20)
            scan_window.wm_title("SCANNING")

            # make the progress bar
            # using a workaround to make fake progress. see inc_bar
            progress_text = tk.Label(scanning_frame, text="Scanning database %d out of 6871" % 1, width=40)
            # 6871 chosen randomly, it has no meaning
            pb = ttk.Progressbar(scanning_frame, orient="horizontal", length=200, mode="determinate", maximum=6871)
            pb.pack()
            progress_text.pack(side="bottom", fill="x", expand=True, padx=100, pady=20)
            scanning_frame.pack()
            scan_window.focus_set()
            scan_window.grab_set()
            scan_window.attributes("-topmost", True)
            self.inc_bar(pb, scan_window, progress_text)

    def inc_bar(self, pb, scan, label):
        pb["value"] += 1
        if pb["value"] <= 6871:
            # could probably store the max as a variable and reference it here
            label.config(text="Scanning database %d out of 6871" % pb["value"])
            self.after(1, self.inc_bar, pb, scan, label)
        else:
            msg.showinfo("Result", "Your card information is not in any hacker database!")
            pb["value"] = 0
            # kinda odd way of removing the window but w/e
            self.bind("<ButtonRelease-1>", scan.destroy())
            # reset the focus back to the cleared input boxes
            self.cc_box.delete(0, tk.END)
            self.exp_box.delete(0, tk.END)
            self.zip_box.delete(0, tk.END)
            self.cc_box.focus_set()


# ya boi main
if __name__ == "__main__":
    program = InputScreen()
    program.mainloop()
