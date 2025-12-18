fetch("/navbar.html")
    .then(r => r.text())
    .then(html => document.getElementsByTagName("nav")[0].innerHTML += html)