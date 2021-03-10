# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import django


class SectorPipeline(object):
    def process_item(self, item, spider):
        try:
            item.save()
        except django.db.utils.IntegrityError as exc:
            if "UNIQUE constraint failed" in str(exc):
                item.update()
            else:
                raise exc
        return item
