from typing import Dict, Any
from datetime import datetime
import json
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Lead, db_engine
import logging

class LeadPipeline:
    def __init__(self):
        self.Session = sessionmaker(bind=db_engine)
        self.leads_processed = 0
        self.setup_logging()

    def setup_logging(self):
        self.logger = logging.getLogger('LeadPipeline')
        self.logger.setLevel(logging.INFO)

    def process_item(self, item: Dict[str, Any], spider) -> Dict[str, Any]:
        """Process each lead item through the pipeline"""
        try:
            # Clean and validate data
            cleaned_item = self.clean_item(item)
            if not self.validate_item(cleaned_item):
                self.logger.warning(f"Invalid lead item: {item}")
                return None

            # Enrich data
            enriched_item = self.enrich_item(cleaned_item)

            # Score the lead
            scored_item = self.score_lead(enriched_item)

            # Save to database
            self.save_to_database(scored_item)

            # Export to file
            self.export_lead(scored_item)

            self.leads_processed += 1
            return scored_item

        except Exception as e:
            self.logger.error(f"Error processing item: {str(e)}")
            return None

    def clean_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Clean and standardize the lead data"""
        cleaned = {}
        for key, value in item.items():
            if isinstance(value, str):
                cleaned[key] = value.strip()
            else:
                cleaned[key] = value
        return cleaned

    def validate_item(self, item: Dict[str, Any]) -> bool:
        """Validate the lead data"""
        required_fields = ['name', 'source']
        return all(item.get(field) for field in required_fields)

    def enrich_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich the lead with additional data"""
        item['processed_at'] = datetime.now().isoformat()
        # Add additional enrichment logic here
        return item

    def score_lead(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate a quality score for the lead"""
        score = 0
        factors = {
            'has_phone': 2,
            'has_email': 2,
            'has_location': 1,
            'has_profession': 1
        }
        
        for factor, weight in factors.items():
            field = factor.replace('has_', '')
            if item.get(field):
                score += weight

        item['quality_score'] = min(score * 10, 100)  # Scale to 0-100
        return item

    def save_to_database(self, item: Dict[str, Any]) -> None:
        """Save the lead to the database"""
        session = self.Session()
        try:
            lead = Lead(
                name=item['name'],
                source=item['source'],
                quality_score=item['quality_score'],
                raw_data=json.dumps(item),
                created_at=datetime.now()
            )
            session.add(lead)
            session.commit()
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            session.rollback()
        finally:
            session.close()

    def export_lead(self, item: Dict[str, Any]) -> None:
        """Export the lead to various formats"""
        timestamp = datetime.now().strftime('%Y%m%d')
        
        # Export to CSV
        df = pd.DataFrame([item])
        df.to_csv(f'data/leads/{timestamp}_leads.csv', 
                 mode='a', 
                 header=not pd.io.common.file_exists(f'data/leads/{timestamp}_leads.csv'),
                 index=False)
        
        # Export to JSON
        with open(f'data/leads/{timestamp}_leads.json', 'a') as f:
            json.dump(item, f)
            f.write('\n')

    def close_spider(self, spider):
        """Cleanup when spider closes"""
        self.logger.info(f"Pipeline finished. Processed {self.leads_processed} leads.")
