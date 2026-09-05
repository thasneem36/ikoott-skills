Alright, let's get into **Stack — Treatment History**. This one's worth 20 marks on its own, same weight as the BST and the Queue. So it matters just as much. Let's build it properly.

## The Basic Concept

Forget patients and treatments for a second. Let's understand Stack with plain numbers first.

A Stack only lets you do things at ONE end — called the **top**. You add on top, and you remove from the top. You can never touch the bottom directly, and you can never touch the middle directly.

Here's the picture:

```
push(10)      push(20)      push(30)       pop()
                                            removes 30 first
   |            | 20 |         | 30 |          | 20 |
   | 10 |       | 10 |         | 20 |          | 10 |
   +----+       +----+         | 10 |          +----+
                                +----+
   top=10       top=20         top=30          top=20
```

Look at the order things come out. 10 went in first, 20 next, 30 last. But when we pop, 30 comes out FIRST — not 10. The last thing that went in is the first thing that comes out.

## The One Rule to Remember

> **Last In, First Out. Whatever you pushed most recently is the first thing you pop.**

That's the whole logic of a Stack. Everything else is just implementation.

## Generic Code — Building It Step by Step

We're not using Java's built-in `Stack` class. We're building our own, using a linked structure, so you actually understand what's happening underneath. Let's go one method at a time — don't rush ahead.

### Step 1 — The Node

Every stack element needs a small box to sit in. That box holds the value, and a link to the box below it.

**File: Node.java**
```java
public class Node {
    int data;      // the actual value stored in this stack element
    Node next;      // reference to the node sitting below this one in the stack

    // Constructor - runs when we create a new Node
    public Node(int data) {   // data: the value we want to store in this node
        this.data = data;     // save the passed-in value into this node's data field
        this.next = null;     // this node has nothing below it yet, so next starts empty
    }
}
```

Nothing fancy here. `data` holds the value. `next` points to whatever is beneath it in the stack. That's it.

### Step 2 — Printing a Node Nicely

Before we move to the Stack class itself, let's give `Node` a clean way to print itself. This is a separate step — we don't cram it into the constructor.

**File: Node.java**
```java
    // toString - controls how a Node looks when printed
    @Override
    public String toString() {
        return "" + data;   // just show the raw value, nothing extra
    }
}
```

Small thing, but it makes our `display()` output readable later, instead of printing memory addresses.

Understood so far? Push through — next we build the actual Stack class.

### Step 3 — The Stack Class and Its Field

Now the class that manages the whole stack. It only needs to remember ONE thing: what's currently on top.

**File: MyStack.java**
```java
public class MyStack {
    Node top;   // points to the node currently at the top of the stack

    // Constructor - runs when we create a new, empty stack
    public MyStack() {
        this.top = null;   // a brand-new stack starts with nothing in it
    }
}
```

That `top` reference is the heart of the whole class. Every operation we write next either reads it or moves it.

### Step 4 — isEmpty() (the helper we'll need soon)

Before we write `pop()` or `display()`, we need a way to check if the stack has anything in it at all. Popping from an empty stack, or displaying an empty stack, has to be handled safely — the assessment specifically asks for this. So we build the check first, as its own method.

**File: MyStack.java**
```java
    // isEmpty - checks whether the stack currently has any elements
    public boolean isEmpty() {
        return top == null;   // if top is not pointing to any node, the stack is empty
    }
}
```

This little method is going to be used inside both `pop()` and `display()` in a moment. That's why we teach it first, on its own, instead of burying it inside those methods.

### Step 5 — push()

This is how we add something to the stack. New elements always go on top.

**File: MyStack.java**
```java
    // push - adds a new value onto the top of the stack
    public void push(int value) {   // value: the number we want to add to the stack
        Node newNode = new Node(value);   // wrap the value in a new node
        newNode.next = top;               // the new node now points down to the old top
        top = newNode;                    // the new node becomes the new top
    }
}
```

Three lines. Wrap the value, link it under the old top, then move `top` to point at it. That's a push.

### Step 6 — pop()

This removes and returns whatever is currently on top. This is where we use the `isEmpty()` check we built earlier.

**File: MyStack.java**
```java
    // pop - removes and returns the value currently on top of the stack
    public int pop() {
        if (isEmpty()) {                                   // check before touching anything
            System.out.println("Stack is empty. Nothing to pop.");
            return -1;   // sentinel value signaling "nothing was popped"
        }
        int poppedValue = top.data;   // grab the value sitting at the top
        top = top.next;               // move top down to the next node
        return poppedValue;           // hand back the value we removed
    }
}
```

See how `isEmpty()` from Step 4 is just reused here, not rewritten? That's exactly why we built it separately first.

### Step 7 — display()

Now let's print out everything currently in the stack, from top to bottom. Same empty check applies here too.

