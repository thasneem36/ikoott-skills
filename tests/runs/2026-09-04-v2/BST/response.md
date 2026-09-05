Alright, let's get into it. **Patient Records using a Binary Search Tree** — this one's worth 20 marks, the single biggest chunk of your assignment alongside the other three structures. So it's worth doing properly, not rushing.

## Basic Concept

Forget patients for a second. Let's understand BST with plain numbers first — that's the cleanest way to see the rule without getting distracted by patient fields.

A Binary Search Tree is just a tree where every node follows one placement rule. Say we insert these numbers in this order: 50, 30, 70, 20, 40, 60, 80.

```
                50
              /    \
            30      70
           /  \    /  \
         20   40  60   80
```

50 goes in first, becomes the root. 30 is smaller than 50, so it goes to the left. 70 is bigger than 50, so it goes to the right. Then 20 is smaller than 50, so we go left to 30 — and 20 is smaller than 30 too, so it becomes 30's left child. Same logic every single time: compare with the current node, go left if smaller, go right if bigger, until you hit an empty spot.

That's it. That's the whole idea of a BST.

## The One Rule

> **Left is always smaller, right is always bigger — compare and move, that's all a BST ever does.**

Keep that sentence in your head. Every method we write today — insert, search, delete, traversal — is just that rule applied in different ways.

## Generic Code — Building It Step By Step

We're going to build this with plain integers first. No Patient objects yet. Once this is solid, we'll swap the data type and reuse the exact same logic.

### Step 1 — The Node class

Every tree is made of nodes. Each node needs to hold a value and know about its left and right children.

File: Node.java
```java
public class Node {
    int data;    // the value stored in this node
    Node left;   // reference to this node's left child (smaller values live here)
    Node right;  // reference to this node's right child (bigger values live here)

    public Node(int data) {   // data: the value we want to store when this node is created
        this.data = data;   // save the value into this node
        this.left = null;   // no left child yet
        this.right = null;  // no right child yet
    }
}
```

Nothing fancy — a value, a left pointer, a right pointer, and a constructor that sets them up. Makes sense so far?

### Step 2 — toString() for Node

Before we move to the tree logic, let's give Node a way to print itself nicely. This is a separate little method on its own — not part of the constructor.

File: Node.java
```java
@Override
public String toString() {
    return "Node(" + data + ")";   // shows the node's value in a readable form when printed
}
```

Small addition, but it'll save us from ugly memory-address output later when we print things.

### Step 3 — The BST class shell

Now the tree itself. A BST just needs to remember one thing: where its root node is.

File: BST.java
```java
public class BST {
    Node root;   // the topmost node of the tree; null means the tree is empty

    public BST() {
        this.root = null;   // a brand-new tree starts empty
    }
}
```

That's the container. Now we add behavior to it, one method at a time.

### Step 4 — insert()

This is the method that places a new value into the tree, following the rule we just learned: smaller goes left, bigger goes right.

File: BST.java
```java
public Node insert(Node current, int value) {
    // current: the node we're currently checking (starts as the root)
    // value: the new number we want to insert into the tree

    if (current == null) {
        return new Node(value);   // found an empty spot, place the new node here
    }

    if (value < current.data) {
        current.left = insert(current.left, value);   // value is smaller, go left
    } else if (value > current.data) {
        current.right = insert(current.right, value);   // value is bigger, go right
    }

    return current;   // hand back this node so the parent's link stays connected
}
```

Notice this method takes `current` as a parameter instead of always starting from `root` inside itself. That's on purpose — it lets the same method call itself again on the left or right side. When you actually use it, you call it like `root = insert(root, value)`, and it rebuilds the chain of links all the way back up.

Does the recursion part make sense — how it keeps calling itself on `current.left` or `current.right` until it finds a null spot?

### Step 5 — search()

Same travel logic as insert, but instead of placing a new node, we're just checking if a value exists.

File: BST.java
```java
public boolean search(Node current, int value) {
    // current: the node we're currently checking (starts as the root)
    // value: the number we're looking for

    if (current == null) {
        return false;   // fell off the tree without finding it — not present
    }

    if (value == current.data) {
        return true;   // found it
    } else if (value < current.data) {
        return search(current.left, value);   // smaller, so search the left side
    } else {
        return search(current.right, value);   // bigger, so search the right side
    }
}
```

Exact same "compare and move" idea — just returning true/false instead of inserting.

### Step 6 — findMin() (helper needed before delete)

