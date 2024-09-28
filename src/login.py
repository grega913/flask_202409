def valid_login(username, password):
    # Replace this with your actual database query or authentication logic
    # For simplicity, let's assume we have a list of valid users and passwords
    valid_users = [('user1', 'password1'), ('user2', 'password2')]
    for user, pw in valid_users:
        if username == user and password == pw:
            return True
    return False

def log_the_user_in(username):
    # Replace this with your actual user session management logic
    # For simplicity, let's just print a success message
    print(f"User {username} logged in successfully!")
    return "You are now logged in!"