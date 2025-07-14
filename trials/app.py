import serial
import time

# First, let's find available COM ports
def find_available_ports():
    import serial.tools.list_ports
    ports = list(serial.tools.list_ports.comports())
    return [port.device for port in ports]

# Try to find and connect to the correct port
def connect_to_sensor():
    available_ports = find_available_ports()
    
    if not available_ports:
        print("No COM ports found! Make sure your USB-TTL converter is connected.")
        return None
    
    print("Available COM ports:", available_ports)
    
    # Try each port to find the one with R307
    for port in available_ports:
        try:
            print(f"Trying to connect to {port}...")
            ser = serial.Serial(port, 57600, timeout=1)
            time.sleep(2)  # Give time for connection to establish
            
            # Send a simple command to test if R307 responds
            test_cmd = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'  # GenImg command
            ser.write(test_cmd)
            response = ser.read(12)
            
            if len(response) >= 9 and response[0:2] == b'\xEF\x01':
                print(f"R307 sensor found on {port}!")
                return ser
            else:
                print(f"No R307 response on {port}")
                ser.close()
                
        except Exception as e:
            print(f"Could not connect to {port}: {e}")
    
    print("R307 sensor not found on any port!")
    return None

# Initialize connection
ser = None

def send_command(command_packet):
    ser.write(command_packet)
    response = ser.read(12)  # R307 typically responds with 12 bytes
    return response

def enroll_fingerprint(finger_id):
    print(f"Enrolling finger ID: {finger_id}")
    
    try:
        # Step 1: Send command to capture image (GenImg)
        print("Place finger on sensor...")
        response = send_command(b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05')
        print(f"GenImg response: {response.hex()}")
        
        # Step 2: Send command to convert image to template (Img2Tz 1)
        print("Converting image to template...")
        response = send_command(b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x01\x00\x08')
        print(f"Img2Tz response: {response.hex()}")
        
        # Step 3: Send command to store template in the specified ID (Store)
        print(f"Storing template with ID {finger_id}...")
        checksum = (0x06 + 0x01 + finger_id + 0x00) & 0xFF
        store_cmd = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x06\x06\x01' + bytes([finger_id]) + b'\x00' + bytes([checksum])
        response = send_command(store_cmd)
        print(f"Store response: {response.hex()}")
        
        print(f"Fingerprint {finger_id} enrollment completed!")
        
    except Exception as e:
        print(f"Error during enrollment: {e}")
        
def verify_fingerprint():
    try:
        # Step 1: Capture image
        print("Place finger for verification...")
        response = send_command(b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05')
        print(f"GenImg response: {response.hex()}")
        
        # Step 2: Convert to template
        response = send_command(b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x04\x02\x01\x00\x08')
        print(f"Img2Tz response: {response.hex()}")
        
        # Step 3: Search for match
        response = send_command(b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x08\x04\x01\x00\x00\x00\x64\x00\x72')
        print(f"Search response: {response.hex()}")
        
        if len(response) >= 12 and response[9] == 0x00:
            finger_id = (response[10] << 8) | response[11]
            print(f"Match found! Finger ID: {finger_id}")
            return finger_id
        else:
            print("No match found")
            return None
            
    except Exception as e:
        print(f"Error during verification: {e}")
        return None

# Example usage
if __name__ == "__main__":
    try:
        print("R307 Fingerprint Sensor Test")
        print("Connecting to sensor...")
        
        # Connect to the sensor
        ser = connect_to_sensor()
        
        if ser is None:
            print("Failed to connect to R307 sensor!")
            print("\nTroubleshooting steps:")
            print("1. Check if USB-TTL converter is plugged in")
            print("2. Verify wiring connections:")
            print("   - R307 Pin 1 (VCC) → USB-TTL +5V")
            print("   - R307 Pin 2 (GND) → USB-TTL GND")
            print("   - R307 Pin 3 (TX)  → USB-TTL RXD")
            print("   - R307 Pin 4 (RX)  → USB-TTL TXD")
            print("3. Install drivers for your USB-TTL converter")
            exit(1)
        
        print("\n1. Enroll fingerprint")
        print("2. Verify fingerprint")
        
        choice = input("Enter choice (1 or 2): ")
        
        if choice == "1":
            finger_id = int(input("Enter finger ID (1-127): "))
            enroll_fingerprint(finger_id)
        elif choice == "2":
            verify_fingerprint()
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\nProgram interrupted")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if ser:
            ser.close()
            print("Serial connection closed")
