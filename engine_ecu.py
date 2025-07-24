import time
import random
import socket # Import the standard socket library

# --- Network Configuration ---
UDP_IP = "127.0.0.1" # Localhost
UDP_PORT = 5005    

def main():
    """
    Simulates an Engine ECU, sending data via a UDP socket.
    """
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("--- Engine ECU Simulation Started ---")
    print(f"Broadcasting data to {UDP_IP}:{UDP_PORT}")
    print("Press Ctrl+C to stop.")

    is_accelerating = True
    engine_rpm = 750

    try:
        while True:
            # --- The engine simulation logic ---
            if is_accelerating:
                engine_rpm += random.randint(20, 60)
                if engine_rpm > 4800: is_accelerating = False
            else:
                engine_rpm -= random.randint(20, 60)
                if engine_rpm < 800: is_accelerating = True

            if engine_rpm < 700: engine_rpm = 700
            if engine_rpm > 5000: engine_rpm = 5000
            speed_from_rpm = (engine_rpm - 700) / 50
            vehicle_speed = int(speed_from_rpm)
            if vehicle_speed < 0: vehicle_speed = 0

            # --- Encode CAN Data ---
            can_data = bytearray(8)
            can_data[0] = (engine_rpm >> 8) & 0xFF
            can_data[1] = engine_rpm & 0xFF
            can_data[2] = vehicle_speed & 0xFF

            # --- Send data over the UDP socket ---
            sock.sendto(can_data, (UDP_IP, UDP_PORT))

            hex_data = ' '.join(f'{b:02X}' for b in can_data)
            print(f"RPM: {engine_rpm:4d} | Speed: {vehicle_speed:3d} km/h | Sent Data: {hex_data}", end='\r')

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n--- Engine ECU Simulation Stopped ---")
        sock.close() # Close the socket when done

if __name__ == '__main__':
    main()