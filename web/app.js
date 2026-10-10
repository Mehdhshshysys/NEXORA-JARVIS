
const state = {
    mode: "idle",
    chatOpen: false,
    listening: false,
    recognition: null,
    requestInProgress: false
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

    const labels = {
        idle: "SYSTEM READY",
        listening: "LISTENING",
        thinking: "THINKING",
        speaking: "NEXORA SPEAKING"
    };

    if (status) {
        status.textContent = labels[newState] || "SYSTEM READY";
    }
}

function addMessage(sender, text, type) {
    const messages = document.getElementById("chatMessages");
    if (!messages) return;

    const message = document.createElement("div");
    message.className = `message ${type}`;

    const title = document.createElement("strong");
    title.textContent = sender;

    const paragraph = document.createElement("p");
    paragraph.textContent = text;

    message.append(title, paragraph);
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
            <button id="closeChat" type="button">×</button>
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
            <button id="sendMessage" type="button">ارسال</button>
        </div>
    `;

    document.body.appendChild(chatPanel);

    document.getElementById("closeChat").addEventListener("click", () => {
        chatPanel.remove();
        state.chatOpen = false;
    });

    document.getElementById("sendMessage")
        .addEventListener("click", sendMessage);

    document.getElementById("chatInput")
        .addEventListener("keydown", event => {
            if (event.key === "Enter") {
                sendMessage();
            }
        });

    document.getElementById("chatInput").focus();
}

async function sendCommand(command) {
    if (!command || state.requestInProgress) return;

    state.requestInProgress = true;
    setState("thinking");

    try {
        const response = await fetch("/api/command", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ command })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        const data = await response.json();

        const result =
            data.response ||
            data.error ||
            "پاسخی دریافت نشد.";

        if (state.chatOpen) {
            addMessage("NEXORA", result, "nexora");
        }

        speakText(result);

    } catch (error) {
        console.error("NEXORA API ERROR:", error);

        if (state.chatOpen) {
            addMessage(
                "NEXORA",
                "اتصال به هسته NEXORA برقرار نشد. اتصال سرور را بررسی کنید.",
                "nexora"
            );
        }

        setState("idle");

    } finally {
        state.requestInProgress = false;
    }
}

async function sendMessage() {
    const input = document.getElementById("chatInput");
    if (!input) return;

    const command = input.value.trim();
    if (!command) return;

    if (state.requestInProgress) {
        addMessage(
            "NEXORA",
            "لطفاً صبر کنید تا درخواست قبلی تمام شود.",
            "nexora"
        );
        return;
    }

    addMessage("YOU", command, "user");
    input.value = "";

    await sendCommand(command);
}

function speakText(text) {
    if (!("speechSynthesis" in window)) {
        console.error("Speech synthesis is not supported.");
        setState("idle");
        return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(String(text));
    speech.lang = "fa-IR";
    speech.rate = 1;
    speech.pitch = 1;
    speech.volume = 1;

    speech.onstart = () => setState("speaking");

    speech.onend = () => {
        if (!state.listening && !state.requestInProgress) {
            setState("idle");
        }
    };

    speech.onerror = event => {
        console.error("NEXORA SPEECH ERROR:", event.error);
        if (!state.listening && !state.requestInProgress) {
            setState("idle");
        }
    };

    window.speechSynthesis.speak(speech);
}

function startVoice() {
    if (state.listening || state.requestInProgress) return;

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        alert(
            "تشخیص گفتار در این مرورگر پشتیبانی نمی‌شود. از نسخه به‌روز Chrome استفاده کنید."
        );
        return;
    }

    if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
    }

    const recognition = new SpeechRecognition();

    recognition.lang = "fa-IR";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    state.recognition = recognition;
    state.listening = true;
    setState("listening");

    recognition.onstart = () => {
        console.log("NEXORA microphone: ON");
    };

    recognition.onresult = event => {
        const transcript =
            event.results?.[0]?.[0]?.transcript?.trim();

        console.log("NEXORA heard:", transcript);

        if (!transcript) {
            setState("idle");
            return;
        }

        if (state.chatOpen) {
            addMessage("YOU", transcript, "user");
        }

        sendCommand(transcript);
    };

    recognition.onerror = event => {
        console.error("NEXORA VOICE ERROR:", event.error);

        if (event.error === "not-allowed" ||
            event.error === "service-not-allowed") {
            alert("دسترسی میکروفون مجاز نیست. مجوز میکروفون مرورگر را بررسی کنید.");
        } else if (event.error === "audio-capture") {
            alert("میکروفون پیدا نشد یا توسط برنامه دیگری استفاده می‌شود.");
        } else if (event.error === "network") {
            console.warn("تشخیص گفتار با خطای شبکه روبه‌رو شد.");
        }

        state.listening = false;

        if (!state.requestInProgress) {
            setState("idle");
        }
    };

    recognition.onend = () => {
        state.listening = false;
        state.recognition = null;

        if (!state.requestInProgress) {
            setState("idle");
        }
    };

    try {
        recognition.start();
    } catch (error) {
        console.error("VOICE START ERROR:", error);

        state.listening = false;
        state.recognition = null;
        setState("idle");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    setState("idle");

    const chatButton = document.querySelector("#chatButton");
    const voiceButton = document.querySelector("#voiceButton");

    if (chatButton) {
        chatButton.addEventListener("click", createChat);
    }

    if (voiceButton) {
        voiceButton.addEventListener("click", startVoice);
    }

    document.addEventListener("keydown", event => {
        const target = event.target;

        const typing = target instanceof HTMLElement &&
            (target.isContentEditable ||
             ["INPUT", "TEXTAREA", "SELECT"].includes(target.tagName));

        if (
            event.code === "KeyZ" &&
            !event.repeat &&
            !event.ctrlKey &&
            !event.altKey &&
            !event.metaKey &&
            !typing
        ) {
            event.preventDefault();
            startVoice();
        }
    });
});
