import os
import cv2
import numpy as np
import subprocess
import wave

def convert_mp3_to_wav(mp3_file, wav_file="static/generated/output.wav"):
    """ Converts an MP3 file to WAV using FFmpeg. """
    try:
        command = f'ffmpeg -y -i "{mp3_file}" -ar 24000 -ac 1 -c:a pcm_s16le "{wav_file}"'
        subprocess.run(command, shell=True, check=True)

        if not os.path.exists(wav_file):
            raise FileNotFoundError(f"[ERROR] Converted WAV file not found: {wav_file}")

        return wav_file
    except Exception as e:
        raise Exception(f"[ERROR] Converting MP3 to WAV: {e}")

def create_avatar_animation(audio_file, output_video="static/generated/final_output.mp4"):
    """
    Generates an avatar animation and merges it with audio using FFmpeg.
    """
    try:
        if not os.path.exists(audio_file):
            raise FileNotFoundError(f"Audio file not found: {audio_file}")

        # Convert MP3 to WAV if needed
        if audio_file.endswith(".mp3"):
            print("[INFO] Converting MP3 to WAV for FFmpeg...")
            audio_file = convert_mp3_to_wav(audio_file)

        # Get audio duration
        with wave.open(audio_file, "rb") as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)

        print(f"[INFO] Audio duration: {duration:.2f} seconds")

        width, height = 400, 400
        fps = 10
        temp_video = "static/generated/temp_video.mp4"

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

        total_frames = int(fps * duration)

        for i in range(total_frames):
            img = np.zeros((height, width, 3), dtype=np.uint8)
            mouth_open = (i % 4 < 2)

            # Draw avatar face
            cv2.circle(img, (200, 200), 100, (0, 255, 255), -1)
            cv2.circle(img, (170, 180), 15, (0, 0, 0), -1)
            cv2.circle(img, (230, 180), 15, (0, 0, 0), -1)

            # Draw mouth animation
            if mouth_open:
                cv2.rectangle(img, (170, 250), (230, 260), (0, 0, 0), -1)
            else:
                cv2.line(img, (170, 255), (230, 255), (0, 0, 0), 3)

            out.write(img)

        out.release()
        cv2.destroyAllWindows()

        # Merge the animation with the audio
        merge_command = f'ffmpeg -y -i "{temp_video}" -i "{audio_file}" -map 0:v -map 1:a -c:v libx264 -c:a aac -b:a 192k -shortest "{output_video}"'
        subprocess.run(merge_command, shell=True, check=True)

        if not os.path.exists(output_video):
            raise FileNotFoundError(f"[ERROR] Merged video was not created: {output_video}")

        print(f"[SUCCESS] Avatar animation with audio saved: {output_video}")
        return output_video

    except Exception as e:
        raise Exception(f"[ERROR] Generating avatar animation: {e}")
