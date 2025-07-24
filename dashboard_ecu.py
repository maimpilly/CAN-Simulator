import socket 

# --- Network Configuration ---
UDP_IP = "127.0.0.1" # Listen on localhost
UDP_PORT = 5005      # Use the same "channel"

def main():
    """
    Simulates a Dashboard ECU, listening for data on a UDP socket.
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind the socket to the address and port
    sock.bind((UDP_IP, UDP_PORT))
    print("--- Dashboard ECU Listener Started ---")
    print(f"Listening for data on {UDP_IP}:{UDP_PORT}...")

    try:
        while True:
            # Wait to receive data. This will block until a message arrives.
            # The '8' means it is expected to receive 8 bytes of data.
            data, addr = sock.recvfrom(8)
            
            # --- Decode the received data payload ---

            # Reconstruct the 16-bit EngineRPM from the first two bytes
            # (Byte 0 is shifted left by 8 bits) and then combined with Byte 1
            engine_rpm = (data[0] << 8) | data[1]

            # The VehicleSpeed is simply the value of the third byte
            vehicle_speed = data[2]

            # --- Display the decoded data ---
            print(f"RPM: {engine_rpm:4d} | Speed: {vehicle_speed:3d} km/h", end='\r')

    except KeyboardInterrupt:
        print("\n--- Dashboard ECU Listener Stopped ---")
        sock.close()

if __name__ == '__main__':
    main()