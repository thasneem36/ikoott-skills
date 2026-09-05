Alright. Queue time. This is worth 20 marks — the Emergency Patient Queue part of your assignment. Let's build it properly, step by step.

## The Basic Concept

Before any code, let's understand what a Queue actually is.

Think of patients arriving at an emergency unit. Whoever comes first, gets treated first. Nobody jumps the line. New patients join at the back. The doctor picks the next patient from the front.

That's it. That's a Queue.

Here's the picture:

```
   ENQUEUE (join here) →                    → DEQUEUE (leave here)

        [ 10 ] → [ 20 ] → [ 30 ] → null
          ^                  ^
        FRONT              REAR
     (next to leave)    (just joined)
```

New values get added at the REAR. Values get removed from the FRONT. Nothing in the middle gets touched.

## One Memorable Rule

> **First one in, first one out — no cutting the line.**

That's FIFO. First-In, First-Out. Whatever gets added first, leaves first. Keep that sentence in your head — it's the whole logic of this data structure.

Now let's code it. We'll start with a plain generic version first — just numbers, no patients yet. Once that logic is solid in your head, we'll swap it for real Patient objects. Same logic, different data.

## Generic Code — Step by Step

First, a Queue needs some kind of "box" to hold each value and point to the next one. That's our Node.

**File: Node.java**
```java
public class Node {
    int data; // the value stored in this node
    Node next; // reference to the next node in the queue, null if this is the last one

    public Node(int data) { // data: the value we want to store when creating a new node
        this.data = data;
        this.next = null;
    }
}
```

This is just a box holding one value, and a pointer to the next box. Nothing fancy.

Now let's give it a `toString()`. This is a separate step — it's not part of the constructor, it's its own override method. We need it so that when we print a node later, it shows something readable instead of a memory address.

**File: Node.java**
```java
// add this inside the Node class, below the constructor

@Override
public String toString() {
    return "" + data; // when we print this node, just show the value it holds
}
```

Good. That's the Node done. Now let's build the actual Queue class — the thing that manages front and rear.

**File: Queue.java**
```java
public class Queue {
    Node front; // points to the first (oldest) node in the queue - this one leaves next
    Node rear; // points to the last (newest) node in the queue - new nodes join here

    public Queue() { // no arguments needed - a brand new queue always starts empty
        this.front = null;
        this.rear = null;
    }
}
```

Empty queue means front and rear both point to nothing. Makes sense — nobody's waiting yet.

Before we write enqueue or dequeue, we need a small helper: `isEmpty()`. Both dequeue and display will need to check this, so we teach it now, on its own, before either of them.

**File: Queue.java**
```java
// add this inside the Queue class

public boolean isEmpty() { // no arguments needed - it just checks the queue's own state
    return front == null; // if front points to nothing, the queue has nobody waiting
}
```

Now — enqueue. Adding a new value to the rear.

**File: Queue.java**
```java
// add this inside the Queue class

public void enqueue(int value) { // value: the data we want to add to the back of the queue
    Node newNode = new Node(value); // wrap the value inside a new node

    if (isEmpty()) {
        front = newNode; // queue was empty, so this node is both front and rear
        rear = newNode;
    } else {
        rear.next = newNode; // link the current last node to this new one
        rear = newNode; // move rear forward so it points to the new last node
    }
}
```

Two cases only. Either the queue was empty and this new node becomes everything, or the queue already had people in it, so we just attach the new node after the current rear and move rear forward.

Next — dequeue. Removing from the front. This is where we use `isEmpty()` — that's why we taught it first.

**File: Queue.java**
```java
// add this inside the Queue class

public int dequeue() { // no arguments needed - dequeue always removes from the front
    if (isEmpty()) {
        System.out.println("Queue is empty. Nothing to dequeue.");
        return -1; // -1 signals "nothing was removed" because the queue had nobody waiting
    }

    int removedValue = front.data; // save the value before we lose this node
    front = front.next; // move front forward, dropping the old front node

    if (front == null) {
        rear = null; // queue is now completely empty, so reset rear too
    }

    return removedValue;
}
```

Notice the empty-queue check right at the top. That's the "appropriate handling of an empty queue" your assignment asks for. Never skip that check — trying to dequeue from an empty queue without it will crash your program.

