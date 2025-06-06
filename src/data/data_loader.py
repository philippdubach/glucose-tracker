# data_loader.py
class DataLoader:
    """Handles loading and initial processing of all data sources"""
    
    def __init__(self, config: Config):
        self.config = config
        
    def load_glucose_data(self, filepath: str) -> pd.DataFrame:
        """Load and preprocess glucose data from LibreView"""
        try:
            df = pd.read_csv(filepath, skiprows=1)
            df['Device Timestamp'] = pd.to_datetime(df['Device Timestamp'], dayfirst=True)
            df = df.set_index('Device Timestamp').sort_index()
            df = df.groupby(level=0).mean()
            df.replace(0, np.nan, inplace=True)
            return df
        except Exception as e:
            raise DataLoadError(f"Failed to load glucose data: {e}")
    
    def load_all_data(self) -> dict:
        """Load all data sources and return as dictionary"""
        return {
            'glucose': self.load_glucose_data(self.config.GLUCOSE_FILE),
            'sleep': self.load_sleep_data(self.config.SLEEP_FILE),
            'workouts': self.load_workout_data(self.config.WORKOUT_FILE),
            'nutrition': self.load_nutrition_data(self.config.NUTRITION_FILE)
        }
