class Notification:
    def __init__(self, notification_as_list):
        if notification_as_list:
            self.id_notification = notification_as_list[0]
            self.date = notification_as_list[1]
            self.type = notification_as_list[2]

            self.id_perfil = notification_as_list[3]

            self.id_follow_follower = notification_as_list[4]
            self.id_follow_followed = notification_as_list[5]

            self.id_postmarkup_perfil = notification_as_list[6]
            self.id_postmarkup_post = notification_as_list[7]

            self.id_commentarymarkup_perfil = notification_as_list[8]
            self.id_commentarymarkup_commentary = notification_as_list[9]
