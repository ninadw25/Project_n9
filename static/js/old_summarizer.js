document.addEventListener('DOMContentLoaded', function() {
    const apiKeyInput = document.getElementById('apiKey');
    const textInput = document.getElementById('textInput');
    const summaryTypeSelect = document.getElementById('summaryType');
    const summarizeButton = document.getElementById('summarizeButton');
    const summaryContent = document.getElementById('summaryContent');
    const statusDiv = document.getElementById('status');
    const saveButton = document.getElementById('saveButton');
    
    let currentSummaryId = null;

    summarizeButton.addEventListener('click', async function() {
         // Validate inputs
         const apiKey = apiKeyInput.value.trim();
         const text = textInput.value.trim();
         const summaryType = summaryTypeSelect.value;
         
         if (!apiKey) {
             statusDiv.textContent = 'Please enter your Groq API key';
             return;
         }
         
         if (!text) {
             statusDiv.textContent = 'Please enter text to summarize';
             return;
         }
         
         // Update UI
         summarizeButton.disabled = true;
         statusDiv.textContent = 'Generating summary...';
         summaryContent.innerHTML = '';
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
                 statusDiv.textContent = 'Summary generated successfully';
                 currentSummaryId = data.summary_id;
                 saveButton.style.display = 'block';
                 
                 // Apply syntax highlighting
                 Prism.highlightAll();
             } else {
                 statusDiv.textContent = `Error: ${data.detail || 'Failed to generate summary'}`;
             }
         } catch (error) {
             statusDiv.textContent = `Error: ${error.message}`;
         } finally {
             summarizeButton.disabled = false;
         }
     });
     
     saveButton.addEventListener('click', function() {
         if (currentSummaryId) {
             window.location.href = `/summary/${currentSummaryId}`;
            }
        });
    });