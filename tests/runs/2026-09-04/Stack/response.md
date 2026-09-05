Alright, let's get into **Treatment History — Stack**. This is worth **20 marks**, same weight as the BST and the Queue, so it deserves the same level of care. Once a patient's treatment is done, we need to store that record somewhere — and a Stack is the perfect fit here. Let's see why.

## Basic Concept

A Stack works on one simple principle: **LIFO — Last In, First Out**.

Think of it like a stack of plates. You put a plate on top, and when you need to take one off, you take the topmost plate first — not the one at the bottom. You can only add and remove from ONE end — the **top**.

Here's the picture:

```
    PUSH 30 -->  |     |  <-- POP removes this first (top)
                 | 30  |
                 | 20  |
                 | 10  |
                 +-----+
                 (bottom)
```

If you push 10, then 20, then 30 — the stack looks like the picture above. When you pop, 30 comes out first, because it went in last.

## The One Rule to Remember

> **"Last one in, first one out — the top is the only door in or out."**

Keep that line in your head. Every operation we write today respects that rule.

## Generic Code — Building the Stack

We're going to build this with a plain generic class first — just `int` data, nothing about patients or treatments yet. We'll build it using a **linked node structure**, one method at a time.

### Step 1 — The Node

**File: `Node.java`**

```java
public class Node {
    int data;      // the value stored in this node
    Node next;     // reference to the next node below this one in the stack

    // Constructor - runs when we create a new Node
    public Node(int data) {   // data: the value we want to store in this node
        this.data = data;     // assign the passed-in value to this node's data field
        this.next = null;     // new node has nothing below it yet
    }
}
```

This is just a box that holds a value and points to the box below it. That's all a Node is.

Understood so far? Good — let's build the Stack class around this.

### Step 2 — The Stack class and its field

**File: `Stack.java`**

```java
public class Stack {
    Node top;   // always points to the topmost node in the stack (null if stack is empty)

    // Constructor - runs when we create a new Stack
    public Stack() {
        this.top = null;   // a brand-new stack starts empty, so top points to nothing
    }
}
```

`top` is the single most important variable here. Every operation we write revolves around this one reference.

### Step 3 — `push()`

**File: `Stack.java`**

```java
public void push(int value) {   // value: the new item we want to add on top of the stack
    Node newNode = new Node(value);  // wrap the value inside a new Node
    newNode.next = top;              // the new node now points down to the current top
    top = newNode;                   // the new node becomes the new top
}
```

Three lines, that's it. We create the node, connect it below to the old top, then move `top` to point at it. Push is always O(1) — instant, no looping.

Make sense? Let's move to checking if the stack is empty, because we need that before we can safely pop.

### Step 4 — `isEmpty()`

**File: `Stack.java`**

```java
public boolean isEmpty() {   // no parameters - just checks the current state of the stack
    return top == null;      // if top points to nothing, the stack has no elements
}
```

Simple check. But this one method is what protects us from crashing later.

### Step 5 — `pop()`

**File: `Stack.java`**

```java
public int pop() {
    if (isEmpty()) {                              // check before removing anything
        System.out.println("Stack is empty!");    // handle the empty case properly
        return -1;                                 // -1 signals "nothing was popped"
    }
    int poppedValue = top.data;   // grab the value sitting at the current top
    top = top.next;               // move top down to the next node, removing the old top
    return poppedValue;           // give back the value that was removed
}
```

Notice we call `isEmpty()` first — that's exactly why we built it before `pop()`. This is the "appropriate handling of an empty stack" the assessment is asking about. Never pop blindly.

### Step 6 — `display()`

**File: `Stack.java`**

```java
public void display() {   // no parameters - just prints the current contents of the stack
    if (isEmpty()) {                               // nothing to show if stack is empty
        System.out.println("Stack is empty!");
        return;
    }
    Node current = top;              // start walking from the top
    System.out.print("Stack (top to bottom): ");
    while (current != null) {        // keep going until we fall off the bottom
        System.out.print(current.data + " ");   // print this node's value
        current = current.next;      // move down to the next node
    }
    System.out.println();
}
```

