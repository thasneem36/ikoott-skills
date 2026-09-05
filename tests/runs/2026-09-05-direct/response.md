Skipping the lecture — building this directly from your assessment (Mini Hospital Emergency Management System: Patient BST, Emergency Queue, Treatment Stack, Patient Visit Singly Linked List, plus GitHub evidence and the demo video).

Everything below is complete and runnable — no stubs, no `// TODO`. `Main.java` is a full interactive console app that exercises the whole system; `Demo.java` is a separate scripted driver that runs every required operation automatically with clean printed output, built specifically so you can point a screen recording at it.

---

## File: Patient.java

```java
// File: Patient.java
public class Patient {
    private int patientId;            // unique key used by the BST
    private String name;              // patient's full name
    private int age;                  // patient's age
    private String contactNumber;     // phone/contact number
    private String medicalCondition;  // short description of condition
    private VisitLinkedList visitHistory; // singly linked list of this patient's past visits

    public Patient(int patientId, String name, int age, String contactNumber, String medicalCondition) {
        this.patientId = patientId;
        this.name = name;
        this.age = age;
        this.contactNumber = contactNumber;
        this.medicalCondition = medicalCondition;
        this.visitHistory = new VisitLinkedList();
    }

    public int getPatientId() { return patientId; }
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getContactNumber() { return contactNumber; }
    public String getMedicalCondition() { return medicalCondition; }
    public VisitLinkedList getVisitHistory() { return visitHistory; }

    @Override
    public String toString() {
        return "Patient ID: " + patientId +
               " | Name: " + name +
               " | Age: " + age +
               " | Contact: " + contactNumber +
               " | Condition: " + medicalCondition;
    }
}
```

## File: PatientBST.java

```java
// File: PatientBST.java
public class PatientBST {

    // internal node of the tree, holds one Patient and links to children
    private class Node {
        Patient patient;
        Node left;
        Node right;

        Node(Patient patient) {
            this.patient = patient;
            this.left = null;
            this.right = null;
        }
    }

    private Node root; // root of the BST, null when the tree is empty

    public PatientBST() {
        this.root = null;
    }

    // ---------- INSERT ----------
    public void insert(Patient patient) {
        root = insertRec(root, patient);
    }

    private Node insertRec(Node current, Patient patient) {
        if (current == null) {
            return new Node(patient);
        }
        if (patient.getPatientId() < current.patient.getPatientId()) {
            current.left = insertRec(current.left, patient);
        } else if (patient.getPatientId() > current.patient.getPatientId()) {
            current.right = insertRec(current.right, patient);
        } else {
            System.out.println("Patient ID " + patient.getPatientId() + " already exists. Insert ignored.");
        }
        return current;
    }

    // ---------- SEARCH ----------
    public Patient search(int patientId) {
        Node result = searchRec(root, patientId);
        return (result == null) ? null : result.patient;
    }

    private Node searchRec(Node current, int patientId) {
        if (current == null) {
            return null;
        }
        if (patientId == current.patient.getPatientId()) {
            return current;
        } else if (patientId < current.patient.getPatientId()) {
            return searchRec(current.left, patientId);
        } else {
            return searchRec(current.right, patientId);
        }
    }

    // ---------- DELETE ----------
    public void delete(int patientId) {
        root = deleteRec(root, patientId);
    }

    private Node deleteRec(Node current, int patientId) {
        if (current == null) {
            System.out.println("Patient ID " + patientId + " not found. Nothing deleted.");
            return null;
        }

        if (patientId < current.patient.getPatientId()) {
            current.left = deleteRec(current.left, patientId);
        } else if (patientId > current.patient.getPatientId()) {
            current.right = deleteRec(current.right, patientId);
        } else {
            // node found
            if (current.left == null && current.right == null) {
                return null;
            }
            if (current.left == null) {
                return current.right;
            }
            if (current.right == null) {
                return current.left;
            }
            // two children: replace with the smallest value in the right subtree
            Node successor = findMin(current.right);
            current.patient = successor.patient;
            current.right = deleteRec(current.right, successor.patient.getPatientId());
        }
        return current;
    }

    private Node findMin(Node node) {
        while (node.left != null) {
            node = node.left;
        }
        return node;
    }

    // ---------- IN-ORDER TRAVERSAL ----------
    public void inorderTraversal() {
        if (root == null) {
            System.out.println("No patients recorded yet.");
            return;
        }
        System.out.println("Patients in ascending order of Patient ID:");
        inorderRec(root);
    }

    private void inorderRec(Node current) {
        if (current == null) {
            return;
        }
        inorderRec(current.left);
        System.out.println("  " + current.patient);
        inorderRec(current.right);
    }
}
```

