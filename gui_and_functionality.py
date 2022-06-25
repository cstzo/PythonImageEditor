from tkinter import ttk, filedialog
from tkinter.filedialog import asksaveasfilename  # allows for GUI to be created and edited images to be downloaded to user's files
from tkinter import *  # allows for GUI customization
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps  # imports all the image methods and built-in functions used
from original_filters import Filters  # imports custom filter class
import os


def run_script():
    """
    This function when called from the main script will run the program and open the GUI
    :return:
    """

    global main, image_being_edited, original_image

    main = Tk()
    main.geometry("950x500")
    main.title("Python Image Editing Software")

    # Creates and places the image being edited canvas that displays the edits
    image_being_edited = Canvas(main, width="600", height="420", relief=RAISED, bd=3)
    image_being_edited.place(x=15, y=15)

    #  Creates and places original image canvas
    original_image = Canvas(main, width='200', height='150', relief=RAISED, bd=3)
    original_image.place(x=630, y=285)

    #  runs the program opening the popup and adding all the GUI features
    GUI()
    open_popup()
    main.mainloop()


im_odd = None


# Image editing functions

def open_popup():
    """
    This function opens the welcoming popup window every time the program is run
    :return:
    """

    popup = Toplevel()
    popup.attributes('-topmost', True)
    popup.geometry("420x120")
    popup.title("Photo Editor Instructions")
    Label(popup, text="Hey!\nWelcome to your new photo editor.\nSimply upload an image,\n "
                      "apply your change and save it back to your computer.", font="arial 12 bold").place(x=0, y=0)

    popup_exit_button = Button(popup, text="Continue", bg='green', fg='white', font='ariel 10 bold',
                               command=popup.destroy)
    popup_exit_button.place(x=175, y=85)


def help():
    """
    This function creates a help menu popup that has detailed instructions on how to use the program when clicked
    :return:
    """

    help_popup = Toplevel()
    help_popup.attributes('-topmost', True)
    help_popup.geometry("460x155")
    help_popup.title("Photo Editor Help Menu")
    Label(help_popup, text="1)Add an image from your files by clicking \'SELECT IMAGE\'\n"
                           "2)Apply one of the available filters\nPress \'UNDO\' to go back\n"
                           "3)To merge multiple filters, click \'LOCK\' between each one\n"
                           "4)When satisfied, click \'SAVE AS..\' to save edited image\n"
                           "5)Select new image or press \'RESET\'", font="arial 12 bold").place(x=0, y=0)

    popup_exit_button = Button(help_popup, text="Back", bg='grey', fg='white', font='ariel 10 bold',
                               command=help_popup.destroy)
    popup_exit_button.place(x=215, y=120)


def selected():
    """
    This function allows the user to select an image to edit directly from their
    files and outputs it to the screen
    :return:
    """

    global image_from_file, img, name

    #  prompts user to insert an image from their computer's files
    image_from_file = filedialog.askopenfilename(initialdir=os.getcwd())

    #  clears the canvas if user chooses to select new image
    image_being_edited.delete("all")

    #  opens image, sets size and placement of the image that will be edited
    name = image_from_file
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))
    selected = ImageTk.PhotoImage(img)

    #  sets size and placement of both canvases
    img.thumbnail((200, 200))
    unedited = ImageTk.PhotoImage(img)
    image_being_edited.create_image(305, 210, image=selected)
    image_being_edited.image = selected
    original_image.image = unedited
    original_image.create_image(105, 80, image=unedited)


def lock():
    """
    This function allows for another filter to be added onto the previous edit
    :return:
    """

    global image_from_file

    file_name = "for_editing_purposes.png"

    if image_being_edited.image == im_odd:
        im_even.save(file_name)
    #  any function from now will now edit upon the newly edited image
    image_from_file = "for_editing_purposes.png"


def undo():
    """
    This function undoes the last filter added to the image
    :return:
    """

    global img, img_from_file, name
    image_being_edited.delete("all")
    img = Image.open(name)
    img.thumbnail((600, 600))
    image = ImageTk.PhotoImage(img)
    image_being_edited.create_image(305, 210, image=image)
    image_being_edited.image = image


