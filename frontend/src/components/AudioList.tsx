import { useEffect, useState } from "react";

type AudioMeta = {
  id: number;
  key: string;
  filename: string;
  content_type: string;
  size: number;
  created_at: string;
  user?: string;
  transcript?: string | null;
};

export default function AudioList() {
  const [audios, setAudios] = useState<AudioMeta[]>([]);
  const [playingUrl, setPlayingUrl] = useState<string | null>(null);

  useEffect(() => {
    fetch("http://backend:8000/api/audios")
      .then(r => r.json())
      .then(setAudios)
      .catch(console.error);
  }, []);

  const play = async (key: string) => {
    const res = await fetch(`http://backend:8000/api/audio-url/${encodeURIComponent(key)}`);
    const data = await res.json();
    setPlayingUrl(data.url);
  };

  return (
    <div>
      <h3>Liste des messages vocaux</h3>
      <ul>
        {audios.map(a => (
          <li key={a.id} style={{ marginBottom: 12 }}>
            <div><strong>{a.filename}</strong> — {Math.round(a.size/1024)} KB — {a.created_at}</div>
            <div>
              <button onClick={() => play(a.key)}>Play</button>
              {a.transcript && <div><em>Transcript:</em> {a.transcript}</div>}
            </div>
          </li>
        ))}
      </ul>

      {playingUrl && <audio src={playingUrl} controls autoPlay />}
    </div>
  );
}