We always print top-first, because that's the order things would actually come out if we kept popping.

That's the full generic Stack — `push`, `isEmpty`, `pop`, `display`. Before we go further, let's actually run it.

## Generic Main Demonstration

Right now the `Stack` class exists but nothing has actually used it. Without a `Main.java` to call these methods, the class is just sitting there unused — nothing runs on its own.

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        Stack stack = new Stack();   // create a new empty stack

        stack.push(10);   // stack: 10
        stack.push(20);   // stack: 20 -> 10
        stack.push(30);   // stack: 30 -> 20 -> 10

        stack.display();          // should print 30 20 10

        int removed = stack.pop();               // removes 30 (last one in)
        System.out.println("Popped: " + removed);

        stack.display();          // should print 20 10
    }
}
```

Run this and you'll see 30 pop out first, exactly matching LIFO. That confirms the logic is correct before we touch anything related to the real assignment.

Are you clear on the generic Stack before we move to the real one? Let me know if you want me to slow down anywhere here.

## Bridge — Moving to the Assessment

Good — the logic is understood now. We're going to apply the exact same push / isEmpty / pop / display logic to the real assignment requirement: **Treatment History**.

What changes: instead of storing a plain `int`, we store a `TreatmentRecord` object — the completed treatment details for a patient.
What stays identical: the LIFO logic, the structure of every method, the empty-check before popping. Nothing about the actual mechanics changes — only the data type moving through the stack.

## Assessment Code — TreatmentRecord and TreatmentStack

### Step 1 — The TreatmentRecord object

**File: `TreatmentRecord.java`**

```java
public class TreatmentRecord {
    String patientId;          // ID of the patient this treatment belongs to
    String patientName;        // name of the patient
    String treatmentDetails;   // description of the treatment given
    String dateCompleted;      // date/time the treatment was completed

    // Constructor - runs when we create a new TreatmentRecord
    public TreatmentRecord(String patientId, String patientName, String treatmentDetails, String dateCompleted) {
        // patientId: the patient's ID this record belongs to
        // patientName: the patient's name, for quick display
        // treatmentDetails: what treatment was performed
        // dateCompleted: when the treatment was finished
        this.patientId = patientId;
        this.patientName = patientName;
        this.treatmentDetails = treatmentDetails;
        this.dateCompleted = dateCompleted;
    }

    @Override
    public String toString() {   // no parameters - controls how this object prints
        return "[" + patientId + " - " + patientName + " | " + treatmentDetails + " | " + dateCompleted + "]";
    }
}
```

This replaces the plain `int` from earlier. Same idea as `Node`'s `data` field — just a richer object now.

### Step 2 — The TreatmentStack class and its field

**File: `TreatmentStack.java`**

```java
public class TreatmentStack {
    TreatmentNode top;   // always points to the topmost treatment record (null if empty)

    // Constructor - runs when we create a new TreatmentStack
    public TreatmentStack() {
        this.top = null;   // starts empty, nothing treated yet
    }
}
```

Notice we need a node type that wraps `TreatmentRecord` instead of `int`. Let's define that quickly — same shape as our earlier `Node`, just holding a different type.

**File: `TreatmentNode.java`**

```java
public class TreatmentNode {
    TreatmentRecord data;   // the treatment record stored in this node
    TreatmentNode next;     // reference to the next node below this one

