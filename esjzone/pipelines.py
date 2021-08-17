# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class TxtPipeline:
    def process_item(self, item, spider):
        with open(f"txt/{item['title']}.txt", "w") as f:
            f.write(item["title"] + "\n")
            for content in item["content"]:
                f.write(content + "\n")
        return item
