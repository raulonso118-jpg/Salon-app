name: Compilar APK Android

on:
  push:
    branches: [ main, master ]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
    - name: Copiar repositorio
      uses: actions/checkout@v4

    - name: Liberar espacio en disco
      run: |
        sudo rm -rf /usr/share/dotnet
        sudo rm -rf /opt/ghc
        sudo rm -rf "/usr/local/share/boost"
        sudo rm -rf "$AGENT_TOOLSDIRECTORY"

    - name: Configurar entorno Python
      uses: actions/setup-python@v5
      with:
        python-version: '3.10'

    - name: Instalar dependencias del sistema
      run: |
        sudo apt-get update
        sudo apt-get install -y \
            git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config \
            zlib1g-dev libncurses5-dev ncurses-dev libsdl2-dev libsdl2-image-dev \
            libsdl2-mixer-dev libsdl2-ttf-dev libffi-dev libssl-dev

    - name: Instalar Buildozer y Cython
      run: |
        pip install --upgrade pip
        pip install --user Cython==0.29.36 buildozer

    - name: Compilar APK con Buildozer
      run: |
        export PATH=$PATH:~/.local/bin
        yes | buildozer -v android debug

    - name: Guardar y subir el archivo APK generado
      uses: actions/upload-artifact@v4
      with:
        name: app-salon-debug
        path: bin/*.apk
