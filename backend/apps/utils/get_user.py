from firebase_admin import auth

import django_backend.settings as settings
from firebase.firebase import FirebaseAdmin
from users.models import User


class GetUser:
    user = NotImplemented
    _is_admin = False

    def get_user(self, token):
        FirebaseAdmin(settings.FIREBASE_ADMIN_CONFIG, settings.FIREBASE_OPTIONS)
        
        if token != settings.ADMIN_TOKEN:
            user = auth.verify_id_token(token)
        else:
            self._is_admin = True
            user = {
                'uid': '1337',
            }
            
        self.user, _ = User.objects.get_or_create(firebase_id=user['uid'])

    @property
    def is_admin(self):
        return self._is_admin
