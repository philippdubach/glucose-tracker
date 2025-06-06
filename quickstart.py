#!/usr/bin/env python3
"""
Glucose Tracker - Quick Start Script

This script provides a simple way to get started with the glucose tracking dashboard.
Run this script to load sample data and generate your first dashboard.

Usage:
    python quickstart.py
    python quickstart.py --data-dir /path/to/your/data
    python quickstart.py --config config.yaml --output dashboard.html
"""

import argparse
import logging
import sys
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

class QuickStartTracker:
    """Simplified version of the glucose tracker for quick testing"""
    
    def __init__(self, data_dir: str = "data/sample", output_dir: str = "output"):
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Configuration
        self.glucose_target_range = (3.9, 10.0)
        self.figure_size = (15, 8)
        
        logger.info(f"Initialized QuickStart with data_dir: {self.data_dir}")
    
    def check_data_files(self) -> bool:
        """Check if required data files exist"""
        required_files = [
            'glucose_data.csv',
            'sleepdata.csv', 
            'workout_data.csv',
            'food_log.csv'
        ]
        
        missing_files = []
        for file in required_files:
            if not (self.data_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            logger.warning(f"Missing files: {missing_files}")
            logger.info("Creating sample data files...")
            self.create_sample_data()
            return True
        
        logger.info("All data files found!")
        return True
    
    def create_sample_data(self):
        """Create sample data files for demonstration"""
        logger.info("Generating sample data...")
        
        # Create sample glucose data
        dates = pd.date_range(
            start=datetime.now() - timedelta(days=7),
            end=datetime.now(),
            freq='5T'  # 5-minute intervals
        )
        
        # Generate realistic glucose values with some variation
        np.random.seed(42)
        baseline = 6.5  # mmol/L
        glucose_values = baseline + np.random.normal(0, 1.2, len(dates))
        glucose_values = np.clip(glucose_values, 3.0, 15.0)  # Realistic range
        
        glucose_df = pd.DataFrame({
            'Device Timestamp': dates,
            'Historic Glucose mmol/L': glucose_values,
            'Scan Glucose mmol/L': glucose_values * (1 + np.random.normal(0, 0.02, len(dates)))
        })
        
        self.data_dir.mkdir(parents=True, exist_ok=True)
        glucose_df.to_csv(self.data_dir / 'glucose_data.csv', index=False)
        
        # Create sample sleep data
        sleep_data = []
        for i in range(7):
            sleep_start = datetime.now() - timedelta(days=7-i) + timedelta(hours=22, minutes=30)
            sleep_end = sleep_start + timedelta(hours=8, minutes=15)
            sleep_data.append({
                'Start': sleep_start,
                'End': sleep_end,
                'Sleep Quality': np.random.choice(['Excellent', 'Good', 'Fair', 'Poor']),
                'Time in bed (seconds)': 8.25 * 3600,
                'Time asleep (seconds)': 7.5 * 3600
            })
        
        sleep_df = pd.DataFrame(sleep_data)
        sleep_df.to_csv(self.data_dir / 'sleepdata.csv', sep=';', index=False)
        
        # Create sample workout data
        workout_data = []
        for i in range(3):  # 3 workouts in the week
            workout_start = datetime.now() - timedelta(days=6-i*2) + timedelta(hours=18)
            workout_end = workout_start + timedelta(hours=1, minutes=30)
            workout_data.append({
                'start_time': workout_start,
                'end_time': workout_end,
                'workout_type': np.random.choice(['Strength', 'Cardio', 'Mixed'])
            })
        
        workout_df = pd.DataFrame(workout_data)
        workout_df.to_csv(self.data_dir / 'workout_data.csv', index=False)
        
        # Create sample nutrition data
        nutrition_data = []
        for i in range(7):
            day = datetime.now() - timedelta(days=7-i)
            # Add 3 meals per day
            for meal_time, meal_name in [(8, 'Breakfast'), (13, 'Lunch'), (19, 'Dinner')]:
                meal_datetime = day.replace(hour=meal_time, minute=0, second=0, microsecond=0)
                nutrition_data.append({
                    'Date': meal_datetime.strftime('%d/%m/%Y'),
                    'Time': meal_datetime.strftime('%H:%M'),
                    'Meal': f"{meal_name} - Sample meal",
                    'P_Macro': np.random.randint(15, 40),  # Protein
                    'F_Macro': np.random.randint(10, 30),  # Fat
                    'C_Macro': np.random.randint(20, 60),  # Carbs
                })
        
        nutrition_df = pd.DataFrame(nutrition_data)
        nutrition_df.to_csv(self.data_dir / 'food_log.csv', index=False)
        
        logger.info("Sample data created successfully!")
    
    def load_data(self) -> dict:
        """Load all data files"""
        logger.info("Loading data files...")
        
        try:
            # Load glucose data
            glucose_df = pd.read_csv(self.data_dir / 'glucose_data.csv')
            glucose_df['Device Timestamp'] = pd.to_datetime(glucose_df['Device Timestamp'])
            glucose_df = glucose_df.set_index('Device Timestamp').sort_index()
            
            # Load sleep data
            sleep_df = pd.read_csv(self.data_dir / 'sleepdata.csv', sep=';')
            sleep_df['Start'] = pd.to_datetime(sleep_df['Start'])
            sleep_df['End'] = pd.to_datetime(sleep_df['End'])
            
            # Load workout data
            workout_df = pd.read_csv(self.data_dir / 'workout_data.csv')
            workout_df['start_time'] = pd.to_datetime(workout_df['start_time'])
            workout_df['end_time'] = pd.to_datetime(workout_df['end_time'])
            
            # Load nutrition data
            nutrition_df = pd.read_csv(self.data_dir / 'food_log.csv')
            nutrition_df['Datetime'] = pd.to_datetime(
                nutrition_df['Date'] + ' ' + nutrition_df['Time'],
                dayfirst=True
            )
            nutrition_df = nutrition_df.set_index('Datetime')
            
            logger.info("Data loaded successfully!")
            
            return {
                'glucose': glucose_df,
                'sleep': sleep_df,
                'workouts': workout_df,
                'nutrition': nutrition_df
            }
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def create_quick_dashboard(self, data: dict) -> str:
        """Create a simplified dashboard"""
        logger.info("Creating dashboard...")
        
        glucose_df = data['glucose']
        
        # Create figure with subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=self.figure_size)
        fig.suptitle('Glucose Tracking Dashboard - Quick Start', fontsize=16, fontweight='bold')
        
        # Plot 1: Glucose over time
        glucose_data = glucose_df['Historic Glucose mmol/L'].dropna()
        ax1.plot(glucose_data.index, glucose_data.values, color='blue', linewidth=1, alpha=0.8)
        ax1.axhspan(self.glucose_target_range[0], self.glucose_target_range[1], 
                   alpha=0.2, color='green', label='Target Range')
        ax1.set_title('Glucose Levels Over Time')
        ax1.set_ylabel('Glucose (mmol/L)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Glucose distribution
        ax2.hist(glucose_data.values, bins=30, alpha=0.7, color='skyblue', edgecolor='black')
        ax2.axvline(glucose_data.mean(), color='red', linestyle='--', 
                   label=f'Mean: {glucose_data.mean():.1f}')
        ax2.axvline(glucose_data.median(), color='orange', linestyle='--',
                   label=f'Median: {glucose_data.median():.1f}')
        ax2.set_title('Glucose Distribution')
        ax2.set_xlabel('Glucose (mmol/L)')
        ax2.set_ylabel('Frequency')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Daily averages
        daily_avg = glucose_data.groupby(glucose_data.index.date).mean()
        ax3.plot(daily_avg.index, daily_avg.values, marker='o', linewidth=2, color='green')
        ax3.set_title('Daily Average Glucose')
        ax3.set_ylabel('Average Glucose (mmol/L)')
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)
        
        # Plot 4: Statistics summary
        ax4.axis('off')
        
        # Calculate statistics
        stats = {
            'Mean': glucose_data.mean(),
            'Median': glucose_data.median(),
            'Std Dev': glucose_data.std(),
            'Min': glucose_data.min(),
            'Max': glucose_data.max(),
            'CV (%)': (glucose_data.std() / glucose_data.mean()) * 100,
        }
        
        # Calculate Time in Range
        in_range = ((glucose_data >= self.glucose_target_range[0]) & 
                   (glucose_data <= self.glucose_target_range[1]))
        tir_percent = (in_range.sum() / len(glucose_data)) * 100
        stats['Time in Range (%)'] = tir_percent
        
        # Display statistics
        stats_text = '\n'.join([f'{key}: {value:.1f}' for key, value in stats.items()])
        ax4.text(0.1, 0.9, 'Summary Statistics:', fontsize=14, fontweight='bold',
                transform=ax4.transAxes)
        ax4.text(0.1, 0.7, stats_text, fontsize=12, transform=ax4.transAxes,
                verticalalignment='top', fontfamily='monospace')
        
        plt.tight_layout()
        
        # Save dashboard
        output_file = self.output_dir / f'glucose_dashboard_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()
        
        logger.info(f"Dashboard saved to: {output_file}")
        return str(output_file)
    
    def print_data_summary(self, data: dict):
        """Print a summary of loaded data"""
        print("\n" + "="*60)
        print("DATA SUMMARY")
        print("="*60)
        
        glucose_df = data['glucose']
        sleep_df = data['sleep']
        workout_df = data['workouts']
        nutrition_df = data['nutrition']
        
        print(f"📊 Glucose Data:")
        print(f"   • Records: {len(glucose_df):,}")
        print(f"   • Date range: {glucose_df.index.min().date()} to {glucose_df.index.max().date()}")
        print(f"   • Average glucose: {glucose_df['Historic Glucose mmol/L'].mean():.1f} mmol/L")
        
        print(f"\n😴 Sleep Data:")
        print(f"   • Sleep sessions: {len(sleep_df)}")
        if len(sleep_df) > 0:
            avg_sleep = sleep_df['Time asleep (seconds)'].mean() / 3600
            print(f"   • Average sleep: {avg_sleep:.1f} hours")
        
        print(f"\n💪 Workout Data:")
        print(f"   • Workout sessions: {len(workout_df)}")
        
        print(f"\n🍽️ Nutrition Data:")
        print(f"   • Meal entries: {len(nutrition_df)}")
        
        print("="*60)

def main():
    """Main function to run the quickstart"""
    parser = argparse.ArgumentParser(description='Glucose Tracker Quick Start')
    parser.add_argument('--data-dir', default='data/sample', 
                       help='Directory containing data files')
    parser.add_argument('--output-dir', default='output',
                       help='Directory for output files')
    parser.add_argument('--create-sample', action='store_true',
                       help='Force creation of sample data')
    
    args = parser.parse_args()
    
    print("🩸 Glucose Tracker - Quick Start")
    print("="*40)
    
    try:
        # Initialize tracker
        tracker = QuickStartTracker(args.data_dir, args.output_dir)
        
        # Check or create data files
        if args.create_sample:
            tracker.create_sample_data()
        else:
            tracker.check_data_files()
        
        # Load data
        data = tracker.load_data()
        
        # Print summary
        tracker.print_data_summary(data)
        
        # Create dashboard
        dashboard_path = tracker.create_quick_dashboard(data)
        
        print(f"\n✅ Quick start completed successfully!")
        print(f"📈 Dashboard saved to: {dashboard_path}")
        print(f"\n💡 Next steps:")
        print(f"   • Open the Jupyter notebook: jupyter notebook notebooks/data_exploration.ipynb")
        print(f"   • Customize your analysis by modifying the configuration")
        print(f"   • Replace sample data with your own data files")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Quick start interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Quick start failed: {e}")
        print(f"\n❌ Error: {e}")
        print("💡 Try running with --create-sample to generate sample data")
        sys.exit(1)

if __name__ == "__main__":
    main()