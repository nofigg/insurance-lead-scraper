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

## License

MIT License - See LICENSE file for details
