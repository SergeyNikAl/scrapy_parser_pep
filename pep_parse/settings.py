from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RESULT_DIR = 'result'

BOT_NAME = 'pep_parse'

PEP_DOMAIN = 'peps.python.org'
ALLOWED_DOMAINS = [PEP_DOMAIN, ]
URLS = [f'https://{PEP_DOMAIN}/']

SPIDER_MODULES = ['pep_parse.spiders']

ROBOTSTXT_OBEY = True

FEEDS = {
    f'{RESULT_DIR}/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True,
    }
}

ITEM_PIPELINES = {
    f'{BOT_NAME}.pipelines.PepParsePipeline': 300,
}