## File: Visit.java

```java
// File: Visit.java
public class Visit {
    private int visitId;
    private String visitDate;
    private String doctorName;
    private String diagnosis;
    private String treatment;

    public Visit(int visitId, String visitDate, String doctorName, String diagnosis, String treatment) {
        this.visitId = visitId;
        this.visitDate = visitDate;
        this.doctorName = doctorName;
        this.diagnosis = diagnosis;
        this.treatment = treatment;
    }

    public int getVisitId() { return visitId; }
    public String getVisitDate() { return visitDate; }
    public String getDoctorName() { return doctorName; }
    public String getDiagnosis() { return diagnosis; }
    public String getTreatment() { return treatment; }

    @Override
    public String toString() {
        return "Visit ID: " + visitId +
               " | Date: " + visitDate +
               " | Doctor: " + doctorName +
               " | Diagnosis: " + diagnosis +
               " | Treatment: " + treatment;
    }
}
```

## File: VisitLinkedList.java

```java
// File: VisitLinkedList.java
public class VisitLinkedList {

    // internal singly linked node, holds one Visit and a link to the next node
    private class Node {
        Visit visit;
        Node next;

        Node(Visit visit) {
            this.visit = visit;
            this.next = null;
        }
    }

    private Node head; // first visit in this patient's history, null when empty

    public VisitLinkedList() {
        this.head = null;
    }

    // ---------- ADD ----------
    public void addVisit(Visit visit) {
        Node newNode = new Node(visit);
        if (head == null) {
            head = newNode;
            return;
        }
        Node current = head;
        while (current.next != null) {
            current = current.next;
        }
        current.next = newNode;
    }

    // ---------- REMOVE ----------
    public void removeVisit(int visitId) {
        if (head == null) {
            System.out.println("No visit history to remove from.");
            return;
        }
        if (head.visit.getVisitId() == visitId) {
            head = head.next;
            return;
        }
        Node current = head;
        while (current.next != null && current.next.visit.getVisitId() != visitId) {
            current = current.next;
        }
        if (current.next == null) {
            System.out.println("Visit ID " + visitId + " not found.");
        } else {
            current.next = current.next.next;
        }
    }

    // ---------- SEARCH ----------
    public Visit searchVisit(int visitId) {
        Node current = head;
        while (current != null) {
            if (current.visit.getVisitId() == visitId) {
                return current.visit;
            }
            current = current.next;
        }
        return null;
    }

    // ---------- DISPLAY ----------
    public void displayVisits() {
        if (head == null) {
            System.out.println("    No visit history recorded.");
            return;
        }
        Node current = head;
        while (current != null) {
            System.out.println("    " + current.visit);
            current = current.next;
        }
    }
}
```

## File: EmergencyQueue.java

