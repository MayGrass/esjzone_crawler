import scrapy
from esjzone.items import EsjzoneItem


class RebuildworldSpider(scrapy.Spider):
    name = "RebuildWorld"
    allowed_domains = ["www.esjzone.cc"]

    def start_requests(self):
        yield scrapy.Request(
            "https://www.esjzone.cc/detail/1584158343.html", callback=self.parse_chapter_list
        )

    def parse_chapter_list(self, response):
        if response.status == 200:
            chapterList = response.css("div#chapterList *")  # 抓chapterList底下所有屬性
            parse_article_start = False
            for chapter in chapterList:
                if parse_article_start:
                    if a := chapter.css("a"):
                        yield scrapy.Request(
                            a.css("::attr(href)").get(),
                            callback=self.parse_article,
                            meta={"title": a.css("p *::text").get()},
                        )
                # 過標題WEB版後才是要開始抓到內容
                elif chapter.css("p::text").get() == "WEB版":
                    parse_article_start = True
        else:
            self.logger.error(f"{response.url=}, {response.status=}, Not 200!")

    def parse_article(self, response):
        if response.status == 200:
            item = EsjzoneItem()
            item["title"] = response.meta["title"]  # 標題
            item["content"] = response.css("div.forum-content p::text").getall()  # 內文
            yield item
        else:
            self.logger.error(f"{response.url=}, {response.status=}, Not 200!")