Before we write `delete()`, we need one small helper. Here's why: when you delete a node that has TWO children, you can't just remove it — you need to replace it with a value that keeps the tree valid. The safe replacement is the smallest value in that node's right subtree. So we need a way to find the minimum value in a subtree, first.

File: BST.java
```java
public int findMin(Node current) {
    // current: the node we start searching from for the smallest value

    while (current.left != null) {
        current = current.left;   // the smallest value is always the leftmost node
    }

    return current.data;
}
```

Keep going left, left, left — the leftmost node in any subtree is always the smallest. Simple, but delete() depends on this, so we needed it in place first.

### Step 7 — delete()

Now the trickiest one. There are three cases to handle when deleting a node:
1. The node has no children — just remove it.
2. The node has one child — replace it with that child.
3. The node has two children — replace its value with the minimum of its right subtree, then delete that minimum from the right subtree.

File: BST.java
```java
public Node delete(Node current, int value) {
    // current: the node we're currently checking (starts as the root)
    // value: the number we want to remove from the tree

    if (current == null) {
        return null;   // value not found, nothing to delete
    }

    if (value < current.data) {
        current.left = delete(current.left, value);   // target is smaller, go left
    } else if (value > current.data) {
        current.right = delete(current.right, value);   // target is bigger, go right
    } else {
        // this is the node to delete

        if (current.left == null && current.right == null) {
            return null;   // case 1: no children, just remove it
        }

        if (current.left == null) {
            return current.right;   // case 2: only a right child, promote it
        }

        if (current.right == null) {
            return current.left;   // case 2: only a left child, promote it
        }

        // case 3: two children — replace value with the smallest in the right subtree
        int minValue = findMin(current.right);
        current.data = minValue;
        current.right = delete(current.right, minValue);   // remove that duplicate now
    }

    return current;
}
```

That `findMin()` we built in the last step is exactly what gets used in case 3. This is why we always teach a helper before the method that calls it — you needed to understand `findMin()` on its own before seeing it get used here.

Take a moment with the three cases — no child, one child, two children. Clear on why each one is handled differently?

### Step 8 — inorderTraversal()

Last method for this pass. This is how we print all values in ascending order — left subtree, then the node itself, then right subtree.

File: BST.java
```java
public void inorderTraversal(Node current) {
    // current: the node we're currently visiting (starts as the root)

    if (current == null) {
        return;   // nothing here, stop
    }

    inorderTraversal(current.left);     // visit everything smaller first
    System.out.print(current.data + " ");  // then print this node
    inorderTraversal(current.right);    // then visit everything bigger
}
```

Left, then self, then right — that ordering is exactly why it comes out sorted.

## Generic Main Method Demonstration

We've got all the methods, but right now they just sit there unused. A class with methods and nobody calling them doesn't actually do anything — we need a `Main.java` to actually run this and see it work.

File: Main.java
```java
public class Main {
    public static void main(String[] args) {
        BST bst = new BST();   // create an empty tree

        bst.root = bst.insert(bst.root, 50);
        bst.root = bst.insert(bst.root, 30);
        bst.root = bst.insert(bst.root, 70);
        bst.root = bst.insert(bst.root, 20);
        bst.root = bst.insert(bst.root, 40);
        bst.root = bst.insert(bst.root, 60);
        bst.root = bst.insert(bst.root, 80);

        System.out.println("In-order traversal:");
        bst.inorderTraversal(bst.root);   // should print: 20 30 40 50 60 70 80
        System.out.println();

        System.out.println("Search 40: " + bst.search(bst.root, 40));   // true
        System.out.println("Search 99: " + bst.search(bst.root, 99));   // false

        bst.root = bst.delete(bst.root, 30);   // delete a node with two children
        System.out.println("After deleting 30:");
        bst.inorderTraversal(bst.root);
        System.out.println();
    }
}
```

Run this in your head with me: insert builds the tree from the diagram we drew earlier, in-order traversal prints them sorted, search checks existence, delete removes 30 and the tree fixes itself. That's the whole generic BST working end to end.

Good with all of this before we move to the real assignment data?

---

Now that the logic is solid, let's move to what your assignment actually asks for. Same exact logic — insert, search, delete, in-order traversal — we're not changing any of the rules. The only thing that changes is what we're storing: instead of a plain `int`, each node will hold a full `Patient` object, and the tree will be keyed by **Patient ID**. That's it. Everything else — left smaller, right bigger, the three delete cases, the recursion pattern — stays identical.

## Assessment Code — Building It Step By Step

### Step 1 — The Patient class

First, we need a class to represent a real patient record, with the fields your assignment asks for: Patient ID, Name, Age, Contact Number, Medical Condition.

