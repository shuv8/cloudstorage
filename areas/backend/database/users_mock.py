class UserMock:
    users = {
        "test_mail@mail.com": {
            "email": "test_mail@mail.com",
            "password": "password",
            "username": "username",
        },
        "test1_mail@mail.com": {
            "email": "test1_mail@mail.com",
            "password": "password1",
            "username": "username1",
        },
        "test2_mail@mail.com": {
            "email": "test2_mail@mail.com",
            "password": "password2",
            "username": "username2",
        }
    }

    def query_by_email(self, query: str):
        return self.users[query]
