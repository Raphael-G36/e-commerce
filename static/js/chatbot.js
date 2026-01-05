// Chatbot functionality with Voice Support
let conversationHistory = [];
let isListening = false;
let recognition;
let speechSynthesis = window.speechSynthesis;
let chatbotInput = null; // Will be set after DOM loads

// Initialize Web Speech API
function initSpeechRecognition() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.warn('Speech Recognition API not supported in this browser');
        return;
    }
    
    try {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isListening = true;
            updateVoiceButtonUI(true);
            console.log('Voice input started');
        };
        
        recognition.onresult = function(event) {
            let finalTranscript = '';
            let interimTranscript = '';
            
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }
            
            // Update input field with final transcript
            if (finalTranscript.trim()) {
                if (chatbotInput) {
                    chatbotInput.value = finalTranscript.trim();
                    console.log('Captured text:', finalTranscript.trim());
                }
            }
            
            // Show interim results
            if (interimTranscript.trim() && chatbotInput) {
                chatbotInput.placeholder = 'Listening... ' + interimTranscript;
            }
        };
        
        recognition.onend = function() {
            isListening = false;
            updateVoiceButtonUI(false);
            
            // Reset placeholder
            if (chatbotInput) {
                chatbotInput.placeholder = 'Type or use voice...';
            }
            
            console.log('Voice input ended');
            
            // Auto-send the message if text was captured
            setTimeout(function() {
                if (chatbotInput && chatbotInput.value.trim()) {
                    console.log('Auto-sending captured voice text:', chatbotInput.value);
                    // Trigger send by clicking the send button
                    const sendBtn = document.getElementById('chatbot-send');
                    if (sendBtn) {
                        sendBtn.click();
                    }
                }
            }, 500); // Small delay to ensure UI updates
        };
        
        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            isListening = false;
            updateVoiceButtonUI(false);
            
            let errorMessage = `❌ Voice Error: ${event.error}`;
            
            // Provide helpful error messages
            switch(event.error) {
                case 'no-speech':
                    errorMessage = '⚠️ No speech detected. Please make sure your microphone is working and try again.';
                    break;
                case 'audio-capture':
                    errorMessage = '⚠️ No microphone found. Please check your audio input device.';
                    break;
                case 'network':
                    errorMessage = '⚠️ Network error. Please check your internet connection.';
                    break;
                case 'aborted':
                    errorMessage = '⚠️ Voice input was cancelled.';
                    break;
            }
            
            addMessage(errorMessage, 'bot');
        };
        
        console.log('Speech Recognition initialized successfully');
    } catch (error) {
        console.error('Error initializing Speech Recognition:', error);
        recognition = null;
    }
}