File: Patient.java
```java
public class Patient {
    int patientId;            // unique ID used as the BST key
    String name;               // patient's full name
    int age;                    // patient's age
    String contactNumber;      // patient's phone number
    String medicalCondition;   // patient's current medical condition

    public Patient(int patientId, String name, int age, String contactNumber, String medicalCondition) {
        // patientId: unique ID for this patient, also used to place them in the BST
        // name: the patient's full name
        // age: the patient's age
        // contactNumber: the patient's phone number
        // medicalCondition: the condition they're being treated for
        this.patientId = patientId;
        this.name = name;
        this.age = age;
        this.contactNumber = contactNumber;
        this.medicalCondition = medicalCondition;
    }
}
```

Five fields, one constructor to set them. Nothing new conceptually — just more fields than our generic `int`.

### Step 2 — toString() for Patient

Just like we did for `Node` in the generic pass, let's give `Patient` its own printable form — this makes our traversal output actually readable instead of just an ID.

File: Patient.java
```java
@Override
public String toString() {
    return "Patient[ID=" + patientId + ", Name=" + name + ", Age=" + age
            + ", Contact=" + contactNumber + ", Condition=" + medicalCondition + "]";
}
```

Now whenever we print a Patient, it shows all their details in one readable line.

### Step 3 — The PatientNode class

In the generic pass, `Node` held an `int`. Now our node needs to hold a `Patient` object instead.

File: PatientNode.java
```java
public class PatientNode {
    Patient patient;      // the patient record stored in this node
    PatientNode left;     // reference to the left child (smaller Patient ID)
    PatientNode right;    // reference to the right child (bigger Patient ID)

    public PatientNode(Patient patient) {   // patient: the Patient record to store in this new node
        this.patient = patient;
        this.left = null;   // no left child yet
        this.right = null;  // no right child yet
    }
}
```

Exact same shape as `Node.java` earlier — value, left, right, constructor. Only the value's type changed from `int` to `Patient`.

### Step 4 — The PatientBST class shell

File: PatientBST.java
```java
public class PatientBST {
    PatientNode root;   // the topmost node of the tree; null means the tree is empty

    public PatientBST() {
        this.root = null;   // a brand-new tree starts empty
    }
}
```

Same shell as `BST.java`, just renamed and pointing at `PatientNode`.

### Step 5 — insert()

Same insert logic as before, but now we compare `patientId` instead of comparing the value directly.

File: PatientBST.java
```java
public PatientNode insert(PatientNode current, Patient patient) {
    // current: the node we're currently checking (starts as the root)
    // patient: the new Patient record we want to insert into the tree

    if (current == null) {
        return new PatientNode(patient);   // found an empty spot, place the new node here
    }

    if (patient.patientId < current.patient.patientId) {
        current.left = insert(current.left, patient);   // smaller ID, go left
    } else if (patient.patientId > current.patient.patientId) {
        current.right = insert(current.right, patient);   // bigger ID, go right
    }

    return current;   // hand back this node so the parent's link stays connected
}
```

Same shape as before — the only real difference is we're now comparing `patient.patientId` instead of a raw `int`.

### Step 6 — search()

File: PatientBST.java
```java
public Patient search(PatientNode current, int patientId) {
    // current: the node we're currently checking (starts as the root)
    // patientId: the ID we're looking for

    if (current == null) {
        return null;   // fell off the tree without finding it — not present
    }

    if (patientId == current.patient.patientId) {
        return current.patient;   // found it, return the actual Patient record
    } else if (patientId < current.patient.patientId) {
        return search(current.left, patientId);   // smaller, search the left side
    } else {
        return search(current.right, patientId);   // bigger, search the right side
    }
}
```

Instead of returning `true`/`false` like the generic version, this returns the actual `Patient` record (or `null` if not found) — more useful for a real system where you'd want to display the patient's details after finding them.

### Step 7 — findMin() (helper needed before delete)

Same reason as before — delete needs this for the two-children case, so we build it first.

File: PatientBST.java
```java
public Patient findMin(PatientNode current) {
    // current: the node we start searching from for the smallest Patient ID

    while (current.left != null) {
        current = current.left;   // the smallest ID is always the leftmost node
    }

    return current.patient;
}
```

### Step 8 — delete()

Same three cases as the generic version — no children, one child, two children.

