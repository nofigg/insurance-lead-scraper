import os
import sys
import logging
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spider import InsuranceLeadSpider
from scraper.models import init_db
from datetime import datetime

def setup_directories():
    """Create necessary directories if they don't exist"""
    directories = [
        'data/leads',
        'logs',
        'config',
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def setup_logging():
    """Configure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('logs/scraper.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """Main entry point for the scraper"""
    try:
        # Setup
        setup_directories()
        setup_logging()
        logging.info("Starting insurance lead scraper...")

        # Initialize database
        init_db()
        logging.info("Database initialized")

        # Configure and start the scraper
        settings = get_project_settings()
        settings.set('ITEM_PIPELINES', {'scraper.pipelines.LeadPipeline': 300})
        
        process = CrawlerProcess(settings)
        process.crawl(InsuranceLeadSpider)
        process.start()

        logging.info("Scraping completed successfully")

    except Exception as e:
        logging.error(f"Error running scraper: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
