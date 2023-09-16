import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variable
db_uri = os.getenv("SQLALCHEMY_DATABASE_URI")

# Now you can use db_uri in your application
print(db_uri)
