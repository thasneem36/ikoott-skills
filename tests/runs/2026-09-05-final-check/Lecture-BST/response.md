Alright, let's start Topic 2: **Patient Records using a Binary Search Tree (BST)**. This one's worth 20 marks on its own — the single biggest chunk of your assignment — so it's worth doing properly.

## The Basic Concept

Forget patients for a second. A BST is just a way of arranging numbers so that for every single node: everything smaller goes to the left, everything bigger goes to the right. That's it. That's the whole idea.

Here's a small tree built from these numbers, inserted in this order: 50, 30, 70, 20, 40.

```
              50
            /    \
          30      70
         /  \
       20    40
```

Look at 50 — everything on its left (30, 20, 40) is smaller than 50. Everything on its right (70) is bigger. Now look at 30 — same rule applies again: 20 is smaller, so it goes left; 40 is bigger, so it goes right. Every single node follows this rule, all the way down. That's what makes searching fast — at each node you only ever need to check one side.

## The One Rule to Remember

> **"Smaller goes left, bigger goes right — at every node, every time."**

That one line is the entire BST. Insert, search, delete — they're all just walking down the tree using that one rule.

## Generic Code — Building It Step by Step

We'll build this with plain integers first — no patients yet. Two files: `Node.java` (a single box in the tree) and `BST.java` (the tree itself, with the logic).

### Step 1 — The Node

File: Node.java
```java
public class Node {
    int data;       // the number stored in this node
    Node left;      // reference to this node's left child (holds smaller values)
    Node right;     // reference to this node's right child (holds bigger values)

    public Node(int data) {   // data: the value this new node should hold
        this.data = data;
        this.left = null;     // brand new node has no children yet
        this.right = null;
    }
}
```

A `Node` is nothing fancy — a value, and two arrows pointing to its children. That's the whole box.

Make sense so far? Let's add one more small thing to `Node` before we move to the tree itself.

### Step 2 — toString() override

File: Node.java
```java
    @Override
    public String toString() {
        return "Node(" + data + ")";
    }
```

This just controls how a `Node` prints itself if we ever print it directly — instead of some ugly memory address, we'll see something readable like `Node(30)`. Small thing now, but it matters a lot more once we're printing real patient records later.

Good — `Node.java` is done. Now let's build the actual tree class, `BST.java`, one method at a time.

### Step 3 — The tree itself: field + constructor

File: BST.java
```java
public class BST {
    Node root;   // the topmost node of the whole tree; null means the tree is empty

    public BST() {
        root = null;   // a brand new tree starts empty
    }
}
```

`root` is the only thing the tree needs to remember — every other node is reached by following left/right arrows starting from `root`.

### Step 4 — insert()

File: BST.java
```java
    public void insert(int value) {       // value: the number we want to add to the tree
        root = insert(root, value);
    }

    private Node insert(Node current, int value) {
        // current: the node we're standing at right now while walking down the tree
        // value: the number we're trying to place into the tree
        if (current == null) {
            return new Node(value);   // found an empty spot — this is where it goes
        }
        if (value < current.data) {
            current.left = insert(current.left, value);   // smaller — go left
        } else if (value > current.data) {
            current.right = insert(current.right, value);  // bigger — go right
        }
        return current;
    }
```

Two methods, same name, but really it's one idea: the public `insert(value)` is the door you knock on, and the private one behind it just keeps applying our one rule — smaller left, bigger right — until it finds an empty spot.

Following that? Let's do search next.

### Step 5 — search()

File: BST.java
```java
    public boolean search(int value) {     // value: the number we're looking for
        return search(root, value);
    }

    private boolean search(Node current, int value) {
        // current: the node we're standing at right now while walking down the tree
        // value: the number we're looking for
        if (current == null) {
            return false;   // fell off the tree without finding it
        }
        if (value == current.data) {
            return true;    // found it
        }
        return value < current.data ? search(current.left, value) : search(current.right, value);
    }
```

Exact same walking pattern as insert — the only difference is we stop and say "found it" when we match, instead of creating a new node.

### Step 6 — findMin() (helper — needed before we can write delete)

