import { useState } from "react";

const App = () => {
  const [listening, setListening] = useState(false);

  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();

  recognition.lang = "en-US";
  recognition.continuous = false;

  recognition.onresult = async (event) => {
    const transcript = event.results[event.results.length - 1][0].transcript;
    console.log("You said:", transcript);

    // Send the transcript to the backend
    const response = await fetch("http://127.0.0.1:8000", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ "transcript": transcript }),
    });

    // Handle response
    const data = await response.json();

    console.log("Jarvin said:", data.text);

    const promptUserAgain = data.promptUserAgain;

    if (promptUserAgain) {
      handleStart();
    }
  };

  recognition.onspeechend = function () {
    recognition.stop();
    setListening(false);
    console.log("Speech ended");
  };

  const handleStart = () => {
    setListening(true);
    recognition.start();
  };

  return (
    <div className="h-screen w-screen flex gap-2 flex-col items-center justify-center">
      <h1 className="text-2xl">Meet Jarvin.</h1>
      <button
        className="bg-neutral-200 px-3 py-2 rounded-lg border-neutral-800 border-[1px]"
        onClick={handleStart}
      >
        {listening ? "Listening..." : "How can I help?"}
      </button>
    </div>
  );
};

export default App;
