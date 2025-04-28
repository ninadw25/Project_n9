document.addEventListener('DOMContentLoaded', function() {
    // Render summary with markdown
    const summaryContent = document.querySelector('.summary-content');
    summaryContent.innerHTML = marked.parse(`{{ summary.summary | safe }}`);
    
    // Apply syntax highlighting
    Prism.highlightAll();
});

function openTab(evt, tabName) {
    // Hide all tab content
    const tabContent = document.getElementsByClassName("tab-content");
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = "none";
    }
    
    // Remove "active" class from all tab buttons
    const tabLinks = document.getElementsByClassName("tab-btn");
    for (let i = 0; i < tabLinks.length; i++) {
        tabLinks[i].className = tabLinks[i].className.replace(" active", "");
    }
    
    // Show the current tab and add "active" class to the button
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}