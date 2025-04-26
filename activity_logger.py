import csv
import os
from datetime import datetime

class ActivityLogger:
    def __init__(self, team_name):
        self.team_name = team_name
        self.log_file = f"team_data/{team_name}_activity_log.csv"
        self.initialize_log()
        
    def initialize_log(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    'Timestamp',
                    'Activity Type',
                    'Round',
                    'Question ID',
                    'Status',
                    'Score',
                    'Time Taken',
                    'Details'
                ])
    
    def log_activity(self, activity_type, round_name, question_id, status, score, time_taken, details):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                timestamp,
                activity_type,
                round_name,
                question_id,
                status,
                score,
                time_taken,
                details
            ])
    
    def log_question_attempt(self, round_name, question_id, status, score, time_taken, details):
        self.log_activity(
            'Question Attempt',
            round_name,
            question_id,
            status,
            score,
            time_taken,
            details
        )
    
    def log_round_start(self, round_name):
        self.log_activity(
            'Round Start',
            round_name,
            '',
            'Started',
            0,
            0,
            f'Started {round_name} round'
        )
    
    def log_round_end(self, round_name, total_score):
        self.log_activity(
            'Round End',
            round_name,
            '',
            'Completed',
            total_score,
            0,
            f'Completed {round_name} round with score {total_score}'
        )
    
    def log_performance_review(self, round_name, review):
        self.log_activity(
            'Performance Review',
            round_name,
            '',
            'Review',
            0,
            0,
            review
        )
    
    def get_team_performance(self):
        performance = {
            'mcq': {'attempted': 0, 'correct': 0, 'score': 0},
            'dsa1': {'attempted': 0, 'correct': 0, 'score': 0},
            'dsa2': {'attempted': 0, 'correct': 0, 'score': 0}
        }
        
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                
                for row in reader:
                    if row[1] == 'Question Attempt':
                        round_name = row[2].lower()
                        if round_name in performance:
                            performance[round_name]['attempted'] += 1
                            if row[4] == 'Correct':
                                performance[round_name]['correct'] += 1
                            performance[round_name]['score'] += float(row[5])
        
        return performance 