**File: MyStack.java**
```java
    // display - prints every value currently in the stack, from top to bottom
    public void display() {
        if (isEmpty()) {                                   // nothing to show if the stack is empty
            System.out.println("Stack is empty.");
            return;
        }
        Node current = top;         // start walking from the top
        while (current != null) {   // keep going until we fall off the bottom
            System.out.print(current + " ");   // uses the toString() we wrote earlier
            current = current.next;             // step down to the next node
        }
        System.out.println();
    }
}
```

That completes `MyStack.java` — constructor, `isEmpty()`, `push()`, `pop()`, `display()`. Four operations, each one built and understood on its own.

## Generic Main Method — Making It Actually Run

Right now we just have classes sitting there. Nothing runs on its own. We need a `Main.java` to actually create a stack and use it — without this, the class exists but nothing actually runs.

**File: Main.java**
```java
public class Main {
    public static void main(String[] args) {
        MyStack stack = new MyStack();   // create a new, empty stack

        stack.push(10);   // stack: 10
        stack.push(20);   // stack: 20 10
        stack.push(30);   // stack: 30 20 10

        System.out.println("Current stack (top to bottom):");
        stack.display();

        int removed = stack.pop();   // removes 30, since it was pushed last
        System.out.println("Popped value: " + removed);

        System.out.println("Stack after pop:");
        stack.display();
    }
}
```

Run this in your head: push 10, 20, 30 — top is 30. Pop takes 30 off first. That's LIFO, exactly like our rule said.

That's the full generic pass. Node holds a value, Stack manages the top, push/pop/display work off that one pointer. Solid so far? Let's move to the real assignment version.

## Bridge — Now Let's Apply This to the Assignment

Good — the logic is understood now. We're going to apply the exact same Stack logic to the real requirement: **Treatment History**.

Nothing about the LOGIC changes. Push still adds to the top, pop still removes from the top, LIFO still applies. The only thing that changes is WHAT we're storing — instead of a plain `int`, each stack element now holds a full **treatment record** with real patient/treatment details.

## Assessment Code — Same Steps, Real Object

### Step 1 — TreatmentRecord.java

This is the data itself — one completed treatment, with enough detail to be useful.

**File: TreatmentRecord.java**
```java
public class TreatmentRecord {
    int patientId;               // ID of the patient who received treatment
    String patientName;          // name of the patient
    String treatmentDescription; // what treatment was given
    String doctorName;           // doctor who carried out the treatment
    String dateCompleted;        // date the treatment was completed

    // Constructor - runs when we create a new completed treatment record
    public TreatmentRecord(int patientId, String patientName, String treatmentDescription,
                            String doctorName, String dateCompleted) {
        // patientId: the ID of the patient this treatment belongs to
        // patientName: the patient's name, for quick display
        // treatmentDescription: short text describing what was treated/done
        // doctorName: the doctor who performed the treatment
        // dateCompleted: when the treatment was finished
        this.patientId = patientId;
        this.patientName = patientName;
        this.treatmentDescription = treatmentDescription;
        this.doctorName = doctorName;
        this.dateCompleted = dateCompleted;
    }
}
```

Five fields, all mapped straight from what a completed treatment record should hold.

### Step 2 — toString() for TreatmentRecord

Same as before — separate step, own block, not bundled with the constructor.

**File: TreatmentRecord.java**
```java
    // toString - controls how a treatment record looks when printed
    @Override
    public String toString() {
        return "Patient ID: " + patientId +
               ", Name: " + patientName +
               ", Treatment: " + treatmentDescription +
               ", Doctor: " + doctorName +
               ", Date Completed: " + dateCompleted;
    }
}
```

Now every treatment record prints itself in one readable line instead of a memory address.

### Step 3 — TreatmentNode.java

This is our stack's version of `Node.java` — except now it wraps a whole `TreatmentRecord` instead of an `int`.

**File: TreatmentNode.java**
```java
public class TreatmentNode {
    TreatmentRecord data;   // the completed treatment record stored in this node
    TreatmentNode next;     // reference to the node sitting below this one in the stack

    // Constructor - runs when we create a new node for the treatment stack
    public TreatmentNode(TreatmentRecord data) {   // data: the treatment record to wrap in this node
        this.data = data;   // save the passed-in treatment record into this node
        this.next = null;   // this node has nothing below it yet
    }
}
```

Compare this to `Node.java` from earlier — structurally identical. Only the type of `data` changed, from `int` to `TreatmentRecord`.

### Step 4 — TreatmentStack.java and Its Field

Same idea as `MyStack.java` — one field, `top`, tracking the top of the stack.

