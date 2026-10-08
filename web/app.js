const state = {
    mode: "idle",
    chatOpen: false,
    listening: false
};

const body = document.body;

function setState(newState) {
    state.mode = newState;

    body.classList.remove(
        "state-idle",
        "state-listening",
        "state-thinking",
        "state-speaking"
    );

    body.classList.add(`state-${newState}`);

    const status = document.querySelector(".status");

    if (!status) return;

    const labels = {
        idle: "SYSTEM READY",
        listening: "LISTENING",
        thinking: "THINKING",
        speaking: "NEXORA SPEAKING"
    };

    status.textContent = labels[newState];
}


function addMessage(sender, text, type) {
    const messages = document.getElementById("chatMessages");

    if (!messages) return;

    const message = document.createElement("div");

    message.className = `message ${type}`;

    message.innerHTML = `
        <strong>${sender}</strong>
        <p></p>
    `;

    message.querySelector("p").textContent = text;

    messages.appendChild(message);

    messages.scrollTop = messages.scrollHeight;
}


function createChat() {
    if (state.chatOpen) return;

    state.chatOpen = true;

    const chatPanel = document.createElement("div");

    chatPanel.className = "chat-panel";

    chatPanel.innerHTML = `
        <div class="chat-header">
            <span>NEXORA CHAT</span>
            <button id="closeChat">×</button>
        </div>

        <div class="chat-messages" id="chatMessages">
            <div class="message nexora">
                <strong>NEXORA</strong>
                <p>سیستم آماده است. چه دستوری دارید؟</p>
            </div>
        </div>

        <div class="chat-input-area">
            <input
                id="chatInput"
                type="text"
                placeholder="دستور خود را وارد کنید..."
                autocomplete="off"
            />

            <button id="sendMessage">
                ارسال
            </button>
        </div>
    `;

    document.body.appendChild(chatPanel);

    document
        .getElementById("closeChat")
        .addEventListener("click", () => {
            chatPanel.remove();
            state.chatOpen = false;
        });

    document
        .getElementById("sendMessage")
        .addEventListener("click", sendMessage);

    document
        .getElementById("chatInput")
        .addEventListener("keydown", event => {
            if (event.key === "Enter") {
                sendMessage();
            }
        });

    document
        .getElementById("chatInput")
        .focus();
}


async function sendCommand(command) {
    if (!command) return;

    setState("thinking");

    try {
        const response = await fetch(
            "/api/command",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    command: command
                })
            }
        );

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        const result =
            data.response ||
            data.error ||
            "پاسخی دریافت نشد.";

        setState("speaking");

        if (state.chatOpen) {
            addMessage(
                "NEXORA",
                result,
                "nexora"
            );
        }

        speakText(result);

        setTimeout(() => {
            setState("idle");
        }, 1200);

    } catch (error) {

        console.error(
            "NEXORA API ERROR:",
            error
        );

        setState("idle");

        if (state.chatOpen) {
            addMessage(
                "NEXORA",
                "اتصال به هسته NEXORA برقرار نشد.",
                "nexora"
            );
        }
    }
}


async function sendMessage() {
    const input = document.getElementById("chatInput");

    if (!input) return;

    const command = input.value.trim();

    if (!command) return;

    addMessage(
        "YOU",
        command,
        "user"
    );

    input.value = "";

    await sendCommand(command);
}


function speakText(text) {
    if (!("speechSynthesis" in window)) {
        return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(text);

    speech.lang = "fa-IR";
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    speech.onstart = () => {
        setState("speaking");
    };

    speech.onend = () => {
        setState("idle");
    };

    window.speechSynthesis.speak(speech);
}


function startVoice() {

    if (state.listening) {
        return;
    }

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        alert(
            "مرورگر شما از تشخیص صدا پشتیبانی نمی‌کند."
        );

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang = "fa-IR";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    state.listening = true;

    setState("listening");

    recognition.onstart = () => {
        console.log(
            "NEXORA microphone: ON"
        );
    };

    recognition.onresult = event => {

        const transcript =
            event.results[0][0].transcript.trim();

        console.log(
            "NEXORA heard:",
            transcript
        );

        state.listening = false;

        if (!transcript) {
            setState("idle");
            return;
        }

        if (state.chatOpen) {
            addMessage(
                "YOU",
                transcript,
                "user"
            );
        }

        sendCommand(transcript);
    };

    recognition.onerror = event => {

        console.error(
            "NEXORA VOICE ERROR:",
            event.error
        );

        state.listening = false;

        setState("idle");

        if (event.error === "not-allowed") {

            alert(
                "دسترسی میکروفون برای NEXORA مجاز نیست."
            );
        }
    };

    recognition.onend = () => {

        state.listening = false;

        if (state.mode === "listening") {
            setState("idle");
        }
    };

    try {

        recognition.start();

    } catch (error) {

        console.error(
            "VOICE START ERROR:",
            error
        );

        state.listening = false;

        setState("idle");
    }
}


document.addEventListener(
    "DOMContentLoaded",
    () => {

        setState("idle");

        const chatButton =
            document.querySelector("#chatButton");

        const voiceButton =
            document.querySelector("#voiceButton");

        if (chatButton) {

            chatButton.addEventListener(
                "click",
                createChat
            );
        }

        if (voiceButton) {

            voiceButton.addEventListener(
                "click",
                startVoice
            );
        }

        document.addEventListener(
            "keydown",
            event => {

                if (
                    event.code === "Space" &&
                    document.activeElement.tagName !== "INPUT" &&
                    document.activeElement.tagName !== "TEXTAREA"
                ) {

                    event.preventDefault();

                    startVoice();
                }
            }
        );
    }
);