Last method for this class — display. Also uses `isEmpty()`.

**File: Queue.java**
```java
// add this inside the Queue class

public void display() { // no arguments needed - just prints the current state of the queue
    if (isEmpty()) {
        System.out.println("Queue is empty. No one is waiting.");
        return;
    }

    Node current = front; // start walking from the front
    System.out.print("Queue (front to rear): ");

    while (current != null) {
        System.out.print(current + " "); // this calls Node's toString() automatically
        current = current.next; // move to the next node
    }

    System.out.println();
}
```

That's the whole generic Queue done: `isEmpty()`, `enqueue()`, `dequeue()`, `display()`. But right now, this class just sits there — nothing actually runs it. We need a `Main` to prove it works.

**File: Main.java**
```java
public class Main {
    public static void main(String[] args) {
        Queue queue = new Queue(); // create a brand new, empty generic queue

        queue.enqueue(10);
        queue.enqueue(20);
        queue.enqueue(30);

        queue.display(); // Queue (front to rear): 10 20 30

        int removed = queue.dequeue(); // removes 10, since it was the first one in
        System.out.println("Dequeued: " + removed);

        queue.display(); // Queue (front to rear): 20 30
    }
}
```

Run this in your head: 10 goes in first, then 20, then 30. Dequeue removes 10 — the oldest one — not 30. That's FIFO working correctly. Without this Main, the Queue class just exists on disk doing nothing. This is what actually proves it runs.

Make sense so far? The logic here — front, rear, isEmpty, enqueue, dequeue — is the entire Queue concept. Nothing changes conceptually from here. What changes next is only the data type.

## Bridge to the Assessment

Good — the logic is solid now. We just moved a plain `int` through a queue. Your assignment doesn't want integers though, it wants real `Patient` objects moving through the Emergency Queue.

Here's what stays exactly the same: front, rear, isEmpty, enqueue logic, dequeue logic, FIFO order — all identical. What changes is just the data type sitting inside the node. Instead of `int data`, we'll have `Patient data`. Same rules, real object.

Let's rebuild it, one method at a time again.

## Assessment Code — Step by Step

First, the Patient object itself.

**File: Patient.java**
```java
public class Patient {
    int patientId; // unique ID used to identify this patient
    String name; // patient's full name
    int age; // patient's age in years
    String contactNumber; // patient's phone number
    String medicalCondition; // short description of what the patient is suffering from

    public Patient(int patientId, String name, int age, String contactNumber, String medicalCondition) {
        // patientId: unique ID for this patient
        // name: patient's full name
        // age: patient's age in years
        // contactNumber: patient's phone number for contact
        // medicalCondition: what condition the patient arrived with
        this.patientId = patientId;
        this.name = name;
        this.age = age;
        this.contactNumber = contactNumber;
        this.medicalCondition = medicalCondition;
    }
}
```

Every field commented, every constructor argument commented. Now, its own separate step — `toString()`, so we can print a Patient in a readable way later.

**File: Patient.java**
```java
// add this inside the Patient class, below the constructor

@Override
public String toString() {
    return "[ID: " + patientId + ", Name: " + name + ", Age: " + age
            + ", Contact: " + contactNumber + ", Condition: " + medicalCondition + "]";
}
```

Now the node that will hold a Patient inside the queue. Same idea as generic `Node.java`, just carrying a different data type.

**File: PatientNode.java**
```java
public class PatientNode {
    Patient data; // the Patient object stored in this node
    PatientNode next; // reference to the next node in the queue, null if this is the last one

    public PatientNode(Patient data) { // data: the Patient object we want to store when creating a new node
        this.data = data;
        this.next = null;
    }
}
```

Now the actual Emergency Queue class.

**File: EmergencyQueue.java**
```java
public class EmergencyQueue {
    PatientNode front; // points to the first (oldest) patient node - this patient is treated next
    PatientNode rear; // points to the last (newest) patient node - new patients join here

    public EmergencyQueue() { // no arguments needed - a new emergency queue always starts empty
        this.front = null;
        this.rear = null;
    }
}
```

Helper first, same as before — `isEmpty()`, before dequeue and display need it.