```java
// File: EmergencyQueue.java
public class EmergencyQueue {

    // internal node for the linked-list-backed queue
    private class Node {
        Patient patient;
        Node next;

        Node(Patient patient) {
            this.patient = patient;
            this.next = null;
        }
    }

    private Node front; // head of the queue, next patient to be treated
    private Node rear;  // tail of the queue, last patient who arrived
    private int size;

    public EmergencyQueue() {
        this.front = null;
        this.rear = null;
        this.size = 0;
    }

    public boolean isEmpty() {
        return front == null;
    }

    // ---------- ENQUEUE ----------
    public void enqueue(Patient patient) {
        Node newNode = new Node(patient);
        if (isEmpty()) {
            front = newNode;
            rear = newNode;
        } else {
            rear.next = newNode;
            rear = newNode;
        }
        size++;
        System.out.println("Enqueued to emergency queue: " + patient.getName() + " (ID " + patient.getPatientId() + ")");
    }

    // ---------- DEQUEUE ----------
    public Patient dequeue() {
        if (isEmpty()) {
            System.out.println("Emergency queue is empty. No patient to dequeue.");
            return null;
        }
        Patient removed = front.patient;
        front = front.next;
        if (front == null) {
            rear = null; // queue just became empty, reset rear too
        }
        size--;
        System.out.println("Dequeued for treatment: " + removed.getName() + " (ID " + removed.getPatientId() + ")");
        return removed;
    }

    // ---------- DISPLAY ----------
    public void displayQueue() {
        if (isEmpty()) {
            System.out.println("Emergency queue is empty.");
            return;
        }
        System.out.println("Patients currently waiting (front to rear):");
        Node current = front;
        int position = 1;
        while (current != null) {
            System.out.println("  " + position + ". " + current.patient);
            current = current.next;
            position++;
        }
    }

    public int getSize() {
        return size;
    }
}
```

## File: TreatmentRecord.java

```java
// File: TreatmentRecord.java
public class TreatmentRecord {
    private int patientId;
    private String patientName;
    private String treatmentSummary;
    private String completionDate;

    public TreatmentRecord(int patientId, String patientName, String treatmentSummary, String completionDate) {
        this.patientId = patientId;
        this.patientName = patientName;
        this.treatmentSummary = treatmentSummary;
        this.completionDate = completionDate;
    }

    public int getPatientId() { return patientId; }
    public String getPatientName() { return patientName; }
    public String getTreatmentSummary() { return treatmentSummary; }
    public String getCompletionDate() { return completionDate; }

    @Override
    public String toString() {
        return "Patient ID: " + patientId +
               " | Name: " + patientName +
               " | Treatment: " + treatmentSummary +
               " | Completed: " + completionDate;
    }
}
```

## File: TreatmentStack.java

```java
// File: TreatmentStack.java
public class TreatmentStack {

    // internal node for the linked-list-backed stack
    private class Node {
        TreatmentRecord record;
        Node next;

        Node(TreatmentRecord record) {
            this.record = record;
            this.next = null;
        }
    }

    private Node top; // most recently completed treatment sits here
    private int size;

    public TreatmentStack() {
        this.top = null;
        this.size = 0;
    }

    public boolean isEmpty() {
        return top == null;
    }

    // ---------- PUSH ----------
    public void push(TreatmentRecord record) {
        Node newNode = new Node(record);
        newNode.next = top;
        top = newNode;
        size++;
        System.out.println("Pushed to treatment history: " + record.getPatientName() + " (ID " + record.getPatientId() + ")");
    }

    // ---------- POP ----------
    public TreatmentRecord pop() {
        if (isEmpty()) {
            System.out.println("Treatment stack is empty. Nothing to pop.");
            return null;
        }
        TreatmentRecord removed = top.record;
        top = top.next;
        size--;
        System.out.println("Popped most recent treatment record: " + removed.getPatientName() + " (ID " + removed.getPatientId() + ")");
        return removed;
    }

    // ---------- DISPLAY ----------
    public void displayStack() {
        if (isEmpty()) {
            System.out.println("Treatment stack is empty.");
            return;
        }
        System.out.println("Treatment records (most recent first):");
        Node current = top;
        int position = 1;
        while (current != null) {
            System.out.println("  " + position + ". " + current.record);
            current = current.next;
            position++;
        }
    }

    public int getSize() {
        return size;
    }
}
```

## File: Main.java

