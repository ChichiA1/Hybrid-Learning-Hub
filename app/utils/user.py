class User:
    def __init__(self, user_id, full_name, email, phone, address, user_type, dob, membership_status="Active"):
        self.user_id = user_id
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.address = address
        self.user_type = user_type
        self.dob = dob
        self.membership_status = membership_status

    def __str__(self):
        return (f"User ID: {self.user_id}, Name: {self.full_name}, Email: {self.email}, Phone: {self.phone}, "
                f"Address: {self.address}, User Type: {self.user_type}, Date of Birth: {self.dob}, "
                f"Membership Status: {self.membership_status}")