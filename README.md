# Glucose Tracker Dashboard

A comprehensive blood sugar tracking and analysis dashboard that integrates data from Abbott CGM devices with workout, nutrition, and sleep data to provide detailed health insights.

## Features

- 📊 **Multi-source Data Integration**: Combines glucose data with sleep, workout, and nutrition information
- 📈 **Interactive Visualizations**: Daily glucose trends with activity overlays
- 📋 **Health Metrics**: Time in Range (TIR), glucose variability, and statistical analysis
- 🎯 **Target Range Monitoring**: Visual indicators for optimal glucose levels
- 📱 **Multiple Export Formats**: PDF, PNG, and interactive HTML dashboards
- ⚙️ **Customizable Configuration**: Easy setup via YAML configuration files

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/philippdubach/glucose-tracker.git
cd glucose-tracker

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

```python
from glucose_tracker import GlucoseTracker

# Initialize tracker
tracker = GlucoseTracker()

# Load your data
tracker.load_data()

# Process and merge data
tracker.process_data()

# Generate dashboard
tracker.generate_dashboard()
```

### Command Line Interface

```bash
# Generate dashboard for specific date range
python -m glucose_tracker --start-date 2024-01-01 --end-date 2024-01-31

# Export to PDF
python -m glucose_tracker --output dashboard.pdf --format pdf

# Use custom config
python -m glucose_tracker --config my_config.yaml
```

## Data Sources

The dashboard integrates data from multiple sources:

| Data Type | Source | File Format | Required Columns |
|-----------|--------|-------------|------------------|
| **Glucose** | Abbott LibreView | CSV | Device Timestamp, Historic Glucose mmol/L |
| **Sleep** | Sleep Cycle App | CSV | Start, End, Sleep Quality, Time in bed |
| **Workouts** | Hevy/Garmin | CSV | start_time, end_time, activity_type |
| **Nutrition** | Food Log | CSV | Date, Time, Meal, P_Macro, F_Macro, C_Macro |

## Configuration

Create a `config.yaml` file to customize your dashboard:

```yaml
glucose:
  target_range: [3.9, 10.0]  # mmol/L
  units: "mmol/L"

visualization:
  figure_size: [15, 4]
  dpi: 300
  theme: "seaborn"

data_sources:
  glucose_file: "data/glucose_data.csv"
  sleep_file: "data/sleepdata.csv"
  workout_file: "data/workout_data.csv"
  nutrition_file: "data/food_log.csv"

export:
  default_format: "png"
  include_statistics: true
  show_annotations: true
```

## Dashboard Features

### 📊 Daily Glucose Trends
- Continuous glucose monitoring visualization
- Target range highlighting (3.9-10.0 mmol/L)
- Median glucose line overlay

### 🏃‍♂️ Activity Integration
- **Strength Training**: Yellow overlay during workout periods
- **Cardio**: Colored markers for cardio activities
- **Sleep**: Blue highlighted periods with quality metrics

### 🍽️ Nutrition Tracking
- Meal markers with macro breakdown
- Smart annotation positioning to avoid overlap
- Glucose response correlation

### 📈 Statistics Panel
- Daily glucose statistics (mean, median, std dev)
- Time in Range (TIR) percentage
- Coefficient of Variation (CV)
- Min/max glucose values

## Sample Output

```
Dashboard Generated Successfully!
┌─────────────────────────────────────────┐
│ Glucose Dashboard - January 2024        │
├─────────────────────────────────────────┤
│ Average TIR: 78.5%                     │
│ Days Analyzed: 31                       │
│ Total Glucose Readings: 8,934           │
│ Average Daily CV: 24.3%                │
└─────────────────────────────────────────┘
```

## Data Privacy & Security

- 🔒 **Local Processing**: All data processing happens locally on your machine
- 🚫 **No Cloud Upload**: Your health data never leaves your device
- 🗂️ **Flexible Storage**: Store data wherever you choose
- 🔐 **Optional Encryption**: Encrypt sensitive data files

## Project Structure

```
glucose-tracker/
├── src/
│   ├── glucose_tracker/
│   │   ├── data/              # Data loading and processing
│   │   ├── visualization/     # Dashboard and plotting
│   │   └── utils/            # Helper functions
├── data/
│   ├── sample/               # Sample data files
│   └── personal/            # Your data (gitignored)
├── tests/                   # Unit tests
├── docs/                    # Documentation
└── notebooks/              # Jupyter analysis examples
```

## Data Format Examples

### Glucose Data (LibreView Export)
```csv
Device Timestamp,Historic Glucose mmol/L,Scan Glucose mmol/L
01/01/2024 00:00,5.2,
01/01/2024 00:15,5.1,5.0
```

### Sleep Data
```csv
Start,End,Sleep Quality,Time in bed (seconds),Time asleep (seconds)
2024-01-01 23:30:00,2024-01-02 07:15:00,Good,27900,25200
```

### Nutrition Data
```csv
Date,Time,Meal,P_Macro,F_Macro,C_Macro
01/01/2024,08:00,Oatmeal with berries,12,8,45
```

## Troubleshooting

### Common Issues

**"No glucose data found"**
- Check file path in config.yaml
- Ensure CSV has correct column names
- Verify date format (DD/MM/YYYY vs MM/DD/YYYY)

**"Memory error with large datasets"**
- Use date filtering: `--start-date` and `--end-date`
- Process data in smaller chunks
- Consider data sampling for exploration

**"Annotations overlapping"**
- Reduce annotation density in config
- Use `show_annotations: false` for cleaner plots
- Adjust figure size for better spacing

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Abbott for LibreView glucose monitoring system
- Sleep Cycle for sleep tracking data
- Hevy and Garmin for workout data integration
- The open-source Python community for excellent libraries

## Disclaimer

⚠️ **Medical Disclaimer**: This tool is for informational purposes only and should not replace professional medical advice. Always consult with healthcare providers for medical decisions.

