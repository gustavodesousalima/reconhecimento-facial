const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const context = canvas.getContext('2d');
const userImage = document.getElementById('userImage');
const popupResult = document.getElementById('popupResult');

// Acessar a câmera do usuário
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        video.play();
    })
    .catch(err => {
        console.error('Erro ao acessar a câmera: ', err);
    });

function captureFrame() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    canvas.toBlob(async function(blob) {
        const formData = new FormData();
        formData.append('image', blob, 'captured_image.jpg');

        const loading = document.getElementById('loading'); // Captura o elemento de loading
        loading.classList.add('show'); // Mostra o loading

        try {
            const response = await fetch('https://lookid.com.br/recognize_face', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            loading.classList.remove('show'); // Esconde o loading

            if (data.error) {
                showPopup(`Erro: ${data.error}`, 'error'); // Chama showPopup com tipo 'error'
                userImage.src = ''; // Limpa imagem em caso de erro
            } else if (data.result === 'Rosto identificado') {
                showPopup(`Resultado: ${data.result}, Nome: ${data.name}`, 'success'); // Chama showPopup com tipo 'success'
                userImage.src = data.image_url; // Exibe a imagem encontrada no S3
            } else {
                showPopup(data.result, 'error'); // Chama showPopup com tipo 'error'
                userImage.src = ''; // Limpa imagem em caso de erro
            }
        } catch (error) {
            loading.classList.remove('show'); // Esconde o loading
            showPopup(`Erro: ${error.message}`, 'error'); // Chama showPopup com tipo 'error'
            userImage.src = ''; // Limpa imagem em caso de erro
        }
    }, 'image/jpg');
}

function showPopup(message, type) {
    popupResult.textContent = message;
    popupResult.className = 'popup-result'; // Reseta as classes
    popupResult.classList.add(type); // Adiciona a classe do tipo (success ou error)
    
    console.log(popupResult.className); // Verifica as classes

    popupResult.classList.add('show'); // Mostra o pop-up

    setTimeout(() => {
        popupResult.classList.remove('show'); // Remove a classe 'show' após 5 segundos
        popupResult.classList.remove('success'); // Remove a classe 'success' ao esconder
        popupResult.classList.remove('error'); // Remove a classe 'error' ao esconder
    }, 5000);
}