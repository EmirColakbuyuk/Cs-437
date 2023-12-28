

$(document).ready(function () {
    initNewsSearch();
});

function initNewsSearch() {
    $('#search-button').click(function () {
        const customUrl = $('#custom-url').val();
        if (customUrl) {
            const encodedUrl = encodeURIComponent(customUrl);
            fetch(`http://localhost:8000/api/secure_api/?url=${encodedUrl}`)
                .then(response => response.json())
                .then(data => {
                    console.log(data);  // Veriyi konsola yazdır
                    updateNewsItems(data.entries);
                })
                .catch(error => {
                    console.error('Error fetching data:', error.message);
                });
        }
    });
}

function updateNewsItems(entries) {
    const newsItemsContainer = $('#news-items-container');
    newsItemsContainer.empty(); // Mevcut haber öğelerini temizle

    if (entries) {
        entries.forEach(item => {
            // Her haber öğesi için HTML oluşturun
            const cardHtml = `
                <div class="col-md-4 mb-3">
                    <a href="${item.link}" class="card-link">
                        <div class="card">
                            ${(item.image && item.image.url) ? `<img src="${item.image.url}" class="card-img-top" alt="${item.title}">` : ''}
                            <div class="card-body">
                                <h5 class="card-title" style="color: red">${item.title}</h5>
                                <p class="card-text">${item.description.slice(0, 100)}...</p>
                                <p class="card-text"><small class="text-muted">${item.time}</small></p>
                            </div>
                        </div>
                    </a>
                </div>
            `;
            newsItemsContainer.append(cardHtml);
        });
    } else {
        console.log('Entries is not an array:', data.entries);
        newsItemsContainer.html('<div class="col-12"><p>No news items found.</p></div>');
    }
}
