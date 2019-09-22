from tkinter import Tk, filedialog, Label, Frame
from PIL import ImageTk

class Dialog(Tk):
    def browsing_image(self):
        file_type_relation = (("png", "*.png"), ("jpeg", "*.jpg"))

        image_filename = filedialog.askopenfilename(
            initialdir='/', title='Selecione uma Imagem para a Postagem', filetype=file_type_relation)

        self.destroy()

        return image_filename

    def show_image(self, load):
        render = ImageTk.PhotoImage(load)

        image = Label(self, image=render)
        image.place(x=0, y=0)

        Frame(self)

        self.mainloop()