    // Constructor - runs when we create a new TreatmentNode
    public TreatmentNode(TreatmentRecord data) {   // data: the treatment record to store
        this.data = data;     // assign the passed-in record to this node
        this.next = null;     // nothing below it yet
    }
}
```

Same structure as before — data type is the only thing that changed.

### Step 3 — `push()`

**File: `TreatmentStack.java`**

```java
public void push(TreatmentRecord record) {   // record: the completed treatment record to add
    TreatmentNode newNode = new TreatmentNode(record);  // wrap the record in a new node
    newNode.next = top;    // new node points down to the current top
    top = newNode;          // new node becomes the new top
}
```

Exact same three lines as the generic version. Only the parameter type changed from `int value` to `TreatmentRecord record`.

### Step 4 — `isEmpty()`

**File: `TreatmentStack.java`**

```java
public boolean isEmpty() {   // no parameters - checks current state of the stack
    return top == null;      // true if there is no top node, meaning stack has no records
}
```

Identical logic, no changes needed.

### Step 5 — `pop()`

**File: `TreatmentStack.java`**

```java
public TreatmentRecord pop() {
    if (isEmpty()) {                                          // check before removing
        System.out.println("No treatment records to remove!"); // empty-case handling
        return null;                                            // null signals nothing was popped
    }
    TreatmentRecord poppedRecord = top.data;   // grab the record at the current top
    top = top.next;                             // move top down, removing old top
    return poppedRecord;                        // return the removed record
}
```

Same structure as before — we still guard with `isEmpty()` first. The only difference is we return `null` instead of `-1`, since we're dealing with an object now, not a number.

### Step 6 — `display()`

**File: `TreatmentStack.java`**

```java
public void display() {   // no parameters - prints all current treatment records
    if (isEmpty()) {
        System.out.println("No treatment records to display!");
        return;
    }
    TreatmentNode current = top;   // start walking from the top
    System.out.println("Treatment History (most recent first):");
    while (current != null) {           // walk until we pass the last node
        System.out.println(current.data);   // uses TreatmentRecord's toString()
        current = current.next;             // move to the next node down
    }
}
```

Most recently completed treatment shows first — which makes sense for a hospital log, you usually want to see the latest treatment at a glance.

## Assessment Main Demonstration

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        TreatmentStack treatmentStack = new TreatmentStack();   // create empty treatment stack

        // create a few completed treatment records
        TreatmentRecord t1 = new TreatmentRecord("P001", "Kamal Perera", "Wound dressing", "2026-09-01");
        TreatmentRecord t2 = new TreatmentRecord("P002", "Nadeesha Silva", "IV fluids administered", "2026-09-02");
        TreatmentRecord t3 = new TreatmentRecord("P003", "Ruwan Fernando", "X-ray and cast applied", "2026-09-03");

        treatmentStack.push(t1);   // Kamal's treatment pushed first
        treatmentStack.push(t2);   // Nadeesha's treatment pushed second
        treatmentStack.push(t3);   // Ruwan's treatment pushed last -> currently on top

        treatmentStack.display();   // should show Ruwan first, then Nadeesha, then Kamal

        TreatmentRecord removed = treatmentStack.pop();   // removes Ruwan's record (most recent)
        System.out.println("Removed record: " + removed);

        treatmentStack.display();   // should now show Nadeesha, then Kamal
    }
}
```

Run this, and you'll see Ruwan's record pop off first — because it was the last treatment completed. That's LIFO doing exactly what the assessment expects from the Treatment History component.

## Class Closing

Quick recap: we built a Stack from scratch — `push`, `isEmpty`, `pop`, `display` — first with plain integers to lock in the LIFO logic, then rebuilt the exact same four methods using `TreatmentRecord` objects for the real Treatment History requirement. The logic never changed — only the data type did.

One takeaway line: **the top is the only door — everything goes in and comes out from there, last in, first out.**

That covers the full 20 marks for Treatment History — Stack. Once you're ready, we can commit this piece of work with a proper message before moving to the next topic. Sound good, or do you want to go over any part of this again first?

---

Since the whole topic is fully done now — both the generic pass and the real Treatment Stack — this is the point where we make a commit for it. Not before, not halfway through.

```
git add .
git commit -m "Implemented treatment stack"
```

`git add .` stages everything you changed — `TreatmentRecord.java`, `TreatmentNode.java`, `TreatmentStack.java`, and your updated `Main.java`. `git commit -m "..."` saves that as one meaningful checkpoint in your history, with a message that clearly says what this commit represents. This is exactly the kind of small, meaningful commit the assessment is looking for — not one giant dump at the end.

Ready to move on to the next part of the learning path, or do you want to stay here a bit longer?
