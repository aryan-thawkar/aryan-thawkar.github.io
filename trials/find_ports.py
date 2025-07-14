import serial.tools.list_ports

def find_available_ports():
    """Find all available COM ports"""
    ports = list(serial.tools.list_ports.comports())
    
    if not ports:
        print("No COM ports found!")
        return None
    
    print("Available COM ports:")
    print("-" * 50)
    
    for i, port in enumerate(ports, 1):
        print(f"{i}. Port: {port.device}")
        print(f"   Description: {port.description}")
        print(f"   Hardware ID: {port.hwid}")
        print("-" * 50)
    
    return [port.device for port in ports]

if __name__ == "__main__":
    available_ports = find_available_ports()
    
    if available_ports:
        print(f"\nFound {len(available_ports)} port(s)")
        print("Look for ports with descriptions containing:")
        print("- 'USB Serial' or 'USB-SERIAL'")
        print("- 'CP210x' (Silicon Labs)")
        print("- 'CH340' or 'CH341' (Chinese USB-Serial)")
        print("- 'FTDI' (Future Technology)")
        print("\nUse one of these ports in your app.py file")
    else:
        print("\nNo ports found. Make sure your USB-TTL converter is:")
        print("1. Plugged into USB port")
        print("2. Drivers are installed")
        print("3. Device is recognized by Windows")
