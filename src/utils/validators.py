from typing import List, Dict, Any


def validate_leads_structure(leads: List[Dict[str, Any]]) -> bool:
    """Validate that leads have required fields"""
    if not isinstance(leads, list):
        return False
    
    required_fields = ['company', 'description']
    for lead in leads:
        if not isinstance(lead, dict):
            return False
        if not all(field in lead for field in required_fields):
            return False
    return True


def validate_emails_structure(emails: List[Dict[str, Any]]) -> bool:
    """Validate that emails have required fields"""
    if not isinstance(emails, list):
        return False
    
    required_fields = ['company', 'email']
    for email in emails:
        if not isinstance(email, dict):
            return False
        if not all(field in email for field in required_fields):
            return False
    return True
