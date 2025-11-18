"""SQLite database for saving and loading user profiles."""
import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import asdict

from tax_core.models import (
    UserProfile,
    ResidencyStatus,
    SalaryIncome,
    MicroBusinessIncome,
    SmallBusinessIncome,
    RentalIncome,
    CapitalGainsIncome,
    DividendsIncome,
    InterestIncome,
    PropertyTaxInput,
)


DB_PATH = Path("data/profiles.db")
DB_PATH.parent.mkdir(exist_ok=True)


def init_db():
    """Initialize the database with required tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            profile_data TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()


def save_profile(name: str, profile: UserProfile, description: str = "") -> int:
    """Save a profile to the database. Returns profile ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Convert profile to JSON
    profile_dict = {
        "year": profile.year,
        "residency": profile.residency.value,
        "salary": [asdict(s) for s in profile.salary] if profile.salary else [],
        "micro_business": [asdict(m) for m in profile.micro_business] if profile.micro_business else [],
        "small_business": [asdict(s) for s in profile.small_business] if profile.small_business else [],
        "rental": [asdict(r) for r in profile.rental] if profile.rental else [],
        "capital_gains": [asdict(cg) for cg in profile.capital_gains] if profile.capital_gains else [],
        "dividends": [asdict(d) for d in profile.dividends] if profile.dividends else [],
        "interest": [asdict(i) for i in profile.interest] if profile.interest else [],
        "property_tax": [asdict(pt) for pt in profile.property_tax] if profile.property_tax else [],
    }
    
    profile_json = json.dumps(profile_dict)
    
    try:
        cursor.execute("""
            INSERT INTO profiles (name, description, profile_data, updated_at)
            VALUES (?, ?, ?, ?)
        """, (name, description, profile_json, datetime.now()))
        profile_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Update if name already exists
        cursor.execute("""
            UPDATE profiles 
            SET description = ?, profile_data = ?, updated_at = ?
            WHERE name = ?
        """, (description, profile_json, datetime.now(), name))
        cursor.execute("SELECT id FROM profiles WHERE name = ?", (name,))
        profile_id = cursor.fetchone()[0]
    
    conn.commit()
    conn.close()
    return profile_id


def load_profile(name: str) -> Optional[UserProfile]:
    """Load a profile by name. Returns None if not found."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT profile_data FROM profiles WHERE name = ?", (name,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    profile_dict = json.loads(row[0])
    
    # Reconstruct UserProfile
    return UserProfile(
        year=profile_dict["year"],
        residency=ResidencyStatus(profile_dict["residency"]),
        salary=[SalaryIncome(**s) for s in profile_dict.get("salary", [])],
        micro_business=[MicroBusinessIncome(**m) for m in profile_dict.get("micro_business", [])],
        small_business=[SmallBusinessIncome(**s) for s in profile_dict.get("small_business", [])],
        rental=[RentalIncome(**r) for r in profile_dict.get("rental", [])],
        capital_gains=[CapitalGainsIncome(**cg) for cg in profile_dict.get("capital_gains", [])],
        dividends=[DividendsIncome(**d) for d in profile_dict.get("dividends", [])],
        interest=[InterestIncome(**i) for i in profile_dict.get("interest", [])],
        property_tax=[PropertyTaxInput(**pt) for pt in profile_dict.get("property_tax", [])],
    )


def list_profiles() -> List[Dict[str, Any]]:
    """List all saved profiles."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, description, created_at, updated_at
        FROM profiles
        ORDER BY updated_at DESC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2] or "",
            "created_at": row[3],
            "updated_at": row[4],
        }
        for row in rows
    ]


def delete_profile(name: str) -> bool:
    """Delete a profile by name. Returns True if deleted, False if not found."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM profiles WHERE name = ?", (name,))
    deleted = cursor.rowcount > 0
    
    conn.commit()
    conn.close()
    return deleted


def get_profile_info(name: str) -> Optional[Dict[str, Any]]:
    """Get profile metadata without loading full profile."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, name, description, created_at, updated_at, profile_data
        FROM profiles WHERE name = ?
    """, (name,))
    
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
    
    profile_dict = json.loads(row[5])
    
    # Count income sources
    income_summary = {
        "salary_count": len(profile_dict.get("salary", [])),
        "micro_business_count": len(profile_dict.get("micro_business", [])),
        "small_business_count": len(profile_dict.get("small_business", [])),
        "rental_count": len(profile_dict.get("rental", [])),
        "capital_gains_count": len(profile_dict.get("capital_gains", [])),
        "dividends_count": len(profile_dict.get("dividends", [])),
        "interest_count": len(profile_dict.get("interest", [])),
        "property_tax_count": len(profile_dict.get("property_tax", [])),
    }
    
    return {
        "id": row[0],
        "name": row[1],
        "description": row[2] or "",
        "created_at": row[3],
        "updated_at": row[4],
        "income_summary": income_summary,
    }

