# visualizer.py
class GlucoseDashboard:
    """Handles visualization and dashboard creation"""
    
    def __init__(self, config: Config):
        self.config = config
        
    def create_daily_plot(self, data: pd.DataFrame, date: datetime.date) -> tuple:
        """Create a single day's glucose plot with annotations"""
        fig, (ax_main, ax_stats) = plt.subplots(1, 2, figsize=self.config.PLOT_FIGURE_SIZE,
                                               gridspec_kw={'width_ratios': [5, 1]})
        
        day_data = self._filter_day_data(data, date)
        
        # Plot glucose line
        glucose_data = day_data['Historic Glucose mmol/L'].dropna()
        ax_main.plot(glucose_data.index, glucose_data.values, color='blue', linewidth=2)
        
        # Add target range
        self._add_target_range(ax_main, date)
        
        # Add activity markers
        self._add_activity_markers(ax_main, day_data, date)
        
        # Add statistics
        self._add_statistics_panel(ax_stats, glucose_data)
        
        self._format_axes(ax_main, date)
        
        return fig, ax_main, ax_stats
    
    def _calculate_time_in_range(self, data: pd.Series) -> float:
        """Calculate time in range percentage"""
        target_min, target_max = self.config.GLUCOSE_TARGET_RANGE
        in_range = (target_min <= data) & (data <= target_max)
        return (in_range.sum() / len(data)) * 100 if len(data) > 0 else 0
