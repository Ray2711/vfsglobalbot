  
from waitlist_check import vfs_checkdates
from dotenv import load_dotenv
import os
load_dotenv()
EMAIL = os.getenv("WAITLIST1_EMAIL")
vfs_checkdates("https://visa.vfsglobal.com/kaz/en/fra/login","Фра Аст", False, EMAIL, "XYZ22680919682")