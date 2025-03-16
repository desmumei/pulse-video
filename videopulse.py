import cv2
import numpy as np
import time
import csv
from retinaface.pulse_retina import PulseMonitor

pulse_monitor = PulseMonitor()

def process_video(input_path, output_path=None, csv_path="heartrate_log.csv"):
    print(f"Input video path: {input_video}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)

    if output_path:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')  
        out = cv2.VideoWriter(output_path, fourcc, fps, frame_size)

    with open(csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Timestamp (s)", "Heart Rate (BPM)"])

        frame_count = 0 

        while True:
            ret, frame = cap.read()
            if not ret:
                break  

            processed_frame, bpm = pulse_monitor.process_frame(frame)

            timestamp = frame_count / fps
            frame_count += 1

            csv_writer.writerow([timestamp, bpm])

            print(f"Timestamp: {timestamp:.2f}s, Estimated BPM: {bpm:.1f}")

            cv2.imshow('Pulse Monitor', processed_frame)

            if output_path:
                out.write(processed_frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    if output_path:
        out.release()
    cv2.destroyAllWindows()

input_video = r"a.mp4"
output_video = "b.mp4"
csv_file_path = "heartrate_log.csv"
process_video(input_video, output_video, csv_file_path)