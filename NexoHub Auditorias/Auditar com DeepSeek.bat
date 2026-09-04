@echo off
chcp 65001 >nul
title NexoHub Auditorias - DeepSeek
cd /d "%~dp0"

rem A chave fica fora do repositorio (este repo e publico).
if not exist "chave_deepseek.txt" (
  echo.
  echo   Falta o arquivo chave_deepseek.txt nesta pasta.
  echo   Crie um arquivo de texto com a chave da API DeepSeek numa linha so.
  echo.
  pause
  exit /b 1
)
set /p DS_KEY=<chave_deepseek.txt

set "ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic"
set "ANTHROPIC_AUTH_TOKEN=%DS_KEY%"
set "ANTHROPIC_DEFAULT_OPUS_MODEL=deepseek-v4-pro"
set "ANTHROPIC_DEFAULT_SONNET_MODEL=deepseek-v4-pro"
set "ANTHROPIC_DEFAULT_HAIKU_MODEL=deepseek-v4-flash"
set "CLAUDE_CODE_SUBAGENT_MODEL=deepseek-v4-flash"
set "DS_KEY="

claude
