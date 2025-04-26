import warnings
import socket
import threading
import json
import os
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QTableWidget, QTableWidgetItem, QPushButton,
                           QHBoxLayout, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class AdminServer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI_HACKBLITZ-XXV Admin Panel")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0', 5000))
        self.server.listen(60)  # Listen for up to 60 connections
        
        # Store connected clients and their data
        self.clients = {}
        self.client_scores = {}
        
        # Create logs directory if it doesn't exist
        if not os.path.exists('admin_logs'):
            os.makedirs('admin_logs')
        
        self.setup_ui()
        self.start_server()
        
    def setup_ui(self):
        main_widget = QWidget()
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("AI_HACKBLITZ-XXV Admin Panel")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("Server Status: Running")
        self.status_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.status_label)
        
        # Connected clients count
        self.clients_label = QLabel("Connected Clients: 0")
        self.clients_label.setFont(QFont("Arial", 12))
        layout.addWidget(self.clients_label)
        
        # Teams table
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(7)
        self.teams_table.setHorizontalHeaderLabels([
            "Team Name", "System IP", "MCQ Score", "DSA1 Score", 
            "DSA2 Score", "Total Score", "Status"
        ])
        self.teams_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 5px;
                border: 1px solid #ccc;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.teams_table)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        refresh_button = QPushButton("Refresh")
        refresh_button.setFont(QFont("Arial", 12))
        refresh_button.clicked.connect(self.refresh_data)
        button_layout.addWidget(refresh_button)
        
        export_button = QPushButton("Export Results")
        export_button.setFont(QFont("Arial", 12))
        export_button.clicked.connect(self.export_results)
        button_layout.addWidget(export_button)
        
        layout.addLayout(button_layout)
        
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)
        
        # Set up refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
    def start_server(self):
        # Start server in a separate thread
        server_thread = threading.Thread(target=self.accept_connections)
        server_thread.daemon = True
        server_thread.start()
        
    def accept_connections(self):
        while True:
            try:
                client_socket, address = self.server.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
            except Exception as e:
                print(f"Error accepting connection: {e}")
                
    def handle_client(self, client_socket, address):
        try:
            while True:
                data = client_socket.recv(4096).decode()
                if not data:
                    break
                    
                # Parse client data
                client_data = json.loads(data)
                team_name = client_data.get('team_name')
                
                if team_name:
                    # Update client data
                    self.clients[team_name] = {
                        'socket': client_socket,
                        'address': address,
                        'data': client_data
                    }
                    
                    # Update scores
                    self.client_scores[team_name] = {
                        'mcq_score': client_data.get('mcq_score', 0),
                        'dsa1_score': client_data.get('dsa1_score', 0),
                        'dsa2_score': client_data.get('dsa2_score', 0),
                        'total_score': client_data.get('total_score', 0),
                        'status': client_data.get('status', 'In Progress')
                    }
                    
                    # Log client data
                    self.log_client_data(team_name, client_data)
                    
                    # Update UI
                    self.update_ui()
                    
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            if team_name in self.clients:
                del self.clients[team_name]
            if team_name in self.client_scores:
                del self.client_scores[team_name]
            self.update_ui()
            
    def log_client_data(self, team_name, data):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"admin_logs/{team_name}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
            
    def update_ui(self):
        # Update connected clients count
        self.clients_label.setText(f"Connected Clients: {len(self.clients)}")
        
        # Update teams table
        self.teams_table.setRowCount(len(self.client_scores))
        for i, (team_name, scores) in enumerate(self.client_scores.items()):
            self.teams_table.setItem(i, 0, QTableWidgetItem(team_name))
            self.teams_table.setItem(i, 1, QTableWidgetItem(str(scores.get('address', ''))))
            self.teams_table.setItem(i, 2, QTableWidgetItem(str(scores.get('mcq_score', 0))))
            self.teams_table.setItem(i, 3, QTableWidgetItem(str(scores.get('dsa1_score', 0))))
            self.teams_table.setItem(i, 4, QTableWidgetItem(str(scores.get('dsa2_score', 0))))
            self.teams_table.setItem(i, 5, QTableWidgetItem(str(scores.get('total_score', 0))))
            self.teams_table.setItem(i, 6, QTableWidgetItem(scores.get('status', 'In Progress')))
            
    def refresh_data(self):
        self.update_ui()
        
    def export_results(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"admin_logs/final_results_{timestamp}.csv"
        
        try:
            with open(filename, 'w') as f:
                f.write("Team Name,MCQ Score,DSA1 Score,DSA2 Score,Total Score,Status\n")
                for team_name, scores in self.client_scores.items():
                    f.write(f"{team_name},{scores['mcq_score']},{scores['dsa1_score']},"
                           f"{scores['dsa2_score']},{scores['total_score']},{scores['status']}\n")
            
            QMessageBox.information(self, "Success", 
                                  f"Results exported to {filename}")
        except Exception as e:
            QMessageBox.critical(self, "Error", 
                               f"Failed to export results: {str(e)}")
            
    def closeEvent(self, event):
        self.server.close()
        event.accept()

def show_admin_panel():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        app = QApplication([])
        window = AdminServer()
        window.show()
        app.exec_()

if __name__ == "__main__":
    show_admin_panel() 