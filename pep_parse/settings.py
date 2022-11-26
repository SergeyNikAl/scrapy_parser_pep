from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

BOT_NAME = 'pep_parse'

ALLOWED_DOMAINS = ['peps.python.org', ]
URL = ['https://peps.python.org/']

SPIDER_MODULES = ['pep_parse.spiders']

ROBOTSTXT_OBEY = True

FEEDS = {
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True,
    }
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.PepParsePipeline': 300,
}
