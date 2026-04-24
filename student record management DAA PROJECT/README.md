# Student Record Management System using AVL Trees

A Python-based student record management system that uses AVL (Adelson-Velsky and Landis) trees for efficient data storage and retrieval with automatic balancing.

## Features

### AVL Tree Operations
- **Insert**: Add new student records with automatic tree balancing
- **Delete**: Remove student records while maintaining tree balance
- **Search**: Fast O(log n) student lookup by roll number
- **Rotations**: Automatic LL, RR, LR, RL rotations for balance maintenance
- **Height Balancing**: Maintains balanced tree structure for optimal performance

### Student Record Management
- Add new student records (Roll Number, Name, Course, CGPA)
- Search students by roll number
- Delete student records
- Edit/update existing student details
- Display all students in sorted order (in-order traversal)

### Data Persistence
- Automatic saving to `students.json` after each operation
- Load existing data on program startup
- JSON format for easy data portability

## File Structure

```
student record management adsa/
├── student_record_system.py    # Main system implementation
├── test_system.py             # Test script with sample data
├── README.md                  # This documentation
└── students.json             # Data storage (created automatically)
```

## Classes

### Student
- Represents individual student records
- Contains roll_number, name, course, cgpa
- Methods for JSON serialization/deserialization

### AVLNode
- Tree node containing student data
- Tracks height for balancing calculations

### AVLTree
- Core AVL tree implementation
- Handles insertions, deletions, searches
- Performs automatic rotations for balance
- Shows rotation types during operations

### StudentRecordSystem
- Main application interface
- Handles file I/O operations
- Provides menu-driven CLI

## Usage

### Running the Main System
```bash
python student_record_system.py
```

### Running Tests
```bash
python test_system.py
```

## Menu Options

1. **Add Student**: Insert new student record
2. **Search Student**: Find student by roll number
3. **Delete Student**: Remove student record
4. **Edit Student**: Update existing student details
5. **Display All Students**: Show sorted list of all students
6. **Exit**: Save and quit

## AVL Tree Rotations

The system demonstrates four types of rotations:

- **LL Rotation**: Left-Left case (right rotation)
- **RR Rotation**: Right-Right case (left rotation)
- **LR Rotation**: Left-Right case (left then right rotation)
- **RL Rotation**: Right-Left case (right then left rotation)

Rotation messages are displayed during operations for educational purposes.

## Data Format

Student records are stored in JSON format:
```json
[
  {
    "roll_number": 101,
    "name": "Alice Johnson",
    "course": "Computer Science",
    "cgpa": 3.8
  }
]
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Educational Value

This implementation is designed for learning:
- Clear separation of AVL tree logic and application logic
- Detailed comments explaining rotation logic
- Visual feedback showing when rotations occur
- Modular design for easy understanding
- Academic-focused CLI interface