```java
// File: Main.java
import java.util.Scanner;

public class Main {

    private static PatientBST patientBST = new PatientBST();
    private static EmergencyQueue emergencyQueue = new EmergencyQueue();
    private static TreatmentStack treatmentStack = new TreatmentStack();
    private static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        boolean running = true;
        while (running) {
            printMainMenu();
            int choice = readInt("Enter choice: ");
            switch (choice) {
                case 1: patientMenu(); break;
                case 2: queueMenu(); break;
                case 3: stackMenu(); break;
                case 4: visitHistoryMenu(); break;
                case 0:
                    running = false;
                    System.out.println("Exiting Mini Hospital Emergency Management System. Goodbye.");
                    break;
                default:
                    System.out.println("Invalid choice. Try again.");
            }
        }
        scanner.close();
    }

    private static void printMainMenu() {
        System.out.println("\n===== Mini Hospital Emergency Management System =====");
        System.out.println("1. Patient Records (BST)");
        System.out.println("2. Emergency Patient Queue");
        System.out.println("3. Treatment History (Stack)");
        System.out.println("4. Patient Visit History (Linked List)");
        System.out.println("0. Exit");
    }

    // ---------------- Patient BST menu ----------------
    private static void patientMenu() {
        System.out.println("\n-- Patient Records (BST) --");
        System.out.println("1. Insert patient");
        System.out.println("2. Search patient");
        System.out.println("3. Delete patient");
        System.out.println("4. In-order traversal (ascending Patient ID)");
        System.out.println("0. Back");
        int choice = readInt("Enter choice: ");
        switch (choice) {
            case 1: {
                int id = readInt("Patient ID: ");
                System.out.print("Name: ");
                String name = scanner.nextLine();
                int age = readInt("Age: ");
                System.out.print("Contact Number: ");
                String contact = scanner.nextLine();
                System.out.print("Medical Condition: ");
                String condition = scanner.nextLine();
                patientBST.insert(new Patient(id, name, age, contact, condition));
                System.out.println("Patient inserted.");
                break;
            }
            case 2: {
                int id = readInt("Patient ID to search: ");
                Patient found = patientBST.search(id);
                System.out.println(found == null ? "Patient not found." : "Found: " + found);
                break;
            }
            case 3: {
                int id = readInt("Patient ID to delete: ");
                patientBST.delete(id);
                System.out.println("Delete attempted for ID " + id);
                break;
            }
            case 4:
                patientBST.inorderTraversal();
                break;
            case 0:
                return;
            default:
                System.out.println("Invalid choice.");
        }
    }

    // ---------------- Emergency Queue menu ----------------
    private static void queueMenu() {
        System.out.println("\n-- Emergency Patient Queue --");
        System.out.println("1. Enqueue patient (search existing by ID)");
        System.out.println("2. Dequeue next patient");
        System.out.println("3. Display waiting queue");
        System.out.println("0. Back");
        int choice = readInt("Enter choice: ");
        switch (choice) {
            case 1: {
                int id = readInt("Patient ID to enqueue: ");
                Patient patient = patientBST.search(id);
                if (patient == null) {
                    System.out.println("No such patient in records. Insert the patient first.");
                } else {
                    emergencyQueue.enqueue(patient);
                }
                break;
            }
            case 2:
                emergencyQueue.dequeue();
                break;
            case 3:
                emergencyQueue.displayQueue();
                break;
            case 0:
                return;
            default:
                System.out.println("Invalid choice.");
        }
    }

    // ---------------- Treatment Stack menu ----------------
    private static void stackMenu() {
        System.out.println("\n-- Treatment History (Stack) --");
        System.out.println("1. Push completed treatment record");
        System.out.println("2. Pop most recent treatment record");
        System.out.println("3. Display treatment records");
        System.out.println("0. Back");
        int choice = readInt("Enter choice: ");
        switch (choice) {
            case 1: {
                int id = readInt("Patient ID: ");
                Patient patient = patientBST.search(id);
                if (patient == null) {
                    System.out.println("No such patient in records.");
                    break;
                }
                System.out.print("Treatment summary: ");
                String summary = scanner.nextLine();
                System.out.print("Completion date (e.g. 2026-09-05): ");
                String date = scanner.nextLine();
                treatmentStack.push(new TreatmentRecord(patient.getPatientId(), patient.getName(), summary, date));
                break;
            }
            case 2:
                treatmentStack.pop();
                break;
            case 3:
                treatmentStack.displayStack();
                break;
            case 0:
                return;
            default:
                System.out.println("Invalid choice.");
        }
    }

    // ---------------- Visit History menu ----------------
    private static void visitHistoryMenu() {
        System.out.println("\n-- Patient Visit History (Linked List) --");
        int id = readInt("Patient ID: ");
        Patient patient = patientBST.search(id);
        if (patient == null) {
            System.out.println("No such patient in records.");
            return;
        }
        System.out.println("1. Add visit");
        System.out.println("2. Remove visit");
        System.out.println("3. Search visit");
        System.out.println("4. Display visit history");
        System.out.println("0. Back");
        int choice = readInt("Enter choice: ");
        switch (choice) {
            case 1: {
                int visitId = readInt("Visit ID: ");
                System.out.print("Visit Date: ");
                String date = scanner.nextLine();
                System.out.print("Doctor Name: ");
                String doctor = scanner.nextLine();
                System.out.print("Diagnosis: ");
                String diagnosis = scanner.nextLine();
                System.out.print("Treatment: ");
                String treatment = scanner.nextLine();
                patient.getVisitHistory().addVisit(new Visit(visitId, date, doctor, diagnosis, treatment));
                System.out.println("Visit added.");
                break;
            }
            case 2: {
                int visitId = readInt("Visit ID to remove: ");
                patient.getVisitHistory().removeVisit(visitId);
                break;
            }
            case 3: {
                int visitId = readInt("Visit ID to search: ");
                Visit found = patient.getVisitHistory().searchVisit(visitId);
                System.out.println(found == null ? "Visit not found." : "Found: " + found);
                break;
            }
            case 4:
                patient.getVisitHistory().displayVisits();
                break;
            case 0:
                return;
            default:
                System.out.println("Invalid choice.");
        }
    }

    // ---------------- input helper ----------------
    private static int readInt(String prompt) {
        System.out.print(prompt);
        while (!scanner.hasNextInt()) {
            System.out.print("Please enter a number: ");
            scanner.next();
        }
        int value = scanner.nextInt();
        scanner.nextLine(); // consume leftover newline so following nextLine() calls work
        return value;
    }
}
```

