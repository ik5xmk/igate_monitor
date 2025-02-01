import socket
import os
import time

# Configurazione del TNC
TNC_IP = "1.2.3.4"             # IP del TNC
TNC_PORT = 8001                # Porta del TNC

# decodifica  un frame KISS
def decode_kiss_frame(frame):
    if frame[0] == 0x00:
        frame = frame[1:]
    return frame.replace(b'\xDB\xDC', b'\xC0').replace(b'\xDB\xDD', b'\xDB')

# decodifica un frame AX.25
def decode_ax25_frame(frame):
    try:
        destination = frame[0:7]
        source = frame[7:14]

        def decode_address(addr):
            callsign = "".join(chr((b >> 1) & 0x7F) for b in addr[:6]).strip()
            ssid = (addr[6] >> 1) & 0x0F
            return f"{callsign}-{ssid}" if ssid else callsign

        destination_call = decode_address(destination)
        source_call = decode_address(source)

        path = []
        path_start = 14
        while path_start + 7 <= len(frame):
            addr = frame[path_start:path_start + 7]
            path.append(decode_address(addr))
            if addr[6] & 0x01:
                break
            path_start += 7

        payload_start = path_start + 7
        payload = frame[payload_start:]
        return {
            "destination": destination_call,
            "source": source_call,
            "path": path,
            "payload": payload,
        }
    except:
        return None

# analizza il payload APRS
def parse_aprs_payload(payload):
    try:
        # da byte a string
        return payload.decode("utf-8", errors="replace")
    except:
        return None

# riceve i pacchetti APRS dal TNC
def receive_aprs_packets(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tnc_socket:
            tnc_socket.connect((ip, port))
            print(f"Connesso al TNC {ip}:{port}")
            buffer = b""

            while True:
                data = tnc_socket.recv(1024)
                if not data:
                    break

                buffer += data

                while b'\xC0' in buffer:
                    start = buffer.find(b'\xC0') + 1
                    end = buffer.find(b'\xC0', start)
                    if end == -1:
                        break

                    frame = buffer[start:end]
                    buffer = buffer[end + 1:]

                    decoded_frame = decode_kiss_frame(frame)
                    ax25_frame = decode_ax25_frame(decoded_frame)

                    if ax25_frame:
                        aprs_payload = parse_aprs_payload(ax25_frame["payload"])
                        print( "\n" + "="*20)
                        print(f"Sorgente: {ax25_frame['source']}")
                        print(f"Destinazione: {ax25_frame['destination']}")
                        print(f"Percorso: {', '.join(ax25_frame['path'])}")
                        print(f"Payload: {aprs_payload}")
                        print("="*20)

                        # prepara testo da inviare al Bot
                        path = ", ".join(ax25_frame['path'])
                        frame_info = (f"Sorgente: {ax25_frame['source']}\n"
                                      f"Destinazione: {ax25_frame['destination']}\n"
                                      f"Percorso: {path}\n"
                                      f"Payload: {aprs_payload}")
                        # richiama il Bot
                        os.system(f"sh igate_monitor.sh '{frame_info}'")
                        time.sleep(1)

    except Exception as e:
        print(f"Errore di connessione: {e}")

if __name__ == "__main__":
    receive_aprs_packets(TNC_IP, TNC_PORT)
