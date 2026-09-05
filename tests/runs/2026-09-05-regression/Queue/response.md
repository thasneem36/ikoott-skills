Alright, let's get into the **Emergency Patient Queue** — this is worth 20 marks in your assessment, same weight as the BST. This one's actually simpler once it clicks. Let's build it up.

---

## Part 1 — The Basic Concept

A Queue is a line. Literally think of people standing in a line at a hospital reception. Whoever came first, gets served first. Nobody can jump the line, and nobody leaves from the middle.

There are two ends you care about:
- **Rear** — where new people join the line
- **Front** — where the next person gets served and leaves

Here's the picture:

```
                 ADD HERE (enqueue)
                        |
                        v
   FRONT  [ 10 ] -> [ 20 ] -> [ 30 ] -> [ 40 ]  REAR
     |
     v
 REMOVE HERE (dequeue)
```

So 10 came in first — 10 leaves first. That's it. That's the whole idea.

**One memorable rule:**
> "First one in line, first one out — a queue never lets anyone skip the line."

Everything we code today is just enforcing that one rule.

---

## Part 2 — Generic Code (plain numbers first, no Patient yet)

We're going to build this with two small classes — a `Node` (one link in the line) and a `Queue` (the line itself, tracking front and rear). We'll do this one piece at a time. Don't jump ahead — each block only makes sense after the one before it.

### Step 1 — The Node skeleton

File: Node.java
```java
public class Node {
    int data;      // the value being carried by this node (whoever is "in line" here)
    Node next;     // reference to the next node behind this one in the queue

    public Node(int data) {
        this.data = data;   // store the value this node is holding
        this.next = null;   // this node has nobody behind it yet
    }
}
```

That's just a box holding a value and pointing to the next box. Nothing fancy. Makes sense? Let's move on.

### Step 2 — The Queue skeleton

File: Queue.java
```java
public class Queue {
    Node front;   // points to the node that will leave next (the person at the front of the line)
    Node rear;    // points to the last node added (the last person in the line)

    public Queue() {
        this.front = null;   // queue starts with nobody in it
        this.rear = null;    // no rear node yet either
    }
}
```

Two pointers — `front` and `rear`. That's the entire state of a queue. Everything else is just moving these two around. Got it? Next.

### Step 3 — isEmpty()

We need this one early because both `dequeue()` and `display()` are going to check it before doing anything.

File: Queue.java
```java
public boolean isEmpty() {
    return front == null;   // if there's no front node, there's nobody in the queue at all
}
```

Simple check — if `front` is `null`, the line is empty. We'll lean on this a lot. Moving on.

### Step 4 — enqueue()

This is how someone joins the back of the line.

File: Queue.java
```java
public void enqueue(int value) {   // value: the new data we want to add to the back of the queue
    Node newNode = new Node(value);   // wrap the value in a new node

    if (isEmpty()) {              // if the queue currently has nobody
        front = newNode;          // this new node is now both the front...
        rear = newNode;           // ...and the rear, since it's the only one
    } else {
        rear.next = newNode;      // link the current last node to this new node
        rear = newNode;           // move the rear pointer forward to the new node
    }
}
```

Notice the special case — if the queue was empty, the new node becomes BOTH front and rear, because it's the only person there. Make sense? Let's do the reverse operation next.

### Step 5 — dequeue()

This is how the front person leaves the line to get treated.

File: Queue.java
```java
public int dequeue() {
    if (isEmpty()) {                                 // nothing to remove
        System.out.println("Queue is empty. Nothing to dequeue.");
        return -1;                                   // sentinel value meaning "no data available"
    }

    int removedValue = front.data;   // grab the value sitting at the front before we lose the reference
    front = front.next;              // move front pointer to the next node in line

    if (front == null) {             // if that removed node was the only one
        rear = null;                 // the queue is now fully empty, so reset rear too
    }

    return removedValue;             // hand back the value that just left the queue
}
```

