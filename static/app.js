let mediaRecorder;
let audioChunks = [];

const recordBtn = document.getElementById("recordBtn");
const stopBtn = document.getElementById("stopBtn");
const transcriptionEl = document.getElementById("transcription");
const aiResponseEl = document.getElementById("aiResponse");
const audioPlayer = document.getElementById("audioPlayer");
const avatarVideo = document.getElementById("avatarVideo");

// Create indicators
const recordingIndicator = document.createElement("p");
recordingIndicator.textContent = "🎤 Recording...";
recordingIndicator.style.color = "red";
recordingIndicator.style.display = "none"; // Initially hidden
document.body.insertBefore(recordingIndicator, document.body.firstChild);

// Create loading indicators for processing steps
const processingIndicator = document.createElement("p");
processingIndicator.innerHTML = "⏳ Processing...";
processingIndicator.style.color = "blue";
processingIndicator.style.display = "none";
document.body.appendChild(processingIndicator);

recordBtn.addEventListener("click", async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (event) => {
      audioChunks.push(event.data);
    };

    mediaRecorder.onstop = async () => {
      recordingIndicator.style.display = "none"; // Hide recording message
      processingIndicator.style.display = "block"; // Show processing message

      const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
      const formData = new FormData();
      formData.append("audio", audioBlob);

      try {
        const response = await fetch("/process_audio/", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();

        // Update UI with results
        transcriptionEl.textContent = `✅ ${data.transcription}`;
        aiResponseEl.textContent = `✅ ${data.ai_response}`;
        audioPlayer.src = data.audio_file;
        avatarVideo.src = data.avatar_video;

        processingIndicator.innerHTML = "✅ Processing Complete!";
        processingIndicator.style.color = "green"; // Indicate success
        setTimeout(() => {
          processingIndicator.style.display = "none"; // Hide after completion
        }, 2000);
      } catch (err) {
        console.error("Error processing audio:", err);
        processingIndicator.innerHTML = "❌ Error processing audio!";
        processingIndicator.style.color = "red";
      }
    };

    mediaRecorder.start();
    recordBtn.disabled = true;
    stopBtn.disabled = false;
    recordingIndicator.style.display = "block"; // Show recording message
  } catch (error) {
    console.error("Microphone access denied:", error);
  }
});

stopBtn.addEventListener("click", () => {
  mediaRecorder.stop();
  recordBtn.disabled = false;
  stopBtn.disabled = true;
  recordingIndicator.textContent = "🎤 Recording Stopped!";
  setTimeout(() => {
    recordingIndicator.style.display = "none";
  }, 2000);
});
