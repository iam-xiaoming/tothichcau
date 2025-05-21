document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('apply-filters').addEventListener('click', function () {
        const checkedBoxes = document.querySelectorAll('.filter-option input:checked');
        const selectedGenres = Array.from(checkedBoxes).map(cb => cb.value);

        const params = new URLSearchParams();
        selectedGenres.forEach(genre => params.append('genres[]', genre));

        fetch(`/api/list/filter-games/?${params.toString()}`)
            .then(response => response.json())
            .then(data => {
                const gamesGrid = document.getElementById('games-grid');
                gamesGrid.innerHTML = ''; // clear old games

                data.games.forEach(game => {
                    const gameCard = document.createElement('div');
                    gameCard.classList.add('game-card');

                    gameCard.innerHTML = `
                        <div class="game-card-image">
                            <img src="${game.image_url}" alt="${game.name}">
                        </div>
                        <div class="game-card-content">
                            <h3 class="game-title">${game.name}</h3>
                            <div class="game-genres">
                                ${game.genres.map(g => `<span class="genre">${g}</span>`).join('')}
                            </div>
                            <div class="game-release">${game.release_date}</div>
                            <p class="game-description line-clamp">${game.description}</p>
                            <div class="game-actions">
                                <a href="/games/${game.status}-game-details/${game.id}/" class="btn-primary">View Details</a>
                            </div>
                        </div>
                    `;
                    gamesGrid.appendChild(gameCard);
                });
            });
    });

    document.getElementById('reset-filters').addEventListener('click', function () {
        const checkedBoxes = document.querySelectorAll('.filter-option input:checked');
        checkedBoxes.forEach(cb => cb.checked = false);

        fetch(`/api/list/filter-games/`)
            .then(response => response.json())
            .then(data => {
                const gamesGrid = document.getElementById('games-grid');
                gamesGrid.innerHTML = ''; // clear old games

                data.games.forEach(game => {
                    const gameCard = document.createElement('div');
                    gameCard.classList.add('game-card');

                    gameCard.innerHTML = `
                        <div class="game-card-image">
                            <img src="${game.image_url}" alt="${game.name}">
                        </div>
                        <div class="game-card-content">
                            <h3 class="game-title">${game.name}</h3>
                            <div class="game-genres">
                                ${game.genres.map(g => `<span class="genre">${g}</span>`).join('')}
                            </div>
                            <div class="game-release">${game.release_date}</div>
                            <p class="game-description line-clamp">${game.description}</p>
                            <div class="game-actions">
                                <a href="/games/${game.status}-game-details/${game.id}/" class="btn-primary">View Details</a>
                            </div>
                        </div>
                    `;
                    gamesGrid.appendChild(gameCard);
                });
            });
    });
});