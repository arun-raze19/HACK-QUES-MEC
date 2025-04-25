import sys
import time
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QRadioButton, QButtonGroup
from PyQt5.QtCore import Qt, QTimer
from pynput import mouse, keyboard
import psutil
import socket
import json
import threading
from mcq_round import MCQRound

class HackathonApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI_HACKBLITZ-XXV")
        self.setGeometry(100, 100, 800, 600)
        
        # Initialize variables
        self.total_score = 0
        self.mcq_score = 0
        self.dsa_score1 = 0
        self.dsa_score2 = 0
        self.last_activity_time = time.time()
        self.is_minimized = False
        self.rounds_completed = {'mcq': False, 'dsa1': False, 'dsa2': False}
        self.mcq_window = None  # Reference to MCQ window
        
        # Setup UI
        self.setup_ui()
        
        # Start monitoring
        self.start_monitoring()
        
        # Setup network communication
        self.setup_network()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Score display
        self.score_label = QLabel("Total Score: 0")
        layout.addWidget(self.score_label)
        
        # Round selection buttons
        self.mcq_button = QPushButton("Start MCQ Round (30 points)")
        self.dsa1_button = QPushButton("Start DSA Round 1 (30 points)")
        self.dsa2_button = QPushButton("Start DSA Round 2 (40 points)")
        
        self.mcq_button.clicked.connect(self.start_mcq)
        self.dsa1_button.clicked.connect(self.start_dsa1)
        self.dsa2_button.clicked.connect(self.start_dsa2)
        
        layout.addWidget(self.mcq_button)
        layout.addWidget(self.dsa1_button)
        layout.addWidget(self.dsa2_button)
        
        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
        
        # Update button states
        self.update_button_states()
        
    def update_button_states(self):
        # Enable/disable buttons based on round completion and scores
        self.mcq_button.setEnabled(not self.rounds_completed['mcq'])
        
        # DSA1 button is enabled only if MCQ is completed with score >= 15
        self.dsa1_button.setEnabled(self.rounds_completed['mcq'] and self.mcq_score >= 15 and not self.rounds_completed['dsa1'])
        
        # DSA2 button is enabled only if DSA1 is completed
        self.dsa2_button.setEnabled(self.rounds_completed['dsa1'] and not self.rounds_completed['dsa2'])
        
        # Update status label
        if not self.rounds_completed['mcq']:
            self.status_label.setText("Status: MCQ Round Available")
        elif self.mcq_score < 15:
            self.status_label.setText("Status: Not Qualified for DSA Rounds (MCQ Score < 15)")
        elif not self.rounds_completed['dsa1']:
            self.status_label.setText("Status: DSA Round 1 Available")
        elif not self.rounds_completed['dsa2']:
            self.status_label.setText("Status: DSA Round 2 Available")
        else:
            self.status_label.setText("Status: All Rounds Completed")
            
    def start_mcq(self):
        if self.mcq_window is None:
            self.mcq_window = MCQRound()
            self.mcq_window.finished.connect(self.mcq_round_finished)
            self.mcq_window.show()
            self.mcq_button.setEnabled(False)  # Disable MCQ button while round is active
        else:
            self.mcq_window.raise_()  # Bring MCQ window to front if it exists
            
    def mcq_round_finished(self, score):
        self.mcq_score = score
        self.total_score += score
        self.rounds_completed['mcq'] = True
        self.mcq_window = None  # Clear reference to MCQ window
        self.update_score_display()
        self.update_button_states()
        self.send_status()
        
        # Show qualification message
        if score >= 15:
            QMessageBox.information(self, "Qualification Status", 
                                  "Congratulations! You have qualified for the DSA rounds.")
        else:
            QMessageBox.warning(self, "Qualification Status", 
                              "You did not qualify for the DSA rounds. Minimum required score is 15.")
        
    def update_score_display(self):
        self.score_label.setText(f"Total Score: {self.total_score}\nMCQ: {self.mcq_score}/30\nDSA1: {self.dsa_score1}/30\nDSA2: {self.dsa_score2}/40")
        
    def start_dsa1(self):
        # Create DSA1 dialog
        dialog = QWidget()
        dialog.setWindowTitle("DSA Round 1")
        dialog.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()
        
        # Add DSA problem 1
        problem_label = QLabel("Problem 1: Implement a function to find the longest substring without repeating characters.")
        layout.addWidget(problem_label)
        
        # Add code editor or input field here
        # For now, we'll just simulate a score
        score = 20  # This should be calculated based on actual solution
        
        dialog.setLayout(layout)
        dialog.exec_()
        
        # Update scores
        self.dsa_score1 = score
        self.total_score += score
        self.rounds_completed['dsa1'] = True
        self.update_score_display()
        self.update_button_states()
        self.send_status()
        
    def start_dsa2(self):
        # Create DSA2 dialog
        dialog = QWidget()
        dialog.setWindowTitle("DSA Round 2")
        dialog.setGeometry(200, 200, 600, 400)
        layout = QVBoxLayout()
        
        # Add DSA problem 2
        problem_label = QLabel("Problem 2: Implement a function to find the median of two sorted arrays.")
        layout.addWidget(problem_label)
        
        # Add code editor or input field here
        # For now, we'll just simulate a score
        score = 30  # This should be calculated based on actual solution
        
        dialog.setLayout(layout)
        dialog.exec_()
        
        # Update scores
        self.dsa_score2 = score
        self.total_score += score
        self.rounds_completed['dsa2'] = True
        self.update_score_display()
        self.update_button_states()
        self.send_status()
        
    def start_monitoring(self):
        # Mouse monitoring
        self.mouse_listener = mouse.Listener(on_move=self.on_mouse_move)
        self.mouse_listener.start()
        
        # Keyboard monitoring
        self.keyboard_listener = keyboard.Listener(on_press=self.on_key_press)
        self.keyboard_listener.start()
        
        # Activity timer
        self.activity_timer = QTimer()
        self.activity_timer.timeout.connect(self.check_activity)
        self.activity_timer.start(1000)  # Check every second
        
    def on_mouse_move(self, x, y):
        self.last_activity_time = time.time()
        
    def on_key_press(self, key):
        self.last_activity_time = time.time()
        
    def check_activity(self):
        current_time = time.time()
        if current_time - self.last_activity_time > 60:  # 1 minute of inactivity
            self.penalize_score(1)  # Penalize 1 point per minute of inactivity
            
    def setup_network(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(('localhost', 5000))  # Connect to admin server
        except:
            print("Could not connect to admin server")
            
    def send_status(self):
        status = {
            'score': self.total_score,
            'mcq_score': self.mcq_score,
            'dsa1_score': self.dsa_score1,
            'dsa2_score': self.dsa_score2,
            'activity': self.last_activity_time,
            'is_minimized': self.is_minimized,
            'rounds_completed': self.rounds_completed
        }
        try:
            self.socket.send(json.dumps(status).encode())
        except:
            pass
            
    def penalize_score(self, points):
        self.total_score = max(0, self.total_score - points)
        self.update_score_display()
        self.send_status()
        
    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            if self.isMinimized():
                self.is_minimized = True
                self.penalize_score(10)
            else:
                self.is_minimized = False
                
    def closeEvent(self, event):
        self.penalize_score(10)
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HackathonApp()
    window.show()
    sys.exit(app.exec_()) 