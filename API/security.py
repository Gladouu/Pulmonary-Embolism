import bcrypt
from sensitive_data import *

password = ADMIN_PWD
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)

password = DR_SHEPERD_PWD
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)

password = DR_SLOAN_PWD
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)

password = TEST_PWD
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
print(hashed_password)
