Alright, let's get into **Emergency Patient Queue**. This is worth 20 marks on its own, same weight as the BST, so it deserves full attention, not a rushed pass. Let's build it properly.

## The Basic Concept

A Queue is a line. Think of any real queue you've stood in — a ticket counter, a bus stop. Whoever came first gets served first. Nobody can jump ahead, and nobody gets served out of turn. That's it. That's the whole idea.

There are two ends that matter:
- **Front** — where someone leaves the queue (gets removed)
- **Rear** — where someone joins the queue (gets added)

Here's a small diagram before we touch any code:

```
Adding 10, 20, 30 into the queue, one after another:

enqueue(10):
Front -> [10] <- Rear

enqueue(20):
Front -> [10] -> [20] <- Rear

enqueue(30):
Front -> [10] -> [20] -> [30] <- Rear

Now dequeue() removes from the FRONT:
removes 10
Front -> [20] -> [30] <- Rear
```

New items always join at the rear. Removals always happen at the front. Nothing else is allowed.

## One Memorable Rule

> **First In, First Out. Whoever joined the line first, leaves the line first.**

That's FIFO. Keep that sentence in your head — it drives every operation we're about to write.

## Generic Code — Building It Piece by Piece

We are NOT touching Patient objects yet. First we build a plain queue that just stores integers, so the logic is crystal clear with zero distractions.

We need two files: one for the node (a single slot in the line), and one for the queue itself (the thing that manages front and rear).

**File: `QueueNode.java`**

```java
public class QueueNode {
    int data;       // the value stored in this queue node
    QueueNode next; // pointer to the next node in the queue (who is standing behind this one)

    public QueueNode(int data) { // data: the value this node should hold when it's created
        this.data = data;  // store the value passed in
        this.next = null;  // brand new node has nobody behind it yet
    }
}
```

This is just a box that holds a value and knows who's next in line behind it. Nothing fancy.

Now the queue class itself. We build this **one method at a time**. Don't rush to the next one until this one makes sense.

**File: `MyQueue.java` — starting with the fields and `enqueue`**

```java
public class MyQueue {
    QueueNode front; // points to the first node in the queue (the next one to be removed)
    QueueNode rear;  // points to the last node in the queue (the most recently added one)

    public void enqueue(int value) { // value: the new integer we want to add to the back of the queue
        QueueNode newNode = new QueueNode(value); // wrap the value in a new node

        if (rear == null) {  // this means the queue is currently empty
            front = newNode; // the new node becomes the front...
            rear = newNode;  // ...and the rear, since it's the only one in line
        } else {
            rear.next = newNode; // the current last person points to the new person behind them
            rear = newNode;      // now the new node officially becomes the last person in line
        }
    }
}
```

`enqueue` only ever touches the rear. It never looks at the front. That's the whole point — joining a queue happens at the back.

Understood so far? Good. Let's add the next method.

**`dequeue` — removing from the front**

```java
public int dequeue() { // no arguments needed — we always remove from the front, never from the middle
    if (front == null) { // this means the queue is empty, there's nobody to remove
        System.out.println("Queue is empty, cannot dequeue.");
        return -1; // sentinel value to signal "nothing was removed"
    }

    int removedValue = front.data; // grab the value at the front before we lose the reference to it
    front = front.next; // move the front pointer forward, to the next person in line

    if (front == null) { // if that removal emptied the queue completely
        rear = null; // reset rear too, otherwise it would still point at a node that's gone
    }

    return removedValue; // hand back the value that was just removed
}
```

Notice the empty-queue check right at the top — that's the "appropriate handling of an empty queue" the assessment specifically asks for. Never skip that check, or your program crashes the moment someone dequeues from nothing.

**`display` — showing what's currently waiting**

```java
public void display() { // no arguments — we just walk the queue from front to rear and print it
    if (front == null) { // handle the empty case first
        System.out.println("Queue is empty.");
        return;
    }

    QueueNode current = front; // start walking from the front
    System.out.print("Front -> ");
    while (current != null) { // keep going until we've passed the last node
        System.out.print(current.data + " -> ");
        current = current.next; // step forward to the next node
    }
    System.out.println("Rear");
}
```

**`isEmpty` — a quick helper**

```java
public boolean isEmpty() { // no arguments — just checks the current state of the queue
    return front == null; // true if there's no front node, meaning nobody is waiting
}
```

That's the full generic queue: `enqueue`, `dequeue`, `display`, `isEmpty`. Four small methods, each doing exactly one job.

## Generic Main Demonstration

Right now, `MyQueue` is just a class sitting there — nothing has actually run yet. We need a `Main.java` to create it and call these methods, otherwise the class exists but does nothing.

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        MyQueue queue = new MyQueue(); // create an empty queue

        queue.enqueue(10); // 10 joins the line
        queue.enqueue(20); // 20 joins the line
        queue.enqueue(30); // 30 joins the line

        queue.display(); // should print: Front -> 10 -> 20 -> 30 -> Rear

        int removed = queue.dequeue(); // removes 10, since it's been waiting the longest
        System.out.println("Removed: " + removed);

        queue.display(); // should print: Front -> 20 -> 30 -> Rear
    }
}
```

Run that in your head: enqueue three values, print the line, dequeue one, print the line again. If the output matches what's in the comments, the logic is solid.

Make sense so far? This generic version is the exact same logic we're about to reuse — just with plain numbers instead of real data.

## Bridge to the Assessment

Good — the logic is understood. Now we apply the SAME exact logic to the real assignment object: `Patient`. Nothing about the FIFO rule changes. `enqueue` still only touches the rear, `dequeue` still only touches the front, the empty check is still there. The only thing that changes is what we're storing — instead of a plain `int`, each node now holds a full `Patient` record.

## Assessment Code — Same Methods, Real Object

First, the `Patient` class itself, holding the fields the assignment asks for.

**File: `Patient.java`**

```java
public class Patient {
    int patientId;    // unique ID used to identify this patient
    String name;      // patient's full name
    int age;          // patient's age
    String contact;   // patient's contact number
    String condition; // patient's medical condition / reason for visit

