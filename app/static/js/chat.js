/**
 * UTH Student Nutrition Meal Planner - Chatbot Controller
 */

document.addEventListener('DOMContentLoaded', function () {
    // === 1. STICKY CHATBOT WIDGET ACTIONS ===
    const chatTrigger = document.getElementById('chat-trigger');
    const chatWindow = document.getElementById('chat-window');
    const chatClose = document.getElementById('chat-close');
    const chatInputText = document.getElementById('chat-input-text');
    const chatBtnSend = document.getElementById('chat-btn-send');
    const chatbotMessagesBox = document.getElementById('chatbot-messages-box');
    
    // Toggle widget window
    if (chatTrigger) {
        chatTrigger.addEventListener('click', function () {
            const isClosed = chatWindow.classList.contains('d-none');
            const openIcon = chatTrigger.querySelector('.chat-icon-open');
            const closeIcon = chatTrigger.querySelector('.chat-icon-close');
            
            if (isClosed) {
                chatWindow.classList.remove('d-none');
                chatWindow.classList.add('fade-in');
                openIcon.classList.add('d-none');
                closeIcon.classList.remove('d-none');
                chatInputText.focus();
                scrollToBottom(chatbotMessagesBox);
            } else {
                closeChatWidget();
            }
        });
    }
    
    if (chatClose) {
        chatClose.addEventListener('click', closeChatWidget);
    }
    
    function closeChatWidget() {
        if (!chatWindow) return;
        const openIcon = chatTrigger.querySelector('.chat-icon-open');
        const closeIcon = chatTrigger.querySelector('.chat-icon-close');
        chatWindow.classList.add('d-none');
        openIcon.classList.remove('d-none');
        closeIcon.classList.add('d-none');
    }
    
    // Send message widget
    if (chatBtnSend) {
        chatBtnSend.addEventListener('click', sendWidgetMessage);
    }
    if (chatInputText) {
        chatInputText.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendWidgetMessage();
            }
        });
    }
    
    function sendWidgetMessage() {
        const text = chatInputText.value.trim();
        if (!text) return;
        
        // Append user message
        appendMessage(chatbotMessagesBox, text, 'user');
        chatInputText.value = '';
        
        // Append typing indicator
        const typingId = appendTypingIndicator(chatbotMessagesBox);
        scrollToBottom(chatbotMessagesBox);
        
        // Post message to backend
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            removeTypingIndicator(chatbotMessagesBox, typingId);
            if (data.success) {
                appendMessage(chatbotMessagesBox, data.reply, 'bot');
            } else {
                appendMessage(chatbotMessagesBox, "Xin lỗi bạn, chatbot đang gặp sự cố nhỏ. Vui lòng thử lại sau nhé!", 'bot');
            }
            scrollToBottom(chatbotMessagesBox);
        })
        .catch(err => {
            console.error(err);
            removeTypingIndicator(chatbotMessagesBox, typingId);
            appendMessage(chatbotMessagesBox, "Lỗi kết nối mạng, vui lòng thử lại.", 'bot');
            scrollToBottom(chatbotMessagesBox);
        });
    }

    // === 2. DEDICATED CHAT PAGE ACTIONS ===
    const chatPageInputText = document.getElementById('chat-page-input-text');
    const chatPageBtnSend = document.getElementById('chat-page-btn-send');
    const chatPageMessagesBox = document.getElementById('chat-page-messages-box');
    const chatSuggestions = document.getElementById('chat-quick-suggestions');
    
    if (chatPageBtnSend) {
        chatPageBtnSend.addEventListener('click', sendPageMessage);
    }
    if (chatPageInputText) {
        chatPageInputText.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendPageMessage();
            }
        });
    }
    
    // Quick suggestion chips
    if (chatSuggestions) {
        chatSuggestions.addEventListener('click', function (e) {
            const btn = e.target.closest('.chat-chip-btn');
            if (btn) {
                const msg = btn.getAttribute('data-msg');
                if (msg) {
                    if (chatPageInputText) {
                        chatPageInputText.value = msg;
                        sendPageMessage();
                    }
                }
            }
        });
    }
    
    function sendPageMessage() {
        const text = chatPageInputText.value.trim();
        if (!text) return;
        
        appendMessage(chatPageMessagesBox, text, 'user');
        chatPageInputText.value = '';
        
        const typingId = appendTypingIndicator(chatPageMessagesBox);
        scrollToBottom(chatPageMessagesBox);
        
        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        })
        .then(res => res.json())
        .then(data => {
            removeTypingIndicator(chatPageMessagesBox, typingId);
            if (data.success) {
                appendMessage(chatPageMessagesBox, data.reply, 'bot');
            } else {
                appendMessage(chatPageMessagesBox, "Xin lỗi bạn, chatbot đang gặp sự cố nhỏ. Vui lòng thử lại sau nhé!", 'bot');
            }
            scrollToBottom(chatPageMessagesBox);
        })
        .catch(err => {
            console.error(err);
            removeTypingIndicator(chatPageMessagesBox, typingId);
            appendMessage(chatPageMessagesBox, "Lỗi kết nối mạng, vui lòng thử lại.", 'bot');
            scrollToBottom(chatPageMessagesBox);
        });
    }

    // === 3. CORE DISPLAY HELPER FUNCTIONS ===
    
    function appendMessage(container, text, sender) {
        if (!container) return;
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message fade-in`;
        
        // Basic Markdown-to-HTML parser for simple representations:
        // - Bold: **text**
        // - Bullet points: - item or * item
        // - Headings: ### text
        // - Newlines: \n
        let htmlContent = parseMarkdownToHtml(text);
        msgDiv.innerHTML = htmlContent;
        
        container.appendChild(msgDiv);
    }
    
    function appendTypingIndicator(container) {
        if (!container) return null;
        const typingId = 'typing_' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.id = typingId;
        typingDiv.className = 'message bot-message fade-in d-flex align-items-center';
        typingDiv.innerHTML = `
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        `;
        container.appendChild(typingDiv);
        return typingId;
    }
    
    function removeTypingIndicator(container, typingId) {
        if (!container || !typingId) return;
        const indicator = document.getElementById(typingId);
        if (indicator) {
            container.removeChild(indicator);
        }
    }
    
    function scrollToBottom(container) {
        if (!container) return;
        setTimeout(() => {
            container.scrollTop = container.scrollHeight;
        }, 50);
    }
    
    function parseMarkdownToHtml(text) {
        let parsed = text;
        
        // Escape HTML to prevent injection
        parsed = parsed
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
            
        // Parse bold: **text** -> <strong>text</strong>
        parsed = parsed.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Parse custom list items:
        // Lines starting with "- " or "* " -> <li>
        let lines = parsed.split('\n');
        let inList = false;
        for (let i = 0; i < lines.length; i++) {
            let line = lines[i].trim();
            if (line.startsWith('- ') || line.startsWith('* ')) {
                let content = line.substring(2);
                if (!inList) {
                    lines[i] = '<ul class="mb-2 ps-3">' + `<li>${content}</li>`;
                    inList = true;
                } else {
                    lines[i] = `<li>${content}</li>`;
                }
            } else {
                if (inList) {
                    lines[i] = '</ul>' + lines[i];
                    inList = false;
                }
            }
        }
        if (inList) {
            lines[lines.length - 1] += '</ul>';
        }
        parsed = lines.join('\n');
        
        // Parse headings: ### Heading -> <h6 class="fw-bold mt-2">
        parsed = parsed.replace(/###\s*(.*?)\r?\n/g, '<h6 class="fw-bold text-success-custom mt-3">$1</h6>');
        parsed = parsed.replace(/###\s*(.*?)$/g, '<h6 class="fw-bold text-success-custom mt-3">$1</h6>');
        
        // Replace remaining newlines with <br>
        parsed = parsed.replace(/\n/g, '<br>');
        
        return parsed;
    }
});
