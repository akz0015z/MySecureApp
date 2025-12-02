let param = new URLSearchParams(window.location.search).get("msg");
if (param) {
    document.body.innerHTML += "<p>Message: " + param + "</p>";
}
