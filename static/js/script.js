$(document).ready(function () {
    initNewsSearch();
});



function updateNewsItems(entries) {
    const newsItemsContainer = $('#news-items-container');
    newsItemsContainer.empty(); // Clear existing items

    if (entries && Array.isArray(entries)) {
        entries.forEach(item => {
            const imageUrl = item.image && item.image.url ? item.image.url : 'default-image-path.jpg';
            const title = item.title || 'No Title';
            const description = item.description || 'No description available.';
            const time = item.time || 'No time available';
            const detailUrl = `/newsDetail/?link=${encodeURIComponent(item.link)}`; // URL'i oluştur

            const cardHtml = `
                <div class="col-md-4 mb-3">
                    <a href="${detailUrl}" class="card-link">  <!-- Burada URL kullanılıyor -->
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

function extractDomain(url) {
    let domain;

    // Remove protocol (http, https, etc.) if present
    if (url.indexOf("://") > -1) {
        domain = url.split('/')[2];
    } else {
        domain = url.split('/')[0];
    }

    // Remove port number and query string if present
    domain = domain.split(':')[0].split('?')[0];

    // Split the domain into its parts
    let domainParts = domain.split('.');

    // Remove the '.tr' if it's the TLD
    if (domainParts[domainParts.length - 1].toLowerCase() === 'tr') {
        domainParts.pop();
    }

    // Join the remaining parts of the domain
    domain = domainParts.join('.');

    return domain;
}


async function initNewsSearch() {
    $('#search-button').click(async function () {
        const fullUrl = $('#custom-url').val();

        if (fullUrl) {
            $('#user-input-title').html(fullUrl);

            try {
                // Extract the domain for the ping operation
                const domainForPing = extractDomain(fullUrl);
                console.log('Domain for ping:', domainForPing);
                console.log('Full URL:', fullUrl);

                // Ping the server with the extracted domain
                const pingResponse = await fetch(`http://localhost:8000/api/ping/?url=${encodeURIComponent(domainForPing)}`);
                if (!pingResponse.ok) {
                    throw new Error(`Ping failed: ${pingResponse.status} - ${pingResponse.statusText}`);
                }
                const pingResult = await pingResponse.text();
                console.log('Ping result:', pingResult);

                // Fetch news data using the full URL
                const response = await fetch(`http://localhost:8000/api/secure_api/?url=${encodeURIComponent(fullUrl)}`);
                if (!response.ok) {
                    throw new Error(`Network response was not ok: ${response.status} - ${response.statusText}`);
                }
                const data = await response.json();
                console.log(data);
                updateNewsItems(data);
            } catch (error) {
                console.error('Error:', error.message);
                $('#news-items-container').html('<div class="col-12"><p>Error occurred. Please try again later.</p></div>');
            }
        }
    });
}
//s