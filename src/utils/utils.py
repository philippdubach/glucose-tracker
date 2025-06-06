# utils.py
class Utils:
    """Utility functions for data processing and formatting"""
    
    @staticmethod
    def seconds_to_time_string(seconds: int) -> str:
        """Convert seconds to HH:MM format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        return f"{hours}:{minutes:02d}h"
    
    @staticmethod
    def validate_data_quality(df: pd.DataFrame) -> dict:
        """Validate data quality and return metrics"""
        return {
            'missing_percentage': df.isnull().sum() / len(df) * 100,
            'date_range': (df.index.min(), df.index.max()),
            'total_records': len(df)
        }