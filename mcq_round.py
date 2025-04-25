import sys
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QRadioButton, QButtonGroup, QPushButton, 
                           QScrollArea, QMessageBox, QDialog, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from create_mcq import categories, generate_random_questions

class MCQRound(QMainWindow):
    finished = pyqtSignal(int)  # Signal to emit score when round is finished
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MCQ Round")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        self.questions = []
        self.selected_answers = {}
        self.current_question = 0
        self.score = 0
        self.time_left = 45 * 60  # 45 minutes in seconds
        
        self.load_questions()
        self.setup_ui()
        self.start_timer()
        
    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second
        
    def load_questions(self):
        try:
            # Get questions directly from create_mcq.py
            self.questions = generate_random_questions()
            
            # Initialize selected answers dictionary
            self.selected_answers = {i: None for i in range(len(self.questions))}
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load questions: {str(e)}")
            sys.exit(1)
            
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Timer
        self.timer_label = QLabel("Time Left: 45:00")
        self.timer_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.timer_label.setStyleSheet("color: #2E7D32;")
        header_layout.addWidget(self.timer_label)
        
        # Question counter
        self.question_counter = QLabel(f"Total Questions: {len(self.questions)}")
        self.question_counter.setFont(QFont("Arial", 12))
        header_layout.addWidget(self.question_counter)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for questions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                border: none;
                background: #f0f0f0;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                min-height: 20px;
                border-radius: 5px;
            }
        """)
        
        # Questions container
        self.questions_container = QWidget()
        self.questions_layout = QVBoxLayout()
        self.questions_layout.setSpacing(20)
        self.questions_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create question widgets
        self.question_widgets = []
        self.option_groups = []
        
        for i, question_data in enumerate(self.questions):
            question_widget = QWidget()
            question_layout = QVBoxLayout()
            
            # Question label
            question_label = QLabel(f"{i+1}. {question_data[0]}")
            question_label.setFont(QFont("Arial", 11))
            question_label.setWordWrap(True)
            question_layout.addWidget(question_label)
            
            # Options
            options_group = QButtonGroup(question_widget)
            options = question_data[1:5]  # Get options A to D
            
            for j, option in enumerate(options):
                radio = QRadioButton(f"{chr(65+j)}. {option}")  # A, B, C, D
                radio.setFont(QFont("Arial", 10))
                radio.setStyleSheet("""
                    QRadioButton {
                        padding: 5px;
                        margin: 2px;
                    }
                    QRadioButton:hover {
                        background-color: #f0f0f0;
                    }
                """)
                options_group.addButton(radio, j)
                question_layout.addWidget(radio)
            
            # Connect radio buttons to answer selection
            options_group.buttonClicked.connect(lambda btn, idx=i: self.select_answer(idx, btn))
            
            question_widget.setLayout(question_layout)
            self.questions_layout.addWidget(question_widget)
            self.question_widgets.append(question_widget)
            self.option_groups.append(options_group)
        
        self.questions_container.setLayout(self.questions_layout)
        scroll.setWidget(self.questions_container)
        main_layout.addWidget(scroll)
        
        # Submit button
        submit_button = QPushButton("Submit Answers")
        submit_button.setFont(QFont("Arial", 12, QFont.Bold))
        submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        submit_button.clicked.connect(self.submit_answers)
        main_layout.addWidget(submit_button, alignment=Qt.AlignCenter)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
    def select_answer(self, question_index, button):
        self.selected_answers[question_index] = button.text()[0]  # Store A, B, C, or D
        
    def update_timer(self):
        self.time_left -= 1
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        
        # Update timer color based on remaining time
        if minutes < 5:
            self.timer_label.setStyleSheet("color: #D32F2F;")  # Red for last 5 minutes
        elif minutes < 15:
            self.timer_label.setStyleSheet("color: #FFA000;")  # Orange for last 15 minutes
        else:
            self.timer_label.setStyleSheet("color: #2E7D32;")  # Green otherwise
            
        self.timer_label.setText(f"Time Left: {minutes:02d}:{seconds:02d}")
        
        if self.time_left <= 0:
            self.timer.stop()
            self.submit_answers()
            
    def submit_answers(self):
        # Calculate score
        self.score = 0
        for i, question in enumerate(self.questions):
            correct_answer = question[5]  # Correct answer is at index 5
            if self.selected_answers[i] == correct_answer:
                self.score += 1
                
        # Show score dialog
        score_dialog = QDialog(self)
        score_dialog.setWindowTitle("Round Complete")
        score_dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Score label
        score_label = QLabel(f"Your Score: {self.score}/{len(self.questions)}")
        score_label.setFont(QFont("Arial", 14, QFont.Bold))
        score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(score_label)
        
        # Qualification status
        status_label = QLabel()
        status_label.setFont(QFont("Arial", 12))
        status_label.setAlignment(Qt.AlignCenter)
        
        if self.score >= 15:  # 50% threshold
            status_label.setText("Congratulations! You have qualified for the next round.")
            status_label.setStyleSheet("color: #2E7D32;")
        else:
            status_label.setText("Sorry, you did not qualify for the next round.")
            status_label.setStyleSheet("color: #D32F2F;")
            
        layout.addWidget(status_label)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.close_round(score_dialog))
        layout.addWidget(ok_button)
        
        score_dialog.setLayout(layout)
        score_dialog.exec_()
        
    def close_round(self, dialog):
        dialog.accept()
        self.finished.emit(self.score)
        self.close()
        
    def closeEvent(self, event):
        # Check if there are unanswered questions
        unanswered = sum(1 for ans in self.selected_answers.values() if ans is None)
        if unanswered > 0:
            reply = QMessageBox.question(
                self, 'Confirm Exit',
                f'You have {unanswered} unanswered questions. Are you sure you want to submit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.submit_answers()
                event.accept()
            else:
                event.ignore()
        else:
            self.submit_answers()
            event.accept() 