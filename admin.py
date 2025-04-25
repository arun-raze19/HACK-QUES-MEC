import socket
import json
import threading
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QTableWidget, QTableWidgetItem, QPushButton, QTabWidget,
                           QGroupBox, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
import psutil
import platform
import os
import sys

class NetworkMonitor(QObject):
    status_update = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.clients = {}
        self.server = None
        self.running = False
        
    def start_server(self, host='0.0.0.0', port=5000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(60)  # Allow up to 60 connections
        self.running = True
        
        # Start accepting connections
        threading.Thread(target=self.accept_connections, daemon=True).start()
        
    def accept_connections(self):
        while self.running:
            try:
                client, address = self.server.accept()
                client_id = f"{address[0]}:{address[1]}"
                self.clients[client_id] = {
                    'socket': client,
                    'data': None,
                    'last_update': time.time(),
                    'status': 'Connected'
                }
                threading.Thread(target=self.handle_client, args=(client_id,), daemon=True).start()
            except:
                break
                
    def handle_client(self, client_id):
        client = self.clients[client_id]['socket']
        while self.running:
            try:
                data = client.recv(4096)
                if not data:
                    break
                status = json.loads(data.decode())
                self.clients[client_id]['data'] = status
                self.clients[client_id]['last_update'] = time.time()
                self.status_update.emit({client_id: status})
            except:
                break
        if client_id in self.clients:
            del self.clients[client_id]
            
    def stop_server(self):
        self.running = False
        if self.server:
            self.server.close()

class AdminApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI_HACKBLITZ-XXV Admin Panel")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize network monitor
        self.monitor = NetworkMonitor()
        self.monitor.status_update.connect(self.update_team_status)
        
        # Setup UI
        self.setup_ui()
        
        # Start monitoring
        self.monitor.start_server()
        
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Teams Overview Tab
        teams_tab = QWidget()
        teams_layout = QVBoxLayout()
        
        # Teams table
        self.teams_table = QTableWidget()
        self.teams_table.setColumnCount(8)
        self.teams_table.setHorizontalHeaderLabels([
            'Team ID', 'IP Address', 'Total Score', 'MCQ Score', 
            'DSA1 Score', 'DSA2 Score', 'Status', 'Last Activity'
        ])
        teams_layout.addWidget(self.teams_table)
        
        # Statistics group
        stats_group = QGroupBox("Statistics")
        stats_layout = QGridLayout()
        
        self.total_teams_label = QLabel("Total Teams: 0")
        self.active_teams_label = QLabel("Active Teams: 0")
        self.qualified_teams_label = QLabel("Qualified Teams: 0")
        self.avg_score_label = QLabel("Average Score: 0")
        
        stats_layout.addWidget(self.total_teams_label, 0, 0)
        stats_layout.addWidget(self.active_teams_label, 0, 1)
        stats_layout.addWidget(self.qualified_teams_label, 1, 0)
        stats_layout.addWidget(self.avg_score_label, 1, 1)
        
        stats_group.setLayout(stats_layout)
        teams_layout.addWidget(stats_group)
        
        teams_tab.setLayout(teams_layout)
        
        # Network Monitor Tab
        network_tab = QWidget()
        network_layout = QVBoxLayout()
        
        # Network status
        network_status = QGroupBox("Network Status")
        network_status_layout = QGridLayout()
        
        self.network_usage_label = QLabel("Network Usage: 0%")
        self.connected_clients_label = QLabel("Connected Clients: 0")
        self.bandwidth_label = QLabel("Bandwidth Usage: 0 KB/s")
        
        network_status_layout.addWidget(self.network_usage_label, 0, 0)
        network_status_layout.addWidget(self.connected_clients_label, 0, 1)
        network_status_layout.addWidget(self.bandwidth_label, 1, 0)
        
        network_status.setLayout(network_status_layout)
        network_layout.addWidget(network_status)
        
        network_tab.setLayout(network_layout)
        
        # Add tabs
        tabs.addTab(teams_tab, "Teams Overview")
        tabs.addTab(network_tab, "Network Monitor")
        
        layout.addWidget(tabs)
        central_widget.setLayout(layout)
        
        # Setup update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_network_stats)
        self.update_timer.start(1000)  # Update every second
        
    def update_team_status(self, status_data):
        for client_id, status in status_data.items():
            row = self.find_team_row(client_id)
            if row == -1:
                row = self.teams_table.rowCount()
                self.teams_table.insertRow(row)
                
            # Update team data
            ip_address = client_id.split(':')[0]
            self.teams_table.setItem(row, 0, QTableWidgetItem(client_id))
            self.teams_table.setItem(row, 1, QTableWidgetItem(ip_address))
            self.teams_table.setItem(row, 2, QTableWidgetItem(str(status['score'])))
            self.teams_table.setItem(row, 3, QTableWidgetItem(str(status['mcq_score'])))
            self.teams_table.setItem(row, 4, QTableWidgetItem(str(status['dsa1_score'])))
            self.teams_table.setItem(row, 5, QTableWidgetItem(str(status['dsa2_score'])))
            
            # Update status
            status_text = "Active"
            if status['is_minimized']:
                status_text = "Minimized"
            if not status['rounds_completed']['mcq']:
                status_text = "In MCQ Round"
            elif status['mcq_score'] < 15:
                status_text = "Not Qualified"
            elif not status['rounds_completed']['dsa1']:
                status_text = "In DSA Round 1"
            elif not status['rounds_completed']['dsa2']:
                status_text = "In DSA Round 2"
            else:
                status_text = "Completed"
                
            self.teams_table.setItem(row, 6, QTableWidgetItem(status_text))
            self.teams_table.setItem(row, 7, QTableWidgetItem(
                time.strftime('%H:%M:%S', time.localtime(status['activity']))
            ))
            
        self.update_statistics()
        
    def find_team_row(self, client_id):
        for row in range(self.teams_table.rowCount()):
            if self.teams_table.item(row, 0).text() == client_id:
                return row
        return -1
        
    def update_statistics(self):
        total_teams = self.teams_table.rowCount()
        active_teams = sum(1 for row in range(total_teams) 
                          if self.teams_table.item(row, 6).text() != "Not Qualified")
        qualified_teams = sum(1 for row in range(total_teams) 
                            if int(self.teams_table.item(row, 3).text()) >= 15)
        
        total_score = sum(int(self.teams_table.item(row, 2).text()) 
                         for row in range(total_teams))
        avg_score = total_score / total_teams if total_teams > 0 else 0
        
        self.total_teams_label.setText(f"Total Teams: {total_teams}")
        self.active_teams_label.setText(f"Active Teams: {active_teams}")
        self.qualified_teams_label.setText(f"Qualified Teams: {qualified_teams}")
        self.avg_score_label.setText(f"Average Score: {avg_score:.2f}")
        
    def update_network_stats(self):
        # Update network statistics
        net_io = psutil.net_io_counters()
        self.bandwidth_label.setText(f"Bandwidth Usage: {net_io.bytes_sent + net_io.bytes_recv} bytes/s")
        self.connected_clients_label.setText(f"Connected Clients: {len(self.monitor.clients)}")
        
        # Check for inactive clients
        current_time = time.time()
        for client_id, client_data in list(self.monitor.clients.items()):
            if current_time - client_data['last_update'] > 30:  # 30 seconds timeout
                row = self.find_team_row(client_id)
                if row != -1:
                    self.teams_table.setItem(row, 6, QTableWidgetItem("Disconnected"))
                    
    def closeEvent(self, event):
        self.monitor.stop_server()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminApp()
    window.show()
    sys.exit(app.exec_()) 