Before we touch `delete()`, we need one small helper method. Deleting a node with two children is the tricky case — when that happens, we don't actually remove the node; we replace its value with the smallest value from its right subtree, then delete that smaller value instead (which is always an easy case). So we need a way to find "the smallest value in this subtree" first.

File: BST.java
```java
    private int findMin(Node current) {
        // current: the node we start searching from — usually the right child of the node being deleted
        while (current.left != null) {
            current = current.left;   // keep going left — the smallest value is always the leftmost node
        }
        return current.data;
    }
```

Remember this one — `delete()` is going to call it in a second.

### Step 7 — delete()

File: BST.java
```java
    public void delete(int value) {        // value: the number we want to remove from the tree
        root = delete(root, value);
    }

    private Node delete(Node current, int value) {
        // current: the node we're standing at right now while walking down the tree
        // value: the number we want to remove
        if (current == null) {
            return null;   // value wasn't found — nothing to delete
        }
        if (value < current.data) {
            current.left = delete(current.left, value);
        } else if (value > current.data) {
            current.right = delete(current.right, value);
        } else {
            // this is the node we want to delete
            if (current.left == null) return current.right;    // no left child — replace with right child
            if (current.right == null) return current.left;    // no left child — replace with right child

            // two children — replace this node's value with the smallest value from its right subtree
            current.data = findMin(current.right);
            current.right = delete(current.right, current.data);  // now delete that duplicate from the right subtree
        }
        return current;
    }
```

There are three cases here — no children, one child, two children — but notice we only had to write real new logic for the two-children case, and that's exactly where `findMin()` from the last step gets used.

### Step 8 — inorder traversal

File: BST.java
```java
    public void inorder() {
        inorder(root);
        System.out.println();
    }

    private void inorder(Node current) {   // current: the node we're currently visiting
        if (current != null) {
            inorder(current.left);                  // visit everything smaller first
            System.out.print(current.data + " ");   // then print this node
            inorder(current.right);                 // then everything bigger
        }
    }
```

"Inorder" just means: left side, then me, then right side. Because of our one rule (smaller left, bigger right), this always prints the values in ascending order — for free, no sorting needed.

That's the whole generic `BST.java` — insert, search, delete, inorder. All four operations your assignment asks for.

## Generic Main.java — Making It Actually Run

A class sitting there with methods doesn't do anything on its own — without a `Main` that creates a `BST` and actually calls these methods, none of this code ever runs. Let's wire it up.

File: Main.java
```java
public class Main {
    public static void main(String[] args) {
        BST tree = new BST();

        tree.insert(50);
        tree.insert(30);
        tree.insert(70);
        tree.insert(20);
        tree.insert(40);

        System.out.print("Inorder traversal: ");
        tree.inorder();   // should print: 20 30 40 50 70

        System.out.println("Search 40: " + tree.search(40));   // true
        System.out.println("Search 100: " + tree.search(100)); // false

        tree.delete(30);
        System.out.print("After deleting 30: ");
        tree.inorder();
    }
}
```

Run that, and you'll see the numbers come out sorted, the searches return true/false correctly, and after deleting 30, it disappears from the printed list but the tree still stays correctly ordered. That's the whole BST concept, proven with plain numbers.

Good — that's Pass 1 fully done. Any part of this feel shaky before we move on? If not, let's apply it to your actual assignment.

## Bridge to the Assessment

Here's the thing — you already understand the BST completely. Nothing about the *logic* changes from here. What changes is just the data type sitting inside the node: instead of a plain `int`, each node is going to hold a full `Patient` record. The rule stays identical — "smaller goes left, bigger goes right" — except now "smaller" and "bigger" are compared using **Patient ID**, since that's the key your assignment tells us to use. Insert, search, findMin, delete, inorder — same five methods, same shape, just built around `Patient` objects instead of `int`.

## Assessment Code — Patient Records BST

### Step 1 — The Patient class

File: Patient.java
```java
public class Patient {
    int patientId;          // unique ID for this patient — this is the BST key
    String name;             // patient's full name
    int age;                 // patient's age
    String contactNumber;    // patient's contact number
    String medicalCondition; // patient's medical condition

    public Patient(int patientId, String name, int age, String contactNumber, String medicalCondition) {
        // patientId: unique ID used to place this patient in the BST
        // name: patient's full name
        // age: patient's age
        // contactNumber: patient's phone number
        // medicalCondition: what condition this patient is being treated for
        this.patientId = patientId;
        this.name = name;
        this.age = age;
        this.contactNumber = contactNumber;
        this.medicalCondition = medicalCondition;
    }
}
```

