/*
 * Connection settings.
 *
 * You do NOT need to edit this file. Click "Setup" in the top-right menu and
 * enter your two n8n Production webhook URLs plus the admin email. The values
 * are stored in this browser (localStorage) and survive a page reload.
 *
 * Optionally pre-fill them here so the page ships ready-to-run:
 */
const DEFAULTS = {
  enquiryWebhook: "",
  chatWebhook: "",
  adminEmail: "",
};

const STORAGE_KEY = "investmentAdvisor.settings";

function readSettings() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (raw) {
      return { ...DEFAULTS, ...JSON.parse(raw) };
    }
  } catch (error) {
    // localStorage may be unavailable on file:// or in private mode.
  }
  return { ...DEFAULTS };
}

function writeSettings(values) {
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(values));
  } catch (error) {
    /* Non-fatal: settings still apply for this page session. */
  }
}

const settings = readSettings();

function requireWebhook(kind) {
  const url = kind === "enquiry" ? settings.enquiryWebhook : settings.chatWebhook;
  if (!url) {
    const which = kind === "enquiry" ? "Enquiry form" : "Chatbot";
    throw new Error(
      `No ${which} webhook set. Click Setup in the top-right menu and paste your n8n Production URL.`
    );
  }
  return url;
}

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

/*
 * Turn a fetch failure into something a learner can act on. A silent
 * "please try again" hides the three mistakes that actually cause this:
 * no URL set, workflow not active, or CORS not opened up.
 */
function describeWebhookError(error) {
  const message = String((error && error.message) || error);

  if (message.startsWith("No ")) {
    return message;
  }

  if (message.includes("404")) {
    return "404 — n8n did not recognise this webhook. Check the workflow is Active and that you used the Production URL, not the Test URL.";
  }

  if (message.includes("500")) {
    return "500 — the workflow ran but errored. Check the n8n execution log; the usual cause is a missing Admin email in Setup, or a credential that needs re-selecting.";
  }

  if (message.includes("Webhook returned")) {
    return `${message}. Check the n8n execution log for this workflow.`;
  }

  return "Could not reach the webhook. Most often this is CORS — in the n8n Webhook node set Allowed Origins (CORS) to *, then Save and re-activate the workflow.";
}

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
    const url = requireWebhook("enquiry");

    // Sent as a POST with a JSON body so the enquiry form and the chatbot use
    // the SAME webhook method. A Webhook node set to POST would 404 a GET.
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "ngrok-skip-browser-warning": "true",
      },
      body: JSON.stringify({
        ...Object.fromEntries(params),
        adminEmail: settings.adminEmail,
      }),
    });

    if (!response.ok) {
      throw new Error(`Webhook returned ${response.status}`);
    }

    setFormStatus("Thank you. Your enquiry has been received.", "success");
    enquiryForm.reset();
  } catch (error) {
    setFormStatus(describeWebhookError(error), "error");
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
    const response = await fetch(requireWebhook("chat"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "ngrok-skip-browser-warning": "true",
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
    loadingMessage.textContent = describeWebhookError(error);
    loadingMessage.classList.remove("loading");
    loadingMessage.classList.add("error");
  } finally {
    chatInput.disabled = false;
    sendButton.disabled = false;
    chatInput.focus();
  }
});

/* ---- Setup menu (top-right) ---- */

const setupMenu = document.querySelector(".setup-menu");
const setupToggle = document.querySelector("#setupToggle");
const setupPanel = document.querySelector("#setupPanel");
const setupClose = document.querySelector("#setupClose");
const setupSave = document.querySelector("#setupSave");
const setupClear = document.querySelector("#setupClear");
const setupBadge = document.querySelector("#setupBadge");

const enquiryInput = document.querySelector("#enquiryWebhook");
const chatWebhookInput = document.querySelector("#chatWebhook");
const adminEmailInput = document.querySelector("#adminEmail");

const enquiryStatus = document.querySelector("#enquiryStatus");
const chatStatusEl = document.querySelector("#chatStatus");
const adminStatus = document.querySelector("#adminStatus");

const testEnquiry = document.querySelector("#testEnquiry");
const testChat = document.querySelector("#testChat");

function setStatus(el, message, type) {
  el.textContent = message;
  el.className = `setup-status ${type || ""}`.trim();
}

