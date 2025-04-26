from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from mcq_round import MCQRound
from dsa_round1 import DSARound1
from dsa_round2 import DSARound2
from datetime import datetime
from hackathon_client import HackathonClient

class HackathonApp(QMainWindow):
    finished = pyqtSignal()  # Signal to indicate hackathon completion
    
    def __init__(self, team_name, logger):
        super().__init__()
        self.team_name = team_name
        self.logger = logger
        self.setWindowTitle(f"Hackathon - {team_name}")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize variables
        self.total_score = 0
        self.mcq_score = 0
        self.dsa1_score = 0
        self.dsa2_score = 0
        self.rounds_completed = {'mcq': False, 'dsa1': False, 'dsa2': False}
        self.start_time = datetime.now()
        
        # Initialize admin client
        self.admin_client = HackathonClient(team_name)
        if self.admin_client.connect():
            self.admin_client.start_heartbeat()
        
        self.setup_ui()
        
    def setup_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel(f"Welcome {self.team_name}!")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Score display
        self.score_label = QLabel("Total Score: 0")
        self.score_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.score_label)
        
        # Round buttons
        self.mcq_button = QPushButton("Start MCQ Round (30 points)")
        self.mcq_button.setFont(QFont("Arial", 12))
        self.mcq_button.clicked.connect(self.start_mcq)
        layout.addWidget(self.mcq_button)
        
        self.dsa1_button = QPushButton("Start DSA Round 1 (30 points)")
        self.dsa1_button.setFont(QFont("Arial", 12))
        self.dsa1_button.clicked.connect(self.start_dsa1)
        layout.addWidget(self.dsa1_button)
        
        self.dsa2_button = QPushButton("Start DSA Round 2 (40 points)")
        self.dsa2_button.setFont(QFont("Arial", 12))
        self.dsa2_button.clicked.connect(self.start_dsa2)
        layout.addWidget(self.dsa2_button)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
        # Update button states
        self.update_button_states()
        
    def update_button_states(self):
        # Enable/disable buttons based on round completion
        self.mcq_button.setEnabled(not self.rounds_completed['mcq'])
        self.dsa1_button.setEnabled(self.rounds_completed['mcq'] and not self.rounds_completed['dsa1'])
        self.dsa2_button.setEnabled(self.rounds_completed['dsa1'] and not self.rounds_completed['dsa2'])
        
        # Update status label
        if not self.rounds_completed['mcq']:
            self.status_label.setText("Status: MCQ Round Available")
        elif not self.rounds_completed['dsa1']:
            self.status_label.setText("Status: DSA Round 1 Available")
        elif not self.rounds_completed['dsa2']:
            self.status_label.setText("Status: DSA Round 2 Available")
        else:
            self.status_label.setText("Status: All Rounds Completed")
            self.show_completion_dialog()
            self.finished.emit()  # Emit finished signal when all rounds are complete
            
    def show_completion_dialog(self):
        # Calculate total time taken
        end_time = datetime.now()
        time_taken = end_time - self.start_time
        hours = time_taken.seconds // 3600
        minutes = (time_taken.seconds % 3600) // 60
        seconds = time_taken.seconds % 60
        
        # Create completion message
        completion_msg = f"""
        <h2>Congratulations! 🎉</h2>
        <p>You have successfully completed AI_HACKBLITZ-XXV!</p>
        
        <h3>Final Results:</h3>
        <ul>
            <li>Total Score: {self.total_score}/100</li>
            <li>MCQ Round: {self.mcq_score}/30</li>
            <li>DSA Round 1: {self.dsa1_score}/30</li>
            <li>DSA Round 2: {self.dsa2_score}/40</li>
        </ul>
        
        <h3>Time Taken:</h3>
        <p>{hours:02d}:{minutes:02d}:{seconds:02d}</p>
        
        <p>Thank you for participating in AI_HACKBLITZ-XXV!</p>
        """
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Hackathon Complete!")
        msg.setTextFormat(Qt.RichText)
        msg.setText(completion_msg)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                min-width: 400px;
                min-height: 300px;
            }
        """)
        msg.exec_()
        
    def start_mcq(self):
        self.logger.log_activity(
            'MCQ',
            'System',
            '',
            'Started',
            0,
            0,
            'MCQ round started'
        )
        self.mcq_window = MCQRound(self.team_name, self.logger)
        self.mcq_window.finished.connect(self.mcq_round_finished)
        self.mcq_window.show()
        self.mcq_button.setEnabled(False)
        
    def mcq_round_finished(self, score):
        self.mcq_score = score
        self.total_score += score
        self.rounds_completed['mcq'] = True
        self.logger.log_activity(
            'MCQ',
            'System',
            '',
            'Completed',
            score,
            0,
            f'MCQ round completed with score: {score}/30'
        )
        self.update_score_display()
        self.update_button_states()
        
        # Update admin panel
        self.admin_client.update_scores(mcq_score=score)
        
        QMessageBox.information(self, "Round Complete", 
                              f"MCQ Round completed with score: {score}/30")
        
    def start_dsa1(self):
        self.logger.log_activity(
            'DSA1',
            'System',
            '',
            'Started',
            0,
            0,
            'DSA Round 1 started'
        )
        self.dsa1_window = DSARound1(self.team_name, self.logger)
        self.dsa1_window.finished.connect(self.dsa1_round_finished)
        self.dsa1_window.show()
        self.dsa1_button.setEnabled(False)
        
    def dsa1_round_finished(self, score):
        self.dsa1_score = score
        self.total_score += score
        self.rounds_completed['dsa1'] = True
        self.logger.log_activity(
            'DSA1',
            'System',
            '',
            'Completed',
            score,
            0,
            f'DSA Round 1 completed with score: {score}/30'
        )
        self.update_score_display()
        self.update_button_states()
        
        # Update admin panel
        self.admin_client.update_scores(dsa1_score=score)
        
        QMessageBox.information(self, "Round Complete", 
                              f"DSA Round 1 completed with score: {score}/30")
        
    def start_dsa2(self):
        self.logger.log_activity(
            'DSA2',
            'System',
            '',
            'Started',
            0,
            0,
            'DSA Round 2 started'
        )
        self.dsa2_window = DSARound2(self.team_name, self.logger)
        self.dsa2_window.finished.connect(self.dsa2_round_finished)
        self.dsa2_window.show()
        self.dsa2_button.setEnabled(False)
        
    def dsa2_round_finished(self, score):
        self.dsa2_score = score
        self.total_score += score
        self.rounds_completed['dsa2'] = True
        self.logger.log_activity(
            'DSA2',
            'System',
            '',
            'Completed',
            score,
            0,
            f'DSA Round 2 completed with score: {score}/40'
        )
        self.update_score_display()
        self.update_button_states()
        
        # Update admin panel
        self.admin_client.update_scores(dsa2_score=score, status='Completed')
        
        # Log final performance review
        self.logger.log_activity(
            'Final',
            'System',
            '',
            'Completed',
            self.total_score,
            0,
            f'Final Score: {self.total_score}\n'
            f'MCQ: {self.mcq_score}/30\n'
            f'DSA1: {self.dsa1_score}/30\n'
            f'DSA2: {self.dsa2_score}/40'
        )
        
    def update_score_display(self):
        self.score_label.setText(
            f"Total Score: {self.total_score}\n"
            f"MCQ: {self.mcq_score}/30\n"
            f"DSA1: {self.dsa1_score}/30\n"
            f"DSA2: {self.dsa2_score}/40"
        )
        
    def closeEvent(self, event):
        self.admin_client.close()
        self.finished.emit()
        super().closeEvent(event) 