def blur(image):
    """
    This function blurs the image being edited based on values input through a slider
    :param image:
    :return:
    """
    global image_from_file, im_even, im_odd
    for m in range(blur_val.get()):
        img = Image.open(image_from_file)
        img.thumbnail((600, 600))
        im_even = img.filter(ImageFilter.GaussianBlur(m))
        im_odd = ImageTk.PhotoImage(im_even)
        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def cartoon(image):
    """
    This function uses original class methods to "cartoon-ify" the image being edited based on values input through a slider
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    for m in range(cartoon_val.get()):
        account1 = Filters(image_from_file)
        f1 = account1.cartoon(int(m))
        imgg = Image.open(f1)
        im_even = imgg
        im_odd = ImageTk.PhotoImage(im_even)
        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def contrast(image):
    """
    This function changes the contrast values image being edited based on values input through a slider
    :param image:
    :return:
    """

    global image_from_file, img4, img5, im_even, im_odd
    for m in range(contrast_val.get()):
        img = Image.open(image_from_file)
        img.thumbnail((600, 600))

        im_even = (ImageEnhance.Contrast(img)).enhance(m)
        im_odd = ImageTk.PhotoImage(im_even)

        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def rotate_image(image):
    """
    This function rotates the image being edited 90, 180, 270, or 360 degrees
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))

    #  rotates image based on inputted val
    im_even = img.rotate(int(rotate_choices.get()))

    #  outputs back to the proper canvas
    im_odd = ImageTk.PhotoImage(im_even)
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def flip_image(image):
    """
    This function flips the image either horizontally or vertically based on the user's selection
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))

    #  flips image left to right or up to down based on user input
    if flip_choices.get() == "Horizontal":
        im_even = img.transpose(Image.FLIP_LEFT_RIGHT)
    elif flip_choices.get() == "Vertical":
        im_even = img.transpose(Image.FLIP_TOP_BOTTOM)
    im_odd = ImageTk.PhotoImage(im_even)

    #  outputs back to the edited image canvas
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def image_border(image):
    """
    This function adds a border of different widths to the image based on the user's size choice
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((580, 580))

    #  adds a border to the image being edited
    im_even = ImageOps.expand(img, border=int(border_choices.get()), fill=30)
    im_odd = ImageTk.PhotoImage(im_even)

    #  outputs new image to the image being edited screen
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def emboss_image():
    """
    This function applies the "emboss" filter onto the image being edited
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))

    im_even = img.filter(ImageFilter.EMBOSS)
    im_odd = ImageTk.PhotoImage(im_even)

    #  outputs new image to the image being edited screen
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def make_bw():
    """
    This function makes the image being edited black and white
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))

    im_even = img.convert("1")

    #  outputs new image to the image being edited screen
    im_odd = ImageTk.PhotoImage(im_even)
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def edge_contour():
    """
    This function applies the "contour" filter to the image being edited when the appropriate button is clicked
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))

    #  applies the contour filter to the image being edited
    im_even = img.filter(ImageFilter.CONTOUR)

    #  outputs new image to the image being edited screen
    im_odd = ImageTk.PhotoImage(im_even)
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def get_edges():
    """
    This function applies the "find_edges" function to the image being edited
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))
    im_even = img.filter(ImageFilter.FIND_EDGES)

    #  outputs new image to the image being edited screen
    im_odd = ImageTk.PhotoImage(im_even)
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def brightness(image):
    """
    This function changes the brightness of an image using values inputted through a slider bar
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    for m in range(brightness_val.get()):
        img = Image.open(image_from_file)
        img.thumbnail((600, 600))
        imgg = ImageEnhance.Brightness(img)
        im_even = imgg.enhance(m)

        #  outputs new image to the image being edited screen
        im_odd = ImageTk.PhotoImage(im_even)
        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def purple(image):
    """
    This function uses original class methods to "purple-ify" the image being edited based on values input through a slider
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    for m in range(purple_val.get()):
        account1 = Filters(image_from_file)
        f1 = account1.purple(int(m))
        im_even = Image.open(f1)
        im_odd = ImageTk.PhotoImage(im_even)

        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def burning(image):
    """
    This function uses original class methods to add a burning effect the image being edited based on values input through a slider
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    for m in range(burning_val.get()):
        account1 = Filters(image_from_file)
        f1 = account1.burning(int(m))
        im_even = Image.open(f1)
        im_odd = ImageTk.PhotoImage(im_even)

        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def saturation(image):
    """
    This function uses original class methods to adjust the saturation level of
    the image being edited based on values input through a slider
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    for m in range(saturation_val.get()):
        account1 = Filters(image_from_file)
        f1 = account1.saturation(int(m))
        im_even = Image.open(f1)
        im_odd = ImageTk.PhotoImage(im_even)

        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def gamma_correction(image):
    """
    This function uses original class methods to correct the gamma values of
     the image being edited based on values input through a slider
    :param image:
    :return:
    """

    global image_from_file, im_even, im_odd
    for m in range(gamma_val.get()):
        account1 = Filters(image_from_file)
        f1 = account1.gamma_correction(int(m))
        im_even = Image.open(f1)
        im_even.thumbnail((600, 600))
        im_odd = ImageTk.PhotoImage(im_even)

        image_being_edited.create_image(305, 210, image=im_odd)
        image_being_edited.image = im_odd


