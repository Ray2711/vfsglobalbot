import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vfs_main import vfs_checkdates

vfs_checkdates("https://visa.vfsglobal.com/kaz/en/ltu/login","Almaty","Astana","Лит Алм","Лит Аст")