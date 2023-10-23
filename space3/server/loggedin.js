fetch('/loggedin')
  .then(response => {
    return response.text();
  })
  .then(data => {
    document.getElementById('username').textContent = data;
  })
  .catch(error => {
    //handle error
  });