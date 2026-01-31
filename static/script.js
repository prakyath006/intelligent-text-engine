document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function appendUserMessage(message) {
        const div = document.createElement('div');
        div.className = 'message user-message';
        div.textContent = message;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    function appendBotMessage(data) {
        const div = document.createElement('div');
        div.className = 'message bot-message';

        // Construct the stats grid HTML
        const statsHtml = `
            <div style="font-weight: 600; color: #a78bfa; margin-bottom: 8px; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">System Agent</div>
            <div style="margin-bottom: 8px;"><strong>Analysis for:</strong> "${data.last_word}"</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-label">📈 Top Words</span>
                    <span class="stat-value">${data.top_words}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">🔍 Suggestions</span>
                    <span class="stat-value highlight">${data.suggestions}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">📝 Prediction</span>
                    <span class="stat-value highlight">${data.next_word}</span>
                </div>
                <div class="stat-card">
                    <span class="stat-label">🔗 Related</span>
                    <span class="stat-value">${data.related_words}</span>
                </div>
            </div>
        `;

        div.innerHTML = statsHtml;
        chatBox.appendChild(div);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        appendUserMessage(text);
        userInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            if (!response.ok) throw new Error('Network response was not ok');

            const data = await response.json();
            appendBotMessage(data);
        } catch (error) {
            console.error('Error:', error);
            const div = document.createElement('div');
            div.className = 'message bot-message';
            div.innerHTML = '<div style="font-weight: 600; color: #ef4444; margin-bottom: 5px;">System Error</div>Error processing request.';
            chatBox.appendChild(div);
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
});
