class Config:
    GLUCOSE_TARGET_RANGE = (3.9, 10.0)  # mmol/L
    PLOT_FIGURE_SIZE = (15, 4)
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # File paths
    DATA_DIR = 'data'
    GLUCOSE_FILE = 'glucose_data.csv'
    SLEEP_FILE = 'sleepdata.csv'
    WORKOUT_FILE = 'workout_data.csv'
    NUTRITION_FILE = 'food_log.csv'