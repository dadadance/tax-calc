"""Base importer class for file imports."""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from dataclasses import dataclass
from tax_core.models import UserProfile


@dataclass
class ImportResult:
    """Result of an import operation."""
    success: bool
    profile: Optional[UserProfile] = None
    errors: List[str] = None
    warnings: List[str] = None
    
    def __post_init__(self):
        """Initialize empty lists if None."""
        if self.errors is None:
            self.errors = []
        if self.warnings is None:
            self.warnings = []


class BaseImporter(ABC):
    """Base class for file importers."""
    
    def __init__(self):
        """Initialize base importer."""
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    @abstractmethod
    def parse(self, file_path: str) -> Dict:
        """
        Parse the file and return raw data.
        
        Args:
            file_path: Path to the file to parse
            
        Returns:
            Dict: Parsed data
        """
        pass
    
    @abstractmethod
    def validate(self, data: Dict) -> bool:
        """
        Validate the parsed data.
        
        Args:
            data: Parsed data dictionary
            
        Returns:
            bool: True if data is valid
        """
        pass
    
    @abstractmethod
    def extract_user_profile(self, data: Dict, year: int) -> UserProfile:
        """
        Extract UserProfile from parsed data.
        
        Args:
            data: Parsed data dictionary
            year: Tax year
            
        Returns:
            UserProfile: Extracted user profile
        """
        pass
    
    def import_data(self, file_path: str, year: int) -> ImportResult:
        """
        Import data from file and return UserProfile.
        
        Args:
            file_path: Path to the file to import
            year: Tax year
            
        Returns:
            ImportResult: Import result with profile or errors
        """
        self.errors = []
        self.warnings = []
        
        try:
            # Parse file
            data = self.parse(file_path)
            
            # Validate data
            if not self.validate(data):
                return ImportResult(
                    success=False,
                    errors=self.errors,
                    warnings=self.warnings,
                )
            
            # Extract profile
            profile = self.extract_user_profile(data, year)
            
            return ImportResult(
                success=True,
                profile=profile,
                errors=self.errors,
                warnings=self.warnings,
            )
            
        except Exception as e:
            self.errors.append(f"Import failed: {str(e)}")
            return ImportResult(
                success=False,
                errors=self.errors,
                warnings=self.warnings,
            )
    
    def get_errors(self) -> List[str]:
        """Get list of errors from last import."""
        return self.errors
    
    def get_warnings(self) -> List[str]:
        """Get list of warnings from last import."""
        return self.warnings

