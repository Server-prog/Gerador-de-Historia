    const form = document.getElementById('registration-form');
    const nameInput = document.getElementById('name');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const successMessage = document.getElementById('success-message');

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let isValid = true;

      // Validação do Nome
      if (nameInput.value.trim() === '') {
        document.getElementById('name-error').style.display = 'block';
        isValid = false;
      } else {
        document.getElementById('name-error').style.display = 'none';
      }

      // Validação do E-mail
      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailPattern.test(emailInput.value)) {
        document.getElementById('email-error').style.display = 'block';
        isValid = false;
      } else {
        document.getElementById('email-error').style.display = 'none';
      }

      // Validação da Senha
      if (passwordInput.value.length < 6) {
        document.getElementById('password-error').style.display = 'block';
        isValid = false;
      } else {
        document.getElementById('password-error').style.display = 'none';
      }

      // Validação da Confirmação de Senha
      if (passwordInput.value !== confirmPasswordInput.value) {
        document.getElementById('confirm-password-error').style.display = 'block';
        isValid = false;
      } else {
        document.getElementById('confirm-password-error').style.display = 'none';
      }

      // Exibir mensagem de sucesso
      if (isValid) {
        successMessage.textContent = 'Cadastro realizado com sucesso!';
        form.reset();
      } else {
        successMessage.textContent = '';
      }
    });
  