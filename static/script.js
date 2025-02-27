let selectedCard = null;
let selectedImage = null;

function openModal(button) {
    selectedCard = button.closest(".product-card");

    // Get current product values
    const productIdText = selectedCard.querySelector(".product-id").textContent;
    const productId = productIdText.replace("Product ID: ", "");
    const productName = selectedCard.querySelector("h2").textContent;
    const productBrand = selectedCard.querySelector(".brand").textContent;
    const productPrice = selectedCard.querySelector(".price").textContent.replace("Price: P ", "");
    const productDescription = selectedCard.querySelector(".description").textContent;
    const isAvailable = selectedCard.querySelector(".status").classList.contains("available") ? "available" : "out-of-stock";
    const productImage = selectedCard.querySelector(".image-container img").src;

    // Set values in the modal
    document.getElementById("productId").value = productId;
    document.getElementById("productName").value = productName;
    document.getElementById("productBrand").value = productBrand;
    document.getElementById("productPrice").value = productPrice;
    document.getElementById("productDescription").value = productDescription;
    document.getElementById("productAvailability").value = isAvailable;
    document.getElementById("previewImg").src = productImage;

    // Reset file input
    document.getElementById("imageUpload").value = "";
    selectedImage = null;

    // Show modal
    document.getElementById("editModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("editModal").style.display = "none";
}

function confirmChanges() {
    if (!selectedCard) return;

    // Update product information
    const newProductId = document.getElementById("productId").value;
    const newProductName = document.getElementById("productName").value;
    const newProductBrand = document.getElementById("productBrand").value;
    const newProductPrice = document.getElementById("productPrice").value;
    const newProductDescription = document.getElementById("productDescription").value;
    const newStatus = document.getElementById("productAvailability").value;

    // Update card elements
    selectedCard.querySelector(".product-id").textContent = `Product ID: ${newProductId}`;
    selectedCard.querySelector("h2").textContent = newProductName;
    selectedCard.querySelector(".brand").textContent = newProductBrand;
    selectedCard.querySelector(".price").textContent = `Price: P ${newProductPrice}`;
    selectedCard.querySelector(".description").textContent = newProductDescription;

    // Update status
    const statusDiv = selectedCard.querySelector(".status");
    statusDiv.textContent = newStatus === "available" ? "Available" : "Out of Stock";
    statusDiv.className = `status ${newStatus}`;

    // Update image if a new one was selected
    if (selectedImage) {
        selectedCard.querySelector(".image-container img").src = selectedImage;
    }

    // Close modal
    closeModal();
}


function removeAllProducts() {
    document.querySelector(".product-grid").innerHTML = "";
}


// Handle image preview
document.addEventListener("DOMContentLoaded", function () {
    const imageUpload = document.getElementById("imageUpload");
    const previewImg = document.getElementById("previewImg");

    imageUpload.addEventListener("change", function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();

            reader.addEventListener("load", function () {
                previewImg.src = this.result;
                selectedImage = this.result;
            });

            reader.readAsDataURL(file);
        }
    });
});

let selectedImageForNewProduct = null;

function openAddProductModal() {
    document.getElementById("addProductModal").style.display = "flex";
    document.getElementById("newProductForm").reset();
    document.getElementById("newPreviewImg").src = "";
    selectedImageForNewProduct = null;
}

function closeAddProductModal() {
    document.getElementById("addProductModal").style.display = "none";
}

function addProduct() {
    const productId = document.getElementById("newProductId").value;
    const productName = document.getElementById("newProductName").value;
    const productBrand = document.getElementById("newProductBrand").value;
    const productPrice = parseFloat(document.getElementById("newProductPrice").value) || 0;
    const productDescription = document.getElementById("newProductDescription").value;
    const isAvailable = document.getElementById("newProductAvailability").value;
    const productImage = selectedImageForNewProduct || "default-image.jpg"; // Fallback image

    if (!productName || !productBrand || productPrice <= 0) {
        alert("Please fill in all required fields correctly.");
        return;
    }

    const productGrid = document.querySelector(".product-grid");

    // Create product card
    const productCard = document.createElement("div");
    productCard.classList.add("product-card");
    productCard.innerHTML = `
        <div class="image-container">
            <img src="${productImage}" alt="${productName}">
        </div>
        <p class="product-id">Product ID: ${productId}</p>
        <h2>${productName}</h2>
        <p class="brand">${productBrand}</p>
        <p class="price">Price: P ${productPrice.toFixed(2)}</p>
        <p class="description">${productDescription}</p>
        <p class="status ${isAvailable}">${isAvailable === "available" ? "Available" : "Out of Stock"}</p>
        <button onclick="openModal(this)">Edit</button>
        <button class="remove-btn" onclick="removeProduct(this)">Remove</button>
    `;

    productGrid.appendChild(productCard);

    closeAddProductModal();
}

// Handle image preview for new product
document.addEventListener("DOMContentLoaded", function () {
    const newImageUpload = document.getElementById("newImageUpload");
    const newPreviewImg = document.getElementById("newPreviewImg");

    newImageUpload.addEventListener("change", function () {
        const file = this.files[0];
        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = function () {
                newPreviewImg.src = this.result;
                selectedImageForNewProduct = this.result;
            };
            reader.readAsDataURL(file);
        } else {
            alert("Please select a valid image file.");
            this.value = "";
        }
    });
});
// Remove the duplicate removeProduct function and keep only one
function removeProduct(button) {
    const productCard = button.closest(".product-card");
    const productName = productCard.querySelector("h2").textContent;

    // Show confirmation alert
    const confirmDelete = confirm(`Are you sure you want to remove "${productName}"?`);
    if (confirmDelete) {
        productCard.remove();
    }
}
 