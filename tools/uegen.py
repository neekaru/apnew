import random
import secrets
from fake_useragent import UserAgent


class User_Agent:
    def __init__(self):
        return

    def uegen(
        self,
        *,
        default: bool | None = False,
        mobile: bool | None = False,
        random: bool | None = False,
        alter: bool | None = False,
        spesific: list[str] | None = None
    ):
        if default:
            return self.GetRandomUserAgent()
        elif mobile:
            return self.GenerateMobileUseragent()

        if random:
            ua = UserAgent(
                browsers=["firefox", "edge", "safari", "chrome"],
                use_external_data=False,
            )
            return ua.random
        elif alter:
            ua = UserAgent(browsers=["edge", "chrome"])
            return ua.random

        if spesific is None:
            specific = []
        elif specific:
            ua1 = UserAgent(browsers=[specific])
            return ua1.random
        return ""

    def GenerateMobileUseragent(self) -> str:
        version = random.randint(86, 109)
        patch = random.randint(4240, 5414)
        build = random.randint(54, 213)
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
            "(Linux; Android 10; JNY-LX1; HMSCore 6.3.0.326)",
            "(Linux; Android 10; FRL-L23; HMSCore 5.2.0.318; GMSCore 21.12.12)",
            "(Linux; Android 6.0.1; Redmi 4A Build/MMB29M)",
            "(Linux; U; Android 9; ru-ru; Redmi 7A Build/PKQ1.190319.001)",
            "(Linux; Android 8.1.0; Redmi Go)",
            "(Linux; Android 8.0.0; moto g(6) play Build/OPP27.91-87)",
            "(Linux; Android 10; moto g(7) Build/QPUS30.52-16-2-13)",
            "(Linux; Android 9; moto g(7) play)",
        )
        device = secrets.choice(MOBILE_STRINGS)
        chrome = f"Mozilla/5.0 {device} AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{version}.0.{patch}.{build} Mobile Safari/537.36"

        android = random.randint(9, 13)
        firefox = f"Mozilla/5.0 (Android {android}; Mobile; rv:68.0) Gecko/68.0 Firefox/{version}.0"

        return random.choice([chrome, firefox])

    def GetRandomUserAgent(self) -> str:
        browserType = ["firefox", "chrome", "opera", "edge"]
        OS = [
            "Windows NT 10.0; Win64; x64",
            "X11; Linux x86_64",
            "Macintosh; Intel Mac OS X 12_5",
        ]

        OSsystem = secrets.choice(OS)
        version = random.randint(81, 109)
        randomBrowser = random.choice(browserType)
        browserTemplate = "Mozilla/5.0 ({0}; rv:{1}.0) Gecko/20100101 Firefox/{1}.0"
        finalVersion = version

        if randomBrowser in ["chrome", "opera", "edge"]:
            patch = random.randint(4950, 5414)
            build = random.randint(72, 284)
            browserTemplate = "Mozilla/5.0 ({0}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{1} Safari/537.36"
            finalVersion = f"{version}.0.{patch}.{build}"

        if randomBrowser == "opera":
            version = random.randint(80, 94)
            patch = random.randint(3500, 4616)
            build = random.randint(26, 238)
            browserTemplate += f" OPR/{version}.0.{patch}.{build}"

        elif randomBrowser == "edge":
            patch = random.randint(800, 1518)
            build = random.randint(40, 100)
            browserTemplate += f" Edg/{version}.0.{patch}.{build}"

        userAgent = browserTemplate.format(OSsystem, finalVersion)

        return userAgent
