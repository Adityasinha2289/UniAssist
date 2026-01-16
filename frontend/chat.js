const input = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");

// -----------------------------
// ENTER TO SEND
// -----------------------------
input.addEventListener("keydown", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// -----------------------------
// MAIN SEND FUNCTION
// -----------------------------
async function sendMessage() {
  const question = input.value.trim();
  if (!question) return;

  // User message
  chatBox.innerHTML += `<div class="message user">${question}</div>`;
  input.value = "";
  chatBox.scrollTop = chatBox.scrollHeight;

  // Typing indicator
  const typingWrapper = document.createElement("div");
  typingWrapper.className = "message bot";
  typingWrapper.innerHTML = `
    <div class="typing">
      <span></span><span></span><span></span>
    </div>
  `;
  chatBox.appendChild(typingWrapper);
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch("http://127.0.0.1:5000/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: question })
    });

    const data = await res.json();
    typingWrapper.remove();

    // Bot message container
    const botMsg = document.createElement("div");
    botMsg.className = "message bot";

    // -----------------------------
    // ANSWER BLOCK (COLLAPSIBLE)
    // -----------------------------
    const answerDiv = document.createElement("div");
    answerDiv.className = "answer-collapsed";
    answerDiv.innerHTML = data.answer;

    botMsg.appendChild(answerDiv);

    // Toggle button (Show more / less)
    const toggleBtn = document.createElement("button");
    toggleBtn.className = "toggle-btn";
    toggleBtn.textContent = "Show more";

    let expanded = false;
    toggleBtn.addEventListener("click", () => {
      expanded = !expanded;
      answerDiv.className = expanded
        ? "answer-expanded"
        : "answer-collapsed";
      toggleBtn.textContent = expanded ? "Show less" : "Show more";
    });

    botMsg.appendChild(toggleBtn);

    // -----------------------------
    // FOLLOW-UP SUGGESTIONS ⭐
    // -----------------------------
    if (data.followups && data.followups.length > 0) {
      const followupDiv = document.createElement("div");
      followupDiv.className = "followups";

      data.followups.forEach(q => {
        const chip = document.createElement("button");
        chip.className = "followup-chip";
        chip.innerText = q;
        chip.onclick = () => {
          input.value = q;
          input.focus();
        };
        followupDiv.appendChild(chip);
      });

      botMsg.appendChild(followupDiv);
    }

    chatBox.appendChild(botMsg);
    chatBox.scrollTop = chatBox.scrollHeight;

  } catch (error) {
    typingWrapper.remove();
    chatBox.innerHTML += `
      <div class="message bot">
        Something went wrong. Please try again.
      </div>
    `;
  }
}
