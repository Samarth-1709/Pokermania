// Function to deal cards dynamically
const cards = [
    { name: "A\u2660", image: "images/cards/ace_of_spades.png" },
    { name: "K\u2660", image: "images/cards/king_of_spades.png" },
    { name: "Q\u2660", image: "images/cards/queen_of_spades.png" },
    { name: "J\u2660", image: "images/cards/jack_of_spades.png" },
    { name: "10\u2660", image: "images/cards/10_of_spades.png" },
    { name: "9\u2660", image: "images/cards/9_of_spades.png" },
    { name: "8\u2660", image: "images/cards/8_of_spades.png" },
    { name: "7\u2660", image: "images/cards/7_of_spades.png" },
    { name: "6\u2660", image: "images/cards/6_of_spades.png" },
    { name: "5\u2660", image: "images/cards/5_of_spades.png" },
    { name: "4\u2660", image: "images/cards/4_of_spades.png" },
    { name: "3\u2660", image: "images/cards/3_of_spades.png" },
    { name: "2\u2660", image: "images/cards/2_of_spades.png" },
];

let stepIndex = 0; // Track the current step
let shuffledCards = []; // Store the shuffled cards globally

function dealCards() {
    shuffledCards = cards.sort(() => Math.random() - 0.5); // Shuffle the cards
    document.getElementById("nextButton").style.display = "block"; // Show the Next button
    nextStep(); // Start the first step
}

function nextStep() {
    const steps = [
        () => setCardImage('player-card-1', shuffledCards[0].image),
        () => setCardImage('player-card-2', shuffledCards[1].image),
        () => setCardImage('player-card-3', shuffledCards[2].image),
        () => setCardImage('player-card-4', shuffledCards[3].image),
        () => setCardImage('community-card-1', shuffledCards[4].image),
        () => setCardImage('community-card-2', shuffledCards[5].image),
        () => setCardImage('community-card-3', shuffledCards[6].image),
        () => setCardImage('community-card-4', shuffledCards[7].image),
        () => setCardImage('community-card-5', shuffledCards[8].image),
        () => {
            dimPage();
            showResults(shuffledCards);
            document.getElementById("nextButton").style.display = "none"; // Hide the button after all steps
        }
    ];

    if (stepIndex < steps.length) {
        steps[stepIndex++](); // Execute the current step and move to the next
    }
}

// Update the setCardImage function as needed
function setCardImage(cardSlotId, cardImageSrc) {
    const cardSlot = document.getElementById(cardSlotId);
    if (cardSlot) {
        const cardImage = document.createElement('img');
        cardImage.src = cardImageSrc;
        cardImage.alt = cardSlotId;
        cardImage.style.width = "100%";
        cardImage.style.height = "100%";
        cardSlot.innerHTML = '';
        cardSlot.appendChild(cardImage);
    }
}


// Function to dim the page
function dimPage() {
    const overlay = document.createElement('div');
    overlay.style.position = 'fixed';
    overlay.style.top = '0';
    overlay.style.left = '0';
    overlay.style.width = '100%';
    overlay.style.height = '100%';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
    overlay.style.zIndex = '9999';
    overlay.id = 'overlay';
    document.body.appendChild(overlay);
}

