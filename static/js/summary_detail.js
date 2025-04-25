document.addEventListener('DOMContentLoaded', function() {
    const summaryContent = document.getElementById('summaryContent');
    if (summaryContent) {
        summaryContent.innerHTML = marked.parse(summaryContent.textContent);
    }
});