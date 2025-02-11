# Insurance Lead Generation Scraper

A sophisticated web scraping solution for generating and organizing life insurance leads. This project implements ethical web scraping practices and includes data processing capabilities for lead qualification.

## Features

- Multi-threaded web scraping engine
- Data validation and cleaning
- Lead scoring system
- Export capabilities (CSV, Excel, JSON)
- Proxy rotation support
- Rate limiting and respectful crawling
- Data deduplication
- Automated lead qualification

## Tech Stack

- Python 3.9+
- Scrapy (Web scraping framework)
- SQLAlchemy (Database ORM)
- PostgreSQL (Data storage)
- Celery (Task queue)
- Redis (Caching/Queue backend)
- FastAPI (REST API)
- Vue.js (Frontend dashboard)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/insurance-lead-scraper.git
cd insurance-lead-scraper
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

1. Configure target sources in `config/sources.yaml`
2. Start the scraping engine:
```bash
python run.py
```

3. Access the dashboard at `http://localhost:8000`

## Ethical Guidelines

- Respect robots.txt
- Implement rate limiting
- Honor website terms of service
- Store only public information
- Implement data retention policies
- Regular data accuracy verification

## Monitoring Updates

To dynamically monitor public directories for updates, you can use the following Windsurf command:

```bash
windsurf \
  --targets "https://www.epcounty.com/directory.htm,https://elpaso.businesslistus.com,https://members.elpaso.org/active-member-directory,https://www.buyep.org/directory/,https://www.elpasodirectory.org/" \
  --scrape-mode "public" \
  --output-format "csv" \
  --output-file "leads.csv" \
  --fields "source,full_name,email,phone,address,city,state,zip,age,gender,marital_status,employment,income,engagement_score,life_event" \
  --append-output true \
  --monitor true \
  --monitor-interval 3600 \
  --change-detection "pattern,frequency" \
  --post-scrape-command "python3 tier_leads.py"
```

### Breaking It Down:
- **--targets**: Specifies the URLs of the directories to scrape.
- **--scrape-mode "public"**: Ensures that only publicly available data is scraped.
- **--output-format "csv" & --output-file "leads.csv"**: Directs the scraped data into a CSV file (which you can continuously append to).
- **--fields**: Lists the data points (columns) you’re collecting—this ensures your CSV is structured and legible.
- **--append-output true**: Tells Windsurf to add new records to the existing CSV so that your file keeps growing.
- **--monitor true & --monitor-interval 3600**: Instructs Windsurf to check the target directories every 3600 seconds (or one hour) for any changes.
- **--change-detection "pattern,frequency"**: Enables Windsurf to recognize when the directory layout or data update rate changes, thereby triggering an automatic re-scrape.
- **--post-scrape-command "python3 tier_leads.py"**: After each scrape, Windsurf runs your Python script to process the CSV file—assigning tiers based on your criteria.

This command automates your workflow end-to-end, from detecting updates on the directories to processing and categorizing your leads.

## Updating the README

As the project grows, the README file will be updated to reflect significant changes, including:
- New features and functionalities
- Changes in installation or usage instructions
- Updates to the tech stack or dependencies
- Contribution guidelines and project status

It is important to keep this document current to provide clear guidance to users and contributors.

## License

MIT License - See LICENSE file for details
