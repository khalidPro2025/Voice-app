import { useRef, useState } from "react";

export default function VoiceRecorder() {
  const [recording, setRecording] = useState(false);
  const [audioUrl, setAudioUrl] = useState<string | null>(null);
  const mediaRef = useRef<MediaRecorder | null>(null);
  const chunks = useRef<Blob[]>([]);

  const start = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

    const mimeType = MediaRecorder.isTypeSupported('audio/ogg;codecs=opus')
      ? 'audio/ogg;codecs=opus'
      : (MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : '');

    const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : undefined);
    mediaRef.current = recorder;
    chunks.current = [];

    recorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.current.push(e.data);
    };

    recorder.onstop = async () => {
      const blob = new Blob(chunks.current, { type: mimeType || 'audio/webm' });
      const url = URL.createObjectURL(blob);
      setAudioUrl(url);

      const form = new FormData();
      const suffix = mimeType?.includes('ogg') ? '.ogg' : '.webm';
      form.append("file", blob, "recording" + suffix);

      const res = await fetch("http://backend:8000/api/upload-audio-s3", {
        method: "POST",
        body: form,
      });

      const json = await res.json().catch(() => null);
      console.log("upload result", json);
    };

    recorder.start();
    setRecording(true);
  };

  const stop = () => {
    mediaRef.current?.stop();
    setRecording(false);
  };

  return (
    <div>
      <button onClick={recording ? stop : start}>
        {recording ? "Stop Recording" : "Start Recording"}
      </button>

      {audioUrl && (
        <div>
          <audio controls src={audioUrl}></audio>
          <a href={audioUrl} download>Download</a>
        </div>
      )}
    </div>
  );
}
