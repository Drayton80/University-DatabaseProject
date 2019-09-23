import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.entities.Commentary import Commentary
from model.entities.Post import Post
from model.entities.Topic import Topic

from view.View import UserView
from view.Dialog import Dialog
from view.InputField import InputField
from view.ViewPartition import ViewPartition


class PostCreate(UserView):
    def run(self):
        self.show()

    def show(self, information_message=None):
        ViewPartition().border_logo()

        print("Gostaria de adicionar uma imagem à Postagem? Digite: \n" ,
              "S - Para sim                                         \n" , 
              "N - Para não                                           " )

        image_add_choice = InputField().show('>>')

        if image_add_choice and image_add_choice.upper() == "S":
            image_path = Dialog().browsing_image()
        else:
            image_path = None
        
        if not image_path or image_path.isspace() or not image_add_choice.upper() == "S":
            image_message_text = "Nenhuma imagem escolhida"
        else:
            image_message_text = image_path

        ViewPartition().border_logo()

        print("Imagem da Postagem>>", image_message_text)
        text = InputField().show('Texto da Postagem>>', show_divisory=False)

        if not image_add_choice and not text:
            return None
        
        post = Post.create_instance(text, image_path, self.logged_user)


class CommentaryCreate(UserView):
    def run(self):
        self.show()

    def show(self, information_message=None):
        ViewPartition().border_logo()
        
        if self.displayed_post:
            print(self.displayed_post)
            ViewPartition().border_divisory()

        text = InputField().show('Texto do Comentário>>', show_divisory=False)

        if self._is_empty_field(text):
            return None
        else:
            Commentary.create_instance(self.displayed_post, text, self.logged_user)

        