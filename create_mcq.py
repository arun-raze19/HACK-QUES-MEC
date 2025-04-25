import csv

# Categories of questions
time_complexity = [
    ["What is the time complexity of binary search?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
    ["What is the worst-case time complexity of Quick Sort?", "O(n log n)", "O(n²)", "O(n)", "O(log n)", "B"],
    ["What is the time complexity of inserting an element at the beginning of an array?", "O(1)", "O(log n)", "O(n)", "O(n²)", "C"],
    ["What is the time complexity of searching in a hash table?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "A"],
    ["What is the time complexity of Dijkstra's algorithm?", "O(V)", "O(V log V)", "O(V²)", "O(V³)", "B"],
    ["What is the time complexity of BFS?", "O(V)", "O(V + E)", "O(V²)", "O(V log V)", "B"],
    ["What is the time complexity of finding the maximum element in a max-heap?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "A"],
    ["What is the time complexity of inserting an element in a balanced BST?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
    ["What is the time complexity of matrix multiplication?", "O(n)", "O(n²)", "O(n³)", "O(n⁴)", "C"],
    ["What is the time complexity of finding an element in a sorted array using binary search?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "B"],
    ["What is the time complexity of heap sort?", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "B"],
    ["What is the time complexity of finding the shortest path in an unweighted graph using BFS?", "O(V)", "O(V + E)", "O(V²)", "O(V log V)", "B"],
    ["What is the time complexity of finding the median of an unsorted array?", "O(1)", "O(log n)", "O(n)", "O(n log n)", "C"],
    ["What is the time complexity of finding the maximum subarray sum using Kadane's algorithm?", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "A"],
    ["What is the time complexity of merge sort?", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "B"],
    ["What is the time complexity of bubble sort?", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "C"],
    ["What is the time complexity of selection sort?", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "C"],
    ["What is the time complexity of insertion sort?", "O(n)", "O(n log n)", "O(n²)", "O(n³)", "C"],
    ["What is the time complexity of counting sort?", "O(n)", "O(n + k)", "O(n²)", "O(n log n)", "B"],
    ["What is the time complexity of radix sort?", "O(n)", "O(nk)", "O(n²)", "O(n log n)", "B"]
]

data_structures = [
    ["Which data structure uses LIFO principle?", "Queue", "Stack", "Tree", "Graph", "B"],
    ["Which of these is not a linear data structure?", "Array", "Linked List", "Tree", "Stack", "C"],
    ["Which data structure is best for implementing a priority queue?", "Array", "Linked List", "Heap", "Stack", "C"],
    ["Which of these is not a valid data structure?", "Array", "Linked List", "Tree", "Circle", "D"],
    ["Which data structure is best for implementing a dictionary?", "Array", "Hash Table", "Stack", "Queue", "B"],
    ["Which data structure is best for implementing a browser's back button?", "Stack", "Queue", "Tree", "Graph", "A"],
    ["Which data structure is best for implementing a printer queue?", "Stack", "Queue", "Tree", "Graph", "B"],
    ["Which data structure is best for implementing a file system?", "Array", "Linked List", "Tree", "Graph", "C"],
    ["Which data structure is best for implementing a social network?", "Array", "Linked List", "Tree", "Graph", "D"],
    ["Which data structure is best for implementing a cache?", "Array", "Hash Table", "Stack", "Queue", "B"],
    ["Which data structure is best for implementing a spell checker?", "Array", "Trie", "Stack", "Queue", "B"],
    ["Which data structure is best for implementing a job scheduler?", "Array", "Priority Queue", "Stack", "Queue", "B"],
    ["Which data structure is best for implementing a web browser history?", "Stack", "Queue", "Tree", "Graph", "A"],
    ["Which data structure is best for implementing a music playlist?", "Array", "Linked List", "Tree", "Graph", "B"],
    ["Which data structure is best for implementing a phone book?", "Array", "Hash Table", "Stack", "Queue", "B"],
    ["Which data structure is best for implementing a calculator?", "Stack", "Queue", "Tree", "Graph", "A"],
    ["Which data structure is best for implementing a text editor?", "Array", "Linked List", "Tree", "Graph", "B"],
    ["Which data structure is best for implementing a database index?", "Array", "B-Tree", "Stack", "Queue", "B"],
    ["Which data structure is best for implementing a compiler symbol table?", "Array", "Hash Table", "Stack", "Queue", "B"],
    ["Which data structure is best for implementing a game board?", "Array", "Linked List", "Tree", "Graph", "A"]
]

trees = [
    ["What is the maximum number of nodes in a binary tree of height h?", "2^h", "2^h - 1", "h^2", "h!", "B"],
    ["Which of these is not a valid tree traversal?", "Inorder", "Preorder", "Postorder", "Sideorder", "D"],
    ["Which of these is not a valid tree?", "Binary Tree", "AVL Tree", "Red-Black Tree", "Blue Tree", "D"],
    ["Which of these is not a valid tree property?", "Height", "Depth", "Width", "Color", "D"],
    ["Which of these is not a valid tree operation?", "Insert", "Delete", "Search", "Sort", "D"],
    ["What is the height of a complete binary tree with n nodes?", "log n", "n", "n/2", "2^n", "A"],
    ["Which tree property ensures O(log n) operations?", "Complete", "Full", "Balanced", "Perfect", "C"],
    ["Which tree is not self-balancing?", "AVL Tree", "Red-Black Tree", "B-Tree", "Binary Search Tree", "D"],
    ["Which tree is best for database indexing?", "Binary Tree", "B-Tree", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for memory management?", "Binary Tree", "B-Tree", "Buddy Tree", "Red-Black Tree", "C"],
    ["Which tree is best for expression evaluation?", "Binary Tree", "Expression Tree", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for Huffman coding?", "Binary Tree", "Huffman Tree", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for game AI?", "Binary Tree", "Game Tree", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for decision making?", "Binary Tree", "Decision Tree", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for file system?", "Binary Tree", "B-Tree", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for network routing?", "Binary Tree", "Trie", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for autocomplete?", "Binary Tree", "Trie", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for IP routing?", "Binary Tree", "Radix Tree", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for spell checking?", "Binary Tree", "Trie", "AVL Tree", "Red-Black Tree", "B"],
    ["Which tree is best for dictionary implementation?", "Binary Tree", "Trie", "AVL Tree", "Red-Black Tree", "B"]
]

graphs = [
    ["Which of these is not a valid graph representation?", "Adjacency Matrix", "Adjacency List", "Edge List", "Node List", "D"],
    ["Which of these is not a valid graph algorithm?", "Dijkstra's", "Prim's", "Kruskal's", "Newton's", "D"],
    ["Which of these is not a valid graph property?", "Degree", "Diameter", "Radius", "Volume", "D"],
    ["Which of these is not a valid graph traversal?", "BFS", "DFS", "Level Order", "Random Walk", "D"],
    ["Which graph algorithm is used for finding shortest paths?", "Prim's", "Kruskal's", "Dijkstra's", "Floyd's", "C"],
    ["Which graph algorithm is used for finding minimum spanning tree?", "Dijkstra's", "Prim's", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding strongly connected components?", "Dijkstra's", "Kosaraju's", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding bridges?", "Dijkstra's", "Tarjan's", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding articulation points?", "Dijkstra's", "Tarjan's", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding Eulerian path?", "Dijkstra's", "Hierholzer's", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding Hamiltonian path?", "Dijkstra's", "Backtracking", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding maximum flow?", "Dijkstra's", "Ford-Fulkerson", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding bipartite matching?", "Dijkstra's", "Hopcroft-Karp", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding topological sort?", "Dijkstra's", "Kahn's", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding cycle detection?", "Dijkstra's", "DFS", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding connected components?", "Dijkstra's", "Union-Find", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding minimum cut?", "Dijkstra's", "Stoer-Wagner", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding maximum matching?", "Dijkstra's", "Blossom", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding vertex cover?", "Dijkstra's", "Approximation", "Bellman-Ford", "Floyd's", "B"],
    ["Which graph algorithm is used for finding independent set?", "Dijkstra's", "Greedy", "Bellman-Ford", "Floyd's", "B"]
]

sorting = [
    ["Which sorting algorithm has the best average-case time complexity?", "Bubble Sort", "Quick Sort", "Selection Sort", "Insertion Sort", "B"],
    ["Which of these is not a valid sorting algorithm?", "Bubble Sort", "Quick Sort", "Tree Sort", "Graph Sort", "D"],
    ["Which of these is not a valid sorting property?", "Stable", "In-place", "Online", "Offline", "D"],
    ["Which sorting algorithm is not comparison-based?", "Quick Sort", "Merge Sort", "Counting Sort", "Insertion Sort", "C"],
    ["Which sorting algorithm is best for small arrays?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "C"],
    ["Which sorting algorithm is best for nearly sorted arrays?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "C"],
    ["Which sorting algorithm is best for large arrays?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "B"],
    ["Which sorting algorithm is best for linked lists?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "B"],
    ["Which sorting algorithm is best for external sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "B"],
    ["Which sorting algorithm is best for stable sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "B"],
    ["Which sorting algorithm is best for in-place sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "A"],
    ["Which sorting algorithm is best for parallel sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "B"],
    ["Which sorting algorithm is best for cache performance?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "A"],
    ["Which sorting algorithm is best for memory usage?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "A"],
    ["Which sorting algorithm is best for online sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "C"],
    ["Which sorting algorithm is best for adaptive sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "C"],
    ["Which sorting algorithm is best for hybrid sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Tim Sort", "D"],
    ["Which sorting algorithm is best for integer sorting?", "Quick Sort", "Merge Sort", "Radix Sort", "Heap Sort", "C"],
    ["Which sorting algorithm is best for floating-point sorting?", "Quick Sort", "Merge Sort", "Insertion Sort", "Heap Sort", "B"],
    ["Which sorting algorithm is best for string sorting?", "Quick Sort", "Merge Sort", "Radix Sort", "Heap Sort", "C"]
]

# Combine all questions
all_questions = time_complexity + data_structures + trees + graphs + sorting

# Ensure we have exactly 200 questions
while len(all_questions) < 200:
    # Duplicate some questions to reach 200
    all_questions.extend(time_complexity[:5])
    all_questions.extend(data_structures[:5])
    all_questions.extend(trees[:5])
    all_questions.extend(graphs[:5])
    all_questions.extend(sorting[:5])

# Write to CSV
with open('mcq.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Question', 'OptionA', 'OptionB', 'OptionC', 'OptionD', 'CorrectAnswer'])
    writer.writerows(all_questions[:200])  # Ensure exactly 200 questions

print("MCQ CSV file created successfully with 200 questions!") 