# Guia de Instalação do BloxRS no R35S

Siga estes passos simples para rodar o jogo no seu console portátil R35S (ArkOS / PortMaster):

---

### Passo 1: Gerar o arquivo `.pck` no PC
1. Abra o **Godot 3.5** no seu computador.
2. Importe o projeto da pasta `godot_project/` (selecione o arquivo `project.godot`).
3. Vá em **Project -> Export...**.
4. Selecione o preset **Linux/X11**.
5. Clique no botão **Export PCK/Zip...** na parte inferior da janela.
6. Salve o arquivo com o nome: `bloxrs.pck` dentro da pasta `r35s_package/bloxrs/`.

---

### Passo 2: Obter o Runtime `frt_3.5.2` (Godot ARM64)
O R35S precisa do executável `frt_3.5.2` (motor Godot compilado para processador ARM64 do R35S).
* Você pode pegá-lo pronto em qualquer jogo Godot que já esteja instalado na pasta `ports/` do seu R35S, **OU**
* Baixar diretamente pelo repositório oficial do PortMaster:
  [PortMaster FRT Releases](https://github.com/efornara/frt/releases) (escolha a versão `frt_3.5.2` para `arm64`).
* Coloque o arquivo `frt_3.5.2` dentro de `r35s_package/bloxrs/`.

---

### Passo 3: Copiar para o Cartão SD do R35S
Insira o cartão SD de jogos (TF2/EASYROMS) no PC:
1. Copie o arquivo `BloxRS.sh` para a pasta:
   `/roms/ports/` (ou `/roms2/ports/`)
2. Copie a pasta inteira `bloxrs/` para dentro de:
   `/roms/ports/` (ou `/roms2/ports/`)

A estrutura final no seu cartão SD deve ficar assim:
```text
roms/
 └── ports/
      ├── BloxRS.sh
      └── bloxrs/
           ├── bloxrs.pck
           ├── frt_3.5.2
           └── log.txt
```

---

### Passo 4: Jogar!
1. Coloque o cartão de volta no seu R35S e ligue o console.
2. Vá até a seção **PORTS** no menu principal do ArkOS.
3. Selecione **BloxRS**.
4. O jogo vai abrir em 640x480 cravado a 60 FPS com os dois analógicos funcionando!

* **Analógico Esquerdo / D-Pad:** Anda
* **Analógico Direito:** Gira a câmera em 360°
* **Botão A / B:** Pula
* **Botão Select / Start:** Sai do jogo
