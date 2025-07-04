import json
import re
from typing import Optional, List, Dict, Any


def extract_json_from_text(text: str) -> Optional[List[Dict[str, Any]]]:
    """Extract JSON from text that might contain other content"""
    # Remove common markdown code block markers
    text = re.sub(r'```json\n?', '', text)
    text = re.sub(r'```\n?', '', text)
    
    # Look for JSON array pattern (more permissive)
    json_patterns = [
        r'\[[\s\S]*?\]',  # Array pattern (most permissive)
        r'\{[\s\S]*?\}',  # Object pattern
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, text, re.DOTALL)
        for match in matches:
            try:
                parsed = json.loads(match.strip())
                # Ensure it's a list for our use case
                if isinstance(parsed, list):
                    return parsed
                elif isinstance(parsed, dict):
                    return [parsed]  # Convert single object to list
            except json.JSONDecodeError:
                continue
    
    # Try parsing the whole text after cleaning
    try:
        # Remove any leading/trailing non-JSON text
        cleaned_text = text.strip()
        # Find the first [ and last ]
        start_idx = cleaned_text.find('[')
        end_idx = cleaned_text.rfind(']')
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            json_text = cleaned_text[start_idx:end_idx+1]
            return json.loads(json_text)
    except (json.JSONDecodeError, ValueError):
        pass
    
    return None