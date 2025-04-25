import csv
import random

# Categories of questions with equal distribution
categories = {
    'time_complexity': [
        ["What is the time complexity of binary search?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
        ["What is the time complexity of linear search?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "C"],
        ["What is the time complexity of bubble sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "C"],
        ["What is the time complexity of merge sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "B"],
        ["What is the time complexity of quick sort (average case)?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "B"],
        ["What is the time complexity of accessing an element in an array?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "A"],
        ["What is the time complexity of inserting an element at the end of a linked list?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "A"],
        ["What is the time complexity of finding an element in a hash table?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "A"],
        ["What is the time complexity of heap sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "B"],
        ["What is the time complexity of selection sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "C"]
    ],
    
    'data_structures': [
        ["Which data structure uses LIFO principle?", "Queue", "Stack", "Tree", "Graph", "B"],
        ["Which data structure uses FIFO principle?", "Queue", "Stack", "Tree", "Graph", "A"],
        ["Which data structure is best for implementing a priority queue?", "Array", "Linked List", "Heap", "Stack", "C"],
        ["Which data structure is best for implementing a dictionary?", "Array", "Linked List", "Hash Table", "Stack", "C"],
        ["Which data structure is best for implementing a browser's back button?", "Queue", "Stack", "Tree", "Graph", "B"],
        ["Which data structure is best for implementing a call center queue?", "Queue", "Stack", "Tree", "Graph", "A"],
        ["Which data structure is best for implementing a file system?", "Queue", "Stack", "Tree", "Graph", "C"],
        ["Which data structure is best for implementing a social network?", "Queue", "Stack", "Tree", "Graph", "D"],
        ["Which data structure is best for implementing a spell checker?", "Queue", "Stack", "Trie", "Graph", "C"],
        ["Which data structure is best for implementing a cache?", "Queue", "Stack", "Hash Table", "Graph", "C"]
    ],
    
    'trees': [
        ["What is the maximum number of nodes in a binary tree of height h?", "2^h", "2^(h+1)-1", "h^2", "h+1", "B"],
        ["What is the height of a complete binary tree with n nodes?", "log n", "n/2", "n", "2^n", "A"],
        ["Which traversal gives nodes in non-decreasing order in a BST?", "Preorder", "Inorder", "Postorder", "Level order", "B"],
        ["What is the time complexity of searching in a balanced BST?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
        ["What is the time complexity of inserting in a balanced BST?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
        ["What is the time complexity of deleting in a balanced BST?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
        ["What is the maximum number of children a node can have in a binary tree?", "1", "2", "3", "4", "B"],
        ["What is the minimum number of nodes in a binary tree of height h?", "h", "h+1", "2h", "2h+1", "B"],
        ["What is the time complexity of finding the minimum element in a BST?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
        ["What is the time complexity of finding the maximum element in a BST?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"]
    ],
    
    'graphs': [
        ["What is the time complexity of BFS?", "O(V)", "O(E)", "O(V+E)", "O(V*E)", "C"],
        ["What is the time complexity of DFS?", "O(V)", "O(E)", "O(V+E)", "O(V*E)", "C"],
        ["What is the time complexity of Dijkstra's algorithm?", "O(V)", "O(E log V)", "O(V+E)", "O(V*E)", "B"],
        ["What is the time complexity of Kruskal's algorithm?", "O(E log V)", "O(V log E)", "O(V+E)", "O(V*E)", "A"],
        ["What is the time complexity of Prim's algorithm?", "O(E log V)", "O(V log E)", "O(V+E)", "O(V*E)", "A"],
        ["What is the time complexity of Bellman-Ford algorithm?", "O(V)", "O(E)", "O(V*E)", "O(V+E)", "C"],
        ["What is the time complexity of Floyd-Warshall algorithm?", "O(V)", "O(E)", "O(V³)", "O(V+E)", "C"],
        ["What is the time complexity of topological sort?", "O(V)", "O(E)", "O(V+E)", "O(V*E)", "C"],
        ["What is the time complexity of finding strongly connected components?", "O(V)", "O(E)", "O(V+E)", "O(V*E)", "C"],
        ["What is the time complexity of finding articulation points?", "O(V)", "O(E)", "O(V+E)", "O(V*E)", "C"]
    ],
    
    'sorting': [
        ["What is the time complexity of bubble sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "C"],
        ["What is the time complexity of selection sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "C"],
        ["What is the time complexity of insertion sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "C"],
        ["What is the time complexity of merge sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "B"],
        ["What is the time complexity of quick sort (average case)?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "B"],
        ["What is the time complexity of heap sort?", "O(n)", "O(n log n)", "O(n²)", "O(1)", "B"],
        ["What is the time complexity of counting sort?", "O(n)", "O(n log n)", "O(n+k)", "O(1)", "C"],
        ["What is the time complexity of radix sort?", "O(n)", "O(n log n)", "O(nk)", "O(1)", "C"],
        ["What is the time complexity of bucket sort?", "O(n)", "O(n log n)", "O(n²)", "O(n+k)", "D"],
        ["What is the time complexity of shell sort?", "O(n)", "O(n log n)", "O(n²)", "O(n^(3/2))", "D"]
    ],
    
    'python_basics': [
        ["What is Python?", "A programming language", "A snake", "A type of coffee", "A computer brand", "A"],
        ["Which symbol is used for comments?", "//", "#", "/*", "--", "B"],
        ["What is the output of print(2 + 2)?", "4", "22", "2+2", "Error", "A"],
        ["Which of these is a Python list?", "[1, 2, 3]", "{1, 2, 3}", "(1, 2, 3)", "1, 2, 3", "A"],
        ["What is the correct way to create a variable?", "var x = 5", "x = 5", "int x = 5", "x := 5", "B"],
        ["What is the output of print('Hello' + 'World')?", "HelloWorld", "Hello World", "Hello+World", "Error", "A"],
        ["Which of these is used for exponentiation?", "^", "**", "^^", "pow", "B"],
        ["What is the output of print(10 / 3)?", "3", "3.333...", "3.0", "Error", "B"],
        ["What is the output of print(len('Python'))?", "6", "5", "7", "Error", "A"],
        ["What is the output of print(2 * 3)?", "6", "23", "2*3", "Error", "A"],
        ["Which of these is not a Python data type?", "int", "float", "string", "character", "D"],
        ["Which of these is a Python tuple?", "(1, 2, 3)", "[1, 2, 3]", "{1, 2, 3}", "1, 2, 3", "A"],
        ["Which of these is a Python dictionary?", "{'key': 'value'}", "['key', 'value']", "('key', 'value')", "key: value", "A"],
        ["Which of these is a Python set?", "{1, 2, 3}", "[1, 2, 3]", "(1, 2, 3)", "1, 2, 3", "A"],
        ["What is the output of print(10 // 3)?", "3", "3.333...", "3.0", "Error", "A"]
    ],
    
    'python_control_flow': [
        ["Which keyword is used for loops?", "loop", "for", "while", "repeat", "B"],
        ["What is the output: for i in range(3): print(i)", "0 1 2", "1 2 3", "0 1 2 3", "Error", "A"],
        ["Which is a valid if statement?", "if x > 5:", "if (x > 5)", "if x > 5 then", "if x > 5;", "A"],
        ["What does 'break' do?", "Ends program", "Skips iteration", "Exits loop", "Continues loop", "C"],
        ["Which is a valid while loop?", "while x > 5:", "while (x > 5)", "while x > 5 do", "while x > 5;", "A"],
        ["What is the output: x = 5; while x > 0: print(x); x -= 1", "5 4 3 2 1", "4 3 2 1 0", "5 4 3 2 1 0", "Error", "A"],
        ["Which keyword skips iteration?", "skip", "continue", "next", "pass", "B"],
        ["What is the output: for i in range(1, 4): print(i)", "1 2 3", "0 1 2 3", "1 2 3 4", "Error", "A"],
        ["Which is a valid elif?", "elif x > 5:", "else if x > 5:", "elseif x > 5:", "elif (x > 5)", "A"],
        ["What is the output: x = 10; if x > 5: print('Yes')", "Yes", "No", "Error", "Nothing", "A"]
    ],
    
    'python_functions': [
        ["What is a function?", "A variable", "Reusable code", "Data structure", "Loop", "B"],
        ["Which keyword returns value?", "return", "give", "back", "output", "A"],
        ["What is the output: def add(x, y): return x + y; print(add(2, 3))", "5", "23", "Error", "Nothing", "A"],
        ["What is a parameter?", "Function name", "Input to function", "Output of function", "Function type", "B"],
        ["What is the output: def greet(): print('Hello'); greet()", "Hello", "Error", "Nothing", "greet", "A"],
        ["Which is valid function definition?", "def my_func():", "function my_func():", "def my_func:", "function my_func:", "A"],
        ["What is the output: def square(x): return x * x; print(square(4))", "16", "8", "4", "Error", "A"],
        ["What is a default parameter?", "Required parameter", "Parameter with default value", "First parameter", "Last parameter", "B"],
        ["What is the output: def multiply(x=2, y=3): return x * y; print(multiply())", "6", "5", "Error", "Nothing", "A"],
        ["Which is valid function call?", "my_func()", "call my_func()", "execute my_func()", "run my_func()", "A"]
    ],
    
    'computer_basics': [
        ["What is RAM?", "Read Access Memory", "Random Access Memory", "Read Only Memory", "Random Only Memory", "B"],
        ["What is the brain of computer?", "CPU", "RAM", "Hard Drive", "Motherboard", "A"],
        ["Which is an input device?", "Monitor", "Printer", "Keyboard", "Speaker", "C"],
        ["What is binary system?", "Base 2", "Base 10", "Base 8", "Base 16", "A"],
        ["What is an OS?", "Software", "Hardware", "Memory", "Processor", "A"],
        ["Which is not an OS?", "Windows", "Linux", "MacOS", "Microsoft", "D"],
        ["What is a byte?", "8 bits", "4 bits", "16 bits", "32 bits", "A"],
        ["What is a compiler?", "Hardware", "Converts code", "Memory", "Processor", "B"],
        ["What is a variable?", "Constant", "Data container", "Function", "Loop", "B"],
        ["What is an algorithm?", "Hardware", "Step-by-step procedure", "Memory", "Processor", "B"]
    ],
    
    'networking_basics': [
        ["What is Internet?", "Computer", "Global network", "Software", "Hardware", "B"],
        ["What is IP address?", "Protocol address", "Password", "Program", "Port", "A"],
        ["What is a router?", "Computer", "Connects networks", "Software", "Memory", "B"],
        ["What is Wi-Fi?", "Wireless Fidelity", "Wired Fidelity", "Wireless File", "Wired File", "A"],
        ["What is a server?", "Computer", "Provides services", "Software", "Hardware", "B"],
        ["What is a client?", "Computer", "Requests services", "Software", "Hardware", "B"],
        ["What is a protocol?", "Computer", "Set of rules", "Software", "Hardware", "B"],
        ["What is HTTP?", "Transfer Protocol", "Transfer Program", "Transfer Port", "Transfer Password", "A"],
        ["What is domain name?", "Computer", "Human-readable address", "Software", "Hardware", "B"],
        ["What is firewall?", "Computer", "Security system", "Software", "Hardware", "B"]
    ],
    
    'web_basics': [
        ["What is HTML?", "Markup Language", "Machine Language", "Memory Language", "Media Language", "A"],
        ["What is CSS?", "Computer Style", "Cascading Style", "Computer System", "Cascading System", "B"],
        ["What is JavaScript?", "Programming language", "Coffee", "Computer", "Software", "A"],
        ["What is web browser?", "Computer", "Accesses web", "Memory", "Processor", "B"],
        ["What is URL?", "Resource Locator", "Resource Language", "Resource Link", "Resource Location", "A"],
        ["What is web server?", "Computer", "Serves web pages", "Software", "Hardware", "B"],
        ["What is cookie?", "Food", "Data piece", "Computer", "Software", "B"],
        ["What is web page?", "Computer", "Web document", "Software", "Hardware", "B"],
        ["What is hyperlink?", "Computer", "Link to page", "Software", "Hardware", "B"],
        ["What is web app?", "Computer", "Runs on web", "Software", "Hardware", "B"]
    ]
}

def generate_random_questions():
    # Separate DSA and non-DSA categories
    dsa_categories = ['time_complexity', 'data_structures', 'trees', 'graphs', 'sorting']
    non_dsa_categories = ['python_basics', 'python_control_flow', 'python_functions', 
                         'computer_basics', 'networking_basics', 'web_basics']
    
    selected_questions = []
    
    # Select 3 questions from each DSA category (15 total)
    for category in dsa_categories:
        category_questions = categories[category]
        random.shuffle(category_questions)
        selected_questions.extend(category_questions[:3])
    
    # Select 2-3 questions from each non-DSA category (15 total)
    for category in non_dsa_categories:
        category_questions = categories[category]
        random.shuffle(category_questions)
        # Take 3 questions from first 3 categories, 2 from last 3 to make 15 total
        num_questions = 3 if non_dsa_categories.index(category) < 3 else 2
        selected_questions.extend(category_questions[:num_questions])
    
    # Final shuffle of all selected questions
    random.shuffle(selected_questions)
    return selected_questions

# Generate and write questions to CSV
questions = generate_random_questions()

# Write to CSV
with open('mcq.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Question', 'OptionA', 'OptionB', 'OptionC', 'OptionD', 'CorrectAnswer'])
    writer.writerows(questions)

print("MCQ CSV file created successfully with exactly 15 DSA and 15 non-DSA questions!") 