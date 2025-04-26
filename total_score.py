from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TotalScore(QMainWindow):
    def __init__(self, mcq_score=0, dsa1_score=0, dsa2_score=0):
        super().__init__()
        self.setWindowTitle("Total Score")
        self.setGeometry(100, 100, 600, 400)
        
        # Scores
        self.mcq_score = mcq_score
        self.dsa1_score = dsa1_score
        self.dsa2_score = dsa2_score
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Final Score Summary")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Individual scores
        mcq_label = QLabel(f"MCQ Round: {self.mcq_score}/30")
        mcq_label.setFont(QFont("Arial", 12))
        layout.addWidget(mcq_label)
        
        dsa1_label = QLabel(f"DSA Round 1: {self.dsa1_score}/30")
        dsa1_label.setFont(QFont("Arial", 12))
        layout.addWidget(dsa1_label)
        
        dsa2_label = QLabel(f"DSA Round 2: {self.dsa2_score}/40")
        dsa2_label.setFont(QFont("Arial", 12))
        layout.addWidget(dsa2_label)
        
        # Total score
        total_score = self.mcq_score + self.dsa1_score + self.dsa2_score
        total_label = QLabel(f"Total Score: {total_score}/100")
        total_label.setFont(QFont("Arial", 14, QFont.Bold))
        total_label.setStyleSheet("color: #2E7D32;")
        layout.addWidget(total_label)
        
        # Percentage
        percentage = (total_score / 100) * 100
        percentage_label = QLabel(f"Percentage: {percentage:.2f}%")
        percentage_label.setFont(QFont("Arial", 12))
        layout.addWidget(percentage_label)
        
        # Close button
        close_button = QPushButton("Close")
        close_button.setFont(QFont("Arial", 12))
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

def show_total_score(mcq_score=0, dsa1_score=0, dsa2_score=0):
    app = QApplication([])
    window = TotalScore(mcq_score, dsa1_score, dsa2_score)
    window.show()
    app.exec_() 