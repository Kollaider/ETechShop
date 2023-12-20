function copyEmailToClipboard() {
    const emailField = document.querySelector('#id_contact');
    const popupElement = document.querySelector('#copyPopup');

    if (emailField && popupElement) {
        const range = document.createRange();
        range.selectNode(emailField);
        window.getSelection().removeAllRanges();
        window.getSelection().addRange(range);

        try {
            // Copy the selected text to the clipboard
            document.execCommand('copy');
            showPopup('Email copied to clipboard');
        } catch (err) {
            console.error('Unable to copy text to clipboard', err);
            showPopup('Copy to clipboard failed');
        }

        window.getSelection().removeAllRanges();
    } else {
        console.error('Email field or popup element not found.');
    }
}

function showPopup(message) {
    const popupElement = document.querySelector('#copyPopup');
    popupElement.textContent = message;
    popupElement.style.display = 'block';

    setTimeout(() => {
        popupElement.style.display = 'none';
    }, 3000); // Adjust the time (in milliseconds) the popup is displayed
}