This is the "real" version of the generic `Node`'s `int data` — instead of one number, we now carry five pieces of information about one patient.

### Step 2 — toString() override

File: Patient.java
```java
    @Override
    public String toString() {
        return "ID: " + patientId + " | Name: " + name + " | Age: " + age +
               " | Contact: " + contactNumber + " | Condition: " + medicalCondition;
    }
```

Same idea as before — this decides how a `Patient` prints itself. This one's going to matter a lot when we display the whole tree, because it turns each record into one readable line instead of a wall of raw fields.

`Patient.java` is done. Now the tree that holds them.

### Step 3 — PatientBST: node structure, field + constructor

Quick note on structure here — instead of a separate `Node` class, we'll give `PatientBST` its own private inner `PatientNode` that wraps a `Patient` plus left/right links. Same idea as `Node.java` earlier, just living inside the tree file since it's only ever used by the tree.

File: PatientBST.java
```java
public class PatientBST {

    private class PatientNode {
        Patient patient;      // the patient record stored in this node
        PatientNode left;     // left child — holds patients with smaller Patient IDs
        PatientNode right;    // right child — holds patients with bigger Patient IDs

        public PatientNode(Patient patient) {   // patient: the Patient record this node will hold
            this.patient = patient;
            this.left = null;
            this.right = null;
        }
    }

    private PatientNode root;   // topmost node of the tree; null means no patients yet

    public PatientBST() {
        root = null;
    }
}
```

Everything here mirrors `Node.java` and the `BST` field/constructor from Pass 1 — just renamed, and holding a `Patient` instead of an `int`.

### Step 4 — insert()

File: PatientBST.java
```java
    public void insert(Patient patient) {   // patient: the new Patient record to add to the tree
        root = insert(root, patient);
    }

    private PatientNode insert(PatientNode current, Patient patient) {
        // current: the node we're standing at right now while walking down the tree
        // patient: the new Patient record we're trying to place into the tree
        if (current == null) {
            return new PatientNode(patient);
        }
        if (patient.patientId < current.patient.patientId) {
            current.left = insert(current.left, patient);
        } else if (patient.patientId > current.patient.patientId) {
            current.right = insert(current.right, patient);
        }
        return current;
    }
```

Identical shape to the generic `insert()`. Only change: we compare `patient.patientId` instead of comparing the number directly.

### Step 5 — search()

File: PatientBST.java
```java
    public Patient search(int patientId) {   // patientId: the ID of the patient we're looking for
        return search(root, patientId);
    }

    private Patient search(PatientNode current, int patientId) {
        // current: the node we're standing at right now while walking down the tree
        // patientId: the ID we're searching for
        if (current == null) {
            return null;   // not found
        }
        if (patientId == current.patient.patientId) {
            return current.patient;
        }
        return patientId < current.patient.patientId
                ? search(current.left, patientId)
                : search(current.right, patientId);
    }
```

