document.addEventListener('DOMContentLoaded', function() {
    const popupResult = document.getElementById('popupResult');

    async function uploadImage() {
        const fileInput = document.getElementById('fileInput');
        const nameInput = document.getElementById('nameInput');
        const termsCheckbox = document.getElementById('termsCheckbox');
        const file = fileInput.files[0];
        const userName = nameInput.value.trim().replace(/\s+/g, '_');

        
        if (!termsCheckbox.checked) {
            showPopup('Você deve aceitar os Termos de Uso e a Política de Privacidade.', 'error');
            return;
        }

        if (!file || !userName) {
            showPopup('Selecione uma imagem e insira um nome.', 'error');
            return;
        }

        const formData = new FormData();
        const fileExtension = file.name.split('.').pop();
        const renamedFile = new File([file], `${userName}.${fileExtension}`, { type: file.type });
        formData.append('image', renamedFile);

        try {
            const response = await fetch('https://lookid.com.br/upload_image', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();
            if (response.ok) {
                showPopup(`Imagem cadastrada com sucesso: ${data.filename}`, 'success');
            } else {
                showPopup(`Erro: ${data.error}`, 'error');
            }
        } catch (error) {
            showPopup(`Erro: ${error.message}`, 'error');
        }
    }

    function showPopup(message, type) {
        popupResult.textContent = message;

        if (type === 'success') {
            popupResult.classList.add('success');
            popupResult.classList.remove('error');
        } else {
            popupResult.classList.add('error');
            popupResult.classList.remove('success');
        }

        popupResult.classList.remove('hidden');

        popupResult.classList.add('show');

        setTimeout(() => {
            popupResult.classList.remove('show');
            popupResult.classList.add('hidden');
        }, 5000);
    }

    window.uploadImage = uploadImage;
});