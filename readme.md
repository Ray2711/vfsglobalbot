# VFS CHECK DATES BOT
bot to check dates on a VFS website using seleniumbase. Requires GUI to bypass cloudflare checks. Sends closest dates to TG groupchat using TG Bot API
# USAGE
`python -m pip install seleniumbase dotenv requests`
`python vfs_...`
Checks Almaty and Astana
# EXPLANATION
```
vfs_checkdates("https://visa.vfsglobal.com/kaz/en/fra/login","Almaty","Astana","Фра Алм","Фра Аст")
```
The script checks for two cities (TODO rewrite city args as an array) and sends closest available date(if available) to TG chat. abbreviations example: for Visa center of France in Moscow, write "Fra Msk" (XXX YYY)