**File: TreatmentStack.java**
```java
public class TreatmentStack {
    TreatmentNode top;   // points to the treatment record currently on top of the stack

    // Constructor - runs when we create a new, empty treatment stack
    public TreatmentStack() {
        this.top = null;   // a brand-new treatment stack starts with nothing in it
    }
}
```

### Step 5 — isEmpty()

Same helper, same reason — we need it before `pop()` and `display()` can safely run.

**File: TreatmentStack.java**
```java
    // isEmpty - checks whether the treatment stack currently has any records
    public boolean isEmpty() {
        return top == null;   // if top isn't pointing to any node, the stack is empty
    }
}
```

### Step 6 — push()

Adds one completed treatment record onto the top of the stack.

**File: TreatmentStack.java**
```java
    // push - adds a newly completed treatment record onto the top of the stack
    public void push(TreatmentRecord record) {   // record: the completed treatment record to add
        TreatmentNode newNode = new TreatmentNode(record);   // wrap the record in a new node
        newNode.next = top;                                  // link the new node under the old top
        top = newNode;                                       // new node becomes the new top
    }
}
```

Exactly the same three-line pattern as generic `push()` — only the type going in changed.

### Step 7 — pop()

Removes and returns the most recently completed treatment record. This uses `isEmpty()` from Step 5.

**File: TreatmentStack.java**
```java
    // pop - removes and returns the most recently completed treatment record
    public TreatmentRecord pop() {
        if (isEmpty()) {                                              // check before touching anything
            System.out.println("Treatment stack is empty. Nothing to pop.");
            return null;   // nothing to return, stack has no records
        }
        TreatmentRecord poppedRecord = top.data;   // grab the record sitting on top
        top = top.next;                             // move top down to the next node
        return poppedRecord;                        // hand back the removed record
    }
}
```

### Step 8 — display()

Prints every treatment record currently sitting in the stack, most recent first.

**File: TreatmentStack.java**
```java
    // display - prints every treatment record currently in the stack, top to bottom
    public void display() {
        if (isEmpty()) {                                              // nothing to show if empty
            System.out.println("Treatment stack is empty.");
            return;
        }
        TreatmentNode current = top;   // start walking from the top
        while (current != null) {      // keep going until we fall off the bottom
            System.out.println(current.data);   // uses TreatmentRecord's toString()
            current = current.next;              // step down to the next node
        }
    }
}
```

That's the full `TreatmentStack.java` — constructor, `isEmpty()`, `push()`, `pop()`, `display()`. Same four operations as the generic version, same order, just operating on real treatment data now.

## Assessment Main Method — Real Usage

**File: Main.java**
```java
public class Main {
    public static void main(String[] args) {
        TreatmentStack treatmentStack = new TreatmentStack();   // create an empty treatment history stack

        // create a few completed treatment records
        TreatmentRecord t1 = new TreatmentRecord(101, "Kumar Silva", "Wound dressing", "Dr. Perera", "2026-09-01");
        TreatmentRecord t2 = new TreatmentRecord(102, "Anjali Fernando", "X-ray review", "Dr. Jayasuriya", "2026-09-02");
        TreatmentRecord t3 = new TreatmentRecord(103, "Ruwan Bandara", "IV medication", "Dr. Perera", "2026-09-03");

        // push completed treatments onto the stack as they finish
        treatmentStack.push(t1);
        treatmentStack.push(t2);
        treatmentStack.push(t3);

        System.out.println("Treatment history (most recent first):");
        treatmentStack.display();

        // pop the most recently completed treatment record
        TreatmentRecord lastCompleted = treatmentStack.pop();
        System.out.println("\nMost recently completed treatment (popped):");
        System.out.println(lastCompleted);

        System.out.println("\nTreatment history after pop:");
        treatmentStack.display();
    }
}
```

Run through it: t1, t2, t3 get pushed in that order, so t3 is on top. Pop takes t3 first — the most recently completed treatment — exactly matching what the assignment asks for: "Pop - remove the most recently completed treatment record."

## Class Closing

Quick recap. In the generic pass, we built `Node` and `MyStack` from scratch — a value, a `next` pointer, a `top` reference, and four operations: `isEmpty`, `push`, `pop`, `display`. In the assessment pass, we kept every bit of that logic identical and just swapped `int` for a real `TreatmentRecord` — `TreatmentNode` and `TreatmentStack` do exactly what `Node` and `MyStack` did.

One takeaway line: **the moment you understand LIFO with plain numbers, you already understand it for any object — only the data type changes, never the logic.**

That's Treatment History — Stack, fully done, both passes. Ready to move on, or want to go over any part of this again first?

---

Since the full topic — generic and assessment — is done, this is a good point to commit.

```
git add .
git commit -m "Implemented treatment stack"
```

One meaningful commit for the whole Stack topic, now that both passes are complete — not partway through, not bundled with other data structures.
