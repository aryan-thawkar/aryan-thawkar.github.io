const container = document.getElementById("project-container");

for (let i = 1; i <= 100; i++) {
    const paddedIndex = i.toString().padStart(2, '0'); // 01 to 100

    const card = document.createElement("div");
    card.classList.add("card");

    const imgDiv = document.createElement("div");
    imgDiv.classList.add("img");
    imgDiv.dataset.index = paddedIndex;
    imgDiv.style.backgroundImage = `url(/Assets/IMGs/${paddedIndex}.png)`;

    imgDiv.addEventListener("mouseenter", function () {
        this.style.backgroundImage = `url(/Assets/GIFs/${this.dataset.index}.gif)`;
    });

    imgDiv.addEventListener("mouseleave", function () {
        this.style.backgroundImage = `url(/Assets/IMGs/${this.dataset.index}.png)`;
    });

    const descriptionDiv = document.createElement("div");
    descriptionDiv.classList.add("description");
    descriptionDiv.innerHTML = `
        <h3>Project ${i}</h3>
        <p>This is a short description of project ${paddedIndex} with hover GIF effect.</p>
    `;

    card.appendChild(imgDiv);
    card.appendChild(descriptionDiv);
    container.appendChild(card);
}
