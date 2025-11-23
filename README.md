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
- Clean, colorful UI themed around comparisons, swaps, and completion states :contentReference[oaicite:0]{index=0}  

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

- `main.py` – Tkinter GUI app (`AlgoVisualizer`), drawing, animation loop, time graph logic :contentReference[oaicite:3]{index=3}  
- `sorting.py` – Sorting algorithms (visual generators + pure functions) :contentReference[oaicite:4]{index=4}  
- `searching.py` – Searching algorithms (visual generators + pure functions) :contentReference[oaicite:5]{index=5}  

---

## 💻 Requirements

- Python 3.x
- Tkinter (usually bundled with Python on most platforms)
- Matplotlib

Install Matplotlib (if not already installed):

```bash
pip install matplotlib
