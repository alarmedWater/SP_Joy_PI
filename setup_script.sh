#!/bin/bash

set -e  # Exit immediately if any command exits with a non-zero status

# Log file
LOG_FILE="setup_log.txt"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to check if a command was successful
check_command_success() {
    if [ $? -ne 0 ]; then
        log_message "Fehler: Der Befehl '$1' war nicht erfolgreich."
        exit 1
    fi
}

# Function to display colored output
color_echo() {
    case "$1" in
        info)
            echo -e "\e[1;34m$2\e[0m"  # Blue
            ;;
        success)
            echo -e "\e[1;32m$2\e[0m"  # Green
            ;;
        error)
            echo -e "\e[1;31m$2\e[0m"  # Red
            ;;
    esac
}

# Function to display user prompts
user_prompt() {
    while true; do
        echo -n "$1 (ja/nein): "
        read choice
        case "$choice" in
            [Jj][Aa])
                return 0
                ;;
            [Nn][Ee][Ii][Nn])
                return 1
                ;;
            *)
                echo "Ungültige Eingabe. Bitte 'ja' oder 'nein' eingeben."
                ;;
        esac
    done
}

# Create or clear the log file
> "$LOG_FILE"

log_message "Starte das Setup-Skript..."

echo "Willkommen beim Raspberry Pi Setup-Skript!"

if user_prompt "Möchten Sie die Paketliste aktualisieren?"; then
    echo "Aktualisiere die Paketliste..."
    sudo apt update >> "$LOG_FILE" 2>&1
    check_command_success "sudo apt update"
    color_echo success "Paketliste aktualisiert."
fi

if user_prompt "Möchten Sie snapd installieren?"; then
    echo "Installiere snapd..."
    sudo apt install snapd -y >> "$LOG_FILE" 2>&1
    check_command_success "sudo apt install snapd"
    color_echo success "snapd installiert."
fi

if user_prompt "Möchten Sie cMake installieren?"; then
    echo "Installiere cMake..."
    sudo apt install cmake -y >> "$LOG_FILE" 2>&1
    check_command_success "sudo apt install cmake"
    color_echo success "cMake installiert."
fi

echo "Prüfe cMake-Version..."
cmake --version
check_command_success "cmake --version"
color_echo success "cMake-Version überprüft."

if user_prompt "Möchten Sie Visual Studio Code installieren?"; then
    echo "Installiere Visual Studio Code..."
    sudo apt install code -y >> "$LOG_FILE" 2>&1
    check_command_success "sudo apt install code"
    color_echo success "Visual Studio Code installiert."
fi

if user_prompt "Möchten Sie erforderliche Pakete für git und Build-Prozess installieren?"; then
    echo "Installiere erforderliche Pakete für git und Build-Prozess..."
    sudo apt install git-core build-essential -y >> "$LOG_FILE" 2>&1
    check_command_success "sudo apt install git-core build-essential"
    color_echo success "Erforderliche Pakete installiert."
fi

if user_prompt "Möchten Sie das WiringPi-Repository klonen und bauen?"; then
    echo "Klonen des WiringPi-Repositorys..."
    git clone https://github.com/WiringPi/WiringPi.git >> "$LOG_FILE" 2>&1
    check_command_success "git clone https://github.com/WiringPi/WiringPi.git"
    color_echo success "WiringPi-Repository geklont."

    echo "Wechsle zum WiringPi-Verzeichnis..."
    cd WiringPi
    check_command_success "cd WiringPi"
    color_echo success "Zum WiringPi-Verzeichnis gewechselt."

    echo "Baue WiringPi..."
    ./build >> "$LOG_FILE" 2>&1
    check_command_success "./build"
    color_echo success "WiringPi erfolgreich gebaut."
fi

if user_prompt "Möchten Sie pybind11 über pip installieren?"; then
    echo "Installiere pybind11 über pip..."
    pip install pybind11 >> "$LOG_FILE" 2>&1
    check_command_success "pip install pybind11"
    color_echo success "pybind11 über pip installiert."
fi

echo "Skript erfolgreich abgeschlossen!"
color_echo success "Skript erfolgreich abgeschlossen!"
log_message "Skript erfolgreich abgeschlossen!"