// Function to show results on the page
function showResults(shuffledCards) {
    const resultsDiv = document.createElement('div');
    resultsDiv.style.position = 'fixed';
    resultsDiv.style.top = '50%';
    resultsDiv.style.left = '50%';
    resultsDiv.style.transform = 'translate(-50%, -50%)';
    resultsDiv.style.backgroundColor = '#1f2937';
    resultsDiv.style.color = 'white';
    resultsDiv.style.padding = '20px';
    resultsDiv.style.borderRadius = '10px';
    resultsDiv.style.textAlign = 'center';
    resultsDiv.style.fontSize = '1rem';
    resultsDiv.style.zIndex = '10000';
    resultsDiv.style.width = '80%';
    resultsDiv.style.maxWidth = '800px';
    resultsDiv.style.overflowY = 'auto';

    const communityCards = shuffledCards.slice(4, 9);
    const player1Cards = shuffledCards.slice(0, 2);
    const player2Cards = shuffledCards.slice(2, 4);

    let communityCardsHTML = '';
    communityCards.forEach(card => {
        communityCardsHTML += `<img src="${card.image}" alt="${card.name}" style="width: 6%; margin: 5px;">`;
    });

    resultsDiv.innerHTML = `
        <h2>Round Complete!</h2>
        <p>
            <strong style="color: #ffcc00;">Player 1</strong> wins <strong style="color: #ffcc00;">15605 chips</strong> from the pot with a <strong style="color: rgb(255, 0, 0);">Straight</strong>!
        </p>


        <br><br/>
        <h3>Community Cards</h3>
        <div>${communityCardsHTML}</div>
        <br><br/>
        <h3>Results</h3>
        <table style="width: 80%; margin-top: 20px; border-collapse: collapse; margin-left: auto; margin-right: auto;">
            <thead>
                <tr>
                    <th style="padding: 5px;">Player</th>
                    <th style="padding: 5px; width: 30%;">Player Cards</th>
                    <th style="padding: 5px; width: 30%;">Best Hand</th>
                    <th style="padding: 5px;">Combinations</th>
                    <th style="padding: 5px;">Chips</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style="padding: 10px; text-align: center;">Player 1</td>
                    <td style="padding: 10px; text-align: center;">
                        <img src="${player1Cards[0].image}" alt="${player1Cards[0].name}" style="width: 22%; margin: 1px;">
                        <img src="${player1Cards[1].image}" alt="${player1Cards[1].name}" style="width: 22%; margin: 1px;">
                    </td>
                    <td style="padding: 10px; text-align: center;">
                        <img src="${player1Cards[0].image}" alt="${player1Cards[0].name}" style="width: 22%; margin: 1px;">
                        <img src="${player1Cards[1].image}" alt="${player1Cards[1].name}" style="width: 22%; margin: 1px;">
                        <img src="${communityCards[0].image}" alt="${communityCards[0].name}" style="width: 22%; margin: 1px;">
                        <img src="${communityCards[1].image}" alt="${communityCards[1].name}" style="width: 22%; margin: 1px;">
                        <img src="${communityCards[2].image}" alt="${communityCards[2].name}" style="width: 22%; margin: 1px;">
                    </td>
                    <td style="padding: 10px; text-align: center;">Straight</td>
                    <td style="padding: 10px; text-align: center;">+15605</td>
                </tr>
                <tr>
                    <td style="padding: 10px; text-align: center;">Player 2</td>
                    <td style="padding: 10px; text-align: center;">
                        <img src="${player2Cards[0].image}" alt="${player2Cards[0].name}" style="width: 22%; margin: 1px;">
                        <img src="${player2Cards[1].image}" alt="${player2Cards[1].name}" style="width: 22%; margin: 1px;">
                    </td>
                    <td style="padding: 10px; text-align: center;">
                        <img src="${player2Cards[0].image}" alt="${player2Cards[0].name}" style="width: 22%; margin: 1px;">
                        <img src="${player2Cards[1].image}" alt="${player2Cards[1].name}" style="width: 22%; margin: 1px;">
                        <img src="${communityCards[0].image}" alt="${communityCards[0].name}" style="width: 22%; margin: 1px;">
                        <img src="${communityCards[1].image}" alt="${communityCards[1].name}" style="width: 22%; margin: 1px;">
                        <img src="${communityCards[2].image}" alt="${communityCards[2].name}" style="width: 22%; margin: 1px;">
                    </td>
                    <td style="padding: 10px; text-align: center;">Pair</td>
                    <td style="padding: 10px; text-align: center;">-15605</td>
                </tr>
            </tbody>
        </table>

        <button onclick="closeResults()" style="margin-top: 20px; padding: 10px 20px; background-color: #ef4444; color: white; border: none; border-radius: 5px;">Close</button>
    `;

    document.body.appendChild(resultsDiv);
}

// Function to close the results and remove the overlay
function closeResults() {
    const overlay = document.getElementById('overlay');
    const resultsDiv = document.querySelector('div[style*="position: fixed"]');

    if (overlay) overlay.remove();
    if (resultsDiv) resultsDiv.remove();

    // Redirect to poker2.html
    window.location.href = 'play.html';
}

// Call the function to deal cards when the page loads
window.onload = dealCards;