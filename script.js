async function getRandomLyrics() {
  const res = await fetch("song-list.json");
  const files = await res.json();

  const randomFile = files[Math.floor(Math.random() * files.length)];
  console.log(randomFile);

  const textRes = await fetch(randomFile);
  const lyricsText = await textRes.text();

  return lyricsText;
}

const lyricsDiv = document.getElementById("lyrics");
const guessedWords = new Set();

function normalize(word) {
  return word
    .toLowerCase()
    .replace(/[’']/g, "'")
    .replace(/[^a-z']/g, "");
}

function renderLyrics(text) {
  lyricsDiv.innerHTML = "";
  const lines = text.split("\n");

  lines.forEach(line => {
    const lineDiv = document.createElement("div");
    lineDiv.classList.add("line");

    const tokens = line.split(/\s+/);

    tokens.forEach(token => {
      const span = document.createElement("span");
      span.classList.add("word");

      const normalized = normalize(token);

      if (normalized && !guessedWords.has(normalized)) {
        span.classList.add("hidden");
        span.dataset.word = normalized;
      } else {
        span.classList.add("revealed");
      }

      span.textContent = token;
      lineDiv.appendChild(span);
      lineDiv.append(" ");
    });

    lyricsDiv.appendChild(lineDiv); 
  });
}

const input = document.getElementById("userInput");

input.addEventListener("input", () => {
  const guess = normalize(input.value);

  if (!guess) return;

  const matches = document.querySelectorAll(
    `.word.hidden[data-word="${guess}"]`
  );

  if (matches.length > 0) {
    guessedWords.add(guess);

    matches.forEach(span => {
      span.classList.remove("hidden");
      span.classList.add("revealed");
    });

    input.value = "";
  }
});

getRandomLyrics().then(text => renderLyrics(text));

function giveUp(){
    const remaining = document.querySelectorAll('.word.hidden');
    remaining.forEach(span => {
        span.classList.remove("hidden");
        span.classList.add("revealed");
    })
    document.getElementById("userInput").disabled = true;
    document.getElementById("giveUp").disabled = true;
}