document.getElementById('search-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    const query = document.getElementById('search-input').value.trim();
    if (query) {
        fetch(`/search/?query=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                const searchResultsDiv = document.getElementById('search-results');
                searchResultsDiv.innerHTML = ''; // Clear previous search results
                if (data.search_results && data.search_results.length > 0) {
                    const ul = document.createElement('ul');
                    data.search_results.forEach(result => {
                        const li = document.createElement('li');
                        li.textContent = result.title;
                        ul.appendChild(li);
                    });
                    searchResultsDiv.appendChild(ul);
                } else {
                    searchResultsDiv.textContent = 'No results found.';
                }
            })
            .catch(error => console.error('Error fetching search results:', error));
    }
});
