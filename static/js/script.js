$(document).ready(function () {
    initNewsSearch();
});



function updateNewsItems(entries) {
    const newsItemsContainer = $('#news-items-container');
    newsItemsContainer.empty();

    if (entries && Array.isArray(entries)) {
        entries.forEach(item => {
            const imageUrl = item.image && item.image.url ? item.image.url : 'default-image-path.jpg';
            const title = item.title || 'No Title';
            const description = item.description || 'No description available.';
            const time = item.time || 'No time available';
            const detailUrl = `/newsDetail/?link=${encodeURIComponent(item.link)}`;

            const cardHtml = `
                <div class="col-md-4 mb-3">
                    <a href="${detailUrl}" class="card-link"> 
                        <div class="card">
                            <img src="${imageUrl}" class="card-img-top" alt="${title}">
                            <div class="card-body">
                                <h5 class="card-title">${title}</h5>
                                <p class="card-text">${description.slice(0, 100)}...</p>
                                <p class="card-text"><small class="text-muted">${time}</small></p>
                            </div>
                        </div>
                    </a>
                </div>
            `;
            newsItemsContainer.append(cardHtml);
        });
    } else {
        console.log('Entries is not an array:', entries);
        newsItemsContainer.html('<div class="col-12"><p>No news items found.</p></div>');
    }
}

function initNewsSearch() {
    $('#search-button').click(function () {
        const userInput = $('#custom-url').val();
        let urlParam = userInput;
        let commandParam = '';


        const ampersandIndex = userInput.indexOf('&');
        if (ampersandIndex !== -1) {
            urlParam = userInput.substring(0, ampersandIndex);
            commandParam = userInput.substring(ampersandIndex + 1);
        }

        let fetchUrl = `http://localhost:8000/api/secure_api/?url=${encodeURIComponent(urlParam)}`;
        if (commandParam) {
            fetchUrl += `&command=${encodeURIComponent(commandParam)}`;
        }

        fetch(fetchUrl)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status} - ${response.statusText}`);
                }
                return response.json();
            })
            .then(data => {
                console.log(data);
                console.log(commandParam);
                updateNewsItems(data);
            })
            .catch(error => {
                console.error('Error fetching data:', error.message);
                $('#news-items-container').html('<div class="col-12"><p>Failed to fetch news data. Please try again later.</p></div>');
            });
    });
}


