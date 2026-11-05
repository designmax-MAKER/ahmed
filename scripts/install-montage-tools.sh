#!/usr/bin/env bash
# تثبيت أدوات المونتاج على Mac أو Linux
# الأدوات: FFmpeg (مونتاج من الترمنال) + Kdenlive + Shotcut (برامج مونتاج) + Audacity (تعديل الصوت)
set -euo pipefail

OS="$(uname -s)"
echo "==> تثبيت أدوات المونتاج على: $OS"

if [ "$OS" = "Darwin" ]; then
  if ! command -v brew >/dev/null 2>&1; then
    echo "==> Homebrew مش موجود، جاري تثبيته..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    eval "$(/opt/homebrew/bin/brew shellenv 2>/dev/null || /usr/local/bin/brew shellenv)"
  fi
  brew install ffmpeg
  brew install --cask kdenlive shotcut audacity

elif [ "$OS" = "Linux" ]; then
  SUDO=""
  [ "$(id -u)" -ne 0 ] && SUDO="sudo"

  if command -v apt-get >/dev/null 2>&1; then
    $SUDO apt-get update
    $SUDO apt-get install -y ffmpeg kdenlive shotcut audacity
  elif command -v dnf >/dev/null 2>&1; then
    # FFmpeg الكامل على Fedora محتاج مستودع RPM Fusion
    $SUDO dnf install -y \
      "https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm" || true
    $SUDO dnf install -y --allowerasing ffmpeg kdenlive shotcut audacity
  elif command -v pacman >/dev/null 2>&1; then
    $SUDO pacman -Sy --noconfirm ffmpeg kdenlive shotcut audacity
  else
    echo "مدير الحزم مش معروف. ثبّت ffmpeg و kdenlive و shotcut و audacity يدويًا." >&2
    exit 1
  fi

else
  echo "نظام غير مدعوم: $OS (على Windows استخدم scripts/install-montage-tools.ps1)" >&2
  exit 1
fi

echo
echo "==> تم التثبيت. التأكد من FFmpeg:"
ffmpeg -version | head -n 1
