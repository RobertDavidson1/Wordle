async function fetchNode(path) {
    const response = await fetch('/traverse', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ path })
    });
    return response.json();
}

function renderTiles(word, container) {
    const tilesRow = document.createElement('div');
    tilesRow.classList.add('tiles-row');
    word.split('').forEach((letter, index) => {
        const tile = document.createElement('div');
        tile.classList.add('tile', 'gray');
        tile.innerText = letter;
        tile.dataset.index = index;
        tile.addEventListener('click', () => {
            if (tile.classList.contains('gray')) {
                tile.classList.remove('gray');
                tile.classList.add('yellow');
            } else if (tile.classList.contains('yellow')) {
                tile.classList.remove('yellow');
                tile.classList.add('green');
            } else if (tile.classList.contains('green')) {
                tile.classList.remove('green');
                tile.classList.add('gray');
            }
        });
        tilesRow.appendChild(tile);
    });
    container.appendChild(tilesRow);
}

function getColouring(container) {
    const tiles = container.querySelectorAll('.tile');
    return Array.from(tiles).map(tile => {
        if (tile.classList.contains('gray')) return '-';
        if (tile.classList.contains('yellow')) return 'y';
        if (tile.classList.contains('green')) return 'g';
    }).join('');
}

document.addEventListener('DOMContentLoaded', () => {
    const treeContainer = document.getElementById('tree-container');
    let currentPath = [];
    
    fetchNode(currentPath).then(data => {
        renderTiles(data['best word'], treeContainer);
    });

    document.getElementById('submit').addEventListener('click', () => {
        const latestTilesRow = treeContainer.lastChild;
        const colouring = getColouring(latestTilesRow);

        currentPath.push(colouring);
        
        fetchNode(currentPath).then(data => {
            renderTiles(data['best word'], treeContainer);
        });
    });

    document.getElementById('reset').addEventListener('click', () => {
        currentPath = [];
        treeContainer.innerHTML = '';
        fetchNode(currentPath).then(data => {
            renderTiles(data['best word'], treeContainer);
        });
    });
});