def min():
    """
    This function applies the "min" filter to the image being edited
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))

    #  applies the contour filter to the image being edited
    im_even = img.filter(ImageFilter.MinFilter)

    #  outputs new image to the image being edited screen
    im_odd = ImageTk.PhotoImage(im_even)
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def max():
    """
    This function applies the "max" filter to the image being edited
    :return:
    """

    global image_from_file, im_even, im_odd
    img = Image.open(image_from_file)
    img.thumbnail((600, 600))

    #  applies the contour filter to the image being edited
    im_even = img.filter(ImageFilter.MaxFilter)

    #  outputs new image to the image being edited screen
    im_odd = ImageTk.PhotoImage(im_even)
    image_being_edited.create_image(305, 210, image=im_odd)
    image_being_edited.image = im_odd


def save():
    """
    This function saves the image that was edited to the user's files and allows them to choose between .png and .jpg extension
    :return:
    """

    global image_from_file, im_even, im_odd

    file_name = asksaveasfilename(defaultextension=f'.{image_from_file.split(".")[-1]}', filetypes=[('png file', '*.png'), ('jpg file', '*.jpg')])

    if file_name:
        if image_being_edited.image == im_odd:
            im_even.save(file_name)


def reset():
    """
    This function clears the canvases for the original image and the one being edited
    :return:
    """

    image_being_edited.delete("all")
    original_image.delete("all")


def spam_popup():
    """
    This function is a "troll" function and opens 400 popups on the user's screen
    :return:
    """

    for i in range(400):
        open_popup()


def GUI():
    """
    This function creates everything necessary for the GUI
    :return:
    """

    global blur_val, cartoon_val, contrast_val, rotate_choices, flip_choices, border_choices, brightness_val, purple_val, burning_val, saturation_val, gamma_val

    blur_slider = Label(main, text="Blur:", font="ariel 10 bold").place(x=630, y=8)
    blur_val = IntVar()
    blur_scale = ttk.Scale(main, from_=0, to=10, variable=blur_val, command=blur, length=80).place(x=675, y=7)

    cartoon_slider = Label(main, text="Cartoon:", font="ariel 10 bold").place(x=630, y=50)
    cartoon_val = IntVar()
    cartoon_scale = Scale(main, from_=2, to=6, variable=cartoon_val, command=cartoon, orient=HORIZONTAL, length=80).place(x=700, y=35)

    contrast_slider = Label(main, text="Contrast:", font="ariel 10 bold").place(x=630, y=90)
    contrast_val = IntVar()
    contrast_scale = ttk.Scale(main, from_=1, to=10, variable=contrast_val, command=contrast, length=80).place(x=700, y=88)

    brightness_slider = Label(main, text="Brightness:", font="ariel 10 bold").place(x=630, y=220)
    brightness_val = IntVar()
    brightness_scale = ttk.Scale(main, from_=1, to=10, variable=brightness_val, command=brightness, length=80).place(x=710, y=220)

    rotate = Label(main, text="Rotate:", font="ariel 10 bold").place(x=630, y=125)
    degrees = [0, 90, 180, 270]
    rotate_choices = ttk.Combobox(main, values=degrees, font='ariel 5 bold')
    rotate_choices.bind("<<ComboboxSelected>>", rotate_image)
    rotate_choices.place(x=685, y=127)

    purple_slider = Label(main, text="Purple!", font="ariel 10 bold").place(x=800, y=220)
    purple_val = IntVar()
    purple_scale = ttk.Scale(main, from_=2, to=6, variable=purple_val, orient=HORIZONTAL, command=purple, length=80).place(x=855, y=220)

    flip_button = Label(main, text="Flip:", font="ariel 10 bold").place(x=630, y=155)
    possibilities = ["Vertical", "Horizontal"]
    flip_choices = ttk.Combobox(main, values=possibilities, font='ariel 5 bold')
    flip_choices.bind("<<ComboboxSelected>>", flip_image)
    flip_choices.place(x=670, y=157)

    burning_slider = Label(main, text="Burning: ", font="ariel 10 bold").place(x=795, y=125)
    burning_val = IntVar()
    burning_scale = ttk.Scale(main, from_=5, to=25, variable=burning_val, orient=HORIZONTAL, command=burning, length=80).place(x=860, y=125)

    saturation_slider = Label(main, text="Saturation: ", font="ariel 10 bold").place(x=625, y=255)
    saturation_val = IntVar()
    saturation_scale = ttk.Scale(main, from_=1, to=100, variable=saturation_val, orient=HORIZONTAL, command=saturation, length=80).place(x=710, y=255)

    gamma_slider = Label(main, text="Gamma: ", font="ariel 10 bold").place(x=795, y=158)
    gamma_val = IntVar()
    gamma_scale = ttk.Scale(main, from_=0.4, to=10.0, variable=gamma_val, orient=HORIZONTAL, command=gamma_correction, length=80).place(x=860, y=158)

    add_border = Label(main, text="Add border:", font="ariel 10 bold").place(x=630, y=185)
    thickness = [5, 10, 15, 20, 25, 30, 35, 40]
    border_choices = ttk.Combobox(main, values=thickness, font="ariel 5 bold")
    border_choices.bind("<<ComboboxSelected>>", image_border)
    border_choices.place(x=715, y=187)

    #  Creates and places "emboss" button
    emboss_button = Button(main, text="Emboss", font="ariel 10 bold", command=emboss_image).place(x=765, y=5)

    #  Creates and places "black and white" button
    b_and_w_button = Button(main, text="Black & White", font="ariel 10 bold", command=make_bw).place(x=835, y=5)

    #  Creates and places "min" button
    min_button = Button(main, text="Min", font="ariel 10 bold", command=min).place(x=790, y=85)

    #  Creates and places "max" button
    max_button = Button(main, text="Max", font="ariel 10 bold", command=max).place(x=835, y=85)

    #  Creates and places "contour" button
    contour_button = Button(main, text="Contour", font="ariel 10 bold", command=edge_contour).place(x=795, y=48)

    #  Creates and places "select image" button
    find_edges_button = Button(main, text="Find Edges", font="ariel 10 bold", command=get_edges).place(x=865, y=48)

    #  Creates and places "select image" button
    select_image_button = Button(main, text="Select Image", bg='black', fg='white', font='ariel 15 bold', command=selected).place(x=170, y=450)

    #  Creates and places "save" button
    save_image_button = Button(main, text="Save As..", bg='black', fg='white', font='ariel 15 bold', command=save).place(x=340, y=450)

    #  Creates and places "exit" button
    exit_button = Button(main, text="Exit", bg='red', fg='white', font='ariel 15 bold', command=main.destroy).place(x=30, y=450)

    #  Creates and places "reset" button
    reset_button = Button(main, text="Reset", bg='white', fg='red', font='ariel 15 bold', command=reset).place(x=530, y=450)

    # Creates and places "undo filter" button
    undo_button = Button(main, text="Undo filter", bg='white', fg='red', font='ariel 8 bold', command=undo, relief=RAISED).place(x=660, y=445)

    # Creates and places "undo filter" button
    lock_button = Button(main, text="Lock filter", bg='white', fg='red', font='ariel 8 bold', command=lock).place(x=740, y=445)

    #  Creates and places "do not click" button
    do_not_click_button = Button(main, text="Don't click..", bg='red', fg='white', font='ariel 7', command=spam_popup).place(x=885, y=470)

    #  Creates and places the help meny popup button
    help_button = Button(main, text='Help', bg='grey', fg='white', font='ariel 9', command=help).place(x=905, y=440)

