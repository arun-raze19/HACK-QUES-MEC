import socket
import json
import threading
import time
from datetime import datetime

class HackathonClient:
    def __init__(self, team_name, admin_host='localhost', admin_port=5000):
        self.team_name = team_name
        self.admin_host = admin_host
        self.admin_port = admin_port
        self.socket = None
        self.connected = False
        self.scores = {
            'mcq_score': 0,
            'dsa1_score': 0,
            'dsa2_score': 0,
            'total_score': 0,
            'status': 'In Progress'
        }
        
    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.admin_host, self.admin_port))
            self.connected = True
            print(f"Connected to admin panel at {self.admin_host}:{self.admin_port}")
            return True
        except Exception as e:
            print(f"Failed to connect to admin panel: {e}")
            return False
            
    def send_update(self):
        if not self.connected:
            return False
            
        try:
            data = {
                'team_name': self.team_name,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'mcq_score': self.scores['mcq_score'],
                'dsa1_score': self.scores['dsa1_score'],
                'dsa2_score': self.scores['dsa2_score'],
                'total_score': self.scores['total_score'],
                'status': self.scores['status']
            }
            
            self.socket.send(json.dumps(data).encode())
            return True
        except Exception as e:
            print(f"Failed to send update: {e}")
            self.connected = False
            return False
            
    def update_scores(self, mcq_score=None, dsa1_score=None, dsa2_score=None, status=None):
        if mcq_score is not None:
            self.scores['mcq_score'] = mcq_score
        if dsa1_score is not None:
            self.scores['dsa1_score'] = dsa1_score
        if dsa2_score is not None:
            self.scores['dsa2_score'] = dsa2_score
        if status is not None:
            self.scores['status'] = status
            
        # Calculate total score
        self.scores['total_score'] = (
            self.scores['mcq_score'] +
            self.scores['dsa1_score'] +
            self.scores['dsa2_score']
        )
        
        # Send update to admin panel
        self.send_update()
        
    def start_heartbeat(self):
        def heartbeat():
            while self.connected:
                try:
                    self.send_update()
                    time.sleep(30)  # Send heartbeat every 30 seconds
                except:
                    self.connected = False
                    break
                    
        heartbeat_thread = threading.Thread(target=heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
        
    def close(self):
        if self.socket:
            self.socket.close()
        self.connected = False 