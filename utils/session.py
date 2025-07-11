class SessionManager:
    def __init__(self, session):
        self.session = session

    def login(self, username, role):
        self.session.logged_in = True
        self.session.username = username
        self.session.role = role

    def logout(self):
        self.session.logged_in = False
        self.session.username = ""
        self.session.role = ""

    def is_admin(self):
        return self.session.role == "admin"