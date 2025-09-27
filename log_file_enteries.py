# log_file_analyzer_with_random_logs.py

import random
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import re

# --- Step 1: Generate Random Logs ---
def generate_random_logs(file_path, num_entries=100):
    levels = ['INFO', 'WARNING', 'ERROR']
    messages = {
        'INFO': ['Server started', 'User logged in', 'Configuration loaded', 'Task completed'],
        'WARNING': ['High memory usage', 'Disk space low', 'API response slow'],
        'ERROR': ['Connection failed', 'Disk read error', 'Null pointer exception', 'Timeout occurred']
    }

    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    with open(file_path, 'w') as file:
        for _ in range(num_entries):
            timestamp = start_time + timedelta(minutes=random.randint(0, 600))  # random time within 10 hours
            level = random.choice(levels)
            message = random.choice(messages[level])
            log_entry = f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {level} - {message}\n"
            file.write(log_entry)
    print(f"{num_entries} random log entries generated in {file_path}")

# --- Step 2: Read Log File ---
def read_log(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()
    return logs

# --- Step 3: Parse Logs ---
def parse_logs(logs):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (\w+) - (.+)'
    parsed_data = []

    for log in logs:
        match = re.match(pattern, log)
        if match:
            timestamp, level, message = match.groups()
            parsed_data.append({
                'timestamp': pd.to_datetime(timestamp),
                'level': level,
                'message': message
            })
    df = pd.DataFrame(parsed_data)
    return df

# --- Step 4: Detect Patterns ---
def detect_patterns(df):
    pattern_counts = df['level'].value_counts()
    print("\n--- Log Level Counts ---")
    print(pattern_counts)

# --- Step 5: Detect Anomalies ---
def detect_anomalies(df):
    error_df = df[df['level'] == 'ERROR']
    errors_per_hour = error_df.groupby(df['timestamp'].dt.hour).size()
    
    mean_errors = errors_per_hour.mean() if not errors_per_hour.empty else 0
    anomalies = errors_per_hour[errors_per_hour > 2 * mean_errors]  # simple threshold
    print("\n--- Anomalies Detected (High Error Hours) ---")
    print(anomalies if not anomalies.empty else "No anomalies detected")

# --- Step 6: Visualization ---
def visualize_logs(df):
    counts = df.groupby(['timestamp', 'level']).size().unstack(fill_value=0)
    counts.plot(kind='line', figsize=(12,6), marker='o')
    plt.title("Log Level Trends Over Time")
    plt.xlabel("Timestamp")
    plt.ylabel("Count")
    plt.grid(True)
    plt.show()

# --- Main Function ---
if __name__ == "__main__":
    log_file = 'random_logs.log'
    
    # Generate 100 random log entries
    generate_random_logs(log_file, 100)
    
    # Analyze generated logs
    logs = read_log(log_file)
    df = parse_logs(logs)
    detect_patterns(df)
    detect_anomalies(df)
    visualize_logs(df)