Two things to notice: we handle the empty case FIRST, before touching any pointers — that's the "appropriate handling of an empty queue" your assessment asks for. And when we remove the last remaining node, we reset `rear` too, otherwise it would be left pointing at a node that no longer exists in the queue. Clear? Good, one more method.

### Step 6 — display()

File: Queue.java
```java
public void display() {
    if (isEmpty()) {                                  // nothing to show
        System.out.println("Queue is empty.");
        return;
    }

    Node current = front;          // start walking from the front of the line
    System.out.print("Front -> ");
    while (current != null) {      // keep going until we fall off the end
        System.out.print(current.data + " -> ");
        current = current.next;    // step to the next node
    }
    System.out.println("Rear");
}
```

We just walk from front to rear, printing as we go. That's the whole generic Queue done — four methods, two skeletons, six steps total. Now let's actually run it.

### Generic Main.java demonstration

Without this, the class exists but nothing actually runs — we need a `main` to create objects and call the methods so we can SEE the queue working.

File: Main.java
```java
public class Main {
    public static void main(String[] args) {
        Queue queue = new Queue();     // create an empty queue

        queue.enqueue(10);             // 10 joins the line
        queue.enqueue(20);             // 20 joins behind 10
        queue.enqueue(30);             // 30 joins behind 20

        queue.display();               // should print: Front -> 10 -> 20 -> 30 -> Rear

        int removed = queue.dequeue(); // removes 10, since it was first in
        System.out.println("Dequeued: " + removed);

        queue.display();               // should now print: Front -> 20 -> 30 -> Rear

        queue.dequeue();
        queue.dequeue();
        queue.dequeue();               // queue is now empty — should print the empty message
    }
}
```

Run that in your head — 10 comes out first, then 20, then 30, then the empty message fires on the fourth dequeue. That's FIFO in action.

---

## Part 3 — Applying It to the Assessment

You understand the logic now — a queue is just two pointers, `front` and `rear`, moving in a disciplined way. Nothing about that logic changes. The only thing that changes is WHAT we're storing — instead of a plain `int`, we're now storing a `Patient` object (the same `Patient` class you already built for the BST). The rules — enqueue at the rear, dequeue from the front, empty check first — stay exactly identical.

Let's rebuild it, one method at a time again, using real patients this time.

### Step 1 — The PatientNode skeleton

File: PatientNode.java
```java
public class PatientNode {
    Patient patient;      // the actual patient object being held in this node
    PatientNode next;     // reference to the next patient node behind this one in the queue

    public PatientNode(Patient patient) {
        this.patient = patient;   // store the incoming patient object
        this.next = null;         // this node has nobody behind it yet
    }
}
```

Exact same shape as `Node.java` — just holding a `Patient` instead of an `int`. Good? Next.

### Step 2 — The EmergencyQueue skeleton

File: EmergencyQueue.java
```java
public class EmergencyQueue {
    PatientNode front;   // points to the patient who will be treated next
    PatientNode rear;    // points to the most recently arrived patient in the queue

    public EmergencyQueue() {
        this.front = null;   // queue starts with no patients waiting
        this.rear = null;    // no rear node yet either
    }
}
```

Same two pointers, same idea, just renamed to fit the hospital context. Clear? Moving on.

### Step 3 — isEmpty()

File: EmergencyQueue.java
```java
public boolean isEmpty() {
    return front == null;   // true only when there is no patient at the front, meaning nobody is waiting
}
```

### Step 4 — enqueue()

File: EmergencyQueue.java
```java
public void enqueue(Patient patient) {   // patient: the new patient arriving at the emergency unit
    PatientNode newNode = new PatientNode(patient);   // wrap the patient in a new queue node

    if (isEmpty()) {              // if nobody is currently waiting
        front = newNode;          // this patient becomes both the front...
        rear = newNode;           // ...and the rear
    } else {
        rear.next = newNode;      // link the current last patient to this new one
        rear = newNode;           // move the rear pointer to the new patient
    }

    System.out.println("Patient " + patient.name + " added to the emergency queue.");
}
```

