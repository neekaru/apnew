# -*- coding: utf-8 -*-
#
# https://github.com/ewwink/Real-Fake-Random-User-Agent/
#

import random

def GetRandomUserAgent():
    browserType = ["firefox", "chrome", "opera", "edge"]
    OS = ["Windows NT 10.0; Win64; x64", "X11; Linux x86_64", "Macintosh; Intel Mac OS X 12_5"]

    OSsystem = OS[random.randint(0, len(OS)-1)]
    version = random.randint(81, 108)
    randomBrowser = browserType[random.randint(0, len(browserType)-1)]
    browserTemplate = "Mozilla/5.0 ({0}; rv:{1}.0) Gecko/20100101 Firefox/{1}.0"
    finalVersion = version

    if randomBrowser in ["chrome", "opera", "edge"]:
        patch = random.randint(4950, 5359)
        build = random.randint(72, 212)
        browserTemplate = "Mozilla/5.0 ({0}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{1} Safari/537.36"
        finalVersion = f"{version}.0.{patch}.{build}"

        if randomBrowser == "opera":
            version = random.randint(80, 94)
            patch = random.randint(3500, 4606)
            build = random.randint(26, 212)
            browserTemplate += f" OPR/{version}.0.{patch}.{build}"
        elif randomBrowser == "edge":
            patch = random.randint(800, 1462)
            build = random.randint(40, 99)
            browserTemplate += f" Edg/{version}.0.{patch}.{build}"
        
    userAgent = browserTemplate.format(OSsystem, finalVersion)

    return userAgent

def GenerateMobileUseragent():
    """
    Reference: https://github.com/vypivshiy/ani-cli-ru/blob/0201a56786972fdc3e92725f4c58f60451bcb25c/anicli_ru/utils/random_agent.py
    """
    version = random.randint(86, 107)
    patch = random.randint(4240, 5304)
    build = random.randint(54, 212)
    MOBILE_STRINGS = (
    "(Linux; Android 6.0; Nexus 5)",
    "(Linux; Android 7.0; Redmi Note 7 Pro)",
    "(Linux; Android 8.1.0; Redmi Note 8 Pro)",
    "(Linux; Android 9.0.0; Redmi Note 9 Pro)",
    "(Linux; Android 6.0; SM-A710F)",
    "(Linux; Android 6.0; SAMSUNG SM-C9000)",
    "(Linux; Android 13; LM-Q720)",
    "(Linux; Android 13; SM-N960U)",
    "(Linux; Android 13; SM-G960U)",
    "(Linux; Android 7.0; SM-G610M Build/NRD90M)",
    "(Linux; Android 6.0; vivo 1713 Build/MRA58K)",
    "(Linux; Android 7.1; Mi A1 Build/N2G47H)",
    )
    device = random.choice(MOBILE_STRINGS)
    baseline = f"Mozilla/5.0 {device} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{patch}.{build} Mobile Safari/537.36"
    return baseline