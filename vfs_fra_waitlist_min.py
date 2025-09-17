  
from waitlist_check import vfs_checkdates
from dotenv import load_dotenv
import os
load_dotenv()
EMAIL = os.getenv("WAITLIST2_EMAIL")
vfs_checkdates("https://visa.vfsglobal.com/kaz/en/fra/login","Фра Алм", False, EMAIL, "XYZ22687824985")