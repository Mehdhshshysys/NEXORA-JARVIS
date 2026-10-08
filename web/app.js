const orb = document.querySelector(".orb");
const core = document.querySelector(".core");
const state = document.querySelector(".state");

const buttons = document.querySelectorAll("button");

let currentState = "idle";

const states = {
    idle: {
        text: "آماده دریافت فرمان",
        speed: "12s",
        scale: "1"
    },

    listening: {
        text: "در حال گوش دادن...",
        speed: "4s",
        scale: "1.08"
    },

    thinking: {
        text: "در حال پردازش...",
        speed: "2s",
        scale: "1.12"
    },

    speaking: {
        text: "NEXORA در حال پاسخ‌گویی...",
        speed: "1.5s",
        scale: "1.16"
    }
};


function setState(newState) {

    if (!states[newState]) {
        return;
    }

    currentState = newState;

    const config = states[newState];

    state.textContent = config.text;

    document.documentElement.style.setProperty(
        "--orb-speed",
        config.speed
    );

    core.style.transform =
        `scale(${config.scale})`;

    document.body.dataset.state = newState;

    console.log(
        `NEXORA STATE: ${newState}`
    );
}


function listen() {

    setState("listening");

    setTimeout(() => {

        setState("thinking");

        setTimeout(() => {

            setState("speaking");

            setTimeout(() => {

                setState("idle");

            }, 2500);

        }, 1800);

    }, 3000);
}


/* =========================
   CHAT
========================= */

function openChat() {

    let chat = document.querySelector(".chat-panel");

    if (chat) {

        chat.classList.toggle("visible");

        return;
    }

    chat = document.createElement("div");

    chat.className = "chat-panel visible";

    chat.innerHTML = `
        <div class="chat-header">
            <span>NEXORA CHAT</span>

            <button class="chat-close">
                ×
            </button>
        </div>

        <div class="chat-messages">

            <div class="message nexora">
                سلام. من NEXORA هستم.
            </div>

            <div class="message nexora">
                آماده دریافت فرمان شما هستم.
            </div>

        </div>

        <div class="chat-input-area">

            <input
                type="text"
                class="chat-input"
                placeholder="پیام خود را بنویسید..."
                autocomplete="off"
            >

            <button class="send-message">
                ➤
            </button>

        </div>
    `;

    document.body.appendChild(chat);

    const close =
        chat.querySelector(".chat-close");

    const input =
        chat.querySelector(".chat-input");

    const send =
        chat.querySelector(".send-message");

    const messages =
        chat.querySelector(".chat-messages");


    close.addEventListener(
        "click",
        () => {

            chat.classList.remove("visible");

        }
    );


    function sendMessage() {

        const text =
            input.value.trim();

        if (!text) {
            return;
        }


        const userMessage =
            document.createElement("div");

        userMessage.className =
            "message user";

        userMessage.textContent =
            text;

        messages.appendChild(
            userMessage
        );


        input.value = "";

        messages.scrollTop =
            messages.scrollHeight;


        setState("thinking");


        setTimeout(() => {

            const reply =
                document.createElement("div");

            reply.className =
                "message nexora";

            reply.textContent =
                "پیام دریافت شد. اتصال به هسته اصلی NEXORA در مرحله بعد اضافه می‌شود.";

            messages.appendChild(
                reply
            );

            messages.scrollTop =
                messages.scrollHeight;

            setState("speaking");


            setTimeout(() => {

                setState("idle");

            }, 1200);

        }, 900);
    }


    send.addEventListener(
        "click",
        sendMessage
    );


    input.addEventListener(
        "keydown",
        (event) => {

            if (event.key === "Enter") {

                sendMessage();

            }

        }
    );

}


/* =========================
   BUTTONS
========================= */

buttons.forEach((button) => {

    button.addEventListener(
        "click",
        () => {

            const text =
                button.textContent.trim();


            if (text.includes("Voice")) {

                listen();

                return;
            }


            if (text.includes("Chat")) {

                openChat();

                return;
            }


            if (text.includes("Settings")) {

                setState("idle");

                alert(
                    "تنظیمات NEXORA در مرحله بعد اضافه می‌شود."
                );

            }

        }
    );

});


/* =========================
   SPACE = VOICE
========================= */

window.addEventListener(
    "keydown",
    (event) => {

        if (
            event.code === "Space" &&
            event.target.tagName !== "INPUT"
        ) {

            event.preventDefault();

            listen();

        }

    }
);


/* =========================
   START
========================= */

setState("idle");
