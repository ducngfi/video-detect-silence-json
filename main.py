import moviepy.editor as mp
from pydub import AudioSegment, silence
import json
import os

def extract_audio_from_video(video_path, audio_path):
    video = mp.VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def detect_silence(audio_path, silence_thresh=-50, min_silence_len=300):
    audio = AudioSegment.from_file(audio_path)
    silence_intervals = silence.detect_silence(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    non_silence_intervals = silence.detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    return silence_intervals, non_silence_intervals

def intervals_to_dict(intervals):
    return [{'start': interval[0] / 1000, 'end': interval[1] / 1000, 'duration': (interval[1] - interval[0]) / 1000} for interval in intervals]

def save_intervals_to_json(silence_intervals, non_silence_intervals, silence_output_json, non_silence_output_json):
    silence_data = intervals_to_dict(silence_intervals)
    non_silence_data = intervals_to_dict(non_silence_intervals)
    
    with open(silence_output_json, 'w') as f:
        json.dump(silence_data, f, indent=4)
    
    with open(non_silence_output_json, 'w') as f:
        json.dump(non_silence_data, f, indent=4)

def main(video_path):
    # Get the directory of the video file
    video_dir = os.path.dirname(video_path)
    
    # Construct paths for the output JSON files in the same directory
    silence_output_json = os.path.join(video_dir, "detect_silence.json")
    non_silence_output_json = os.path.join(video_dir, "detect_non_silence.json")
    
    audio_path = os.path.join(video_dir, "temp_audio.wav")
    extract_audio_from_video(video_path, audio_path)
    silence_intervals, non_silence_intervals = detect_silence(audio_path)
    save_intervals_to_json(silence_intervals, non_silence_intervals, silence_output_json, non_silence_output_json)
    os.remove(audio_path)

if __name__ == "__main__":
    video_path = "/Users/duc/Videos/20240718_C0925_copy.MP4"
    main(video_path)

