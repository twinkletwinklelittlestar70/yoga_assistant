export const doAnalyse = (url) => {
  return fetch('/api/analyse', {
    body: JSON.stringify({url}),
    cache: 'no-cache',
    headers: {
      'content-type': 'application/json'
    },
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, cors, *same-origin
  })
  .then(response => response.json())
}