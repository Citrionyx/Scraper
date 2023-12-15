    // get the search bar
const input = document.querySelector('input')

// get the button
const button = document.querySelector('button')

// set event listener
button.addEventListener('click', () => {
  // run ajax request
  fetch("http://127.0.0.1:5005/scrape", {
  method: "POST",
  body: JSON.stringify({
    search_query: input.value,
    stores_to_scrape: ["marko", "polo"],
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
  .then((response) => response.json())
  .then((json) => console.log(json));
})