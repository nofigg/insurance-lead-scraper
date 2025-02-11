import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import datetime
import yaml
import json
from typing import Dict, Any
from fake_useragent import UserAgent
import logging

class InsuranceLeadSpider(CrawlSpider):
    name = 'insurance_leads'
    
    def __init__(self, *args, **kwargs):
        super(InsuranceLeadSpider, self).__init__(*args, **kwargs)
        self.load_config()
        self.ua = UserAgent()
        self.setup_logging()

    def load_config(self):
        with open('config/sources.yaml', 'r') as f:
            self.config = yaml.safe_load(f)
        
        # Set up the allowed domains and start URLs from config
        self.allowed_domains = []
        self.start_urls = []
        for source in self.config['sources']:
            if source['enabled']:
                domain = source['url_pattern'].split('/')[2]
                self.allowed_domains.append(domain)
                self.start_urls.append(source['url_pattern'])

    def setup_logging(self):
        logging.basicConfig(
            filename=self.config['settings']['logging']['file'],
            level=getattr(logging, self.config['settings']['logging']['level']),
            format='%(asctime)s [%(levelname)s] %(message)s'
        )

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url=url,
                headers={'User-Agent': self.ua.random},
                callback=self.parse_lead,
                meta={'proxy': self.get_proxy()} if self.config['settings']['proxy']['enabled'] else {}
            )

    def get_proxy(self) -> str:
        # Implement proxy rotation logic here
        return None  # Placeholder

    def parse_lead(self, response):
        for source in self.config['sources']:
            if source['url_pattern'] in response.url:
                rules = source['scrape_rules']
                for rule in rules:
                    for item in response.css(rule['selector']):
                        lead = {}
                        for field, selector in rule['fields'].items():
                            lead[field] = item.css(selector + '::text').get()
                        
                        if self.is_valid_lead(lead):
                            lead['source'] = source['name']
                            lead['timestamp'] = datetime.now().isoformat()
                            lead['url'] = response.url
                            yield self.process_lead(lead)

    def is_valid_lead(self, lead: Dict[str, Any]) -> bool:
        # Implement lead validation logic
        required_fields = ['name', 'location']
        return all(lead.get(field) for field in required_fields)

    def process_lead(self, lead: Dict[str, Any]) -> Dict[str, Any]:
        # Enrich lead data
        lead['quality_score'] = self.calculate_quality_score(lead)
        lead['processed'] = True
        return lead

    def calculate_quality_score(self, lead: Dict[str, Any]) -> float:
        # Implement lead scoring logic
        score = 0.0
        # Add scoring logic based on various factors
        return score

    def closed(self, reason):
        # Cleanup and final processing
        logging.info(f"Spider closed: {reason}")

# Additional helper functions
def clean_text(text: str) -> str:
    if text:
        return ' '.join(text.strip().split())
    return ''