File: PatientBST.java
```java
public PatientNode delete(PatientNode current, int patientId) {
    // current: the node we're currently checking (starts as the root)
    // patientId: the ID of the patient we want to remove

    if (current == null) {
        return null;   // not found, nothing to delete
    }

    if (patientId < current.patient.patientId) {
        current.left = delete(current.left, patientId);   // target is smaller, go left
    } else if (patientId > current.patient.patientId) {
        current.right = delete(current.right, patientId);   // target is bigger, go right
    } else {
        // this is the node to delete

        if (current.left == null && current.right == null) {
            return null;   // case 1: no children
        }

        if (current.left == null) {
            return current.right;   // case 2: only a right child
        }

        if (current.right == null) {
            return current.left;   // case 2: only a left child
        }

        // case 3: two children — replace with the smallest patient in the right subtree
        Patient minPatient = findMin(current.right);
        current.patient = minPatient;
        current.right = delete(current.right, minPatient.patientId);   // remove that duplicate now
    }

    return current;
}
```

Identical structure to the generic `delete()` — just swapped `int value` for `int patientId`, and we're moving `Patient` objects around instead of raw numbers.

### Step 9 — inorderTraversal()

File: PatientBST.java
```java
public void inorderTraversal(PatientNode current) {
    // current: the node we're currently visiting (starts as the root)

    if (current == null) {
        return;   // nothing here, stop
    }

    inorderTraversal(current.left);        // visit smaller Patient IDs first
    System.out.println(current.patient);   // print this patient (uses Patient's toString)
    inorderTraversal(current.right);       // then visit bigger Patient IDs
}
```

This is where that `toString()` we wrote earlier pays off — `System.out.println(current.patient)` automatically uses it to print a clean, readable line per patient.

## Assessment Main Method Demonstration

Now let's actually run this with real patient data.

File: Main.java
```java
public class Main {
    public static void main(String[] args) {
        PatientBST patientBST = new PatientBST();   // create an empty patient tree

        patientBST.root = patientBST.insert(patientBST.root,
                new Patient(105, "Nimal Perera", 45, "0771234567", "Fracture"));
        patientBST.root = patientBST.insert(patientBST.root,
                new Patient(102, "Kamala Silva", 30, "0719876543", "Fever"));
        patientBST.root = patientBST.insert(patientBST.root,
                new Patient(110, "Ruwan Fernando", 60, "0754561234", "Chest Pain"));
        patientBST.root = patientBST.insert(patientBST.root,
                new Patient(101, "Anjali Rathnayake", 22, "0701112233", "Sprain"));
        patientBST.root = patientBST.insert(patientBST.root,
                new Patient(108, "Saman Kumara", 50, "0765554443", "Burn"));

        System.out.println("All patients (in-order by Patient ID):");
        patientBST.inorderTraversal(patientBST.root);

        System.out.println("\nSearching for Patient ID 108:");
        Patient found = patientBST.search(patientBST.root, 108);
        System.out.println(found != null ? found : "Not found");

        System.out.println("\nDeleting Patient ID 102:");
        patientBST.root = patientBST.delete(patientBST.root, 102);

        System.out.println("Patients after deletion:");
        patientBST.inorderTraversal(patientBST.root);
    }
}
```

This is basically what your assignment expects for the BST component: insert patients, search by ID, delete a patient, and display everyone in ascending Patient ID order using in-order traversal.

## Class Closing

Quick recap of what we covered:
- Generic pass: built `Node.java` and `BST.java` from scratch — insert, search, findMin, delete, in-order traversal — all with plain integers, plus a `Main.java` to run it.
- Assessment pass: rebuilt the exact same logic with `Patient.java`, `PatientNode.java`, and `PatientBST.java`, keyed by `patientId` instead of a raw number, and ran it with real patient records.

One line to remember: **the logic never changes, only the data type does — that's the whole trick to applying any data structure to a real assignment.**

## Git — Committing This Work

The BST topic is fully done now — both the generic version and the real Patient version, all four operations. This is exactly the point where we commit, not before. Two meaningful commits make sense here, matching the kind of commit history your assignment expects:

```
git add .
git commit -m "Implemented patient BST"
```

This one covers `Patient.java`, `PatientNode.java`, `PatientBST.java`, and the `insert()` method — the tree exists and you can build it.

```
git add .
git commit -m "Added BST search and deletion"
```

This one covers `search()`, `findMin()`, `delete()`, and `inorderTraversal()` — the rest of the BST behavior.

Two small, meaningful commits instead of one giant dump — that's exactly what "small, frequent, meaningful commits = strong evidence" means. This is also literally one of the example commit messages your assignment lists, so you're matching what's expected.

That's the full BST component — 20 marks worth, done. How are you feeling about it — good to move on to the next part of the learning path, or want me to go over any piece of this again first?