document.addEventListener('DOMContentLoaded', function() {
    const chatbotToggle = document.getElementById('chatbot-toggle');
    const chatbotContainer = document.getElementById('chatbot-container');
    const chatbotClose = document.getElementById('chatbot-close');
    chatbotInput = document.getElementById('chatbot-input');
    const chatbotSend = document.getElementById('chatbot-send');
    const voiceBtn = document.getElementById('chatbot-voice-btn');
    const voiceToggleBtn = document.getElementById('chatbot-voice-toggle');
    
    // Initialize speech recognition
    initSpeechRecognition();
    
    // Toggle chatbot
    if (chatbotToggle) {
        chatbotToggle.addEventListener('click', function() {
            chatbotContainer.style.display = chatbotContainer.style.display === 'none' ? 'flex' : 'none';
            if (chatbotContainer.style.display === 'flex') {
                if (chatbotInput) chatbotInput.focus();
                // Hide badge when opened
                const badge = document.getElementById('chatbot-badge');
                if (badge) badge.style.display = 'none';
            }
        });
    }
    
    // Close chatbot
    if (chatbotClose) {
        chatbotClose.addEventListener('click', function() {
            chatbotContainer.style.display = 'none';
        });
    }
    
    // Voice input button
    if (voiceBtn) {
        voiceBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            if (!recognition) {
                console.error('Speech Recognition not available');
                addMessage('❌ Voice input is not supported in your browser. Please use Chrome, Edge, or Safari.', 'bot');
                return;
            }
            
            try {
                if (isListening) {
                    console.log('Stopping voice input');
                    recognition.stop();
                } else {
                    console.log('Starting voice input');
                    // Clear input field
                    if (chatbotInput) {
                        chatbotInput.value = '';
                        chatbotInput.placeholder = 'Listening... speak now';
                    }
                    recognition.start();
                }
            } catch (error) {
                console.error('Voice input error:', error);
                addMessage(`❌ Error: ${error.message}. Please try again.`, 'bot');
            }
        });
    }
    
    // Voice output toggle
    if (voiceToggleBtn) {
        voiceToggleBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            const isEnabled = localStorage.getItem('voiceOutput') !== 'false';
            localStorage.setItem('voiceOutput', isEnabled ? 'false' : 'true');
            voiceToggleBtn.classList.toggle('voice-enabled');
            
            const icon = voiceToggleBtn.querySelector('i');
            if (icon) {
                if (isEnabled) {
                    icon.classList.remove('fa-volume-up');
                    icon.classList.add('fa-volume-mute');
                } else {
                    icon.classList.remove('fa-volume-mute');
                    icon.classList.add('fa-volume-up');
                }
            }
        });
    }
    
    // Send message function
    function sendMessage() {
        const message = chatbotInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        chatbotInput.value = '';
        
        // Show typing indicator
        const typingIndicator = addTypingIndicator();
        
        // Send to API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            if (typingIndicator) typingIndicator.remove();
            
            if (data.success) {
                // Add bot response
                addMessage(data.response, 'bot');
                
                // Update conversation history
                conversationHistory.push(
                    { role: 'user', content: message },
                    { role: 'assistant', content: data.response }
                );
                
                // Keep history limited to last 10 messages
                if (conversationHistory.length > 10) {
                    conversationHistory = conversationHistory.slice(-10);
                }
                
                // Speak response if voice output is enabled
                if (localStorage.getItem('voiceOutput') !== 'false') {
                    speakText(data.response);
                }
            } else {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        })
        .catch(error => {
            if (typingIndicator) typingIndicator.remove();
            addMessage('Sorry, I\'m having trouble connecting. Please try again later.', 'bot');
            console.error('Chatbot error:', error);
        });
    }
    
    // Send on button click
    if (chatbotSend) {
        chatbotSend.addEventListener('click', sendMessage);
    }
    
    // Send on Enter key
    if (chatbotInput) {
        chatbotInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                sendMessage();
            }
        });
    }
});

// Add message to chat
function addMessage(message, type) {
    const chatbotMessages = document.getElementById('chatbot-messages');
    if (!chatbotMessages) return null;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `chatbot-message ${type}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.textContent = message;
    
    contentDiv.appendChild(p);
    messageDiv.appendChild(contentDiv);
    chatbotMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    
    return messageDiv;
}

// Add typing indicator
function addTypingIndicator() {
    const chatbotMessages = document.getElementById('chatbot-messages');
    if (!chatbotMessages) return null;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'chatbot-message bot-message typing-indicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    
    const p = document.createElement('p');
    p.innerHTML = '<span></span><span></span><span></span>';
    
    contentDiv.appendChild(p);
    messageDiv.appendChild(contentDiv);
    chatbotMessages.appendChild(messageDiv);
    
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    
    return messageDiv;
}

// Voice output function
function speakText(text) {
    // Check browser support
    if (!window.speechSynthesis) {
        console.error('Speech Synthesis API not supported');
        return;
    }
    
    // Cancel any ongoing speech
    window.speechSynthesis.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    utterance.pitch = 1;
    utterance.volume = 1;
    utterance.lang = 'en-US';
    
    utterance.onstart = function() {
        console.log('Speech output started');
    };
    
    utterance.onend = function() {
        console.log('Speech output finished');
    };
    
    utterance.onerror = function(event) {
        console.error('Speech output error:', event.error);
    };
    
    window.speechSynthesis.speak(utterance);
}

// Update voice button UI
function updateVoiceButtonUI(listening) {
    const voiceBtn = document.getElementById('chatbot-voice-btn');
    if (voiceBtn) {
        if (listening) {
            voiceBtn.classList.add('recording');
            voiceBtn.innerHTML = '<i class="fas fa-microphone-slash"></i>';
        } else {
            voiceBtn.classList.remove('recording');
            voiceBtn.innerHTML = '<i class="fas fa-microphone-alt"></i>';
        }
    }
}

