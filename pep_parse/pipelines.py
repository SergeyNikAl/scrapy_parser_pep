import csv
from collections import defaultdict
from datetime import datetime as dt
import os

import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, Session

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEADERS_PEP_TABLE = ('Статус', 'Количество')
TIME_FORMAT = '%Y-%m-%dT%H-%M-%S'
TOTAL_STATUSES = 'Total'

Base = declarative_base()


class Pep(Base):
    __tablename__ = 'pep'
    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    name = Column(String(200))
    status = Column(String(50))


class PepParsePipeline:
    status_count = defaultdict(int)
    total = 0

    def open_spider(self, spider):
        engine = create_engine('sqlite:///posts.db')
        Base.metadata.create_all(engine)
        self.session = Session(engine)

    def process_item(self, item, spider):
        pep = Pep(
            number=item['number'],
            name=item['name'],
            status=item['status'],
        )
        if not self.session.query(Pep).filter(Pep.number == pep.number).all():
            self.session.add(pep)
            self.session.commit()
        if item.get('status'):
            self.total += 1
            self.status_count[
                item['status']
            ] = self.status_count.get(item['status'], 0) + 1
        return item

    def close_spider(self, spider):
        filename = os.path.join(
            BASE_DIR,
            'results',
            f'status_summary_{dt.now().strftime(TIME_FORMAT)}.csv'
        )
        results = [HEADERS_PEP_TABLE]
        results.extend(self.status_count.items())
        results.append((TOTAL_STATUSES, self.total))
        with open(filename, mode='w', encoding='utf-8') as file:
            sqlalchemy.select([
                Pep.status,
                sqlalchemy.func.count(Pep.status).label('status_count')
            ]).group_by(Pep.status)
            writer = csv.writer(file)
            writer.writerows(results)
        self.session.close()
