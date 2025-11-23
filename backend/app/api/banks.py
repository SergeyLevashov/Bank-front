from fastapi import APIRouter
from typing import List, Dict
import os
import json
from pathlib import Path

router = APIRouter()


def get_available_banks() -> Dict[str, List[str]]:
    """
    Get list of available banks from config files.
    Returns dict with banks categorized by product type.
    """
    bank_data_path = Path(__file__).parent.parent.parent / "configs" / "bank_data"
    
    banks = {
        "debit": set(),
        "credit": set()
    }
    
    # Check if directory exists
    if not bank_data_path.exists():
        # Return default list if configs not found
        return {
            "debit": ["Сбербанк", "ВТБ", "Альфа-Банк", "Т-Банк", "Газпромбанк", "Локо-Банк", "МТС Банк", "Райффайзенбанк"],
            "credit": ["Сбербанк", "ВТБ", "Альфа-Банк", "Т-Банк", "Газпромбанк", "Локо-Банк", "МТС Банк", "Райффайзенбанк"]
        }
    
    # Parse config files to extract bank names
    for file in bank_data_path.glob("*.json"):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                bank_name = data.get("bank", "")
                
                if "debit" in file.name.lower():
                    banks["debit"].add(bank_name)
                elif "credit" in file.name.lower():
                    banks["credit"].add(bank_name)
        except Exception as e:
            continue
    
    # Convert sets to sorted lists
    return {
        "debit": sorted(list(banks["debit"])),
        "credit": sorted(list(banks["credit"]))
    }


@router.get("/available")
async def get_banks():
    """
    Returns list of available banks for dropdown lists.
    Categorized by product type.
    """
    banks = get_available_banks()
    
    # Combine all banks for general list
    all_banks = sorted(list(set(banks["debit"] + banks["credit"])))
    
    return {
        "all": all_banks,
        "by_product": banks,
        "product_types": [
            "Кредитная карта",
            "Дебетовая карта",
            "Потребительский кредит",
            "Ипотека"
        ]
    }
