var rules_element = document.querySelector('.rules-wrapper');

document.getElementById("rules").onclick = function() {
    rules_element.classList.toggle('rules-active')
};

document.getElementById("rules-close").onclick = function() {
    rules_element.classList.toggle('rules-active')
};
