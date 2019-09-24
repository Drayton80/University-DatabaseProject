import os
import sys

sys.path.append(os.path.abspath(os.path.join('..')))

from model.entities.User import User
from model.entities.Post import Post
from model.entities.Commentary import Commentary
from model.entities.Notification import Notification
from model.relationships.Follow import Follow

from view.View import UserView
from view.InputField import InputField
from view.ViewPartition import ViewPartition
from view.Create import CommentaryCreate
from view.List import List
from view.Dialog import Dialog

class NotificationView(UserView):
    def run(self):
        displayed_notifications = self.logged_user.get_user_notifications()
        selected_notification_index = self._filter_selected_index(self._show_notifications_list(displayed_notifications))
        
        while True:
            if self._is_empty_field(selected_notification_index):
                return None
            
            elif self._is_value_a_number(selected_notification_index) and ( 
                not self._is_out_of_bounds(selected_notification_index, len(displayed_notifications))):
                returned_information = self._show_selected_notification(displayed_notifications[selected_notification_index])
                
                if returned_information:
                    return returned_information
                else:
                    selected_notification_index = self._filter_selected_index(self._show_notifications_list(displayed_notifications))

            else:
                selected_notification_index = self._filter_selected_index(self._show_notifications_list(displayed_notifications, information_message='Escolha Inválida'))
                       
    def _show_notifications_list(self, notifications_list, information_message=None):
        ViewPartition().border_logo()
        print("Central de Notificações")
        ViewPartition().border_divisory()
        
        if_list_is_empty_message = 'Você não possui Notificações'

        List(notifications_list, 
            if_list_is_empty_message=if_list_is_empty_message, 
            separator='\n', index_left_list_element=False, word_before_index='Notificação ').run()

        ViewPartition().border_divisory()

        if notifications_list:
            print('Caso deseje acessar alguma Notificação, selecione ela pelo número acima dela')
        print("(Caso deseje retornar, deixe o campo em branco)")

        ViewPartition().border_information_message(information_message)

        return self._filter_selected_value(InputField().show('>>'))

    def _show_selected_notification(self, notification, information_message=None):
        ViewPartition().border_logo()
        print(notification)
        ViewPartition().border_divisory()
        
        if notification.notification_type == 'follow':
            if self.logged_user.privacy:
                print("Você aceitará o pedido dele?: \n" ,
                        "S - Para sim                \n" , 
                        "N - Para não                  " )

                choice = self._filter_selected_value(InputField().show('>>'))

                if choice not in ['S', 'N']:
                    return None

                follow_relationship = Follow.get_follow_instance(notification.id_follow_follower, notification.id_follow_followed)
                follow_relationship.set_confirmation(True if choice == 'S' else False)
                Notification.delete_instance(notification.notification_id)

                return {'command': 'access_user', 'object': User.get_user_instance(notification.id_follow_follower)}
            else:
                return {'command': 'access_user', 'object': User.get_user_instance(notification.id_follow_follower)}
            
        elif notification.notification_type == 'post markup':
            return {'command': 'access_post', 'object': Post.get_post_instance(notification.id_postmarkup_post)}

        elif notification.notification_type == 'commentary markup':
            commentary = Commentary.get_commentary_instance(notification.id_commentarymarkup_commentary)
            post = Post.get_post_instance(commentary.post_id)

            return {'command': 'access_post', 'object': post}
        
        else:
            return None


