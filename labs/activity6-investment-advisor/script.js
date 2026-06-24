const WEBHOOK_URL =
  "https://n8n.srv923061.hstgr.cloud/webhook/12663502-ff47-45b6-9a8f-c67c083603d9";

const enquiryForm = document.querySelector("#enquiryForm");
const formStatus = document.querySelector("#formStatus");
const chatToggle = document.querySelector("#chatToggle");
const chatWindow = document.querySelector("#chatWindow");
const chatClose = document.querySelector("#chatClose");
const chatForm = document.querySelector("#chatForm");
const chatInput = document.querySelector("#chatInput");
const chatHistory = document.querySelector("#chatHistory");
const chatContact = {
  name: "",
  phone: "",
  email: "",
};
let chatStep = "name";

function setFormStatus(message, type) {
  formStatus.textContent = message;
  formStatus.className = `form-status ${type || ""}`.trim();
}

enquiryForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const submitButton = enquiryForm.querySelector("button[type='submit']");
  const formData = new FormData(enquiryForm);
  const params = new URLSearchParams({ type: "enquiry" });

  for (const [key, value] of formData.entries()) {
    params.set(key, String(value).trim());
  }

  submitButton.disabled = true;
  submitButton.textContent = "Submitting...";
  setFormStatus("", "");

  try {
    const response = await fetch(`${WEBHOOK_URL}?${params.toString()}`, {
      method: "GET",
      headers: {
        Accept: "application/json",
      },
    });

    if (!response.ok) {
      throw new Error(`Webhook returned ${response.status}`);
    }

    setFormStatus("Thank you. Your enquiry has been received.", "success");
    enquiryForm.reset();
  } catch (error) {
    setFormStatus(
      "We could not submit your enquiry right now. Please try again shortly.",
      "error"
    );
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = "Submit Enquiry";
  }
});

function openChat() {
  chatWindow.hidden = false;
  chatToggle.hidden = true;
  chatToggle.setAttribute("aria-expanded", "true");
  window.setTimeout(() => chatInput.focus(), 80);
}

function closeChat() {
  chatWindow.hidden = true;
  chatToggle.hidden = false;
  chatToggle.setAttribute("aria-expanded", "false");
}

function appendMessage(text, sender, extraClass) {
  const message = document.createElement("div");
  message.className = ["chat-message", sender, extraClass].filter(Boolean).join(" ");
  message.textContent = text;
  chatHistory.appendChild(message);
  chatHistory.scrollTop = chatHistory.scrollHeight;
  return message;
}

function updateChatPrompt() {
  const prompts = {
    name: "Enter your full name...",
    phone: "Enter your phone number...",
    email: "Enter your email address...",
    question: "Type your investment question...",
  };
  chatInput.placeholder = prompts[chatStep];
  chatInput.type = chatStep === "email" ? "email" : chatStep === "phone" ? "tel" : "text";
  chatInput.autocomplete =
    chatStep === "email" ? "email" : chatStep === "phone" ? "tel" : "off";
}

function isValidEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

async function readWebhookReply(response) {
  const fallback = "Thank you. Our advisor will get back to you shortly.";
  const contentType = response.headers.get("content-type") || "";

  if (contentType.includes("application/json")) {
    const data = await response.json();
    return data.reply || data.message || fallback;
  }

  const text = (await response.text()).trim();
  if (!text) {
    return fallback;
  }

  try {
    const data = JSON.parse(text);
    return data.reply || data.message || fallback;
  } catch (error) {
    return text;
  }
}

chatToggle.addEventListener("click", openChat);
chatClose.addEventListener("click", closeChat);

chatForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  const message = chatInput.value.trim();
  if (!message) {
    return;
  }

  appendMessage(message, "user");
  chatInput.value = "";

  if (chatStep === "name") {
    chatContact.name = message;
    chatStep = "phone";
    appendMessage("Thank you. What phone number can our advisor use to reach you?", "bot");
    updateChatPrompt();
    chatInput.focus();
    return;
  }

  if (chatStep === "phone") {
    chatContact.phone = message;
    chatStep = "email";
    appendMessage("Thanks. Please share your email address as well.", "bot");
    updateChatPrompt();
    chatInput.focus();
    return;
  }

  if (chatStep === "email") {
    if (!isValidEmail(message)) {
      appendMessage("Please enter a valid email address so our advisor can follow up.", "bot");
      chatInput.focus();
      return;
    }

    chatContact.email = message;
    chatStep = "question";
    appendMessage(
      "Thank you. I have your contact details. What investment planning question can I help with?",
      "bot"
    );
    updateChatPrompt();
    chatInput.focus();
    return;
  }

  chatInput.disabled = true;
  const sendButton = chatForm.querySelector("button");
  sendButton.disabled = true;
  const loadingMessage = appendMessage("Thinking...", "bot", "loading");

  try {
    const response = await fetch(WEBHOOK_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        type: "chat",
        message,
        name: chatContact.name,
        phone: chatContact.phone,
        email: chatContact.email,
        source: "investment-advisor-website",
      }),
    });

    if (!response.ok) {
      throw new Error(`Webhook returned ${response.status}`);
    }

    loadingMessage.textContent = await readWebhookReply(response);
    loadingMessage.classList.remove("loading");
  } catch (error) {
    loadingMessage.textContent =
      "Thank you. Our advisor will get back to you shortly.";
    loadingMessage.classList.remove("loading");
  } finally {
    chatInput.disabled = false;
    sendButton.disabled = false;
    chatInput.focus();
  }
});
