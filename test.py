import csv
import bcrypt


class Users:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.active = True
        self.password = None

    def user_info(self):
        print(
            f"Name: {self.name}\nPhone: {self.phone}\nEmail: {self.email}\nHashed Password: {self.password}\nActive: {self.active}"
        )

    def export_user(self):
        with open(f"{self.name}.csv", "w") as outfile:
            user_dictionary = {
                "name": self.name,
                "phone": self.phone,
                "email": self.email,
                "active": self.active,
            }
            csv_writer = csv.DictWriter(
                outfile, fieldnames=["name", "phone", "email", "active"]
            )
            csv_writer.writeheader()
            csv_writer.writerow(user_dictionary)
            print("Wrote User to CSV!")

    def change_password(self, password):
        # Get new password from user and then hash
        salt = bcrypt.gensalt()
        self.password = bcrypt.hashpw(password, salt)


john = Users("John Ipson", "970-867-5140", "john@devpipeline.com")
shawn = Users("Shawn", "444-222-1111", "shawn@coolguy.com")

john.user_info()

password = input("Type in a super secure password: ")
check_password = input("Type in the same password: ")

if password == check_password:
    password = password.encode()
    john.change_password(password)

john.user_info()
# my_user.export_user()


# new_user.user_info()
# new_user.export_user()
