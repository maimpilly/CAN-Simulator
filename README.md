# Python CAN Bus Communication Simulator

![Language](https://img.shields.io/badge/Language-Python-blue.svg)
![Protocol](https://img.shields.io/badge/Protocol-CAN%20(Simulated)-orange.svg)
![Version](https://img.shields.io/badge/Version-1.0-brightgreen.svg)

## Project Goal

The goal of this project is to simulate the complete communication lifecycle on a vehicle's CAN (Controller Area Network) bus. It demonstrates the core principles of how different Electronic Control Units (ECUs) exchange information in a real car.

This project focuses on the software-level challenges of the CAN protocol: designing message formats, encoding data into byte payloads, broadcasting that data over a network, and decoding it on the receiving end.

## Simulating the Bus: Why UDP?

The CAN bus is fundamentally a broadcast network. To reliably simulate this broadcast behavior between two separate running scripts (processes), this project uses **UDP (User Datagram Protocol) sockets** as the transport layer.

This is a common technique in virtual automotive testing, analogous to **"CAN over Ethernet"**, where CAN frames are sent over an IP network. The core of the project remains the **CAN data protocol**, which involves the strict formatting, encoding, and decoding of the 8-byte data payload. At the same time, UDP provides a robust and universally compatible "virtual wire" between the ECUs.

## System Design

This simulation consists of two primary ECUs communicating over the network:

1.  **Engine ECU (`engine_ecu.py`):**
    * **Role:** Acts as the primary data producer.
    * **Function:** Simulates a running engine with fluctuating RPM and vehicle speed. It encodes these values into a defined CAN message format and broadcasts it onto the network every 100 milliseconds.

2.  **Dashboard ECU (`dashboard_ecu.py`):**
    * **Role:** Acts as the primary data consumer.
    * **Function:** Listens for messages on the network. When it receives a message from the Engine ECU, it decodes the raw byte payload back into human-readable RPM and speed values and displays them.

## CAN Message Design (Virtual DBC)

A single CAN message, `EngineStatus`, is defined for this simulation with a unique Message ID.

* **Message Name:** `EngineStatus`
* **Message ID:** `0x101` (Not used in the UDP version, but part of the design)

The 8-byte data payload is structured as follows:
```
| Signal Name    | Start Bit | Length (bits) | Occupied Bytes | Description                          |
| :------------- | :-------: | :-----------: | :------------: | :------------------------------------|   
| `EngineRPM`    | 0         | 16            | 0-1            | The engine's revolutions per minute. |
| `VehicleSpeed` | 16        | 8             | 2              | The vehicle's speed in km/h.         |
| *Unused*       | 24        | 40            | 3-7            | Reserved for future use.             |
```

## How to Run the Simulation

This simulation requires two separate terminals running concurrently.

#### Dependencies
* Python 3

#### Execution Steps
1.  Clone the repository.
2.  Open your **first terminal**, navigate to the project directory, and start the Engine ECU:
    ```bash
    python engine_ecu.py
    ```
3.  Open a **second terminal**, navigate to the same directory, and start the Dashboard ECU:
    ```bash
    python dashboard_ecu.py
    ```

### Build & Execution Steps

This project also uses CMake to manage the build process.

1.  Clone the repository.
2.  Open a terminal in the project's root directory.
3.  **Configure the project** by creating a build directory:
    ```bash
    cmake -B build
    ```
4.  **Compile the project** using the generated build files:
    ```bash
    cmake --build build
    ```
5.  **Run the executable**, which is now located inside the `build` directory:
    ```bash
    ./build/spi_test

#### Expected Output

* **Terminal 1 (Engine):** You will see a live-updating display of the engine's state and the raw hexadecimal data being sent.
    ```
    RPM: 2777 | Speed:  41 km/h | Sent Data: 0A D9 29 00 00 00 00 00
    ```
* **Terminal 2 (Dashboard):** You will see a live-updating display of the decoded data received from the engine.
    ```
    RPM: 2777 | Speed:  41 km/h
    ```

