async function getRandomLyrics() {
  const res = await fetch("song-list.json");
  const files = await res.json();

  const randomFile = files[Math.floor(Math.random() * files.length)];
  rawSongName = extractSongName(randomFile);
  normalizedSongName = normalizeSongName(rawSongName);
  console.log(randomFile);
  console.log(normalizedSongName);

  const textRes = await fetch(randomFile);
  const lyricsText = await textRes.text();

  return lyricsText;
}

let normalizedSongName = "";
let rawSongName = "";
const lyricsDiv = document.getElementById("lyrics");
const guessedWords = new Set();
let numGuessed = 0;
let total = 0;
let gameWon = false;

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
        span.classList.add("lyric-hidden");
        span.dataset.word = normalized;
        total++;
      } else {
        span.classList.add("revealed");
      }

      span.textContent = token;
      lineDiv.appendChild(span);
      lineDiv.append(" ");
    });
    lyricsDiv.appendChild(lineDiv); 
  });
  document.getElementById("score").innerHTML = `0 / ${total} guessed`;
}

const input = document.getElementById("userInput");

input.addEventListener("input", () => {
  const guess = normalize(input.value);

  if (!guess) return;

  const matches = document.querySelectorAll(
    `.word.lyric-hidden[data-word="${guess}"]`
  );

  if (matches.length > 0) {
    guessedWords.add(guess);

    matches.forEach(span => {
      span.classList.remove("lyric-hidden");
      span.classList.add("revealed");
      numGuessed ++;
      document.getElementById("score").textContent = numGuessed + " / " + total + " guessed";
    });

    input.value = "";
  }
});

input.addEventListener("input", () => {
  if (gameWon) return;

  const userGuess = normalizeSongName(input.value);

  if (userGuess === normalizedSongName) {
    triggerWin();
  }
});

document.getElementById("closeModalBtn").addEventListener("click", () => {
  winModal.classList.add("hidden");
});

document.getElementById("reopenModalBtn").addEventListener("click", () => {
  winModal.classList.remove("hidden");
});

getRandomLyrics().then(text => renderLyrics(text));

function giveUp(){
  const remaining = document.querySelectorAll('.word.lyric-hidden');
  remaining.forEach(span => {
      span.classList.remove("lyric-hidden");
      span.classList.add("revealed");
  })
  document.getElementById("userInput").disabled = true;
  document.getElementById("giveUp").disabled = true;
}

function newSong(){
  total = 0;
  numGuessed = 0;
  getRandomLyrics().then(text => renderLyrics(text));
  document.getElementById("userInput").disabled = false;
  document.getElementById("userInput").value = "";
  document.getElementById("giveUp").disabled = false;
}

function normalizeSongName(name) {
  return name
    .toLowerCase()
    .replace(/\(.*?\)$/g, "")
    .replace(/[^a-z0-9 ]/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function extractSongName(randomFile) {
  return randomFile
    .replace(/^.*\//, "")
    .replace(/\.txt$/, "");
}

function triggerWin() {
  gameWon = true;

  const winModal = document.getElementById("winModal");
  const winSummary = document.getElementById("winSummary");

  const modalSongName = document.getElementById("modalSongName");
  const modalCorrectCount = document.getElementById("modalCorrectCount");

  const winSongName = document.getElementById("winSongName");

  // Fill modal
  modalSongName.textContent = rawSongName;
  modalCorrectCount.textContent = numGuessed;

  // Fill persistent summary
  winSongName.textContent = rawSongName;

  winModal.classList.remove("hidden");
  winSummary.classList.remove("hidden");
}