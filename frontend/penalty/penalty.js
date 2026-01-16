async function calculatePenalty() {
  const offence = document.getElementById("offence").value;
  const count = document.getElementById("count").value;
  const result = document.getElementById("result");

  if (!offence) {
    alert("Please select an offence.");
    return;
  }

  const res = await fetch("http://127.0.0.1:5000/penalty/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ offence, count })
  });

  const data = await res.json();

  if (data.error) {
    result.innerHTML = `<p>${data.error}</p>`;
    result.classList.remove("hidden");
    return;
  }

  result.innerHTML = `
    <h3>⚠️ Penalty Result</h3>
    <p><strong>Offence:</strong> ${data.offence}</p>
    <p><strong>Occurrence:</strong> ${data.occurrence}</p>
    <p><strong>Fine:</strong> ₹${data.fine}</p>
    <p><strong>Action:</strong> ${data.action}</p>
    <p><strong>Notes:</strong> ${data.notes}</p>
    <p style="font-size:12px;opacity:0.7">${data.source}</p>
  `;

  result.classList.remove("hidden");
}
