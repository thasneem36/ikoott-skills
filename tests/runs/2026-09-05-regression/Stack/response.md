Alright, let's move into **Treatment History — Stack**. This one is worth 20 marks on its own, so it matters just as much as the BST or the Queue. Let's build it properly.

## 1. Basic Concept

Forget patients for a second. Think of a stack of plates. You put a plate on top, and when you need one, you take from the top too. You never pull one from the bottom or the middle.

That's exactly what a Stack data structure does. The last thing you add is the first thing that comes out.

Here's a small picture of it, using plain numbers:

```
Push 10, then 20, then 30:

   push 10      push 20      push 30
   -------      -------      -------
                            |  30  | <- TOP
                |  20  |    |  20  |
   |  10  |     |  10  |    |  10  |
   -------      -------     -------

Now if we pop():
   removes 30 first (last one in, first one out)
```

So the "top" pointer always tracks whichever element was added most recently. That's the whole idea.

## 2. One Memorable Rule

> **Stack = LIFO — Last In, First Out. Whatever went in last comes out first.**

Keep that one line in your head for everything we build next.

## 3. Generic Code — Building It Step by Step

We're going to build this with plain integers first, no patient data yet. Two classes: a `Node` (the box that holds a value) and a `Stack` (the container that manages the boxes).

### Step 1 — Node skeleton

File: `Node.java`

```java
// File: Node.java
public class Node {
    int data;   // the value this node holds
    Node next;  // pointer to the node sitting below this one in the stack

    public Node(int data) { // data: the value to store in this new node
        this.data = data; // save the value passed in
        this.next = null; // this node has nothing below it yet
    }
}
```

That's it for `Node` — just a value and a pointer. Nothing fancy. Make sense before we move on?

### Step 2 — Stack skeleton

File: `Stack.java`

```java
// File: Stack.java
public class Stack {
    private Node top;  // reference to the topmost node in the stack
    private int size;  // how many elements are currently stored

    public Stack() {
        this.top = null; // stack starts completely empty
        this.size = 0;   // zero elements at the start
    }
}
```

Just fields and a constructor here — no logic yet. That's deliberate, we add behaviour one method at a time.

### Step 3 — isEmpty()

File: `Stack.java`

```java
// File: Stack.java
public boolean isEmpty() {
    return top == null; // if nothing is being pointed at by top, the stack has no elements
}
```

Small method, but we'll lean on it in almost everything else, since a stack must always handle the "nothing in here" case cleanly.

### Step 4 — push()

File: `Stack.java`

```java
// File: Stack.java
public void push(int value) { // value: the number we want to add to the top of the stack
    Node newNode = new Node(value); // wrap the value in a new node
    newNode.next = top;             // the new node points down to whatever was previously on top
    top = newNode;                  // the new node now becomes the top
    size++;                         // one more element is now in the stack
}
```

Notice the order: point the new node down first, THEN move top up to it. If you did it the other way around you'd lose the rest of the stack.

### Step 5 — pop()

File: `Stack.java`

```java
// File: Stack.java
public int pop() {
    if (isEmpty()) { // nothing to remove
        System.out.println("Stack is empty. Cannot pop.");
        return -1; // sentinel value since there's no real data to return
    }
    int value = top.data; // grab the value at the top before we lose the reference to it
    top = top.next;        // move top down to the next node
    size--;                // one less element in the stack
    return value;          // hand the removed value back to whoever called pop()
}
```

This is where `isEmpty()` from Step 3 earns its keep — we check it first before touching anything.

### Step 6 — display()

File: `Stack.java`

```java
// File: Stack.java
public void display() {
    if (isEmpty()) { // nothing to print
        System.out.println("Stack is empty.");
        return;
    }
    Node current = top; // start walking from the top
    System.out.print("Stack (top to bottom): ");
    while (current != null) {              // keep going until there are no more nodes
        System.out.print(current.data + " "); // print this node's value
        current = current.next;               // step down to the next node
    }
    System.out.println();
}
```

That covers push, pop, display, and the empty-stack handling — everything the assessment asks for on the generic level. Good so far?

## 4. Generic Main Demonstration

All four methods exist now, but a class sitting alone does nothing. We need a `Main` that actually creates a `Stack` object and calls these methods, otherwise none of this code ever runs.

File: `Main.java`

```java
// File: Main.java
public class Main {
    public static void main(String[] args) {
        Stack stack = new Stack(); // create an empty stack

        stack.push(10); // push 10 onto the stack
        stack.push(20); // push 20 onto the stack
        stack.push(30); // push 30 onto the stack

        stack.display(); // show the stack from top to bottom

        int removed = stack.pop(); // remove whatever is on top
        System.out.println("Popped: " + removed);

        stack.display(); // show the stack again, after the pop
    }
}
```

Run this in your head: push 10, 20, 30 → top is 30. Pop takes 30 off first. That's LIFO in action.

## 5. Bridge Line

Okay — the logic is solid now. Push, pop, display, empty-check, all understood with plain numbers. Now we do the exact same thing again, except instead of a `Node` holding an `int`, we hold a full `TreatmentRecord`. The rules don't change at all — only the type of data sitting inside each node changes.

