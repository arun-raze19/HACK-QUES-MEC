import sys
import random
import subprocess
import tempfile
import os
import platform
import json
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QLabel, QPushButton, QScrollArea, QMessageBox, 
                           QDialog, QHBoxLayout, QTextEdit, QComboBox)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont, QColor
from datetime import datetime

class DSARound2(QMainWindow):
    finished = pyqtSignal(int)  # Signal to emit score when round is finished
    
    def __init__(self, team_name, logger):
        super().__init__()
        self.team_name = team_name
        self.logger = logger
        self.setWindowTitle("DSA Round 2")
        self.setGeometry(100, 100, 1000, 800)
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        
        # Detect Python interpreters
        self.python_interpreters = self.detect_python_interpreters()
        
        self.questions = self.get_questions()
        self.current_question = 0
        self.score = 0
        self.time_left = 45 * 60  # 45 minutes in seconds
        self.start_time = datetime.now()
        self.user_answers = {}
        
        self.setup_ui()
        self.start_timer()
        
        # Log round start
        self.logger.log_activity(
            'DSA2',
            'System',
            '',
            'Started',
            0,
            0,
            'DSA Round 2 started'
        )
        
    def detect_python_interpreters(self):
        interpreters = {}
        possible_paths = {
            'Windows': {
                'python': ['python', 'py'],
                'python3': ['python3', 'py -3']
            },
            'Linux': {
                'python': ['python', 'python2'],
                'python3': ['python3']
            },
            'Darwin': {  # macOS
                'python': ['python', 'python2'],
                'python3': ['python3']
            }
        }
        
        system = platform.system()
        if system in possible_paths:
            for version, paths in possible_paths[system].items():
                for path in paths:
                    try:
                        result = subprocess.run(
                            [path, '--version'],
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            interpreters[version] = path
                            break
                    except:
                        continue
        
        return interpreters

    def get_questions(self):
        # Pool of 5 moderate-level problems with test cases
        problem_pool = [
            {
                "question": "Implement a function to find the number of islands in a 2D grid. An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.",
                "input_format": "The function should take a 2D grid of '1's (land) and '0's (water) as input.",
                "output_format": "Return the number of islands.",
                "test_cases": [
                    {"input": "[[1,1,1,1,0],[1,1,0,1,0],[1,1,0,0,0],[0,0,0,0,0]]", "output": "1", "points": 3.33},
                    {"input": "[[1,1,0,0,0],[1,1,0,0,0],[0,0,1,0,0],[0,0,0,1,1]]", "output": "3", "points": 3.33},
                    {"input": "[[1,0,1,0,1],[0,1,0,1,0],[1,0,1,0,1],[0,1,0,1,0]]", "output": "10", "points": 3.33},
                    {"input": "[[1,1,1],[0,1,0],[1,1,1]]", "output": "1", "points": 3.33},
                    {"input": "[[1,0,1,0,1],[1,0,1,0,1],[1,1,1,1,1]]", "output": "1", "points": 3.33},
                    {"input": "[[1,1,1,1,1],[1,0,0,0,1],[1,0,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]", "output": "2", "points": 3.33},
                    {"input": "[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]", "output": "0", "points": 3.33},
                    {"input": "[[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]]", "output": "1", "points": 3.33},
                    {"input": "[[1,0,1,0,1],[0,1,0,1,0],[1,0,1,0,1],[0,1,0,1,0],[1,0,1,0,1]]", "output": "13", "points": 3.33},
                    {"input": "[[1,1,0,0,0,0],[1,1,0,0,0,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,0,0,0,1,1],[0,0,0,0,1,1]]", "output": "3", "points": 3.33},
                    {"input": "[[1,0,0,0,0,1],[0,1,0,0,1,0],[0,0,1,1,0,0],[0,0,1,1,0,0],[0,1,0,0,1,0],[1,0,0,0,0,1]]", "output": "6", "points": 3.33},
                    {"input": "[[1,1,1,0,0,0],[1,0,1,0,0,0],[1,1,1,0,0,0],[0,0,0,1,1,1],[0,0,0,1,0,1],[0,0,0,1,1,1]]", "output": "2", "points": 3.33}
                ],
                "total_points": 40
            },
            {
                "question": "Implement a function to find the minimum number of coins needed to make up a given amount using coins of given denominations.",
                "input_format": "The function should take an array of coin denominations and the target amount as input.",
                "output_format": "Return the minimum number of coins needed to make up the amount. If it's not possible, return -1.",
                "test_cases": [
                    {"input": "[1,2,5]\n11", "output": "3", "points": 3.33},
                    {"input": "[2]\n3", "output": "-1", "points": 3.33},
                    {"input": "[1,2,5,10,20,50,100]\n73", "output": "4", "points": 3.33},
                    {"input": "[1,3,4,5]\n7", "output": "2", "points": 3.33},
                    {"input": "[1,2,5,10]\n18", "output": "4", "points": 3.33},
                    {"input": "[1,5,10,25]\n30", "output": "2", "points": 3.33},
                    {"input": "[1,2,5,10,20]\n43", "output": "5", "points": 3.33},
                    {"input": "[2,5,10,20]\n1", "output": "-1", "points": 3.33},
                    {"input": "[1,3,4,5]\n10", "output": "2", "points": 3.33},
                    {"input": "[1,2,5,10,20,50]\n65", "output": "3", "points": 3.33},
                    {"input": "[1,2,5,10,20,50,100]\n127", "output": "4", "points": 3.33},
                    {"input": "[1,2,5,10,20,50,100]\n200", "output": "2", "points": 3.33}
                ],
                "total_points": 40
            },
            {
                "question": "Implement a function to find the longest palindromic substring in a given string.",
                "input_format": "The function should take a string as input.",
                "output_format": "Return the longest palindromic substring.",
                "test_cases": [
                    {"input": "babad", "output": "bab", "points": 3.33},
                    {"input": "cbbd", "output": "bb", "points": 3.33},
                    {"input": "a", "output": "a", "points": 3.33},
                    {"input": "ac", "output": "a", "points": 3.33},
                    {"input": "racecar", "output": "racecar", "points": 3.33},
                    {"input": "abacdfgdcaba", "output": "aba", "points": 3.33},
                    {"input": "forgeeksskeegfor", "output": "geeksskeeg", "points": 3.33},
                    {"input": "abcbabcbabcba", "output": "abcbabcbabcba", "points": 3.33},
                    {"input": "abacabacabbacabacab", "output": "bacabacabbacabacab", "points": 3.33},
                    {"input": "abacabacabbacabacaba", "output": "abacabacabbacabacaba", "points": 3.33},
                    {"input": "abacabacabbacabacabac", "output": "abacabacabbacabacaba", "points": 3.33},
                    {"input": "abacabacabbacabacabaca", "output": "abacabacabbacabacaba", "points": 3.33}
                ],
                "total_points": 40
            },
            {
                "question": "Implement a function to find the maximum product subarray in a given array of integers.",
                "input_format": "The function should take an array of integers as input.",
                "output_format": "Return the maximum product of any contiguous subarray.",
                "test_cases": [
                    {"input": "[2,3,-2,4]", "output": "6", "points": 3.33},
                    {"input": "[-2,0,-1]", "output": "0", "points": 3.33},
                    {"input": "[2,3,-2,4,-1]", "output": "48", "points": 3.33},
                    {"input": "[-2,-3,-4]", "output": "12", "points": 3.33},
                    {"input": "[0,2]", "output": "2", "points": 3.33},
                    {"input": "[-2,3,-4]", "output": "24", "points": 3.33},
                    {"input": "[2,-5,-2,-4,3]", "output": "24", "points": 3.33},
                    {"input": "[3,-1,4]", "output": "4", "points": 3.33},
                    {"input": "[1,2,-3,0,-4,-5]", "output": "20", "points": 3.33},
                    {"input": "[2,-5,3,1,-4,0,-10,2,8]", "output": "120", "points": 3.33},
                    {"input": "[-1,-2,-3,0]", "output": "6", "points": 3.33},
                    {"input": "[1,2,3,4,5,6,7,8,9,10]", "output": "3628800", "points": 3.33}
                ],
                "total_points": 40
            },
            {
                "question": "Implement a function to find the minimum window substring in a given string that contains all characters of another string.",
                "input_format": "The function should take two strings s and t as input.",
                "output_format": "Return the minimum window substring of s that contains all characters of t.",
                "test_cases": [
                    {"input": "ADOBECODEBANC\nABC", "output": "BANC", "points": 3.33},
                    {"input": "a\na", "output": "a", "points": 3.33},
                    {"input": "a\nb", "output": "", "points": 3.33},
                    {"input": "ab\nb", "output": "b", "points": 3.33},
                    {"input": "cabwefgewcwaefgcf\ncae", "output": "cwae", "points": 3.33},
                    {"input": "aaflslflsldkalskaaa\naaa", "output": "aaa", "points": 3.33},
                    {"input": "abababaabababaabababa\naba", "output": "aba", "points": 3.33},
                    {"input": "abababaabababaabababa\nabab", "output": "abab", "points": 3.33},
                    {"input": "abababaabababaabababa\nababa", "output": "ababa", "points": 3.33},
                    {"input": "abababaabababaabababa\nababab", "output": "ababab", "points": 3.33},
                    {"input": "abababaabababaabababa\nabababa", "output": "abababa", "points": 3.33},
                    {"input": "abababaabababaabababa\nabababab", "output": "abababaab", "points": 3.33}
                ],
                "total_points": 40
            }
        ]
        
        # Randomly select one problem
        return [random.choice(problem_pool)]
        
    def setup_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Add background watermark
        watermark = QLabel("AI_HACKBLITZ-XXV", main_widget)
        watermark.setStyleSheet("""
            QLabel {
                color: rgba(0, 0, 0, 0.05);
                font-size: 48px;
                font-family: Arial;
            }
        """)
        watermark.setAlignment(Qt.AlignCenter)
        watermark.setGeometry(0, 0, main_widget.width(), main_widget.height())
        watermark.setAttribute(Qt.WA_TransparentForMouseEvents)
        watermark.lower()  # Send to back
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Timer
        self.timer_label = QLabel("Time Left: 45:00")
        self.timer_label.setFont(QFont("Arial", 12, QFont.Bold))
        self.timer_label.setStyleSheet("color: #2E7D32;")
        header_layout.addWidget(self.timer_label)
        
        # Language selection
        self.language_combo = QComboBox()
        # Add Python options based on detected interpreters
        if 'python' in self.python_interpreters:
            self.language_combo.addItem("Python")
        if 'python3' in self.python_interpreters:
            self.language_combo.addItem("Python3")
        # Add other languages
        self.language_combo.addItems(["C++", "Java", "C", "C#"])
        self.language_combo.setFont(QFont("Arial", 12))
        header_layout.addWidget(self.language_combo)
        
        # Question counter
        self.question_counter = QLabel("DSA Round 2")
        self.question_counter.setFont(QFont("Arial", 12))
        header_layout.addWidget(self.question_counter)
        
        main_layout.addLayout(header_layout)
        
        # Question display
        self.question_display = QTextEdit()
        self.question_display.setReadOnly(True)
        self.question_display.setFont(QFont("Arial", 11))
        self.question_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ccc;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.question_display)
        
        # Code input area
        self.code_input = QTextEdit()
        self.code_input.setFont(QFont("Courier New", 10))
        self.code_input.setStyleSheet("""
            QTextEdit {
                background-color: #f8f8f8;
                border: 1px solid #ccc;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.code_input)
        
        # Terminal output area
        self.terminal_output = QTextEdit()
        self.terminal_output.setReadOnly(True)
        self.terminal_output.setFont(QFont("Courier New", 10))
        self.terminal_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 1px solid #ccc;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.terminal_output)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        # Run button
        run_button = QPushButton("Run Code")
        run_button.setFont(QFont("Arial", 12, QFont.Bold))
        run_button.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                padding: 10px;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        run_button.clicked.connect(self.run_code)
        button_layout.addWidget(run_button)
        
        # Submit button
        submit_button = QPushButton("Submit Answer")
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
        button_layout.addWidget(submit_button)
        
        main_layout.addLayout(button_layout)
        
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Display question
        self.display_question()
        
    def display_question(self):
        question = self.questions[0]  # Only one question
        question_text = f"""
        <h3>DSA Round 2</h3>
        <p><b>Question:</b> {question['question']}</p>
        <p><b>Input Format:</b> {question['input_format']}</p>
        <p><b>Output Format:</b> {question['output_format']}</p>
        <p><b>Total Points:</b> {question['total_points']}</p>
        <h4>Test Cases:</h4>
        <table style="width:100%; border-collapse: collapse; margin-top: 10px;">
            <tr style="background-color: #f2f2f2;">
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Test Case</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Input</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Expected Output</th>
                <th style="border: 1px solid #ddd; padding: 8px; text-align: left;">Points</th>
            </tr>
        """
        
        for i, test_case in enumerate(question['test_cases'], 1):
            question_text += f"""
            <tr>
                <td style="border: 1px solid #ddd; padding: 8px;">{i}</td>
                <td style="border: 1px solid #ddd; padding: 8px; font-family: monospace;">{test_case['input']}</td>
                <td style="border: 1px solid #ddd; padding: 8px; font-family: monospace;">{test_case['output']}</td>
                <td style="border: 1px solid #ddd; padding: 8px;">{test_case['points']}</td>
            </tr>
            """
            
        question_text += "</table>"
        self.question_display.setHtml(question_text)
        
        # Set default solution function template
        default_code = """def solution(s):
    # Your code here
    pass"""
        self.code_input.setText(self.user_answers.get(0, default_code))
        
    def compile_and_run(self, code, language, test_cases):
        score = 0
        results = []
        self.terminal_output.clear()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            if language == "Python" or language == "Python3":
                file_path = os.path.join(temp_dir, "solution.py")
                with open(file_path, "w") as f:
                    # Add proper Python code structure with input handling
                    if language == "Python3":
                        f.write("#!/usr/bin/env python3\n")
                    else:
                        f.write("#!/usr/bin/env python\n")
                    f.write("import sys\n")
                    f.write("import ast\n")
                    f.write("import json\n\n")
                    f.write("class TreeNode:\n")
                    f.write("    def __init__(self, val=0, left=None, right=None):\n")
                    f.write("        self.val = val\n")
                    f.write("        self.left = left\n")
                    f.write("        self.right = right\n\n")
                    f.write("def build_tree(nodes):\n")
                    f.write("    if not nodes:\n")
                    f.write("        return None\n")
                    f.write("    root = TreeNode(nodes[0])\n")
                    f.write("    queue = [root]\n")
                    f.write("    i = 1\n")
                    f.write("    while queue and i < len(nodes):\n")
                    f.write("        node = queue.pop(0)\n")
                    f.write("        if nodes[i] is not None:\n")
                    f.write("            node.left = TreeNode(nodes[i])\n")
                    f.write("            queue.append(node.left)\n")
                    f.write("        i += 1\n")
                    f.write("        if i < len(nodes) and nodes[i] is not None:\n")
                    f.write("            node.right = TreeNode(nodes[i])\n")
                    f.write("            queue.append(node.right)\n")
                    f.write("        i += 1\n")
                    f.write("    return root\n\n")
                    f.write(code)
                    f.write("\n\n")
                    f.write("if __name__ == '__main__':\n")
                    f.write("    try:\n")
                    f.write("        input_data = sys.stdin.read().strip()\n")
                    f.write("        # Handle different input formats\n")
                    f.write("        if '\\n' in input_data:\n")
                    f.write("            # Multi-line input\n")
                    f.write("            lines = input_data.split('\\n')\n")
                    f.write("            if len(lines) == 2:\n")
                    f.write("                # Two lines (e.g., array and number)\n")
                    f.write("                try:\n")
                    f.write("                    arr = ast.literal_eval(lines[0])\n")
                    f.write("                    num = ast.literal_eval(lines[1])\n")
                    f.write("                    result = solution(arr, num)\n")
                    f.write("                except:\n")
                    f.write("                    result = solution(lines[0], lines[1])\n")
                    f.write("            else:\n")
                    f.write("                # Multiple arrays\n")
                    f.write("                arrays = [ast.literal_eval(line) for line in lines]\n")
                    f.write("                result = solution(*arrays)\n")
                    f.write("        elif input_data.startswith('[') and input_data.endswith(']'):\n")
                    f.write("            # Single array input (BST case)\n")
                    f.write("            nodes = ast.literal_eval(input_data)\n")
                    f.write("            root = build_tree(nodes)\n")
                    f.write("            result = solution(root)\n")
                    f.write("        else:\n")
                    f.write("            # String or number input\n")
                    f.write("            try:\n")
                    f.write("                input_data = ast.literal_eval(input_data)\n")
                    f.write("            except:\n")
                    f.write("                pass\n")
                    f.write("            result = solution(input_data)\n")
                    f.write("        # Convert result to string\n")
                    f.write("        if isinstance(result, (list, tuple, dict)):\n")
                    f.write("            print(json.dumps(result))\n")
                    f.write("        else:\n")
                    f.write("            print(str(result))\n")
                    f.write("    except Exception as e:\n")
                    f.write("        print(f'Error: {str(e)}', file=sys.stderr)\n")
                
                try:
                    # Make file executable on Unix-like systems
                    if platform.system() != 'Windows':
                        os.chmod(file_path, 0o755)
                    
                    interpreter = self.python_interpreters['python3' if language == "Python3" else 'python']
                    
                    for i, test_case in enumerate(test_cases, 1):
                        self.terminal_output.append(f"\n=== Test Case {i} ===")
                        self.terminal_output.append(f"Input: {test_case['input']}")
                        self.terminal_output.append(f"Expected Output: {test_case['output']}")
                        
                        # Compile Python code to bytecode first
                        compile_process = subprocess.run(
                            [interpreter, "-m", "py_compile", file_path],
                            capture_output=True,
                            text=True
                        )
                        
                        if compile_process.returncode != 0:
                            self.terminal_output.append(f"Compilation Error:\n{compile_process.stderr}")
                            return 0, [{"passed": False, "points": 0} for _ in test_cases]
                        
                        # Run the compiled code
                        process = subprocess.run(
                            [interpreter, file_path],
                            input=test_case["input"].encode(),
                            capture_output=True,
                            timeout=5
                        )
                        
                        output = process.stdout.decode().strip()
                        error = process.stderr.decode().strip()
                        
                        if error:
                            self.terminal_output.append(f"Error:\n{error}")
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Runtime Error)")
                            continue
                        
                        # Normalize output for comparison
                        try:
                            # Try to parse output as JSON for array/list comparisons
                            output = json.dumps(json.loads(output))
                            expected = json.dumps(json.loads(test_case["output"]))
                        except:
                            # If not JSON, compare as strings
                            output = str(output)
                            expected = str(test_case["output"])
                        
                        self.terminal_output.append(f"Your Output: {output}")
                        
                        if output == expected:
                            score += test_case["points"]
                            results.append({"passed": True, "points": test_case["points"]})
                            self.terminal_output.append("Result: ✓ Passed")
                        else:
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Wrong Answer)")
                            
                except Exception as e:
                    self.terminal_output.append(f"Error: {str(e)}")
                    return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    
            elif language == "C++":
                file_path = os.path.join(temp_dir, "solution.cpp")
                exe_path = os.path.join(temp_dir, "solution")
                with open(file_path, "w") as f:
                    f.write("#include <iostream>\n")
                    f.write("#include <vector>\n")
                    f.write("#include <string>\n")
                    f.write("#include <sstream>\n")
                    f.write("#include <algorithm>\n\n")
                    f.write(code)
                    f.write("\n\n")
                    f.write("int main() {\n")
                    f.write("    std::string input;\n")
                    f.write("    std::getline(std::cin, input);\n")
                    f.write("    // Handle input and call solution\n")
                    f.write("    auto result = solution(input);\n")
                    f.write("    std::cout << result << std::endl;\n")
                    f.write("    return 0;\n")
                    f.write("}\n")
                
                try:
                    self.terminal_output.append("Compiling C++ code...")
                    compile_process = subprocess.run(
                        ["g++", "-std=c++11", "-O2", file_path, "-o", exe_path],
                        capture_output=True,
                        text=True
                    )
                    if compile_process.returncode != 0:
                        self.terminal_output.append(f"Compilation Error:\n{compile_process.stderr}")
                        return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    self.terminal_output.append("Compilation successful!")
                    
                    for i, test_case in enumerate(test_cases, 1):
                        self.terminal_output.append(f"\n=== Test Case {i} ===")
                        self.terminal_output.append(f"Input: {test_case['input']}")
                        self.terminal_output.append(f"Expected Output: {test_case['output']}")
                        
                        process = subprocess.run(
                            [exe_path],
                            input=test_case["input"].encode(),
                            capture_output=True,
                            timeout=5
                        )
                        output = process.stdout.decode().strip()
                        error = process.stderr.decode().strip()
                        
                        if error:
                            self.terminal_output.append(f"Error:\n{error}")
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Runtime Error)")
                            continue
                        
                        self.terminal_output.append(f"Your Output: {output}")
                        
                        if output == test_case["output"]:
                            score += test_case["points"]
                            results.append({"passed": True, "points": test_case["points"]})
                            self.terminal_output.append("Result: ✓ Passed")
                        else:
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Wrong Answer)")
                            
                except Exception as e:
                    self.terminal_output.append(f"Error: {str(e)}")
                    return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    
            elif language == "Java":
                file_path = os.path.join(temp_dir, "Solution.java")
                with open(file_path, "w") as f:
                    f.write(code)
                try:
                    self.terminal_output.append("Compiling Java code...")
                    compile_process = subprocess.run(
                        ["javac", file_path],
                        capture_output=True,
                        text=True
                    )
                    if compile_process.returncode != 0:
                        self.terminal_output.append(f"Compilation Error:\n{compile_process.stderr}")
                        return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    self.terminal_output.append("Compilation successful!")
                    
                    for i, test_case in enumerate(test_cases, 1):
                        self.terminal_output.append(f"\n=== Test Case {i} ===")
                        self.terminal_output.append(f"Input: {test_case['input']}")
                        self.terminal_output.append(f"Expected Output: {test_case['output']}")
                        
                        process = subprocess.run(
                            ["java", "-cp", temp_dir, "Solution"],
                            input=test_case["input"].encode(),
                            capture_output=True,
                            timeout=5
                        )
                        output = process.stdout.decode().strip()
                        error = process.stderr.decode().strip()
                        
                        if error:
                            self.terminal_output.append(f"Error:\n{error}")
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Runtime Error)")
                            continue
                        
                        self.terminal_output.append(f"Your Output: {output}")
                        
                        if output == test_case["output"]:
                            score += test_case["points"]
                            results.append({"passed": True, "points": test_case["points"]})
                            self.terminal_output.append("Result: ✓ Passed")
                        else:
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Wrong Answer)")
                            
                except Exception as e:
                    self.terminal_output.append(f"Error: {str(e)}")
                    return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    
            elif language == "C":
                file_path = os.path.join(temp_dir, "solution.c")
                exe_path = os.path.join(temp_dir, "solution")
                with open(file_path, "w") as f:
                    f.write(code)
                try:
                    self.terminal_output.append("Compiling C code...")
                    compile_process = subprocess.run(
                        ["gcc", file_path, "-o", exe_path],
                        capture_output=True,
                        text=True
                    )
                    if compile_process.returncode != 0:
                        self.terminal_output.append(f"Compilation Error:\n{compile_process.stderr}")
                        return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    self.terminal_output.append("Compilation successful!")
                    
                    for i, test_case in enumerate(test_cases, 1):
                        self.terminal_output.append(f"\n=== Test Case {i} ===")
                        self.terminal_output.append(f"Input: {test_case['input']}")
                        self.terminal_output.append(f"Expected Output: {test_case['output']}")
                        
                        process = subprocess.run(
                            [exe_path],
                            input=test_case["input"].encode(),
                            capture_output=True,
                            timeout=5
                        )
                        output = process.stdout.decode().strip()
                        error = process.stderr.decode().strip()
                        
                        if error:
                            self.terminal_output.append(f"Error:\n{error}")
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Runtime Error)")
                            continue
                        
                        self.terminal_output.append(f"Your Output: {output}")
                        
                        if output == test_case["output"]:
                            score += test_case["points"]
                            results.append({"passed": True, "points": test_case["points"]})
                            self.terminal_output.append("Result: ✓ Passed")
                        else:
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Wrong Answer)")
                            
                except Exception as e:
                    self.terminal_output.append(f"Error: {str(e)}")
                    return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    
            elif language == "C#":
                file_path = os.path.join(temp_dir, "Solution.cs")
                exe_path = os.path.join(temp_dir, "Solution.exe")
                with open(file_path, "w") as f:
                    f.write(code)
                try:
                    self.terminal_output.append("Compiling C# code...")
                    compile_process = subprocess.run(
                        ["csc", file_path],
                        capture_output=True,
                        text=True
                    )
                    if compile_process.returncode != 0:
                        self.terminal_output.append(f"Compilation Error:\n{compile_process.stderr}")
                        return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    self.terminal_output.append("Compilation successful!")
                    
                    for i, test_case in enumerate(test_cases, 1):
                        self.terminal_output.append(f"\n=== Test Case {i} ===")
                        self.terminal_output.append(f"Input: {test_case['input']}")
                        self.terminal_output.append(f"Expected Output: {test_case['output']}")
                        
                        process = subprocess.run(
                            ["mono", exe_path],
                            input=test_case["input"].encode(),
                            capture_output=True,
                            timeout=5
                        )
                        output = process.stdout.decode().strip()
                        error = process.stderr.decode().strip()
                        
                        if error:
                            self.terminal_output.append(f"Error:\n{error}")
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Runtime Error)")
                            continue
                        
                        self.terminal_output.append(f"Your Output: {output}")
                        
                        if output == test_case["output"]:
                            score += test_case["points"]
                            results.append({"passed": True, "points": test_case["points"]})
                            self.terminal_output.append("Result: ✓ Passed")
                        else:
                            results.append({"passed": False, "points": 0})
                            self.terminal_output.append("Result: ✗ Failed (Wrong Answer)")
                            
                except Exception as e:
                    self.terminal_output.append(f"Error: {str(e)}")
                    return 0, [{"passed": False, "points": 0} for _ in test_cases]
                    
        return score, results
        
    def submit_answers(self):
        # Store current answer
        current_question = self.questions[self.current_question]
        code = self.code_input.toPlainText()
        language = self.language_combo.currentText()
        
        # Calculate time taken
        end_time = datetime.now()
        time_taken = end_time - self.start_time
        minutes = time_taken.seconds // 60
        seconds = time_taken.seconds % 60
        
        # Log submission attempt
        self.logger.log_activity(
            'DSA2',
            'System',
            f'Question {self.current_question + 1}',
            'Submitted',
            0,
            0,
            f'Submitted solution in {language}'
        )
        
        # Compile and run code
        score, test_results = self.compile_and_run(code, language, current_question["test_cases"])
        
        # Log results
        self.logger.log_activity(
            'DSA2',
            'System',
            f'Question {self.current_question + 1}',
            'Completed',
            score,
            0,
            f'Score: {score}/{current_question["total_points"]}'
        )
        
        # Show score dialog
        score_dialog = QDialog(self)
        score_dialog.setWindowTitle("Round Complete")
        score_dialog.setFixedSize(300, 200)
        
        layout = QVBoxLayout()
        
        # Score label
        score_label = QLabel(f"Your Score: {score}/{current_question['total_points']}")
        score_label.setFont(QFont("Arial", 14, QFont.Bold))
        score_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(score_label)
        
        # Time taken label
        time_label = QLabel(f"Time Taken: {minutes:02d}:{seconds:02d}")
        time_label.setFont(QFont("Arial", 12))
        time_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(time_label)
        
        # Qualification status
        status_label = QLabel()
        status_label.setFont(QFont("Arial", 12))
        status_label.setAlignment(Qt.AlignCenter)
        
        if score >= current_question["total_points"] * 0.5:  # 50% threshold
            status_label.setText("Congratulations! You have completed the hackathon.")
            status_label.setStyleSheet("color: #2E7D32;")
        else:
            status_label.setText("Sorry, you did not complete the hackathon successfully.")
            status_label.setStyleSheet("color: #D32F2F;")
            
        layout.addWidget(status_label)
        
        # OK button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(lambda: self.close_round(score_dialog, score, time_taken))
        layout.addWidget(ok_button)
        
        score_dialog.setLayout(layout)
        score_dialog.exec_()
        
    def close_round(self, dialog, score, time_taken):
        dialog.accept()
        self.finished.emit(score)
        self.close()
        
    def closeEvent(self, event):
        # Check if there are unanswered questions
        if not hasattr(self, 'user_answers') or not self.user_answers:
            reply = QMessageBox.question(
                self, 'Confirm Exit',
                'You have not submitted any answers. Are you sure you want to exit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Log early exit
                self.logger.log_activity(
                    'DSA2',
                    'System',
                    '',
                    'Exited',
                    0,
                    0,
                    'Exited without completing the round'
                )
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def run_code(self):
        # Get selected language
        language = self.language_combo.currentText()
        
        # Get the code
        code = self.code_input.toPlainText()
        
        if not code.strip():
            QMessageBox.warning(self, "Warning", "Please write some code before running.")
            return
        
        # Compile and run the code
        score, results = self.compile_and_run(
            code,
            language,
            self.questions[0]["test_cases"]
        )
        
        # Show a message with the score
        QMessageBox.information(
            self,
            "Run Results",
            f"Your code passed {sum(test['passed'] for test in results)} out of {len(results)} test cases.\n"
            f"Score: {score}/{self.questions[0]['total_points']}"
        )

    def start_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)  # Update every second
        
    def update_timer(self):
        self.time_left -= 1
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        
        # Update timer color based on remaining time
        if minutes < 10:
            self.timer_label.setStyleSheet("color: #D32F2F;")  # Red for last 10 minutes
        elif minutes < 20:
            self.timer_label.setStyleSheet("color: #FFA000;")  # Orange for last 20 minutes
        else:
            self.timer_label.setStyleSheet("color: #2E7D32;")  # Green otherwise
            
        self.timer_label.setText(f"Time Left: {minutes:02d}:{seconds:02d}")
        
        if self.time_left <= 0:
            self.timer.stop()
            self.submit_answers() 