# main.py
class GlucoseTracker:
    """Main application class coordinating all components"""
    
    def __init__(self, config_path: str = None):
        self.config = Config()
        self.data_loader = DataLoader(self.config)
        self.data_processor = DataProcessor(self.config)
        self.dashboard = GlucoseDashboard(self.config)
        self.data = None
        
    def load_data(self):
        """Load all data sources"""
        try:
            self.data = self.data_loader.load_all_data()
            logger.info("Data loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise
    
    def process_data(self):
        """Process and merge all data"""
        if not self.data:
            raise ProcessingError("No data loaded")
        
        self.processed_data = self.data_processor.merge_all_data(self.data)
        
    def generate_dashboard(self, output_path: str = None):
        """Generate complete dashboard"""
        if not self.processed_data:
            raise ProcessingError("No processed data available")
        
        self.dashboard.create_multi_day_dashboard(self.processed_data, output_path)

if __name__ == "__main__":
    tracker = GlucoseTracker()
    tracker.load_data()
    tracker.process_data()
    tracker.generate_dashboard()
    
def mark_activities_vectorized(df: pd.DataFrame, activity_periods: pd.DataFrame) -> pd.DataFrame:
    """Use numpy broadcasting for efficient activity marking"""
    df_times = df.index.values
    for _, period in activity_periods.iterrows():
        mask = (df_times >= period['start_time']) & (df_times <= period['end_time'])
        df.loc[mask, 'activity'] = 1
    return df

# Efficient data filtering
def filter_date_range_efficient(df: pd.DataFrame, start_date: str, end_date: str) -> pd.DataFrame:
    """Use pandas date filtering for better performance"""
    return df.loc[start_date:end_date]