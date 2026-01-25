async function scan() {
  const res = await fetch("/zigbee/scan");
  const devices = await res.json();

  const container = document.getElementById("devices");
  container.innerHTML = "";

  devices.forEach(d => {
    const card = document.createElement("div");
    card.className = "device";

    card.innerHTML = `
      <h3>${d.name}</h3>
      <label class="switch">
        <input type="checkbox" ${d.state ? "checked" : ""}
               onchange="toggle('${d.ieee}', this.checked)">
        <span class="slider"></span>
      </label>
    `;

    container.appendChild(card);
  });
}

async function toggle(ieee, value) {
  await fetch("/zigbee/toggle", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ ieee, value })
  });
}
