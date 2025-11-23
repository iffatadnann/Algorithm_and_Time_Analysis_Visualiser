# Algorithm and Time Analysis Visualizer

A desktop GUI tool built with Python and Tkinter that lets you **visualize classic sorting and searching algorithms** step-by-step, and **see their time performance** on different input sizes.

---

## ✨ Features

- Interactive **visualization** of:
  - Sorting algorithms (bar chart animation)
  - Searching algorithms (highlighted comparisons)
- **Time analysis graph** (input size vs running time) using Matplotlib
- Adjustable **animation speed**
- Automatic **random data generation**
- Clean, colorful UI themed around comparisons, swaps, and completion states

---

## 🧠 Supported Algorithms

### Sorting Algorithms   

Visual & timing support for:

- **Bubble Sort**
- **Insertion Sort**
- **Selection Sort**
- **Merge Sort**
- **Quick Sort**
- **Tim Sort** (TimSort-inspired hybrid)

Each has:

- A **generator-based version** (`*_sort_gen`) for step-by-step visualization
- A **pure function** (`*_sort`) for fast timing in the time graph

### Searching Algorithms   

Visual & timing support for:

- **Linear Search**
- **Binary Search**
- **Jump Search**

Each has:

- A **generator-based version** (`*_search_gen`) that yields compare/found/done states
- A **pure function** (`*_search`) for timing

---

## 🏗 Project Structure

- `main.py` – Tkinter GUI app (`AlgoVisualizer`), drawing, animation loop, time graph logic 
- `sorting.py` – Sorting algorithms (visual generators + pure functions) 
- `searching.py` – Searching algorithms (visual generators + pure functions)

---

## 💻 Requirements

- Python 3.x
- Tkinter (usually bundled with Python on most platforms)
- Matplotlib

Install Matplotlib (if not already installed):

pip install matplotlib

🚀 How to Run

From the project folder, run:

python main.py
This will open the “Algorithm and Time Analysis Visualizer” window.

🕹 Using the Visualizer
1. Choose Mode & Algorithm

At the top control bar: 

main

Mode:

Sorting

Searching

Algorithm:

Changes based on mode:

Sorting: Bubble, Insertion, Selection, Merge, Quick, Tim

Searching: Linear, Binary, Jump

2. Adjust Speed

Use the Speed slider (50–800) to control animation delay (in ms) between steps. 

main

3. Generate Data

Click “Generate Data”:

You’ll be asked for array size (e.g., 30).

For Sorting mode: creates a random unsorted array.

For Searching mode: creates a sorted random array (required for Binary & Jump Search).

The array is drawn as vertical bars with values above them.

4. Run the Algorithm

Click “Run”:

For Sorting:

Bars change color to indicate comparisons, swaps, overwrites.

Status bar updates when sorting completes and shows comparison count.

For Searching:

You’ll be prompted for a target value.

Comparisons are highlighted, and when found, the bar is marked and summary shown (found/not found + comparisons).

5. View Time Complexity Graph

Click “Show Time Graph”:

Runs the non-visual version of the currently selected algorithm on arrays of sizes:

10, 50, 100, 200, 400

Measures execution time and plots:

X-axis: Input size (n)

Y-axis: Time (seconds)

This gives an empirical feel for the algorithm’s time complexity.

🎨 Visualization Details

The canvas draws: 

main

One rectangle per element in the array

Height proportional to value

Optional color map to highlight:

Comparisons

Swaps / overwrites

Found elements

Completed arrays

Algorithms communicate via generator “actions” such as:

Sorting:

('compare', i, j)

('swap', i, j)

('overwrite', i, value)

('done', comparisons)

Searching:

('compare', index, None, comparisons)

('found', index, comparisons)

('done', comparisons)

The GUI consumes these actions to drive the animation and update the status bar.

🔧 Extending the Project

To add a new algorithm:

Implement a generator in sorting.py or searching.py that yields actions in the same format.

Add a pure function version for fast timing.

Register the generator in:

SORT_GEN or SEARCH_GEN in main.py.

The new algorithm will automatically appear in the algorithm dropdown for the relevant mode.