Same walk as before. Only real difference: instead of returning `true`/`false`, we return the actual `Patient` record we found (or `null` if there's no match) — more useful for the hospital system than a plain boolean.

### Step 6 — findMin() (helper — needed before delete again)

File: PatientBST.java
```java
    private Patient findMin(PatientNode current) {
        // current: the node we start searching from — usually the right child of the node being deleted
        while (current.left != null) {
            current = current.left;   // smallest Patient ID is always the leftmost node
        }
        return current.patient;
    }
```

Exact same job as the generic `findMin()` — just returns the whole `Patient` object instead of a raw `int`, since that's what `delete()` needs to copy over.

### Step 7 — delete()

File: PatientBST.java
```java
    public void delete(int patientId) {   // patientId: the ID of the patient record to remove
        root = delete(root, patientId);
    }

    private PatientNode delete(PatientNode current, int patientId) {
        // current: the node we're standing at right now while walking down the tree
        // patientId: the ID of the patient we want to remove
        if (current == null) {
            return null;   // ID wasn't found — nothing to delete
        }
        if (patientId < current.patient.patientId) {
            current.left = delete(current.left, patientId);
        } else if (patientId > current.patient.patientId) {
            current.right = delete(current.right, patientId);
        } else {
            // this is the patient record we want to delete
            if (current.left == null) return current.right;
            if (current.right == null) return current.left;

            // two children — replace this node's patient with the smallest-ID patient from the right subtree
            current.patient = findMin(current.right);
            current.right = delete(current.right, current.patient.patientId);
        }
        return current;
    }
```

Same three cases as the generic version, word for word in logic — no children, one child, two children — just working on `Patient` records keyed by `patientId` instead of raw numbers.

### Step 8 — inorder traversal (display patients in ascending order of Patient ID)

File: PatientBST.java
```java
    public void displayInorder() {
        displayInorder(root);
    }

    private void displayInorder(PatientNode current) {   // current: the node we're currently visiting
        if (current != null) {
            displayInorder(current.left);            // smaller Patient IDs first
            System.out.println(current.patient);      // uses Patient's toString() from earlier
            displayInorder(current.right);            // bigger Patient IDs after
        }
    }
```

This is exactly the requirement from your assessment sheet: "perform an in-order traversal to display patients in ascending order of Patient ID." Because we're keying the tree on `patientId`, walking it inorder gives us that ascending order automatically — and it prints nicely because of the `toString()` we wrote earlier.

That's the full `PatientBST.java` — insert, search, delete, displayInorder, all backed by real `Patient` records.

## Assessment Main.java — Running It for Real

File: Main.java
```java
public class Main {
    public static void main(String[] args) {
        PatientBST patientTree = new PatientBST();

        patientTree.insert(new Patient(1005, "Nimal Perera", 34, "0771234567", "Fracture"));
        patientTree.insert(new Patient(1002, "Kamala Silva", 61, "0719876543", "Hypertension"));
        patientTree.insert(new Patient(1008, "Ruwan Fernando", 27, "0765551234", "Asthma"));
        patientTree.insert(new Patient(1001, "Anusha Jayasuriya", 45, "0701112233", "Diabetes"));
        patientTree.insert(new Patient(1004, "Chamara Bandara", 19, "0754443322", "Sprained Ankle"));

        System.out.println("All patients (ascending Patient ID):");
        patientTree.displayInorder();

        System.out.println();
        Patient found = patientTree.search(1008);
        System.out.println("Search 1008: " + (found != null ? found : "Not found"));

        System.out.println();
        patientTree.delete(1002);
        System.out.println("After deleting patient 1002:");
        patientTree.displayInorder();
    }
}
```

Run this and you'll see all five patients printed out sorted by Patient ID, patient 1008 found by search, and after deleting 1002, the list shrinks by exactly one — everything else still perfectly sorted. That's your Patient Records BST, fully working, satisfying every bullet point under that 20-mark component: insert, search by ID, delete, and inorder traversal in ascending order.

## Wrapping Up This Topic

Quick recap: we built the whole BST idea on plain integers first — one rule, "smaller left, bigger right," used for insert, search, delete (with `findMin` as its little helper), and inorder traversal. Then we rebuilt the exact same five methods around real `Patient` records keyed on `patientId`, and nothing about the logic had to change — only the data type. **One takeaway to keep with you: a BST is never about the data type — it's about the comparison rule, whatever you're comparing.**

Since the whole BST topic — both the generic version and the real Patient version — is now fully done, this is a good point to save it to git. Two commits, matching the style your assignment sheet itself gives as examples:

```
git add .
git commit -m "Implemented patient BST"
```

```
git add .
git commit -m "Added BST search and deletion"
```

First commit covers `Patient.java` and the `PatientBST` structure plus `insert()`. Second one covers `search()` and `delete()` (traversal rides along with whichever commit you make it in — no need to split that out separately). Two separate, meaningful commits — not one giant dump — exactly what the marking scheme is looking for.

That's the Binary Search Tree component fully covered — 20 marks done. How are you feeling about this one? Ready to move on to Topic 3, the Emergency Patient Queue, or want to go over any part of the BST again first?
