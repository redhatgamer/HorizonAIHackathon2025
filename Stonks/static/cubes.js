// document.addEventListener("DOMContentLoaded", function() {
//     const cubeContainer = document.getElementById("cubeContainer");
//     // Add your cube animation logic here
// });


function createCubes() {
    const container = document.getElementById('cubeContainer');
    if (!container) return;
    container.innerHTML = '';
    const cubeCount = 20;
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    for (let i = 0; i < cubeCount; i++) {
        const cube = document.createElement('div');
        cube.className = 'cube';
        cube.innerHTML = `
            <div class="front"></div>
            <div class="back"></div>
            <div class="right"></div>
            <div class="left"></div>
            <div class="top"></div>
            <div class="bottom"></div>
        `;
        
        const x = Math.random() * (viewportWidth - 60);
        const y = Math.random() * (viewportHeight - 60);
        cube.style.left = `${x}px`;
        cube.style.top = `${y}px`;
        
        const duration = 15 + Math.random() * 10;
        cube.style.animationDuration = `${duration}s`;
        
        container.appendChild(cube);
    }
}

// Run immediately, on load, and on resize
createCubes();
window.addEventListener('load', createCubes);
window.addEventListener('resize', createCubes);