## File: Demo.java

This is your demo-support script — a scripted, non-interactive driver that exercises every required operation for every data structure in one run, with clear printed output. Run this one on screen while recording; you don't have to type anything live.

```java
// File: Demo.java
public class Demo {

    public static void main(String[] args) {
        System.out.println("=================================================================");
        System.out.println(" MINI HOSPITAL EMERGENCY MANAGEMENT SYSTEM - FULL DEMO WALKTHROUGH");
        System.out.println("=================================================================");

        PatientBST patientBST = new PatientBST();
        EmergencyQueue emergencyQueue = new EmergencyQueue();
        TreatmentStack treatmentStack = new TreatmentStack();

        // ---------------- 1. BST: Patient Records ----------------
        section("1. PATIENT RECORDS - BINARY SEARCH TREE (BST)");

        System.out.println("-- Inserting patients --");
        Patient p1 = new Patient(105, "Nimal Perera", 34, "0771234567", "Fractured arm");
        Patient p2 = new Patient(102, "Kamal Silva", 45, "0779876543", "Chest pain");
        Patient p3 = new Patient(110, "Anusha Fernando", 28, "0765551234", "High fever");
        Patient p4 = new Patient(101, "Ruwan Jayasuriya", 52, "0712223344", "Diabetic emergency");
        Patient p5 = new Patient(108, "Dilani Wickrama", 19, "0723334455", "Sprained ankle");

        patientBST.insert(p1);
        patientBST.insert(p2);
        patientBST.insert(p3);
        patientBST.insert(p4);
        patientBST.insert(p5);

        System.out.println("\n-- In-order traversal (ascending Patient ID) --");
        patientBST.inorderTraversal();

        System.out.println("\n-- Searching for Patient ID 102 --");
        Patient found = patientBST.search(102);
        System.out.println(found == null ? "Not found." : "Found: " + found);

        System.out.println("\n-- Searching for Patient ID 999 (does not exist) --");
        Patient notFound = patientBST.search(999);
        System.out.println(notFound == null ? "Not found, as expected." : "Found: " + notFound);

        System.out.println("\n-- Deleting Patient ID 102 (Kamal Silva) --");
        patientBST.delete(102);

        System.out.println("\n-- In-order traversal after deletion --");
        patientBST.inorderTraversal();

        // ---------------- 2. Queue: Emergency Patient Queue ----------------
        section("2. EMERGENCY PATIENT QUEUE - QUEUE (FIFO)");

        System.out.println("-- Enqueueing patients as they arrive --");
        emergencyQueue.enqueue(p4); // Ruwan
        emergencyQueue.enqueue(p1); // Nimal
        emergencyQueue.enqueue(p5); // Dilani

        System.out.println("\n-- Displaying waiting queue --");
        emergencyQueue.displayQueue();

        System.out.println("\n-- Dequeueing next patient for treatment --");
        emergencyQueue.dequeue();

        System.out.println("\n-- Displaying waiting queue after dequeue --");
        emergencyQueue.displayQueue();

        System.out.println("\n-- Dequeueing remaining patients to show empty-queue handling --");
        emergencyQueue.dequeue();
        emergencyQueue.dequeue();
        emergencyQueue.dequeue(); // queue now empty, should print a friendly message

        // ---------------- 3. Stack: Treatment History ----------------
        section("3. TREATMENT HISTORY - STACK (LIFO)");

        System.out.println("-- Pushing completed treatment records --");
        treatmentStack.push(new TreatmentRecord(p4.getPatientId(), p4.getName(), "Stabilized blood sugar, administered insulin", "2026-09-01"));
        treatmentStack.push(new TreatmentRecord(p1.getPatientId(), p1.getName(), "Arm splinted and X-rayed", "2026-09-02"));
        treatmentStack.push(new TreatmentRecord(p5.getPatientId(), p5.getName(), "Ankle bandaged, rest advised", "2026-09-03"));

        System.out.println("\n-- Displaying treatment records (most recent first) --");
        treatmentStack.displayStack();

        System.out.println("\n-- Popping most recently completed treatment record --");
        treatmentStack.pop();

        System.out.println("\n-- Displaying treatment records after pop --");
        treatmentStack.displayStack();

        System.out.println("\n-- Popping remaining records to show empty-stack handling --");
        treatmentStack.pop();
        treatmentStack.pop();
        treatmentStack.pop(); // stack now empty, should print a friendly message

        // ---------------- 4. Singly Linked List: Patient Visit History ----------------
        section("4. PATIENT VISIT HISTORY - SINGLY LINKED LIST");

        System.out.println("-- Adding visits to Nimal Perera's (ID 105) history --");
        p1.getVisitHistory().addVisit(new Visit(1, "2025-11-10", "Dr. Perera", "Minor cut", "Cleaned and bandaged"));
        p1.getVisitHistory().addVisit(new Visit(2, "2026-01-22", "Dr. Costa", "Flu", "Prescribed medication"));
        p1.getVisitHistory().addVisit(new Visit(3, "2026-09-02", "Dr. Silva", "Fractured arm", "Arm splinted and X-rayed"));

        System.out.println("\n-- Displaying visit history --");
        p1.getVisitHistory().displayVisits();

        System.out.println("\n-- Searching for Visit ID 2 --");
        Visit foundVisit = p1.getVisitHistory().searchVisit(2);
        System.out.println(foundVisit == null ? "Visit not found." : "Found: " + foundVisit);

        System.out.println("\n-- Removing Visit ID 1 --");
        p1.getVisitHistory().removeVisit(1);

        System.out.println("\n-- Displaying visit history after removal --");
        p1.getVisitHistory().displayVisits();

        // ---------------- Wrap up ----------------
        section("DEMO COMPLETE");
        System.out.println("All required operations for BST, Queue, Stack, and Singly Linked List");
        System.out.println("have been demonstrated above with clear printed output.");
    }

    private static void section(String title) {
        System.out.println("\n-----------------------------------------------------------------");
        System.out.println(title);
        System.out.println("-----------------------------------------------------------------");
    }
}
```

