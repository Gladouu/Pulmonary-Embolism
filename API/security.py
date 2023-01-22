import bcrypt
import os

required_envs = ['ADMIN_PWD', 'DR_SHEPERD_PWD', 'DR_SLOAN_PWD', 'TEST_PWD']

for env in required_envs:
    if env not in os.environ:
        raise ValueError(f"{env} env var is not set.")


password = os.environ("ADMIN_PWD")
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)

password = os.environ("DR_SHEPERD_PWD")
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)

password = os.environ("DR_SLOAN_PWD")
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)

password = os.environ("TEST_PWD")
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)
