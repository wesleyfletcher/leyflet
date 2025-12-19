fetch("/templates/head.html")
    .then(r => r.text())
    .then(html => document.getElementsByTagName("head")[0].innerHTML += html)

fetch("/templates/navbar.html")
    .then(r => r.text())
    .then(html => document.getElementsByTagName("nav")[0].innerHTML += html)