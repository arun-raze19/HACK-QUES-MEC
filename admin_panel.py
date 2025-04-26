from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QPushButton, QMessageBox, QTableWidget,
                           QTableWidgetItem, QHBoxLayout, QFileDialog, QTabWidget,
                           QTextEdit)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import csv
import os
import pandas as pd
from activity_logger import ActivityLogger

class AdminPanel(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Admin Panel")
        self.setGeometry(100, 100, 1200, 800)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Hackathon Admin Panel")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Teams tab
        teams_tab = QWidget()
        teams_layout = QVBoxLayout()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("Refresh Data")
        refresh_button.setFont(QFont("Arial", 12))
        refresh_button.clicked.connect(self.load_data)
        button_layout.addWidget(refresh_button)
        
        export_button = QPushButton("Export All Data")
        export_button.setFont(QFont("Arial", 12))
        export_button.clicked.connect(self.export_data)
        button_layout.addWidget(export_button)
        
        teams_layout.addLayout(button_layout)
        
        # Teams table
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(15)
        self.teams_table.setHorizontalHeaderLabels([
            "Team Name", "Registration Time",
            "Contestant 1", "Email 1", "Phone 1",
            "Contestant 2", "Email 2", "Phone 2",
            "Contestant 3", "Email 3", "Phone 3",
            "MCQ Score", "DSA1 Score", "DSA2 Score",
            "Total Score"
        ])
        teams_layout.addWidget(self.teams_table)
        
        teams_tab.setLayout(teams_layout)
        self.tabs.addTab(teams_tab, "Teams")
        
        # Activity Logs tab
        logs_tab = QWidget()
        logs_layout = QVBoxLayout()
        
        self.logs_table = QTableWidget()
        self.logs_table.setColumnCount(8)
        self.logs_table.setHorizontalHeaderLabels([
            "Timestamp", "Activity Type", "Round",
            "Question ID", "Status", "Score",
            "Time Taken", "Details"
        ])
        logs_layout.addWidget(self.logs_table)
        
        logs_tab.setLayout(logs_layout)
        self.tabs.addTab(logs_tab, "Activity Logs")
        
        # Performance Review tab
        review_tab = QWidget()
        review_layout = QVBoxLayout()
        
        self.review_text = QTextEdit()
        self.review_text.setReadOnly(True)
        review_layout.addWidget(self.review_text)
        
        review_tab.setLayout(review_layout)
        self.tabs.addTab(review_tab, "Performance Review")
        
        layout.addWidget(self.tabs)
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
        # Load initial data
        self.load_data()
        
    def load_data(self):
        # Clear tables
        self.teams_table.setRowCount(0)
        self.logs_table.setRowCount(0)
        self.review_text.clear()
        
        # Get all CSV files
        csv_files = [f for f in os.listdir('team_data') if f.endswith('.csv')]
        
        for file in csv_files:
            try:
                # Load team data
                if not file.endswith('_activity_log.csv'):
                    with open(os.path.join('team_data', file), 'r') as f:
                        reader = csv.reader(f)
                        data = list(reader)
                        
                        # Extract team info
                        team_name = data[0][1]
                        reg_time = data[1][1]
                        
                        # Extract contestant info
                        contestants = []
                        for row in data[4:7]:  # Skip header rows
                            contestants.extend(row[1:])  # Skip contestant number
                        
                        # Add row to teams table
                        row = self.teams_table.rowCount()
                        self.teams_table.insertRow(row)
                        
                        # Add data to cells
                        self.teams_table.setItem(row, 0, QTableWidgetItem(team_name))
                        self.teams_table.setItem(row, 1, QTableWidgetItem(reg_time))
                        
                        for i, value in enumerate(contestants):
                            self.teams_table.setItem(row, i+2, QTableWidgetItem(value))
                        
                        # Add placeholder for scores
                        for i in range(3):
                            self.teams_table.setItem(row, i+11, QTableWidgetItem("0"))
                        self.teams_table.setItem(row, 14, QTableWidgetItem("0"))
                
                # Load activity logs
                if file.endswith('_activity_log.csv'):
                    with open(os.path.join('team_data', file), 'r') as f:
                        reader = csv.reader(f)
                        next(reader)  # Skip header
                        
                        for row in reader:
                            log_row = self.logs_table.rowCount()
                            self.logs_table.insertRow(log_row)
                            
                            for i, value in enumerate(row):
                                self.logs_table.setItem(log_row, i, QTableWidgetItem(value))
            
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")
        
        # Generate performance review
        self.generate_performance_review()
        
        # Resize columns to content
        self.teams_table.resizeColumnsToContents()
        self.logs_table.resizeColumnsToContents()
        
    def generate_performance_review(self):
        review_text = "Performance Review\n\n"
        
        # Get all team names
        team_names = set()
        for row in range(self.teams_table.rowCount()):
            team_names.add(self.teams_table.item(row, 0).text())
        
        for team_name in team_names:
            logger = ActivityLogger(team_name)
            performance = logger.get_team_performance()
            
            review_text += f"Team: {team_name}\n"
            review_text += "=" * 50 + "\n"
            
            for round_name, stats in performance.items():
                review_text += f"\n{round_name.upper()} Round:\n"
                review_text += f"Questions Attempted: {stats['attempted']}\n"
                review_text += f"Correct Answers: {stats['correct']}\n"
                review_text += f"Total Score: {stats['score']}\n"
                
                if stats['attempted'] > 0:
                    accuracy = (stats['correct'] / stats['attempted']) * 100
                    review_text += f"Accuracy: {accuracy:.2f}%\n"
                
                review_text += "-" * 30 + "\n"
            
            review_text += "\n"
        
        self.review_text.setText(review_text)
        
    def export_data(self):
        # Get save location
        filename, _ = QFileDialog.getSaveFileName(
            self, "Export Data", "", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                # Create DataFrame from teams table
                teams_data = []
                for row in range(self.teams_table.rowCount()):
                    row_data = []
                    for col in range(self.teams_table.columnCount()):
                        item = self.teams_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    teams_data.append(row_data)
                
                # Create DataFrame
                df_teams = pd.DataFrame(teams_data, columns=[
                    "Team Name", "Registration Time",
                    "Contestant 1", "Email 1", "Phone 1",
                    "Contestant 2", "Email 2", "Phone 2",
                    "Contestant 3", "Email 3", "Phone 3",
                    "MCQ Score", "DSA1 Score", "DSA2 Score",
                    "Total Score"
                ])
                
                # Save to CSV
                df_teams.to_csv(filename, index=False)
                
                # Export activity logs
                logs_filename = filename.replace('.csv', '_logs.csv')
                logs_data = []
                for row in range(self.logs_table.rowCount()):
                    row_data = []
                    for col in range(self.logs_table.columnCount()):
                        item = self.logs_table.item(row, col)
                        row_data.append(item.text() if item else "")
                    logs_data.append(row_data)
                
                df_logs = pd.DataFrame(logs_data, columns=[
                    "Timestamp", "Activity Type", "Round",
                    "Question ID", "Status", "Score",
                    "Time Taken", "Details"
                ])
                
                df_logs.to_csv(logs_filename, index=False)
                
                QMessageBox.information(self, "Success", "Data exported successfully!")
                
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Error exporting data: {str(e)}")

def show_admin_panel():
    app = QApplication([])
    window = AdminPanel()
    window.show()
    app.exec_() 