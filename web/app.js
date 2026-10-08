const state = {
    mode: "idle",
    chatOpen: false
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


function addMessage(sender, text, type) {

    const messages = document.getElementById(
        "chatMessages"
    );

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


async function sendMessage() {

    const input = document.getElementById(
        "chatInput"
    );

    if (!input) return;

    const command = input.value.trim();

    if (!command) return;

    addMessage(
        "YOU",
        command,
        "user"
    );

    input.value = "";

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

        if (!