Identical structure to the generic `enqueue()` — only difference is we're wrapping a `Patient` instead of an `int`, and printing a nicer message. Good? Next.

### Step 5 — dequeue()

File: EmergencyQueue.java
```java
public Patient dequeue() {
    if (isEmpty()) {                                          // no patient currently waiting
        System.out.println("No patients waiting. Queue is empty.");
        return null;                                          // nothing to hand back
    }

    Patient treatedPatient = front.patient;   // grab the patient sitting at the front
    front = front.next;                       // move front pointer to the next waiting patient

    if (front == null) {                      // that was the last patient in the queue
        rear = null;                          // reset rear since the queue is now empty
    }

    return treatedPatient;                    // hand back the patient who is now going in for treatment
}
```

Same empty-check-first pattern, same rear-reset-on-last-node pattern. Nothing new logically — just real data now. Clear? Last method.

### Step 6 — display()

File: EmergencyQueue.java
```java
public void display() {
    if (isEmpty()) {
        System.out.println("No patients currently waiting.");
        return;
    }

    PatientNode current = front;      // start walking from the front of the line
    System.out.println("Patients currently waiting:");
    while (current != null) {
        System.out.println("- ID: " + current.patient.patientId
                + ", Name: " + current.patient.name
                + ", Condition: " + current.patient.medicalCondition);
        current = current.next;       // step to the next waiting patient
    }
}
```

Same walk-and-print pattern as before, just printing patient details instead of a plain number.

### Assessment Main demonstration

File: Main.java
```java
public class Main {
    public static void main(String[] args) {
        EmergencyQueue emergencyQueue = new EmergencyQueue();   // create the hospital's emergency queue

        Patient p1 = new Patient(101, "Nimal Perera", 45, "0771234567", "Chest Pain");
        Patient p2 = new Patient(102, "Kamala Silva", 30, "0719876543", "Fracture");
        Patient p3 = new Patient(103, "Ruwan Fernando", 60, "0754561230", "Breathing Difficulty");

        emergencyQueue.enqueue(p1);
        emergencyQueue.enqueue(p2);
        emergencyQueue.enqueue(p3);

        emergencyQueue.display();          // shows all 3 patients currently waiting

        Patient nextForTreatment = emergencyQueue.dequeue();   // p1 leaves first — FIFO
        System.out.println("Now treating: " + nextForTreatment.name);

        emergencyQueue.display();          // shows only p2 and p3 left waiting

        emergencyQueue.dequeue();
        emergencyQueue.dequeue();
        emergencyQueue.dequeue();          // queue is now empty — should print the empty message
    }
}
```

Run through that in your head: Nimal came in first, so Nimal gets treated first, even though Kamala and Ruwan are also waiting. That's the FIFO rule doing exactly what the assessment expects — and the empty-queue message fires cleanly on that last extra dequeue instead of crashing.

---

## Class Closing

Quick recap: a Queue is just two pointers — `front` and `rear` — and four operations built around one rule: first in, first out. We built it generically with plain integers first (`Node` + `Queue`), then rebuilt the exact same logic with real `Patient` objects (`PatientNode` + `EmergencyQueue`), and the only thing that actually changed was the data type being carried.

**Takeaway line:** if you can enqueue and dequeue with integers, you can enqueue and dequeue with anything — the queue doesn't care what it's carrying, only about the order.

Now that the whole Queue topic — generic and assessment both — is fully done, let's lock this in with a commit.

File: Git commit for this topic
```
git add .
git commit -m "Implemented emergency queue"
```

That's one clean, meaningful commit for this entire component — matches exactly what your assessment's example commit list expects.

Are you good with the Queue, or want me to go over any part again before we move on to the Treatment Stack next?
