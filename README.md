# Keylogger: A Comprehensive Activity Monitoring System

Keylogger is a tool designed to track and log user activity on a system. It captures keystrokes, takes screenshots, records audio, tracks clipboard activity, and securely transmits the collected data to a remote server using Twilio. The project is built using Python and involves encryption for data security.

## Features

- **Keystroke Logging**: Captures all the keystrokes typed by the user.
- **Screenshot Capture**: Takes periodic screenshots at defined intervals.
- **Audio Recording**: Records audio through the system’s microphone.
- **Clipboard Monitoring**: Monitors changes in the clipboard content.
- **System Information**: Collects system information such as IP address.
- **Data Encryption**: Encrypts captured data using asymmetric key encryption.
- **Remote Data Transmission**: Sends encrypted data to a remote server using Twilio.
- **Log Deletion**: Automatically deletes local logs after they are sent securely to the remote server.

## Technologies Used

- **Python** - Primary language used for the project.
- **Socket** - For network communication.
- **Pynput** - For capturing keyboard and mouse events.
- **Twilio** - For sending data to a remote server.
- **SoundDevice** - For recording audio.
- **Scapy** - For system and network information.
- **Cryptography** - For encrypting and decrypting data.

## Installation Guide

### Prerequisites

- Python 3.x
- Pip (Python Package Installer)
- Twilio account (for sending data)

### Clone the Repository

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/Keylogger.git
   cd Keylogger
### Install Dependencies

Install the required Python libraries by running the following commands:

1. Update the package list and install `pip` (if not installed):

   ```bash
   sudo apt update
   sudo apt install python3-pip


## Twilio Configuration

1. **Set up your Twilio account**:
   - Visit [Twilio's website](https://www.twilio.com/) and create an account if you don't have one.

2. **Get your Twilio credentials**:
   - Once logged in to your Twilio account, go to the [Twilio Console](https://www.twilio.com/console).
   - Copy your **Account SID** and **Auth Token** from the console.

3. **Configure the API settings**:
   - Open the `TwilioConfig.py` file in your project.
   - Replace the placeholders with your actual **Account SID**, **Auth Token**, and **Phone Numbers**.
   - Example configuration:

   ```python
   account_sid = 'your_account_sid'
   auth_token = 'your_auth_token'
   from_number = 'your_twilio_phone_number'
   to_number = 'recipient_phone_number'
## Usage

### Running the Keylogger

1. **Set up Encryption and Twilio Configuration**: 
   - Ensure that you have configured the encryption key and the Twilio credentials as outlined in the **Twilio Configuration** section above.

2. **Start the Keylogger**: 
   - Once the setup is complete, you can start the keylogger by running the following command:

   ```bash
   python Keylogger.py
   ```

## Contact
For questions or support, please contact:

- **Y Manish Kumar**: [ymanishk602@gmail.com](mailto:ymanishk602@gmail.com)
  
## Contributing
Feel free to submit issues and pull requests. Contributions are welcome!


## License
This project is licensed under the MIT License.

