# unused code

# import re

# from ..util.captcha import RecaptchaV3
# from ..util.encrypt import base64decode, decrypt_url
# from ..util.utils import fix_url, rget, rpost


# # adfly bypass
# def adfly(url):
#     res = rget(url, is_cf=True).text
#     out = {"error": False, "src_url": url}
#     try:
#         ysmm = re.findall("ysmm\s+=\s+['|\"](.*?)['|\"]", res)[0]
#     except:
#         out["error"] = True
#         return out
#     url = decrypt_url(ysmm)
#     if re.search(r"go\.php\?u\=", url):
#         url = base64decode(re.sub(r"(.*?)u=", "", url)).decode()
#     elif "&dest=" in url:
#         url = fix_url(re.sub(r"(.*?)dest=", "", url), unquote=True)
#     out["bypassed_url"] = url
#     return out


# print(adfly("http://lyksoomu.com/aQJ2"))
