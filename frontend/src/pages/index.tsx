import VoiceRecorder from "../components/VoiceRecorder";
import dynamic from "next/dynamic";

const AudioList = dynamic(() => import("../components/AudioList"), { ssr: false });

export default function Home() {
  return (
    <main style={{ padding: 32 }}>
      <h1>🎤 Enregistreur vocal</h1>
      <VoiceRecorder />
      <hr />
      <AudioList />
    </main>
  );
}