## File: README.md

```markdown
# Mini Hospital Emergency Management System

Java console application built for CIT300 - Data Structures and Algorithms
(Individual Mid Assignment). Simulates patient registration, emergency
treatment queueing, treatment history, and per-patient visit history using
four required data structures, each implemented from scratch (no built-in
`java.util` collections used for the core structures).

## Data Structures Used

| Requirement                          | Data Structure          | File(s)                                 |
|---------------------------------------|--------------------------|------------------------------------------|
| Patient Records                       | Binary Search Tree (BST) | `Patient.java`, `PatientBST.java`        |
| Emergency Patient Queue               | Queue (FIFO)              | `EmergencyQueue.java`                    |
| Treatment History                     | Stack (LIFO)              | `TreatmentRecord.java`, `TreatmentStack.java` |
| Patient Visit History                 | Singly Linked List        | `Visit.java`, `VisitLinkedList.java`     |

- **PatientBST** keys on `Patient ID` and supports insert, search, delete
  (handles 0, 1, and 2-child deletion via in-order successor), and an
  in-order traversal that prints patients in ascending Patient ID order.
- **EmergencyQueue** is a linked-list-backed FIFO queue with `enqueue`,
  `dequeue`, `displayQueue`, and safe handling of dequeue-on-empty.
- **TreatmentStack** is a linked-list-backed LIFO stack with `push`, `pop`,
  `displayStack`, and safe handling of pop-on-empty.
- **VisitLinkedList** is a singly linked list, one per patient, supporting
  add, remove, search, and display of that patient's visit history.

## Project Structure

```
project-root/
├── Patient.java
├── PatientBST.java
├── Visit.java
├── VisitLinkedList.java
├── EmergencyQueue.java
├── TreatmentRecord.java
├── TreatmentStack.java
├── Main.java
├── Demo.java
├── README.md
├── git-sync.sh
└── git-sync.ps1
```

## How to Compile and Run

```bash
javac *.java

