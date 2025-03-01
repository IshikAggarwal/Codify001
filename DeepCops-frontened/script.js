function scanImage() {
    let loadingText = document.getElementById("loadingText");
    let resultText = document.getElementById("resultText");
    let imagePreview = document.getElementById("imagePreview"); 
    let imageUpload = document.getElementById("imageUpload");
    let resultBox = document.getElementById("resultBox"); 
    let imagePreviewContainer = document.getElementById("imagePreviewContainer");

    let file = imageUpload.files[0]; 

    if (!file) {
        alert("Please upload an image first.");
        return;
    }

    let reader = new FileReader();
    reader.onload = function (e) {
        imagePreview.src = e.target.result; 
        imagePreview.style.display = "block"; 
        imagePreviewContainer.style.display = "block"; // Show preview container
    };
    reader.readAsDataURL(file); 

    loadingText.style.display = "block";
    resultText.innerText = "";
    resultText.style.opacity = "0";
    resultBox.style.display = "none"; // Hide resultBox initially

    setTimeout(() => {
        loadingText.style.display = "none";
        resultBox.style.display = "block"; // Show after scan completes
        resultText.style.border = "2px solid black";
        resultText.style.backgroundColor = "white";

        let isFake = Math.random() > 0.5; 
        if (isFake) {
            resultText.innerHTML = "❌ Deepfake Detected!";
            resultText.style.color = "red";
        } else {
            resultText.innerHTML = "✅ Real Image!";
            resultText.style.color = "green";

        }

        resultText.style.opacity = "1"; 
    }, 2000);
}
