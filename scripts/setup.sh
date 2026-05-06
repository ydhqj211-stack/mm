#!/bin/bash
set -e

echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    git \
    wget \
    unzip \
    openjdk-11-jdk

echo "Installing Python dependencies..."
pip3 install --upgrade pip
pip3 install buildozer

echo "Setting up Android SDK..."
if [ ! -d "$HOME/android-sdk" ]; then
    mkdir -p $HOME/android-sdk/cmdline-tools
    cd $HOME/android-sdk/cmdline-tools
    wget -q https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O cmdline-tools.zip
    unzip -q cmdline-tools.zip
    mv cmdline-tools latest
    rm cmdline-tools.zip
fi

export ANDROID_SDK_ROOT=$HOME/android-sdk
export PATH=$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools

echo "Accepting Android SDK licenses..."
yes | sdkmanager --licenses 2>/dev/null || true

echo "Installing Android SDK components..."
sdkmanager "platform-tools" "platforms;android-30" "build-tools;30.0.3" "ndk;21e"

echo "Setting environment variables..."
echo "ANDROID_SDK_ROOT=$HOME/android-sdk" >> ~/.bashrc
echo "ANDROID_NDK_ROOT=$HOME/android-sdk/ndk/21e" >> ~/.bashrc
echo "export PATH=\$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin:$ANDROID_SDK_ROOT/platform-tools" >> ~/.bashrc

echo "Setup complete!"
echo ""
echo "To build the APK, run:"
echo "  buildozer android debug"