import csv

# This script processes leads from leads.csv and assigns a tier based on specified criteria.

def assign_tier(lead):
    score = 0
    try:
        income = float(lead.get("income", 0))
    except ValueError:
        income = 0
    if income >= 80000:
        score += 3
    elif income >= 50000:
        score += 2
    else:
        score += 1

    try:
        engagement = float(lead.get("engagement_score", 0))
    except ValueError:
        engagement = 0
    if engagement >= 7:
        score += 3
    elif engagement >= 4:
        score += 2
    else:
        score += 1

    life_event = lead.get("life_event", "").lower()
    if life_event in ["new baby", "home purchase", "marriage"]:
        score += 3

    if score >= 8:
        return "hot"
    elif score >= 5:
        return "medium"
    else:
        return "warm"

def process_leads(csv_file_path):
    leads_with_tiers = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row["lead_tier"] = assign_tier(row)
            leads_with_tiers.append(row)
    return leads_with_tiers

def print_leads(leads):
    headers = list(leads[0].keys()) if leads else []
    print("\t".join(headers))
    for lead in leads:
        print("\t".join([str(lead.get(header, "")) for header in headers]))

if __name__ == "__main__":
    csv_path = "leads.csv"
    leads = process_leads(csv_path)
    print_leads(leads)
