document.addEventListener('DOMContentLoaded', function() {
    // Get the summary and original text from the server-rendered template
    const summaryContent = document.querySelector('.summary-content');
    const originalContent = document.querySelector('.original-text pre');
    
    // Initialize markdown rendering for summary
    if (summaryContent.textContent.trim()) {
        summaryContent.innerHTML = marked.parse(summaryContent.textContent);
    }
    
    // Tab switching functionality
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Update button states
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Update content visibility
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            
            // Re-run syntax highlighting when switching tabs
            if (tabId === 'summary-tab') {
                Prism.highlightAll();
            }
        });
    });
    
    // Show summary tab by default
    document.querySelector('[data-tab="summary-tab"]').click();
});