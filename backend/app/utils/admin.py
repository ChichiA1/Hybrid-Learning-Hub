class Admin:
    def __init__(self, admin_id, full_name, email, phone, password):
        self.admin_id = admin_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.password = password

    def __str__(self):
        return f"Admin ID: {self.admin_id}, Name: {self.full_name}, Email: {self.email}, Phone: {self.phone}"