document.addEventListener("DOMContentLoaded", () => {
    const coverImageInput = document.getElementById("coverImage");
    const coverPreview = document.getElementById("coverPreview");
    const form = document.getElementById("interactiveStoryForm");
  
    // Pré-visualização da imagem
    coverImageInput.addEventListener("change", (event) => {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = () => {
          coverPreview.innerHTML = `<img src="${reader.result}" alt="Imagem de Capa" style="max-height: 100%; max-width: 100%;"/>`;
        };
        reader.readAsDataURL(file);
      } else {
        coverPreview.innerHTML = "Pré-visualização da Imagem";
      }
    });
  
    // Validação do formulário
    form.addEventListener("submit", (event) => {
      const title = document.getElementById("storyTitle").value.trim();
      const description = document.getElementById("storyDescription").value.trim();
  
      if (!title || !description) {
        alert("Por favor, preencha todos os campos obrigatórios!");
        event.preventDefault();
      } else {
        alert("Sua história foi criada com sucesso!");
      }
    });
  });
  