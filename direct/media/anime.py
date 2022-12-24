from util.html.parser import get_bs4, get_link_or_title
from util.network.http import HEADER_DEFAULT, rget


class kusonime:
    def __init__(self):
        self.__home = "https://kusonime.com"

    def home(self, number: int):
        if number > 0:
            url = f"{self.__home}/page/{number}"
        else:
            url = self.__home
        base = get_bs4(rget(url, headers=HEADER_DEFAULT).text)
        judul = get_link_or_title(
            base,
            tag="h2",
            multiple=True,
            args="#venkonten > div.vezone > div.venser > div > div.rseries > div.rapi > div.venz > ul > div:nth-child(n+1) > div > div.content > h2",
        )
        link = get_link_or_title(
            base,
            tag="a",
            attr="href",
            multiple=True,
            args="#venkonten > div.vezone > div.venser > div > div.rseries > div.rapi > div.venz > ul > div:nth-child(n+1) > div > div.content > h2",
        )
        waktu = get_link_or_title(
            base,
            tag="p",
            multiple=True,
            args="#venkonten > div.vezone > div.venser > div > div.rseries > div.rapi > div.venz > ul > div:nth-child(n+1) > div > div.content > p:nth-child(3)",
        )
        for i, time in enumerate(waktu):
            time = time.replace(
                "Released on ", "Dirilis Jam "
            )  # Replace "Released on" with "Dirilis Jam"
            time = time.split(" ")  # Split the string into two parts at the space
            time[3] = time[3].upper()
            waktu[i] = " ".join(time)
        genre = get_link_or_title(
            base,
            tag="p",
            multiple=True,
            args="#venkonten > div.vezone > div.venser > div > div.rseries > div.rapi > div.venz > ul > div:nth-child(n+1) > div > div.content > p:nth-child(4)",
        )
        genre = [i.replace("Genre", "").strip() for i in genre]
        data = {"judul": judul, "link": link, "release_time": waktu, "genre": genre}
        zipped_values = zip(
            data["judul"], data["link"], data["release_time"], data["genre"]
        )
        transformed_data = [
            {"judul": judul, "link": link, "release_time": release_time, "genre": genre}
            for judul, link, release_time, genre in zipped_values
        ]
        return transformed_data
