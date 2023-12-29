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





function initNewsSearch() {
    $('#search-button').click(function () {
        const customUrl = $('#custom-url').val();
        if (customUrl) {
            const encodedUrl = encodeURIComponent(customUrl);
            fetch(`http://localhost:8000/api/secure_api/?url=${encodedUrl}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data); 
                    updateNewsItems(data); 
                    
                })
                .catch(error => {
                    console.error('Error fetching data:', error.message);
                });
        }
    });
}