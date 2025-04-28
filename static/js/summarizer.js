document.addEventListener('DOMContentLoaded', function() {
    const apiKeyInput = document.getElementById('apiKey');
    const textInput = document.getElementById('textInput');
    const summaryTypeSelect = document.getElementById('summaryType');
    const summarizeButton = document.getElementById('summarizeButton');
    const summaryContent = document.getElementById('summaryContent');
    const statusDiv = document.getElementById('status');
    const saveButton = document.getElementById('saveButton');
    
    let currentSummaryId = null;

    // Try to load API key from localStorage if available
    if (localStorage.getItem('groqApiKey')) {
        apiKeyInput.value = localStorage.getItem('groqApiKey');
    }

    summarizeButton.addEventListener('click', async function() {
        // Validate inputs
        const apiKey = apiKeyInput.value.trim();
        const text = textInput.value.trim();
        const summaryType = summaryTypeSelect.value;
        
        if (!apiKey) {
            displayStatus('Please enter your Groq API key', 'error');
            return;
        }
        
        if (!text) {
            displayStatus('Please enter text to summarize', 'error');
            return;
        }
        
        // Save API key to localStorage for convenience
        localStorage.setItem('groqApiKey', apiKey);
        
        // Update UI for loading state
        summarizeButton.disabled = true;
        summarizeButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        displayStatus('Generating summary...', 'info');
        summaryContent.innerHTML = '<p class="loading placeholder-text">Processing your text...</p>';
        saveButton.style.display = 'none';
        
        try {
            // Send request to backend
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: text,
                    summary_type: summaryType,
                    groq_api_key: apiKey
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Display summary with markdown rendering
                summaryContent.innerHTML = marked.parse(data.summary);
                displayStatus('Summary generated successfully', 'success');
                currentSummaryId = data.summary_id;
                saveButton.style.display = 'block';
                
                // Apply syntax highlighting
                Prism.highlightAll();
            } else {
                displayStatus(`Error: ${data.detail || 'Failed to generate summary'}`, 'error');
                summaryContent.innerHTML = '<p class="placeholder-text">An error occurred. Please try again.</p>';
            }
        } catch (error) {
            displayStatus(`Error: ${error.message}`, 'error');
            summaryContent.innerHTML = '<p class="placeholder-text">An error occurred. Please try again.</p>';
        } finally {
            summarizeButton.disabled = false;
            summarizeButton.innerHTML = '<i class="fas fa-magic"></i> Generate Summary';
        }
    });
    
    saveButton.addEventListener('click', async function() {
        if (currentSummaryId) {
            try {
                displayStatus('Saving summary...', 'info');
                saveButton.disabled = true;
                saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
                
                const response = await fetch(`/api/save_summary/${currentSummaryId}`, {
                    method: 'POST'
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (data.status === 'success') {
                        window.location.href = `/summary/${currentSummaryId}`;
                    } else {
                        displayStatus('Failed to save summary', 'error');
                    }
                } else {
                    const error = await response.json();
                    displayStatus(`Error: ${error.detail || 'Failed to save summary'}`, 'error');
                }
            } catch (error) {
                displayStatus(`Error: ${error.message}`, 'error');
            } finally {
                saveButton.disabled = false;
                saveButton.innerHTML = '<i class="fas fa-save"></i> Save Summary';
            }
        }
    });
    
    // Helper function to display status messages with appropriate styling
    function displayStatus(message, type) {
        statusDiv.textContent = message;
        
        // Reset all status styling
        statusDiv.style.backgroundColor = '';
        statusDiv.style.color = '';
        
        // Apply appropriate styling based on message type
        switch(type) {
            case 'success':
                statusDiv.style.backgroundColor = 'rgba(16, 185, 129, 0.2)';
                statusDiv.style.color = 'var(--success)';
                break;
            case 'error':
                statusDiv.style.backgroundColor = 'rgba(239, 68, 68, 0.2)';
                statusDiv.style.color = 'var(--danger)';
                break;
            case 'info':
                statusDiv.style.backgroundColor = 'rgba(59, 130, 246, 0.2)';
                statusDiv.style.color = 'var(--primary)';
                break;
        }
    }
    
    // Handle textarea auto-resize
    textInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Focus the text input field when the page loads
    textInput.focus();
});