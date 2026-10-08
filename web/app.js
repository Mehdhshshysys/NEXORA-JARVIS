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

                setState("thinking");

                return;
            }

            if (text.includes("Settings")) {

                setState("idle");

                alert(
                    "NEXORA Settings در مرحله بعد اضافه می‌شود."
                );

            }

        }
    );

});


window.addEventListener(
    "keydown",
    (event) => {

        if (event.code === "Space") {

            event.preventDefault();

            listen();

        }

    }
);


setState("idle");