## 6. Assessment Code — Treatment History

Same one-method-at-a-time approach, just with the real objects this time.

### Step 1 — TreatmentRecord skeleton

File: `TreatmentRecord.java`

```java
// File: TreatmentRecord.java
public class TreatmentRecord {
    int patientId;            // ID of the patient who received treatment
    String patientName;       // name of the patient
    String treatmentDetails;  // what treatment or procedure was carried out
    String dateCompleted;     // the date this treatment was completed
    TreatmentRecord next;     // pointer to the treatment record below this one in the stack

    public TreatmentRecord(int patientId, String patientName, String treatmentDetails, String dateCompleted) {
        // patientId: ID of the treated patient
        // patientName: name of the treated patient
        // treatmentDetails: description of the treatment performed
        // dateCompleted: date the treatment was finished
        this.patientId = patientId;
        this.patientName = patientName;
        this.treatmentDetails = treatmentDetails;
        this.dateCompleted = dateCompleted;
        this.next = null; // nothing below this record yet
    }
}
```

This plays the exact same role `Node` played before — it's just carrying more information now.

### Step 2 — TreatmentStack skeleton

File: `TreatmentStack.java`

```java
// File: TreatmentStack.java
public class TreatmentStack {
    private TreatmentRecord top; // reference to the most recently completed treatment record
    private int size;            // how many treatment records are currently stored

    public TreatmentStack() {
        this.top = null; // no treatment records yet
        this.size = 0;   // starts empty
    }
}
```

### Step 3 — isEmpty()

File: `TreatmentStack.java`

```java
// File: TreatmentStack.java
public boolean isEmpty() {
    return top == null; // no top record means there's no treatment history yet
}
```

### Step 4 — push()

File: `TreatmentStack.java`

```java
// File: TreatmentStack.java
public void push(TreatmentRecord record) { // record: the completed treatment record to store
    record.next = top; // new record points down to whatever was previously on top
    top = record;        // this new record becomes the top of the stack
    size++;               // one more treatment record is now stored
}
```

Same exact structure as generic `push()` — only the parameter type changed from `int` to `TreatmentRecord`.

### Step 5 — pop()

File: `TreatmentStack.java`

```java
// File: TreatmentStack.java
public TreatmentRecord pop() {
    if (isEmpty()) { // nothing to remove
        System.out.println("No treatment records to remove.");
        return null; // nothing to hand back
    }
    TreatmentRecord removed = top; // grab the top record before losing the reference
    top = top.next;                 // move top down to the next record
    size--;                          // one less record stored
    return removed;                  // hand back the removed record
}
```

### Step 6 — display()

File: `TreatmentStack.java`

```java
// File: TreatmentStack.java
public void display() {
    if (isEmpty()) { // nothing to show
        System.out.println("No treatment records available.");
        return;
    }
    TreatmentRecord current = top; // start from the most recently completed treatment
    System.out.println("Treatment History (most recent first):");
    while (current != null) { // walk down the stack until there are no more records
        System.out.println("Patient ID: " + current.patientId
            + ", Name: " + current.patientName
            + ", Treatment: " + current.treatmentDetails
            + ", Date: " + current.dateCompleted); // print this record's details
        current = current.next; // move down to the next record
    }
}
```

That's the full `TreatmentStack` — push, pop, display, and empty handling, all working on real patient treatment records now.

## 7. Assessment Main Demonstration

File: `Main.java`

```java
// File: Main.java
public class Main {
    public static void main(String[] args) {
        TreatmentStack treatmentStack = new TreatmentStack(); // create an empty treatment history stack

        treatmentStack.push(new TreatmentRecord(101, "Nimal Perera", "Wound dressing", "2026-09-01"));
        treatmentStack.push(new TreatmentRecord(102, "Kamala Silva", "X-ray and cast", "2026-09-02"));
        treatmentStack.push(new TreatmentRecord(103, "Ruwan Fernando", "IV fluids", "2026-09-03"));

        treatmentStack.display(); // show all completed treatments, most recent first

        TreatmentRecord removed = treatmentStack.pop(); // remove the most recently completed treatment
        System.out.println("Removed record for: " + removed.patientName);

        treatmentStack.display(); // show what's left after the pop
    }
}
```

Ruwan's record was pushed last, so it's the first one popped off. That's your LIFO rule, now working on actual treatment data for the assignment.

## 8. Git Checkpoint

Treatment History is fully built now — both the generic version and the real assessment version. This is exactly the point where we commit, since the whole topic is done, not half-done.

```
git add .
git commit -m "Implemented treatment stack"
```

One clean, meaningful commit for this whole component. Don't touch this again until the next topic actually changes these files.

## 9. Class Closing

Quick recap: we built a Stack from scratch — first with plain integers so the LIFO logic was crystal clear, then rebuilt the exact same push, pop, display, and empty-check logic using real `TreatmentRecord` objects for the hospital system. Nothing about the logic changed between the two — only the data type did.

**Takeaway: a Stack always gives you back the last thing you put in, first — that's what makes it perfect for "most recently completed treatment first."**

That's Treatment History done, 20 marks banked. Ready to move on to the next part, or do you want to go over anything here again first?
