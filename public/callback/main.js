const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const code = urlParams.get('code')
const state = urlParams.get('state')
fetchToken();

async function fetchToken() {
    let response = await fetch('/api/Authentication?code=' + code);
    let message = await response.text();
    console.log(message);
}