import csv
import random
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QRadioButton, 
                           QButtonGroup, QPushButton, QMessageBox, QScrollArea,
                           QProgressBar, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer, QTime, pyqtSignal
from datetime import datetime, timedelta

class MCQRound(QWidget):
    finished = pyqtSignal(int)  # Signal to emit when round is finished
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MCQ Round - AI_HACKBLITZ-XXV")
        self.setGeometry(200, 200, 1000, 800)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        self.questions = []
        self.current_question = None
        self.score = 0
        self.start_time = None
        self.end_time = None
        self.button_groups = []
        
        # Timer setup
        self.time_left = 45 * 60  # 45 minutes in seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        
        self.load_questions()
        self.setup_ui()
        
        # Start timer
        self.timer.start(1000)  # Update every second
        
    def load_questions(self):
        try:
            with open('mcq.csv', 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                all_questions = []
                for row in reader:
                    if len(row) >= 6:  # Ensure row has all required fields
                        question = {
                            'question': row[0].strip(),
                            'options': {
                                'A': row[1].strip(),
                                'B': row[2].strip(),
                                'C': row[3].strip(),
                                'D': row[4].strip()
                            },
                            'correct': row[5].strip().upper()
                        }
                        # Validate correct answer format
                        if question['correct'] in ['A', 'B', 'C', 'D']:
                            all_questions.append(question)
                
                if not all_questions:
                    raise ValueError("No valid questions found in the CSV file")
                
                # Randomly select 30 questions from the pool
                self.questions = random.sample(all_questions, min(30, len(all_questions)))
                print(f"Loaded {len(self.questions)} questions")
                
        except Exception as e:
            print(f"Failed to load questions: {str(e)}")
            raise

    def setup_ui(self):
        main_layout = QVBoxLayout()
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Timer display
        timer_layout = QVBoxLayout()
        self.timer_label = QLabel("Time Remaining: 45:00")
        self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        timer_layout.addWidget(self.timer_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(45 * 60)
        self.progress_bar.setValue(45 * 60)
        self.progress_bar.setTextVisible(False)
        timer_layout.addWidget(self.progress_bar)
        
        header_layout.addLayout(timer_layout)
        
        # Question counter
        self.question_counter = QLabel(f"Questions: 1/{len(self.questions)}")
        self.question_counter.setStyleSheet("font-size: 16px; font-weight: bold;")
        header_layout.addWidget(self.question_counter)
        
        main_layout.addLayout(header_layout)
        
        # Create scroll area for questions
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        
        # Add questions
        for i, q in enumerate(self.questions):
            question_group = QWidget()
            question_layout = QVBoxLayout()
            
            # Question label
            question_label = QLabel(f"{i+1}. {q['question']}")
            question_label.setWordWrap(True)
            question_label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
            question_layout.addWidget(question_label)
            
            # Options
            button_group = QButtonGroup()
            for option_key, option_text in q['options'].items():
                radio = QRadioButton(f"{option_key}. {option_text}")
                radio.setStyleSheet("font-size: 13px; margin-left: 20px;")
                button_group.addButton(radio)
                question_layout.addWidget(radio)
                
            self.button_groups.append(button_group)
            question_group.setLayout(question_layout)
            self.scroll_layout.addWidget(question_group)
            
        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        
        # Submit button
        button_layout = QHBoxLayout()
        self.submit_button = QPushButton("Submit Answers")
        self.submit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 16px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.submit_button.clicked.connect(self.calculate_score)
        button_layout.addWidget(self.submit_button)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        
    def update_timer(self):
        self.time_left -= 1
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        
        # Update timer label
        self.timer_label.setText(f"Time Remaining: {minutes:02d}:{seconds:02d}")
        
        # Update progress bar
        self.progress_bar.setValue(self.time_left)
        
        # Change color based on time remaining
        if self.time_left <= 5 * 60:  # Last 5 minutes
            self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: red;")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: red; }")
        elif self.time_left <= 15 * 60:  # Last 15 minutes
            self.timer_label.setStyleSheet("font-size: 16px; font-weight: bold; color: orange;")
            self.progress_bar.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
            
        # Auto-submit when time is up
        if self.time_left <= 0:
            self.timer.stop()
            QMessageBox.warning(self, "Time's Up!", "The time for MCQ round has ended. Your answers will be submitted automatically.")
            self.calculate_score()
            
    def calculate_score(self):
        # Stop the timer
        self.timer.stop()
        
        self.score = 0
        for i, (q, button_group) in enumerate(zip(self.questions, self.button_groups)):
            checked_button = button_group.checkedButton()
            if checked_button:
                selected_option = checked_button.text()[0]  # Get the option letter (A, B, C, D)
                if selected_option == q['correct']:
                    self.score += 1
                
        # Show score
        QMessageBox.information(self, "MCQ Round Complete", 
                              f"Your score: {self.score}/30\n"
                              f"You need at least 15 points to qualify for DSA rounds.")
        
        # Emit finished signal with score
        self.finished.emit(self.score)
        
        # Close the window
        self.close()
        
    def closeEvent(self, event):
        # Stop the timer
        self.timer.stop()
        
        # Ensure all questions are answered
        unanswered = [i+1 for i, group in enumerate(self.button_groups) 
                     if not group.checkedButton()]
        
        if unanswered:
            reply = QMessageBox.question(self, 'Unanswered Questions',
                                       f'You have unanswered questions: {unanswered}\n'
                                       'Are you sure you want to submit?',
                                       QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            
            if reply == QMessageBox.No:
                event.ignore()
                return
                
        event.accept() 