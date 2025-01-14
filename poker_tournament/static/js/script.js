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
    const replaysBody = document.getElementById('replaysBody');
    if (!replaysBody) return;

    // Fetching the bot data from the server dynamically
    fetch(`/bots/replays/?bot_name=${botName}`)
        .then(response => response.json())
        .then(replays => {
            // Clear previous content
            replaysBody.innerHTML = '';

            replays.forEach(replay => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${replay.replay_id}</td>
                    <td>${replay.bot_name}</td>
                    <td>${replay.opponent}</td>
                    <td>${replay.date}</td>
                    <td>${replay.result}</td>
                    <td>${replay.earnings}</td>
                    <td><button class="replay-btn" data-replayId="${replay.replay_id}">Replay</button></td>
                `;
                replaysBody.appendChild(row);
            });

            // Add event listener to replay buttons
            document.querySelectorAll('.replay-btn').forEach(button => {
                button.addEventListener('click', function() {
                    const replayId = this.getAttribute('data-replayId');
                    window.location.href = `/game/${replayId}/`; // Adjust the URL accordingly
                });
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
