let gravador, mediaRecorder, audioBlob;

    // Lógica para gravação de áudio
    document.getElementById("gravarAudio").addEventListener("click", async function () {
      try {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          alert("Seu navegador não suporta gravação de áudio.");
          return;
        }

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        const audioChunks = [];
        mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
        mediaRecorder.onstop = () => {
          audioBlob = new Blob(audioChunks, { type: "audio/wav" });
          const audioUrl = URL.createObjectURL(audioBlob);
          const audioPreview = new Audio(audioUrl);
          audioPreview.controls = true;
          document.getElementById("statusGravacao").innerText = "Gravação finalizada! Prévia do áudio:";
          document.getElementById("statusGravacao").appendChild(audioPreview);
        };

        mediaRecorder.start();
        document.getElementById("statusGravacao").innerText = "Gravando... Clique novamente para parar.";
        this.innerText = "Parar Gravação";

        this.onclick = () => {
          mediaRecorder.stop();
          this.innerText = "Gravar Áudio";
          this.onclick = null; // Reseta o botão para evitar confusão
        };
      } catch (err) {
        alert("Erro ao acessar o microfone: " + err.message);
      }
    });

    // Lógica para envio do formulário
    document.getElementById("formHistoria").addEventListener("submit", async function (e) {
      e.preventDefault();

      const formData = new FormData(this);
      if (audioBlob) {
        formData.append("audio", audioBlob, "gravacao.wav");
      }

      try {
        const response = await fetch("/enviar_historia", {
          method: "POST",
          body: formData,
        });

        const resultado = await response.json();
        document.getElementById("resultado").innerText = JSON.stringify(resultado, null, 2);
      } catch (error) {
        document.getElementById("resultado").innerText = "Erro ao enviar história: " + error.message;
      }
    });