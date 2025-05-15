const imageUpload = document.getElementById("imageUpload");
const preview = document.getElementById("preview");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultDiv = document.getElementById("result");

let base64Image = "";

imageUpload.addEventListener("change", () => {
    const file = imageUpload.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
        base64Image = reader.result;
        preview.src = base64Image;
        preview.style.display = "block";
        analyzeBtn.disabled = false;
        resultDiv.innerHTML = "";
    };
    reader.readAsDataURL(file);
});

analyzeBtn.addEventListener("click", async () => {
    if (!base64Image) return;

    analyzeBtn.disabled = true;
    resultDiv.innerHTML = "Analyzing emotion and fetching music...";

    try {
        const response = await fetch("/detect-emotion", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ image: base64Image }),
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        const data = await response.json();

        let html = `<p><strong>Detected Emotion:</strong> ${data.emotion}</p>`;
        html += `<p><strong>Genre:</strong> ${data.genre}</p>`;
        html += `<h3>Recommended Tracks:</h3>`;

        if (data.tracks.length === 0) {
            html += "<p>No tracks found for this mood.</p>";
        } else {
            data.tracks.forEach(track => {
                html += `<div class="track"><a href="${track.url}" target="_blank">${track.name}</a> by ${track.artist}</div>`;
            });
        }

        resultDiv.innerHTML = html;
    } catch (err) {
        resultDiv.innerHTML = `<p style="color:red;">Error: ${err.message}</p>`;
    } finally {
        analyzeBtn.disabled = false;
    }
});