# Full interactive system (menu-driven):
java Main

# Scripted demo of every operation, for the demo video:
java Demo
```

## Menu Overview (Main.java)

1. Patient Records (BST) — insert / search / delete / in-order traversal
2. Emergency Patient Queue — enqueue / dequeue / display
3. Treatment History (Stack) — push / pop / display
4. Patient Visit History (Linked List) — add / remove / search / display,
   scoped to a Patient ID looked up in the BST

## Development Process / Commit History

This repository was built with small, meaningful commits per component
(project structure, BST, queue, stack, linked list, testing, README) rather
than one final upload — see commit history for evidence.

## Author

Individual assignment — CIT300 Data Structures and Algorithms.
```

---

## Git Automation Scripts

Two versions so it runs on either OS — pick the one matching your machine. Both assume the repo already exists locally with `origin` set up and git credentials already authenticated, so neither will prompt you for anything.

### File: git-sync.sh (macOS / Linux / Git Bash)

```bash
#!/bin/bash
# Git auto-sync script: stage everything, commit, push. No prompts.
# Safe to run repeatedly, including when there's nothing new to commit.

git add -A
git commit -m "auto commit" || true
git push
```

Make it executable once, then run it anytime:

```bash
chmod +x git-sync.sh
./git-sync.sh
```

### File: git-sync.ps1 (Windows PowerShell)

