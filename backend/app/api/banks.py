from fastapi import APIRouter
from typing import List, Dict
import json
from pathlib import Path

router = APIRouter()


def get_available_banks() -> Dict[str, any]:
    """
    Get list of available banks from config files.
    Returns dict with banks categorized by product type.
    """
    bank_data_path = Path(__file__).parent.parent.parent / "configs" / "bank_data"
    
    banks_by_product = {
        "debit": set(),
        "credit": set()
    }
    
    all_banks = set()
    
    # Check if directory exists
    if bank_data_path.exists():
        # Parse config files to extract bank names
        for file in bank_data_path.glob("*.json"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Handle different file structures
                    if "Сбербанк" in data:
                        # Multi-bank comparison file
                        for bank_key in data.keys():
                            all_banks.add(bank_key)
                    elif "bank" in data:
                        # Single bank file
                        bank_name = data["bank"]
                        all_banks.add(bank_name)
                        
                        if "debit" in file.name.lower():
                            banks_by_product["debit"].add(bank_name)
                        elif "credit" in file.name.lower():
                            banks_by_product["credit"].add(bank_name)
            except Exception as e:
                continue
    
    # Default banks if nothing found
    if not all_banks:
        all_banks = {"Сбербанк", "ВТБ", "Альфа-Банк", "Т-Банк", "Газпромбанк", 
                     "Локо-Банк", "МТС Банк", "Райффайзенбанк"}
        banks_by_product = {
            "debit": all_banks.copy(),
            "credit": all_banks.copy()
        }
    
    # Convert sets to sorted lists
    return {
        "all": sorted(list(all_banks)),
        "by_product": {
            "debit": sorted(list(banks_by_product["debit"])),
            "credit": sorted(list(banks_by_product["credit"]))
        },
        "product_types": [
            "Кредитная карта",
            "Дебетовая карта",
            "Потребительский кредит",
            "Ипотека"
        ]
    }


@router.get("/available")
async def get_banks():
    """
    Returns list of available banks for dropdown lists.
    Categorized by product type.
    """
    return get_available_banks()
