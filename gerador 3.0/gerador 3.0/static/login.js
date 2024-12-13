const form = document.getElementById('login-form');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const successMessage = document.getElementById('success-message');

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let isValid = true;

      // Validação do E-mail
      const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailPattern.test(emailInput.value)) {
        document.getElementById('email-error').style.display = 'block';
        isValid = false;
      } else {
        document.getElementById('email-error').style.display = 'none';
      }

      // Validação da Senha
      if (passwordInput.value.trim() === '') {
        document.getElementById('password-error').style.display = 'block';
        isValid = false;
      } else {
        document.getElementById('password-error').style.display = 'none';
      }

      // Exibir mensagem de sucesso
      if (isValid) {
        successMessage.textContent = 'Login realizado com sucesso!';
        form.reset();
      } else {
        successMessage.textContent = '';
      }
    });