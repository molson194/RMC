const queryString = window.location.search;
console.log(queryString);
const urlParams = new URLSearchParams(queryString);
const code = urlParams.get('code');
const state = urlParams.get('state');

(async function () {
  let response = await fetch('/api/Authentication?token=' + code);
  let message = await response.text();
  console.log(message);
})();