    public Patient(int patientId, String name, int age, String contact, String condition) {
        // patientId: unique ID for this patient
        // name: the patient's full name
        // age: the patient's age
        // contact: the patient's contact number
        // condition: the patient's medical condition on arrival
        this.patientId = patientId; // store the ID passed in
        this.name = name;           // store the name passed in
        this.age = age;             // store the age passed in
        this.contact = contact;     // store the contact number passed in
        this.condition = condition; // store the medical condition passed in
    }
}
```

Now the node that holds a `Patient` instead of an `int`.

**File: `PatientQueueNode.java`**

```java
public class PatientQueueNode {
    Patient patient;       // the patient stored in this node
    PatientQueueNode next; // pointer to the next node in the queue

    public PatientQueueNode(Patient patient) { // patient: the patient object this node should wrap
        this.patient = patient; // store the patient passed in
        this.next = null;       // brand new node has nobody behind it yet
    }
}
```

Now we rebuild the queue class, one method at a time again, exactly like before.

**File: `PatientQueue.java` — fields and `enqueue`**

```java
public class PatientQueue {
    PatientQueueNode front; // points to the first patient in line (next to be treated)
    PatientQueueNode rear;  // points to the last patient in line (most recently arrived)

    public void enqueue(Patient patient) { // patient: the new patient arriving at the emergency unit
        PatientQueueNode newNode = new PatientQueueNode(patient); // wrap the patient in a new node

        if (rear == null) {  // queue is currently empty, nobody waiting
            front = newNode; // new node becomes the front...
            rear = newNode;  // ...and the rear
        } else {
            rear.next = newNode; // current last patient points to the new arrival
            rear = newNode;      // new arrival is now the last one in line
        }
    }
}
```

Same structure as the generic version. Only the type changed — `int` became `Patient`.

**`dequeue` — the next patient gets called in for treatment**

```java
public Patient dequeue() { // no arguments — we always treat whoever is at the front of the line
    if (front == null) { // empty queue check — nobody is waiting
        System.out.println("No patients waiting.");
        return null;
    }

    Patient removedPatient = front.patient; // save the patient at the front before removing them
    front = front.next; // move front forward to the next patient in line

    if (front == null) { // if that removal emptied the queue
        rear = null; // reset rear too
    }

    return removedPatient; // hand back the patient who is now going in for treatment
}
```

**`display` — show everyone currently waiting**

```java
public void display() { // no arguments — walks the queue and prints every waiting patient
    if (front == null) { // handle empty queue first
        System.out.println("No patients currently waiting.");
        return;
    }

    PatientQueueNode current = front; // start at the front of the line
    System.out.println("Patients waiting for treatment:");
    while (current != null) { // keep going until we pass the last patient
        Patient p = current.patient;
        System.out.println("ID: " + p.patientId + " | Name: " + p.name + " | Condition: " + p.condition);
        current = current.next; // move to the next patient in line
    }
}
```

**`isEmpty` — helper, same as before**

```java
public boolean isEmpty() { // no arguments — checks whether any patient is currently waiting
    return front == null; // true if there's no front node, meaning the queue is empty
}
```

## Assessment Main Demonstration

Now let's actually run it with real patient data.

**File: `Main.java`**

```java
public class Main {
    public static void main(String[] args) {
        PatientQueue emergencyQueue = new PatientQueue(); // create an empty emergency queue

        // create a few patients arriving at the emergency unit
        Patient p1 = new Patient(101, "Nimal Perera", 45, "0771234567", "Chest Pain");
        Patient p2 = new Patient(102, "Kamala Silva", 30, "0777654321", "Fracture");
        Patient p3 = new Patient(103, "Ruwan Fernando", 60, "0712345678", "Breathing Difficulty");

        emergencyQueue.enqueue(p1); // Nimal joins the queue first
        emergencyQueue.enqueue(p2); // Kamala joins next
        emergencyQueue.enqueue(p3); // Ruwan joins last

        emergencyQueue.display(); // show everyone currently waiting

        Patient nextPatient = emergencyQueue.dequeue(); // call in the next patient for treatment
        System.out.println("Now treating: " + nextPatient.name);

        emergencyQueue.display(); // show who's left waiting
    }
}
```

Nimal arrived first, so Nimal gets treated first — even though Kamala and Ruwan are also waiting. That's FIFO in action, with real data this time.

## Committing This Work

The full Queue topic is done now — both the generic version and the real Patient version. This is exactly the point where we commit, not before. Half-finished logic doesn't get committed as if it's done.

```
git add .
git commit -m "Implemented emergency queue"
```

One clean commit, right after finishing this one data structure. That's the pattern we'll repeat for every topic — small, meaningful commits tied to real progress, never one giant commit dumped at the end.

## Class Closing

Quick recap: we built a generic queue first with plain integers — `enqueue`, `dequeue`, `display`, `isEmpty` — to lock in the FIFO logic. Then we rebuilt the exact same four methods around a real `Patient` object, and nothing about the logic changed, only the data type did.

Takeaway line to remember: **the front is where people leave, the rear is where people arrive — never the other way around.**

That's the full 20 marks for Emergency Patient Queue covered. Ready to move on to the next part, or do you want to go over anything in this again?