function looksLikeUrl(value) {
  try {
    const parsed = new URL(value);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch (error) {
    return false;
  }
}

/* Red dot until both webhooks and the admin email are in place. */
function refreshBadge() {
  const ready =
    Boolean(settings.enquiryWebhook) &&
    Boolean(settings.chatWebhook) &&
    Boolean(settings.adminEmail);
  setupBadge.hidden = false;
  setupBadge.className = `setup-badge ${ready ? "ready" : ""}`.trim();
  setupBadge.title = ready ? "Setup complete" : "Setup incomplete";
}

function applySettings() {
  const enquiry = enquiryInput.value.trim().replace(/\s+/g, "");
  const chat = chatWebhookInput.value.trim().replace(/\s+/g, "");
  const admin = adminEmailInput.value.trim();
  let ok = true;

  if (enquiry && !looksLikeUrl(enquiry)) {
    setStatus(enquiryStatus, "Must start with http:// or https://", "error");
    ok = false;
  } else {
    settings.enquiryWebhook = enquiry;
    setStatus(enquiryStatus, enquiry ? "Saved." : "", enquiry ? "success" : "");
  }

  if (chat && !looksLikeUrl(chat)) {
    setStatus(chatStatusEl, "Must start with http:// or https://", "error");
    ok = false;
  } else {
    settings.chatWebhook = chat;
    setStatus(chatStatusEl, chat ? "Saved." : "", chat ? "success" : "");
  }

  if (admin && !isValidEmail(admin)) {
    setStatus(adminStatus, "Enter a valid email address.", "error");
    ok = false;
  } else {
    settings.adminEmail = admin;
    setStatus(
      adminStatus,
      admin ? "Enquiries will be emailed here." : "",
      admin ? "success" : ""
    );
  }

  if (ok) {
    writeSettings(settings);
  }
  refreshBadge();
  return ok;
}

/*
 * Send a harmless probe so learners can verify each webhook independently
 * before using the real form or chat.
 */
async function testWebhook(kind, url, statusEl, button) {
  if (!url) {
    setStatus(statusEl, "Enter the webhook URL first.", "error");
    return;
  }
  if (!looksLikeUrl(url)) {
    setStatus(statusEl, "Must start with http:// or https://", "error");
    return;
  }

  button.disabled = true;
  setStatus(statusEl, "Testing...", "pending");

  const payload =
    kind === "enquiry"
      ? {
          type: "enquiry",
          name: "Connection Test",
          email: "test@example.com",
          phone: "",
          goal: "Connection test",
          message: "Connection test from the Investment Advisor website.",
          adminEmail: settings.adminEmail || adminEmailInput.value.trim(),
          test: true,
        }
      : {
          type: "chat",
          message: "Connection test from the Investment Advisor website.",
          name: "Connection Test",
          phone: "",
          email: "",
          source: "webhook-test",
          test: true,
        };

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "ngrok-skip-browser-warning": "true",
      },
      body: JSON.stringify(payload),
    });

    if (response.ok) {
      setStatus(statusEl, `Success — n8n responded with ${response.status}.`, "success");
    } else if (response.status === 404) {
      setStatus(
        statusEl,
        "404 — not recognised. Check the workflow is Active and that this is the Production URL.",
        "error"
      );
    } else if (response.status === 500) {
      setStatus(
        statusEl,
        "500 — the workflow ran but errored. Check the n8n execution log (often a missing admin email or credential).",
        "error"
      );
    } else {
      setStatus(statusEl, `n8n responded with ${response.status}.`, "error");
    }
  } catch (error) {
    setStatus(
      statusEl,
      "Could not reach it. Usually CORS — set Allowed Origins (CORS) to * in the Webhook node, then re-activate.",
      "error"
    );
  } finally {
    button.disabled = false;
  }
}

function openSetup() {
  setupPanel.hidden = false;
  setupToggle.setAttribute("aria-expanded", "true");
  window.setTimeout(() => enquiryInput.focus(), 60);
}

function closeSetup() {
  setupPanel.hidden = true;
  setupToggle.setAttribute("aria-expanded", "false");
}

setupToggle.addEventListener("click", () => {
  if (setupPanel.hidden) {
    openSetup();
  } else {
    closeSetup();
  }
});

setupClose.addEventListener("click", closeSetup);

setupSave.addEventListener("click", () => {
  if (applySettings()) {
    setupSave.textContent = "Saved";
    window.setTimeout(() => {
      setupSave.textContent = "Save settings";
    }, 1400);
  }
});

setupClear.addEventListener("click", () => {
  enquiryInput.value = "";
  chatWebhookInput.value = "";
  adminEmailInput.value = "";
  settings.enquiryWebhook = "";
  settings.chatWebhook = "";
  settings.adminEmail = "";
  writeSettings(settings);
  [enquiryStatus, chatStatusEl, adminStatus].forEach((el) => setStatus(el, "", ""));
  refreshBadge();
});

testEnquiry.addEventListener("click", () =>
  testWebhook("enquiry", enquiryInput.value.trim(), enquiryStatus, testEnquiry)
);

testChat.addEventListener("click", () =>
  testWebhook("chat", chatWebhookInput.value.trim(), chatStatusEl, testChat)
);

// Close when clicking outside the menu or pressing Escape.
document.addEventListener("click", (event) => {
  if (!setupPanel.hidden && !setupMenu.contains(event.target)) {
    closeSetup();
  }
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && !setupPanel.hidden) {
    closeSetup();
  }
});

enquiryInput.value = settings.enquiryWebhook;
chatWebhookInput.value = settings.chatWebhook;
adminEmailInput.value = settings.adminEmail;
refreshBadge();

if (!settings.enquiryWebhook || !settings.chatWebhook || !settings.adminEmail) {
  openSetup();
}
