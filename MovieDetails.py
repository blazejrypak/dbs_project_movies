from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup

driver = webdriver.Firefox()


class MovieDetails:
    def __init__(self):
        self.base_url = "https://www.csfd.cz/"
        self.url = "film/10135-forrest-gump/prehled/"

    def get_soup(self, page_source):
        return BeautifulSoup(driver.page_source, "html5lib")

    def get_poster(self, main_content):
        img = main_content.find('img')
        img_url = img['src']
        return img_url[2:]

    def get_name(self, li):
        if li.find('img') is None:
            return None
        else:
            return {
                "lang": li.find('img')['title'],
                "title": li.find('h3').text
            }

    def get_names(self, info):
        names = info.find("ul", {"class": "names"})
        all_names = []
        for li in names.findAll('li'):
            title = self.get_name(li)
            if title is not None:
                all_names.append(self.get_name(li))
        return all_names

    def get_genres(self, info):
        genres_obj = info.find("p", {"class": "genre"})
        return str(genres_obj.text).split(' / ')

    # TODO, make directory from it
    def get_origin(self, info):
        origin_obj = info.find("p", {"class": "origin"})
        # print(origin_obj.text)

    def parse_creators_item(self, div):
        role_type = div.find('h4').text
        url_names = div.findAll('a')
        names = []
        for url in url_names:
            names.append({
                "url": url['href'],
                "person_name": url.text
            })
        return {
            "type": str(role_type).rstrip(":"),
            "names": names
        }

    def get_creators(self, info):
        creators_obj = info.find("div", {"class": "creators"})
        divs = creators_obj.findAll("div")
        creators = []
        for div in divs:
            creators.append(self.parse_creators_item(div))
        return creators

    def get_rating(self, sidebar):
        return {
            "rating": str(sidebar.find("h2", {"class": "average"}).text).rstrip('%')
        }

    def get_plot(self, main):
        plot_obj = main.find("div", {"id": "plots"})
        content = plot_obj.find("div", {"class": "content"})
        # display_block = content.find("div", {"style": "display: block;"})
        display_block = content.find("ul")
        return {
            "plot": str(display_block.text).strip('\n\t')
        }

    def get_tags(self, sidebar):
        related_tags_obj = sidebar.find("div", {"class": "ct-related tags"})
        content = related_tags_obj.find("div", {"class": "content"})
        url_tags = content.findAll('a')
        tags = []
        for url in url_tags:
            tags.append({
                "url": url['href'],
                "name": url.text
            })
        return tags

    def get_reviews(self, soup):
        pass

    def get_data(self, url):
        driver.get(self.base_url + url)
        assert "ČSFD.cz" in driver.title
        soup = self.get_soup(driver.page_source)
        page_content = soup.find("div", {"class": "page-content"})
        main_content = page_content.find("div", {"class": "content"})
        info = main_content.find("div", {"class": "info"})
        try:
            # print(self.get_poster(main_content))
            # print(self.get_names(info))
            # print(self.get_genres(info))
            # print(self.get_origin(info))
            # print(self.get_creators(info))
            # print(self.get_rating(soup))
            # print(self.get_plot(soup))
            print(self.get_tags(soup))
        except TypeError:
            driver.close()

# poster = main_content.find("div", {"class": "image"})
# info = main_content.find("div", {"class": "info"})
# names = info.find("ul", {"class": "names"})
# genre = info.find("p", {"class": "genre"})
# origin = info.find("p", {"class": "origin"})
# creators = info.find("div", {"class": "creators"})
# print(poster, names, genre, origin, creators)


movieDetails = MovieDetails()
movieDetails.get_data(movieDetails.url)
driver.close()
