import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional
import logging

from ..utils.exceptions import ProcessingError

logger = logging.getLogger(__name__)


class DataProcessor:
    """Processes and merges data from multiple sources"""
    
    def __init__(self, config):
        self.config = config
        
    def create_timeline_dataframe(self, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Create minute-by-minute timeline dataframe"""
        date_range = pd.date_range(start=start_date, end=end_date, freq='T')
        df = pd.DataFrame(index=date_range)
        
        # Initialize activity columns
        df[['Sleep', 'Strength', 'Cardio', 'Nutrition']] = 0
        
        return df
    
    def mark_activities_vectorized(self, df: pd.DataFrame, activity_periods: pd.DataFrame, 
                                 activity_column: str) -> pd.DataFrame:
        """Use numpy broadcasting for efficient activity marking"""
        if activity_periods.empty:
            return df
            
        df_times = df.index.values
        
        # Ensure the activity column exists
        if activity_column not in df.columns:
            df[activity_column] = 0
            
        for _, period in activity_periods.iterrows():
            start_time = pd.to_datetime(period['start_time']).value
            end_time = pd.to_datetime(period['end_time']).value
            
            # Use numpy broadcasting for efficient comparison
            mask = (df_times >= start_time) & (df_times <= end_time)
            df.loc[mask, activity_column] = 1
            
        return df
    
    def filter_date_range_efficient(self, df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
        """Use pandas date filtering for better performance"""
        try:
            return df.loc[start_date:end_date]
        except KeyError as e:
            logger.warning(f"Date range {start_date} to {end_date} not found in data: {e}")
            return pd.DataFrame()
    
    def merge_all_data(self, data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """Merge all data sources into a single timeline dataframe"""
        try:
            # Get date range from glucose data
            glucose_df = data_dict['glucose']
            start_date = glucose_df.index.min().floor('D')
            end_date = glucose_df.index.max().ceil('D')
            
            # Create base timeline
            timeline_df = self.create_timeline_dataframe(start_date, end_date)
            
            # Merge glucose data
            timeline_df = timeline_df.join(
                glucose_df[["Historic Glucose mmol/L", "Scan Glucose mmol/L"]], 
                how='left'
            )
            
            # Merge nutrition data
            if 'nutrition' in data_dict and not data_dict['nutrition'].empty:
                nutrition_df = data_dict['nutrition']
                timeline_df = timeline_df.join(
                    nutrition_df[["Meal", 'P_Macro', 'F_Macro', 'C_Macro']], 
                    how='left'
                )
                timeline_df['Nutrition'] = timeline_df['Meal'].notna().astype(int)
            
            # Mark activities using vectorized approach
            if 'sleep' in data_dict and not data_dict['sleep'].empty:
                timeline_df = self.mark_activities_vectorized(
                    timeline_df, data_dict['sleep'], 'Sleep'
                )
            
            if 'workouts' in data_dict and not data_dict['workouts'].empty:
                # Split workouts by type if needed
                strength_workouts = data_dict['workouts'][
                    data_dict['workouts']['type'] == 'strength'
                ] if 'type' in data_dict['workouts'].columns else data_dict['workouts']
                
                timeline_df = self.mark_activities_vectorized(
                    timeline_df, strength_workouts, 'Strength'
                )
            
            # Calculate derived metrics
            timeline_df = self.calculate_metrics(timeline_df)
            
            logger.info(f"Successfully merged data covering {start_date} to {end_date}")
            return timeline_df
            
        except Exception as e:
            logger.error(f"Failed to merge data: {e}")
            raise ProcessingError(f"Data merging failed: {e}")
    
    def calculate_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate derived metrics like ROC and interpolated values"""
        try:
            # Rate of change calculation
            glucose_col = "Historic Glucose mmol/L"
            if glucose_col in df.columns:
                time_diff_minutes = df.index.to_series().diff().dt.total_seconds() / 60
                df["Rate of Change (ROC)"] = df[glucose_col].diff() / time_diff_minutes
                
                # Interpolated glucose values
                df['Glucose_interpolated'] = df[glucose_col].interpolate(method='linear')
            
            return df
            
        except Exception as e:
            logger.error(f"Failed to calculate metrics: {e}")
            raise ProcessingError(f"Metrics calculation failed: {e}")
    
    def validate_processed_data(self, df: pd.DataFrame) -> Dict[str, any]:
        """Validate the processed dataframe and return quality metrics"""
        validation_results = {
            'total_records': len(df),
            'date_range': (df.index.min(), df.index.max()),
            'missing_glucose_pct': df['Historic Glucose mmol/L'].isnull().sum() / len(df) * 100,
            'activity_coverage': {
                'sleep': df['Sleep'].sum() / len(df) * 100,
                'strength': df['Strength'].sum() / len(df) * 100,
                'nutrition_events': df['Nutrition'].sum()
            }
        }
        
        return validation_results