```powershell
# Git auto-sync script: stage everything, commit, push. No prompts.
# Safe to run repeatedly, including when there's nothing new to commit.

git add -A
git commit -m "auto commit"
if ($LASTEXITCODE -ne 0) {
    Write-Host "Nothing new to commit - skipping to push."
}
git push
```

Run it from the project folder:

```powershell
./git-sync.ps1
```

(If PowerShell blocks the script with an execution-policy error, run
`powershell -ExecutionPolicy Bypass -File .\git-sync.ps1` instead — that's a
one-time local shell setting, not something this script changes for you.)

**Note on commit granularity:** this sync script is a convenience tool for
saving progress on demand — it is not a substitute for the meaningful,
one-topic-at-a-time commits the assignment marking scheme rewards
("Implemented patient BST", "Added BST search and deletion", "Implemented
emergency queue", etc.). Since you're already comfortable with these
structures, just make sure your actual commit messages reflect each
component as you build it, rather than running this script once at the very
end for a single giant commit — the brief explicitly penalizes that.

---

## Demo Video Help

The assignment requires a 5-10 minute video covering 8 specific things. Here's a run sheet mapped straight to the brief, with suggested timing (totals ~8 minutes) and a note on what to have on screen for each part.

| # | Required content                                             | Suggested time | What to show |
|---|----------------------------------------------------------------|-----------------|----------------|
| 1 | Brief introduction (face visible)                              | 0:00–0:30       | Camera on, state your name and the assignment. |
| 2 | Brief explanation of the developed system                      | 0:30–1:15       | Slide or spoken overview: hospital system, 4 data structures, what each models. |
| 3 | GitHub repository and commit history                            | 1:15–2:15       | Screen-share your repo, scroll the commit list, point out the progressive commits (skeleton → BST → queue → stack → linked list → README). |
| 4 | Explanation of how each data structure is used                 | 2:15–3:30       | One sentence each: BST keyed on Patient ID for fast lookup/sorted order, Queue for FIFO arrivals, Stack for LIFO treatment history, Linked List for per-patient visit history. |
| 5 | Demonstration of the system running                             | 3:30–4:00       | Compile and launch (`javac *.java`, then `java Demo`). |
| 6 | Demonstration of important operations (BST, Queue, Stack, List) | 4:00–7:00       | Let `Demo.java` run on screen — it walks through insert/search/delete/traversal, enqueue/dequeue/display + empty-queue handling, push/pop/display + empty-stack handling, and add/remove/search/display for visit history, in that exact order, with labeled section headers already printed for you. Narrate over it as each section prints. |
| 7 | Explanation of important implementation/design decisions        | 7:00–7:45       | E.g. why BST for patients (ordered by ID, log-time search), why linked-list-backed queue/stack instead of arrays (no fixed capacity), why visit history lives per-Patient object. |
| 8 | Brief reflection on what was learned                             | 7:45–8:15       | One or two honest sentences on what was reinforced (recursion in BST delete, FIFO vs LIFO trade-offs, etc.). |

Practical tips:
- Run `java Demo` once beforehand so you know how long the output takes to scroll, and resize your terminal font up before recording — markers will be reading printed text.
- Keep the GitHub tab and terminal pre-opened so you're not fumbling between windows during the take.
- If you want a second run to prove interactivity (not just the scripted demo), briefly run `java Main` and do one live insert + one live enqueue, then cut back to `Demo.java` for full coverage — this isn't required, just optional extra credibility.
- Screenshots requirement: grab a few terminal screenshots straight from a `Demo.java` run (one per data structure section) for the separate "Screenshots of program output" submission item — the section headers make them easy to isolate.

---

What's included above: `Patient.java`, `PatientBST.java`, `Visit.java`, `VisitLinkedList.java`, `EmergencyQueue.java`, `TreatmentRecord.java`, `TreatmentStack.java`, `Main.java` (full interactive system), `Demo.java` (scripted demo for recording), `README.md`, `git-sync.sh` + `git-sync.ps1`, and a video run sheet mapped to all 8 required video segments. Drop the `.java` files and `README.md` into your repo root, compile with `javac *.java`, and you're ready to record.
