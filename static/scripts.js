function openTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.style.display = 'none');
    document.getElementById(tabName).style.display = 'block';
}

function cifrarTexto() {
    const a = parseInt(document.getElementById('numero-a').value);
    const b = parseInt(document.getElementById('numero-b').value);
    const mensaje = document.getElementById('cifrar-input').value.trim();

    if (!validateInputText(mensaje)) {
        return;
    }

    const upperCaseText = mensaje.toUpperCase();

    fetch('/cifrar', {
        method: 'POST', headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }, body: `a=${a}&b=${b}&mensaje=${upperCaseText}`
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('output-container').style.display = 'flex';
            document.getElementById('cifrado-output').innerHTML = data.mensaje_cifrado;
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

function descifrarTexto() {
    const a = parseInt(document.getElementById('numero-a').value);
    const b = parseInt(document.getElementById('numero-b').value);
    const mensajeCifrado = document.getElementById('descifrar-input').value.trim();

    const upperCaseText = mensajeCifrado.toUpperCase();

    fetch('/descifrar', {
        method: 'POST', headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }, body: `a=${a}&b=${b}&mensajeCifrado=${upperCaseText}`
    })
        .then(response => response.json())
        .then(data => {
            document.getElementById('output-container').style.display = 'flex';
            document.getElementById('cifrado-output').innerHTML = data.decrypt_text;
            createPlot(data.frecuencias,"chart-container" );
        })
        .catch(error => {
            console.error('Error:', error);
        });
}


function validateInputText(text) {
    // Validar que el texto tenga al menos 90 palabras
    const words = text.split(/\s+/);
    if (words.length < 90) {
        alert('El texto debe tener al menos 90 palabras.');
        return false;
    }

    // Validar que el texto no tenga números
    if (/\d/.test(text)) {
        alert('El texto no debe contener números.');
        return false;
    }

    return true;
}







