from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout,
                           QHBoxLayout, QScrollArea)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import csv
import os
from datetime import datetime
from activity_logger import ActivityLogger
from hackathon_interface import HackathonApp

class LoginPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hackathon Registration")
        self.setGeometry(100, 100, 800, 600)
        
        # Create CSV directory if it doesn't exist
        if not os.path.exists('team_data'):
            os.makedirs('team_data')
        
        # Show rules and regulations
        self.show_rules_and_regulations()
        
        self.setup_ui()
        
    def show_rules_and_regulations(self):
        rules = """
        <h2>AI_HACKBLITZ-XXV Rules and Regulations</h2>
        
        <h3>General Rules:</h3>
        <ul>
            <li>Teams must consist of 1-3 members</li>
            <li>All team members must be present during the hackathon</li>
            <li>No external help or resources allowed during the competition</li>
            <li>No pre-written code allowed</li>
            <li>All code must be written during the hackathon</li>
        </ul>
        
        <h3>Round Structure:</h3>
        <ul>
            <li><b>MCQ Round (30 points):</b>
                <ul>
                    <li>15 questions on DSA and programming concepts</li>
                    <li>Time limit: 45 minutes</li>
                    <li>Minimum 50% required to qualify for next round</li>
                </ul>
            </li>
            <li><b>DSA Round 1 (30 points):</b>
                <ul>
                    <li>One problem with multiple test cases</li>
                    <li>Time limit: 20 minutes</li>
                    <li>Minimum 50% required to qualify for next round</li>
                </ul>
            </li>
            <li><b>DSA Round 2 (40 points):</b>
                <ul>
                    <li>One advanced problem with multiple test cases</li>
                    <li>Time limit: 30 minutes</li>
                    <li>Minimum 50% required to complete the hackathon</li>
                </ul>
            </li>
        </ul>
        
        <h3>Scoring:</h3>
        <ul>
            <li>Total possible score: 100 points</li>
            <li>MCQ Round: 30 points</li>
            <li>DSA Round 1: 30 points</li>
            <li>DSA Round 2: 40 points</li>
        </ul>
        
        <h3>Code Submission Rules:</h3>
        <ul>
            <li>Code must be submitted before the time limit</li>
            <li>All test cases must pass for full points</li>
            <li>Partial points awarded for passing some test cases</li>
            <li>Code must be original and written during the hackathon</li>
        </ul>
        
        <h3>Disqualification Rules:</h3>
        <ul>
            <li>Using pre-written code</li>
            <li>Seeking external help</li>
            <li>Violating time limits</li>
            <li>Attempting to cheat or bypass security measures</li>
        </ul>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("AI_HACKBLITZ-XXV Rules and Regulations")
        msg.setTextFormat(Qt.RichText)
        msg.setText(rules)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                min-width: 600px;
                min-height: 400px;
            }
        """)
        msg.exec_()
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("AI_HACKBLITZ-XXV Registration")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Team Information
        team_form = QFormLayout()
        
        self.team_name = QLineEdit()
        team_form.addRow("Team Name:", self.team_name)
        
        # Contestant Information
        contestant_layout = QVBoxLayout()
        contestant_title = QLabel("Contestant Information")
        contestant_title.setFont(QFont("Arial", 12, QFont.Bold))
        contestant_layout.addWidget(contestant_title)
        
        # Create form for each contestant
        self.contestant_forms = []
        for i in range(3):
            form = QFormLayout()
            
            name = QLineEdit()
            email = QLineEdit()
            phone = QLineEdit()
            
            # Make contestant 2 and 3 optional
            if i == 0:
                form.addRow(f"Contestant {i+1} Name (Required):", name)
                form.addRow(f"Contestant {i+1} Email (Required):", email)
                form.addRow(f"Contestant {i+1} Phone (Required):", phone)
            else:
                form.addRow(f"Contestant {i+1} Name (Optional):", name)
                form.addRow(f"Contestant {i+1} Email (Optional):", email)
                form.addRow(f"Contestant {i+1} Phone (Optional):", phone)
            
            self.contestant_forms.append({
                'name': name,
                'email': email,
                'phone': phone
            })
            
            contestant_layout.addLayout(form)
        
        # Submit button
        submit_button = QPushButton("Start Hackathon")
        submit_button.setFont(QFont("Arial", 12))
        submit_button.clicked.connect(self.submit_data)
        layout.addWidget(submit_button)
        
        # Add all layouts to main layout
        layout.addLayout(team_form)
        layout.addLayout(contestant_layout)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
    def submit_data(self):
        # Validate team name
        team_name = self.team_name.text().strip()
        if not team_name:
            QMessageBox.warning(self, "Error", "Please enter a team name")
            return
        
        # Validate first contestant (required)
        first_contestant = self.contestant_forms[0]
        if not all([first_contestant['name'].text().strip(), 
                   first_contestant['email'].text().strip(), 
                   first_contestant['phone'].text().strip()]):
            QMessageBox.warning(self, "Error", "Please fill all details for Contestant 1")
            return
        
        # Save data to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"team_data/{team_name}_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Team Name', team_name])
            writer.writerow(['Registration Time', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([])
            writer.writerow(['Contestant', 'Name', 'Email', 'Phone'])
            
            # Write first contestant (required)
            writer.writerow([
                "Contestant 1",
                first_contestant['name'].text().strip(),
                first_contestant['email'].text().strip(),
                first_contestant['phone'].text().strip()
            ])
            
            # Write optional contestants if they have any data
            for i in range(1, 3):
                contestant = self.contestant_forms[i]
                name = contestant['name'].text().strip()
                email = contestant['email'].text().strip()
                phone = contestant['phone'].text().strip()
                
                # Only write if at least one field is filled
                if any([name, email, phone]):
                    writer.writerow([
                        f"Contestant {i+1}",
                        name,
                        email,
                        phone
                    ])
        
        # Initialize activity logger for the team
        self.logger = ActivityLogger(team_name)
        self.logger.log_activity(
            'Registration',
            'System',
            '',
            'Completed',
            0,
            0,
            'Team registration completed'
        )
        
        # Show success message
        QMessageBox.information(self, "Success", "Team registration successful! Starting hackathon...")
        
        # Hide login window
        self.hide()
        
        # Start hackathon interface
        self.hackathon = HackathonApp(team_name, self.logger)
        self.hackathon.show()
        
        # Connect hackathon close signal to show final results
        self.hackathon.finished.connect(self.show_final_results)
        
    def show_final_results(self):
        # Show final results and logs
        from admin_panel import show_admin_panel
        show_admin_panel()
        self.close()

def show_login_page():
    app = QApplication([])
    window = LoginPage()
    window.show()
    app.exec_() 