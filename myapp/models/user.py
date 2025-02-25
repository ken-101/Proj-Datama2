from flask_login import UserMixin
from myapp import login_manager

class User(UserMixin):
    def __init__(self, id, email, user_type, name=None):
        self.id = id
        self.email = email
        self.user_type = user_type  # 'buyer' or 'seller'
        self.name = name

    @staticmethod
    def get_by_id(supabase, user_id):
        response = supabase.table('users').select('*').eq('id', user_id).execute()
        if response.data:
            user_data = response.data[0]
            return User(
                id=user_data['id'],
                email=user_data['email'],
                user_type=user_data['user_type'],
                name=user_data.get('name')
            )
        return None

@login_manager.user_loader
def load_user(user_id):
    from flask import current_app
    from supabase import create_client
    
    supabase = create_client(
        current_app.config['SUPABASE_URL'],
        current_app.config['SUPABASE_KEY']
    )
    
    return User.get_by_id(supabase, user_id)