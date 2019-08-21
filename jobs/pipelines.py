# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class JobsPipeline(object):
    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='hhw7231562',
            db='pluralism',  # 数据库名
            charset='utf8'
        )
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql_3 = """
                                INSERT into position_secondary_area(area,first_level_id) VALUES(%s,%s) ON DUPLICATE KEY UPDATE area=%s
                                """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql_3, (item['area'], 1, item['area']))
        # 提交，不进行提交无法保存到数据库
        area_id = self.cursor.lastrowid
        if area_id == 0:
            m = self.cursor.execute("SELECT * FROM position_secondary_area where area=%s", item['area'])
            for r in self.cursor.fetchall():
                for j, i in zip(range(1), r):
                    area_id = i
        print(area_id)
        self.conn.commit()

        insert_sql = """
                        INSERT into position_sub_position(position) VALUES(%s) ON DUPLICATE KEY UPDATE position=%s
                        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (item['sort'], item['sort']))
        # 提交，不进行提交无法保存到数据库
        sort_id = self.cursor.lastrowid
        if sort_id == 0:
            m = self.cursor.execute("SELECT * FROM position_sub_position where position=%s", item['sort'])
            for r in self.cursor.fetchall():
                for j, i in zip(range(1), r):
                    sort_id = i
        print(sort_id)
        self.conn.commit()

        insert_sql2 = """
                                INSERT into position_companymodel(company,introduction) VALUES(%s,%s) ON DUPLICATE KEY UPDATE company=(%s)
                                """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql2, (item['company'],
                                         item['introduction'],
                                         item['company']))
        # 提交，不进行提交无法保存到数据库
        company_id = self.cursor.lastrowid
        if company_id == 0:
            m = self.cursor.execute("SELECT * FROM position_companymodel where company=%s", item['company'])
            for r in self.cursor.fetchall():
                for j, i in zip(range(1), r):
                    company_id = i
        print(company_id)
        self.conn.commit()

        insert_sql_1 = """
                                INSERT into position_positionmodel(title,wage,settlement,people,details,company_id,sort_id,area_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                                """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql_1, (item['title'],
                                           item['wage'],
                                           item['settlement'],
                                           item['people'],
                                           item['details'],
                                           company_id,
                                           sort_id,
                                           area_id))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

        return item

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()