**File: EmergencyQueue.java**
```java
// add this inside the EmergencyQueue class

public boolean isEmpty() { // no arguments needed - it just checks the queue's own state
    return front == null; // if front points to nothing, no patient is currently waiting
}
```

Enqueue — adding a patient to the waiting line.

**File: EmergencyQueue.java**
```java
// add this inside the EmergencyQueue class

public void enqueuePatient(Patient patient) { // patient: the Patient object to add to the waiting queue
    PatientNode newNode = new PatientNode(patient); // wrap the patient inside a new node

    if (isEmpty()) {
        front = newNode; // queue was empty, so this node is both front and rear
        rear = newNode;
    } else {
        rear.next = newNode; // link the current last patient node to this new one
        rear = newNode; // move rear forward so it points to the new last node
    }
}
```

Dequeue — pulling the next patient out for treatment. Empty-check first, exactly like before.

**File: EmergencyQueue.java**
```java
// add this inside the EmergencyQueue class

public Patient dequeuePatient() { // no arguments needed - always removes from the front
    if (isEmpty()) {
        System.out.println("Queue is empty. No patient to treat right now.");
        return null; // null signals "nothing was removed" because no patient was waiting
    }

    Patient removedPatient = front.data; // save the patient before we lose this node
    front = front.next; // move front forward, dropping the old front node

    if (front == null) {
        rear = null; // queue is now completely empty, so reset rear too
    }

    return removedPatient;
}
```

And display — showing everyone currently waiting.

**File: EmergencyQueue.java**
```java
// add this inside the EmergencyQueue class

public void displayQueue() { // no arguments needed - just prints everyone currently waiting
    if (isEmpty()) {
        System.out.println("Queue is empty. No patients waiting.");
        return;
    }

    PatientNode current = front; // start walking from the front
    System.out.println("Patients waiting (front to rear):");

    while (current != null) {
        System.out.println(current.data); // uses Patient's toString() automatically
        current = current.next; // move to the next node
    }
}
```

That covers everything your assignment asks for: enqueue, dequeue, display all waiting patients, and proper empty-queue handling. Now let's actually run it with real patients.

**File: Main.java**
```java
public class Main {
    public static void main(String[] args) {
        EmergencyQueue emergencyQueue = new EmergencyQueue(); // create a new, empty emergency queue

        Patient p1 = new Patient(101, "Kamal Perera", 45, "0771234567", "Chest Pain");
        Patient p2 = new Patient(102, "Nimali Silva", 30, "0719876543", "Fracture");
        Patient p3 = new Patient(103, "Ruwan Fernando", 60, "0765551234", "Breathing Difficulty");

        emergencyQueue.enqueuePatient(p1);
        emergencyQueue.enqueuePatient(p2);
        emergencyQueue.enqueuePatient(p3);

        emergencyQueue.displayQueue();

        Patient treated = emergencyQueue.dequeuePatient(); // removes Kamal Perera, first one in
        System.out.println("Now treating: " + treated);

        emergencyQueue.displayQueue();
    }
}
```

Kamal was enqueued first, so Kamal gets treated first — even though Ruwan arrived with a more serious-sounding condition. That's the whole point of a strict FIFO queue: no priority, no sorting, just arrival order. If you want priority-based treatment, that's a different structure — but this assignment specifically wants a plain FIFO queue here.

## Recap

Two passes, same logic both times:
- Generic pass: `Node`, `Queue` — front, rear, isEmpty, enqueue, dequeue, display, all working on plain integers.
- Assessment pass: `Patient`, `PatientNode`, `EmergencyQueue` — identical logic, just carrying real patient data instead of integers.

**Takeaway line:** a Queue never cares what's inside it — it only cares about the order things came in.

That's the full Emergency Patient Queue done — 20 marks worth of logic built and tested. Before we commit this and move to the next part, are you good with everything here, or want me to go over any piece again — enqueue, dequeue, or the empty-queue handling?

---

Once you're ready, here's the commit for this topic. We only commit now because the whole Queue topic — both passes — is fully done. Not halfway through, not just the generic part.

```
git add .
git commit -m "Implemented emergency queue"
```

One commit, one completed piece of work. That's what "small, frequent, meaningful commits" looks like — not one giant commit with everything dumped in at the end.

Ready to move on to Treatment History next — the Stack — whenever you are.
