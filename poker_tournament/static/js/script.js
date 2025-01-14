function changePage(page) {
    // Hide all pages first
    const pages = ['home', 'play', 'leaderboard'];
    pages.forEach(p => {
        const element = document.getElementById(`${p}-page`);
        if (element) {
            element.style.display = 'none';
        }
    });
    
    // Show the selected page
    const selectedPage = document.getElementById(`${page}-page`);
    if (selectedPage) {
        selectedPage.style.display = 'block';
    }
    
    // If it's the home page, redirect to index.html
    if (page === 'home') {
        window.location.href = 'index.html';
    }
}

// Bot deployment handling
function handleBotSubmit(event) {
    event.preventDefault();
    
    const form = event.target;
    const botName = form.querySelector('#botName').value;
    const botFile = form.querySelector('#botFile').files[0];
    const description = form.querySelector('#description').value;

    // Show deployment status
    const deploymentStatus = document.querySelector('.deployment-status');
    const statusMessage = document.querySelector('#statusMessage');
    const progressBar = document.querySelector('.progress');
    
    deploymentStatus.style.display = 'block';
    statusMessage.textContent = 'Uploading bot...';
    
    // Simulate upload progress
    let progress = 0;
    const interval = setInterval(() => {
        progress += 10;
        progressBar.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(interval);
            statusMessage.textContent = 'Bot deployed successfully!';
            
            // Reset form after successful deployment
            setTimeout(() => {
                form.reset();
                deploymentStatus.style.display = 'none';
                progressBar.style.width = '0%';
            }, 2000);
        }
    }, 300);

    // In a real application, you would send the data to your server here
    console.log('Bot Details:', {
        name: botName,
        file: botFile,
        description: description
    });
}


// File validation
document.getElementById('botFile')?.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file && !file.name.endsWith('.py')) {
        alert('Please upload a Python (.py) file only');
        e.target.value = '';
    }
});

function populateReplays(botName) { 
    const mockReplays = [
        {
            replayId: 1,
            botName: 'AlphaPoker',
            opponent: 'Opponent1',
            date: '2025-01-01',
            result: 'Win',
            earnings: '$500',
        },
        {
            replayId: 2,
            botName: 'AlphaPoker',
            opponent: 'Opponent2',
            date: '2025-01-02',
            result: 'Loss',
            earnings: '$-300',
        },
        {
            replayId: 3,
            botName: 'BetaBrawler',
            opponent: 'Opponent3',
            date: '2025-01-03',
            result: 'Win',
            earnings: '$800',
        },
        {
            replayId: 4,
            botName: 'GammaCrusher',
            opponent: 'Opponent4',
            date: '2025-01-04',
            result: 'Draw',
            earnings: '$0',
        }
    ];

    const replaysBody = document.getElementById('replaysBody');
    if (!replaysBody) return;

    let filteredReplays;

    // Show all replays if 'All Bots' is selected
    if (botName === 'all') {
        filteredReplays = mockReplays;
    } else {
        filteredReplays = mockReplays.filter(replay => replay.botName === botName);
    }

    // Clear the table and add filtered rows
    replaysBody.innerHTML = '';
    filteredReplays.forEach(replay => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${replay.replayId}</td>
            <td>${replay.botName}</td>
            <td>${replay.opponent}</td>
            <td>${replay.date}</td>
            <td>${replay.result}</td>
            <td>${replay.earnings}</td>
            <td><button class="replay-btn" data-replayId="${replay.replayId}">Replay</button></td>
        `;
        replaysBody.appendChild(row);
    });

    // Add event listener to the replay buttons
    document.querySelectorAll('.replay-btn').forEach(button => {
        button.addEventListener('click', function() {
            const replayId = this.getAttribute('data-replayId');
            window.location.href = `game.html?replayId=${replayId}`;
        });
    });
}

// Event listener to change the bot filter
document.getElementById('botFilter').addEventListener('change', function() {
    const selectedBot = this.value;
    populateReplays(selectedBot);
});

// Initial population of replays for the default option (All Bots)
populateReplays('all');
